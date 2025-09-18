"""
Correlation ID utilities for distributed tracing.
"""

import uuid
import contextvars
from typing import Optional
from fastapi import Request


# Context variable for correlation ID
correlation_id_context: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    'correlation_id', default=None
)


def generate_correlation_id() -> str:
    """Generate a new correlation ID."""
    return str(uuid.uuid4())


def get_correlation_id() -> Optional[str]:
    """Get current correlation ID from context."""
    return correlation_id_context.get()


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation ID in current context."""
    correlation_id_context.set(correlation_id)


def extract_correlation_id_from_request(request: Request) -> str:
    """Extract or generate correlation ID from HTTP request."""
    # Try to get from X-Correlation-ID header
    correlation_id = request.headers.get("X-Correlation-ID")
    
    # Try alternative headers
    if not correlation_id:
        correlation_id = request.headers.get("X-Request-ID")
    
    if not correlation_id:
        correlation_id = request.headers.get("X-Trace-ID")
    
    # Generate new one if not found
    if not correlation_id:
        correlation_id = generate_correlation_id()
    
    return correlation_id


def add_correlation_id_to_response_headers(correlation_id: str) -> dict:
    """Generate response headers with correlation ID."""
    return {
        "X-Correlation-ID": correlation_id,
        "X-Request-ID": correlation_id
    }


class CorrelationIDManager:
    """Manager for correlation ID context."""
    
    def __init__(self):
        self.current_id: Optional[str] = None
    
    def start_request(self, request: Request) -> str:
        """Start request processing with correlation ID."""
        correlation_id = extract_correlation_id_from_request(request)
        set_correlation_id(correlation_id)
        self.current_id = correlation_id
        return correlation_id
    
    def get_current_id(self) -> Optional[str]:
        """Get current correlation ID."""
        return get_correlation_id() or self.current_id
    
    def clear_context(self) -> None:
        """Clear correlation ID context."""
        set_correlation_id(None)
        self.current_id = None


# Global correlation ID manager
correlation_manager = CorrelationIDManager()