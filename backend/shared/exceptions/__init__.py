"""
Custom exception classes for A-EMS applications.
"""

from typing import Any, Dict, Optional


class AEMSException(Exception):
    """Base exception class for A-EMS applications."""
    
    def __init__(self, message: str, code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.code = code or "AEMS_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(AEMSException):
    """Authentication-related errors."""
    
    def __init__(self, message: str = "Authentication failed", details: Dict[str, Any] = None):
        super().__init__(message, "AUTH_ERROR", details)


class AuthorizationError(AEMSException):
    """Authorization-related errors."""
    
    def __init__(self, message: str = "Access denied", details: Dict[str, Any] = None):
        super().__init__(message, "AUTHZ_ERROR", details)


class ValidationError(AEMSException):
    """Data validation errors."""
    
    def __init__(self, message: str = "Validation failed", field: str = None, details: Dict[str, Any] = None):
        error_details = details or {}
        if field:
            error_details["field"] = field
        super().__init__(message, "VALIDATION_ERROR", error_details)


class DatabaseError(AEMSException):
    """Database operation errors."""
    
    def __init__(self, message: str = "Database operation failed", details: Dict[str, Any] = None):
        super().__init__(message, "DB_ERROR", details)


class BusinessLogicError(AEMSException):
    """Business logic validation errors."""
    
    def __init__(self, message: str, rule: str = None, details: Dict[str, Any] = None):
        error_details = details or {}
        if rule:
            error_details["rule"] = rule
        super().__init__(message, "BUSINESS_ERROR", error_details)


class ExternalServiceError(AEMSException):
    """External service integration errors."""
    
    def __init__(self, message: str, service: str = None, details: Dict[str, Any] = None):
        error_details = details or {}
        if service:
            error_details["service"] = service
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", error_details)


class AIServiceError(ExternalServiceError):
    """AI service specific errors."""
    
    def __init__(self, message: str = "AI service error", details: Dict[str, Any] = None):
        super().__init__(message, "deepseek_ai", details)


class RateLimitError(AEMSException):
    """Rate limiting errors."""
    
    def __init__(self, message: str = "Rate limit exceeded", limit: int = None, details: Dict[str, Any] = None):
        error_details = details or {}
        if limit:
            error_details["limit"] = limit
        super().__init__(message, "RATE_LIMIT_ERROR", error_details)


class ConfigurationError(AEMSException):
    """Configuration errors."""
    
    def __init__(self, message: str = "Configuration error", config_key: str = None, details: Dict[str, Any] = None):
        error_details = details or {}
        if config_key:
            error_details["config_key"] = config_key
        super().__init__(message, "CONFIG_ERROR", error_details)


class NotFoundError(AEMSException):
    """Resource not found errors."""
    
    def __init__(self, resource: str = "Resource", resource_id: str = None, details: Dict[str, Any] = None):
        message = f"{resource} not found"
        error_details = details or {}
        error_details["resource"] = resource
        if resource_id:
            error_details["resource_id"] = resource_id
            message = f"{resource} with ID {resource_id} not found"
        super().__init__(message, "NOT_FOUND_ERROR", error_details)


class ConflictError(AEMSException):
    """Resource conflict errors."""
    
    def __init__(self, message: str = "Resource conflict", resource: str = None, details: Dict[str, Any] = None):
        error_details = details or {}
        if resource:
            error_details["resource"] = resource
        super().__init__(message, "CONFLICT_ERROR", error_details)


class MFARequiredError(AuthenticationError):
    """Multi-factor authentication required."""
    
    def __init__(self, message: str = "Multi-factor authentication required", details: Dict[str, Any] = None):
        super().__init__(message, {"mfa_required": True, **(details or {})})


class PasswordExpiredError(AuthenticationError):
    """Password has expired and needs to be changed."""
    
    def __init__(self, message: str = "Password has expired", details: Dict[str, Any] = None):
        super().__init__(message, {"password_expired": True, **(details or {})})


class AccountLockedError(AuthenticationError):
    """Account is locked due to too many failed login attempts."""
    
    def __init__(self, message: str = "Account is temporarily locked", 
                 locked_until: str = None, details: Dict[str, Any] = None):
        error_details = details or {}
        if locked_until:
            error_details["locked_until"] = locked_until
        error_details["account_locked"] = True
        super().__init__(message, error_details)


# Exception mapping for HTTP status codes
EXCEPTION_STATUS_MAP = {
    AuthenticationError: 401,
    AuthorizationError: 403,
    ValidationError: 422,
    DatabaseError: 500,
    BusinessLogicError: 400,
    ExternalServiceError: 503,
    AIServiceError: 503,
    RateLimitError: 429,
    ConfigurationError: 500,
    NotFoundError: 404,
    ConflictError: 409,
    MFARequiredError: 401,
    PasswordExpiredError: 401,
    AccountLockedError: 423
}