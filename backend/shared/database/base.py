"""
Base database classes and utilities for A-EMS microservices.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from typing import Generator

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://aems_user:aems_password@localhost:5432/aems_db"
)

# SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Metadata for schema management
metadata = MetaData()


class DatabaseBase:
    """Base class for database operations."""
    
    def __init__(self):
        self.db = None
    
    def get_db(self) -> Generator:
        """Get database session."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def create_all_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=engine)
    
    def drop_all_tables(self):
        """Drop all tables."""
        Base.metadata.drop_all(bind=engine)


# Database dependency for FastAPI
def get_database() -> Generator:
    """Database dependency for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()