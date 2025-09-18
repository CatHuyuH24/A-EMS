"""
Configuration settings for API Gateway.
"""

import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Gateway settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS settings
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    allowed_headers: List[str] = ["*"]
    
    # Rate limiting
    rate_limit_per_minute: int = 100
    
    # Service discovery
    service_discovery_enabled: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    # Security
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
_settings: Settings = None


def get_settings() -> Settings:
    """Get application settings."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings