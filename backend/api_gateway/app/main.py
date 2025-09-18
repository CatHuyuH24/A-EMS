"""
API Gateway main application for A-EMS microservices.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx
import os
from typing import Dict
import logging

# Import shared utilities
import sys
sys.path.append('..')
from shared.logging.logger import get_logger
from shared.logging.middleware import LoggingMiddleware
from shared.middleware import add_middleware
from .routing import setup_routes
from .config import get_settings

# Initialize logger
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("API Gateway starting up")
    
    # Initialize HTTP client for service communication
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
    )
    
    yield
    
    # Cleanup
    await app.state.http_client.aclose()
    logger.info("API Gateway shutting down")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="A-EMS API Gateway",
        description="API Gateway for A-EMS microservices",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Add shared middleware
    add_middleware(app, {
        "allowed_origins": settings.allowed_origins,
        "rate_limit": settings.rate_limit_per_minute,
        "excluded_paths": [
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]
    })
    
    # Setup routes
    setup_routes(app)
    
    return app


# Create app instance
app = create_app()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0"
    }