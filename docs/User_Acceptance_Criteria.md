# User Acceptance Criteria (UAC)

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
