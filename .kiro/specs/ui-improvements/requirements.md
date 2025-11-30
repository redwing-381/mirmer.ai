# UI Improvements Requirements

## Introduction

This document defines requirements for improving the user interface with better settings organization, collapsible sidebar, improved limit messaging, and fixing usage tracking issues.

## Glossary

- **Settings Sidebar**: Navigation tabs within settings page (Usage, Subscription, Profile)
- **Collapsible Sidebar**: Conversation list sidebar that can be hidden/shown
- **Limit Message**: In-chat notification when user reaches query limits
- **Neobrutalism**: Design style with bold borders, shadows, and vibrant colors
- **Usage Tracking**: Backend system that records and updates query counts

## Requirements

### Requirement 1

**User Story:** As a user, I want organized settings with tabs, so that I can easily find usage, subscription, and profile information

#### Acceptance Criteria

1. THE Settings Page SHALL display a vertical sidebar with three navigation tabs: Usage, Subscription, and Profile
2. WHEN a user clicks a tab, THE System SHALL display the corresponding content in the main area
3. THE Usage tab SHALL show daily and monthly query statistics with progress bars and detailed breakdown
4. THE Subscription tab SHALL show current plan, benefits, and upgrade/cancel options
5. THE Profile tab SHALL show user information, email, and account settings

### Requirement 2

**User Story:** As a user, I want the usage stats removed from the conversation page sidebar, so that I have more space for my conversation list

#### Acceptance Criteria

1. THE Conversation Page Sidebar SHALL not display the usage stats widget
2. THE Conversation Page Sidebar SHALL display only the conversation list and action buttons
3. THE System SHALL continue to track usage in the background
4. THE Sidebar SHALL display a Settings button that navigates to the Settings page
5. WHEN a user wants to check usage details, THE System SHALL show them in the Settings page Usage tab

### Requirement 3

**User Story:** As a user, I want to see a clear message in the chat when I hit my limit, so that I understand why I cannot continue the conversation

#### Acceptance Criteria

1. WHEN a user reaches their daily or monthly limit, THE System SHALL display a prominent warning message in the chat input area
2. THE Warning message SHALL clearly state which limit was reached (daily or monthly) and the current usage
3. THE Warning message SHALL include an "Upgrade to Pro" button with clear benefits
4. THE Warning message SHALL use the neobrutalism design style with yellow background for high visibility
5. THE System SHALL disable the message input field and send button when limit is reached

### Requirement 4

**User Story:** As a user, I want to collapse the conversation sidebar, so that I have more space to read and focus on the current conversation

#### Acceptance Criteria

1. THE Conversation Page SHALL display a toggle button to collapse and expand the sidebar
2. WHEN a user clicks the toggle button, THE Sidebar SHALL animate smoothly with a slide transition
3. WHEN the sidebar is collapsed, THE Conversation area SHALL expand to use the additional width
4. THE Toggle button SHALL remain visible and accessible when sidebar is collapsed
5. THE System SHALL persist the sidebar state in localStorage and restore it on page reload

### Requirement 5

**User Story:** As a developer, I want to use neobrutalism design components, so that the UI is consistent and visually appealing

#### Acceptance Criteria

1. THE Settings sidebar tabs SHALL use neobrutalism style with bold borders and shadows
2. THE Limit warning message SHALL use neobrutalism alert style with yellow background
3. THE Sidebar toggle button SHALL use neobrutalism button style with icon
4. THE System SHALL maintain consistent spacing, colors, and typography across all components
5. THE Components SHALL be reusable and follow the existing neobrutalism design system

### Requirement 6

**User Story:** As a developer, I want to fix the usage tracking system, so that query counts update correctly in real-time

#### Acceptance Criteria

1. WHEN a user sends a message, THE Backend SHALL increment the usage counters immediately
2. WHEN usage stats are requested, THE Backend SHALL return the current accurate counts
3. THE Backend SHALL log all usage tracking operations for debugging
4. THE Frontend SHALL refresh usage stats after each message is sent
5. THE System SHALL handle race conditions between message sending and stats updates
