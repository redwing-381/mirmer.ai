# Requirements Document

## Introduction

This feature addresses a critical bug where users who purchase a Pro subscription through Razorpay are not seeing their account tier updated from "Free" to "Pro" in the application UI. The payment is processed successfully, but the user profile continues to display the Free plan status, preventing users from accessing Pro features they have paid for.

## Glossary

- **Mirmer AI System**: The multi-LLM consultation platform
- **User Profile**: The account information and subscription status displayed in the settings page
- **Razorpay**: The payment processing service used for subscription management
- **Subscription Tier**: The user's plan level (Free, Pro, or Enterprise)
- **Webhook**: An HTTP callback that Razorpay sends to notify the system of payment events
- **Usage Record**: The database record tracking user query limits and subscription status

## Requirements

### Requirement 1

**User Story:** As a user who purchases a Pro subscription, I want my account to immediately reflect my Pro status, so that I can access the features I paid for without delay.

#### Acceptance Criteria

1. WHEN a user completes a Pro subscription payment THEN the Mirmer AI System SHALL update the user's tier to "pro" in the database
2. WHEN a user's tier is updated to "pro" THEN the Mirmer AI System SHALL update the daily limit to 100 queries
3. WHEN a user's tier is updated to "pro" THEN the Mirmer AI System SHALL update the monthly limit to 3000 queries
4. WHEN a subscription payment is authorized THEN the Mirmer AI System SHALL store the Razorpay subscription ID in the usage record
5. WHEN a subscription status changes THEN the Mirmer AI System SHALL update the subscription_status field in the usage record

### Requirement 2

**User Story:** As a user viewing my settings page, I want to see my current subscription status accurately, so that I know what features I have access to.

#### Acceptance Criteria

1. WHEN a user loads the settings page THEN the Mirmer AI System SHALL fetch the current usage record from the database
2. WHEN displaying subscription information THEN the Mirmer AI System SHALL show the tier value from the usage record
3. WHEN a user's tier is "pro" THEN the Mirmer AI System SHALL display "PRO" as the current plan
4. WHEN a user's tier is "free" THEN the Mirmer AI System SHALL display "FREE" as the current plan
5. WHEN the settings page loads THEN the Mirmer AI System SHALL display the correct daily and monthly limits based on the user's tier

### Requirement 3

**User Story:** As a developer debugging subscription issues, I want comprehensive logging of payment events, so that I can identify and resolve problems quickly.

#### Acceptance Criteria

1. WHEN a Razorpay webhook is received THEN the Mirmer AI System SHALL log the event type and payload
2. WHEN a subscription update fails THEN the Mirmer AI System SHALL log the error with user context
3. WHEN a subscription is successfully updated THEN the Mirmer AI System SHALL log the user ID and new tier
4. WHEN webhook signature verification fails THEN the Mirmer AI System SHALL log the failure with request details
5. WHEN a database update occurs THEN the Mirmer AI System SHALL log the before and after states

### Requirement 4

**User Story:** As a system administrator, I want the subscription status to sync correctly even if webhooks are delayed, so that users always have accurate access to their purchased features.

#### Acceptance Criteria

1. WHEN a user loads the settings page THEN the Mirmer AI System SHALL verify the subscription status with Razorpay if a subscription ID exists
2. WHEN the Razorpay API returns an active subscription THEN the Mirmer AI System SHALL update the local database if it differs
3. WHEN the Razorpay API returns a cancelled subscription THEN the Mirmer AI System SHALL downgrade the user to free tier
4. WHEN the Razorpay API is unavailable THEN the Mirmer AI System SHALL use the cached database value
5. WHEN a subscription status mismatch is detected THEN the Mirmer AI System SHALL log the discrepancy for investigation

### Requirement 5

**User Story:** As a user who just purchased a subscription, I want to see my updated status without refreshing the page, so that I have immediate confirmation of my purchase.

#### Acceptance Criteria

1. WHEN a user completes payment and returns to the app THEN the Mirmer AI System SHALL refresh the usage statistics
2. WHEN usage statistics are refreshed THEN the Mirmer AI System SHALL fetch the latest data from the backend
3. WHEN the backend returns updated tier information THEN the Mirmer AI System SHALL update the UI immediately
4. WHEN the subscription status changes THEN the Mirmer AI System SHALL update all displayed limits and features
5. WHEN a user navigates to the settings page after payment THEN the Mirmer AI System SHALL display the updated Pro status
