import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api, LoginRequest } from '@/lib/api'
import { useAuthStore } from '@/store/auth-store'
import { toast } from 'react-hot-toast'

// Query Keys
export const QUERY_KEYS = {
  // Auth
  me: ['auth', 'me'],
  
  // Dashboard
  overview: ['dashboard', 'overview'],
  metrics: (timeframe?: string) => ['dashboard', 'metrics', timeframe],
  
  // Chat
  chatHistory: (sessionId: string) => ['chat', 'history', sessionId],
  suggestions: ['chat', 'suggestions'],
  
  // Sales
  salesMetrics: ['sales', 'metrics'],
  customers: (params?: any) => ['sales', 'customers', params],
  pipeline: ['sales', 'pipeline'],
  
  // Finance
  financeMetrics: ['finance', 'metrics'],
  budgets: ['finance', 'budgets'],
  expenses: (params?: any) => ['finance', 'expenses', params],
  
  // HR
  hrMetrics: ['hr', 'metrics'],
  employees: (params?: any) => ['hr', 'employees', params],
  
  // Reports
  reports: (params?: any) => ['reports', params],
  report: (id: string) => ['reports', id],
} as const

// Auth Hooks
export const useLogin = () => {
  const { login: setAuthData } = useAuthStore()

  return useMutation({
    mutationFn: async (data: LoginRequest) => {
      const response = await api.auth.login(data)
      return response.data
    },
    onSuccess: (data) => {
      // Update auth store
      setAuthData(data.user, data.accessToken, data.refreshToken)
      // Set token in API client
      api.setAuthToken(data.accessToken)
      toast.success('Login successful!')
    },
    onError: (error: any) => {
      console.error('Login error:', error)
      // Error handling is done in API client
    },
  })
}

export const useLogout = () => {
  const { logout } = useAuthStore()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async () => {
      try {
        await api.auth.logout()
      } catch (error) {
        // Continue with logout even if API call fails
        console.warn('Logout API call failed:', error)
      }
    },
    onSuccess: () => {
      // Clear auth data
      logout()
      // Remove token from API client
      api.removeAuthToken()
      // Clear all queries
      queryClient.clear()
      toast.success('Logged out successfully')
    },
  })
}

export const useMe = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.me,
    queryFn: async () => {
      const response = await api.auth.getMe()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: (failureCount, error: any) => {
      // Don't retry on auth errors
      if (error?.response?.status === 401) return false
      return failureCount < 2
    },
  })
}

export const useChangePassword = () => {
  return useMutation({
    mutationFn: async (data: { currentPassword: string; newPassword: string }) => {
      const response = await api.auth.changePassword(data)
      return response.data
    },
    onSuccess: () => {
      toast.success('Password changed successfully!')
    },
  })
}

// Dashboard Hooks
export const useDashboardOverview = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.overview,
    queryFn: async () => {
      const response = await api.dashboard.getOverview()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 2 * 60 * 1000, // 2 minutes
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
  })
}

export const useDashboardMetrics = (timeframe?: string) => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.metrics(timeframe),
    queryFn: async () => {
      const response = await api.dashboard.getMetrics(timeframe)
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 2 * 60 * 1000,
  })
}

// Chat Hooks
export const useSendMessage = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: { message: string; sessionId?: string; context?: any }) => {
      const response = await api.chat.sendMessage(data)
      return response.data
    },
    onSuccess: (data, variables) => {
      // Invalidate chat history for this session
      if (variables.sessionId) {
        queryClient.invalidateQueries({
          queryKey: QUERY_KEYS.chatHistory(variables.sessionId),
        })
      }
      // Invalidate suggestions
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.suggestions,
      })
    },
  })
}

export const useChatHistory = (sessionId: string) => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.chatHistory(sessionId),
    queryFn: async () => {
      const response = await api.chat.getChatHistory(sessionId)
      return response.data
    },
    enabled: isAuthenticated && !!sessionId,
    staleTime: 1 * 60 * 1000, // 1 minute
  })
}

export const useChatSuggestions = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.suggestions,
    queryFn: async () => {
      const response = await api.chat.getSuggestions()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 10 * 60 * 1000, // 10 minutes
  })
}

// Sales Hooks
export const useSalesMetrics = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.salesMetrics,
    queryFn: async () => {
      const response = await api.sales.getMetrics()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  })
}

export const useCustomers = (params?: any) => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.customers(params),
    queryFn: async () => {
      const response = await api.sales.getCustomers(params)
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 2 * 60 * 1000,
  })
}

export const useSalesPipeline = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.pipeline,
    queryFn: async () => {
      const response = await api.sales.getPipeline()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  })
}

// Finance Hooks
export const useFinanceMetrics = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.financeMetrics,
    queryFn: async () => {
      const response = await api.finance.getMetrics()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  })
}

export const useBudgets = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.budgets,
    queryFn: async () => {
      const response = await api.finance.getBudgets()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 10 * 60 * 1000,
  })
}

export const useExpenses = (params?: any) => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.expenses(params),
    queryFn: async () => {
      const response = await api.finance.getExpenses(params)
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 2 * 60 * 1000,
  })
}

// HR Hooks
export const useHRMetrics = () => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.hrMetrics,
    queryFn: async () => {
      const response = await api.hr.getMetrics()
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  })
}

export const useEmployees = (params?: any) => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.employees(params),
    queryFn: async () => {
      const response = await api.hr.getEmployees(params)
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  })
}

// Reports Hooks
export const useReports = (params?: any) => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.reports(params),
    queryFn: async () => {
      const response = await api.reports.getReports(params)
      return response.data
    },
    enabled: isAuthenticated,
    staleTime: 2 * 60 * 1000,
  })
}

export const useGenerateReport = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: any) => {
      const response = await api.reports.generateReport(data)
      return response.data
    },
    onSuccess: () => {
      // Invalidate reports list
      queryClient.invalidateQueries({
        queryKey: ['reports'],
      })
      toast.success('Report generated successfully!')
    },
  })
}

export const useReport = (id: string) => {
  const { isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: QUERY_KEYS.report(id),
    queryFn: async () => {
      const response = await api.reports.getReport(id)
      return response.data
    },
    enabled: isAuthenticated && !!id,
    staleTime: 5 * 60 * 1000,
  })
}