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

## 2. Data API Service (`/data`)

Provides access to core business data. All endpoints require authentication.

---

### `GET /data/kpis`

- **Description:** Retrieves a summary of main Key Performance Indicators for the dashboard.
- **Query Parameters:**
  - `period` (string, optional): e.g., "monthly", "quarterly", "yearly". Defaults to "monthly".
- **Success Response (200 OK):**
  ```json
  {
    "kpis": [
      { "name": "Total Revenue", "value": 1200000, "change": "+5.2%" },
      { "name": "New Customers", "value": 10453, "change": "+2.1%" },
      { "name": "Churn Rate", "value": "2.1%", "change": "-0.5%" }
    ]
  }
  ```

---

### `GET /data/sales-over-time`

- **Description:** Retrieves data points for sales trends charts.
- **Query Parameters:**
  - `startDate` (string, ISO 8601): e.g., "2023-01-01"
  - `endDate` (string, ISO 8601): e.g., "2023-12-31"
  - `granularity` (string): "daily", "weekly", "monthly".
- **Success Response (200 OK):**
  ```json
  {
    "data": [
      { "date": "2023-01-31", "sales": 85000 },
      { "date": "2023-02-28", "sales": 92000 },
      { "date": "2023-03-31", "sales": 110000 }
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
