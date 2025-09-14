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

- **Frontend:** Next.js SPA for UI and user interaction
- **API Gateway:** Central entry point for all client requests, handling routing and authentication
- **Backend Microservices:** Python/FastAPI services for Auth, Sales, Finance, HR, Products, Risk, Reports, and AI Orchestration
- **Database:** PostgreSQL for persistent storage
- **AI Integration:** DeepSeek for natural language processing and business insights

For architecture diagrams, data flow, and deployment details, see [System Architecture](./docs/System_Architecture.md).

---

## Core Features

- **Executive Dashboard:** Real-time, customizable analytics across all business domains
- **AI Chat Assistant:** Conversational interface for natural language queries, visualizations, and recommendations
- **Comprehensive Reporting:** Custom report generation, scheduling, and export
- **Enterprise-Grade Authentication & Security:**
  - MFA (TOTP, backup codes)
  - OAuth 2.0 / OIDC (Google)
  - RBAC, session/device management, audit logging
- **Comprehensive Logging & Monitoring:**
  - Structured JSON logging with correlation ID tracking
  - Centralized log aggregation and real-time monitoring
  - User-friendly error notifications with toast messages
  - Security and audit event tracking
- **Risk & Compliance:** Monitoring, incident tracking, regulatory reporting
- **Product & Inventory Management:** Analytics, lifecycle, demand forecasting
- **Mobile-Responsive & Accessible Design**

See [Project Information and Scope](./docs/Project_Info_Scope.md) for a full feature breakdown.

---

## Technology Stack

- **Frontend:** Next.js, TypeScript, Tailwind CSS, Recharts
- **Backend:** Python, FastAPI (microservices)
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **AI:** DeepSeek

---

## Directory Structure

```
/
├── backend/                  # Python/FastAPI Microservices
│   ├── services/             # Domain-specific services (auth, sales, etc.)
│   ├── shared/               # Shared libraries/modules
│   └── Dockerfile
├── frontend/                 # Next.js/TypeScript Application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   └── Dockerfile
├── infra/                    # Infrastructure configs (docker-compose.yml)
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
└── README.md
```

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

- Docker
- Node.js
- Python

### Installation & Running

1. **Clone the repository:**
   `bash
git clone https://github.com/CatHuyuH24/A-EMS.git
cd A-EMS
`

2. **Launch the application stack:**
   `bash
docker-compose -f infra/docker-compose.yml up --build
`

3. **Access the application:** - Frontend: [http://localhost:3000](http://localhost:3000) - Backend API: [http://localhost:8000](http://localhost:8000)

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
- [API Specification](./docs/API_Specification.md)
- [UI/UX Design Guidelines](./docs/UI_UX.md)
- [Logging Guide](./docs/Logging_Guide.md)
- [Project Plan](./docs/Project_Plan.md)
- [User Stories](./docs/User_Story.md)
- [User Journeys](./docs/User_Journey.md)
- [User Acceptance Criteria](./docs/User_Acceptance_Criteria.md)
- [Endpoint Status](./docs/Endpoint_Status.md)
