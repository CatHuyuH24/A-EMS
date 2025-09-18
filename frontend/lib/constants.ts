// Application constants

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
} as const

// Authentication
export const AUTH_CONFIG = {
  TOKEN_STORAGE_KEY: 'aems_auth_token',
  REFRESH_TOKEN_STORAGE_KEY: 'aems_refresh_token',
  USER_STORAGE_KEY: 'aems_user_data',
  TOKEN_REFRESH_THRESHOLD: 5 * 60 * 1000, // 5 minutes before expiry
  SESSION_TIMEOUT: 24 * 60 * 60 * 1000, // 24 hours
} as const

// Local Storage Keys
export const STORAGE_KEYS = {
  THEME: 'aems_theme',
  SIDEBAR_COLLAPSED: 'aems_sidebar_collapsed',
  DASHBOARD_LAYOUT: 'aems_dashboard_layout',
  USER_PREFERENCES: 'aems_user_preferences',
  CHAT_HISTORY: 'aems_chat_history',
  ONBOARDING_COMPLETED: 'aems_onboarding_completed',
} as const

// Route Paths
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  CHAT: '/chat',
  SALES: '/sales',
  FINANCE: '/finance',
  HR: '/hr',
  REPORTS: '/reports',
  PROFILE: '/profile',
  SETTINGS: '/settings',
} as const

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    ME: '/auth/me',
    CHANGE_PASSWORD: '/auth/password',
  },
  
  // Dashboard
  DASHBOARD: {
    OVERVIEW: '/dashboard/overview',
    METRICS: '/dashboard/metrics',
  },
  
  // AI Chat
  CHAT: {
    SEND_MESSAGE: '/ai/chat',
    HISTORY: '/ai/chat/history',
    SUGGESTIONS: '/ai/suggestions',
  },
  
  // Sales
  SALES: {
    METRICS: '/sales/metrics',
    CUSTOMERS: '/sales/customers',
    PIPELINE: '/sales/pipeline',
    LEADS: '/sales/leads',
    DEALS: '/sales/deals',
  },
  
  // Finance
  FINANCE: {
    METRICS: '/finance/metrics',
    BUDGETS: '/finance/budgets',
    EXPENSES: '/finance/expenses',
    INVOICES: '/finance/invoices',
    REPORTS: '/finance/reports',
  },
  
  // HR
  HR: {
    METRICS: '/hr/metrics',
    EMPLOYEES: '/hr/employees',
    DEPARTMENTS: '/hr/departments',
    PAYROLL: '/hr/payroll',
    PERFORMANCE: '/hr/performance',
  },
  
  // Reports
  REPORTS: {
    LIST: '/reports',
    GENERATE: '/reports/generate',
    DETAIL: '/reports',
  },
} as const

// UI Constants
export const UI_CONSTANTS = {
  SIDEBAR_WIDTH: 256,
  SIDEBAR_COLLAPSED_WIDTH: 64,
  HEADER_HEIGHT: 64,
  MOBILE_BREAKPOINT: 768,
  TABLET_BREAKPOINT: 1024,
  DESKTOP_BREAKPOINT: 1280,
} as const

// Theme Configuration
export const THEME_CONFIG = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system',
} as const

// Chart Colors
export const CHART_COLORS = {
  PRIMARY: '#3B82F6',
  SUCCESS: '#10B981',
  WARNING: '#F59E0B',
  ERROR: '#EF4444',
  INFO: '#6366F1',
  SECONDARY: '#6B7280',
  ACCENT: '#8B5CF6',
} as const

// Status Colors
export const STATUS_COLORS = {
  ACTIVE: '#10B981',
  INACTIVE: '#6B7280',
  PENDING: '#F59E0B',
  COMPLETED: '#10B981',
  CANCELLED: '#EF4444',
  DRAFT: '#6B7280',
  PUBLISHED: '#10B981',
} as const

// User Roles
export const USER_ROLES = {
  SUPER_ADMIN: 'super_admin',
  ADMIN: 'admin',
  MANAGER: 'manager',
  EMPLOYEE: 'employee',
  VIEWER: 'viewer',
} as const

// Permissions
export const PERMISSIONS = {
  // Sales
  SALES_VIEW: 'sales:view',
  SALES_CREATE: 'sales:create',
  SALES_EDIT: 'sales:edit',
  SALES_DELETE: 'sales:delete',
  
  // Finance
  FINANCE_VIEW: 'finance:view',
  FINANCE_CREATE: 'finance:create',
  FINANCE_EDIT: 'finance:edit',
  FINANCE_DELETE: 'finance:delete',
  
  // HR
  HR_VIEW: 'hr:view',
  HR_CREATE: 'hr:create',
  HR_EDIT: 'hr:edit',
  HR_DELETE: 'hr:delete',
  
  // Reports
  REPORTS_VIEW: 'reports:view',
  REPORTS_CREATE: 'reports:create',
  REPORTS_DELETE: 'reports:delete',
  
  // Admin
  ADMIN_USERS: 'admin:users',
  ADMIN_SETTINGS: 'admin:settings',
  ADMIN_SYSTEM: 'admin:system',
} as const

// Dashboard Widgets
export const DASHBOARD_WIDGETS = {
  SALES_OVERVIEW: 'sales_overview',
  FINANCE_OVERVIEW: 'finance_overview',
  HR_OVERVIEW: 'hr_overview',
  RECENT_ACTIVITIES: 'recent_activities',
  AI_INSIGHTS: 'ai_insights',
  QUICK_ACTIONS: 'quick_actions',
  PERFORMANCE_METRICS: 'performance_metrics',
  NOTIFICATIONS: 'notifications',
} as const

// File Upload
export const FILE_UPLOAD = {
  MAX_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'application/pdf',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv',
  ],
  ALLOWED_EXTENSIONS: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf', 'xls', 'xlsx', 'csv'],
} as const

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
} as const

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM dd, yyyy',
  INPUT: 'yyyy-MM-dd',
  DATETIME: 'MMM dd, yyyy HH:mm',
  TIME: 'HH:mm',
  SHORT: 'MM/dd/yyyy',
  LONG: 'MMMM dd, yyyy',
} as const

// Chat Configuration
export const CHAT_CONFIG = {
  MAX_MESSAGE_LENGTH: 2000,
  TYPING_TIMEOUT: 1000,
  MAX_HISTORY_ITEMS: 50,
  AUTO_SAVE_DELAY: 2000,
  SUGGESTION_TIMEOUT: 5000,
} as const

// Notification Types
export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
} as const

// Loading States
export const LOADING_STATES = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error',
} as const

// Animation Durations (in ms)
export const ANIMATIONS = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
  VERY_SLOW: 1000,
} as const

// Keyboard Shortcuts
export const KEYBOARD_SHORTCUTS = {
  SEARCH: 'cmd+k',
  NEW_CHAT: 'cmd+n',
  TOGGLE_SIDEBAR: 'cmd+b',
  TOGGLE_THEME: 'cmd+shift+t',
  LOGOUT: 'cmd+shift+q',
} as const

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection and try again.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  FORBIDDEN: 'Access denied. You don\'t have permission to access this resource.',
  NOT_FOUND: 'The requested resource was not found.',
  SERVER_ERROR: 'Server error. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  SESSION_EXPIRED: 'Your session has expired. Please log in again.',
  RATE_LIMITED: 'Too many requests. Please wait before trying again.',
} as const

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN: 'Successfully logged in!',
  LOGOUT: 'Successfully logged out!',
  SAVE: 'Changes saved successfully!',
  DELETE: 'Item deleted successfully!',
  UPDATE: 'Updated successfully!',
  CREATE: 'Created successfully!',
  UPLOAD: 'File uploaded successfully!',
} as const

// Feature Flags (for development/testing)
export const FEATURE_FLAGS = {
  ENABLE_CHAT: true,
  ENABLE_NOTIFICATIONS: true,
  ENABLE_DARK_MODE: true,
  ENABLE_EXPORT: true,
  ENABLE_AI_SUGGESTIONS: true,
  DEBUG_MODE: process.env.NODE_ENV === 'development',
} as const

// Environment Configuration
export const ENV_CONFIG = {
  PRODUCTION: process.env.NODE_ENV === 'production',
  DEVELOPMENT: process.env.NODE_ENV === 'development',
  TEST: process.env.NODE_ENV === 'test',
  API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
  WEBSOCKET_URL: process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8000/ws',
  APP_VERSION: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
} as const