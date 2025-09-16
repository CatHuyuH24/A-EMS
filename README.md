# A-EMS (AI-Driven Enterprise Management System)

_Last updated: 14/09/2025_

A-EMS is a web application designed to serve as a "Digital Chief of Staff" for CEOs and senior leadership. It delivers comprehensive insights, real-time analytics, and AI-powered decision support through an intuitive dashboard and conversational assistant.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Core Features](#core-features)
- [Technology Stack](#technology-stack)
- [Directory Structure](#directory-structure)
- [UI/UX Guidelines](#uiux-guidelines)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

---

## Overview

A-EMS transforms raw business data into actionable intelligence, empowering leaders with:

- Holistic business insights across Sales, Finance, HR, Products, Risk, and Reporting
- Predictive analytics and forecasting
- Natural language query interface for complex analysis and reporting
- Real-time performance monitoring and alerting
- Data-driven recommendations and compliance insights
- Enterprise-grade security and authentication

For a detailed project scope, see [Project Information and Scope](./docs/Project_Info_Scope.md).

---

## System Architecture

A-EMS is built on a **microservices architecture** for scalability, resilience, and maintainability. The system is fully containerized using Docker and orchestrated with Docker Compose.

**Key Components:**

- **Frontend:** Next.js SPA with advanced chat interface and real-time streaming support
- **API Gateway:** Central routing with authentication, rate limiting, and request correlation
- **Backend Microservices:** Python/FastAPI services for Auth, Sales, Finance, HR, Products, Risk, Reports, and enhanced AI Orchestration
- **Database Infrastructure:**
  - PostgreSQL 15+ with Docker containerization and PgBouncer connection pooling
  - Database-per-Service pattern with shared core entities (authentication, tenants)
  - Enterprise security with row-level security policies and data encryption
  - Performance optimization with strategic indexing, partitioning, and query optimization
  - Automated backup and recovery systems with point-in-time recovery
- **AI Orchestrator Service:** Advanced conversational AI with:
  - Multi-turn conversation management and context preservation
  - Real-time streaming responses with WebSocket/SSE support
  - Session history and conversation analytics
  - Contextual business data integration and intelligent prompt engineering
  - Feedback loops for continuous improvement and quality tracking
- **AI Integration:** DeepSeek with sophisticated prompt engineering and business context injection

For architecture diagrams, data flow, and deployment details, see [System Architecture](./docs/System_Architecture.md).

---

## Core Features

### 🎯 Executive Dashboard

- **Real-time Analytics:** Customizable dashboards across all business domains
- **Interactive Visualizations:** Dynamic charts and KPIs with drill-down capabilities
- **Performance Monitoring:** Live tracking of critical business metrics
- **Custom Report Generation:** Automated scheduling and export functionality

### 🤖 Advanced AI Assistant

- **Multi-Turn Conversations:** Context-aware chat with session continuity
- **Natural Language Queries:** Ask complex business questions in plain English
- **Real-Time Streaming:** Live response generation for improved user experience
- **Contextual Suggestions:** Intelligent follow-up questions and analysis recommendations
- **Conversation Analytics:** Usage patterns and interaction quality tracking
- **Feedback System:** Continuous learning from user interactions
- **Business Context Integration:** Deep understanding of your enterprise data
- **Interactive Visualizations:** AI-generated charts and insights embedded in chat responses

### 🔐 Enterprise-Grade Security

- **Multi-Factor Authentication:** TOTP, backup codes, and device management
- **OAuth 2.0 / OIDC Integration:** Seamless Google authentication
- **Role-Based Access Control (RBAC):** Granular permissions and security policies
- **Session Management:** Comprehensive device tracking and security monitoring
- **Audit Logging:** Complete security event tracking and compliance reporting

### 📊 Comprehensive Business Intelligence

- **Sales Analytics:** Revenue tracking, pipeline management, performance forecasting
- **Financial Insights:** Cash flow, profitability, budget variance analysis
- **HR Metrics:** Employee performance, retention, recruitment analytics
- **Risk & Compliance:** Monitoring, incident tracking, regulatory reporting
- **Product Management:** Lifecycle analytics, inventory optimization, demand forecasting

### �️ Enterprise Database Architecture

- **PostgreSQL 15+:** Advanced database engine with full Docker containerization
- **Database-per-Service Pattern:** Microservices-optimized architecture with shared core entities
- **Performance Optimization:** Strategic indexing, time-series partitioning, and query optimization
- **Security & Compliance:** Row-level security policies, data encryption, and comprehensive audit trails
- **Connection Pooling:** PgBouncer for optimal performance and resource management
- **Backup & Recovery:** Automated backup systems with point-in-time recovery capabilities
- **Migration Management:** Version-controlled database migrations with rollback support
- **Multi-Tenant Ready:** Enterprise-grade tenant isolation and scalability

### �🔧 Advanced Technical Features

- **Structured Logging:** JSON-formatted logs with correlation ID tracking
- **Centralized Monitoring:** Real-time system health and performance tracking
- **Error Handling:** Comprehensive error management with user-friendly notifications
- **Mobile-Responsive Design:** Optimized experience across all devices
- **Accessibility Compliance:** WCAG 2.1 AA standards with keyboard navigation support

See [Project Information and Scope](./docs/Project_Info_Scope.md) for a full feature breakdown.

---

## Technology Stack

- **Frontend:** Next.js, TypeScript, Tailwind CSS, Recharts
- **Backend:** Python, FastAPI (microservices architecture)
- **Database:** PostgreSQL 15+ with advanced enterprise features
- **Database Infrastructure:** PgBouncer connection pooling, automated backups, performance monitoring
- **Infrastructure:** Docker containerization, Docker Compose orchestration
- **AI:** DeepSeek integration with intelligent context management

---

## Directory Structure

### Enterprise Microservices Architecture

The project follows a comprehensive microservices architecture optimized for scalability, maintainability, and AI-driven development:

```
/
├── backend/                           # Python/FastAPI Microservices Ecosystem
│   ├── services/                      # Domain-specific microservices
│   │   ├── auth_service/              # Authentication & Security
│   │   │   ├── app/                   # FastAPI application
│   │   │   │   ├── api/               # REST endpoints
│   │   │   │   ├── core/              # Business logic
│   │   │   │   ├── models/            # SQLAlchemy models
│   │   │   │   ├── schemas/           # Pydantic schemas
│   │   │   │   └── services/          # Service layer
│   │   │   ├── tests/                 # Unit & integration tests
│   │   │   ├── migrations/            # Database migrations
│   │   │   └── Dockerfile
│   │   ├── sales_service/             # Sales Domain (CRM, Pipeline, Analytics)
│   │   ├── finance_service/           # Finance Domain (Budget, Expenses, KPIs)
│   │   ├── hr_service/                # HR Domain (Employees, Recruitment)
│   │   ├── products_service/          # Products Domain (Catalog, Inventory)
│   │   ├── risk_service/              # Risk & Compliance Management
│   │   ├── reports_service/           # Reporting & Analytics Engine
│   │   └── ai_service/                # AI Orchestrator (Chat, Context Management)
│   ├── shared/                        # Shared Libraries & Utilities
│   │   ├── database/                  # Database utilities & migrations
│   │   │   ├── base.py                # Base database classes
│   │   │   ├── connection.py          # Connection pooling
│   │   │   ├── migrations/            # Migration management
│   │   │   └── models/                # Shared models (Users, Tenants)
│   │   ├── auth/                      # Authentication utilities
│   │   ├── logging/                   # Structured logging
│   │   ├── middleware/                # Shared middleware
│   │   └── utils/                     # Common utilities
│   ├── api_gateway/                   # API Gateway & Load Balancer
│   └── scripts/                       # Development & deployment scripts
├── frontend/                          # Next.js/TypeScript SPA
│   ├── app/                           # Next.js 13+ app directory
│   │   ├── (auth)/                    # Authentication routes
│   │   ├── dashboard/                 # Executive dashboard
│   │   ├── chat/                      # AI Chat interface
│   │   └── api/                       # API route handlers
│   ├── components/                    # React components library
│   │   ├── ui/                        # Base UI components
│   │   ├── auth/                      # Authentication components
│   │   ├── dashboard/                 # Dashboard widgets
│   │   ├── chat/                      # Chat interface
│   │   └── charts/                    # Data visualization
│   ├── lib/                           # Utilities & API clients
│   ├── hooks/                         # Custom React hooks
│   ├── store/                         # State management
│   └── styles/                        # Tailwind CSS styles
├── infra/                            # Infrastructure & DevOps
│   ├── docker/                       # Docker configurations
│   │   ├── docker-compose.yml        # Complete application stack
│   │   ├── docker-compose.dev.yml    # Development environment
│   │   └── docker-compose.prod.yml   # Production configuration
│   ├── database/                     # Database infrastructure
│   │   ├── init/                     # Database initialization scripts
│   │   │   ├── 01-extensions.sql     # PostgreSQL extensions
│   │   │   ├── 02-schemas.sql        # Database schemas
│   │   │   ├── 03-functions.sql      # Custom functions
│   │   │   └── 04-seed-data.sql      # Development data
│   │   ├── scripts/                  # Database management
│   │   │   ├── backup.sh             # Automated backups
│   │   │   ├── restore.sh            # Recovery procedures
│   │   │   ├── health_check.sh       # Health monitoring
│   │   │   └── performance_monitor.sh # Performance tracking
│   │   ├── config/                   # Database configurations
│   │   │   ├── postgresql.conf       # PostgreSQL settings
│   │   │   ├── pg_hba.conf          # Access control
│   │   │   └── pgbouncer.ini        # Connection pooling
│   │   └── Dockerfile.postgres       # Custom PostgreSQL image
│   ├── monitoring/                   # Observability stack
│   │   ├── prometheus/               # Metrics collection
│   │   ├── grafana/                  # Visualization dashboards
│   │   └── docker-compose.monitoring.yml
│   └── scripts/                      # Infrastructure automation
├── docs/                             # Comprehensive Documentation
│   ├── architecture/                 # System architecture docs
│   │   ├── System_Architecture.md
│   │   ├── Database_Schema.md        # Complete database design
│   │   └── Data_Dictionary.md        # Data specifications
│   ├── api/                          # API documentation
│   ├── development/                  # Developer guides
│   ├── deployment/                   # Deployment guides
│   └── [Additional documentation files...]
├── tests/                            # Comprehensive testing suite
│   ├── integration/                  # Cross-service integration tests
│   ├── e2e/                         # End-to-end testing
│   └── performance/                  # Load & performance testing
├── .github/workflows/                # CI/CD automation
├── scripts/                          # Project-wide automation
│   ├── setup.sh                      # Initial setup
│   ├── dev.sh                        # Development environment
│   ├── test.sh                       # Test runner
│   └── clean.sh                      # Resource cleanup
└── [Configuration files...]
```

### Architecture Highlights:

- **🏗️ Microservices**: Each business domain has its own independent service
- **🗄️ Database-per-Service**: Dedicated PostgreSQL schemas with shared core entities
- **🐳 Docker-First**: Complete containerization with development/production configs
- **🤖 AI-Ready**: Dedicated AI service with conversation management and context persistence
- **🔐 Enterprise Security**: Comprehensive authentication, authorization, and audit systems
- **📊 Observability**: Built-in monitoring, logging, and performance tracking
- **🚀 CI/CD Ready**: GitHub Actions integration for automated deployment
- **📚 Documentation**: Extensive documentation for enterprise maintenance

---

## UI/UX Guidelines

A-EMS prioritizes clarity, efficiency, and accessibility:

- **Sidebar navigation** with quick access to all domains
- **Dashboard**: Responsive grid of KPI cards, charts, and tables
- **AI Chat**: Modern messaging interface with embedded visualizations
- **Authentication**: Clean, multi-option login and MFA flows
- **Accessibility**: WCAG 2.1 AA compliance, keyboard navigation, screen reader support

For detailed wireframes, color palette, typography, and component specs, see [UI/UX Design Guidelines](./docs/UI_UX.md).

---

## Getting Started

### Prerequisites

- **Docker & Docker Compose** 24.0+ (for containerized deployment)
- **Node.js** 18+ (for local frontend development)
- **Python** 3.11+ (for local backend development)
- **PostgreSQL** 15+ client tools (optional, for direct database access)
- **Git** (for version control)

### Quick Start

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CatHuyuH24/A-EMS.git
   cd A-EMS
   ```

2. **Environment setup:**

   ```bash
   # Copy environment templates
   cp .env.example .env
   cp infra/docker/.env.example infra/docker/.env

   # Edit environment variables (database passwords, API keys, etc.)
   ```

3. **Initialize the complete application stack:**

   ```bash
   # Start all services (database, backend, frontend)
   docker-compose -f infra/docker/docker-compose.yml up --build
   ```

4. **Database initialization (first run):**

   ```bash
   # Wait for PostgreSQL to be ready, then run migrations
   docker-compose -f infra/docker/docker-compose.yml exec backend python -m shared.database.migrations.run_migrations

   # Optional: Load development seed data
   docker-compose -f infra/docker/docker-compose.yml exec backend python -m shared.database.seeds.run_seeds
   ```

5. **Access the application:**
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Database**: `localhost:5432` (Direct) / `localhost:6432` (PgBouncer)

### Development Workflow

#### Database Management

```bash
# Connect to database via PgBouncer (recommended)
psql -h localhost -p 6432 -U aems_user -d aems_db

# Direct PostgreSQL connection
psql -h localhost -p 5432 -U aems_user -d aems_db

# Run database migrations
docker-compose -f infra/docker/docker-compose.yml exec backend python -m shared.database.migrations.run_migrations

# Create database backup
docker-compose -f infra/docker/docker-compose.yml exec postgres pg_dump -U aems_user aems_db > backup_$(date +%Y%m%d).sql

# Monitor database performance
docker-compose -f infra/docker/docker-compose.yml exec postgres psql -U aems_user -d aems_db -c "SELECT * FROM pg_stat_activity;"
```

#### Service Management

```bash
# Start specific services only
docker-compose -f infra/docker/docker-compose.yml up postgres pgbouncer auth_service

# Scale specific service
docker-compose -f infra/docker/docker-compose.yml up --scale sales_service=2

# View service logs
docker-compose -f infra/docker/docker-compose.yml logs -f ai_service

# Restart specific service
docker-compose -f infra/docker/docker-compose.yml restart finance_service
```

#### Health Checks & Monitoring

```bash
# Database connectivity check
docker-compose -f infra/docker/docker-compose.yml exec postgres pg_isready -U aems_user -d aems_db

# Run comprehensive health checks
./infra/database/scripts/health_check.sh

# Monitor system resources
docker-compose -f infra/docker/docker-compose.yml top

# View application metrics
curl http://localhost:8000/health
```

#### Development Mode

```bash
# Development environment with hot reload
docker-compose -f infra/docker/docker-compose.yml -f infra/docker/docker-compose.dev.yml up

# Run tests
./scripts/test.sh

# Clean development environment
./scripts/clean.sh
```

### Production Deployment

```bash
# Production deployment
docker-compose -f infra/docker/docker-compose.yml -f infra/docker/docker-compose.prod.yml up -d

# Enable monitoring stack
docker-compose -f infra/monitoring/docker-compose.monitoring.yml up -d

# Set up automated backups
./infra/scripts/setup_backups.sh
```

---

## Contributing

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines on code of conduct and submitting pull requests.

---

## License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for details.

---

## References

- [Project Information and Scope](./docs/Project_Info_Scope.md)
- [System Architecture](./docs/System_Architecture.md)
- [Database Schema](./docs/Database_Schema.md)
- [Data Dictionary](./docs/Data_Dictionary.md)
- [API Specification](./docs/API_Specification.md)
- [UI/UX Design Guidelines](./docs/UI_UX.md)
- [Logging Guide](./docs/Logging_Guide.md)
- [Project Plan](./docs/Project_Plan.md)
- [User Stories](./docs/User_Story.md)
- [User Journeys](./docs/User_Journey.md)
- [User Acceptance Criteria](./docs/User_Acceptance_Criteria.md)
- [Endpoint Status](./docs/Endpoint_Status.md)
