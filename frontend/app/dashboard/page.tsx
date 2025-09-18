'use client'

import { useDashboardOverview } from '@/hooks/api'
import DashboardLayout from '@/components/layout/dashboard-layout'
import MetricsCard from '@/components/dashboard/metrics-card'
import ActivityFeed from '@/components/dashboard/activity-feed'
import AIInsights from '@/components/dashboard/ai-insights'
import QuickActions from '@/components/dashboard/quick-actions'

export default function DashboardPage() {
  const { data: overview, isLoading, error } = useDashboardOverview()

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    )
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">
                Error loading dashboard
              </h3>
              <div className="mt-2 text-sm text-red-700">
                Unable to load dashboard data. Please try refreshing the page.
              </div>
            </div>
          </div>
        </div>
      </DashboardLayout>
    )
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
        {overview?.metrics && (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <MetricsCard
              title="Total Revenue"
              value={overview.metrics.totalRevenue}
              format="currency"
              trend={{ value: 12.5, direction: 'up' }}
              icon="currency-dollar"
              color="green"
            />
            <MetricsCard
              title="Total Customers"
              value={overview.metrics.totalCustomers}
              format="number"
              trend={{ value: 8.2, direction: 'up' }}
              icon="users"
              color="blue"
            />
            <MetricsCard
              title="Total Employees"
              value={overview.metrics.totalEmployees}
              format="number"
              trend={{ value: 2.1, direction: 'up' }}
              icon="user-group"
              color="purple"
            />
            <MetricsCard
              title="Active Projects"
              value={overview.metrics.activeProjects}
              format="number"
              trend={{ value: -3.4, direction: 'down' }}
              icon="briefcase"
              color="orange"
            />
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* AI Insights */}
            {overview?.aiInsights && (
              <AIInsights insights={overview.aiInsights} />
            )}

            {/* Recent Activities */}
            {overview?.recentActivities && (
              <ActivityFeed activities={overview.recentActivities} />
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <QuickActions />

            {/* Notifications */}
            {overview?.notifications && (
              <div className="bg-white shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Recent Notifications
                  </h3>
                  <div className="mt-5">
                    <div className="flow-root">
                      <ul className="-mb-8">
                        {overview.notifications.slice(0, 5).map((notification, index) => (
                          <li key={notification.id}>
                            <div className="relative pb-8">
                              {index !== overview.notifications.slice(0, 5).length - 1 && (
                                <span
                                  className="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200"
                                  aria-hidden="true"
                                />
                              )}
                              <div className="relative flex items-start space-x-3">
                                <div className={`relative flex items-center justify-center w-10 h-10 rounded-full ${
                                  notification.type === 'success' ? 'bg-green-100' :
                                  notification.type === 'warning' ? 'bg-yellow-100' :
                                  notification.type === 'error' ? 'bg-red-100' :
                                  'bg-blue-100'
                                }`}>
                                  <div className={`w-5 h-5 ${
                                    notification.type === 'success' ? 'text-green-600' :
                                    notification.type === 'warning' ? 'text-yellow-600' :
                                    notification.type === 'error' ? 'text-red-600' :
                                    'text-blue-600'
                                  }`}>
                                    {notification.type === 'success' && (
                                      <svg fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                      </svg>
                                    )}
                                    {notification.type === 'warning' && (
                                      <svg fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                      </svg>
                                    )}
                                    {notification.type === 'error' && (
                                      <svg fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                                      </svg>
                                    )}
                                    {notification.type === 'info' && (
                                      <svg fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                                      </svg>
                                    )}
                                  </div>
                                </div>
                                <div className="min-w-0 flex-1">
                                  <div>
                                    <div className="text-sm">
                                      <p className="font-medium text-gray-900">
                                        {notification.title}
                                      </p>
                                    </div>
                                    <p className="mt-0.5 text-sm text-gray-500">
                                      {notification.message}
                                    </p>
                                    <div className="mt-2 text-xs text-gray-400">
                                      {new Date(notification.timestamp).toLocaleDateString()}
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}