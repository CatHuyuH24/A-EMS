'use client';

import Link from 'next/link';
import { ROUTES } from '@/lib/constants';

const quickActions = [
  {
    name: 'New Chat',
    description: 'Ask AI about your business',
    href: ROUTES.CHAT,
    icon: ChatBubbleLeftIcon,
    color: 'bg-blue-500 hover:bg-blue-600',
  },
  {
    name: 'Generate Report',
    description: 'Create a business report',
    href: ROUTES.REPORTS,
    icon: DocumentTextIcon,
    color: 'bg-green-500 hover:bg-green-600',
  },
  {
    name: 'View Sales',
    description: 'Check sales metrics',
    href: ROUTES.SALES,
    icon: CurrencyDollarIcon,
    color: 'bg-purple-500 hover:bg-purple-600',
  },
  {
    name: 'HR Dashboard',
    description: 'Manage employees',
    href: ROUTES.HR,
    icon: UsersIcon,
    color: 'bg-orange-500 hover:bg-orange-600',
  },
];

// Hero Icons components
function ChatBubbleLeftIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z"
      />
    </svg>
  );
}

function DocumentTextIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
      />
    </svg>
  );
}

function CurrencyDollarIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 6v12m-3-2.818.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12s-1.536-.219-2.121-.659c-1.172-.879-1.172-2.303 0-3.182C10.464 7.781 11.232 7.562 12 7.562s1.536.219 2.121.659L15 9M12 6c-.552 0-1 .448-1 1s.448 1 1 1 1-.448 1-1-.448-1-1-1Z"
      />
    </svg>
  );
}

function UsersIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z"
      />
    </svg>
  );
}

export default function QuickActions() {
  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
          Quick Actions
        </h3>
        <div className="grid grid-cols-1 gap-4">
          {quickActions.map((action) => {
            const IconComponent = action.icon;

            return (
              <Link
                key={action.name}
                href={action.href}
                className="group relative rounded-lg p-4 transition-all hover:shadow-md"
              >
                <div className="flex items-center space-x-3">
                  <div
                    className={`flex-shrink-0 inline-flex items-center justify-center h-10 w-10 rounded-lg text-white transition-colors ${action.color}`}
                  >
                    <IconComponent className="h-5 w-5" aria-hidden="true" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <h4 className="text-sm font-medium text-gray-900 group-hover:text-gray-600">
                      {action.name}
                    </h4>
                    <p className="text-sm text-gray-500">
                      {action.description}
                    </p>
                  </div>
                  <div className="flex-shrink-0">
                    <svg
                      className="h-5 w-5 text-gray-400 group-hover:text-gray-600 transition-colors"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Additional actions */}
      <div className="bg-gray-50 px-4 py-4 sm:px-6">
        <div className="flex justify-between items-center">
          <div className="text-sm">
            <span className="font-medium text-gray-900">Need help?</span>
            <span className="text-gray-500 ml-1">
              Try asking the AI assistant
            </span>
          </div>
          <Link
            href={ROUTES.CHAT}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            Ask AI
          </Link>
        </div>
      </div>
    </div>
  );
}
