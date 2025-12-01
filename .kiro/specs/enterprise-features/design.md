# Design Document

## Overview

This design document outlines the architecture and implementation approach for making Mirmer AI a complete, enterprise-ready application. The design focuses on adding critical features for enterprise customer acquisition, enhanced user experience, administrative capabilities, and API access while maintaining the existing 3-stage council architecture.

The implementation will be incremental, ensuring each feature integrates seamlessly with the existing FastAPI backend and React frontend.

## Architecture

### High-Level Architecture

The system maintains the existing architecture with these additions:

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Landing Page │  │   App Page   │  │  Admin Dashboard │  │
│  │ + Contact    │  │ + Search     │  │                  │  │
│  │   Form       │  │ + Export     │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ REST API / SSE
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ API Routes   │  │ Admin Routes │  │  Email Service   │  │
│  │ + Export     │  │              │  │                  │  │
│  │ + Search     │  │              │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Conversations│  │ Enterprise   │  │  API Keys        │  │
│  │ + Tags       │  │ Inquiries    │  │                  │  │
│  │ + Ratings    │  │              │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### New Components

1. **Enterprise Contact System**: Form submission, email notifications, admin tracking
2. **Search Engine**: Full-text search across conversation titles and content
3. **Export Service**: Generate Markdown, PDF, and JSON exports
4. **Sharing Service**: Create and manage shareable conversation links
5. **Rating System**: Store and retrieve user feedback on responses
6. **Admin Dashboard**: Monitor metrics, manage users, track inquiries
7. **API Gateway**: Authenticate and route API requests
8. **Email Service**: Send transactional emails for notifications
9. **Tag Management**: Associate and filter conversations by tags

## Components and Interfaces

### 1. Enterprise Contact Form Component

**Frontend Component**: `EnterpriseContactModal.jsx`

```javascript
interface EnterpriseContactForm {
  name: string;
  email: string;
  company: string;
  companySize: string; // "1-10", "11-50", "51-200", "201-1000", "1000+"
  phone?: string;
  message: string;
  useCase?: string;
}
```

**Backend API Endpoint**: `POST /api/enterprise/contact`

```python
class EnterpriseInquiry(BaseModel):
    name: str
    email: str
    company: str
    company_size: str
    phone: Optional[str]
    message: str
    use_case: Optional[str]
```

### 2. Search System

**Frontend Component**: `SearchBar.jsx` (integrated into Sidebar)

**Backend API Endpoint**: `GET /api/conversations/search?q={query}&user_id={user_id}`

```python
class SearchResult(BaseModel):
    conversation_id: str
    title: str
    snippet: str  # Matching message excerpt
    created_at: str
    match_score: float
```

### 3. Export Service

**Frontend Component**: `ExportMenu.jsx`

**Backend API Endpoints**:
- `GET /api/conversations/{id}/export/markdown`
- `GET /api/conversations/{id}/export/pdf`
- `GET /api/conversations/{id}/export/json`

```python
class ExportFormat(Enum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    JSON = "json"
```

### 4. Sharing Service

**Frontend Component**: `ShareModal.jsx`

**Backend API Endpoints**:
- `POST /api/conversations/{id}/share` - Create share link
- `GET /api/shared/{share_token}` - Access shared conversation
- `DELETE /api/conversations/{id}/share` - Revoke share link

```python
class SharedConversation(BaseModel):
    share_token: str
    conversation_id: str
    created_at: str
    expires_at: Optional[str]
    view_count: int
```

### 5. Rating and Feedback System

**Frontend Component**: `RatingButtons.jsx`

**Backend API Endpoint**: `POST /api/conversations/{id}/messages/{message_index}/rating`

```python
class MessageRating(BaseModel):
    rating: int  # 1 (thumbs down) or 5 (thumbs up)
    feedback_text: Optional[str]
    conversation_id: str
    message_index: int
    user_id: str
    created_at: str
```

### 6. Admin Dashboard

**Frontend Page**: `AdminDashboard.jsx`

**Backend API Endpoints**:
- `GET /api/admin/metrics` - System-wide metrics
- `GET /api/admin/users` - User list with pagination
- `GET /api/admin/users/{user_id}` - Detailed user info
- `GET /api/admin/enterprise-inquiries` - Contact form submissions
- `PATCH /api/admin/enterprise-inquiries/{id}` - Update inquiry status
- `POST /api/admin/users/{user_id}/upgrade` - Manually upgrade user

```python
class AdminMetrics(BaseModel):
    total_users: int
    active_users_today: int
    total_conversations: int
    total_queries_today: int
    free_users: int
    pro_users: int
    enterprise_users: int
    total_revenue_monthly: float
    pending_inquiries: int
```

### 7. API Access System

**Frontend Component**: `APIKeysSettings.jsx`

**Backend API Endpoints**:
- `POST /api/api-keys/generate` - Create new API key
- `GET /api/api-keys` - List user's API keys
- `DELETE /api/api-keys/{key_id}` - Revoke API key
- `POST /api/v1/chat` - API endpoint for sending messages
- `GET /api/v1/conversations` - API endpoint for listing conversations

```python
class APIKey(BaseModel):
    key_id: str
    key_prefix: str  # First 8 chars for display
    name: str
    created_at: str
    last_used_at: Optional[str]
    is_active: bool
```

### 8. Tag Management

**Frontend Component**: `TagManager.jsx`

**Backend API Endpoints**:
- `POST /api/conversations/{id}/tags` - Add tag to conversation
- `DELETE /api/conversations/{id}/tags/{tag}` - Remove tag
- `GET /api/tags` - List all user's tags with counts

```python
class Tag(BaseModel):
    name: str
    color: str  # Hex color code
    conversation_count: int
```

### 9. Email Notification Service

**Backend Service**: `email_service.py`

```python
class EmailService:
    @staticmethod
    def send_enterprise_inquiry_confirmation(email: str, name: str)
    
    @staticmethod
    def send_enterprise_inquiry_notification(inquiry: EnterpriseInquiry)
    
    @staticmethod
    def send_subscription_expiry_reminder(user_email: str, days_remaining: int)
    
    @staticmethod
    def send_usage_limit_alert(user_email: str, percentage: int)
    
    @staticmethod
    def send_subscription_renewal_confirmation(user_email: str, receipt_url: str)
```

## Data Models

### Database Schema Extensions

```sql
-- Enterprise inquiries table
CREATE TABLE enterprise_inquiries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    company_size VARCHAR(50) NOT NULL,
    phone VARCHAR(50),
    message TEXT NOT NULL,
    use_case TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- pending, contacted, qualified, closed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contacted_by VARCHAR(255),
    notes TEXT
);

-- Tags table
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(7) DEFAULT '#4ECDC4',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, name)
);

-- Conversation tags junction table
CREATE TABLE conversation_tags (
    conversation_id VARCHAR(255) NOT NULL,
    tag_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (conversation_id, tag_id),
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Message ratings table
CREATE TABLE message_ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id VARCHAR(255) NOT NULL,
    message_index INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    rating INTEGER NOT NULL CHECK (rating IN (1, 5)),
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(conversation_id, message_index, user_id)
);

-- Shared conversations table
CREATE TABLE shared_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    share_token VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    view_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true
);

-- API keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(8) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Add columns to existing users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture_url TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_preference VARCHAR(20) DEFAULT 'light';
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_notifications_enabled BOOLEAN DEFAULT true;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT false;

-- Add columns to existing conversations table
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS is_archived BOOLEAN DEFAULT false;
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS archived_at TIMESTAMP;
```

## 
#
# Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Enterprise Contact Form Properties

Property 1: Form validation rejects incomplete data
*For any* enterprise contact form submission with missing required fields (name, email, company, or message), the validation should reject the submission and indicate which fields are missing
**Validates: Requirements 1.2**

Property 2: Valid submissions trigger API calls
*For any* valid enterprise contact form data, submitting the form should result in an API call to the backend with the form data
**Validates: Requirements 1.3**

Property 3: Backend storage includes timestamps
*For any* enterprise inquiry received by the backend, storing it in the database should create a record with a timestamp
**Validates: Requirements 1.4**

Property 4: Confirmation emails are sent to submitters
*For any* successfully stored enterprise inquiry, a confirmation email should be sent to the email address provided in the inquiry
**Validates: Requirements 1.5**

Property 5: Admin notifications are sent for new inquiries
*For any* successfully stored enterprise inquiry, an admin notification email should be sent to the configured admin email address
**Validates: Requirements 1.6**

### Search and Organization Properties

Property 6: Search results match query
*For any* search query and set of conversations, all returned results should contain the query text in either the title or message content
**Validates: Requirements 2.1**

Property 7: Matching text is highlighted
*For any* search result, if the conversation title contains the search query, the matching text should be highlighted in the display
**Validates: Requirements 2.2**

Property 8: Rename updates conversation title
*For any* conversation and valid new title, renaming the conversation should immediately update the title in both the UI and database
**Validates: Requirements 2.4**

Property 9: Tag association persists
*For any* conversation and tag, adding the tag to the conversation should create a persistent association in the database
**Validates: Requirements 2.5**

Property 10: Tag filtering is accurate
*For any* tag, filtering conversations by that tag should return only conversations that have been associated with that tag
**Validates: Requirements 2.6**

### Export and Sharing Properties

Property 11: Markdown export contains all content
*For any* conversation, exporting to Markdown should produce a file that contains all user messages and assistant responses from all three stages
**Validates: Requirements 3.2**

Property 12: PDF export produces valid documents
*For any* conversation, exporting to PDF should produce a valid PDF file that can be opened by standard PDF readers
**Validates: Requirements 3.3**

Property 13: JSON export round-trip
*For any* conversation, exporting to JSON and then parsing the JSON should produce a data structure equivalent to the original conversation
**Validates: Requirements 3.4**

Property 14: Share links are unique
*For any* two different conversations, generating share links should produce different unique tokens
**Validates: Requirements 3.5**

Property 15: Shared conversations are accessible without auth
*For any* valid share token, accessing the shared conversation endpoint should return the conversation data without requiring user authentication
**Validates: Requirements 3.6**

### Response Regeneration and Model Selection Properties

Property 16: Regeneration uses same query
*For any* assistant response in a conversation, regenerating should execute the 3-stage council process with the exact same user query that produced the original response
**Validates: Requirements 4.1**

Property 17: Model preferences persist
*For any* Pro user and set of selected models, saving model preferences should persist those selections and retrieve them on subsequent sessions
**Validates: Requirements 4.3**

Property 18: Council respects model preferences
*For any* Pro user with saved model preferences, sending a message should execute the council process using only the models in the user's preferences
**Validates: Requirements 4.4**

### Rating and Feedback Properties

Property 19: Ratings are recorded with metadata
*For any* rating action (thumbs up or down) on an assistant response, the system should store the rating with the conversation ID, message index, user ID, and timestamp
**Validates: Requirements 5.2**

Property 20: Feedback is associated with ratings
*For any* feedback text submitted with a rating, the system should store the feedback text linked to the corresponding rating record
**Validates: Requirements 5.4**

Property 21: Rating indicators are displayed
*For any* conversation that has been rated by the user, viewing the conversation history should display the rating indicator
**Validates: Requirements 5.5**

### Admin Dashboard Properties

Property 22: Admin authorization is enforced
*For any* user attempting to access the admin dashboard, the system should verify admin privileges and deny access to non-admin users
**Validates: Requirements 6.1**

Property 23: Metrics are calculated correctly
*For any* state of the database, the admin dashboard metrics (total users, daily queries, subscriptions, revenue) should accurately reflect the current data
**Validates: Requirements 6.2**

Property 24: User list is complete
*For any* set of users in the database, the admin user list should display all users with their tier, usage, and subscription status
**Validates: Requirements 6.3**

Property 25: User details are accurate
*For any* user selected by an admin, the detailed view should display accurate information including usage history from the database
**Validates: Requirements 6.4**

Property 26: Inquiry list is complete
*For any* set of enterprise inquiries in the database, the admin inquiry list should display all inquiries with their current status
**Validates: Requirements 6.5**

Property 27: Inquiry status updates persist
*For any* enterprise inquiry, when an admin updates its status, the change should be persisted to the database
**Validates: Requirements 6.6**

### API Access Properties

Property 28: API keys are unique
*For any* two API key generation requests, the system should create different unique keys
**Validates: Requirements 7.2**

Property 29: Valid API keys authenticate requests
*For any* API request with a valid API key, the system should authenticate the user and process the request
**Validates: Requirements 7.3**

Property 30: Invalid API keys are rejected
*For any* API request with an invalid or missing API key, the system should return a 401 Unauthorized error
**Validates: Requirements 7.4**

Property 31: API message requests execute council
*For any* valid API request to send a message, the system should execute the full 3-stage council process and return the results
**Validates: Requirements 7.5**

Property 32: API conversation list returns valid JSON
*For any* API request to list conversations, the system should return the user's conversation history as valid, parseable JSON
**Validates: Requirements 7.6**

Property 33: API rate limits are enforced
*For any* user who has exceeded their tier's query limit, API requests should be rejected with a 429 Too Many Requests error
**Validates: Requirements 7.7**

### Conversation Management Properties

Property 34: Bulk selection enables actions
*For any* selection of two or more conversations, the bulk action buttons (delete, archive, tag) should become enabled
**Validates: Requirements 8.1**

Property 35: Archiving removes from main list
*For any* set of conversations, archiving them should mark them as archived in the database and remove them from the main conversation list
**Validates: Requirements 8.2**

Property 36: Archived conversations appear in archive tab
*For any* archived conversation, it should appear in the archived conversations tab and not in the main list
**Validates: Requirements 8.3**

Property 37: Unarchiving restores to main list
*For any* archived conversation, unarchiving should mark it as not archived and restore it to the main conversation list
**Validates: Requirements 8.4**

### User Profile Properties

Property 38: Display name updates propagate
*For any* valid display name change, the update should persist to the database and be reflected in all UI locations (sidebar, settings, messages)
**Validates: Requirements 9.2**

Property 39: Profile pictures are stored and displayed
*For any* valid image file uploaded as a profile picture, the system should store it and display it in the sidebar and settings page
**Validates: Requirements 9.3**

Property 40: Theme changes apply immediately
*For any* theme preference change, the new theme should be applied to the UI immediately without requiring a page reload
**Validates: Requirements 9.5**

### Email Notification Properties

Property 41: Payment failure triggers notification
*For any* subscription payment failure event received from the payment provider, the system should send an email notification to the user
**Validates: Requirements 10.2**

Property 42: Usage limit alerts are sent
*For any* user who reaches 80% of their daily query limit, the system should send an email alert
**Validates: Requirements 10.3**

Property 43: Renewal confirmations are sent
*For any* successful subscription renewal event, the system should send a confirmation email with receipt information
**Validates: Requirements 10.4**

Property 44: Notification preferences are respected
*For any* user who has disabled email notifications in their settings, the system should not send any notification emails to that user
**Validates: Requirements 10.5**

## Error Handling

### Frontend Error Handling

1. **Form Validation Errors**: Display inline error messages for invalid form inputs
2. **API Request Failures**: Show user-friendly error messages with retry options
3. **Export Failures**: Notify users if export generation fails and suggest trying again
4. **Share Link Errors**: Handle expired or invalid share tokens gracefully
5. **Upload Errors**: Validate file types and sizes before upload, show clear error messages

### Backend Error Handling

1. **Database Errors**: Log errors, return 500 status with generic message to users
2. **Email Service Failures**: Log failures but don't block the main operation (e.g., inquiry submission succeeds even if email fails)
3. **API Authentication Errors**: Return appropriate 401/403 status codes with clear messages
4. **Rate Limiting**: Return 429 status with information about when the limit resets
5. **Export Generation Errors**: Catch and log errors, return 500 with user-friendly message
6. **Invalid Share Tokens**: Return 404 for expired/invalid tokens

### Error Logging

- All errors should be logged with context (user ID, operation, timestamp)
- Critical errors (database failures, payment issues) should trigger admin alerts
- Error logs should be structured for easy querying and analysis

## Testing Strategy

### Unit Testing

**Frontend Unit Tests** (using Vitest + React Testing Library):
- Form validation logic
- Search filtering logic
- Tag management functions
- Export format generation
- Theme switching logic
- API client functions

**Backend Unit Tests** (using pytest):
- Input validation functions
- Search query building
- Export generation (Markdown, PDF, JSON)
- Share token generation and validation
- API key generation and hashing
- Email template rendering
- Admin authorization checks

### Property-Based Testing

We will use **fast-check** for JavaScript/TypeScript property-based testing and **Hypothesis** for Python property-based testing.

Each property-based test should run a minimum of 100 iterations to ensure thorough coverage of the input space.

**Property-Based Tests to Implement**:

1. **Form Validation Property Tests**:
   - Generate random form data with missing fields, verify validation catches all cases
   - Generate random valid form data, verify all pass validation

2. **Search Property Tests**:
   - Generate random conversations and search queries, verify all results match the query
   - Generate random search results, verify highlighting is correct

3. **Export Property Tests**:
   - Generate random conversations, verify Markdown export contains all content
   - Generate random conversations, verify JSON export round-trips correctly
   - Generate random conversations, verify PDF export produces valid PDFs

4. **Share Link Property Tests**:
   - Generate multiple share requests, verify all tokens are unique
   - Generate random share tokens, verify access control works correctly

5. **API Key Property Tests**:
   - Generate multiple API key requests, verify all keys are unique
   - Generate random API requests with valid/invalid keys, verify authentication

6. **Tag Property Tests**:
   - Generate random tag operations, verify associations persist correctly
   - Generate random tag filters, verify filtering is accurate

7. **Archive Property Tests**:
   - Generate random archive/unarchive operations, verify state transitions are correct

8. **Rating Property Tests**:
   - Generate random ratings, verify all are stored with correct metadata

### Integration Testing

- Test complete user flows (signup → create conversation → export → share)
- Test admin workflows (view metrics → manage user → update inquiry status)
- Test API workflows (generate key → authenticate → send message → list conversations)
- Test email sending with test email service
- Test payment webhook handling with mock Razorpay events

### End-to-End Testing

- Test critical user journeys in a staging environment
- Test enterprise contact form submission end-to-end
- Test subscription upgrade flow with test payment credentials
- Test API access with real API keys in staging

## Implementation Notes

### Phase 1: Foundation (Enterprise Contact + Search)
- Implement enterprise contact form and backend
- Add email service for notifications
- Implement conversation search functionality
- Add database migrations for new tables

### Phase 2: Export and Sharing
- Implement export service (Markdown, PDF, JSON)
- Add sharing functionality with token generation
- Create public share page

### Phase 3: User Experience Enhancements
- Add rating and feedback system
- Implement tag management
- Add conversation archiving
- Enhance user profile and settings

### Phase 4: Admin and API
- Build admin dashboard
- Implement API key management
- Create API endpoints for programmatic access
- Add API documentation

### Phase 5: Notifications and Polish
- Implement email notification system
- Add scheduled tasks for expiry reminders
- Polish UI/UX across all new features
- Performance optimization

### Technology Choices

**Email Service**: Use **SendGrid** or **AWS SES** for transactional emails
- Reliable delivery
- Template management
- Analytics and tracking
- Reasonable pricing

**PDF Generation**: Use **WeasyPrint** (Python) or **Puppeteer** (Node.js)
- WeasyPrint: Pure Python, good for server-side generation
- Puppeteer: Better styling control, requires Node.js

**API Authentication**: Use **JWT tokens** derived from API keys
- Stateless authentication
- Can include user tier and permissions in token
- Standard approach for API access

**Search Implementation**: Use **PostgreSQL full-text search**
- Already using PostgreSQL
- Good performance for moderate data sizes
- No additional infrastructure needed
- Can upgrade to Elasticsearch later if needed

**File Storage**: Use **AWS S3** or **Cloudinary** for profile pictures
- Scalable and reliable
- CDN integration
- Image optimization

### Security Considerations

1. **API Keys**: Hash keys before storing, only show full key once at generation
2. **Share Tokens**: Use cryptographically secure random generation
3. **Admin Access**: Require additional authentication for sensitive operations
4. **Rate Limiting**: Implement rate limiting on all API endpoints
5. **Input Validation**: Sanitize all user inputs to prevent injection attacks
6. **CORS**: Configure CORS properly for API access
7. **Email**: Validate email addresses, implement rate limiting on email sending
8. **File Uploads**: Validate file types and sizes, scan for malware

### Performance Considerations

1. **Search**: Index conversation titles and content for fast searching
2. **Export**: Generate exports asynchronously for large conversations
3. **Admin Dashboard**: Cache metrics with short TTL to reduce database load
4. **API**: Implement request caching where appropriate
5. **Email**: Queue emails for async sending to avoid blocking requests
6. **Pagination**: Implement pagination for conversation lists and admin views

### Monitoring and Analytics

1. **Track**: Enterprise inquiry conversion rates
2. **Monitor**: API usage patterns and error rates
3. **Alert**: On critical errors (database failures, email service down)
4. **Measure**: Export usage by format
5. **Track**: Share link creation and access patterns
6. **Monitor**: Admin dashboard usage
7. **Measure**: User engagement with new features
