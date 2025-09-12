# System Architecture

## 1. Guiding Principles

- **Scalability:** The system must be able to handle growing amounts of data and user traffic.
- **Resilience:** The failure of one component should not bring down the entire system.
- **Maintainability:** Services should be independently deployable and easy to understand.
- **Security:** Data must be protected at rest and in transit.

## 2. High-Level Architecture

A-EMS will be built on a **Microservices Architecture**. This choice provides separation of concerns, allows for independent scaling of services, and enables technology diversity if needed in the future. The entire system will be containerized with **Docker** and orchestrated via **Docker Compose** for development and initial deployment.

```mermaid
graph TD
    subgraph User Interaction
        A[Frontend - Next.js]
    end

    subgraph API Layer
        B[API Gateway]
    end

    subgraph Backend Services
        C[Auth Service]
        D[Sales Service]
        E[Finance Service]
        F[HR Service]
        G[AI Orchestrator Service]
    end

    subgraph Data Persistence
        H[PostgreSQL Database]
    end

    subgraph External Services
        I[DeepSeek AI]
    end

    A -- HTTPS --> B
    B -- Route --> C
    B -- Route --> D
    B -- Route --> E
    B -- Route --> F
    B -- Route --> G

    C -- CRUD --> H
    D -- CRUD --> H
    E -- CRUD --> H
    F -- CRUD --> H

    G -- Fetches Data --> D
    G -- Fetches Data --> E
    G -- Sends Prompt --> I
```

### Components:

1.  **Frontend (Next.js):** A single-page application (SPA) that serves as the user's entry point. It is responsible for rendering the UI, managing user state, and communicating with the backend via a central API Gateway.
2.  **API Gateway:** A single entry point for all client requests. It routes traffic to the appropriate microservice and handles cross-cutting concerns like authentication and rate limiting.
3.  **Backend Microservices (Python/FastAPI):**
    - **Auth Service:** Manages user identity, authentication (e.g., JWT), and authorization.
    - **Sales Service:** Comprehensive sales data management including pipeline, forecasting, customer analytics, and territory performance.
    - **Finance Service:** Complete financial management including KPIs, cash flow, budgeting, expense tracking, revenue recognition, and profitability analysis.
    - **HR Service:** Full HR analytics covering headcount, recruitment, performance management, compensation, engagement, and training metrics.
    - **AI Orchestrator Service:** Acts as a bridge between the user's query and the DeepSeek AI model. It fetches context from other services and performs intelligent data aggregation before querying the AI.
4.  **PostgreSQL Database:** The primary relational database. While shown as a single instance for simplicity, in a true microservice architecture, each service might have its own dedicated database or schema.
5.  **DeepSeek AI:** An external, third-party service that provides the core natural language processing and generation capabilities.

## 3. Data Flow

### Example 1: User Logs In

1.  User enters credentials in the **Frontend**.
2.  Frontend sends a request to the **API Gateway**, which routes it to the **Auth Service**.
3.  **Auth Service** validates credentials against the **PostgreSQL Database**.
4.  On success, it generates a JSON Web Token (JWT) and returns it to the user.
5.  The **Frontend** stores the JWT for subsequent authenticated requests.

### Example 2: User Asks the AI a Question

1.  User types "Compare our sales in Q1 vs Q2" into the chat interface on the **Frontend**.
2.  Frontend sends the authenticated request (with JWT) to the **API Gateway**, which routes it to the **AI Orchestrator Service**.
3.  The **AI Orchestrator Service** calls the **Sales Service** via the API Gateway to fetch sales data for Q1 and Q2.
4.  It then constructs a detailed prompt (e.g., "Given the following sales data [...], compare Q1 and Q2.").
5.  The prompt is sent to the external **DeepSeek AI API**.
6.  DeepSeek processes the request and returns a natural language answer with analysis.
7.  The **AI Orchestrator Service** forwards the answer back to the **Frontend**, which displays it to the user.

## 4. Infrastructure & Deployment

- **Containerization:** All services (frontend, backend microservices, database) will be packaged as **Docker** containers. This is defined in `Dockerfile`s within each service's directory.
- **Orchestration:** `docker-compose.yml` in the `infra/` directory will define and link all the services, allowing the entire application stack to be brought up or down with a single command (`docker-compose up`).
- **Environment:** This setup is ideal for local development and can be adapted for deployment to cloud platforms like AWS (ECS/EKS), Google Cloud (GKE), or Azure (AKS) using their respective container orchestration services.
