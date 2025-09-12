# API Specification (Initial Draft)

This document provides a preliminary specification for the RESTful APIs that will power the A-EMS application. This is a living document and will be updated as development progresses.

**Base URL:** `/api/v1`

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

- **Description:** Registers a new user.
- **Request Body:**
  ```json
  {
    "email": "newuser@example.com",
    "password": "strongpassword456",
    "full_name": "New User"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "id": "user_uuid_123",
    "email": "newuser@example.com",
    "full_name": "New User"
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
