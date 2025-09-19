import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { useAuthStore } from '@/store/auth-store';
import { User } from '@/types';
import toast from 'react-hot-toast';

export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  role?: string;
}

// Login mutation
export const useLogin = () => {
  return useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      return useAuthStore
        .getState()
        .login(credentials.email, credentials.password);
    },
    onSuccess: () => {
      toast.success('Login successful!');
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Login failed');
    },
  });
};

// Register mutation
export const useRegister = () => {
  return useMutation({
    mutationFn: async (userData: RegisterData) => {
      const response = await api.post('/auth/register', userData);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Registration successful! Please log in.');
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Registration failed');
    },
  });
};

// Logout mutation
export const useLogout = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      return useAuthStore.getState().logout();
    },
    onSuccess: () => {
      queryClient.clear();
      toast.success('Logged out successfully');
    },
    onError: (error: any) => {
      // Still clear query cache on error
      queryClient.clear();
      toast.error(error?.response?.data?.detail || 'Logout failed');
    },
  });
};

// Get current user query
export const useCurrentUser = () => {
  const { user, isAuthenticated } = useAuthStore();

  return useQuery({
    queryKey: ['user', 'current'],
    queryFn: async () => {
      const response = await api.get('/auth/me');
      return response.data;
    },
    enabled: !!isAuthenticated,
    staleTime: 5 * 60 * 1000, // 5 minutes
    initialData: user,
  });
};

// Refresh token mutation
export const useRefreshToken = () => {
  return useMutation({
    mutationFn: async () => {
      return useAuthStore.getState().refreshToken();
    },
    onError: () => {
      // If refresh fails, user is already logged out by the store
      toast.error('Session expired. Please log in again.');
    },
  });
};

// Update user profile mutation
export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (userData: Partial<User>) => {
      const response = await api.put('/auth/profile', userData);
      return response.data;
    },
    onSuccess: (data) => {
      useAuthStore.getState().updateUser(data);
      queryClient.setQueryData(['user', 'current'], data);
      toast.success('Profile updated successfully');
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Profile update failed');
    },
  });
};

// Change password mutation
export const useChangePassword = () => {
  return useMutation({
    mutationFn: async (passwords: {
      current_password: string;
      new_password: string;
    }) => {
      const response = await api.post('/auth/change-password', passwords);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Password changed successfully');
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Password change failed');
    },
  });
};
