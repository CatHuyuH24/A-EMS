# API Specification (Overall)

_Last updated: 14/09/2025_

This document provides a preliminary specification for the RESTful APIs that will power the A-EMS application. This is a living document and will be updated as development progresses.

**Base URL:** `/api/v1`

## Logging & Monitoring

All API endpoints implement comprehensive logging for monitoring, debugging, and security purposes:

- **Request Tracking**: Each API request includes correlation IDs for end-to-end tracing
- **Security Logging**: Authentication attempts, authorization failures, and security events are logged
- **Performance Monitoring**: Response times, error rates, and service health metrics are tracked
- **Error Handling**: API errors return structured error responses and trigger appropriate frontend notifications

For detailed logging implementation and error handling patterns, see [Logging Guide](./Logging_Guide.md).

---

## 1. Auth Service (`/auth`)

Handles user authentication and authorization.

---

### `POST /auth/login`

- **Description:** Authenticates a user and returns a JWT.
- **Request Body:**
  ```json
  {
    "email": "ceo@example.com",
    "password": "securepassword123"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **Error Response (401 Unauthorized):**
  ```json
  {
    "detail": "Incorrect email or password"
  }
  ```

---

### `POST /auth/register`

- **Description:** Registers a new user. This endpoint is designed for administrative use and does not include UI registration forms. New users must be added through administrative interfaces or API calls.
- **Authentication:** Requires admin-level JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "email": "newuser@example.com",
    "password": "strongpassword456",
    "full_name": "New User",
    "role": "executive",
    "department": "C-Suite",
    "permissions": ["dashboard:read", "reports:read", "ai:chat"],
    "require_mfa": true,
    "send_welcome_email": true
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "id": "user_uuid_123",
    "email": "newuser@example.com",
    "full_name": "New User",
    "role": "executive",
    "department": "C-Suite",
    "permissions": ["dashboard:read", "reports:read", "ai:chat"],
    "mfa_enabled": false,
    "mfa_setup_required": true,
    "created_at": "2025-09-14T10:30:00Z"
  }
  ```
- **Error Response (403 Forbidden):**
  ```json
  {
    "detail": "Insufficient permissions to create users"
  }
  ```
- **Error Response (409 Conflict):**
  ```json
  {
    "detail": "User with this email already exists"
  }
  ```

---

### `POST /auth/logout`

- **Description:** Invalidates the current user session and JWT token.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:** Empty
- **Success Response (200 OK):**
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

---

### `GET /auth/verify`

- **Description:** Verifies the validity of the current JWT token and returns user information.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Success Response (200 OK):**
  ```json
  {
    "user": {
      "id": "user_uuid_123",
      "email": "user@example.com",
      "full_name": "User Name",
      "role": "executive",
      "permissions": ["dashboard:read", "reports:read", "ai:chat"],
      "mfa_enabled": true
    },
    "token_valid": true,
    "expires_at": "2025-09-14T18:30:00Z"
  }
  ```

---

### `POST /auth/change-password`

- **Description:** Changes the user's password. Requires current password verification.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "current_password": "oldpassword123",
    "new_password": "newstrongpassword456",
    "confirm_password": "newstrongpassword456"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Password updated successfully"
  }
  ```
- **Error Response (400 Bad Request):**
  ```json
  {
    "detail": "Current password is incorrect"
  }
  ```
- **Error Response (422 Unprocessable Entity):**
  ```json
  {
    "detail": "Password does not meet security requirements"
  }
  ```

---

### `POST /auth/forgot-password`

- **Description:** Initiates password reset process by sending reset email.
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Password reset email sent if account exists"
  }
  ```

---

### `POST /auth/reset-password`

- **Description:** Resets password using token from email.
- **Request Body:**
  ```json
  {
    "reset_token": "jwt_reset_token_from_email",
    "new_password": "newstrongpassword789",
    "confirm_password": "newstrongpassword789"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Password reset successfully"
  }
  ```
- **Error Response (400 Bad Request):**
  ```json
  {
    "detail": "Invalid or expired reset token"
  }
  ```

---

## 1.1. Multi-Factor Authentication (MFA)

### `GET /auth/mfa/status`

- **Description:** Returns current MFA configuration status for the authenticated user.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Success Response (200 OK):**
  ```json
  {
    "mfa_enabled": true,
    "methods": [
      {
        "type": "totp",
        "enabled": true,
        "backup_codes_remaining": 8
      },
      {
        "type": "sms",
        "enabled": false,
        "phone_number": null
      }
    ],
    "setup_required": false
  }
  ```

---

### `POST /auth/mfa/setup/totp`

- **Description:** Initiates TOTP (Time-based One-Time Password) setup process.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Success Response (200 OK):**
  ```json
  {
    "secret": "JBSWY3DPEHPK3PXP",
    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "manual_entry_key": "JBSWY3DPEHPK3PXP",
    "backup_codes": [
      "123456789",
      "987654321",
      "456789123",
      "789123456",
      "321654987",
      "654987321",
      "147258369",
      "963852741"
    ]
  }
  ```

---

### `POST /auth/mfa/verify/totp`

- **Description:** Verifies TOTP code during setup or authentication.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "code": "123456",
    "setup_mode": false
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "verified": true,
    "message": "TOTP code verified successfully"
  }
  ```
- **Error Response (400 Bad Request):**
  ```json
  {
    "detail": "Invalid TOTP code"
  }
  ```

---

### `POST /auth/mfa/enable`

- **Description:** Enables MFA for the user after successful TOTP verification.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "totp_code": "123456"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "MFA enabled successfully",
    "backup_codes": [
      "123456789",
      "987654321",
      "456789123",
      "789123456",
      "321654987",
      "654987321",
      "147258369",
      "963852741"
    ]
  }
  ```

---

### `POST /auth/mfa/disable`

- **Description:** Disables MFA for the user. Requires password confirmation.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "password": "userpassword123",
    "totp_code": "123456"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "MFA disabled successfully"
  }
  ```

---

### `POST /auth/mfa/regenerate-backup-codes`

- **Description:** Generates new backup codes and invalidates old ones.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "totp_code": "123456"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "backup_codes": [
      "123456789",
      "987654321",
      "456789123",
      "789123456",
      "321654987",
      "654987321",
      "147258369",
      "963852741"
    ]
  }
  ```

---

## 1.2. OAuth 2.0 / OIDC Authentication with Google

### `GET /auth/oauth/google/login`

- **Description:** Redirects user to Google OAuth 2.0 authorization server.
- **Query Parameters:**
  - `redirect_uri` (string, optional): Post-login redirect URL. Defaults to dashboard.
- **Success Response (302 Found):**
  - Redirects to Google OAuth authorization URL
  - URL format: `https://accounts.google.com/oauth/authorize?client_id=...&redirect_uri=...&scope=openid%20email%20profile&response_type=code&state=...`

---

### `POST /auth/oauth/google/callback`

- **Description:** Handles OAuth callback from Google and exchanges authorization code for tokens.
- **Request Body:**
  ```json
  {
    "code": "authorization_code_from_google",
    "state": "random_state_parameter"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": "user_uuid_123",
      "email": "user@gmail.com",
      "full_name": "User Name",
      "picture": "https://lh3.googleusercontent.com/...",
      "google_id": "google_user_id_123",
      "role": "executive",
      "permissions": ["dashboard:read", "reports:read", "ai:chat"],
      "mfa_enabled": false,
      "first_login": false
    }
  }
  ```
- **Error Response (400 Bad Request):**
  ```json
  {
    "detail": "Invalid authorization code or state parameter"
  }
  ```
- **Error Response (403 Forbidden):**
  ```json
  {
    "detail": "Google account not authorized for this system"
  }
  ```

---

### `POST /auth/oauth/google/link`

- **Description:** Links existing user account with Google OAuth.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "google_access_token": "google_oauth_access_token"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Google account linked successfully",
    "google_email": "user@gmail.com"
  }
  ```

---

### `DELETE /auth/oauth/google/unlink`

- **Description:** Unlinks Google OAuth from user account.
- **Authentication:** Requires valid JWT token in Authorization header.
- **Request Body:**
  ```json
  {
    "password": "userpassword123"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Google account unlinked successfully"
  }
  ```

---

## 2. Domain-Specific Data Services

To align with a microservices architecture, the general `/data` service is broken down into domain-specific services. Each service manages its own data and exposes a dedicated set of endpoints.

---

### 2.1. Sales Service (`/sales`)

Provides comprehensive access to sales-related data, performance metrics, forecasts, and customer analytics.

#### `GET /sales/overview`

- **Description:** Retrieves key sales metrics and KPIs for a given period.
- **Query Parameters:**
  - `period` (string, optional): "daily", "weekly", "monthly", "quarterly", "yearly". Defaults to "monthly".
- **Success Response (200 OK):**
  ```json
  {
    "total_revenue": 1250000,
    "new_deals": 45,
    "win_rate": "28%",
    "average_deal_size": 27777,
    "pipeline_value": 890000,
    "conversion_rate": "3.2%",
    "customer_acquisition_cost": 1200,
    "customer_lifetime_value": 15000
  }
  ```

#### `GET /sales/performance`

- **Description:** Retrieves sales performance data over time for trend analysis.
- **Query Parameters:**
  - `startDate` (string, ISO 8601)
  - `endDate` (string, ISO 8601)
  - `granularity` (string): "daily", "weekly", "monthly".
- **Success Response (200 OK):**
  ```json
  {
    "data": [
      {
        "date": "2023-01-31",
        "revenue": 85000,
        "deals": 30,
        "pipeline": 150000
      },
      {
        "date": "2023-02-28",
        "revenue": 92000,
        "deals": 35,
        "pipeline": 180000
      }
    ]
  }
  ```

#### `GET /sales/pipeline`

- **Description:** Retrieves current sales pipeline data by stage.
- **Success Response (200 OK):**
  ```json
  {
    "pipeline_stages": [
      { "stage": "Prospect", "count": 120, "value": 2400000 },
      { "stage": "Qualified", "count": 85, "value": 1700000 },
      { "stage": "Proposal", "count": 32, "value": 960000 },
      { "stage": "Negotiation", "count": 15, "value": 450000 }
    ],
    "total_pipeline_value": 5510000,
    "weighted_pipeline": 1653000
  }
  ```

#### `GET /sales/customers`

- **Description:** Retrieves customer analytics and segmentation data.
- **Query Parameters:**
  - `segment` (string, optional): "new", "returning", "churned", "at_risk"
- **Success Response (200 OK):**
  ```json
  {
    "total_customers": 1250,
    "new_customers_this_period": 45,
    "customer_segments": [
      { "segment": "Enterprise", "count": 150, "revenue_contribution": "65%" },
      { "segment": "SMB", "count": 800, "revenue_contribution": "25%" },
      { "segment": "Startup", "count": 300, "revenue_contribution": "10%" }
    ],
    "churn_rate": "2.1%",
    "retention_rate": "97.9%"
  }
  ```

#### `GET /sales/forecast`

- **Description:** Retrieves sales forecast data for planning.
- **Query Parameters:**
  - `horizon` (string): "30d", "90d", "1y"
- **Success Response (200 OK):**
  ```json
  {
    "forecast_period": "90d",
    "predicted_revenue": 3750000,
    "confidence_interval": { "lower": 3400000, "upper": 4100000 },
    "monthly_breakdown": [
      { "month": "2023-10", "predicted": 1200000, "confidence": "high" },
      { "month": "2023-11", "predicted": 1250000, "confidence": "medium" },
      { "month": "2023-12", "predicted": 1300000, "confidence": "medium" }
    ]
  }
  ```

#### `GET /sales/territories`

- **Description:** Retrieves sales performance by geographical territories.
- **Success Response (200 OK):**
  ```json
  {
    "territories": [
      {
        "region": "North America",
        "revenue": 5200000,
        "deals": 145,
        "growth": "+12%"
      },
      { "region": "Europe", "revenue": 3800000, "deals": 98, "growth": "+8%" },
      {
        "region": "Asia Pacific",
        "revenue": 2100000,
        "deals": 67,
        "growth": "+25%"
      },
      {
        "region": "Latin America",
        "revenue": 900000,
        "deals": 23,
        "growth": "+5%"
      }
    ]
  }
  ```

---

### 2.2. Finance Service (`/finance`)

Provides comprehensive access to financial data, KPIs, budgeting, cash flow, and expense management.

#### `GET /finance/kpis`

- **Description:** Retrieves top-level financial KPIs and health indicators.
- **Query Parameters:**
  - `period` (string, optional): "monthly", "quarterly", "yearly". Defaults to "monthly".
- **Success Response (200 OK):**
  ```json
  {
    "kpis": [
      {
        "name": "Gross Margin",
        "value": "65%",
        "change": "+1.2%",
        "target": "70%"
      },
      {
        "name": "Net Profit",
        "value": 450000,
        "change": "+8.1%",
        "target": 500000
      },
      {
        "name": "Operating Margin",
        "value": "18%",
        "change": "+0.8%",
        "target": "20%"
      },
      { "name": "EBITDA", "value": 890000, "change": "+12%", "target": 1000000 }
    ],
    "financial_health_score": 85,
    "cash_runway_months": 18
  }
  ```

#### `GET /finance/cash-flow`

- **Description:** Retrieves detailed cash flow analysis and projections.
- **Query Parameters:**
  - `period` (string, optional): "monthly", "quarterly"
- **Success Response (200 OK):**
  ```json
  {
    "current_cash": 2500000,
    "cash_flow": {
      "operating": 350000,
      "investing": -125000,
      "financing": 50000,
      "net": 275000
    },
    "monthly_data": [
      {
        "month": "2023-07",
        "inflow": 1200000,
        "outflow": 950000,
        "net": 250000
      },
      {
        "month": "2023-08",
        "inflow": 1350000,
        "outflow": 1025000,
        "net": 325000
      }
    ],
    "burn_rate": 180000,
    "runway_months": 18
  }
  ```

#### `GET /finance/expenses`

- **Description:** Retrieves expense breakdown and analysis by category.
- **Query Parameters:**
  - `category` (string, optional): "operational", "marketing", "rd", "administrative"
  - `period` (string, optional): "monthly", "quarterly"
- **Success Response (200 OK):**
  ```json
  {
    "total_expenses": 850000,
    "categories": [
      {
        "category": "Personnel",
        "amount": 520000,
        "percentage": 61.2,
        "change": "+5%"
      },
      {
        "category": "Marketing",
        "amount": 128000,
        "percentage": 15.1,
        "change": "+12%"
      },
      {
        "category": "Operations",
        "amount": 95000,
        "percentage": 11.2,
        "change": "-2%"
      },
      {
        "category": "R&D",
        "amount": 75000,
        "percentage": 8.8,
        "change": "+8%"
      },
      {
        "category": "Administrative",
        "amount": 32000,
        "percentage": 3.7,
        "change": "+1%"
      }
    ],
    "cost_per_employee": 4250,
    "expense_trends": "increasing"
  }
  ```

#### `GET /finance/budget`

- **Description:** Retrieves budget vs actual performance analysis.
- **Query Parameters:**
  - `department` (string, optional): specific department filter
- **Success Response (200 OK):**
  ```json
  {
    "overall_variance": -2.1,
    "departments": [
      {
        "department": "Sales",
        "budget": 200000,
        "actual": 185000,
        "variance": -7.5,
        "status": "under"
      },
      {
        "department": "Marketing",
        "budget": 150000,
        "actual": 162000,
        "variance": +8.0,
        "status": "over"
      },
      {
        "department": "R&D",
        "budget": 300000,
        "actual": 295000,
        "variance": -1.7,
        "status": "on_track"
      }
    ],
    "quarterly_forecast": 2850000
  }
  ```

#### `GET /finance/revenue-recognition`

- **Description:** Retrieves revenue recognition and deferred revenue data.
- **Success Response (200 OK):**
  ```json
  {
    "recognized_revenue": 1200000,
    "deferred_revenue": 450000,
    "unbilled_revenue": 125000,
    "monthly_recognition": [
      { "month": "2023-10", "amount": 380000, "contracts": 25 },
      { "month": "2023-11", "amount": 420000, "contracts": 28 },
      { "month": "2023-12", "amount": 465000, "contracts": 32 }
    ],
    "arr": 14400000,
    "mrr": 1200000
  }
  ```

#### `GET /finance/profitability`

- **Description:** Retrieves profitability analysis by product, customer segment, or region.
- **Query Parameters:**
  - `breakdown` (string): "product", "customer_segment", "region"
- **Success Response (200 OK):**
  ```json
  {
    "breakdown_type": "product",
    "overall_margin": 42.5,
    "items": [
      {
        "name": "Enterprise Suite",
        "revenue": 800000,
        "costs": 320000,
        "margin": 60.0
      },
      {
        "name": "Professional Plan",
        "revenue": 450000,
        "costs": 270000,
        "margin": 40.0
      },
      {
        "name": "Starter Plan",
        "revenue": 200000,
        "costs": 160000,
        "margin": 20.0
      }
    ]
  }
  ```

---

### 2.3. HR Service (`/hr`)

Provides comprehensive access to human resources data, including workforce analytics, recruitment, performance, and organizational health metrics.

#### `GET /hr/headcount`

- **Description:** Retrieves current employee headcount, demographics, and turnover analytics.
- **Query Parameters:**
  - `department` (string, optional): filter by specific department
  - `level` (string, optional): "junior", "senior", "manager", "executive"
- **Success Response (200 OK):**
  ```json
  {
    "total_employees": 520,
    "new_hires_this_month": 15,
    "departures_this_month": 8,
    "turnover_rate": "1.8%",
    "by_department": [
      { "department": "Engineering", "count": 185, "growth": "+8%" },
      { "department": "Sales", "count": 95, "growth": "+12%" },
      { "department": "Marketing", "count": 42, "growth": "+5%" },
      { "department": "Operations", "count": 85, "growth": "+3%" },
      { "department": "HR", "count": 25, "growth": "+2%" }
    ],
    "demographics": {
      "gender_distribution": { "male": 62, "female": 35, "other": 3 },
      "age_distribution": { "under_30": 45, "30_50": 48, "over_50": 7 },
      "tenure_distribution": {
        "under_1y": 28,
        "1_3y": 35,
        "3_5y": 22,
        "over_5y": 15
      }
    }
  }
  ```

#### `GET /hr/recruitment`

- **Description:** Retrieves recruitment pipeline and hiring metrics.
- **Query Parameters:**
  - `position` (string, optional): filter by specific job position
  - `status` (string, optional): "open", "in_progress", "filled", "cancelled"
- **Success Response (200 OK):**
  ```json
  {
    "open_positions": 28,
    "applications_received": 145,
    "interviews_scheduled": 42,
    "offers_extended": 12,
    "offers_accepted": 8,
    "time_to_hire_avg": 35,
    "cost_per_hire": 3500,
    "positions": [
      {
        "role": "Senior Software Engineer",
        "status": "open",
        "applications": 25,
        "stage": "screening"
      },
      {
        "role": "Product Manager",
        "status": "in_progress",
        "applications": 18,
        "stage": "final_interview"
      },
      {
        "role": "Sales Director",
        "status": "offer_extended",
        "applications": 12,
        "stage": "negotiation"
      }
    ],
    "sourcing_channels": [
      { "channel": "Job Boards", "applications": 58, "success_rate": "12%" },
      { "channel": "Referrals", "applications": 35, "success_rate": "28%" },
      { "channel": "LinkedIn", "applications": 32, "success_rate": "15%" },
      { "channel": "Recruiters", "applications": 20, "success_rate": "35%" }
    ]
  }
  ```

#### `GET /hr/performance`

- **Description:** Retrieves employee performance metrics and analytics.
- **Query Parameters:**
  - `period` (string, optional): "quarterly", "annually"
  - `department` (string, optional): filter by department
- **Success Response (200 OK):**
  ```json
  {
    "overall_performance_score": 4.2,
    "performance_distribution": {
      "exceeds_expectations": 15,
      "meets_expectations": 68,
      "needs_improvement": 14,
      "unsatisfactory": 3
    },
    "by_department": [
      { "department": "Engineering", "avg_score": 4.3, "top_performers": 28 },
      { "department": "Sales", "avg_score": 4.1, "top_performers": 15 },
      { "department": "Marketing", "avg_score": 4.0, "top_performers": 8 }
    ],
    "goal_completion_rate": 87,
    "promotion_rate": "12%",
    "training_completion": 92
  }
  ```

#### `GET /hr/compensation`

- **Description:** Retrieves compensation and benefits analytics.
- **Query Parameters:**
  - `level` (string, optional): employee level filter
  - `benchmark` (boolean, optional): include market benchmark data
- **Success Response (200 OK):**
  ```json
  {
    "total_payroll": 3200000,
    "average_salary": 95000,
    "salary_ranges": [
      { "level": "Junior", "min": 65000, "max": 85000, "avg": 75000 },
      { "level": "Senior", "min": 85000, "max": 120000, "avg": 102000 },
      { "level": "Manager", "min": 120000, "max": 160000, "avg": 140000 },
      { "level": "Director", "min": 160000, "max": 220000, "avg": 190000 }
    ],
    "benefits_cost_per_employee": 18500,
    "equity_participation_rate": 85,
    "pay_equity_score": 0.96
  }
  ```

#### `GET /hr/engagement`

- **Description:** Retrieves employee engagement and satisfaction metrics.
- **Success Response (200 OK):**
  ```json
  {
    "engagement_score": 7.8,
    "satisfaction_score": 8.1,
    "nps_score": 42,
    "survey_participation": 89,
    "key_metrics": [
      { "metric": "Work-Life Balance", "score": 7.5, "trend": "improving" },
      { "metric": "Career Development", "score": 7.2, "trend": "stable" },
      { "metric": "Management Quality", "score": 8.0, "trend": "improving" },
      { "metric": "Compensation Satisfaction", "score": 7.8, "trend": "stable" }
    ],
    "retention_risk": {
      "high_risk": 12,
      "medium_risk": 35,
      "low_risk": 473
    }
  }
  ```

#### `GET /hr/training`

- **Description:** Retrieves training and development analytics.
- **Success Response (200 OK):**
  ```json
  {
    "total_training_hours": 2840,
    "avg_hours_per_employee": 28,
    "training_programs": [
      {
        "program": "Leadership Development",
        "participants": 45,
        "completion": 92,
        "satisfaction": 8.5
      },
      {
        "program": "Technical Skills",
        "participants": 185,
        "completion": 87,
        "satisfaction": 8.2
      },
      {
        "program": "Compliance Training",
        "participants": 520,
        "completion": 98,
        "satisfaction": 7.5
      }
    ],
    "certification_achievements": 67,
    "training_budget_utilization": 78,
    "skill_gap_analysis": [
      {
        "skill": "Data Analysis",
        "current_level": 6.2,
        "target_level": 8.0,
        "gap": 1.8
      },
      {
        "skill": "Project Management",
        "current_level": 7.1,
        "target_level": 8.5,
        "gap": 1.4
      }
    ]
  }
  ```

---

### 2.4. Products Service (`/products`)

Provides comprehensive access to product management, inventory tracking, and product analytics.

#### `GET /products/overview`

- **Description:** Retrieves key product metrics and KPIs including inventory levels, top performers, and stock alerts.
- **Query Parameters:**
  - `category` (string, optional): Filter by product category
  - `status` (string, optional): "active", "discontinued", "out_of_stock"
- **Success Response (200 OK):**
  ```json
  {
    "total_products": 1250,
    "active_products": 1180,
    "out_of_stock": 15,
    "low_stock_alerts": 45,
    "total_inventory_value": 2500000,
    "top_performing_products": [
      {
        "id": "PRD001",
        "name": "Enterprise Suite",
        "revenue": 890000,
        "units_sold": 450
      },
      {
        "id": "PRD002",
        "name": "Professional Plan",
        "revenue": 650000,
        "units_sold": 320
      }
    ]
  }
  ```

#### `GET /products/inventory`

- **Description:** Retrieves detailed inventory management data including stock levels, warehouse locations, and movement history.
- **Query Parameters:**
  - `warehouse` (string, optional): Filter by warehouse location
  - `alert_level` (string, optional): "low", "critical", "normal"
- **Success Response (200 OK):**
  ```json
  {
    "warehouses": [
      {
        "location": "Main Warehouse",
        "total_products": 850,
        "capacity_used": "78%"
      },
      {
        "location": "Secondary Warehouse",
        "total_products": 400,
        "capacity_used": "45%"
      }
    ],
    "inventory_items": [
      {
        "product_id": "PRD001",
        "name": "Enterprise Suite",
        "current_stock": 125,
        "reserved": 25,
        "available": 100,
        "reorder_point": 50,
        "status": "normal",
        "last_restocked": "2023-09-01"
      }
    ],
    "stock_movements": [
      {
        "date": "2023-09-12",
        "type": "inbound",
        "quantity": 50,
        "reason": "purchase_order"
      },
      {
        "date": "2023-09-10",
        "type": "outbound",
        "quantity": 15,
        "reason": "sale"
      }
    ]
  }
  ```

#### `GET /products/analytics`

- **Description:** Retrieves product performance analytics including sales trends, profitability, and customer preferences.
- **Query Parameters:**
  - `period` (string, optional): "monthly", "quarterly", "yearly"
  - `metric` (string, optional): "revenue", "units", "profit_margin"
- **Success Response (200 OK):**
  ```json
  {
    "performance_metrics": [
      {
        "product_id": "PRD001",
        "name": "Enterprise Suite",
        "revenue": 890000,
        "units_sold": 450,
        "profit_margin": 65.5,
        "growth_rate": "+12%",
        "customer_satisfaction": 4.6
      }
    ],
    "category_analysis": [
      { "category": "Software", "revenue_share": 78, "growth": "+15%" },
      { "category": "Services", "revenue_share": 22, "growth": "+8%" }
    ],
    "demand_forecast": [
      { "month": "2023-10", "predicted_demand": 120, "confidence": "high" },
      { "month": "2023-11", "predicted_demand": 135, "confidence": "medium" }
    ]
  }
  ```

#### `GET /products/catalog`

- **Description:** Retrieves product catalog with detailed product information, pricing, and availability.
- **Query Parameters:**
  - `search` (string, optional): Search term for product name or description
  - `category` (string, optional): Filter by category
  - `price_range` (string, optional): "under_100", "100_500", "over_500"
- **Success Response (200 OK):**
  ```json
  {
    "products": [
      {
        "id": "PRD001",
        "name": "Enterprise Suite",
        "description": "Comprehensive business management solution",
        "category": "Software",
        "price": 299.99,
        "currency": "USD",
        "availability": "in_stock",
        "stock_quantity": 125,
        "specifications": {
          "version": "2.1",
          "license_type": "annual",
          "support_level": "premium"
        },
        "images": ["url1", "url2"],
        "created_date": "2023-01-15",
        "last_updated": "2023-09-01"
      }
    ],
    "filters": {
      "categories": ["Software", "Services", "Hardware"],
      "price_ranges": ["under_100", "100_500", "over_500"]
    }
  }
  ```

#### `GET /products/lifecycle`

- **Description:** Retrieves product lifecycle analytics including launch performance, maturity metrics, and retirement planning.
- **Success Response (200 OK):**
  ```json
  {
    "lifecycle_stages": [
      {
        "product_id": "PRD001",
        "name": "Enterprise Suite",
        "stage": "growth",
        "days_in_market": 245,
        "stage_metrics": {
          "adoption_rate": "85%",
          "market_penetration": "12%",
          "customer_feedback": 4.6
        }
      }
    ],
    "retirement_candidates": [
      {
        "product_id": "PRD099",
        "name": "Legacy Tool",
        "reason": "low_demand",
        "replacement_product": "PRD001"
      }
    ]
  }
  ```

---

### 2.5. Risk Management Service (`/risk`)

Provides comprehensive risk assessment, compliance monitoring, and regulatory reporting capabilities.

#### `GET /risk/overview`

- **Description:** Retrieves enterprise risk dashboard with key risk indicators and compliance status.
- **Query Parameters:**
  - `risk_level` (string, optional): "low", "medium", "high", "critical"
  - `category` (string, optional): "operational", "financial", "compliance", "cybersecurity"
- **Success Response (200 OK):**
  ```json
  {
    "overall_risk_score": 3.2,
    "risk_trend": "decreasing",
    "active_risks": 45,
    "critical_risks": 3,
    "compliance_status": "compliant",
    "last_assessment": "2023-09-01",
    "risk_categories": [
      {
        "category": "Operational",
        "score": 2.8,
        "count": 15,
        "trend": "stable"
      },
      {
        "category": "Financial",
        "score": 3.5,
        "count": 12,
        "trend": "improving"
      },
      { "category": "Compliance", "score": 2.1, "count": 8, "trend": "stable" },
      {
        "category": "Cybersecurity",
        "score": 4.2,
        "count": 10,
        "trend": "worsening"
      }
    ]
  }
  ```

#### `GET /risk/assessments`

- **Description:** Retrieves detailed risk assessments including risk register, impact analysis, and mitigation strategies.
- **Query Parameters:**
  - `status` (string, optional): "active", "closed", "monitoring"
  - `owner` (string, optional): Filter by risk owner department
- **Success Response (200 OK):**
  ```json
  {
    "risk_assessments": [
      {
        "risk_id": "RSK001",
        "title": "Data Breach Risk",
        "category": "cybersecurity",
        "probability": 0.3,
        "impact": 4.5,
        "risk_score": 1.35,
        "status": "active",
        "owner": "IT Department",
        "mitigation_plan": "Implement additional security measures",
        "due_date": "2023-10-15",
        "last_reviewed": "2023-09-01"
      }
    ],
    "mitigation_actions": [
      {
        "action_id": "ACT001",
        "description": "Deploy advanced threat detection",
        "status": "in_progress",
        "completion": 65,
        "due_date": "2023-09-30"
      }
    ]
  }
  ```

#### `GET /risk/compliance`

- **Description:** Retrieves compliance monitoring data including regulatory requirements, audit findings, and remediation status.
- **Query Parameters:**
  - `regulation` (string, optional): "GDPR", "SOX", "HIPAA", "PCI_DSS"
  - `status` (string, optional): "compliant", "non_compliant", "pending"
- **Success Response (200 OK):**
  ```json
  {
    "compliance_summary": {
      "overall_status": "compliant",
      "compliance_score": 94.2,
      "regulations_tracked": 12,
      "active_violations": 2,
      "pending_remediation": 3
    },
    "regulatory_requirements": [
      {
        "regulation": "GDPR",
        "status": "compliant",
        "last_audit": "2023-08-15",
        "next_review": "2023-11-15",
        "compliance_score": 98.5,
        "findings": []
      },
      {
        "regulation": "SOX",
        "status": "pending",
        "last_audit": "2023-07-01",
        "next_review": "2023-10-01",
        "compliance_score": 89.2,
        "findings": [
          {
            "finding_id": "SOX001",
            "severity": "medium",
            "description": "Internal control documentation incomplete",
            "remediation_plan": "Complete documentation by Q4",
            "due_date": "2023-12-31"
          }
        ]
      }
    ]
  }
  ```

#### `GET /risk/incidents`

- **Description:** Retrieves incident management data including security incidents, operational disruptions, and response metrics.
- **Query Parameters:**
  - `severity` (string, optional): "low", "medium", "high", "critical"
  - `status` (string, optional): "open", "investigating", "resolved", "closed"
- **Success Response (200 OK):**
  ```json
  {
    "incident_summary": {
      "total_incidents": 125,
      "open_incidents": 8,
      "avg_resolution_time": "4.2 hours",
      "escalated_incidents": 2
    },
    "recent_incidents": [
      {
        "incident_id": "INC001",
        "title": "System Performance Degradation",
        "severity": "high",
        "category": "operational",
        "status": "investigating",
        "reported_date": "2023-09-12T10:30:00Z",
        "assigned_to": "IT Operations",
        "impact": "Service slowdown affecting 30% of users",
        "estimated_resolution": "2023-09-12T16:00:00Z"
      }
    ]
  }
  ```

#### `GET /risk/monitoring`

- **Description:** Retrieves real-time risk monitoring data including key risk indicators, early warning signals, and trend analysis.
- **Success Response (200 OK):**
  ```json
  {
    "monitoring_dashboard": {
      "risk_indicators": [
        {
          "indicator": "System Uptime",
          "current_value": 99.8,
          "threshold": 99.5,
          "status": "normal",
          "trend": "stable"
        },
        {
          "indicator": "Security Threats",
          "current_value": 15,
          "threshold": 10,
          "status": "warning",
          "trend": "increasing"
        }
      ],
      "early_warnings": [
        {
          "warning_id": "WRN001",
          "type": "threshold_breach",
          "indicator": "Failed Login Attempts",
          "severity": "medium",
          "triggered_at": "2023-09-12T14:30:00Z"
        }
      ]
    }
  }
  ```

---

### 2.6. Reports Service (`/reports`)

Provides comprehensive reporting capabilities including report generation, scheduling, export, and distribution.

#### `GET /reports`

- **Description:** Retrieves list of available reports with metadata and access permissions.
- **Query Parameters:**
  - `category` (string, optional): "financial", "operational", "compliance", "custom"
  - `access_level` (string, optional): "public", "restricted", "confidential"
- **Success Response (200 OK):**
  ```json
  {
    "available_reports": [
      {
        "report_id": "RPT001",
        "name": "Monthly Financial Summary",
        "category": "financial",
        "description": "Comprehensive financial performance report",
        "access_level": "restricted",
        "last_generated": "2023-09-01T09:00:00Z",
        "next_scheduled": "2023-10-01T09:00:00Z",
        "available_formats": ["PDF", "Excel", "CSV"],
        "data_sources": ["finance", "sales"],
        "estimated_generation_time": "2 minutes"
      }
    ],
    "report_categories": [
      { "category": "financial", "count": 12 },
      { "category": "operational", "count": 18 },
      { "category": "compliance", "count": 8 },
      { "category": "custom", "count": 5 }
    ]
  }
  ```

#### `POST /reports/generate`

- **Description:** Generates a custom report based on specified parameters and data sources.
- **Request Body:**
  ```json
  {
    "report_name": "Q3 Performance Analysis",
    "data_sources": ["sales", "finance", "hr"],
    "date_range": {
      "start_date": "2023-07-01",
      "end_date": "2023-09-30"
    },
    "filters": {
      "departments": ["sales", "marketing"],
      "regions": ["north_america", "europe"]
    },
    "format": "PDF",
    "delivery_method": "email",
    "recipients": ["ceo@company.com", "cfo@company.com"]
  }
  ```
- **Success Response (202 Accepted):**
  ```json
  {
    "generation_id": "GEN_20230912_001",
    "status": "queued",
    "estimated_completion": "2023-09-12T15:30:00Z",
    "progress_url": "/reports/status/GEN_20230912_001"
  }
  ```

#### `GET /reports/status/{generation_id}`

- **Description:** Retrieves the generation status of a requested report.
- **Success Response (200 OK):**
  ```json
  {
    "generation_id": "GEN_20230912_001",
    "status": "completed",
    "progress": 100,
    "started_at": "2023-09-12T15:00:00Z",
    "completed_at": "2023-09-12T15:25:00Z",
    "download_url": "/reports/download/GEN_20230912_001",
    "expires_at": "2023-09-19T15:25:00Z"
  }
  ```

#### `GET /reports/download/{generation_id}`

- **Description:** Downloads the generated report file.
- **Success Response (200 OK):**
  - Returns the report file as a binary download with appropriate content-type headers.

#### `GET /reports/scheduled`

- **Description:** Retrieves information about scheduled reports and their execution history.
- **Success Response (200 OK):**
  ```json
  {
    "scheduled_reports": [
      {
        "schedule_id": "SCH001",
        "report_id": "RPT001",
        "name": "Monthly Financial Summary",
        "frequency": "monthly",
        "next_execution": "2023-10-01T09:00:00Z",
        "recipients": ["ceo@company.com", "cfo@company.com"],
        "format": "PDF",
        "status": "active"
      }
    ],
    "execution_history": [
      {
        "execution_id": "EXE001",
        "schedule_id": "SCH001",
        "executed_at": "2023-09-01T09:00:00Z",
        "status": "success",
        "duration": "3 minutes",
        "file_size": "2.5 MB"
      }
    ]
  }
  ```

#### `POST /reports/schedule`

- **Description:** Creates a new scheduled report with specified frequency and delivery options.
- **Request Body:**
  ```json
  {
    "report_id": "RPT001",
    "frequency": "monthly",
    "day_of_month": 1,
    "time": "09:00",
    "timezone": "UTC",
    "format": "PDF",
    "delivery_method": "email",
    "recipients": ["ceo@company.com", "cfo@company.com"]
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "schedule_id": "SCH002",
    "status": "active",
    "next_execution": "2023-10-01T09:00:00Z"
  }
  ```

---

## 3. AI Orchestrator Service (`/ai`)

Handles interactions with the AI assistant.

---

### `POST /ai/chat`

- **Description:** Sends a user's natural language query to the AI and gets a response.
- **Request Body:**
  ```json
  {
    "query": "What were our total sales in Q2?",
    "session_id": "session_uuid_abc"
  }
  ```
- **Success Response (200 OK):**
  The response can be complex and may include text, data, or instructions for the frontend to render a chart.
  ```json
  {
    "response_type": "composite", // or "text", "chart"
    "text_response": "Sales for Q2 were $450,000. Here is the breakdown by region:",
    "chart_data": {
      "type": "bar",
      "data": [
        { "region": "North", "sales": 200000 },
        { "region": "South", "sales": 150000 },
        { "region": "West", "sales": 100000 }
      ]
    }
  }
  ```
