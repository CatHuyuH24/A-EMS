# Data Dictionary

_Last updated: 16/09/2025_

This document provides a comprehensive data dictionary for the A-EMS (AI-Driven Enterprise Management System) database. It defines all entities, attributes, relationships, data types, constraints, and business rules necessary for the microservices architecture.

---

## Table of Contents

- [Overview](#overview)
- [Database Design Principles](#database-design-principles)
- [Common Data Types & Standards](#common-data-types--standards)
- [Core Entities](#core-entities)
- [Authentication & Security](#authentication--security)
- [Business Domain Entities](#business-domain-entities)
- [AI & Analytics](#ai--analytics)
- [System & Audit](#system--audit)
- [Relationships Overview](#relationships-overview)
- [Business Rules & Constraints](#business-rules--constraints)
- [Docker Integration](#docker-integration)

---

## Overview

The A-EMS database is designed to support a microservices architecture with the following design goals:

- **Scalability**: Support for horizontal scaling and service-specific database optimization
- **Data Integrity**: Strong referential integrity with appropriate constraints
- **Performance**: Optimized for read-heavy analytical workloads with real-time dashboard updates
- **Security**: Role-based access control with comprehensive audit trails
- **Compliance**: Built-in support for regulatory requirements and data governance

**Database Technology**: PostgreSQL 15+ with Docker containerization
**Character Set**: UTF-8 (supports international characters)
**Collation**: en_US.UTF-8

---

## Database Design Principles

### 1. Multi-Tenant Ready

- All business entities include `tenant_id` for future multi-tenancy support
- Tenant isolation enforced at database and application levels

### 2. Audit Trail

- All business-critical tables include audit fields: `created_at`, `updated_at`, `created_by`, `updated_by`
- Comprehensive logging of data changes for compliance and debugging

### 3. Soft Delete Pattern

- Critical business data uses `deleted_at` timestamp instead of hard deletes
- Maintains data integrity for historical reporting and analytics

### 4. Performance Optimization

- Strategic indexing for common query patterns
- Partitioning for large time-series data (metrics, logs)
- Materialized views for complex analytical queries

### 5. Data Quality

- Comprehensive constraints and validation rules
- Standardized data formats (phone numbers, emails, currencies)

---

## Common Data Types & Standards

### Standard Field Types

| Type            | PostgreSQL Type            | Description                 | Example                                |
| --------------- | -------------------------- | --------------------------- | -------------------------------------- |
| **Primary Key** | `UUID`                     | Universal unique identifier | `f47ac10b-58cc-4372-a567-0e02b2c3d479` |
| **Foreign Key** | `UUID`                     | References to other tables  | Same as primary key                    |
| **Timestamp**   | `TIMESTAMP WITH TIME ZONE` | ISO 8601 with timezone      | `2025-09-16T10:30:00+00:00`            |
| **Currency**    | `DECIMAL(15,2)`            | Monetary amounts            | `1234567.89`                           |
| **Percentage**  | `DECIMAL(5,2)`             | Percentages 0-100           | `12.34`                                |
| **Email**       | `VARCHAR(255)`             | Email addresses             | `user@company.com`                     |
| **Phone**       | `VARCHAR(20)`              | International phone format  | `+1-555-123-4567`                      |
| **URL**         | `VARCHAR(2048)`            | Web URLs                    | `https://example.com/path`             |
| **Status**      | `VARCHAR(50)`              | Enumerated status values    | `active`, `inactive`, `pending`        |

### Audit Fields Standard

All business tables include these standard audit fields:

```sql
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
created_by UUID NOT NULL REFERENCES users(id),
updated_by UUID NOT NULL REFERENCES users(id),
deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
```

### Business Rules Enforcement

- **Email Validation**: CHECK constraint with regex pattern
- **Phone Validation**: CHECK constraint for international format
- **Currency Precision**: Always 2 decimal places for monetary values
- **Percentage Range**: CHECK constraint (0.00 <= percentage <= 100.00)
- **Status Values**: CHECK constraints for valid enumerated values

---

## Core Entities

### Tenants

**Purpose**: Multi-tenancy support for enterprise deployments
**Service**: Shared across all services

| Field               | Type                     | Constraints                   | Description                   |
| ------------------- | ------------------------ | ----------------------------- | ----------------------------- |
| `id`                | UUID                     | PRIMARY KEY                   | Unique tenant identifier      |
| `name`              | VARCHAR(255)             | NOT NULL, UNIQUE              | Tenant organization name      |
| `slug`              | VARCHAR(100)             | NOT NULL, UNIQUE              | URL-safe tenant identifier    |
| `settings`          | JSONB                    | NOT NULL DEFAULT '{}'         | Tenant-specific configuration |
| `subscription_plan` | VARCHAR(50)              | NOT NULL DEFAULT 'enterprise' | Subscription tier             |
| `status`            | VARCHAR(20)              | NOT NULL DEFAULT 'active'     | Tenant status                 |
| `created_at`        | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()        | Creation timestamp            |
| `updated_at`        | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()        | Last update timestamp         |

**Constraints**:

- `CHECK (status IN ('active', 'inactive', 'suspended'))`
- `CHECK (subscription_plan IN ('basic', 'professional', 'enterprise'))`

---

## Authentication & Security

### Users

**Purpose**: User account management and authentication
**Service**: Auth Service

| Field                   | Type                     | Constraints                | Description               |
| ----------------------- | ------------------------ | -------------------------- | ------------------------- |
| `id`                    | UUID                     | PRIMARY KEY                | Unique user identifier    |
| `tenant_id`             | UUID                     | NOT NULL, FK → tenants(id) | Tenant association        |
| `email`                 | VARCHAR(255)             | NOT NULL, UNIQUE           | User email address        |
| `username`              | VARCHAR(100)             | UNIQUE                     | Optional username         |
| `password_hash`         | VARCHAR(255)             | NOT NULL                   | Bcrypt password hash      |
| `first_name`            | VARCHAR(100)             | NOT NULL                   | User first name           |
| `last_name`             | VARCHAR(100)             | NOT NULL                   | User last name            |
| `role`                  | VARCHAR(50)              | NOT NULL DEFAULT 'user'    | User role                 |
| `status`                | VARCHAR(20)              | NOT NULL DEFAULT 'active'  | Account status            |
| `email_verified`        | BOOLEAN                  | NOT NULL DEFAULT FALSE     | Email verification status |
| `last_login`            | TIMESTAMP WITH TIME ZONE |                            | Last successful login     |
| `failed_login_attempts` | INTEGER                  | NOT NULL DEFAULT 0         | Failed login counter      |
| `locked_until`          | TIMESTAMP WITH TIME ZONE |                            | Account lock expiration   |
| `created_at`            | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp        |
| `updated_at`            | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp     |
| `deleted_at`            | TIMESTAMP WITH TIME ZONE |                            | Soft delete timestamp     |

**Constraints**:

- `CHECK (role IN ('admin', 'manager', 'user', 'viewer'))`
- `CHECK (status IN ('active', 'inactive', 'suspended', 'pending'))`
- `CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')`
- `CHECK (failed_login_attempts >= 0)`

**Indexes**:

- `btree(email)` - Primary login lookup
- `btree(tenant_id, status)` - Tenant user queries
- `btree(last_login)` - Activity reports

### User_Sessions

**Purpose**: JWT token and session management
**Service**: Auth Service

| Field                | Type                     | Constraints               | Description                |
| -------------------- | ------------------------ | ------------------------- | -------------------------- |
| `id`                 | UUID                     | PRIMARY KEY               | Session identifier         |
| `user_id`            | UUID                     | NOT NULL, FK → users(id)  | Associated user            |
| `token_hash`         | VARCHAR(255)             | NOT NULL, UNIQUE          | JWT token hash             |
| `refresh_token_hash` | VARCHAR(255)             | UNIQUE                    | Refresh token hash         |
| `device_info`        | JSONB                    |                           | Device/browser information |
| `ip_address`         | INET                     | NOT NULL                  | Client IP address          |
| `user_agent`         | TEXT                     |                           | Browser user agent         |
| `expires_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL                  | Token expiration           |
| `last_activity`      | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()    | Last activity timestamp    |
| `status`             | VARCHAR(20)              | NOT NULL DEFAULT 'active' | Session status             |
| `created_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()    | Creation timestamp         |

**Constraints**:

- `CHECK (status IN ('active', 'expired', 'revoked'))`
- `CHECK (expires_at > created_at)`

### User_MFA

**Purpose**: Multi-factor authentication configuration
**Service**: Auth Service

| Field          | Type                     | Constraints              | Description                       |
| -------------- | ------------------------ | ------------------------ | --------------------------------- |
| `id`           | UUID                     | PRIMARY KEY              | MFA configuration ID              |
| `user_id`      | UUID                     | NOT NULL, FK → users(id) | Associated user                   |
| `mfa_type`     | VARCHAR(20)              | NOT NULL                 | MFA method type                   |
| `is_enabled`   | BOOLEAN                  | NOT NULL DEFAULT FALSE   | MFA enabled status                |
| `secret_key`   | VARCHAR(255)             |                          | TOTP secret key (encrypted)       |
| `backup_codes` | TEXT[]                   |                          | Array of backup codes (encrypted) |
| `last_used`    | TIMESTAMP WITH TIME ZONE |                          | Last successful MFA               |
| `created_at`   | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()   | Creation timestamp                |
| `updated_at`   | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()   | Last update timestamp             |

**Constraints**:

- `CHECK (mfa_type IN ('totp', 'sms', 'email'))`
- `UNIQUE (user_id, mfa_type)`

### OAuth_Connections

**Purpose**: OAuth provider account linking
**Service**: Auth Service

| Field              | Type                     | Constraints               | Description                     |
| ------------------ | ------------------------ | ------------------------- | ------------------------------- |
| `id`               | UUID                     | PRIMARY KEY               | Connection identifier           |
| `user_id`          | UUID                     | NOT NULL, FK → users(id)  | Associated user                 |
| `provider`         | VARCHAR(50)              | NOT NULL                  | OAuth provider name             |
| `provider_user_id` | VARCHAR(255)             | NOT NULL                  | Provider user identifier        |
| `provider_email`   | VARCHAR(255)             |                           | Provider email address          |
| `access_token`     | TEXT                     |                           | OAuth access token (encrypted)  |
| `refresh_token`    | TEXT                     |                           | OAuth refresh token (encrypted) |
| `token_expires_at` | TIMESTAMP WITH TIME ZONE |                           | Token expiration                |
| `provider_data`    | JSONB                    |                           | Additional provider data        |
| `status`           | VARCHAR(20)              | NOT NULL DEFAULT 'active' | Connection status               |
| `created_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()    | Creation timestamp              |
| `updated_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()    | Last update timestamp           |

**Constraints**:

- `CHECK (provider IN ('google', 'microsoft', 'linkedin'))`
- `CHECK (status IN ('active', 'inactive', 'revoked'))`
- `UNIQUE (provider, provider_user_id)`

---

## Business Domain Entities

### Sales Domain

#### Sales_Metrics

**Purpose**: Sales performance tracking and KPI calculations
**Service**: Sales Service

| Field                       | Type                     | Constraints                | Description              |
| --------------------------- | ------------------------ | -------------------------- | ------------------------ |
| `id`                        | UUID                     | PRIMARY KEY                | Metric record identifier |
| `tenant_id`                 | UUID                     | NOT NULL, FK → tenants(id) | Tenant association       |
| `metric_date`               | DATE                     | NOT NULL                   | Metric calculation date  |
| `period_type`               | VARCHAR(20)              | NOT NULL                   | Aggregation period       |
| `total_revenue`             | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Total revenue amount     |
| `pipeline_value`            | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Active pipeline value    |
| `deals_closed`              | INTEGER                  | NOT NULL DEFAULT 0         | Number of deals closed   |
| `deals_lost`                | INTEGER                  | NOT NULL DEFAULT 0         | Number of deals lost     |
| `win_rate`                  | DECIMAL(5,2)             | NOT NULL DEFAULT 0         | Win rate percentage      |
| `customer_acquisition_cost` | DECIMAL(10,2)            | NOT NULL DEFAULT 0         | Average CAC              |
| `customer_lifetime_value`   | DECIMAL(10,2)            | NOT NULL DEFAULT 0         | Average CLV              |
| `churn_rate`                | DECIMAL(5,2)             | NOT NULL DEFAULT 0         | Customer churn rate      |
| `created_at`                | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp       |
| `updated_at`                | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp    |
| `created_by`                | UUID                     | NOT NULL, FK → users(id)   | Creator user             |
| `updated_by`                | UUID                     | NOT NULL, FK → users(id)   | Last updater user        |

**Constraints**:

- `CHECK (period_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'))`
- `CHECK (win_rate >= 0 AND win_rate <= 100)`
- `CHECK (churn_rate >= 0 AND churn_rate <= 100)`
- `UNIQUE (tenant_id, metric_date, period_type)`

#### Customers

**Purpose**: Customer relationship management
**Service**: Sales Service

| Field                | Type                     | Constraints                | Description                 |
| -------------------- | ------------------------ | -------------------------- | --------------------------- |
| `id`                 | UUID                     | PRIMARY KEY                | Customer identifier         |
| `tenant_id`          | UUID                     | NOT NULL, FK → tenants(id) | Tenant association          |
| `company_name`       | VARCHAR(255)             | NOT NULL                   | Customer company name       |
| `contact_email`      | VARCHAR(255)             | NOT NULL                   | Primary contact email       |
| `contact_phone`      | VARCHAR(20)              |                            | Primary contact phone       |
| `industry`           | VARCHAR(100)             |                            | Customer industry           |
| `company_size`       | VARCHAR(50)              |                            | Company size category       |
| `territory`          | VARCHAR(100)             |                            | Sales territory             |
| `customer_segment`   | VARCHAR(50)              | NOT NULL                   | Customer segment            |
| `acquisition_date`   | DATE                     | NOT NULL                   | Customer acquisition date   |
| `lifetime_value`     | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Customer lifetime value     |
| `total_revenue`      | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Total revenue from customer |
| `last_purchase_date` | DATE                     |                            | Last purchase date          |
| `status`             | VARCHAR(20)              | NOT NULL DEFAULT 'active'  | Customer status             |
| `billing_address`    | JSONB                    |                            | Billing address information |
| `custom_fields`      | JSONB                    |                            | Additional custom data      |
| `created_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp          |
| `updated_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp       |
| `created_by`         | UUID                     | NOT NULL, FK → users(id)   | Creator user                |
| `updated_by`         | UUID                     | NOT NULL, FK → users(id)   | Last updater user           |
| `deleted_at`         | TIMESTAMP WITH TIME ZONE |                            | Soft delete timestamp       |

**Constraints**:

- `CHECK (status IN ('active', 'inactive', 'churned', 'prospect'))`
- `CHECK (customer_segment IN ('enterprise', 'mid_market', 'smb', 'startup'))`
- `CHECK (company_size IN ('1-10', '11-50', '51-200', '201-1000', '1000+'))`

#### Sales_Pipeline

**Purpose**: Sales pipeline and opportunity tracking
**Service**: Sales Service

| Field                 | Type                     | Constraints                  | Description                   |
| --------------------- | ------------------------ | ---------------------------- | ----------------------------- |
| `id`                  | UUID                     | PRIMARY KEY                  | Pipeline record identifier    |
| `tenant_id`           | UUID                     | NOT NULL, FK → tenants(id)   | Tenant association            |
| `customer_id`         | UUID                     | NOT NULL, FK → customers(id) | Associated customer           |
| `opportunity_name`    | VARCHAR(255)             | NOT NULL                     | Opportunity name              |
| `stage`               | VARCHAR(50)              | NOT NULL                     | Current pipeline stage        |
| `value`               | DECIMAL(15,2)            | NOT NULL                     | Opportunity value             |
| `probability`         | DECIMAL(5,2)             | NOT NULL                     | Close probability percentage  |
| `expected_close_date` | DATE                     | NOT NULL                     | Expected close date           |
| `actual_close_date`   | DATE                     |                              | Actual close date             |
| `sales_rep`           | UUID                     | NOT NULL, FK → users(id)     | Assigned sales representative |
| `source`              | VARCHAR(100)             |                              | Lead source                   |
| `status`              | VARCHAR(20)              | NOT NULL DEFAULT 'open'      | Opportunity status            |
| `notes`               | TEXT                     |                              | Additional notes              |
| `created_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Creation timestamp            |
| `updated_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Last update timestamp         |
| `created_by`          | UUID                     | NOT NULL, FK → users(id)     | Creator user                  |
| `updated_by`          | UUID                     | NOT NULL, FK → users(id)     | Last updater user             |

**Constraints**:

- `CHECK (stage IN ('lead', 'qualified', 'proposal', 'negotiation', 'closed_won', 'closed_lost'))`
- `CHECK (status IN ('open', 'closed_won', 'closed_lost', 'on_hold'))`
- `CHECK (probability >= 0 AND probability <= 100)`
- `CHECK (value > 0)`

### Finance Domain

#### Finance_Metrics

**Purpose**: Financial KPIs and performance tracking
**Service**: Finance Service

| Field                 | Type                     | Constraints                | Description              |
| --------------------- | ------------------------ | -------------------------- | ------------------------ |
| `id`                  | UUID                     | PRIMARY KEY                | Metric record identifier |
| `tenant_id`           | UUID                     | NOT NULL, FK → tenants(id) | Tenant association       |
| `metric_date`         | DATE                     | NOT NULL                   | Metric calculation date  |
| `period_type`         | VARCHAR(20)              | NOT NULL                   | Aggregation period       |
| `total_revenue`       | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Total revenue            |
| `total_expenses`      | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Total expenses           |
| `gross_profit`        | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Gross profit             |
| `net_profit`          | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Net profit               |
| `ebitda`              | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | EBITDA                   |
| `gross_margin`        | DECIMAL(5,2)             | NOT NULL DEFAULT 0         | Gross margin percentage  |
| `net_margin`          | DECIMAL(5,2)             | NOT NULL DEFAULT 0         | Net margin percentage    |
| `cash_flow`           | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Operating cash flow      |
| `accounts_receivable` | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | AR balance               |
| `accounts_payable`    | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | AP balance               |
| `cash_balance`        | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Cash and equivalents     |
| `burn_rate`           | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Monthly burn rate        |
| `runway_months`       | DECIMAL(5,1)             | NOT NULL DEFAULT 0         | Cash runway in months    |
| `created_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp       |
| `updated_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp    |
| `created_by`          | UUID                     | NOT NULL, FK → users(id)   | Creator user             |
| `updated_by`          | UUID                     | NOT NULL, FK → users(id)   | Last updater user        |

**Constraints**:

- `CHECK (period_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'))`
- `UNIQUE (tenant_id, metric_date, period_type)`

#### Budget_Plans

**Purpose**: Budget planning and tracking
**Service**: Finance Service

| Field                 | Type                     | Constraints                | Description            |
| --------------------- | ------------------------ | -------------------------- | ---------------------- |
| `id`                  | UUID                     | PRIMARY KEY                | Budget plan identifier |
| `tenant_id`           | UUID                     | NOT NULL, FK → tenants(id) | Tenant association     |
| `name`                | VARCHAR(255)             | NOT NULL                   | Budget plan name       |
| `fiscal_year`         | INTEGER                  | NOT NULL                   | Fiscal year            |
| `department`          | VARCHAR(100)             | NOT NULL                   | Department name        |
| `category`            | VARCHAR(100)             | NOT NULL                   | Budget category        |
| `planned_amount`      | DECIMAL(15,2)            | NOT NULL                   | Planned budget amount  |
| `actual_amount`       | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Actual spent amount    |
| `variance`            | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Budget variance        |
| `variance_percentage` | DECIMAL(5,2)             | NOT NULL DEFAULT 0         | Variance percentage    |
| `period_start`        | DATE                     | NOT NULL                   | Budget period start    |
| `period_end`          | DATE                     | NOT NULL                   | Budget period end      |
| `status`              | VARCHAR(20)              | NOT NULL DEFAULT 'active'  | Budget status          |
| `notes`               | TEXT                     |                            | Budget notes           |
| `created_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp     |
| `updated_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp  |
| `created_by`          | UUID                     | NOT NULL, FK → users(id)   | Creator user           |
| `updated_by`          | UUID                     | NOT NULL, FK → users(id)   | Last updater user      |

**Constraints**:

- `CHECK (status IN ('active', 'locked', 'archived'))`
- `CHECK (period_end > period_start)`
- `CHECK (planned_amount > 0)`

#### Expense_Transactions

**Purpose**: Expense tracking and categorization
**Service**: Finance Service

| Field              | Type                     | Constraints                | Description               |
| ------------------ | ------------------------ | -------------------------- | ------------------------- |
| `id`               | UUID                     | PRIMARY KEY                | Transaction identifier    |
| `tenant_id`        | UUID                     | NOT NULL, FK → tenants(id) | Tenant association        |
| `transaction_date` | DATE                     | NOT NULL                   | Transaction date          |
| `amount`           | DECIMAL(15,2)            | NOT NULL                   | Transaction amount        |
| `currency`         | VARCHAR(3)               | NOT NULL DEFAULT 'USD'     | Currency code (ISO 4217)  |
| `category`         | VARCHAR(100)             | NOT NULL                   | Expense category          |
| `subcategory`      | VARCHAR(100)             |                            | Expense subcategory       |
| `vendor`           | VARCHAR(255)             | NOT NULL                   | Vendor/supplier name      |
| `description`      | TEXT                     | NOT NULL                   | Transaction description   |
| `department`       | VARCHAR(100)             |                            | Responsible department    |
| `employee_id`      | UUID                     | FK → users(id)             | Associated employee       |
| `receipt_url`      | VARCHAR(2048)            |                            | Receipt document URL      |
| `tax_amount`       | DECIMAL(15,2)            | NOT NULL DEFAULT 0         | Tax amount                |
| `is_reimbursable`  | BOOLEAN                  | NOT NULL DEFAULT FALSE     | Reimbursable expense flag |
| `approval_status`  | VARCHAR(20)              | NOT NULL DEFAULT 'pending' | Approval status           |
| `approved_by`      | UUID                     | FK → users(id)             | Approving user            |
| `approved_at`      | TIMESTAMP WITH TIME ZONE |                            | Approval timestamp        |
| `created_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp        |
| `updated_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp     |
| `created_by`       | UUID                     | NOT NULL, FK → users(id)   | Creator user              |
| `updated_by`       | UUID                     | NOT NULL, FK → users(id)   | Last updater user         |

**Constraints**:

- `CHECK (amount > 0)`
- `CHECK (approval_status IN ('pending', 'approved', 'rejected', 'cancelled'))`
- `CHECK (currency ~ '^[A-Z]{3}$')`

### HR Domain

#### HR_Metrics

**Purpose**: Human resources KPIs and workforce analytics
**Service**: HR Service

| Field                   | Type                     | Constraints                | Description                 |
| ----------------------- | ------------------------ | -------------------------- | --------------------------- |
| `id`                    | UUID                     | PRIMARY KEY                | Metric record identifier    |
| `tenant_id`             | UUID                     | NOT NULL, FK → tenants(id) | Tenant association          |
| `metric_date`           | DATE                     | NOT NULL                   | Metric calculation date     |
| `period_type`           | VARCHAR(20)              | NOT NULL                   | Aggregation period          |
| `total_headcount`       | INTEGER                  | NOT NULL DEFAULT 0         | Total employee count        |
| `new_hires`             | INTEGER                  | NOT NULL DEFAULT 0         | New hires in period         |
| `departures`            | INTEGER                  | NOT NULL DEFAULT 0         | Departures in period        |
| `turnover_rate`         | DECIMAL(5,2)             | NOT NULL DEFAULT 0         | Employee turnover rate      |
| `open_positions`        | INTEGER                  | NOT NULL DEFAULT 0         | Open job positions          |
| `time_to_hire_avg`      | INTEGER                  | NOT NULL DEFAULT 0         | Average time to hire (days) |
| `employee_satisfaction` | DECIMAL(3,1)             | NOT NULL DEFAULT 0         | Employee satisfaction score |
| `engagement_score`      | DECIMAL(3,1)             | NOT NULL DEFAULT 0         | Employee engagement score   |
| `training_hours`        | INTEGER                  | NOT NULL DEFAULT 0         | Training hours completed    |
| `overtime_hours`        | INTEGER                  | NOT NULL DEFAULT 0         | Overtime hours worked       |
| `absenteeism_rate`      | DECIMAL(5,2)             | NOT NULL DEFAULT 0         | Absenteeism rate            |
| `created_at`            | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp          |
| `updated_at`            | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp       |
| `created_by`            | UUID                     | NOT NULL, FK → users(id)   | Creator user                |
| `updated_by`            | UUID                     | NOT NULL, FK → users(id)   | Last updater user           |

**Constraints**:

- `CHECK (period_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'))`
- `CHECK (turnover_rate >= 0)`
- `CHECK (employee_satisfaction >= 0 AND employee_satisfaction <= 10)`
- `CHECK (engagement_score >= 0 AND engagement_score <= 10)`
- `CHECK (absenteeism_rate >= 0 AND absenteeism_rate <= 100)`
- `UNIQUE (tenant_id, metric_date, period_type)`

#### Employees

**Purpose**: Employee information and workforce management
**Service**: HR Service

| Field                 | Type                     | Constraints                | Description               |
| --------------------- | ------------------------ | -------------------------- | ------------------------- |
| `id`                  | UUID                     | PRIMARY KEY                | Employee identifier       |
| `tenant_id`           | UUID                     | NOT NULL, FK → tenants(id) | Tenant association        |
| `user_id`             | UUID                     | FK → users(id)             | Associated user account   |
| `employee_id`         | VARCHAR(50)              | NOT NULL                   | Company employee ID       |
| `first_name`          | VARCHAR(100)             | NOT NULL                   | Employee first name       |
| `last_name`           | VARCHAR(100)             | NOT NULL                   | Employee last name        |
| `email`               | VARCHAR(255)             | NOT NULL                   | Work email address        |
| `phone`               | VARCHAR(20)              |                            | Work phone number         |
| `department`          | VARCHAR(100)             | NOT NULL                   | Department name           |
| `job_title`           | VARCHAR(150)             | NOT NULL                   | Job title                 |
| `manager_id`          | UUID                     | FK → employees(id)         | Direct manager            |
| `hire_date`           | DATE                     | NOT NULL                   | Hire date                 |
| `employment_type`     | VARCHAR(20)              | NOT NULL                   | Employment type           |
| `status`              | VARCHAR(20)              | NOT NULL DEFAULT 'active'  | Employment status         |
| `salary`              | DECIMAL(12,2)            |                            | Annual salary (encrypted) |
| `salary_currency`     | VARCHAR(3)               | NOT NULL DEFAULT 'USD'     | Salary currency           |
| `location`            | VARCHAR(255)             |                            | Work location             |
| `remote_work`         | BOOLEAN                  | NOT NULL DEFAULT FALSE     | Remote work enabled       |
| `performance_rating`  | DECIMAL(3,1)             |                            | Last performance rating   |
| `last_promotion_date` | DATE                     |                            | Last promotion date       |
| `termination_date`    | DATE                     |                            | Termination date          |
| `termination_reason`  | VARCHAR(255)             |                            | Termination reason        |
| `created_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp        |
| `updated_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp     |
| `created_by`          | UUID                     | NOT NULL, FK → users(id)   | Creator user              |
| `updated_by`          | UUID                     | NOT NULL, FK → users(id)   | Last updater user         |
| `deleted_at`          | TIMESTAMP WITH TIME ZONE |                            | Soft delete timestamp     |

**Constraints**:

- `CHECK (employment_type IN ('full_time', 'part_time', 'contractor', 'intern'))`
- `CHECK (status IN ('active', 'inactive', 'terminated', 'on_leave'))`
- `CHECK (performance_rating >= 1 AND performance_rating <= 5)`
- `UNIQUE (tenant_id, employee_id)`

#### Recruitment_Pipeline

**Purpose**: Recruitment and hiring pipeline management
**Service**: HR Service

| Field                 | Type                     | Constraints                  | Description                  |
| --------------------- | ------------------------ | ---------------------------- | ---------------------------- |
| `id`                  | UUID                     | PRIMARY KEY                  | Pipeline record identifier   |
| `tenant_id`           | UUID                     | NOT NULL, FK → tenants(id)   | Tenant association           |
| `job_title`           | VARCHAR(150)             | NOT NULL                     | Job position title           |
| `department`          | VARCHAR(100)             | NOT NULL                     | Hiring department            |
| `candidate_name`      | VARCHAR(255)             | NOT NULL                     | Candidate full name          |
| `candidate_email`     | VARCHAR(255)             | NOT NULL                     | Candidate email              |
| `candidate_phone`     | VARCHAR(20)              |                              | Candidate phone              |
| `stage`               | VARCHAR(50)              | NOT NULL                     | Current recruitment stage    |
| `source`              | VARCHAR(100)             |                              | Candidate source             |
| `recruiter_id`        | UUID                     | NOT NULL, FK → users(id)     | Assigned recruiter           |
| `hiring_manager_id`   | UUID                     | NOT NULL, FK → employees(id) | Hiring manager               |
| `resume_url`          | VARCHAR(2048)            |                              | Resume document URL          |
| `cover_letter_url`    | VARCHAR(2048)            |                              | Cover letter URL             |
| `application_date`    | DATE                     | NOT NULL                     | Application submission date  |
| `expected_start_date` | DATE                     |                              | Expected start date          |
| `salary_expectation`  | DECIMAL(12,2)            |                              | Candidate salary expectation |
| `status`              | VARCHAR(20)              | NOT NULL DEFAULT 'active'    | Application status           |
| `rejection_reason`    | TEXT                     |                              | Rejection reason             |
| `notes`               | TEXT                     |                              | Recruiter notes              |
| `created_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Creation timestamp           |
| `updated_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Last update timestamp        |
| `created_by`          | UUID                     | NOT NULL, FK → users(id)     | Creator user                 |
| `updated_by`          | UUID                     | NOT NULL, FK → users(id)     | Last updater user            |

**Constraints**:

- `CHECK (stage IN ('applied', 'screening', 'interview', 'reference_check', 'offer', 'hired', 'rejected'))`
- `CHECK (status IN ('active', 'hired', 'rejected', 'withdrawn'))`

### Products Domain

#### Products

**Purpose**: Product catalog and inventory management
**Service**: Products Service

| Field              | Type                     | Constraints                | Description              |
| ------------------ | ------------------------ | -------------------------- | ------------------------ |
| `id`               | UUID                     | PRIMARY KEY                | Product identifier       |
| `tenant_id`        | UUID                     | NOT NULL, FK → tenants(id) | Tenant association       |
| `sku`              | VARCHAR(100)             | NOT NULL                   | Stock keeping unit       |
| `name`             | VARCHAR(255)             | NOT NULL                   | Product name             |
| `description`      | TEXT                     |                            | Product description      |
| `category`         | VARCHAR(100)             | NOT NULL                   | Product category         |
| `subcategory`      | VARCHAR(100)             |                            | Product subcategory      |
| `brand`            | VARCHAR(100)             |                            | Product brand            |
| `unit_cost`        | DECIMAL(10,2)            | NOT NULL                   | Unit cost                |
| `selling_price`    | DECIMAL(10,2)            | NOT NULL                   | Selling price            |
| `profit_margin`    | DECIMAL(5,2)             | NOT NULL                   | Profit margin percentage |
| `weight`           | DECIMAL(10,3)            |                            | Product weight (kg)      |
| `dimensions`       | JSONB                    |                            | Product dimensions       |
| `lifecycle_stage`  | VARCHAR(50)              | NOT NULL                   | Product lifecycle stage  |
| `launch_date`      | DATE                     |                            | Product launch date      |
| `discontinue_date` | DATE                     |                            | Discontinuation date     |
| `supplier_info`    | JSONB                    |                            | Supplier information     |
| `status`           | VARCHAR(20)              | NOT NULL DEFAULT 'active'  | Product status           |
| `created_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp       |
| `updated_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp    |
| `created_by`       | UUID                     | NOT NULL, FK → users(id)   | Creator user             |
| `updated_by`       | UUID                     | NOT NULL, FK → users(id)   | Last updater user        |
| `deleted_at`       | TIMESTAMP WITH TIME ZONE |                            | Soft delete timestamp    |

**Constraints**:

- `CHECK (lifecycle_stage IN ('development', 'launch', 'growth', 'maturity', 'decline', 'discontinued'))`
- `CHECK (status IN ('active', 'inactive', 'discontinued', 'out_of_stock'))`
- `CHECK (selling_price > unit_cost)`
- `UNIQUE (tenant_id, sku)`

#### Inventory_Levels

**Purpose**: Inventory tracking across warehouses
**Service**: Products Service

| Field                | Type                     | Constraints                 | Description                 |
| -------------------- | ------------------------ | --------------------------- | --------------------------- |
| `id`                 | UUID                     | PRIMARY KEY                 | Inventory record identifier |
| `tenant_id`          | UUID                     | NOT NULL, FK → tenants(id)  | Tenant association          |
| `product_id`         | UUID                     | NOT NULL, FK → products(id) | Associated product          |
| `warehouse_location` | VARCHAR(100)             | NOT NULL                    | Warehouse location          |
| `current_stock`      | INTEGER                  | NOT NULL DEFAULT 0          | Current stock level         |
| `reserved_stock`     | INTEGER                  | NOT NULL DEFAULT 0          | Reserved stock              |
| `available_stock`    | INTEGER                  | NOT NULL DEFAULT 0          | Available stock             |
| `reorder_level`      | INTEGER                  | NOT NULL                    | Reorder threshold           |
| `max_stock_level`    | INTEGER                  | NOT NULL                    | Maximum stock level         |
| `last_restock_date`  | DATE                     |                             | Last restocking date        |
| `last_stock_take`    | DATE                     |                             | Last stock count date       |
| `stock_value`        | DECIMAL(15,2)            | NOT NULL DEFAULT 0          | Total stock value           |
| `turnover_rate`      | DECIMAL(5,2)             | NOT NULL DEFAULT 0          | Inventory turnover rate     |
| `created_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()      | Creation timestamp          |
| `updated_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()      | Last update timestamp       |
| `created_by`         | UUID                     | NOT NULL, FK → users(id)    | Creator user                |
| `updated_by`         | UUID                     | NOT NULL, FK → users(id)    | Last updater user           |

**Constraints**:

- `CHECK (current_stock >= 0)`
- `CHECK (reserved_stock >= 0)`
- `CHECK (available_stock >= 0)`
- `CHECK (reorder_level > 0)`
- `CHECK (max_stock_level > reorder_level)`
- `UNIQUE (tenant_id, product_id, warehouse_location)`

#### Product_Performance

**Purpose**: Product sales and performance analytics
**Service**: Products Service

| Field              | Type                     | Constraints                 | Description                   |
| ------------------ | ------------------------ | --------------------------- | ----------------------------- |
| `id`               | UUID                     | PRIMARY KEY                 | Performance record identifier |
| `tenant_id`        | UUID                     | NOT NULL, FK → tenants(id)  | Tenant association            |
| `product_id`       | UUID                     | NOT NULL, FK → products(id) | Associated product            |
| `metric_date`      | DATE                     | NOT NULL                    | Metric date                   |
| `period_type`      | VARCHAR(20)              | NOT NULL                    | Period type                   |
| `units_sold`       | INTEGER                  | NOT NULL DEFAULT 0          | Units sold                    |
| `revenue`          | DECIMAL(15,2)            | NOT NULL DEFAULT 0          | Revenue generated             |
| `profit`           | DECIMAL(15,2)            | NOT NULL DEFAULT 0          | Profit generated              |
| `returns`          | INTEGER                  | NOT NULL DEFAULT 0          | Units returned                |
| `customer_rating`  | DECIMAL(3,1)             |                             | Average customer rating       |
| `review_count`     | INTEGER                  | NOT NULL DEFAULT 0          | Number of reviews             |
| `price_elasticity` | DECIMAL(5,4)             |                             | Price elasticity score        |
| `demand_forecast`  | INTEGER                  |                             | Forecasted demand             |
| `created_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()      | Creation timestamp            |
| `updated_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()      | Last update timestamp         |
| `created_by`       | UUID                     | NOT NULL, FK → users(id)    | Creator user                  |
| `updated_by`       | UUID                     | NOT NULL, FK → users(id)    | Last updater user             |

**Constraints**:

- `CHECK (period_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'))`
- `CHECK (customer_rating >= 1 AND customer_rating <= 5)`
- `CHECK (units_sold >= 0)`
- `CHECK (returns >= 0)`
- `UNIQUE (tenant_id, product_id, metric_date, period_type)`

### Risk & Compliance Domain

#### Risk_Assessments

**Purpose**: Enterprise risk management and tracking
**Service**: Risk Service

| Field              | Type                     | Constraints                  | Description                |
| ------------------ | ------------------------ | ---------------------------- | -------------------------- |
| `id`               | UUID                     | PRIMARY KEY                  | Risk assessment identifier |
| `tenant_id`        | UUID                     | NOT NULL, FK → tenants(id)   | Tenant association         |
| `risk_name`        | VARCHAR(255)             | NOT NULL                     | Risk name/title            |
| `risk_category`    | VARCHAR(100)             | NOT NULL                     | Risk category              |
| `description`      | TEXT                     | NOT NULL                     | Risk description           |
| `likelihood`       | INTEGER                  | NOT NULL                     | Likelihood score (1-5)     |
| `impact`           | INTEGER                  | NOT NULL                     | Impact score (1-5)         |
| `risk_score`       | INTEGER                  | NOT NULL                     | Calculated risk score      |
| `risk_level`       | VARCHAR(20)              | NOT NULL                     | Risk level classification  |
| `owner_id`         | UUID                     | NOT NULL, FK → employees(id) | Risk owner                 |
| `status`           | VARCHAR(20)              | NOT NULL DEFAULT 'open'      | Risk status                |
| `mitigation_plan`  | TEXT                     |                              | Risk mitigation strategy   |
| `contingency_plan` | TEXT                     |                              | Contingency plan           |
| `last_review_date` | DATE                     |                              | Last review date           |
| `next_review_date` | DATE                     | NOT NULL                     | Next review date           |
| `created_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Creation timestamp         |
| `updated_at`       | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Last update timestamp      |
| `created_by`       | UUID                     | NOT NULL, FK → users(id)     | Creator user               |
| `updated_by`       | UUID                     | NOT NULL, FK → users(id)     | Last updater user          |
| `deleted_at`       | TIMESTAMP WITH TIME ZONE |                              | Soft delete timestamp      |

**Constraints**:

- `CHECK (risk_category IN ('operational', 'financial', 'strategic', 'compliance', 'cybersecurity', 'reputational'))`
- `CHECK (likelihood >= 1 AND likelihood <= 5)`
- `CHECK (impact >= 1 AND impact <= 5)`
- `CHECK (risk_score >= 1 AND risk_score <= 25)`
- `CHECK (risk_level IN ('low', 'medium', 'high', 'critical'))`
- `CHECK (status IN ('open', 'mitigated', 'accepted', 'transferred', 'closed'))`

#### Compliance_Status

**Purpose**: Regulatory compliance tracking and monitoring
**Service**: Risk Service

| Field               | Type                     | Constraints                  | Description                  |
| ------------------- | ------------------------ | ---------------------------- | ---------------------------- |
| `id`                | UUID                     | PRIMARY KEY                  | Compliance record identifier |
| `tenant_id`         | UUID                     | NOT NULL, FK → tenants(id)   | Tenant association           |
| `regulation`        | VARCHAR(100)             | NOT NULL                     | Regulation name              |
| `requirement`       | VARCHAR(255)             | NOT NULL                     | Specific requirement         |
| `status`            | VARCHAR(20)              | NOT NULL                     | Compliance status            |
| `compliance_score`  | DECIMAL(5,2)             | NOT NULL                     | Compliance score (0-100)     |
| `evidence_url`      | VARCHAR(2048)            |                              | Evidence document URL        |
| `responsible_party` | UUID                     | NOT NULL, FK → employees(id) | Responsible employee         |
| `last_audit_date`   | DATE                     |                              | Last audit date              |
| `next_audit_date`   | DATE                     | NOT NULL                     | Next audit date              |
| `findings`          | TEXT                     |                              | Audit findings               |
| `remediation_plan`  | TEXT                     |                              | Remediation plan             |
| `due_date`          | DATE                     |                              | Compliance due date          |
| `created_at`        | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Creation timestamp           |
| `updated_at`        | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()       | Last update timestamp        |
| `created_by`        | UUID                     | NOT NULL, FK → users(id)     | Creator user                 |
| `updated_by`        | UUID                     | NOT NULL, FK → users(id)     | Last updater user            |

**Constraints**:

- `CHECK (regulation IN ('GDPR', 'SOX', 'HIPAA', 'PCI_DSS', 'ISO_27001', 'SOC2'))`
- `CHECK (status IN ('compliant', 'non_compliant', 'partial', 'not_applicable'))`
- `CHECK (compliance_score >= 0 AND compliance_score <= 100)`

#### Incidents

**Purpose**: Incident management and tracking
**Service**: Risk Service

| Field                | Type                     | Constraints                | Description                |
| -------------------- | ------------------------ | -------------------------- | -------------------------- |
| `id`                 | UUID                     | PRIMARY KEY                | Incident identifier        |
| `tenant_id`          | UUID                     | NOT NULL, FK → tenants(id) | Tenant association         |
| `incident_number`    | VARCHAR(50)              | NOT NULL                   | Unique incident number     |
| `title`              | VARCHAR(255)             | NOT NULL                   | Incident title             |
| `description`        | TEXT                     | NOT NULL                   | Incident description       |
| `severity`           | VARCHAR(20)              | NOT NULL                   | Incident severity          |
| `category`           | VARCHAR(100)             | NOT NULL                   | Incident category          |
| `status`             | VARCHAR(20)              | NOT NULL DEFAULT 'open'    | Incident status            |
| `reporter_id`        | UUID                     | NOT NULL, FK → users(id)   | Incident reporter          |
| `assigned_to`        | UUID                     | FK → employees(id)         | Assigned resolver          |
| `reported_at`        | TIMESTAMP WITH TIME ZONE | NOT NULL                   | Incident report time       |
| `acknowledged_at`    | TIMESTAMP WITH TIME ZONE |                            | Acknowledgment time        |
| `resolved_at`        | TIMESTAMP WITH TIME ZONE |                            | Resolution time            |
| `resolution_time`    | INTEGER                  |                            | Resolution time in minutes |
| `impact_description` | TEXT                     |                            | Impact description         |
| `root_cause`         | TEXT                     |                            | Root cause analysis        |
| `resolution_notes`   | TEXT                     |                            | Resolution notes           |
| `lessons_learned`    | TEXT                     |                            | Lessons learned            |
| `created_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp         |
| `updated_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp      |
| `created_by`         | UUID                     | NOT NULL, FK → users(id)   | Creator user               |
| `updated_by`         | UUID                     | NOT NULL, FK → users(id)   | Last updater user          |

**Constraints**:

- `CHECK (severity IN ('low', 'medium', 'high', 'critical'))`
- `CHECK (status IN ('open', 'acknowledged', 'investigating', 'resolved', 'closed'))`
- `CHECK (category IN ('security', 'operational', 'data', 'system', 'compliance', 'other'))`
- `UNIQUE (tenant_id, incident_number)`

---

## AI & Analytics

### AI_Conversations

**Purpose**: AI chat history and conversation management
**Service**: AI Orchestrator Service

| Field             | Type                     | Constraints                | Description             |
| ----------------- | ------------------------ | -------------------------- | ----------------------- |
| `id`              | UUID                     | PRIMARY KEY                | Conversation identifier |
| `tenant_id`       | UUID                     | NOT NULL, FK → tenants(id) | Tenant association      |
| `user_id`         | UUID                     | NOT NULL, FK → users(id)   | Associated user         |
| `session_id`      | UUID                     | NOT NULL                   | Conversation session ID |
| `title`           | VARCHAR(255)             |                            | Conversation title      |
| `status`          | VARCHAR(20)              | NOT NULL DEFAULT 'active'  | Conversation status     |
| `context_data`    | JSONB                    |                            | Conversation context    |
| `total_messages`  | INTEGER                  | NOT NULL DEFAULT 0         | Total message count     |
| `last_message_at` | TIMESTAMP WITH TIME ZONE |                            | Last message timestamp  |
| `created_at`      | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp      |
| `updated_at`      | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp   |

**Constraints**:

- `CHECK (status IN ('active', 'archived', 'deleted'))`
- `CHECK (total_messages >= 0)`

### AI_Messages

**Purpose**: Individual AI conversation messages
**Service**: AI Orchestrator Service

| Field                | Type                     | Constraints                         | Description                   |
| -------------------- | ------------------------ | ----------------------------------- | ----------------------------- |
| `id`                 | UUID                     | PRIMARY KEY                         | Message identifier            |
| `conversation_id`    | UUID                     | NOT NULL, FK → ai_conversations(id) | Parent conversation           |
| `message_type`       | VARCHAR(20)              | NOT NULL                            | Message type                  |
| `content`            | TEXT                     | NOT NULL                            | Message content               |
| `metadata`           | JSONB                    |                                     | Message metadata              |
| `response_time`      | INTEGER                  |                                     | Response time in milliseconds |
| `tokens_used`        | INTEGER                  |                                     | AI tokens consumed            |
| `visualization_data` | JSONB                    |                                     | Chart/visualization data      |
| `feedback_rating`    | INTEGER                  |                                     | User feedback rating (1-5)    |
| `feedback_text`      | TEXT                     |                                     | User feedback text            |
| `created_at`         | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()              | Creation timestamp            |

**Constraints**:

- `CHECK (message_type IN ('user', 'ai', 'system'))`
- `CHECK (feedback_rating >= 1 AND feedback_rating <= 5)`
- `CHECK (tokens_used >= 0)`

### AI_Analytics

**Purpose**: AI usage analytics and performance metrics
**Service**: AI Orchestrator Service

| Field                 | Type                     | Constraints                | Description                 |
| --------------------- | ------------------------ | -------------------------- | --------------------------- |
| `id`                  | UUID                     | PRIMARY KEY                | Analytics record identifier |
| `tenant_id`           | UUID                     | NOT NULL, FK → tenants(id) | Tenant association          |
| `metric_date`         | DATE                     | NOT NULL                   | Metric date                 |
| `total_conversations` | INTEGER                  | NOT NULL DEFAULT 0         | Total conversations         |
| `total_messages`      | INTEGER                  | NOT NULL DEFAULT 0         | Total messages              |
| `avg_response_time`   | INTEGER                  | NOT NULL DEFAULT 0         | Average response time (ms)  |
| `total_tokens_used`   | INTEGER                  | NOT NULL DEFAULT 0         | Total AI tokens consumed    |
| `user_satisfaction`   | DECIMAL(3,2)             | NOT NULL DEFAULT 0         | Average user satisfaction   |
| `most_common_queries` | JSONB                    |                            | Most common query types     |
| `performance_metrics` | JSONB                    |                            | Performance metrics         |
| `created_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp          |
| `updated_at`          | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Last update timestamp       |

**Constraints**:

- `CHECK (user_satisfaction >= 0 AND user_satisfaction <= 5)`
- `CHECK (total_conversations >= 0)`
- `CHECK (total_messages >= 0)`
- `UNIQUE (tenant_id, metric_date)`

---

## System & Audit

### Audit_Logs

**Purpose**: Comprehensive system audit trail
**Service**: Shared across all services

| Field            | Type                     | Constraints                | Description                     |
| ---------------- | ------------------------ | -------------------------- | ------------------------------- |
| `id`             | UUID                     | PRIMARY KEY                | Audit log identifier            |
| `tenant_id`      | UUID                     | NOT NULL, FK → tenants(id) | Tenant association              |
| `user_id`        | UUID                     | FK → users(id)             | Associated user (if applicable) |
| `action`         | VARCHAR(100)             | NOT NULL                   | Action performed                |
| `entity_type`    | VARCHAR(100)             | NOT NULL                   | Entity type affected            |
| `entity_id`      | UUID                     |                            | Entity identifier               |
| `old_values`     | JSONB                    |                            | Previous values                 |
| `new_values`     | JSONB                    |                            | New values                      |
| `ip_address`     | INET                     |                            | Client IP address               |
| `user_agent`     | TEXT                     |                            | Client user agent               |
| `correlation_id` | UUID                     |                            | Request correlation ID          |
| `service_name`   | VARCHAR(50)              | NOT NULL                   | Originating service             |
| `severity`       | VARCHAR(20)              | NOT NULL DEFAULT 'info'    | Log severity level              |
| `created_at`     | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW()     | Creation timestamp              |

**Constraints**:

- `CHECK (action IN ('create', 'read', 'update', 'delete', 'login', 'logout', 'access_denied'))`
- `CHECK (severity IN ('debug', 'info', 'warning', 'error', 'critical'))`

### System_Metrics

**Purpose**: System performance and health monitoring
**Service**: Shared across all services

| Field          | Type                     | Constraints            | Description              |
| -------------- | ------------------------ | ---------------------- | ------------------------ |
| `id`           | UUID                     | PRIMARY KEY            | Metric record identifier |
| `service_name` | VARCHAR(50)              | NOT NULL               | Service name             |
| `metric_name`  | VARCHAR(100)             | NOT NULL               | Metric name              |
| `metric_value` | DECIMAL(15,4)            | NOT NULL               | Metric value             |
| `unit`         | VARCHAR(20)              | NOT NULL               | Measurement unit         |
| `tags`         | JSONB                    |                        | Additional metric tags   |
| `timestamp`    | TIMESTAMP WITH TIME ZONE | NOT NULL DEFAULT NOW() | Metric timestamp         |

**Constraints**:

- `CHECK (unit IN ('count', 'ms', 'seconds', 'percent', 'bytes', 'rate'))`

---

## Relationships Overview

### Core Relationships

1. **Tenants ← → All Entities**: Every business entity belongs to a tenant for multi-tenancy support
2. **Users ← → Employees**: Users may have associated employee records for HR data
3. **Users ← → AI_Conversations**: Users create and participate in AI conversations
4. **Customers ← → Sales_Pipeline**: Customers have multiple sales opportunities
5. **Employees ← → Manager**: Self-referencing hierarchy for organizational structure
6. **Products ← → Inventory_Levels**: Products tracked across multiple warehouse locations
7. **Risk_Assessments ← → Employees**: Risk owners and responsible parties

### Service Boundaries

- **Auth Service**: users, user_sessions, user_mfa, oauth_connections
- **Sales Service**: customers, sales_pipeline, sales_metrics
- **Finance Service**: finance_metrics, budget_plans, expense_transactions
- **HR Service**: employees, recruitment_pipeline, hr_metrics
- **Products Service**: products, inventory_levels, product_performance
- **Risk Service**: risk_assessments, compliance_status, incidents
- **AI Service**: ai_conversations, ai_messages, ai_analytics
- **Shared**: tenants, audit_logs, system_metrics

---

## Business Rules & Constraints

### Data Quality Rules

1. **Email Validation**: All email fields must match RFC 5322 standard
2. **Phone Validation**: Phone numbers in international format (+country-area-number)
3. **Currency Precision**: All monetary values stored with exactly 2 decimal places
4. **Percentage Range**: All percentage values between 0.00 and 100.00
5. **Date Consistency**: End dates must be after start dates
6. **Positive Values**: Quantities, amounts, and counts must be non-negative

### Security Rules

1. **Password Storage**: Passwords stored using bcrypt with minimum 12 rounds
2. **Token Security**: JWTs include expiration and are invalidated on logout
3. **MFA Enforcement**: Administrative users must enable MFA
4. **Audit Trail**: All data modifications logged with user attribution
5. **Soft Delete**: Business-critical data uses soft delete pattern
6. **Data Encryption**: Sensitive fields (salary, tokens) encrypted at rest

### Performance Rules

1. **Indexing Strategy**: All foreign keys and commonly queried fields indexed
2. **Partitioning**: Time-series data partitioned by date for performance
3. **Archival**: Historical data archived after configurable retention period
4. **Caching**: Frequently accessed lookup data cached at application layer

### Compliance Rules

1. **Data Retention**: Personal data retention periods enforced automatically
2. **Right to Erasure**: Support for GDPR data deletion requests
3. **Access Control**: Row-level security for multi-tenant data isolation
4. **Consent Tracking**: User consent preferences tracked and honored

---

## Docker Integration

### Database Container Configuration

**Base Configuration**:

```yaml
# docker-compose.yml - Database Service
services:
  postgres:
    image: postgres:15-alpine
    container_name: a-ems-postgres
    environment:
      POSTGRES_DB: a_ems
      POSTGRES_USER: a_ems_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_MULTIPLE_DATABASES: 'auth_db,sales_db,finance_db,hr_db,products_db,risk_db,ai_db'
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/database/init:/docker-entrypoint-initdb.d
      - ./backend/database/migrations:/app/migrations
    ports:
      - '5432:5432'
    networks:
      - a-ems-network
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U a_ems_user -d a_ems']
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: '10m'
        max-file: '3'
```

### Development vs Production Configurations

**Development**:

- Single shared database with schema separation
- Debug logging enabled
- Local volume mounts for live schema updates
- No connection pooling

**Production**:

- Service-specific databases for true microservice isolation
- Connection pooling with PgBouncer
- Encrypted storage volumes
- Automated backup scheduling
- Read replicas for analytics queries

### Migration and Seeding Strategy

**Database Initialization**:

```bash
# Located in ./backend/database/init/
01-create-databases.sql    # Create service-specific databases
02-create-extensions.sql   # Enable required PostgreSQL extensions
03-create-schemas.sql      # Create schemas and basic structure
04-seed-reference-data.sql # Insert reference/lookup data
```

**Migration Management**:

- Alembic for Python-based database migrations
- Service-specific migration directories
- Automated migration on container startup
- Rollback capabilities for production deployments

### Backup and Recovery

**Automated Backup**:

```yaml
services:
  postgres-backup:
    image: kartoza/pg-backup:15.0
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_DB: a_ems
      POSTGRES_USER: a_ems_user
      POSTGRES_PASS: ${POSTGRES_PASSWORD}
      BACKUP_FREQUENCY: daily
      BACKUP_RETENTION: 30
    volumes:
      - backup_data:/backup
    depends_on:
      - postgres
    networks:
      - a-ems-network
```

### Monitoring and Logging Integration

**Database Metrics Collection**:

- PostgreSQL metrics exposed via pg_stat_statements
- Custom metrics for business KPIs
- Integration with Prometheus/Grafana stack
- Automated alert configuration for critical metrics

**Query Performance Monitoring**:

- Slow query logging enabled
- Query execution plan analysis
- Index usage monitoring
- Connection pool statistics

This comprehensive data dictionary provides the foundation for implementing a robust, scalable, and maintainable database system that fully supports the A-EMS microservices architecture and business requirements.
