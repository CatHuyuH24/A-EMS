# Backend - Python/FastAPI Microservices Ecosystem

This directory contains all backend services for the A-EMS application, built using a microservices architecture with Python/FastAPI.

## Architecture

- **services/**: Domain-specific microservices
- **shared/**: Common utilities and libraries
- **api_gateway/**: Central API gateway and routing
- **scripts/**: Development and deployment scripts

## Services

- **auth_service**: Authentication & Security
- **sales_service**: Sales Domain (CRM, Pipeline, Analytics)
- **finance_service**: Finance Domain (Budget, Expenses, KPIs)
- **hr_service**: HR Domain (Employees, Recruitment)
- **products_service**: Products Domain (Catalog, Inventory)
- **risk_service**: Risk & Compliance Management
- **reports_service**: Reporting & Analytics Engine
- **ai_service**: AI Orchestrator (Chat, Context Management)

## Development

```bash
# Install dependencies for all services
python scripts/setup_dev.py

# Run tests
python scripts/run_tests.py

# Deploy services
python scripts/deploy.py
```
