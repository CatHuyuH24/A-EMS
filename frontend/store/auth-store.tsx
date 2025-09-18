'use client'

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { createContext, useContext, ReactNode } from 'react'
import { api } from '@/lib/api'

// Types
interface User {
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

interface AuthTokens {
  accessToken: string
  refreshToken: string
  tokenType: string
  expiresIn: number
}

interface AuthState {
  user: User | null
  tokens: AuthTokens | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

interface AuthActions {
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>
  logout: () => Promise<void>
  refreshToken: () => Promise<void>
  updateUser: (userData: Partial<User>) => void
  clearError: () => void
  setLoading: (loading: boolean) => void
}

type AuthStore = AuthState & AuthActions

// Create the store
const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Actions
      login: async (email: string, password: string, rememberMe = false) => {
        set({ isLoading: true, error: null })
        
        try {
          const response = await api.auth.login({
            email,
            password,
            rememberMe,
          })

          const { user, ...tokens } = response.data

          set({
            user,
            tokens,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          })

          // Set API token for future requests
          api.setAuthToken(tokens.accessToken)
        } catch (error: any) {
          set({
            user: null,
            tokens: null,
            isAuthenticated: false,
            isLoading: false,
            error: error.response?.data?.message || 'Login failed',
          })
          throw error
        }
      },

      logout: async () => {
        set({ isLoading: true })
        
        try {
          await api.auth.logout()
        } catch (error) {
          // Continue with logout even if API call fails
          console.error('Logout API call failed:', error)
        } finally {
          // Clear all auth data
          set({
            user: null,
            tokens: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          })
          
          // Remove API token
          api.removeAuthToken()
        }
      },

      refreshToken: async () => {
        const { tokens } = get()
        
        if (!tokens?.refreshToken) {
          throw new Error('No refresh token available')
        }

        try {
          const response = await api.auth.refreshToken(tokens.refreshToken)
          const newTokens = response.data

          set({
            tokens: newTokens,
            error: null,
          })

          // Update API token
          api.setAuthToken(newTokens.accessToken)
        } catch (error: any) {
          // Refresh failed, logout user
          get().logout()
          throw error
        }
      },

      updateUser: (userData: Partial<User>) => {
        const { user } = get()
        
        if (user) {
          set({
            user: { ...user, ...userData },
          })
        }
      },

      clearError: () => {
        set({ error: null })
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Context for providing auth store
const AuthContext = createContext<ReturnType<typeof useAuthStore> | null>(null)

// Provider component
interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const store = useAuthStore()
  
  return (
    <AuthContext.Provider value={store}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook to use auth store
export function useAuth() {
  const context = useContext(AuthContext)
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  
  return context
}

// Export the store for direct access if needed
export { useAuthStore }