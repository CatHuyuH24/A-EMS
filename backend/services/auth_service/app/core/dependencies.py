"""
FastAPI dependencies for authentication service.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sys
sys.path.append('../../../../')

from shared.auth.jwt_handler import jwt_handler
from shared.database.base import get_database
from sqlalchemy.orm import Session

# Initialize security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database)
) -> dict:
    """Get current authenticated user from token."""
    
    # Verify token
    payload = jwt_handler.verify_access_token(credentials.credentials)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token", "message": "Could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extract user information
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token", "message": "Token missing user ID"},
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return {
        "id": user_id,
        "email": payload.get("email"),
        "role": payload.get("role"),
        "tenant_id": payload.get("tenant_id")
    }


async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Get current active user (additional validation if needed)."""
    # Add additional checks if required
    return current_user


async def require_admin_role(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Require admin role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Insufficient permissions", "message": "Admin role required"}
        )
    return current_user


async def require_manager_role(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Require manager role or higher."""
    allowed_roles = ["admin", "manager"]
    if current_user.get("role") not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Insufficient permissions", "message": "Manager role or higher required"}
        )
    return current_user