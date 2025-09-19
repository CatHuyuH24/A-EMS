'use client';

import {
  useDashboardMetrics,
  useRecentActivities,
  useAIInsights,
} from '@/hooks';
import DashboardLayout from '@/components/layout/dashboard-layout';
import MetricsCard from '@/components/dashboard/metrics-card';
import ActivityFeed from '@/components/dashboard/activity-feed';
import AIInsights from '@/components/dashboard/ai-insights';
import QuickActions from '@/components/dashboard/quick-actions';

export default function DashboardPage() {
  const { data: metrics, isLoading: metricsLoading } = useDashboardMetrics();
  const { data: activities, isLoading: activitiesLoading } =
    useRecentActivities();
  const { data: insights, isLoading: insightsLoading } = useAIInsights();

  const isLoading = metricsLoading || activitiesLoading || insightsLoading;

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Welcome back! Here's what's happening with your business.
          </p>
        </div>

        {/* Metrics Cards */}
        {metrics && (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {metrics.map((metric: any, index: number) => (
              <MetricsCard
                key={index}
                title={metric.title}
                value={metric.value}
                format={metric.format}
                trend={metric.trend}
                icon={metric.icon}
                color={metric.color}
              />
            ))}
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* AI Insights */}
            {insights && <AIInsights insights={insights} />}

            {/* Recent Activities */}
            {activities && <ActivityFeed activities={activities} />}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <QuickActions />

            {/* Notifications */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Recent Notifications
                </h3>
                <div className="mt-5">
                  <p className="text-gray-500">No new notifications</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
