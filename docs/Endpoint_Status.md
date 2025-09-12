# Endpoint Status Tracker

This document tracks the development status of all API endpoints for the A-EMS project.

**Status Legend:**

- `Not Started`: The endpoint has been defined but no work has begun.
- `In Progress`: The endpoint is actively being developed.
- `Completed`: Development is complete, and initial testing has passed.
- `Blocked`: Development is blocked by a dependency.

---

## Auth Service

| Method | Endpoint         | Description             | Status        | Notes |
| ------ | ---------------- | ----------------------- | ------------- | ----- |
| POST   | `/auth/login`    | Authenticate user       | `Not Started` |       |
| POST   | `/auth/register` | Register a new user     | `Not Started` |       |
| POST   | `/auth/refresh`  | Refresh an access token | `Not Started` |       |

---

## Data Services

### Sales Service

| Method | Endpoint             | Description               | Status        | Notes |
| ------ | -------------------- | ------------------------- | ------------- | ----- |
| GET    | `/sales/overview`    | Get key sales metrics     | `Not Started` |       |
| GET    | `/sales/performance` | Get sales trend data      | `Not Started` |       |
| GET    | `/sales/pipeline`    | Get sales pipeline data   | `Not Started` |       |
| GET    | `/sales/customers`   | Get customer analytics    | `Not Started` |       |
| GET    | `/sales/forecast`    | Get sales forecast        | `Not Started` |       |
| GET    | `/sales/territories` | Get territory performance | `Not Started` |       |

### Finance Service

| Method | Endpoint                       | Description                  | Status        | Notes |
| ------ | ------------------------------ | ---------------------------- | ------------- | ----- |
| GET    | `/finance/kpis`                | Get top-level financial KPIs | `Not Started` |       |
| GET    | `/finance/cash-flow`           | Get cash flow analysis       | `Not Started` |       |
| GET    | `/finance/expenses`            | Get expense breakdown        | `Not Started` |       |
| GET    | `/finance/budget`              | Get budget vs actual         | `Not Started` |       |
| GET    | `/finance/revenue-recognition` | Get revenue recognition data | `Not Started` |       |
| GET    | `/finance/profitability`       | Get profitability analysis   | `Not Started` |       |

### HR Service

| Method | Endpoint           | Description               | Status        | Notes |
| ------ | ------------------ | ------------------------- | ------------- | ----- |
| GET    | `/hr/headcount`    | Get employee headcount    | `Not Started` |       |
| GET    | `/hr/recruitment`  | Get recruitment metrics   | `Not Started` |       |
| GET    | `/hr/performance`  | Get performance analytics | `Not Started` |       |
| GET    | `/hr/compensation` | Get compensation data     | `Not Started` |       |
| GET    | `/hr/engagement`   | Get engagement metrics    | `Not Started` |       |
| GET    | `/hr/training`     | Get training analytics    | `Not Started` |       |

---

## AI Orchestrator Service

| Method | Endpoint   | Description            | Status        | Notes                          |
| ------ | ---------- | ---------------------- | ------------- | ------------------------------ |
| POST   | `/ai/chat` | Post a query to the AI | `Not Started` | Blocked by DeepSeek API access |

---
