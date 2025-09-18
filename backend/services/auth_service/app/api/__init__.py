"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
sys.path.append('../../../')

from shared.database.base import get_database
from shared.schemas import (
    LoginRequestSchema,
    TokenResponseSchema,
    UserCreateSchema,
    UserResponseSchema,
    PasswordChangeSchema,
    MFAVerificationSchema
)
from ..services.auth_service import AuthService
from ..core.dependencies import get_current_user

auth_router = APIRouter()


@auth_router.post("/login", response_model=TokenResponseSchema)
async def login(
    request: LoginRequestSchema,
    db: Session = Depends(get_database)
):
    """User login endpoint."""
    auth_service = AuthService(db)
    
    try:
        tokens = await auth_service.login(
            email=request.email,
            password=request.password,
            remember_me=request.remember_me
        )
        return tokens
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Authentication failed", "message": str(e)}
        )


@auth_router.post("/register", response_model=UserResponseSchema)
async def register(
    request: UserCreateSchema,
    db: Session = Depends(get_database)
):
    """User registration endpoint."""
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.register(request)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Registration failed", "message": str(e)}
        )


@auth_router.post("/refresh", response_model=TokenResponseSchema)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_database)
):
    """Refresh access token."""
    auth_service = AuthService(db)
    
    try:
        tokens = await auth_service.refresh_token(refresh_token)
        return tokens
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token refresh failed", "message": str(e)}
        )


@auth_router.post("/logout")
async def logout(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """User logout endpoint."""
    auth_service = AuthService(db)
    
    try:
        await auth_service.logout(current_user["id"])
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Logout failed", "message": str(e)}
        )


@auth_router.get("/me", response_model=UserResponseSchema)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """Get current user information."""
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.get_user_by_id(current_user["id"])
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found", "message": str(e)}
        )


@auth_router.put("/password", response_model=dict)
async def change_password(
    request: PasswordChangeSchema,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """Change user password."""
    auth_service = AuthService(db)
    
    try:
        await auth_service.change_password(
            user_id=current_user["id"],
            current_password=request.current_password,
            new_password=request.new_password
        )
        return {"message": "Password changed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Password change failed", "message": str(e)}
        )


@auth_router.post("/mfa/verify", response_model=TokenResponseSchema)
async def verify_mfa(
    request: MFAVerificationSchema,
    db: Session = Depends(get_database)
):
    """Verify MFA token."""
    auth_service = AuthService(db)
    
    try:
        tokens = await auth_service.verify_mfa(
            session_token=request.session_token,
            mfa_token=request.token
        )
        return tokens
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "MFA verification failed", "message": str(e)}
        )


@auth_router.get("/mfa/setup")
async def setup_mfa(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """Setup MFA for user."""
    auth_service = AuthService(db)
    
    try:
        mfa_data = await auth_service.setup_mfa(current_user["id"])
        return mfa_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "MFA setup failed", "message": str(e)}
        )