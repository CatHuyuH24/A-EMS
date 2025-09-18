"""
Authentication service main application.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys
import os

# Add parent directory to path for shared imports
sys.path.append('../../')
from shared.logging.logger import get_logger
from shared.logging.middleware import LoggingMiddleware
from shared.middleware import add_middleware
from shared.database.base import DatabaseBase
from .api import auth_router
from .core.config import get_settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Auth Service starting up")
    
    # Initialize database
    db_manager = DatabaseBase()
    try:
        db_manager.create_all_tables()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    yield
    
    logger.info("Auth Service shutting down")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="A-EMS Authentication Service",
        description="Authentication and authorization service for A-EMS",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan
    )
    
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Add shared middleware
    add_middleware(app, {
        "excluded_paths": ["/health", "/docs", "/redoc", "/openapi.json"]
    })
    
    # Include API routes
    app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
    
    return app


# Create app instance
app = create_app()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "auth-service",
        "version": "1.0.0"
    }