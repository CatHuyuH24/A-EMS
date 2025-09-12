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

## Data API Service

| Method | Endpoint                | Description             | Status        | Notes |
| ------ | ----------------------- | ----------------------- | ------------- | ----- |
| GET    | `/data/kpis`            | Get main dashboard KPIs | `Not Started` |       |
| GET    | `/data/sales-over-time` | Get sales trend data    | `Not Started` |       |
| GET    | `/data/sales-by-region` | Get sales breakdown     | `Not Started` |       |

---

## AI Orchestrator Service

| Method | Endpoint   | Description            | Status        | Notes                          |
| ------ | ---------- | ---------------------- | ------------- | ------------------------------ |
| POST   | `/ai/chat` | Post a query to the AI | `Not Started` | Blocked by DeepSeek API access |

---
