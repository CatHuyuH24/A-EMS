"""
Shared Pydantic schemas for A-EMS microservices.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
import uuid


class BaseSchema(BaseModel):
    """Base schema with common fields."""
    
    class Config:
        from_attributes = True
        validate_assignment = True
        str_strip_whitespace = True


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class TenantSchema(BaseSchema):
    """Tenant information schema."""
    id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)


class UserBaseSchema(BaseSchema):
    """Base user schema."""
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    role: str = Field(default="user", max_length=50)


class UserCreateSchema(UserBaseSchema):
    """Schema for creating users."""
    password: str = Field(..., min_length=8)
    tenant_id: uuid.UUID


class UserUpdateSchema(BaseSchema):
    """Schema for updating users."""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(UserBaseSchema, TimestampSchema):
    """Schema for user responses."""
    id: uuid.UUID
    tenant_id: uuid.UUID
    is_active: bool
    mfa_enabled: bool
    last_login_at: Optional[datetime]


class LoginRequestSchema(BaseSchema):
    """Schema for login requests."""
    email: EmailStr
    password: str = Field(..., min_length=1)
    remember_me: bool = Field(default=False)


class MFAVerificationSchema(BaseSchema):
    """Schema for MFA verification."""
    token: str = Field(..., min_length=6, max_length=6)
    session_token: str = Field(..., min_length=1)


class TokenResponseSchema(BaseSchema):
    """Schema for token responses."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class PasswordChangeSchema(BaseSchema):
    """Schema for password change requests."""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)


class PasswordResetRequestSchema(BaseSchema):
    """Schema for password reset requests."""
    email: EmailStr


class PasswordResetSchema(BaseSchema):
    """Schema for password reset."""
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)


class APIErrorSchema(BaseSchema):
    """Schema for API error responses."""
    error: str
    message: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None


class PaginationSchema(BaseSchema):
    """Schema for pagination parameters."""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.limit


class PaginatedResponseSchema(BaseSchema):
    """Schema for paginated responses."""
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int
    
    @validator('pages', always=True)
    def calculate_pages(cls, v, values):
        total = values.get('total', 0)
        limit = values.get('limit', 20)
        return (total + limit - 1) // limit if total > 0 else 1


class HealthCheckSchema(BaseSchema):
    """Schema for health check responses."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: Optional[str] = None
    uptime: Optional[float] = None
    checks: Optional[Dict[str, Any]] = None


class BusinessMetricSchema(BaseSchema):
    """Schema for business metrics."""
    name: str = Field(..., min_length=1)
    value: float
    unit: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class AuditLogSchema(BaseSchema, TimestampSchema):
    """Schema for audit logs."""
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    tenant_id: uuid.UUID
    action: str
    resource: Optional[str]
    resource_id: Optional[str]
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    user_agent: Optional[str]
    correlation_id: Optional[str]


class SessionSchema(BaseSchema):
    """Schema for user sessions."""
    id: uuid.UUID
    user_id: uuid.UUID
    session_token: str
    expires_at: datetime
    is_active: bool
    device_info: Optional[Dict[str, Any]]
    ip_address: Optional[str]


class MFASetupSchema(BaseSchema):
    """Schema for MFA setup."""
    secret: str
    qr_code: str
    backup_codes: List[str]


class MFAEnableSchema(BaseSchema):
    """Schema for enabling MFA."""
    secret: str = Field(..., min_length=1)
    verification_code: str = Field(..., min_length=6, max_length=6)


class ChatMessageSchema(BaseSchema):
    """Schema for chat messages."""
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponseSchema(BaseSchema):
    """Schema for chat responses."""
    response: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None