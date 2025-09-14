# Project Information and Scope

_Last updated: 14/09/2025_

## 1. Project Overview

- **Project Name:** A-EMS (AI-Driven Enterprise Management System)
- **Vision:** To build a "Digital Chief of Staff," an intelligent virtual assistant that provides CEOs and senior leadership with comprehensive information, deep insights, and real-time, data-driven decision-making capabilities.
- **Core Goal:** To transform raw business data into actionable intelligence, presented through an intuitive and interactive web application.

## 2. Core Features

1.  **Executive Dashboard:** A comprehensive, real-time visualization of key business metrics across all domains:

    - **Sales Analytics:** Revenue tracking, pipeline management, customer analytics, territory performance, and sales forecasting
    - **Financial Management:** KPIs monitoring, cash flow analysis, budget tracking, expense management, revenue recognition, and profitability analysis
    - **HR Analytics:** Workforce metrics, recruitment analytics, performance management, compensation analysis, engagement tracking, and training effectiveness
    - **Product Management:** Inventory tracking, product analytics, lifecycle management, catalog management, and demand forecasting
    - **Risk & Compliance:** Enterprise risk assessment, compliance monitoring, incident management, regulatory reporting, and risk analytics
    - **Business Intelligence:** Custom report generation, scheduled reporting, export capabilities, and real-time dashboard visualization

2.  **AI Chat Assistant (DeepSeek Integration):** An advanced conversational interface allowing users to:

    - Ask natural language questions about any business domain
    - Request custom visualizations and analysis
    - Get predictive insights and recommendations
    - Maintain conversation context for follow-up questions

3.  **Microservices Backend:** A scalable architecture supporting:
    - Domain-specific data services (Sales, Finance, HR, Products, Risk, Reports)
    - Intelligent AI orchestration and data aggregation across all business domains
    - Real-time data processing and updates
    - Advanced analytics and comprehensive reporting capabilities
    - Enterprise risk management and compliance monitoring

## 3. Technology Stack

- **Frontend:** Next.js, TypeScript, Tailwind CSS, Recharts (for visualizations).
- **Backend:** Python, FastAPI, PostgreSQL.
- **Infrastructure:** Docker for containerization and consistent development/deployment environments.
- **AI:** DeepSeek model for the intelligent assistant feature.

## 4. Project Scope

### In-Scope:

- Development of comprehensive executive dashboard with domain-specific analytics (Sales, Finance, HR, Products, Risk, Reports)
- Advanced AI chat interface with contextual understanding and visualization capabilities
- Implementation of microservices-based backend with domain-specific services:
  - Sales Service: Pipeline, forecasting, customer analytics, territory management
  - Finance Service: KPIs, cash flow, budgeting, expense tracking, profitability analysis
  - HR Service: Workforce analytics, recruitment, performance, compensation, engagement
  - Products Service: Inventory management, product analytics, lifecycle tracking, demand forecasting
  - Risk Service: Enterprise risk assessment, compliance monitoring, incident management, regulatory reporting
  - Reports Service: Custom report generation, scheduling, export capabilities, real-time dashboards
- Containerization of the entire application stack using Docker
- Integration with DeepSeek AI for intelligent business insights across all domains and comprehensive reporting
- Advanced data visualization with interactive charts and real-time updates
- **Enterprise-Grade Authentication & Security System:**
  - Multi-Factor Authentication (MFA) with TOTP and backup codes
  - OAuth 2.0 / OIDC integration with Google for seamless authentication
  - Comprehensive password management (change, reset, forgot password flows)
  - Administrative user management with role-based access control (RBAC)
  - Session management with device tracking and remote termination capabilities
  - Security audit logging and compliance monitoring
  - Brute force protection and account lockout mechanisms
  - JWT-based authentication with secure token handling
- Mobile-responsive design with accessibility compliance

### Out-of-Scope (for initial phase):

- Advanced, multi-source data ETL (Extract, Transform, Load) pipelines.
- Mobile application development.
- Multi-tenancy architecture.
- On-premise deployment (initial focus is on a containerized cloud-ready solution).

## 5. Proposed Directory Structure

To ensure a clean and scalable project, the following directory structure is proposed:

```
/
├── backend/                  # Python/FastAPI Microservices
│   ├── services/             # Individual microservices
│   │   ├── auth_service/
│   │   ├── sales_service/
│   │   ├── finance_service/
│   │   ├── hr_service/
│   │   ├── products_service/
│   │   ├── risk_service/
│   │   ├── reports_service/
│   │   └── ai_service/
│   ├── shared/               # Shared libraries/modules
│   └── Dockerfile            # Base Dockerfile for services
├── frontend/                 # Next.js/TypeScript Application
│   ├── app/                  # Next.js 13+ app directory
│   ├── components/           # React components
│   ├── lib/                  # Helper functions and libraries
│   ├── public/               # Static assets
│   └── Dockerfile
├── infra/                    # Infrastructure configurations
│   └── docker-compose.yml    # Main Docker Compose file for all services
├── docs/                     # Project documentation
│   ├── Project_Info_Scope.md
│   ├── Project_Plan.md
│   ├── System_Architecture.md
│   ├── UI_UX.md
│   ├── API_Specification.md
│   ├── User_Story.md
│   ├── User_Journey.md
│   ├── User_Acceptance_Criteria.md
│   └── Endpoint_Status.md
└── README.md                 # Main project README
```
