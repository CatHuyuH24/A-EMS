"""
Database connection management and pooling utilities.
"""

import asyncio
import logging
from contextlib import contextmanager
from typing import Generator, Optional
import psycopg2
from psycopg2 import pool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import os

logger = logging.getLogger(__name__)

class DatabaseConnectionManager:
    """Database connection manager with pooling support."""
    
    def __init__(self):
        self.connection_pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool."""
        try:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise ValueError("DATABASE_URL environment variable not set")
            
            # Parse connection parameters
            connection_params = self._parse_database_url(database_url)
            
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=20,
                **connection_params
            )
            logger.info("Database connection pool initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise
    
    def _parse_database_url(self, url: str) -> dict:
        """Parse database URL into connection parameters."""
        # Simple URL parsing (in production, use urllib.parse)
        # Format: postgresql://user:password@host:port/database
        url = url.replace("postgresql://", "")
        auth_part, host_part = url.split("@")
        user, password = auth_part.split(":")
        host_db_part = host_part.split("/")
        host_port = host_db_part[0]
        database = host_db_part[1]
        
        if ":" in host_port:
            host, port = host_port.split(":")
        else:
            host, port = host_port, "5432"
        
        return {
            "user": user,
            "password": password,
            "host": host,
            "port": int(port),
            "database": database
        }
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool."""
        connection = None
        try:
            connection = self.connection_pool.getconn()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    def close_all_connections(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("All database connections closed")


# Global connection manager instance
connection_manager = DatabaseConnectionManager()


def test_database_connection() -> bool:
    """Test database connectivity."""
    try:
        from .base import engine
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


async def health_check() -> dict:
    """Perform database health check."""
    try:
        is_connected = test_database_connection()
        return {
            "database": {
                "status": "healthy" if is_connected else "unhealthy",
                "connected": is_connected
            }
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "database": {
                "status": "unhealthy",
                "connected": False,
                "error": str(e)
            }
        }