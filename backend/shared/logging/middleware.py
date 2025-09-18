"""
Logging middleware for FastAPI applications.
"""

import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .logger import get_logger
from .correlation import correlation_manager

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging with correlation IDs."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and response with logging."""
        start_time = time.time()
        
        # Start correlation ID tracking
        correlation_id = correlation_manager.start_request(request)
        
        # Log request
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra_data={
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "headers": dict(request.headers),
                "client_ip": request.client.host if request.client else None,
                "type": "request_start"
            }
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.log_api_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration
            )
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Request-ID"] = correlation_id
            
            return response
            
        except Exception as e:
            # Calculate duration for error case
            duration = time.time() - start_time
            
            # Log error
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra_data={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration * 1000,
                    "error": str(e),
                    "type": "request_error"
                }
            )
            
            raise
        
        finally:
            # Clear correlation context
            correlation_manager.clear_context()


class DatabaseLoggingMixin:
    """Mixin for logging database operations."""
    
    def log_query(self, query: str, duration: float):
        """Log database query execution."""
        logger.log_database_query(query, duration)
    
    def log_transaction(self, operation: str, table: str, duration: float):
        """Log database transaction."""
        logger.info(
            f"Database transaction: {operation} on {table}",
            extra_data={
                "operation": operation,
                "table": table,
                "duration_ms": duration * 1000,
                "type": "database_transaction"
            }
        )


class BusinessEventLogger:
    """Logger for business events and analytics."""
    
    def __init__(self):
        self.logger = get_logger("business_events")
    
    def log_user_action(self, user_id: str, action: str, resource: str, 
                       tenant_id: str = None, extra_data: dict = None):
        """Log user business actions."""
        self.logger.log_business_event(
            event="user_action",
            resource=resource,
            action=action,
            user_id=user_id,
            tenant_id=tenant_id,
            extra_data=extra_data
        )
    
    def log_system_event(self, event: str, description: str, extra_data: dict = None):
        """Log system events."""
        self.logger.log_business_event(
            event="system_event",
            resource="system",
            action=event,
            extra_data={
                "description": description,
                **(extra_data or {})
            }
        )
    
    def log_ai_interaction(self, user_id: str, query: str, response_type: str,
                          duration: float, tenant_id: str = None):
        """Log AI chat interactions."""
        self.logger.log_business_event(
            event="ai_interaction",
            resource="ai_chat",
            action="query",
            user_id=user_id,
            tenant_id=tenant_id,
            extra_data={
                "query_length": len(query),
                "response_type": response_type,
                "duration_ms": duration * 1000
            }
        )


# Global business event logger
business_logger = BusinessEventLogger()