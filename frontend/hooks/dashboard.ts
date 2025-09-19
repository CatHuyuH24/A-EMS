import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface DashboardMetric {
  id: string;
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'increase' | 'decrease';
  format?: 'currency' | 'number' | 'percentage';
  icon?: string;
  color?: 'blue' | 'green' | 'yellow' | 'red' | 'purple';
}

export interface Activity {
  id: string;
  type:
    | 'sale'
    | 'expense'
    | 'user_registration'
    | 'report_generated'
    | 'system_alert'
    | 'task_completed';
  title: string;
  description: string;
  timestamp: Date;
  metadata?: {
    amount?: number;
    user?: string;
    priority?: 'low' | 'medium' | 'high';
  };
}

export interface AIInsight {
  id: string;
  type: 'opportunity' | 'warning' | 'trend' | 'recommendation';
  title: string;
  description: string;
  confidence: number;
  actionable: boolean;
  priority: 'low' | 'medium' | 'high';
  timestamp: Date;
  metadata?: {
    dataSource?: string;
    affectedMetrics?: string[];
    estimatedImpact?: string;
  };
}

// Get dashboard metrics query
export const useDashboardMetrics = () => {
  return useQuery({
    queryKey: ['dashboard', 'metrics'],
    queryFn: async () => {
      const response = await api.get('/dashboard/metrics');
      return response.data;
    },
    staleTime: 60 * 1000, // 1 minute
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
  });
};

// Get recent activities query
export const useRecentActivities = (limit: number = 10) => {
  return useQuery({
    queryKey: ['dashboard', 'activities', limit],
    queryFn: async () => {
      const response = await api.get('/dashboard/activities', {
        params: { limit },
      });
      return response.data;
    },
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Refetch every minute
  });
};

// Get AI insights query
export const useAIInsights = (limit: number = 5) => {
  return useQuery({
    queryKey: ['dashboard', 'ai-insights', limit],
    queryFn: async () => {
      const response = await api.get('/dashboard/ai-insights', {
        params: { limit },
      });
      return response.data;
    },
    staleTime: 2 * 60 * 1000, // 2 minutes
    refetchInterval: 10 * 60 * 1000, // Refetch every 10 minutes
  });
};

// Get chart data query
export const useChartData = (chartType: string, timeRange: string = '7d') => {
  return useQuery({
    queryKey: ['dashboard', 'charts', chartType, timeRange],
    queryFn: async () => {
      const response = await api.get(`/dashboard/charts/${chartType}`, {
        params: { timeRange },
      });
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    enabled: !!chartType,
  });
};

// Get dashboard summary query (overview data)
export const useDashboardSummary = () => {
  return useQuery({
    queryKey: ['dashboard', 'summary'],
    queryFn: async () => {
      const response = await api.get('/dashboard/summary');
      return response.data;
    },
    staleTime: 2 * 60 * 1000, // 2 minutes
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
  });
};

// Get department metrics query
export const useDepartmentMetrics = (department: string) => {
  return useQuery({
    queryKey: ['dashboard', 'departments', department],
    queryFn: async () => {
      const response = await api.get(
        `/dashboard/departments/${department}/metrics`
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    enabled: !!department,
  });
};

// Get real-time alerts query
export const useRealTimeAlerts = () => {
  return useQuery({
    queryKey: ['dashboard', 'alerts'],
    queryFn: async () => {
      const response = await api.get('/dashboard/alerts');
      return response.data;
    },
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 30 * 1000, // Refetch every 30 seconds
  });
};

// Get performance trends query
export const usePerformanceTrends = (
  metric: string,
  period: string = '30d'
) => {
  return useQuery({
    queryKey: ['dashboard', 'trends', metric, period],
    queryFn: async () => {
      const response = await api.get('/dashboard/trends', {
        params: { metric, period },
      });
      return response.data;
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
    enabled: !!metric,
  });
};
