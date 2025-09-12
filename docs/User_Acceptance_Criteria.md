# User Acceptance Criteria (UAC)

This document lists the criteria that must be met for a user story to be considered "done" or "accepted."

---

### UAC for US-101: View High-Level KPIs

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** the page loads,
- **Then** I should see at least three distinct "KPI cards" at the top of the page.
- **And** each card must display a title (e.g., "Total Revenue"), a large numerical value, and a percentage change from the previous period.
- **And** the data must be for the most recently completed period (e.g., last month).

---

### UAC for US-102: View MRR Trend Chart

- **Given** I am a logged-in user on the Executive Dashboard page,
- **When** the page loads,
- **Then** I should see a line chart titled "Monthly Recurring Revenue".
- **And** the chart's x-axis must show the last 12 full months.
- **And** the chart's y-axis must show revenue values.
- **And** hovering over a data point on the line must show a tooltip with the specific month and MRR value.

---

### UAC for US-201: Ask a Simple Question to AI

- **Given** I am a logged-in user on the AI Chat page,
- **When** I type "What were our sales last month?" into the input box and press Enter,
- **Then** my question should appear in the chat history, right-aligned.
- **And** after a short processing time, a response from the AI should appear in the chat history, left-aligned.
- **And** the response must contain the correct sales figure for the previous month.

---

### UAC for US-203: Request a Chart from AI

- **Given** I am a logged-in user on the AI Chat page,
- **When** I type "Show me a pie chart of expenses by department" and press Enter,
- **Then** my question should appear in the chat history.
- **And** the AI's response should contain a rendered pie chart visualization.
- **And** the pie chart must correctly represent the expense data for each department.
- **And** the chart must have a legend or labels indicating which department each slice represents.

---

### UAC for US-301: User Login

- **Given** I am on the login page,
- **When** I enter a valid, registered email and the correct password,
- **And** I click the "Log In" button,
- **Then** I should be redirected to the Executive Dashboard.
- **And** my session should be authenticated.

- **Given** I am on the login page,
- **When** I enter an invalid email or incorrect password,
- **And** I click the "Log In" button,
- **Then** I should remain on the login page.
- **And** an error message "Incorrect email or password" should be displayed.
