# System Architecture

_Last updated: 14/09/2025_

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
        H[Products Service]
        I[Risk Service]
        J[Reports Service]
    end

    subgraph Data Persistence
        K[PostgreSQL Database]
    end

    subgraph External Services
        L[DeepSeek AI]
    end

    A -- HTTPS --> B
    B -- Route --> C
    B -- Route --> D
    B -- Route --> E
    B -- Route --> F
    B -- Route --> G
    B -- Route --> H
    B -- Route --> I
    B -- Route --> J

    C -- CRUD --> K
    D -- CRUD --> K
    E -- CRUD --> K
    F -- CRUD --> K
    H -- CRUD --> K
    I -- CRUD --> K
    J -- CRUD --> K

    G -- Fetches Data --> D
    G -- Fetches Data --> E
    G -- Fetches Data --> F
    G -- Fetches Data --> H
    G -- Fetches Data --> I
    G -- Sends Prompt --> L
```

### Components:

1.  **Frontend (Next.js):** A single-page application (SPA) that serves as the user's entry point. It is responsible for rendering the UI, managing user state, and communicating with the backend via a central API Gateway.
2.  **API Gateway:** A single entry point for all client requests. It routes traffic to the appropriate microservice and handles cross-cutting concerns like authentication and rate limiting.
3.  **Backend Microservices (Python/FastAPI):**
    - **Enhanced Auth Service:** Manages comprehensive user identity, authentication, and authorization including:
      - JWT-based authentication with refresh tokens
      - Multi-Factor Authentication (MFA) with TOTP and backup codes
      - OAuth 2.0 / OIDC integration with Google
      - Password management (change, reset, forgot password)
      - Role-based access control (RBAC)
      - Session management and token validation
      - User provisioning and account lifecycle management
    - **Sales Service:** Comprehensive sales data management including pipeline, forecasting, customer analytics, and territory performance.
    - **Finance Service:** Complete financial management including KPIs, cash flow, budgeting, expense tracking, revenue recognition, and profitability analysis.
    - **HR Service:** Full HR analytics covering headcount, recruitment, performance management, compensation, engagement, and training metrics.
    - **Products Service:** Complete product management including inventory tracking, product analytics, lifecycle management, catalog management, and demand forecasting.
    - **Risk Management Service:** Enterprise risk assessment including compliance monitoring, incident management, regulatory reporting, and risk analytics with early warning systems.
    - **Reports Service:** Comprehensive reporting capabilities including custom report generation, scheduling, export functionality, and real-time dashboard visualization from multiple data sources.
    - **AI Orchestrator Service:** Advanced AI interaction management with comprehensive features including:
      - **Multi-turn Conversations:** Context-aware chat sessions with memory persistence
      - **Session Management:** Conversation history tracking and context preservation
      - **Smart Context Aggregation:** Intelligent data gathering from multiple business services
      - **Response Optimization:** Chart generation, insights extraction, and recommendation engines
      - **User Feedback Loop:** Quality improvement through rating and feedback collection
      - **Contextual Suggestions:** Proactive query recommendations based on user role and history
      - **Real-time Streaming:** Optional SSE-based streaming for enhanced user experience
      - **Analytics & Monitoring:** Usage patterns, performance metrics, and quality analytics
      - **DeepSeek Integration:** Advanced prompt engineering and response processing
4.  **PostgreSQL Database:** The primary relational database. While shown as a single instance for simplicity, in a true microservice architecture, each service might have its own dedicated database or schema.
5.  **DeepSeek AI:** An external, third-party service that provides the core natural language processing and generation capabilities.

## 3. Data Flow

### Example 1: Enhanced User Authentication Flow

#### Standard Login

1.  User enters credentials in the **Frontend**.
2.  Frontend sends a request to the **API Gateway**, which routes it to the **Auth Service**.
3.  **Auth Service** validates credentials against the **PostgreSQL Database**.
4.  If MFA is enabled, **Auth Service** returns an MFA challenge requiring TOTP code.
5.  User provides TOTP code, **Auth Service** validates it.
6.  On success, it generates a JSON Web Token (JWT) and refresh token, returns them to the user.
7.  The **Frontend** stores the JWT for subsequent authenticated requests.

#### OAuth 2.0 Google Login

1.  User clicks "Login with Google" in the **Frontend**.
2.  Frontend redirects to Google OAuth authorization server.
3.  User authenticates with Google and grants permissions.
4.  Google redirects back to **Frontend** with authorization code.
5.  Frontend sends authorization code to **Auth Service** via **API Gateway**.
6.  **Auth Service** exchanges code for Google access token and user info.
7.  **Auth Service** either creates new user or links to existing account.
8.  **Auth Service** generates JWT and returns user session data.

#### MFA Setup Flow

1.  User navigates to MFA settings in **Frontend**.
2.  Frontend requests TOTP setup from **Auth Service**.
3.  **Auth Service** generates secret key and QR code, returns to **Frontend**.
4.  User scans QR code with authenticator app and enters verification code.
5.  **Auth Service** validates TOTP code and enables MFA for user.
6.  **Auth Service** generates backup codes and returns them securely.

#### Administrative User Registration

1.  Administrator accesses user management interface in **Frontend**.
2.  Administrator fills out new user form with role and permissions.
3.  Frontend sends registration request to **Auth Service** via **API Gateway**.
4.  **Auth Service** validates administrator permissions and creates user account.
5.  **Auth Service** sends welcome email with temporary password to new user.
6.  New user must change password and setup MFA on first login.

### Example 2: Enhanced AI Chat Interaction Flow

#### Multi-turn Conversation with Context

1.  User types "Compare our sales in Q1 vs Q2" into the chat interface on the **Frontend**.
2.  Frontend sends the authenticated request (with JWT and session_id) to the **API Gateway**, which routes it to the **AI Orchestrator Service**.
3.  **AI Orchestrator Service** performs intelligent context gathering:

- Retrieves conversation history for session continuity
- Calls **Sales Service** via API Gateway to fetch Q1 and Q2 sales data
- Calls **Finance Service** for related financial context
- Aggregates user permissions to determine data access scope

4.  **AI Orchestrator Service** constructs comprehensive prompt with business context and sends to **DeepSeek AI**.
5.  **DeepSeek AI** processes the request and returns structured analysis with recommendations.
6.  **AI Orchestrator Service** processes the response:

- Generates chart data specifications for frontend rendering
- Extracts key insights and recommendations
- Creates contextual follow-up suggestions
- Stores conversation in session history

7.  Enhanced response is returned to **Frontend** including:

- Natural language analysis
- Chart visualization data
- Key insights and recommendations
- Suggested follow-up questions

8.  **Frontend** renders the complete response with interactive visualizations.

#### Context Management and Follow-up

9.  User asks follow-up question: "What drove the increase in Q2?"
10. **AI Orchestrator Service** maintains context from previous exchange:
    - References previous Q1/Q2 comparison
    - Accesses deeper sales and market data
    - Provides contextual analysis without requiring context restatement

### Example 3: Password Change Flow

1.  User navigates to account settings in **Frontend**.
2.  User enters current password and new password in form.
3.  Frontend sends password change request to **Auth Service** via **API Gateway**.
4.  **Auth Service** validates current password and enforces password policy.
5.  **Auth Service** updates password hash in **PostgreSQL Database**.
6.  **Auth Service** invalidates all existing sessions except current one.
7.  **Auth Service** sends password change confirmation email to user.

## 4. Infrastructure & Deployment

- **Containerization:** All services (frontend, backend microservices, database) will be packaged as **Docker** containers. This is defined in `Dockerfile`s within each service's directory.
- **Orchestration:** `docker-compose.yml` in the `infra/` directory will define and link all the services, allowing the entire application stack to be brought up or down with a single command (`docker-compose up`).
- **Environment:** This setup is ideal for local development and can be adapted for deployment to cloud platforms like AWS (ECS/EKS), Google Cloud (GKE), or Azure (AKS) using their respective container orchestration services.

## 5. Logging Architecture & Flow

### 5.1. Logging Principles

The A-EMS system implements comprehensive logging across all components following these principles:

- **Structured Logging**: All logs use JSON format for machine readability and consistent parsing
- **Correlation IDs**: Every request is tracked with unique identifiers across all services
- **Centralized Collection**: Docker logging drivers aggregate logs from all containers
- **Security**: No sensitive data (PII, passwords, tokens) in logs

### 5.2. Backend Logging Flow

```mermaid
graph TD
    A[Frontend Request] --> B[API Gateway]
    B --> |Generate Correlation ID| C[Service 1]
    B --> |Forward Correlation ID| D[Service 2]
    C --> |Structured JSON Logs| E[Docker Stdout]
    D --> |Structured JSON Logs| F[Docker Stdout]
    B --> |Request/Response Logs| G[Docker Stdout]
    E --> H[Docker Log Driver]
    F --> H
    G --> H
    H --> I[Centralized Log Storage]
    I --> J[Log Analysis & Monitoring]
```

**Log Flow Process:**

1. **Request Initiation**: Frontend sends request with optional correlation ID
2. **Gateway Processing**: API Gateway generates or forwards correlation ID, logs request details
3. **Service Processing**: Each microservice logs operations with correlation ID context
4. **Container Logging**: All logs output to stdout/stderr (captured by Docker)
5. **Log Aggregation**: Docker logging driver collects and formats logs
6. **Storage & Monitoring**: Logs stored for analysis and real-time monitoring

### 5.3. Frontend Error Handling Flow

```mermaid
graph TD
    A[User Action] --> B[React Component]
    B --> C[API Call]
    C --> D{API Response}
    D -->|Success| E[Update UI State]
    D -->|Error| F[Error Boundary/Handler]
    F --> G[Log Client Error]
    F --> H[Show Toast Notification]
    G --> I[Send to Backend Logger]
    H --> J[User-Friendly Message]

    K[Unhandled Error] --> L[Global Error Boundary]
    L --> M[Log Critical Error]
    L --> N[Show Fallback UI]
    M --> I
```

**Frontend Error Types & Responses:**

- **401 Unauthorized**: Redirect to login with session expired message
- **403 Forbidden**: Warning toast with permission denied message
- **422 Validation**: Contextual error toast with specific field issues
- **500 Server Error**: Generic error toast with "try again later" message
- **Network Error**: Connectivity issue notification

### 5.4. Monitoring & Observability

**Key Metrics Tracked:**

- **Request Tracing**: End-to-end request flow with correlation IDs
- **Performance Monitoring**: Response times, database query performance
- **Error Rates**: Service-level error frequencies and patterns
- **Security Events**: Authentication failures, suspicious activities
- **Business Metrics**: User actions, feature usage analytics

**Log Categories:**

- **Application Logs**: Business logic, user actions, system operations
- **Security Logs**: Authentication, authorization, security events
- **Performance Logs**: Response times, resource usage, bottlenecks
- **Audit Logs**: Data access, configuration changes, admin actions

For detailed logging implementation guidelines, see [Logging Guide](./Logging_Guide.md).
