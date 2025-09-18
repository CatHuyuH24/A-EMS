"""
Password utilities for secure password handling.
"""

import bcrypt
import secrets
import string
from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)


class PasswordUtils:
    """Password hashing and validation utilities."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to hash password: {e}")
            raise
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to verify password: {e}")
            return False
    
    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Generate a secure random password."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """Validate password strength and return feedback."""
        result = {
            "is_valid": False,
            "score": 0,
            "feedback": []
        }
        
        # Length check
        if len(password) < 8:
            result["feedback"].append("Password must be at least 8 characters long")
        elif len(password) >= 12:
            result["score"] += 2
        else:
            result["score"] += 1
        
        # Uppercase check
        if not re.search(r"[A-Z]", password):
            result["feedback"].append("Password must contain at least one uppercase letter")
        else:
            result["score"] += 1
        
        # Lowercase check
        if not re.search(r"[a-z]", password):
            result["feedback"].append("Password must contain at least one lowercase letter")
        else:
            result["score"] += 1
        
        # Number check
        if not re.search(r"\d", password):
            result["feedback"].append("Password must contain at least one number")
        else:
            result["score"] += 1
        
        # Special character check
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            result["feedback"].append("Password must contain at least one special character")
        else:
            result["score"] += 1
        
        # Common patterns check
        common_patterns = [
            r"123",
            r"abc",
            r"password",
            r"admin",
            r"qwerty"
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                result["feedback"].append("Password contains common patterns")
                result["score"] -= 1
                break
        
        # Final validation
        result["is_valid"] = len(result["feedback"]) == 0 and result["score"] >= 4
        
        return result


class TOTPUtils:
    """TOTP (Time-based One-Time Password) utilities for MFA."""
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a base32 secret for TOTP."""
        return secrets.token_urlsafe(20)[:16].upper()
    
    @staticmethod
    def generate_backup_codes(count: int = 8) -> list:
        """Generate backup codes for MFA."""
        codes = []
        for _ in range(count):
            code = ''.join(secrets.choice(string.digits) for _ in range(8))
            # Format as XXXX-XXXX
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)
        return codes
    
    @staticmethod
    def hash_backup_codes(codes: list) -> list:
        """Hash backup codes for storage."""
        return [PasswordUtils.hash_password(code) for code in codes]
    
    @staticmethod
    def verify_backup_code(code: str, hashed_codes: list) -> bool:
        """Verify a backup code against hashed codes."""
        for hashed_code in hashed_codes:
            if PasswordUtils.verify_password(code, hashed_code):
                return True
        return False


# Global instances
password_utils = PasswordUtils()
totp_utils = TOTPUtils()