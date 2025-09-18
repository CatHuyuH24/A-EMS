"""
Shared middleware for A-EMS microservices.
"""

import time
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..logging.logger import get_logger
from ..logging.correlation import correlation_manager

logger = get_logger(__name__)


class CORSMiddleware(BaseHTTPMiddleware):
    """Custom CORS middleware."""
    
    def __init__(self, app, allowed_origins: list = None, allowed_methods: list = None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or ["*"]
        self.allowed_methods = allowed_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle CORS headers."""
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allowed_methods)
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Correlation-ID"
            return response
        
        response = await call_next(request)
        
        # Add CORS headers to response
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allowed_methods)
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Correlation-ID"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware."""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.client_requests = {}  # In production, use Redis
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Apply rate limiting."""
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old entries
        minute_ago = current_time - 60
        self.client_requests = {
            ip: [req_time for req_time in times if req_time > minute_ago]
            for ip, times in self.client_requests.items()
        }
        
        # Check current client rate
        client_times = self.client_requests.get(client_ip, [])
        
        if len(client_times) >= self.requests_per_minute:
            logger.warning(
                f"Rate limit exceeded for IP: {client_ip}",
                extra_data={
                    "client_ip": client_ip,
                    "requests_count": len(client_times),
                    "limit": self.requests_per_minute,
                    "type": "rate_limit_exceeded"
                }
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Limit: {self.requests_per_minute} per minute"
                }
            )
        
        # Record request
        client_times.append(current_time)
        self.client_requests[client_ip] = client_times
        
        return await call_next(request)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for protected routes."""
    
    def __init__(self, app, excluded_paths: list = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/health", "/docs", "/openapi.json"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate authentication for protected routes."""
        # Skip authentication for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)
        
        # Skip authentication for OPTIONS requests
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Get authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning(
                f"Missing or invalid authorization header for {request.url.path}",
                extra_data={
                    "path": request.url.path,
                    "method": request.method,
                    "type": "auth_missing"
                }
            )
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Authentication required",
                    "message": "Valid authorization token required"
                }
            )
        
        try:
            # Extract token
            token = auth_header.split(" ")[1]
            
            # Validate token (implement token validation logic)
            # For now, we'll add the token to request state
            request.state.token = token
            
            return await call_next(request)
            
        except Exception as e:
            logger.error(
                f"Authentication error: {str(e)}",
                extra_data={
                    "path": request.url.path,
                    "error": str(e),
                    "type": "auth_error"
                }
            )
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Authentication failed",
                    "message": "Invalid or expired token"
                }
            )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle and log errors."""
        try:
            return await call_next(request)
            
        except HTTPException as e:
            # Log HTTP exceptions
            logger.warning(
                f"HTTP exception: {e.status_code} - {e.detail}",
                extra_data={
                    "status_code": e.status_code,
                    "detail": e.detail,
                    "path": request.url.path,
                    "type": "http_exception"
                }
            )
            raise
            
        except Exception as e:
            # Log unexpected errors
            logger.error(
                f"Unexpected error: {str(e)}",
                extra_data={
                    "error": str(e),
                    "path": request.url.path,
                    "method": request.method,
                    "type": "unexpected_error"
                }
            )
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred",
                    "correlation_id": correlation_manager.get_current_id()
                }
            )


def add_middleware(app, config: dict = None):
    """Add all middleware to FastAPI app."""
    config = config or {}
    
    # Add error handling middleware (outermost)
    app.add_middleware(ErrorHandlingMiddleware)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allowed_origins=config.get("allowed_origins", ["*"]),
        allowed_methods=config.get("allowed_methods", ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    )
    
    # Add rate limiting middleware
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=config.get("rate_limit", 60)
    )
    
    # Add authentication middleware
    app.add_middleware(
        AuthenticationMiddleware,
        excluded_paths=config.get("excluded_paths", ["/health", "/docs", "/openapi.json"])
    )