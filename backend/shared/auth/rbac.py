"""
Role-Based Access Control (RBAC) utilities.
"""

from enum import Enum
from typing import List, Dict, Set, Optional
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class Role(Enum):
    """User roles in the system."""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    VIEWER = "viewer"


class Permission(Enum):
    """System permissions."""
    # User management
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    
    # Dashboard access
    VIEW_DASHBOARD = "view_dashboard"
    VIEW_ANALYTICS = "view_analytics"
    
    # Sales permissions
    VIEW_SALES = "view_sales"
    MANAGE_SALES = "manage_sales"
    VIEW_CUSTOMERS = "view_customers"
    MANAGE_CUSTOMERS = "manage_customers"
    
    # Finance permissions
    VIEW_FINANCE = "view_finance"
    MANAGE_FINANCE = "manage_finance"
    VIEW_BUDGETS = "view_budgets"
    MANAGE_BUDGETS = "manage_budgets"
    
    # HR permissions
    VIEW_HR = "view_hr"
    MANAGE_HR = "manage_hr"
    VIEW_EMPLOYEES = "view_employees"
    MANAGE_EMPLOYEES = "manage_employees"
    
    # Products permissions
    VIEW_PRODUCTS = "view_products"
    MANAGE_PRODUCTS = "manage_products"
    
    # Risk permissions
    VIEW_RISK = "view_risk"
    MANAGE_RISK = "manage_risk"
    
    # Reports permissions
    VIEW_REPORTS = "view_reports"
    CREATE_REPORTS = "create_reports"
    MANAGE_REPORTS = "manage_reports"
    
    # AI permissions
    USE_AI_CHAT = "use_ai_chat"
    VIEW_AI_ANALYTICS = "view_ai_analytics"
    
    # System permissions
    MANAGE_SYSTEM = "manage_system"
    VIEW_LOGS = "view_logs"


class RBACManager:
    """Role-Based Access Control manager."""
    
    def __init__(self):
        self.role_permissions = self._initialize_role_permissions()
    
    def _initialize_role_permissions(self) -> Dict[Role, Set[Permission]]:
        """Initialize role-permission mappings."""
        return {
            Role.ADMIN: {
                # Full access to everything
                Permission.CREATE_USER, Permission.READ_USER, Permission.UPDATE_USER, Permission.DELETE_USER,
                Permission.VIEW_DASHBOARD, Permission.VIEW_ANALYTICS,
                Permission.VIEW_SALES, Permission.MANAGE_SALES, Permission.VIEW_CUSTOMERS, Permission.MANAGE_CUSTOMERS,
                Permission.VIEW_FINANCE, Permission.MANAGE_FINANCE, Permission.VIEW_BUDGETS, Permission.MANAGE_BUDGETS,
                Permission.VIEW_HR, Permission.MANAGE_HR, Permission.VIEW_EMPLOYEES, Permission.MANAGE_EMPLOYEES,
                Permission.VIEW_PRODUCTS, Permission.MANAGE_PRODUCTS,
                Permission.VIEW_RISK, Permission.MANAGE_RISK,
                Permission.VIEW_REPORTS, Permission.CREATE_REPORTS, Permission.MANAGE_REPORTS,
                Permission.USE_AI_CHAT, Permission.VIEW_AI_ANALYTICS,
                Permission.MANAGE_SYSTEM, Permission.VIEW_LOGS
            },
            
            Role.MANAGER: {
                # Management-level access
                Permission.READ_USER, Permission.UPDATE_USER,
                Permission.VIEW_DASHBOARD, Permission.VIEW_ANALYTICS,
                Permission.VIEW_SALES, Permission.MANAGE_SALES, Permission.VIEW_CUSTOMERS, Permission.MANAGE_CUSTOMERS,
                Permission.VIEW_FINANCE, Permission.MANAGE_FINANCE, Permission.VIEW_BUDGETS, Permission.MANAGE_BUDGETS,
                Permission.VIEW_HR, Permission.MANAGE_HR, Permission.VIEW_EMPLOYEES, Permission.MANAGE_EMPLOYEES,
                Permission.VIEW_PRODUCTS, Permission.MANAGE_PRODUCTS,
                Permission.VIEW_RISK, Permission.MANAGE_RISK,
                Permission.VIEW_REPORTS, Permission.CREATE_REPORTS, Permission.MANAGE_REPORTS,
                Permission.USE_AI_CHAT, Permission.VIEW_AI_ANALYTICS
            },
            
            Role.USER: {
                # Standard user access
                Permission.READ_USER,
                Permission.VIEW_DASHBOARD, Permission.VIEW_ANALYTICS,
                Permission.VIEW_SALES, Permission.VIEW_CUSTOMERS,
                Permission.VIEW_FINANCE, Permission.VIEW_BUDGETS,
                Permission.VIEW_HR, Permission.VIEW_EMPLOYEES,
                Permission.VIEW_PRODUCTS,
                Permission.VIEW_RISK,
                Permission.VIEW_REPORTS, Permission.CREATE_REPORTS,
                Permission.USE_AI_CHAT
            },
            
            Role.VIEWER: {
                # Read-only access
                Permission.VIEW_DASHBOARD,
                Permission.VIEW_SALES, Permission.VIEW_CUSTOMERS,
                Permission.VIEW_FINANCE, Permission.VIEW_BUDGETS,
                Permission.VIEW_HR, Permission.VIEW_EMPLOYEES,
                Permission.VIEW_PRODUCTS,
                Permission.VIEW_RISK,
                Permission.VIEW_REPORTS,
                Permission.USE_AI_CHAT
            }
        }
    
    def has_permission(self, role: str, permission: Permission) -> bool:
        """Check if a role has a specific permission."""
        try:
            user_role = Role(role.lower())
            return permission in self.role_permissions.get(user_role, set())
        except ValueError:
            logger.warning(f"Unknown role: {role}")
            return False
    
    def get_role_permissions(self, role: str) -> Set[Permission]:
        """Get all permissions for a role."""
        try:
            user_role = Role(role.lower())
            return self.role_permissions.get(user_role, set())
        except ValueError:
            logger.warning(f"Unknown role: {role}")
            return set()
    
    def can_access_resource(self, user_role: str, resource: str, action: str) -> bool:
        """Check if a user can perform an action on a resource."""
        permission_map = {
            "users": {
                "create": Permission.CREATE_USER,
                "read": Permission.READ_USER,
                "update": Permission.UPDATE_USER,
                "delete": Permission.DELETE_USER
            },
            "dashboard": {
                "view": Permission.VIEW_DASHBOARD
            },
            "sales": {
                "view": Permission.VIEW_SALES,
                "manage": Permission.MANAGE_SALES
            },
            "finance": {
                "view": Permission.VIEW_FINANCE,
                "manage": Permission.MANAGE_FINANCE
            },
            "hr": {
                "view": Permission.VIEW_HR,
                "manage": Permission.MANAGE_HR
            },
            "products": {
                "view": Permission.VIEW_PRODUCTS,
                "manage": Permission.MANAGE_PRODUCTS
            },
            "risk": {
                "view": Permission.VIEW_RISK,
                "manage": Permission.MANAGE_RISK
            },
            "reports": {
                "view": Permission.VIEW_REPORTS,
                "create": Permission.CREATE_REPORTS,
                "manage": Permission.MANAGE_REPORTS
            },
            "ai": {
                "chat": Permission.USE_AI_CHAT,
                "analytics": Permission.VIEW_AI_ANALYTICS
            }
        }
        
        resource_permissions = permission_map.get(resource.lower())
        if not resource_permissions:
            return False
        
        required_permission = resource_permissions.get(action.lower())
        if not required_permission:
            return False
        
        return self.has_permission(user_role, required_permission)


# Global RBAC manager instance
rbac_manager = RBACManager()


def require_permission(permission: Permission):
    """Decorator to require specific permission."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This would be implemented with FastAPI dependency injection
            # For now, it's a placeholder
            user = kwargs.get('current_user')
            if not user:
                raise PermissionError("Authentication required")
            
            if not rbac_manager.has_permission(user.get('role'), permission):
                raise PermissionError(f"Permission {permission.value} required")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role: Role):
    """Decorator to require specific role."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('current_user')
            if not user:
                raise PermissionError("Authentication required")
            
            if user.get('role').lower() != role.value:
                raise PermissionError(f"Role {role.value} required")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator