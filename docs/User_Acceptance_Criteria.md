# User Acceptance Criteria (UAC)

_Last updated: 14/09/2025_

This document lists the criteria that must be met for user stories to be considered "done" or "accepted."

---

## Epic: Executive Dashboard

### UAC for US-101: View High-Level Sales KPIs

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** the page loads,
- **Then** I should see sales KPI cards displaying Total Revenue, Pipeline Value, Win Rate, and Customer Acquisition Cost.
- **And** each card must display a title, large numerical value, percentage change from previous period, and visual indicator (green/red) for positive/negative change.

### UAC for US-106: View Financial KPIs

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** the page loads,
- **Then** I should see financial KPI cards displaying Gross Margin, Net Profit, EBITDA, and Cash Flow.
- **And** each financial KPI must include actual value, target value, and progress toward target.
- **And** cash runway must be displayed in months with appropriate color coding (green >12 months, yellow 6-12 months, red <6 months).

### UAC for US-111: View HR Metrics

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** the page loads,
- **Then** I should see HR metrics including total headcount, new hires, departures, and turnover rate.
- **And** employee engagement score must be displayed with trend indicator.
- **And** recruitment metrics must show open positions and time-to-hire average.

### UAC for US-102: View Sales Performance Chart

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** the page loads,
- **Then** I should see a line chart titled "Sales Performance Over Time".
- **And** the chart's x-axis must show the last 12 months.
- **And** the chart must display multiple metrics (revenue, deals closed, pipeline value) with different colored lines.
- **And** hovering over data points must show tooltips with specific values.

### UAC for US-107: View Cash Flow Trends

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** I navigate to the financial section,
- **Then** I should see a cash flow chart showing inflows, outflows, and net cash flow.
- **And** the chart must include projections for the next 3-6 months.
- **And** burn rate and runway calculations must be clearly displayed.

---

## Epic: Advanced Analytics & Insights

### UAC for US-201: View Sales Forecasts

- **Given** I am a logged-in user with access to sales analytics,
- **When** I access the sales forecast section,
- **Then** I should see predicted revenue for the next 30, 90, and 365 days.
- **And** confidence intervals must be displayed (lower and upper bounds).
- **And** I should be able to adjust forecast parameters (seasonality, growth assumptions).

### UAC for US-204: Analyze Profitability

- **Given** I am a logged-in user viewing profitability analysis,
- **When** I select a breakdown type (product, customer segment, or region),
- **Then** I should see a detailed breakdown with revenue, costs, and margin for each category.
- **And** items should be sortable by margin percentage.
- **And** I should be able to drill down into individual categories for more detail.

### UAC for US-207: Analyze Performance Data

- **Given** I am a logged-in user viewing HR analytics,
- **When** I access the performance section,
- **Then** I should see performance scores by department with comparative analysis.
- **And** I should see distribution of performance ratings (exceeds, meets, needs improvement).
- **And** trend data should show performance changes over time.

---

## Epic: AI Chat Assistant

### UAC for US-301: Ask Simple Questions

- **Given** I am a logged-in user on the AI Chat page,
- **When** I type "What was our revenue last month?" into the input box and press Enter,
- **Then** my question should appear in the chat history, right-aligned.
- **And** after a processing time (<5 seconds), a response from the AI should appear, left-aligned.
- **And** the response must contain the correct revenue figure with supporting context (change from previous month, contributing factors).

### UAC for US-304: Ask Comparative Questions

- **Given** I am a logged-in user on the AI Chat page,
- **When** I type "How do Q3 sales compare to Q2?" and press Enter,
- **Then** the AI should provide a detailed comparison including percentage change, absolute difference, and key drivers.
- **And** the response should include relevant context about market conditions or business changes.

### UAC for US-305: Request Visualizations

- **Given** I am a logged-in user on the AI Chat page,
- **When** I type "Show me a chart of pipeline progression over the last 6 months" and press Enter,
- **Then** my question should appear in the chat history.
- **And** the AI's response should contain a rendered chart visualization.
- **And** the chart must correctly represent pipeline data with proper labels and legends.
- **And** I should be able to interact with the chart (hover for details, zoom if applicable).

### UAC for US-307: Ask Finance Questions

- **Given** I am a logged-in user on the AI Chat page,
- **When** I type "What were our main expense increases this quarter?" and press Enter,
- **Then** the AI should provide a breakdown of expense categories with percentage increases.
- **And** the response should include explanations for major increases where data is available.
- **And** recommendations for cost optimization should be included when appropriate.

### UAC for US-310: Ask HR Questions

- **Given** I am a logged-in user on the AI Chat page,
- **When** I type "How is employee satisfaction trending?" and press Enter,
- **Then** the AI should provide current satisfaction scores with trend analysis.
- **And** key drivers of satisfaction changes should be identified.
- **And** actionable recommendations should be provided based on the data.

### UAC for US-302: Maintain Context

- **Given** I am in an active AI chat session,
- **When** I ask a follow-up question like "What about the previous quarter?" without restating the original topic,
- **Then** the AI should understand the context and provide relevant information for the previous quarter.
- **And** the response should reference the original question context.

### UAC for US-303: Handle Limitations

- **Given** I am a logged-in user on the AI Chat page,
- **When** I ask a question that cannot be answered with available data,
- **Then** the AI should clearly state that it cannot provide a complete answer.
- **And** the AI should explain what data would be needed to answer the question.
- **And** the AI should offer alternative questions or analyses that are possible with current data.

---

## Epic: User Authentication & Security

### UAC for US-401: User Login

- **Given** I am on the login page,
- **When** I enter a valid, registered email and the correct password,
- **And** I click the "Log In" button,
- **Then** I should be redirected to the Executive Dashboard.
- **And** my session should be authenticated with appropriate JWT token.
- **And** I should have access to features based on my role permissions.

### UAC for US-401: Failed Login

- **Given** I am on the login page,
- **When** I enter an invalid email or incorrect password,
- **And** I click the "Log In" button,
- **Then** I should remain on the login page.
- **And** an error message "Incorrect email or password" should be displayed.
- **And** no sensitive information should be revealed about which field was incorrect.

### UAC for US-402: Session Management

- **Given** I am logged in and actively using the application,
- **When** I remain idle for the configured timeout period,
- **Then** I should be automatically logged out for security.
- **And** I should see a session timeout message.
- **And** any unsaved work should be preserved where possible.

---

## Epic: Products Dashboard & Analytics

### UAC for US-116: View Product KPIs

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** I navigate to the Products section,
- **Then** I should see product KPI cards displaying Total Products, Inventory Value, Top Performers, and Stock Alerts.
- **And** stock alert cards must show critical and low stock items with quantities and reorder recommendations.
- **And** top performers must display product name, revenue contribution, and units sold.

### UAC for US-117: View Inventory Levels

- **Given** I am a logged-in user on the Products Dashboard page,
- **When** the page loads,
- **Then** I should see inventory levels across all warehouses with real-time stock quantities.
- **And** warehouse capacity utilization must be displayed as percentage with visual indicators.
- **And** low stock alerts must be prominently displayed with recommended actions.

### UAC for US-210: Analyze Product Profitability

- **Given** I am a logged-in user on the Product Analytics page,
- **When** I select "Profitability Analysis",
- **Then** I should see a table of products ranked by profit margin.
- **And** each product must display revenue, cost, profit margin percentage, and trend indicator.
- **And** I must be able to filter by product category, date range, and warehouse location.

---

## Epic: Risk Management & Compliance

### UAC for US-121: View Risk Score

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** I navigate to the Risk section,
- **Then** I should see our overall enterprise risk score with trend indicator.
- **And** risk score must be color-coded (green: low, yellow: medium, red: high, critical: dark red).
- **And** the score breakdown by category must be displayed in a donut chart.

### UAC for US-122: View Active Risks by Category

- **Given** I am a logged-in user on the Risk Dashboard page,
- **When** the page loads,
- **Then** I should see active risks categorized by type (operational, financial, cybersecurity, compliance).
- **And** each risk must display title, severity level, owner, and mitigation status.
- **And** risks must be sortable by severity, date created, and due date.

### UAC for US-213: Conduct Scenario Analysis

- **Given** I am a logged-in user on the Risk Analytics page,
- **When** I select "Scenario Analysis",
- **Then** I should be able to model different risk scenarios and view potential business impact.
- **And** each scenario must show probability, financial impact, and recommended mitigation actions.
- **And** I must be able to save scenarios and share them with stakeholders.

---

## Epic: Reports & Business Intelligence

### UAC for US-401: View Report Catalog

- **Given** I am a logged-in user on the Reports page,
- **When** the page loads,
- **Then** I should see a catalog of all available reports organized by category.
- **And** each report must display name, description, data sources, and last generated timestamp.
- **And** I must be able to search and filter reports by category, access level, and data source.

### UAC for US-402: Generate Custom Reports

- **Given** I am a logged-in user on the Reports page,
- **When** I click "Create Custom Report",
- **Then** I should be able to select data sources, date ranges, filters, and output format.
- **And** the system must show an estimated generation time before I confirm the request.
- **And** I must receive a confirmation with generation ID and progress tracking URL.

### UAC for US-405: Schedule Recurring Reports

- **Given** I am a logged-in user on the Reports page,
- **When** I select "Schedule Report" for any available report,
- **Then** I must be able to set frequency (daily, weekly, monthly), recipients, and delivery method.
- **And** the system must show next execution time and provide schedule confirmation.
- **And** scheduled reports must appear in my "Scheduled Reports" dashboard with management options.

---

## Enhanced AI Chat Assistant Criteria

### UAC for US-313: Products-Related AI Queries

- **Given** I am using the AI chat interface,
- **When** I ask "Which products have the highest profit margins?",
- **Then** the AI should provide a ranked list of products with specific profit margin percentages.
- **And** the response must include revenue and cost data to support the calculation.
- **And** the AI should offer to generate a detailed profitability report if requested.

### UAC for US-316: Risk-Related AI Queries

- **Given** I am using the AI chat interface,
- **When** I ask "What are our highest priority risks?",
- **Then** the AI should provide a prioritized list of active risks with severity levels.
- **And** each risk must include impact assessment and current mitigation status.
- **And** the AI should suggest next steps or actions for high-priority risks.

### UAC for US-319: Report Generation AI Queries

- **Given** I am using the AI chat interface,
- **When** I ask "Generate a quarterly executive summary",
- **Then** the AI should confirm report parameters (data sources, date range) and initiate generation.
- **And** I must receive a generation ID and estimated completion time.
- **And** the AI should notify me when the report is ready for download.

---

## Epic: User Authentication & Security

### UAC for US-501: Basic Login Functionality

- **Given** I am on the A-EMS login page,
- **When** I enter valid email and password credentials,
- **Then** I should be successfully authenticated and redirected to the dashboard.
- **And** I should receive a valid JWT token for subsequent API requests.
- **And** my session should be maintained as I navigate the application.

### UAC for US-502: Session Management

- **Given** I am logged into the A-EMS application,
- **When** I remain inactive for 30 minutes,
- **Then** I should be automatically logged out for security.
- **And** I should receive a warning notification 5 minutes before automatic logout.
- **And** I should have the option to extend my session.

### UAC for US-503: Secure Logout

- **Given** I am logged into the A-EMS application,
- **When** I click the logout button,
- **Then** my session should be terminated server-side.
- **And** I should be redirected to the login page.
- **And** my JWT token should be invalidated and unusable for further requests.

### UAC for US-505: Password Change

- **Given** I am logged in and on the account settings page,
- **When** I submit a password change form with current password and valid new password,
- **Then** my password should be updated successfully.
- **And** all other sessions except current should be terminated.
- **And** I should receive an email confirmation of the password change.

### UAC for US-506: Forgot Password

- **Given** I am on the login page and have forgotten my password,
- **When** I click "Forgot Password" and enter my email address,
- **Then** I should receive a password reset email if the account exists.
- **And** the reset link should be valid for only 1 hour.
- **And** I should be able to set a new password using the reset link.

### UAC for US-507: Password Requirements

- **Given** I am creating or changing a password,
- **When** I enter a password,
- **Then** the system must enforce minimum 8 characters, including uppercase, lowercase, number, and special character.
- **And** real-time validation feedback must be displayed.
- **And** commonly used passwords should be rejected.

### UAC for US-510: MFA Setup

- **Given** I am logged in and want to enable two-factor authentication,
- **When** I navigate to MFA setup in security settings,
- **Then** I should be presented with a QR code and manual entry option.
- **And** I should be able to scan the QR code with my authenticator app.
- **And** I must successfully verify a TOTP code to complete setup.

### UAC for US-511: MFA Login

- **Given** I have MFA enabled and am logging in,
- **When** I enter correct email and password,
- **Then** I should be prompted for a 6-digit TOTP code.
- **And** I should be able to enter the code from my authenticator app.
- **And** successful verification should complete the login process.

### UAC for US-513: MFA Backup Codes

- **Given** I have completed MFA setup,
- **When** the setup is confirmed,
- **Then** I should receive 8 backup codes for emergency access.
- **And** each backup code should be usable only once.
- **And** I should be able to regenerate backup codes when needed.

### UAC for US-517: Google OAuth Login

- **Given** I am on the A-EMS login page,
- **When** I click "Sign in with Google",
- **Then** I should be redirected to Google's authentication page.
- **And** after Google authentication, I should be redirected back to A-EMS.
- **And** if my Google account is authorized, I should be logged in automatically.

### UAC for US-519: Link Google Account

- **Given** I am logged in with email/password and want to link Google,
- **When** I connect my Google account in account settings,
- **Then** my Google account should be successfully linked.
- **And** I should be able to use either authentication method in the future.
- **And** my existing A-EMS data and preferences should remain unchanged.

### UAC for US-523: Admin User Creation

- **Given** I am an administrator in the user management interface,
- **When** I create a new user account with role and permissions,
- **Then** the user account should be created successfully.
- **And** the new user should receive a welcome email with setup instructions.
- **And** the user should be required to set up MFA on first login if configured.

### UAC for US-527: User Management Dashboard

- **Given** I am an administrator,
- **When** I access the user management interface,
- **Then** I should see a list of all user accounts with search and filter capabilities.
- **And** I should be able to view user details, status, and last login information.
- **And** I should be able to activate, deactivate, or reset user accounts.

### UAC for US-531: Session Monitoring

- **Given** I am logged in and viewing my account settings,
- **When** I access the security section,
- **Then** I should see all my active sessions with device and location information.
- **And** I should be able to terminate any individual session remotely.
- **And** I should be able to terminate all other sessions except my current one.

### UAC for US-536: Security Compliance

- **Given** the A-EMS application is in operation,
- **When** any communication occurs between frontend and backend,
- **Then** all data must be encrypted using HTTPS/TLS 1.3 or higher.
- **And** JWT tokens must be stored securely in httpOnly cookies.
- **And** all authentication events must be logged for security auditing.

### UAC for US-537: Brute Force Protection

- **Given** someone attempts to log in to an account,
- **When** there are 5 consecutive failed login attempts,
- **Then** the account should be temporarily locked for 15 minutes.
- **And** the legitimate user should receive an email notification of the lockout.
- **And** administrators should be able to manually unlock accounts if needed.

---

## Cross-Functional Requirements

### Performance Criteria

- **Dashboard Load Time:** Initial dashboard must load within 3 seconds
- **Chart Rendering:** All charts must render within 2 seconds of data availability
- **AI Response Time:** AI responses must be provided within 10 seconds for simple queries
- **Data Refresh:** Real-time data updates should occur without full page refresh

### Accessibility Criteria

- **Keyboard Navigation:** All interactive elements must be accessible via keyboard
- **Screen Reader Support:** All content must be accessible to screen readers
- **Color Contrast:** All text must meet WCAG 2.1 AA contrast requirements
- **Mobile Responsiveness:** All features must work on mobile devices (320px+ width)

### Data Accuracy Criteria

- **KPI Calculations:** All KPI values must match source system calculations within 0.1%
- **Chart Data:** Chart visualizations must accurately represent underlying data
- **AI Responses:** AI-generated insights must be factually correct based on available data
- **Real-time Updates:** Data must be current within 15 minutes of source system updates
