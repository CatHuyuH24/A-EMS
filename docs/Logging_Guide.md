# Logging Guide

_Last updated: 14/09/2025_

This document provides comprehensive logging strategies and implementation guidelines for the A-EMS (AI-Driven Enterprise Management System) microservices architecture.

---

## Table of Contents

- [Logging Principles & Levels](#logging-principles--levels)
- [Backend Logging (Microservices & Docker)](#backend-logging-microservices--docker)
- [Frontend Logging & Error Notification](#frontend-logging--error-notification)
- [Example Log Entries](#example-log-entries)
- [Log Management & Monitoring](#log-management--security)
- [External references](#external-references)

---

## Logging Principles & Levels

### Core Principles

1. **Structured Logging**: All logs must use JSON format for machine readability and consistent parsing
2. **Centralized Logging**: All service logs aggregated through Docker logging drivers
3. **Correlation IDs**: Every request tracked with unique identifiers across all services
4. **Sensitive Data Protection**: No PII, passwords, tokens, or sensitive business data in logs
5. **Performance Awareness**: Logging must not significantly impact application performance
6. **Contextual Information**: Logs include sufficient context for debugging and monitoring

### Log Levels (Python logging standard)

- **DEBUG**: Detailed information for diagnosing problems (development only)
- **INFO**: General information about system operation and user actions
- **WARNING**: Something unexpected happened, but the application continues
- **ERROR**: Serious problem occurred, functionality may be affected
- **CRITICAL**: Very serious error occurred, application may abort

### Log Level Usage Guidelines

```python
# DEBUG - Development debugging only
logger.debug(f"Processing user request", extra={
    "user_id": user_id,
    "endpoint": "/api/v1/sales/overview"
})

# INFO - Normal operations, audit trail
logger.info("User authentication successful", extra={
    "correlation_id": correlation_id,
    "user_id": user_id,
    "auth_method": "jwt",
    "ip_address": request_ip
})

# WARNING - Unexpected but recoverable situations
logger.warning("API rate limit approaching", extra={
    "correlation_id": correlation_id,
    "user_id": user_id,
    "current_requests": 95,
    "rate_limit": 100
})

# ERROR - Functionality impacted
logger.error("Database connection failed", extra={
    "correlation_id": correlation_id,
    "service": "sales_service",
    "error_type": "connection_timeout",
    "retry_attempt": 3
})

# CRITICAL - System-wide impact
logger.critical("Service unable to start", extra={
    "service": "auth_service",
    "error_type": "startup_failure",
    "config_file": "/app/config.yml"
})
```

---

## Backend Logging (Microservices & Docker)

### Implementation Strategy

#### 1. Python FastAPI Service Logging Setup

**Requirements:**

- `python-json-logger` for structured JSON logging
- `uvicorn` with JSON log formatter
- Custom correlation ID middleware

**Configuration per service:**

```python
# logging_config.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging(service_name: str, log_level: str = "INFO"):
    """Configure structured logging for microservice"""

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove default handlers
    logger.handlers.clear()

    # JSON formatter for structured logs
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (captured by Docker)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set service context
    logging.basicConfig(level=getattr(logging, log_level.upper()))

    return logger

# Usage in main.py
from logging_config import setup_logging

logger = setup_logging("auth_service", "INFO")
```

**Correlation ID Middleware:**

```python
# middleware/correlation.py
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or extract correlation ID
        correlation_id = (
            request.headers.get("x-correlation-id") or
            str(uuid.uuid4())
        )

        # Add to request state
        request.state.correlation_id = correlation_id

        # Log request start
        logger.info("Request started", extra={
            "correlation_id": correlation_id,
            "method": request.method,
            "url": str(request.url),
            "user_agent": request.headers.get("user-agent"),
            "ip_address": request.client.host
        })

        response = await call_next(request)

        # Add correlation ID to response headers
        response.headers["x-correlation-id"] = correlation_id

        # Log request completion
        logger.info("Request completed", extra={
            "correlation_id": correlation_id,
            "status_code": response.status_code,
            "response_time_ms": "calculated_by_middleware"
        })

        return response
```

#### 2. Service-Specific Logging Requirements

**Auth Service:**

- All authentication attempts (success/failure)
- MFA operations (setup, verification)
- Password changes and security events
- OAuth flows and token operations
- Session management events

**Business Services (Sales, Finance, HR, etc.):**

- Data retrieval and aggregation operations
- Cache hits/misses for performance monitoring
- External API calls and responses
- Data processing errors and warnings

**AI Orchestrator Service:**

- DeepSeek API interactions (request/response times)
- Context aggregation from multiple services
- Prompt construction and optimization
- AI response processing and formatting

#### 3. Docker Logging Configuration

**docker-compose.yml logging setup:**

```yaml
version: '3.8'
services:
  auth_service:
    build: ./backend/services/auth_service
    logging:
      driver: 'json-file'
      options:
        max-size: '100m'
        max-file: '5'
        labels: 'service=auth_service,environment=development'
    environment:
      - LOG_LEVEL=INFO
      - SERVICE_NAME=auth_service

  api_gateway:
    build: ./backend/api_gateway
    logging:
      driver: 'json-file'
      options:
        max-size: '100m'
        max-file: '5'
        labels: 'service=api_gateway,environment=development'
    environment:
      - LOG_LEVEL=INFO
      - SERVICE_NAME=api_gateway

  # Repeat for all services...
```

#### 4. Log Aggregation & Rotation

**Container Log Management:**

- JSON file driver with size and rotation limits
- Structured log forwarding to centralized systems (future: ELK stack, Splunk, etc.)
- Docker log labels for service identification

---

## Frontend Logging & Error Notification

### General Principles

1. **User-Centric**: Error messages must be understandable and actionable for business users
2. **Error Type Distinction**: Differentiate between system errors, validation errors, and permission issues
3. **Progressive Disclosure**: Show summary first, details on request
4. **Consistent UX**: Uniform toast notification styling and positioning

### Implementation Steps

#### 1. Global Error Boundary (React)

**Installation:**

```bash
npm install react-hot-toast @types/react-hot-toast
```

**Global Error Boundary Setup:**

```typescript
// components/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';
import toast from 'react-hot-toast';
import { logger } from '@/lib/logger';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log the error for monitoring
    logger.error('Unhandled React error', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString(),
    });

    // Show user-friendly error toast
    toast.error(
      'Something unexpected happened. Please refresh the page or try again.',
      {
        duration: 6000,
        position: 'top-right',
        id: 'global-error', // Prevent duplicates
      }
    );
  }

  public render() {
    if (this.state.hasError) {
      // Fallback UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg
                  className="h-8 w-8 text-red-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-gray-800">
                  Application Error
                </h3>
                <div className="mt-2 text-sm text-gray-500">
                  <p>
                    We're sorry, but something went wrong. Please refresh the
                    page to continue.
                  </p>
                </div>
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => window.location.reload()}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Refresh Page
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

#### 2. API Error Handling in Data-Fetching Hooks

**Custom API Hook with Error Handling:**

```typescript
// hooks/useApiCall.ts
import { useState, useCallback } from 'react';
import toast from 'react-hot-toast';
import { logger } from '@/lib/logger';

interface ApiError {
  message: string;
  status?: number;
  code?: string;
  details?: Record<string, any>;
}

interface ApiCallOptions {
  showSuccessToast?: boolean;
  successMessage?: string;
  customErrorHandler?: (error: ApiError) => void;
}

export function useApiCall<T>(
  apiFunction: (...args: any[]) => Promise<T>,
  options: ApiCallOptions = {}
) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [data, setData] = useState<T | null>(null);

  const execute = useCallback(
    async (...args: any[]) => {
      setLoading(true);
      setError(null);

      try {
        const result = await apiFunction(...args);
        setData(result);

        if (options.showSuccessToast) {
          toast.success(
            options.successMessage || 'Operation completed successfully'
          );
        }

        return result;
      } catch (err: any) {
        const apiError: ApiError = {
          message: err.message || 'An unexpected error occurred',
          status: err.status,
          code: err.code,
          details: err.details,
        };

        setError(apiError);

        // Log error for debugging
        logger.error('API call failed', {
          endpoint: apiFunction.name,
          error: apiError,
          timestamp: new Date().toISOString(),
        });

        // Handle different error types with appropriate toasts
        if (options.customErrorHandler) {
          options.customErrorHandler(apiError);
        } else {
          handleApiError(apiError);
        }

        throw apiError;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction, options]
  );

  return { execute, loading, error, data };
}

// Specialized error notification handlers
function handleApiError(error: ApiError) {
  const { status, code, message } = error;

  switch (status) {
    case 401:
      toast.error('Your session has expired. Please log in again.', {
        duration: 5000,
        icon: '🔐',
        position: 'top-right',
      });
      // Redirect to login
      window.location.href = '/login';
      break;

    case 403:
      toast(
        (t) => (
          <div className="flex">
            <div className="flex-1">
              <p className="font-medium text-gray-900">Permission Denied</p>
              <p className="text-sm text-gray-500">
                You don't have permission to perform this action.
              </p>
            </div>
          </div>
        ),
        {
          duration: 4000,
          icon: '⚠️',
          position: 'top-right',
          style: {
            background: '#FEF3C7',
            border: '1px solid #F59E0B',
          },
        }
      );
      break;

    case 422:
      // Validation errors - contextual toasts
      toast.error(message || 'Please check your input and try again.', {
        duration: 4000,
        icon: '❌',
        position: 'top-right',
        style: {
          background: '#FEE2E2',
          border: '1px solid #EF4444',
        },
      });
      break;

    case 500:
    case 502:
    case 503:
    case 504:
      toast.error(
        'Server error. Our team has been notified. Please try again later.',
        {
          duration: 6000,
          icon: '🔧',
          position: 'top-right',
        }
      );
      break;

    default:
      toast.error(message || 'Something went wrong. Please try again.', {
        duration: 4000,
        position: 'top-right',
      });
  }
}
```

#### 3. Frontend Logging Setup

**Client-Side Logger:**

```typescript
// lib/logger.ts
interface LogEntry {
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  timestamp: string;
  userId?: string;
  sessionId?: string;
  url?: string;
  userAgent?: string;
  extra?: Record<string, any>;
}

class ClientLogger {
  private sessionId: string;

  constructor() {
    this.sessionId = this.generateSessionId();
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private createLogEntry(
    level: LogEntry['level'],
    message: string,
    extra?: Record<string, any>
  ): LogEntry {
    return {
      level,
      message,
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId,
      url: window.location.href,
      userAgent: navigator.userAgent,
      extra,
    };
  }

  debug(message: string, extra?: Record<string, any>) {
    const entry = this.createLogEntry('debug', message, extra);
    console.debug('[DEBUG]', entry);
  }

  info(message: string, extra?: Record<string, any>) {
    const entry = this.createLogEntry('info', message, extra);
    console.info('[INFO]', entry);

    // Send to monitoring service in production
    if (process.env.NODE_ENV === 'production') {
      this.sendToBackend(entry);
    }
  }

  warn(message: string, extra?: Record<string, any>) {
    const entry = this.createLogEntry('warn', message, extra);
    console.warn('[WARN]', entry);
    this.sendToBackend(entry);
  }

  error(message: string, extra?: Record<string, any>) {
    const entry = this.createLogEntry('error', message, extra);
    console.error('[ERROR]', entry);
    this.sendToBackend(entry);
  }

  private async sendToBackend(entry: LogEntry) {
    try {
      await fetch('/api/v1/logs/frontend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify(entry),
      });
    } catch (error) {
      // Silently fail - don't break app due to logging
      console.warn('Failed to send log to backend:', error);
    }
  }
}

export const logger = new ClientLogger();
```

#### 4. Toast Notification Setup

**Toast Provider Setup (in \_app.tsx):**

```typescript
// pages/_app.tsx
import { Toaster } from 'react-hot-toast';
import { ErrorBoundary } from '@/components/ErrorBoundary';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ErrorBoundary>
      <Component {...pageProps} />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#fff',
            color: '#374151',
            boxShadow:
              '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            border: '1px solid #E5E7EB',
            borderRadius: '0.5rem',
          },
          success: {
            iconTheme: {
              primary: '#10B981',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#EF4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </ErrorBoundary>
  );
}
```

---

## Example Log Entries

### Backend Service Logs

#### Authentication Success

```json
{
  "timestamp": "2025-09-14T10:30:45.123Z",
  "level": "INFO",
  "service": "auth_service",
  "correlation_id": "req_123e4567-e89b-12d3-a456-426614174000",
  "message": "User authentication successful",
  "user_id": "user_456",
  "auth_method": "password",
  "mfa_enabled": true,
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0..."
}
```

#### Database Connection Error

```json
{
  "timestamp": "2025-09-14T10:31:12.456Z",
  "level": "ERROR",
  "service": "sales_service",
  "correlation_id": "req_789f0123-g45h-67i8-j901-234567890123",
  "message": "Database connection failed",
  "error_type": "connection_timeout",
  "database_host": "postgres_db",
  "retry_attempt": 2,
  "max_retries": 3,
  "operation": "fetch_sales_overview"
}
```

#### AI Service Integration

```json
{
  "timestamp": "2025-09-14T10:32:08.789Z",
  "level": "INFO",
  "service": "ai_orchestrator",
  "correlation_id": "req_abc1234d-e5f6-78g9-h012-345678901234",
  "message": "DeepSeek API call successful",
  "user_id": "user_456",
  "prompt_tokens": 150,
  "response_tokens": 320,
  "response_time_ms": 2340,
  "context_services": ["sales_service", "finance_service"],
  "query_type": "comparative_analysis"
}
```

### Frontend Logs

#### User Navigation

```json
{
  "level": "info",
  "message": "User navigated to dashboard",
  "timestamp": "2025-09-14T10:33:15.123Z",
  "sessionId": "session_1726305195123_abc123",
  "userId": "user_456",
  "url": "https://a-ems.app.com/dashboard",
  "userAgent": "Mozilla/5.0...",
  "extra": {
    "previous_page": "/login",
    "load_time_ms": 890
  }
}
```

#### API Error on Frontend

```json
{
  "level": "error",
  "message": "API call failed: Sales data fetch",
  "timestamp": "2025-09-14T10:34:22.456Z",
  "sessionId": "session_1726305195123_abc123",
  "userId": "user_456",
  "url": "https://a-ems.app.com/dashboard",
  "extra": {
    "endpoint": "/api/v1/sales/overview",
    "status": 500,
    "correlation_id": "req_def5678e-f90g-12h3-i456-789012345678",
    "user_action": "dashboard_refresh"
  }
}
```

---

## Log Management & Security

### Management

- **Console Output**: All services log to stdout/stderr (captured by Docker)
- **Local Storage**: JSON file driver with log rotation (100MB max, 5 files)
- **Real-time Viewing**: `docker-compose logs -f [service_name]`

### Security & Privacy

- **Data Masking**: Automatic PII redaction in log aggregation pipeline
- **Access Control**: Role-based access to log viewing interfaces
- **Audit Logging**: Separate secure logging for compliance events
- **Encryption**: Log data encrypted at rest and in transit

---

## External references

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [FastAPI Logging Configuration](https://fastapi.tiangolo.com/tutorial/logging/)
- [React Error Boundaries](https://reactjs.org/docs/error-boundaries.html)
- [React Hot Toast Documentation](https://react-hot-toast.com/)
- [Docker Logging Configuration](https://docs.docker.com/config/containers/logging/)
