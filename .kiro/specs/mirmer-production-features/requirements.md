# Requirements Document - Mirmer AI Production Features

## Introduction

This document outlines the requirements for transforming Mirmer AI from MVP to a production-ready SaaS product with monetization, cloud storage, and enhanced user experience features.

## Glossary

- **Mirmer AI Platform**: The production multi-LLM consultation system
- **Stripe**: Payment processing platform for subscriptions
- **Firestore**: Google's cloud NoSQL database
- **Pro Tier**: Paid subscription tier with unlimited queries
- **Free Tier**: Limited tier with 10 queries/day
- **AI Title Generation**: Using LLM to create conversation titles
- **Conversation Search**: Full-text search across conversation history
- **Export Feature**: Download conversations as PDF or Markdown

## Requirements

### Requirement 1: Stripe Payment Integration

**User Story:** As a user, I want to upgrade to Pro tier with unlimited queries, so that I can use the platform without daily limits

#### Acceptance Criteria

1. THE Mirmer AI Platform SHALL integrate Stripe for payment processing
2. THE Mirmer AI Platform SHALL provide a subscription checkout flow for Pro tier
3. WHEN a user completes payment, THE Mirmer AI Platform SHALL update their tier to "pro"
4. THE Mirmer AI Platform SHALL sync subscription status with Stripe webhooks
5. THE Mirmer AI Platform SHALL allow Pro users unlimited queries per day

### Requirement 2: Firestore Cloud Database

**User Story:** As a developer, I want conversations stored in Firestore, so that data is backed up and accessible from anywhere

#### Acceptance Criteria

1. THE Mirmer AI Platform SHALL store all conversations in Firestore collections
2. THE Mirmer AI Platform SHALL organize conversations by user ID in Firestore
3. THE Mirmer AI Platform SHALL migrate existing JSON conversations to Firestore
4. THE Mirmer AI Platform SHALL implement real-time listeners for conversation updates
5. THE Mirmer AI Platform SHALL maintain backward compatibility during migration

### Requirement 3: AI-Powered Title Generation

**User Story:** As a user, I want meaningful conversation titles, so that I can easily find past conversations

#### Acceptance Criteria

1. WHEN a user sends the first message, THE Mirmer AI Platform SHALL generate a descriptive title using an LLM
2. THE Mirmer AI Platform SHALL limit title generation to 8 words maximum
3. THE Mirmer AI Platform SHALL use the cheapest available model for title generation
4. THE Mirmer AI Platform SHALL run title generation in parallel with the 3-stage process
5. THE Mirmer AI Platform SHALL update the conversation title automatically

### Requirement 4: Conversation Search

**User Story:** As a user, I want to search my conversation history, so that I can quickly find specific topics

#### Acceptance Criteria

1. THE Mirmer AI Platform SHALL provide a search input in the sidebar
2. THE Mirmer AI Platform SHALL search across conversation titles and message content
3. THE Mirmer AI Platform SHALL display search results in real-time as user types
4. THE Mirmer AI Platform SHALL highlight matching text in search results
5. THE Mirmer AI Platform SHALL allow clearing search to show all conversations

### Requirement 5: Export Functionality

**User Story:** As a user, I want to export conversations, so that I can save or share important consultations

#### Acceptance Criteria

1. THE Mirmer AI Platform SHALL provide an export button for each conversation
2. THE Mirmer AI Platform SHALL support export to Markdown format
3. THE Mirmer AI Platform SHALL support export to PDF format
4. THE Mirmer AI Platform SHALL include all 3 stages in exported files
5. THE Mirmer AI Platform SHALL format exported files with proper styling and structure
