# A-EMS (AI-Driven Enter- **Backend:** Microservices architecture using Python & FastAPI. The backend is composed of domain-specific services (e.g., Auth, Sales, Finance) to ensure scalability and separation of concerns.

- **Frontend:** Next.js, TypeScript, Tailwind CSS, and Recharts for data visualization.
- **Database:** PostgreSQL.
- **Infrastructure:** Docker and Docker Compose for containerization and orchestration.
- **AI:** DeepSeek for natural language processing and insights.

## Directory Structure

The project is organized into a modular structure to support microservices development:

````
/
├── backend/         # Contains all backend microservices
│   └── services/    # Each business domain as a service
├── frontend/        # Next.js/TypeScript Application
├── infra/           # Docker Compose and infrastructure configurations
├── docs/            # All project documentation
└── README.md
```ystem)

A-EMS is a web application designed to be a "Digital Chief of Staff" for CEOs and senior leadership. It provides comprehensive insights and data-driven decision-making capabilities in real-time through an intuitive dashboard and an AI-powered chat assistant.

## Table of Contents

- [Introduction](#introduction)
- [Project Vision](#project-vision)
- [Technology Stack](#technology-stack)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project aims to build a comprehensive enterprise management system from the ground up, leveraging a modern technology stack and an AI-driven development process. The system provides:

- **Real-time Executive Dashboard** with comprehensive analytics across Sales, Finance, and HR domains
- **Advanced AI Assistant** (powered by DeepSeek) for natural language business intelligence queries
- **Microservices Architecture** with domain-specific services for scalability and maintainability
- **Interactive Data Visualizations** with real-time updates and mobile responsiveness

## Project Vision

To create a "Digital Chief of Staff" - an intelligent virtual assistant that empowers leaders with:
- Holistic business insights across all operational domains
- Predictive analytics and forecasting capabilities
- Natural language query interface for complex data analysis
- Real-time performance monitoring and alerting
- Data-driven decision support with actionable recommendations

## Technology Stack

- **Backend:** Microservices architecture using Python & FastAPI.
- **Frontend:** Next.js, TypeScript, Tailwind CSS, and Recharts for data visualization.
- **Database:** PostgreSQL.
- **Infrastructure:** Docker and Docker Compose for containerization and orchestration.
- **AI:** DeepSeek for natural language processing and insights.

## Directory Structure

The project is organized into the following main directories:

````

/
├── backend/ # Python/FastAPI Microservices
├── frontend/ # Next.js/TypeScript Application
├── infra/ # Docker Compose and infrastructure configurations
├── docs/ # All project documentation
└── README.md

````

For more details, please refer to the [Project Information and Scope](./docs/Project_Info_Scope.md) document.

## Getting Started

### Prerequisites

- Docker
- Node.js
- Python

### Installation & Running

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/CatHuyuH24/A-EMS.git
    cd A-EMS
    ```

2.  **Launch the application stack:**
    _This command will build and start the frontend, backend, and database containers._

    ```bash
    docker-compose -f infra/docker-compose.yml up --build
    ```

3.  **Access the application:**
    - **Frontend:** `http://localhost:3000`
    - **Backend API:** `http://localhost:8000`

## Contributing

Please read the [contributing guidelines](./docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
````
