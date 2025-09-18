import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { toast } from 'react-hot-toast'

// Types
interface LoginRequest {
  email: string
  password: string
  rememberMe?: boolean
}

interface LoginResponse {
  user: {
    id: string
    email: string
    firstName?: string
    lastName?: string
    role: string
    tenantId: string
    isActive: boolean
    mfaEnabled: boolean
    lastLoginAt?: string
  }
  accessToken: string
  refreshToken: string
  tokenType: string
  expiresIn: number
}

interface RefreshTokenResponse {
  accessToken: string
  refreshToken: string
  tokenType: string
  expiresIn: number
}

interface ApiError {
  error: string
  message: string
  code?: string
  details?: Record<string, any>
  correlationId?: string
}

// API Client Class
class ApiClient {
  private client: AxiosInstance
  private authToken: string | null = null

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token to requests
        if (this.authToken) {
          config.headers.Authorization = `Bearer ${this.authToken}`
        }

        // Add correlation ID for request tracking
        config.headers['X-Correlation-ID'] = this.generateCorrelationId()

        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response
      },
      async (error) => {
        const originalRequest = error.config

        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            await this.handleTokenRefresh()
            return this.client(originalRequest)
          } catch (refreshError) {
            // Refresh failed, redirect to login
            this.handleAuthError()
            return Promise.reject(refreshError)
          }
        }

        // Handle other errors
        this.handleApiError(error)
        return Promise.reject(error)
      }
    )
  }

  private generateCorrelationId(): string {
    return `frontend-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }

  private async handleTokenRefresh() {
    // This should be implemented based on your auth store
    // For now, it's a placeholder
    const refreshToken = localStorage.getItem('refreshToken')
    
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    const response = await this.client.post('/auth/refresh', {
      refreshToken,
    })

    const { accessToken } = response.data
    this.setAuthToken(accessToken)
    
    return response.data
  }

  private handleAuthError() {
    // Clear auth data and redirect to login
    this.removeAuthToken()
    localStorage.removeItem('refreshToken')
    
    // Only redirect if we're not already on a public page
    if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/login')) {
      window.location.href = '/login'
    }
  }

  private handleApiError(error: any) {
    const apiError: ApiError = error.response?.data || {
      error: 'Network Error',
      message: 'Unable to connect to the server',
    }

    // Show appropriate toast notifications
    switch (error.response?.status) {
      case 400:
        toast.error(apiError.message || 'Invalid request')
        break
      case 401:
        // Don't show toast for auth errors as they're handled by redirect
        break
      case 403:
        toast.error('Access denied. You don\'t have permission to perform this action.')
        break
      case 404:
        toast.error('The requested resource was not found.')
        break
      case 422:
        toast.error(apiError.message || 'Validation failed')
        break
      case 429:
        toast.error('Too many requests. Please try again later.')
        break
      case 500:
      case 502:
      case 503:
      case 504:
        toast.error('Server error. Please try again later.')
        break
      default:
        if (!navigator.onLine) {
          toast.error('No internet connection. Please check your network.')
        } else {
          toast.error(apiError.message || 'An unexpected error occurred')
        }
    }
  }

  // Auth token management
  setAuthToken(token: string) {
    this.authToken = token
  }

  removeAuthToken() {
    this.authToken = null
  }

  // Generic HTTP methods
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.get<T>(url, config)
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.post<T>(url, data, config)
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.put<T>(url, data, config)
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.patch<T>(url, data, config)
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.delete<T>(url, config)
  }

  // Auth endpoints
  auth = {
    login: (data: LoginRequest) => 
      this.post<LoginResponse>('/auth/login', data),
    
    logout: () => 
      this.post('/auth/logout'),
    
    refreshToken: (refreshToken: string) => 
      this.post<RefreshTokenResponse>('/auth/refresh', { refreshToken }),
    
    getMe: () => 
      this.get('/auth/me'),
    
    changePassword: (data: { currentPassword: string; newPassword: string }) => 
      this.put('/auth/password', data),
  }

  // Dashboard endpoints
  dashboard = {
    getOverview: () => 
      this.get('/dashboard/overview'),
    
    getMetrics: (timeframe?: string) => 
      this.get('/dashboard/metrics', { params: { timeframe } }),
  }

  // Chat endpoints
  chat = {
    sendMessage: (data: { message: string; sessionId?: string; context?: any }) => 
      this.post('/ai/chat', data),
    
    getChatHistory: (sessionId: string) => 
      this.get(`/ai/chat/history/${sessionId}`),
    
    getSuggestions: () => 
      this.get('/ai/suggestions'),
  }

  // Sales endpoints
  sales = {
    getMetrics: () => 
      this.get('/sales/metrics'),
    
    getCustomers: (params?: any) => 
      this.get('/sales/customers', { params }),
    
    getPipeline: () => 
      this.get('/sales/pipeline'),
  }

  // Finance endpoints
  finance = {
    getMetrics: () => 
      this.get('/finance/metrics'),
    
    getBudgets: () => 
      this.get('/finance/budgets'),
    
    getExpenses: (params?: any) => 
      this.get('/finance/expenses', { params }),
  }

  // HR endpoints
  hr = {
    getMetrics: () => 
      this.get('/hr/metrics'),
    
    getEmployees: (params?: any) => 
      this.get('/hr/employees', { params }),
  }

  // Reports endpoints
  reports = {
    getReports: (params?: any) => 
      this.get('/reports', { params }),
    
    generateReport: (data: any) => 
      this.post('/reports/generate', data),
    
    getReport: (id: string) => 
      this.get(`/reports/${id}`),
  }
}

// Create and export API instance
export const api = new ApiClient()

// Export types
export type {
  LoginRequest,
  LoginResponse,
  RefreshTokenResponse,
  ApiError,
}