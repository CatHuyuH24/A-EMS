"""
Structured logging utilities for A-EMS microservices.
"""

import logging
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import os
import sys


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add correlation ID if available
        if hasattr(record, 'correlation_id'):
            log_entry["correlation_id"] = record.correlation_id
        
        # Add user context if available
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        
        if hasattr(record, 'tenant_id'):
            log_entry["tenant_id"] = record.tenant_id
        
        # Add service context
        log_entry["service"] = os.getenv("SERVICE_NAME", "unknown")
        log_entry["version"] = os.getenv("SERVICE_VERSION", "dev")
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add any extra fields
        if hasattr(record, 'extra_data'):
            log_entry["extra"] = record.extra_data
        
        return json.dumps(log_entry)


class CorrelationFilter(logging.Filter):
    """Filter to add correlation ID to log records."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add correlation ID to record if not present."""
        if not hasattr(record, 'correlation_id'):
            record.correlation_id = getattr(self, '_correlation_id', str(uuid.uuid4()))
        return True


class AEMSLogger:
    """Enhanced logger for A-EMS services."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.correlation_id: Optional[str] = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger configuration."""
        # Set log level from environment
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.logger.setLevel(getattr(logging, log_level))
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JSONFormatter())
        console_handler.addFilter(CorrelationFilter())
        self.logger.addHandler(console_handler)
        
        # File handler for production
        if os.getenv("ENVIRONMENT") == "production":
            file_handler = logging.FileHandler("/var/log/aems/application.log")
            file_handler.setFormatter(JSONFormatter())
            file_handler.addFilter(CorrelationFilter())
            self.logger.addHandler(file_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def set_correlation_id(self, correlation_id: str):
        """Set correlation ID for current context."""
        self.correlation_id = correlation_id
        # Update filter
        for handler in self.logger.handlers:
            for filter_obj in handler.filters:
                if isinstance(filter_obj, CorrelationFilter):
                    filter_obj._correlation_id = correlation_id
    
    def _log(self, level: int, message: str, extra_data: Optional[Dict[str, Any]] = None, 
             user_id: Optional[str] = None, tenant_id: Optional[str] = None):
        """Internal logging method."""
        extra = {
            'correlation_id': self.correlation_id,
            'extra_data': extra_data or {},
            'user_id': user_id,
            'tenant_id': tenant_id
        }
        
        self.logger.log(level, message, extra=extra)
    
    def debug(self, message: str, extra_data: Optional[Dict[str, Any]] = None, 
              user_id: Optional[str] = None, tenant_id: Optional[str] = None):
        """Log debug message."""
        self._log(logging.DEBUG, message, extra_data, user_id, tenant_id)
    
    def info(self, message: str, extra_data: Optional[Dict[str, Any]] = None,
             user_id: Optional[str] = None, tenant_id: Optional[str] = None):
        """Log info message."""
        self._log(logging.INFO, message, extra_data, user_id, tenant_id)
    
    def warning(self, message: str, extra_data: Optional[Dict[str, Any]] = None,
                user_id: Optional[str] = None, tenant_id: Optional[str] = None):
        """Log warning message."""
        self._log(logging.WARNING, message, extra_data, user_id, tenant_id)
    
    def error(self, message: str, extra_data: Optional[Dict[str, Any]] = None,
              user_id: Optional[str] = None, tenant_id: Optional[str] = None):
        """Log error message."""
        self._log(logging.ERROR, message, extra_data, user_id, tenant_id)
    
    def critical(self, message: str, extra_data: Optional[Dict[str, Any]] = None,
                 user_id: Optional[str] = None, tenant_id: Optional[str] = None):
        """Log critical message."""
        self._log(logging.CRITICAL, message, extra_data, user_id, tenant_id)
    
    def log_api_request(self, method: str, path: str, status_code: int, 
                       duration: float, user_id: Optional[str] = None,
                       tenant_id: Optional[str] = None):
        """Log API request details."""
        extra_data = {
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration * 1000,
            "type": "api_request"
        }
        self.info(f"{method} {path} - {status_code} ({duration:.3f}s)", 
                 extra_data, user_id, tenant_id)
    
    def log_database_query(self, query: str, duration: float, 
                          user_id: Optional[str] = None, tenant_id: Optional[str] = None):
        """Log database query performance."""
        extra_data = {
            "query": query[:200],  # Truncate long queries
            "duration_ms": duration * 1000,
            "type": "database_query"
        }
        self.debug(f"Database query executed ({duration:.3f}s)", 
                  extra_data, user_id, tenant_id)
    
    def log_auth_event(self, event: str, user_email: str, success: bool,
                      ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """Log authentication events."""
        extra_data = {
            "event": event,
            "user_email": user_email,
            "success": success,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "type": "auth_event"
        }
        level = logging.INFO if success else logging.WARNING
        message = f"Auth event: {event} for {user_email} - {'Success' if success else 'Failed'}"
        self._log(level, message, extra_data)
    
    def log_business_event(self, event: str, resource: str, action: str,
                          user_id: Optional[str] = None, tenant_id: Optional[str] = None,
                          extra_data: Optional[Dict[str, Any]] = None):
        """Log business events for analytics."""
        event_data = {
            "event": event,
            "resource": resource,
            "action": action,
            "type": "business_event"
        }
        if extra_data:
            event_data.update(extra_data)
        
        message = f"Business event: {event} - {action} on {resource}"
        self.info(message, event_data, user_id, tenant_id)


def get_logger(name: str) -> AEMSLogger:
    """Get logger instance for a module."""
    return AEMSLogger(name)


# Module-level logger
logger = get_logger(__name__)