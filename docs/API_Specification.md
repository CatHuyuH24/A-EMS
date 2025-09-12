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

Provides access to sales-related data, trends, and forecasts.

#### `GET /sales/overview`

- **Description:** Retrieves key sales metrics for a given period.
- **Query Parameters:**
  - `period` (string, optional): "daily", "weekly", "monthly". Defaults to "monthly".
- **Success Response (200 OK):**
  ```json
  {
    "total_revenue": 1250000,
    "new_deals": 45,
    "win_rate": "28%",
    "average_deal_size": 27777
  }
  ```

#### `GET /sales/performance`

- **Description:** Retrieves sales performance data over time for charts.
- **Query Parameters:**
  - `startDate` (string, ISO 8601)
  - `endDate` (string, ISO 8601)
  - `granularity` (string): "daily", "weekly", "monthly".
- **Success Response (200 OK):**
  ```json
  {
    "data": [
      { "date": "2023-01-31", "revenue": 85000, "deals": 30 },
      { "date": "2023-02-28", "revenue": 92000, "deals": 35 }
    ]
  }
  ```

---

### 2.2. Finance Service (`/finance`)

Provides access to financial KPIs, cash flow, and expense data.

#### `GET /finance/kpis`

- **Description:** Retrieves top-level financial KPIs for the dashboard.
- **Success Response (200 OK):**
  ```json
  {
    "kpis": [
      { "name": "Gross Margin", "value": "65%", "change": "+1.2%" },
      { "name": "Net Profit", "value": 450000, "change": "+8.1%" },
      { "name": "Cash Flow", "value": 890000, "status": "healthy" }
    ]
  }
  ```

---

### 2.3. HR Service (`/hr`)

Provides access to human resources data like headcount and recruitment.

#### `GET /hr/headcount`

- **Description:** Retrieves current employee headcount and turnover rates.
- **Success Response (200 OK):**
  ```json
  {
    "total_employees": 520,
    "new_hires_this_month": 15,
    "turnover_rate": "1.8%"
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
