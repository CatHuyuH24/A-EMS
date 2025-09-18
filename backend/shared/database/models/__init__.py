"""
Shared database models for A-EMS microservices.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, UUID, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..base import Base


class TimestampMixin:
    """Mixin for timestamp fields."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete


class TenantMixin:
    """Mixin for multi-tenant support."""
    
    @declared_attr
    def tenant_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False)


class Tenant(Base, TimestampMixin):
    """Tenant model for multi-tenancy support."""
    
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="tenant")


class User(Base, TimestampMixin, TenantMixin):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    
    # MFA fields
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255), nullable=True)
    mfa_backup_codes = Column(Text, nullable=True)  # JSON string of backup codes
    
    # OAuth fields
    google_id = Column(String(255), nullable=True)
    
    # Session tracking
    last_login_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")


class AuditLog(Base, TimestampMixin, TenantMixin):
    """Audit log for tracking user actions and system events."""
    
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=True)
    resource_id = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)  # JSON string
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    correlation_id = Column(String(255), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")


class Session(Base, TimestampMixin):
    """User session management."""
    
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    refresh_token = Column(String(255), unique=True, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    device_info = Column(Text, nullable=True)  # JSON string
    ip_address = Column(String(45), nullable=True)
    
    # Relationships
    user = relationship("User")