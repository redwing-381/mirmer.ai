# Implementation Plan

## Phase 1: Foundation - Enterprise Contact and Search

- [x] 1. Set up email service infrastructure
- [x] 1.1 Install and configure email service library (SendGrid or AWS SES)
  - Add email service credentials to environment variables
  - Create email service configuration in backend
  - _Requirements: 1.5, 1.6, 10.2, 10.3, 10.4_

- [x] 1.2 Create email service module with template rendering
  - Implement `email_service.py` with base email sending functionality
  - Create HTML email templates for enterprise inquiries, notifications
  - _Requirements: 1.5, 1.6_

- [x] 1.3 Write property test for email service
  - **Property 4: Confirmation emails are sent to submitters**
  - **Property 5: Admin notifications are sent for new inquiries**
  - **Validates: Requirements 1.5, 1.6**

- [ ] 2. Implement enterprise contact form backend
- [ ] 2.1 Create database migration for enterprise_inquiries table
  - Add migration script to create enterprise_inquiries table with all fields
  - Run migration in development environment
  - _Requirements: 1.4_

- [ ] 2.2 Create Pydantic models for enterprise inquiries
  - Define `EnterpriseInquiry` request model
  - Define `EnterpriseInquiryResponse` model
  - _Requirements: 1.2, 1.3_

- [ ] 2.3 Implement POST /api/enterprise/contact endpoint
  - Add validation for required fields (name, email, company, message)
  - Store inquiry in database with timestamp
  - Trigger confirmation and admin notification emails
  - _Requirements: 1.2, 1.3, 1.4, 1.5, 1.6_

- [ ] 2.4 Write property test for form validation
  - **Property 1: Form validation rejects incomplete data**
  - **Validates: Requirements 1.2**

- [ ] 2.5 Write property test for inquiry storage
  - **Property 3: Backend storage includes timestamps**
  - **Validates: Requirements 1.4**

- [ ] 3. Implement enterprise contact form frontend
- [ ] 3.1 Create EnterpriseContactModal component
  - Build form UI with all required fields
  - Add form validation logic
  - Implement submission handler with API call
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 3.2 Integrate contact modal into PricingSection
  - Update "Contact Sales" button to open modal
  - Update Enterprise tier "Get Started" to open modal
  - _Requirements: 1.1_

- [ ] 3.3 Write unit test for contact form validation
  - Test that missing required fields are caught
  - Test that valid submissions trigger API call
  - _Requirements: 1.2, 1.3_

- [ ] 4. Implement conversation search functionality
- [ ] 4.1 Add full-text search indexes to conversations table
  - Create database migration to add search indexes on title and messages
  - Optimize for search performance
  - _Requirements: 2.1_

- [ ] 4.2 Implement GET /api/conversations/search endpoint
  - Add query parameter parsing
  - Implement PostgreSQL full-text search query
  - Return matching conversations with snippets
  - _Requirements: 2.1_

- [ ] 4.3 Write property test for search accuracy
  - **Property 6: Search results match query**
  - **Validates: Requirements 2.1**

- [ ] 4.4 Create SearchBar component for frontend
  - Build search input with real-time filtering
  - Implement debouncing for search queries
  - Display search results with highlighting
  - _Requirements: 2.1, 2.2_

- [ ] 4.5 Integrate SearchBar into Sidebar component
  - Add search bar above conversation list
  - Update conversation list to show search results
  - _Requirements: 2.1, 2.2_

- [ ] 4.6 Write property test for search highlighting
  - **Property 7: Matching text is highlighted**
  - **Validates: Requirements 2.2**

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Phase 2: Export and Sharing

- [ ] 6. Implement conversation export backend
- [ ] 6.1 Create export service module
  - Implement Markdown export generator
  - Implement JSON export generator
  - Add export utility functions
  - _Requirements: 3.2, 3.4_

- [ ] 6.2 Install and configure PDF generation library
  - Add WeasyPrint or Puppeteer to dependencies
  - Create PDF template with styling
  - _Requirements: 3.3_

- [ ] 6.3 Implement PDF export generator
  - Convert conversation to HTML
  - Generate styled PDF from HTML
  - _Requirements: 3.3_

- [ ] 6.4 Create export API endpoints
  - Implement GET /api/conversations/{id}/export/markdown
  - Implement GET /api/conversations/{id}/export/pdf
  - Implement GET /api/conversations/{id}/export/json
  - Add proper content-type headers and file downloads
  - _Requirements: 3.2, 3.3, 3.4_

- [ ] 6.5 Write property test for Markdown export
  - **Property 11: Markdown export contains all content**
  - **Validates: Requirements 3.2**

- [ ] 6.6 Write property test for JSON export round-trip
  - **Property 13: JSON export round-trip**
  - **Validates: Requirements 3.4**

- [ ] 6.7 Write property test for PDF export validity
  - **Property 12: PDF export produces valid documents**
  - **Validates: Requirements 3.3**

- [ ] 7. Implement conversation sharing backend
- [ ] 7.1 Create database migration for shared_conversations table
  - Add shared_conversations table with share_token, expires_at, view_count
  - Add indexes for efficient token lookup
  - _Requirements: 3.5_

- [ ] 7.2 Implement share token generation
  - Create cryptographically secure token generator
  - Implement POST /api/conversations/{id}/share endpoint
  - Store share record in database
  - _Requirements: 3.5_

- [ ] 7.3 Implement public share access endpoint
  - Create GET /api/shared/{share_token} endpoint
  - Return conversation data without authentication
  - Increment view count on access
  - _Requirements: 3.6_

- [ ] 7.4 Implement share link revocation
  - Create DELETE /api/conversations/{id}/share endpoint
  - Mark share as inactive in database
  - _Requirements: 3.5_

- [ ] 7.5 Write property test for share token uniqueness
  - **Property 14: Share links are unique**
  - **Validates: Requirements 3.5**

- [ ] 7.6 Write property test for unauthenticated access
  - **Property 15: Shared conversations are accessible without auth**
  - **Validates: Requirements 3.6**

- [ ] 8. Implement export and sharing frontend
- [ ] 8.1 Create ExportMenu component
  - Build dropdown menu with format options
  - Implement download handlers for each format
  - Add loading states during export generation
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 8.2 Create ShareModal component
  - Build modal with share link display
  - Add copy-to-clipboard functionality
  - Show share link statistics (views)
  - Add revoke share option
  - _Requirements: 3.5_

- [ ] 8.3 Create SharedConversationPage component
  - Build public page for viewing shared conversations
  - Display conversation in read-only mode
  - Add "Create your own" CTA
  - _Requirements: 3.6_

- [ ] 8.4 Integrate export and share into ChatInterface
  - Add export button to conversation header
  - Add share button to conversation header
  - _Requirements: 3.1, 3.5_

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Phase 3: User Experience Enhancements

- [ ] 10. Implement rating and feedback system
- [ ] 10.1 Create database migration for message_ratings table
  - Add message_ratings table with rating, feedback_text, conversation_id, message_index
  - Add unique constraint on (conversation_id, message_index, user_id)
  - _Requirements: 5.2, 5.4_

- [ ] 10.2 Implement rating API endpoints
  - Create POST /api/conversations/{id}/messages/{index}/rating endpoint
  - Store rating with metadata (timestamp, user_id)
  - Support optional feedback text
  - _Requirements: 5.2, 5.4_

- [ ] 10.3 Create GET /api/conversations/{id}/ratings endpoint
  - Return all ratings for a conversation
  - Include rating indicators for display
  - _Requirements: 5.5_

- [ ] 10.4 Write property test for rating storage
  - **Property 19: Ratings are recorded with metadata**
  - **Property 20: Feedback is associated with ratings**
  - **Validates: Requirements 5.2, 5.4**

- [ ] 10.5 Create RatingButtons component
  - Build thumbs up/down buttons
  - Add feedback text box on rating
  - Implement rating submission
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 10.6 Integrate ratings into Stage3 component
  - Add RatingButtons below final answer
  - Display existing rating if present
  - _Requirements: 5.1, 5.5_

- [ ] 10.7 Add rating indicators to Sidebar
  - Show rating icons on rated conversations
  - _Requirements: 5.5_

- [ ] 11. Implement tag management system
- [ ] 11.1 Create database migrations for tags tables
  - Add tags table with user_id, name, color
  - Add conversation_tags junction table
  - Add indexes for efficient querying
  - _Requirements: 2.5_

- [ ] 11.2 Implement tag API endpoints
  - Create POST /api/conversations/{id}/tags endpoint
  - Create DELETE /api/conversations/{id}/tags/{tag} endpoint
  - Create GET /api/tags endpoint to list user's tags
  - _Requirements: 2.5, 2.6_

- [ ] 11.3 Write property test for tag associations
  - **Property 9: Tag association persists**
  - **Property 10: Tag filtering is accurate**
  - **Validates: Requirements 2.5, 2.6**

- [ ] 11.4 Create TagManager component
  - Build tag creation UI
  - Implement tag color picker
  - Add tag assignment to conversations
  - _Requirements: 2.5_

- [ ] 11.5 Add tag filtering to Sidebar
  - Display tag list with counts
  - Implement tag filter functionality
  - Show active tag filters
  - _Requirements: 2.6_

- [ ] 11.6 Add context menu to conversation items
  - Implement right-click context menu
  - Add rename, delete, and tag options
  - _Requirements: 2.3_

- [ ] 11.7 Write property test for conversation rename
  - **Property 8: Rename updates conversation title**
  - **Validates: Requirements 2.4**

- [ ] 12. Implement conversation archiving
- [ ] 12.1 Add archive columns to conversations table
  - Create migration to add is_archived and archived_at columns
  - _Requirements: 8.2_

- [ ] 12.2 Implement archive API endpoints
  - Create POST /api/conversations/bulk/archive endpoint
  - Create POST /api/conversations/bulk/unarchive endpoint
  - Create GET /api/conversations/archived endpoint
  - _Requirements: 8.2, 8.3, 8.4_

- [ ] 12.3 Write property test for archive operations
  - **Property 35: Archiving removes from main list**
  - **Property 36: Archived conversations appear in archive tab**
  - **Property 37: Unarchiving restores to main list**
  - **Validates: Requirements 8.2, 8.3, 8.4**

- [ ] 12.4 Add bulk selection to Sidebar
  - Implement checkbox selection for conversations
  - Add bulk action toolbar
  - _Requirements: 8.1_

- [ ] 12.5 Add archived conversations tab
  - Create "Archived" tab in Sidebar
  - Display archived conversations
  - Add unarchive functionality
  - _Requirements: 8.3, 8.4_

- [ ] 12.6 Implement bulk delete with confirmation
  - Add confirmation dialog for bulk delete
  - Implement bulk delete API call
  - _Requirements: 8.5_

- [ ] 13. Enhance user profile and settings
- [ ] 13.1 Add profile columns to users table
  - Create migration for display_name, profile_picture_url, theme_preference, email_notifications_enabled
  - _Requirements: 9.2, 9.3, 9.5, 10.5_

- [ ] 13.2 Implement profile API endpoints
  - Create PATCH /api/users/profile endpoint for display name
  - Create POST /api/users/profile-picture endpoint for image upload
  - Create PATCH /api/users/preferences endpoint for theme and notifications
  - _Requirements: 9.2, 9.3, 9.5, 10.5_

- [ ] 13.3 Write property test for profile updates
  - **Property 38: Display name updates propagate**
  - **Property 40: Theme changes apply immediately**
  - **Validates: Requirements 9.2, 9.5**

- [ ] 13.4 Enhance SettingsPage with profile section
  - Add profile picture upload
  - Add display name editor
  - Display account creation date
  - _Requirements: 9.1, 9.2, 9.3_

- [ ] 13.5 Add preferences section to SettingsPage
  - Add theme selector (light/dark)
  - Add email notification toggle
  - Implement immediate theme application
  - _Requirements: 9.4, 9.5, 10.5_

- [ ] 13.6 Update Sidebar to show profile picture
  - Display user's profile picture in sidebar header
  - _Requirements: 9.3_

- [ ] 14. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Phase 4: Admin Dashboard and API Access

- [ ] 15. Implement admin dashboard backend
- [ ] 15.1 Add is_admin column to users table
  - Create migration to add is_admin boolean column
  - _Requirements: 6.1_

- [ ] 15.2 Create admin authorization middleware
  - Implement admin privilege verification
  - Add admin-only route decorator
  - _Requirements: 6.1_

- [ ] 15.3 Write property test for admin authorization
  - **Property 22: Admin authorization is enforced**
  - **Validates: Requirements 6.1**

- [ ] 15.4 Implement admin metrics endpoint
  - Create GET /api/admin/metrics endpoint
  - Calculate total users, daily queries, subscriptions, revenue
  - _Requirements: 6.2_

- [ ] 15.5 Write property test for metrics calculation
  - **Property 23: Metrics are calculated correctly**
  - **Validates: Requirements 6.2**

- [ ] 15.6 Implement admin users management endpoints
  - Create GET /api/admin/users endpoint with pagination
  - Create GET /api/admin/users/{user_id} endpoint for details
  - Create POST /api/admin/users/{user_id}/upgrade endpoint
  - _Requirements: 6.3, 6.4_

- [ ] 15.7 Write property test for user list completeness
  - **Property 24: User list is complete**
  - **Property 25: User details are accurate**
  - **Validates: Requirements 6.3, 6.4**

- [ ] 15.8 Implement admin enterprise inquiries endpoints
  - Create GET /api/admin/enterprise-inquiries endpoint
  - Create PATCH /api/admin/enterprise-inquiries/{id} endpoint for status updates
  - _Requirements: 6.5, 6.6_

- [ ] 15.9 Write property test for inquiry management
  - **Property 26: Inquiry list is complete**
  - **Property 27: Inquiry status updates persist**
  - **Validates: Requirements 6.5, 6.6**

- [ ] 16. Implement admin dashboard frontend
- [ ] 16.1 Create AdminDashboard page component
  - Build dashboard layout with navigation
  - Add admin route protection
  - _Requirements: 6.1_

- [ ] 16.2 Create MetricsOverview component
  - Display key metrics cards (users, queries, revenue)
  - Add charts for trends
  - _Requirements: 6.2_

- [ ] 16.3 Create UsersManagement component
  - Build user list table with pagination
  - Add search and filter functionality
  - Implement user detail modal
  - Add manual upgrade functionality
  - _Requirements: 6.3, 6.4_

- [ ] 16.4 Create EnterpriseInquiries component
  - Build inquiries table with status tracking
  - Add status update functionality
  - Implement inquiry detail view with notes
  - _Requirements: 6.5, 6.6_

- [ ] 16.5 Add admin navigation to app
  - Add "Admin" link for admin users
  - Create admin route in App.jsx
  - _Requirements: 6.1_

- [ ] 17. Implement API access system
- [ ] 17.1 Create database migration for api_keys table
  - Add api_keys table with key_hash, key_prefix, name, user_id
  - Add indexes for efficient lookup
  - _Requirements: 7.2_

- [ ] 17.2 Implement API key generation
  - Create secure key generation function
  - Implement key hashing for storage
  - Create POST /api/api-keys/generate endpoint
  - _Requirements: 7.2_

- [ ] 17.3 Write property test for API key uniqueness
  - **Property 28: API keys are unique**
  - **Validates: Requirements 7.2**

- [ ] 17.4 Implement API key management endpoints
  - Create GET /api/api-keys endpoint to list keys
  - Create DELETE /api/api-keys/{key_id} endpoint to revoke
  - _Requirements: 7.2_

- [ ] 17.5 Create API authentication middleware
  - Implement API key validation
  - Extract user from API key
  - Add rate limiting for API requests
  - _Requirements: 7.3, 7.4, 7.7_

- [ ] 17.6 Write property test for API authentication
  - **Property 29: Valid API keys authenticate requests**
  - **Property 30: Invalid API keys are rejected**
  - **Property 33: API rate limits are enforced**
  - **Validates: Requirements 7.3, 7.4, 7.7**

- [ ] 17.7 Implement API v1 endpoints
  - Create POST /api/v1/chat endpoint for sending messages
  - Create GET /api/v1/conversations endpoint for listing
  - Add API documentation
  - _Requirements: 7.5, 7.6_

- [ ] 17.8 Write property test for API functionality
  - **Property 31: API message requests execute council**
  - **Property 32: API conversation list returns valid JSON**
  - **Validates: Requirements 7.5, 7.6**

- [ ] 17.9 Create APIKeysSettings component
  - Build API keys management UI
  - Add key generation form
  - Display existing keys with revoke option
  - Show API documentation link
  - _Requirements: 7.1_

- [ ] 17.10 Integrate API settings into SettingsPage
  - Add API Keys tab for Pro/Enterprise users
  - Show upgrade prompt for Free users
  - _Requirements: 7.1_

- [ ] 18. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Phase 5: Notifications and Polish

- [ ] 19. Implement response regeneration
- [ ] 19.1 Add regenerate endpoint
  - Create POST /api/conversations/{id}/messages/{index}/regenerate endpoint
  - Re-run council process with original query
  - Replace message in conversation
  - _Requirements: 4.1_

- [ ] 19.2 Write property test for regeneration
  - **Property 16: Regeneration uses same query**
  - **Validates: Requirements 4.1**

- [ ] 19.3 Add regenerate button to Stage3 component
  - Add "Regenerate" button below final answer
  - Implement regeneration with loading state
  - _Requirements: 4.1_

- [ ] 20. Implement model selection for Pro users
- [ ] 20.1 Add model_preferences column to users table
  - Create migration for JSON column storing selected models
  - _Requirements: 4.3_

- [ ] 20.2 Implement model preferences endpoints
  - Create GET /api/users/model-preferences endpoint
  - Create PATCH /api/users/model-preferences endpoint
  - _Requirements: 4.3_

- [ ] 20.3 Write property test for model preferences
  - **Property 17: Model preferences persist**
  - **Property 18: Council respects model preferences**
  - **Validates: Requirements 4.3, 4.4**

- [ ] 20.4 Update council.py to respect user preferences
  - Modify stage1_collect_responses to use user's selected models
  - Fall back to default models if none selected
  - _Requirements: 4.4_

- [ ] 20.5 Create ModelSelection component
  - Build model selection UI with checkboxes
  - Display model descriptions
  - Save preferences on change
  - _Requirements: 4.2, 4.3_

- [ ] 20.6 Add model selection to SettingsPage
  - Add Models tab for Pro users
  - Show upgrade prompt for Free users
  - _Requirements: 4.2, 4.5_

- [ ] 21. Implement email notification system
- [ ] 21.1 Expand email service with notification templates
  - Add subscription expiry reminder template
  - Add payment failure notification template
  - Add usage limit alert template
  - Add renewal confirmation template
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 21.2 Implement notification trigger functions
  - Create function to send payment failure notifications
  - Create function to send usage limit alerts
  - Create function to send renewal confirmations
  - _Requirements: 10.2, 10.3, 10.4_

- [ ] 21.3 Write property test for notification preferences
  - **Property 41: Payment failure triggers notification**
  - **Property 42: Usage limit alerts are sent**
  - **Property 43: Renewal confirmations are sent**
  - **Property 44: Notification preferences are respected**
  - **Validates: Requirements 10.2, 10.3, 10.4, 10.5**

- [ ] 21.4 Integrate notifications into payment webhook handler
  - Add notification calls to payment failure handler
  - Add notification calls to renewal handler
  - _Requirements: 10.2, 10.4_

- [ ] 21.5 Integrate usage limit alerts into usage tracking
  - Check usage percentage after each query
  - Send alert when reaching 80%
  - Respect user notification preferences
  - _Requirements: 10.3, 10.5_

- [ ] 21.6 Create scheduled task for expiry reminders
  - Implement daily job to check expiring subscriptions
  - Send reminders 7 days before expiry
  - _Requirements: 10.1_

- [ ] 22. Final polish and optimization
- [ ] 22.1 Add loading states and error handling
  - Ensure all async operations have loading indicators
  - Add error boundaries for React components
  - Improve error messages throughout the app
  - _All requirements_

- [ ] 22.2 Optimize database queries
  - Add missing indexes
  - Optimize N+1 queries
  - Add query result caching where appropriate
  - _All requirements_

- [ ] 22.3 Add comprehensive API documentation
  - Create API documentation page
  - Document all API endpoints with examples
  - Add authentication guide
  - _Requirements: 7.5, 7.6_

- [ ] 22.4 Implement analytics tracking
  - Track feature usage (exports, shares, API calls)
  - Track enterprise inquiry conversion
  - Add admin analytics dashboard
  - _Requirements: 6.2_

- [ ] 22.5 Security audit and hardening
  - Review all input validation
  - Audit authentication and authorization
  - Test rate limiting
  - Review CORS configuration
  - _All requirements_

- [ ] 23. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
