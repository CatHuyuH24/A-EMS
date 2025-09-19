// Common Types

// Authentication Types
export interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  role: string;
  tenantId: string;
  isActive: boolean;
  mfaEnabled: boolean;
  lastLoginAt?: string;
  createdAt: string;
  updatedAt: string;
  avatar?: string;
  timezone?: string;
  locale?: string;
}

export interface AuthResponse {
  user: User;
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface ChangePasswordData {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

// API Response Types
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
  timestamp: string;
  correlationId?: string;
}

export interface PaginatedResponse<T = any> {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

export interface ApiError {
  error: string;
  message: string;
  code?: string;
  details?: Record<string, any>;
  correlationId?: string;
}

// Dashboard Types
export interface DashboardOverview {
  metrics: {
    totalRevenue: number;
    totalCustomers: number;
    totalEmployees: number;
    activeProjects: number;
  };
  recentActivities: Activity[];
  aiInsights: AIInsight[];
  notifications: Notification[];
}

export interface Activity {
  id: string;
  type: 'sales' | 'finance' | 'hr' | 'system';
  title: string;
  description: string;
  timestamp: string;
  userId: string;
  userName: string;
  metadata?: Record<string, any>;
}

export interface AIInsight {
  id: string;
  type: 'recommendation' | 'alert' | 'prediction';
  title: string;
  description: string;
  confidence: number;
  category: string;
  actionable: boolean;
  metadata?: Record<string, any>;
}

export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  actionUrl?: string;
  actionText?: string;
}

// Chat Types
export interface ChatMessage {
  id: string;
  sessionId: string;
  content: string;
  type: 'user' | 'assistant';
  timestamp: string;
  metadata?: {
    sources?: string[];
    confidence?: number;
    suggestedActions?: string[];
  };
}

export interface ChatSession {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  messageCount: number;
  lastMessage?: string;
}

export interface ChatSuggestion {
  id: string;
  text: string;
  category: string;
  priority: number;
}

// Sales Types
export interface Customer {
  id: string;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  industry?: string;
  status: 'active' | 'inactive' | 'prospect';
  totalValue: number;
  lastContactDate?: string;
  assignedSalesRep?: string;
  createdAt: string;
  updatedAt: string;
  tags?: string[];
}

export interface Deal {
  id: string;
  title: string;
  customerId: string;
  customerName: string;
  value: number;
  stage:
    | 'lead'
    | 'qualified'
    | 'proposal'
    | 'negotiation'
    | 'closed_won'
    | 'closed_lost';
  probability: number;
  expectedCloseDate?: string;
  actualCloseDate?: string;
  assignedTo: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface SalesMetrics {
  totalRevenue: number;
  monthlyRevenue: number;
  dealsClosed: number;
  dealsInPipeline: number;
  averageDealSize: number;
  conversionRate: number;
  salesGrowth: number;
  topPerformers: Array<{
    id: string;
    name: string;
    revenue: number;
    dealsCount: number;
  }>;
}

// Finance Types
export interface Budget {
  id: string;
  name: string;
  category: string;
  allocatedAmount: number;
  spentAmount: number;
  remainingAmount: number;
  period: 'monthly' | 'quarterly' | 'yearly';
  startDate: string;
  endDate: string;
  status: 'active' | 'inactive' | 'completed';
  approvedBy: string;
}

export interface Expense {
  id: string;
  description: string;
  amount: number;
  category: string;
  date: string;
  status: 'pending' | 'approved' | 'rejected';
  submittedBy: string;
  approvedBy?: string;
  receiptUrl?: string;
  budgetId?: string;
  notes?: string;
  createdAt: string;
}

export interface FinanceMetrics {
  totalRevenue: number;
  totalExpenses: number;
  netProfit: number;
  burnRate: number;
  cashFlow: number;
  budgetUtilization: number;
  expensesByCategory: Array<{
    category: string;
    amount: number;
    percentage: number;
  }>;
}

// HR Types
export interface Employee {
  id: string;
  employeeId: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  department: string;
  position: string;
  manager?: string;
  startDate: string;
  endDate?: string;
  salary: number;
  status: 'active' | 'inactive' | 'terminated';
  address?: Address;
  emergencyContact?: Contact;
  benefits?: string[];
  skills?: string[];
  certifications?: Certification[];
}

export interface Department {
  id: string;
  name: string;
  description: string;
  managerId: string;
  employeeCount: number;
  budget: number;
  location?: string;
}

export interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}

export interface Contact {
  name: string;
  relationship: string;
  phone: string;
  email?: string;
}

export interface Certification {
  name: string;
  issuer: string;
  issueDate: string;
  expiryDate?: string;
  credentialId?: string;
}

export interface HRMetrics {
  totalEmployees: number;
  newHires: number;
  terminations: number;
  turnoverRate: number;
  averageSalary: number;
  departmentBreakdown: Array<{
    department: string;
    count: number;
    percentage: number;
  }>;
}

// Report Types
export interface Report {
  id: string;
  title: string;
  description: string;
  type: 'sales' | 'finance' | 'hr' | 'custom';
  format: 'pdf' | 'excel' | 'csv';
  status: 'generating' | 'completed' | 'failed';
  parameters: Record<string, any>;
  fileUrl?: string;
  fileSize?: number;
  generatedBy: string;
  generatedAt: string;
  expiresAt?: string;
}

export interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  type: 'sales' | 'finance' | 'hr' | 'custom';
  parameters: ReportParameter[];
  defaultValues?: Record<string, any>;
}

export interface ReportParameter {
  name: string;
  label: string;
  type: 'text' | 'number' | 'date' | 'select' | 'multiselect';
  required: boolean;
  options?: Array<{ value: string; label: string }>;
  defaultValue?: any;
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
  };
}

// Theme Types
export type ThemeMode = 'light' | 'dark' | 'system';

export interface ThemeConfig {
  mode: ThemeMode;
  primaryColor: string;
  accentColor: string;
  sidebarCollapsed: boolean;
}

// UI Component Types
export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
  icon?: string;
}

export interface TableColumn<T = any> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  width?: number;
  render?: (value: any, row: T) => React.ReactNode;
}

export interface TableProps<T = any> {
  data: T[];
  columns: TableColumn<T>[];
  loading?: boolean;
  pagination?: {
    page: number;
    pageSize: number;
    total: number;
    onPageChange: (page: number) => void;
    onPageSizeChange: (pageSize: number) => void;
  };
  sorting?: {
    column: keyof T;
    direction: 'asc' | 'desc';
    onSort: (column: keyof T, direction: 'asc' | 'desc') => void;
  };
  selection?: {
    selectedRows: T[];
    onSelectionChange: (rows: T[]) => void;
  };
}

// Form Types
export interface FormField {
  name: string;
  label: string;
  type:
    | 'text'
    | 'email'
    | 'password'
    | 'number'
    | 'select'
    | 'textarea'
    | 'checkbox'
    | 'date';
  required?: boolean;
  placeholder?: string;
  options?: SelectOption[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: RegExp;
    custom?: (value: any) => string | null;
  };
}

export interface FormProps {
  fields: FormField[];
  onSubmit: (data: Record<string, any>) => void;
  loading?: boolean;
  initialValues?: Record<string, any>;
  submitText?: string;
  resetText?: string;
}

// Chart Types
export interface ChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string | string[];
    borderWidth?: number;
  }>;
}

export interface ChartOptions {
  responsive?: boolean;
  maintainAspectRatio?: boolean;
  plugins?: {
    legend?: {
      display?: boolean;
      position?: 'top' | 'bottom' | 'left' | 'right';
    };
    tooltip?: {
      enabled?: boolean;
    };
  };
  scales?: {
    x?: {
      display?: boolean;
      grid?: {
        display?: boolean;
      };
    };
    y?: {
      display?: boolean;
      beginAtZero?: boolean;
      grid?: {
        display?: boolean;
      };
    };
  };
}

// State Management Types
export interface LoadingState {
  loading: boolean;
  error: string | null;
  success: boolean;
}

export interface AsyncState<T = any> extends LoadingState {
  data: T | null;
}

// Utility Types
export type WithId<T> = T & { id: string };
export type WithTimestamps<T> = T & {
  createdAt: string;
  updatedAt: string;
};
export type WithOptionalId<T> = T & { id?: string };
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Environment Types
export interface EnvironmentConfig {
  NODE_ENV: 'development' | 'production' | 'test';
  NEXT_PUBLIC_API_BASE_URL: string;
  NEXT_PUBLIC_WEBSOCKET_URL: string;
  NEXT_PUBLIC_APP_VERSION: string;
}

// Navigation Types
export interface NavigationItem {
  id: string;
  label: string;
  icon?: string;
  href?: string;
  children?: NavigationItem[];
  badge?: string;
  disabled?: boolean;
  permissions?: string[];
}

export interface Breadcrumb {
  label: string;
  href?: string;
}

// Search Types
export interface SearchResult {
  id: string;
  title: string;
  description: string;
  type: string;
  url: string;
  relevance: number;
  metadata?: Record<string, any>;
}

export interface SearchFilters {
  type?: string[];
  dateRange?: {
    start: string;
    end: string;
  };
  categories?: string[];
  tags?: string[];
}

// Export all types
// Constants types can be imported directly when needed
