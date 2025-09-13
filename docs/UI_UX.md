# UI/UX Design Guidelines

## 1. Design Philosophy

- **Clarity & Simplicity:** The UI should be intuitive, clean, and uncluttered. The primary goal is to present complex information in a simple, digestible format.
- **Data-First:** Design decisions should prioritize the clear and accurate representation of data.
- **Efficiency:** The user (a CEO or executive) is time-poor. The interface must enable them to find information and insights as quickly as possible.

## 2. Key Components & Wireframes

### 2.1. Main Layout

The application will use a standard sidebar navigation layout.

- **Sidebar (Left):** Contains links to the main pages:
  - Dashboard
  - AI Chat
  - Reports (Future)
  - Settings (Future)
- **Main Content Area (Right):** Displays the content of the selected page.

### 2.2. Executive Dashboard

The dashboard is the heart of the application. It will be a grid of customizable widgets.

- **Layout:** A responsive grid (e.g., 12-column).
- **Widgets (built with Recharts):**
  - **KPI Cards:** Large, clear display of single key metrics (e.g., "Total Revenue," "New Customers," "Churn Rate").
  - **Line Charts:** For showing trends over time (e.g., "Monthly Recurring Revenue (MRR) over last 12 months").
  - **Bar Charts:** For comparing categories (e.g., "Sales by Region").
  - **Pie/Donut Charts:** For showing composition (e.g., "Revenue by Product Line").
  - **Data Tables:** For displaying detailed, tabular data.

**Wireframe Sketch:**

```
+----------------------------------------------------------------------+
| Sidebar | Header (User Profile, Notifications)                       |
|---------+------------------------------------------------------------|
|         |                                                            |
| Dash    | +-----------------+ +-----------------+ +-----------------+  |
| AI Chat | | KPI: Revenue    | | KPI: Users      | | KPI: Churn      |  |
|         | | $1.2M           | | 10,453          | | 2.1%            |  |
|         | +-----------------+ +-----------------+ +-----------------+  |
|         |                                                            |
|         | +-----------------------------------+ +------------------+   |
|         | | Line Chart: MRR over Time         | | Pie: Sales by..|   |
|         | |                                   | |                  |   |
|         | |                                   | |                  |   |
|         | +-----------------------------------+ +------------------+   |
|         |                                                            |
+----------------------------------------------------------------------+
```

### 2.3. AI Chat Interface

This interface should feel familiar, like modern messaging apps.

- **Layout:**
  - A main chat window displaying the conversation history.
  - A text input box at the bottom for the user to type their query.
- **Message Types:**
  - **User Query:** Right-aligned, simple text bubble.
  - **AI Response (Text):** Left-aligned, may contain formatted text (bold, lists).
  - **AI Response (Data/Chart):** If the AI's response includes a visualization (e.g., "Show me a chart of sales by region"), it should render the chart directly in the chat window. This is a key feature.

**Wireframe Sketch:**

```
+----------------------------------------------------------------------+
| Sidebar | Header                                                     |
|---------+------------------------------------------------------------|
|         |                                                            |
| Dash    | Chat History Window:                                       |
| AI Chat |                                                            |
|         |   [AI]: Hello! How can I help you analyze your business?   |
|         |                                                            |
|         |                [User]: What were our sales in Q2?          |
|         |                                                            |
|         |   [AI]: Sales for Q2 were $450,000. Here is the breakdown: |
|         |   [AI]: +------------------+                               |
|         |        | Bar Chart        |                               |
|         |        +------------------+                               |
|         |                                                            |
|         |------------------------------------------------------------|
|         | [ Type your question...                                  ] |
+----------------------------------------------------------------------+
```

## 3. Design System & Style Guide

### 3.1. Color Palette

- **Primary Colors:**

  - Brand Blue: `#1E40AF` (Primary actions, navigation)
  - Dark Blue: `#1E3A8A` (Hover states, selected states)
  - Light Blue: `#3B82F6` (Secondary elements)

- **Semantic Colors:**

  - Success Green: `#10B981` (Positive KPIs, success messages)
  - Warning Amber: `#F59E0B` (Alerts, warnings)
  - Error Red: `#EF4444` (Errors, declining metrics)
  - Info Cyan: `#06B6D4` (Information, neutral status)

- **Neutral Colors:**
  - Gray 900: `#111827` (Primary text)
  - Gray 700: `#374151` (Secondary text)
  - Gray 500: `#6B7280` (Tertiary text, placeholder)
  - Gray 300: `#D1D5DB` (Borders, dividers)
  - Gray 100: `#F3F4F6` (Background, cards)
  - White: `#FFFFFF` (Primary background)

### 3.2. Typography

- **Primary Font:** Inter (Sans-serif)

  - Headers: Inter 600-700 (Semibold-Bold)
  - Body: Inter 400-500 (Regular-Medium)
  - Small Text: Inter 400 (Regular)

- **Typography Scale:**
  - H1: 2.5rem (40px) - Page titles
  - H2: 2rem (32px) - Section headers
  - H3: 1.5rem (24px) - Subsection headers
  - H4: 1.25rem (20px) - Card titles
  - Body Large: 1.125rem (18px) - Important body text
  - Body: 1rem (16px) - Regular body text
  - Body Small: 0.875rem (14px) - Secondary text
  - Caption: 0.75rem (12px) - Labels, captions

### 3.3. Spacing System

- **Base Unit:** 4px
- **Common Spacing Values:**
  - xs: 4px (1 unit)
  - sm: 8px (2 units)
  - md: 16px (4 units)
  - lg: 24px (6 units)
  - xl: 32px (8 units)
  - 2xl: 48px (12 units)
  - 3xl: 64px (16 units)

### 3.4. Component Guidelines

#### KPI Cards

- **Size:** Minimum 280px width × 160px height
- **Padding:** 24px
- **Border Radius:** 12px
- **Shadow:** 0 1px 3px rgba(0, 0, 0, 0.1)
- **Typography:**
  - Title: Body Small (14px), Gray 700
  - Value: H2 (32px), Gray 900
  - Change: Body Small (14px), Success/Error color

#### Charts & Visualizations

- **Color Palette (Accessible):**

  - Primary: `#3B82F6` (Blue)
  - Secondary: `#10B981` (Green)
  - Tertiary: `#F59E0B` (Amber)
  - Quaternary: `#EF4444` (Red)
  - Quinary: `#8B5CF6` (Purple)
  - Senary: `#06B6D4` (Cyan)

- **Grid Lines:** Gray 200, 1px stroke
- **Axes:** Gray 600, 12px font
- **Legends:** Body Small, Gray 700
- **Tooltips:** White background, Gray 900 text, subtle shadow

#### Buttons

- **Primary Button:**

  - Background: Brand Blue `#1E40AF`
  - Text: White
  - Padding: 12px 24px
  - Border Radius: 8px
  - Hover: Dark Blue `#1E3A8A`

- **Secondary Button:**
  - Background: Gray 100 `#F3F4F6`
  - Text: Gray 700 `#374151`
  - Border: 1px Gray 300
  - Hover: Gray 200

#### Data Tables

- **Header:** Gray 100 background, Gray 900 text, 14px font
- **Rows:** White/Gray 50 alternating, Gray 700 text, 16px font
- **Borders:** Gray 200, 1px
- **Padding:** 16px vertical, 12px horizontal
- **Hover:** Gray 50 background

### 3.5. Layout Specifications

#### Dashboard Grid System

- **Container:** 12-column CSS Grid
- **Breakpoints:**
  - Desktop: 1024px+ (4 columns for KPIs)
  - Tablet: 768px-1023px (2 columns for KPIs)
  - Mobile: < 768px (1 column)

#### Sidebar Navigation

- **Width:** 280px (collapsed: 72px)
- **Background:** White
- **Border:** 1px Gray 200 right border
- **Navigation Items:**
  - Padding: 12px 16px
  - Hover: Gray 50 background
  - Active: Light Blue background, Brand Blue text
  - Icon Size: 20px
- **Menu Structure:**
  - Dashboard (Home icon)
  - Sales (TrendingUp icon)
  - Finance (DollarSign icon)
  - HR (Users icon)
  - Products (Package icon)
  - Risk & Compliance (Shield icon)
  - Reports (FileText icon)
  - AI Assistant (Bot icon)
  - Settings (Settings icon)

### 3.6. Responsive Design Standards

#### Mobile-First Approach

- **Base styles:** Mobile (320px+)
- **Tablet:** 768px+ (md breakpoint)
- **Desktop:** 1024px+ (lg breakpoint)
- **Large Desktop:** 1280px+ (xl breakpoint)

#### Adaptive Components

- **KPI Cards:** Stack vertically on mobile, 2x2 grid on tablet, 4x1 on desktop
- **Charts:** Reduce height on mobile, adjust font sizes
- **Tables:** Horizontal scroll on mobile with sticky first column
- **Sidebar:** Collapsible on tablet, overlay on mobile

### 3.7. Accessibility Standards

#### WCAG 2.1 AA Compliance

- **Color Contrast:** Minimum 4.5:1 for normal text, 3:1 for large text
- **Focus Indicators:** 2px blue outline with 2px offset
- **Alt Text:** All images and charts must have descriptive alt text
- **Keyboard Navigation:** All interactive elements must be keyboard accessible

#### Screen Reader Support

- **Semantic HTML:** Proper heading hierarchy, landmarks
- **ARIA Labels:** For complex widgets and charts
- **Live Regions:** For dynamic content updates
- **Skip Links:** For main navigation

### 3.8. Animation & Interaction Guidelines

#### Micro-interactions

- **Hover Transitions:** 150ms ease-in-out
- **Button Press:** Scale 0.98 transform
- **Loading States:** Subtle pulse animation
- **Page Transitions:** 300ms slide animations

#### Data Updates

- **Chart Animations:** 800ms ease-out transitions
- **KPI Updates:** Highlight with subtle background flash
- **Real-time Data:** Smooth value transitions, not instant jumps
