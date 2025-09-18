"""
Common utility functions for A-EMS microservices.
"""

import hashlib
import hmac
import secrets
import string
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import json
import re


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)


def generate_api_key(prefix: str = "aems") -> str:
    """Generate an API key with prefix."""
    token = secrets.token_urlsafe(32)
    return f"{prefix}_{token}"


def hash_string(value: str, salt: str = None) -> str:
    """Hash a string using SHA-256."""
    if salt is None:
        salt = secrets.token_hex(16)
    
    hash_input = f"{value}{salt}".encode('utf-8')
    return hashlib.sha256(hash_input).hexdigest()


def verify_signature(data: str, signature: str, secret: str) -> bool:
    """Verify HMAC signature."""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = f"{name[:250]}.{ext}" if ext else name[:255]
    
    return filename


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Simple international format validation
    pattern = r'^\+?1?-?\.?\s?\(?\d{3}\)?-?\.?\s?\d{3}-?\.?\s?\d{4}$'
    return re.match(pattern, phone.replace(' ', '')) is not None


def mask_sensitive_data(data: Dict[str, Any], fields: List[str] = None) -> Dict[str, Any]:
    """Mask sensitive fields in data dictionary."""
    if fields is None:
        fields = ['password', 'token', 'secret', 'key', 'api_key', 'auth']
    
    masked_data = data.copy()
    
    for field in fields:
        for key in masked_data:
            if field.lower() in key.lower():
                value = masked_data[key]
                if isinstance(value, str) and len(value) > 4:
                    masked_data[key] = f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"
                else:
                    masked_data[key] = "***"
    
    return masked_data


def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries."""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def flatten_dict(data: Dict[str, Any], parent_key: str = '', separator: str = '.') -> Dict[str, Any]:
    """Flatten nested dictionary."""
    items = []
    
    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))
    
    return dict(items)


def get_utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
    """Format datetime to string."""
    return dt.strftime(format_str)


def parse_datetime(date_string: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse string to datetime."""
    return datetime.strptime(date_string, format_str)


def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date."""
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def format_currency(amount: float, currency: str = "USD", locale: str = "en_US") -> str:
    """Format currency amount."""
    # Simple formatting (in production, use locale-specific formatting)
    symbol_map = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = symbol_map.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """Format percentage value."""
    return f"{value:.{decimal_places}f}%"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def normalize_string(text: str) -> str:
    """Normalize string for comparison."""
    return re.sub(r'\s+', ' ', text.strip().lower())


def is_json_serializable(obj: Any) -> bool:
    """Check if object is JSON serializable."""
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False


def safe_json_loads(json_string: str, default: Any = None) -> Any:
    """Safely load JSON string."""
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def generate_slug(text: str, max_length: int = 50) -> str:
    """Generate URL-friendly slug from text."""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'\s+', '-', text.lower())
    # Remove non-alphanumeric characters except hyphens
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug[:max_length] if slug else generate_secure_token(8)


class Timer:
    """Simple timer context manager."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0