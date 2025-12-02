# Design Document

## Overview

This design addresses the critical bug where Pro subscription purchases are not reflected in the user's profile. The issue stems from potential webhook delivery failures, timing issues, and lack of client-side refresh mechanisms. The solution implements a multi-layered approach: improved webhook handling, proactive status verification, enhanced logging, and automatic UI updates.

## Architecture

The subscription status synchronization system consists of three main components:

1. **Webhook Handler** (Backend) - Processes Razorpay webhook events and updates database
2. **Status Verification Service** (Backend) - Proactively checks subscription status with Razorpay API
3. **UI Refresh Mechanism** (Frontend) - Automatically updates displayed subscription information

### Data Flow

```
Payment Completion → Razorpay Webhook → Backend Handler → Database Update
                                                              ↓
User Loads Settings → Backend API → Status Verification → Return Current Status
                                                              ↓
Frontend Receives Data → Update UI → Display Pro Status
```

## Components and Interfaces

### Backend Components

#### 1. Enhanced Webhook Handler (`backend/main.py`)

**Purpose**: Process Razorpay webhook events with improved error handling and logging

**Interface**:
```python
@app.post("/api/webhooks/razorpay")
async def razorpay_webhook(request: Request) -> dict
```

**Responsibilities**:
- Verify webhook signature
- Parse event payload
- Route to appropriate handler based on event type
- Log all events and errors
- Return success/failure status

#### 2. Improved Payment Service (`backend/payments.py`)

**Purpose**: Handle subscription lifecycle events with robust error handling

**Key Methods**:
```python
@staticmethod
def handle_payment_authorized(payload: Dict[str, Any], db: Session) -> bool

@staticmethod
def handle_subscription_updated(payload: Dict[str, Any], db: Session) -> bool

@staticmethod
def verify_and_sync_subscription(user_id: str, db: Session) -> Dict[str, Any]
```

**Enhancements**:
- Add detailed logging before and after database updates
- Implement transaction rollback on errors
- Add subscription status verification method
- Handle edge cases (missing user_id, invalid subscription_id)

#### 3. Status Verification Endpoint (`backend/main.py`)

**Purpose**: Allow frontend to trigger subscription status verification

**Interface**:
```python
@app.get("/api/payments/verify-subscription")
async def verify_subscription_status(user_id: str = Header(...)) -> dict
```

**Responsibilities**:
- Fetch subscription from Razorpay API
- Compare with local database
- Update database if mismatch detected
- Return current status

### Frontend Components

#### 1. Enhanced Settings Page (`frontend/src/pages/SettingsPage.jsx`)

**Purpose**: Display accurate subscription status with automatic refresh

**Key Functions**:
```javascript
const loadUsageStats = async () => { /* ... */ }
const verifySubscriptionStatus = async () => { /* ... */ }
```

**Enhancements**:
- Add subscription verification on page load
- Implement automatic refresh after payment
- Add manual refresh button
- Show loading states during verification

#### 2. Subscription Manager Component (`frontend/src/components/SubscriptionManager.jsx`)

**Purpose**: Display detailed subscription information

**Enhancements**:
- Add real-time status indicator
- Show last sync timestamp
- Add manual sync button
- Display error messages clearly

## Data Models

### Usage Model (Existing - Enhanced)

```python
class Usage(Base):
    __tablename__ = 'usage'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), unique=True, nullable=False, index=True)
    tier = Column(String(20), default='free', nullable=False)
    
    # Subscription fields
    razorpay_subscription_id = Column(String(128), nullable=True, index=True)
    subscription_status = Column(String(20), nullable=True)
    
    # Usage limits
    daily_used = Column(Integer, default=0)
    daily_limit = Column(Integer, default=10)
    monthly_used = Column(Integer, default=0)
    monthly_limit = Column(Integer, default=300)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**No schema changes required** - existing fields are sufficient.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After reviewing the prework, several properties can be consolidated:

- Properties 1.2 and 1.3 (daily/monthly limits) can be combined into a single property about tier-appropriate limits
- Properties 3.1-3.5 (logging) are all variations of "appropriate logging occurs" and can be consolidated
- Properties 2.3 and 2.4 are examples that validate property 2.2
- Properties related to UI updates (5.2, 5.3, 5.4) can be combined into a comprehensive UI sync property

### Correctness Properties

Property 1: Subscription payment updates tier
*For any* successful subscription payment webhook, the user's tier in the database should be updated to "pro" and the razorpay_subscription_id should be stored
**Validates: Requirements 1.1, 1.4**

Property 2: Pro tier sets correct limits
*For any* user upgraded to "pro" tier, the daily_limit should be set to 100 and monthly_limit should be set to 3000
**Validates: Requirements 1.2, 1.3**

Property 3: Status changes update database
*For any* subscription status change event, the subscription_status field in the usage record should be updated to match the new status
**Validates: Requirements 1.5**

Property 4: Displayed tier matches database
*For any* usage record, the tier displayed in the UI should match the tier value stored in the database
**Validates: Requirements 2.2**

Property 5: Tier determines displayed limits
*For any* user tier, the displayed daily and monthly limits should match the expected values for that tier (free: 10/300, pro: 100/3000)
**Validates: Requirements 2.5**

Property 6: All events are logged
*For any* webhook event, subscription update, or error, an appropriate log entry should be created with relevant context (event type, user ID, status changes)
**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

Property 7: Sync corrects mismatches
*For any* mismatch between Razorpay subscription status and local database status, the system should update the local database to match Razorpay and log the discrepancy
**Validates: Requirements 4.2, 4.5**

Property 8: API failures use cached data
*For any* Razorpay API failure, the system should return the cached database value without error
**Validates: Requirements 4.4**

Property 9: UI updates reflect backend changes
*For any* tier or status change received from the backend, all related UI elements (tier badge, limits, features) should update immediately
**Validates: Requirements 5.2, 5.3, 5.4**

## Error Handling

### Webhook Processing Errors

**Scenario**: Webhook signature verification fails
- **Response**: Return 400 Bad Request
- **Logging**: Log the failure with request headers and IP
- **User Impact**: None (invalid webhook rejected)

**Scenario**: Database update fails during webhook processing
- **Response**: Rollback transaction, return 500 Internal Server Error
- **Logging**: Log the error with full context (user_id, subscription_id, error message)
- **User Impact**: Webhook will be retried by Razorpay

**Scenario**: User not found in database
- **Response**: Create new usage record with pro tier
- **Logging**: Log the new user creation
- **User Impact**: None (user gets pro access)

### Status Verification Errors

**Scenario**: Razorpay API is unavailable
- **Response**: Return cached database value
- **Logging**: Log the API failure
- **User Impact**: User sees last known status (may be stale)

**Scenario**: Subscription ID not found in Razorpay
- **Response**: Mark subscription as invalid, downgrade to free
- **Logging**: Log the invalid subscription
- **User Impact**: User loses pro access (requires support intervention)

**Scenario**: Network timeout during verification
- **Response**: Return cached database value after timeout
- **Logging**: Log the timeout
- **User Impact**: User sees last known status

### Frontend Errors

**Scenario**: API call fails when loading settings
- **Response**: Display error message, show cached data if available
- **Logging**: Console error log
- **User Impact**: User sees error message, may need to refresh

**Scenario**: Subscription data is missing or malformed
- **Response**: Display "Unknown" status, provide refresh button
- **Logging**: Console error log
- **User Impact**: User can manually refresh to retry

## Testing Strategy

### Unit Testing

**Backend Unit Tests**:
- Test webhook signature verification with valid/invalid signatures
- Test payment handler with various webhook payloads
- Test status verification with mocked Razorpay API responses
- Test error handling for missing user_id, invalid subscription_id
- Test database transaction rollback on errors

**Frontend Unit Tests**:
- Test settings page data loading
- Test UI updates when tier changes
- Test error message display
- Test manual refresh functionality

### Property-Based Testing

We will use **Hypothesis** (Python) for backend property-based testing.

Each property-based test should run a minimum of 100 iterations to ensure comprehensive coverage.

**Backend Property Tests**:
- Property 1: Generate random webhook payloads with valid subscription data, verify tier updates
- Property 2: Generate random user records, upgrade to pro, verify limits are 100/3000
- Property 3: Generate random status change events, verify database updates
- Property 6: Generate random webhook events, verify log entries are created
- Property 7: Generate random subscription states with mismatches, verify sync behavior
- Property 8: Simulate API failures, verify cached data is returned

**Frontend Property Tests** (if applicable):
- Property 4: Generate random usage records, verify displayed tier matches
- Property 5: Generate random tiers, verify displayed limits match expected values
- Property 9: Generate random tier changes, verify all UI elements update

### Integration Testing

**End-to-End Scenarios**:
1. Complete payment flow: Simulate Razorpay webhook → Verify database update → Load settings page → Verify UI shows Pro
2. Status sync flow: Create mismatch → Load settings page → Verify sync occurs → Verify UI updates
3. Error recovery flow: Simulate API failure → Verify cached data shown → API recovers → Verify sync occurs

### Manual Testing Checklist

- [ ] Purchase Pro subscription through Razorpay test mode
- [ ] Verify webhook is received and processed
- [ ] Check database for tier update
- [ ] Load settings page and verify Pro status displayed
- [ ] Verify daily/monthly limits show 100/3000
- [ ] Test manual refresh button
- [ ] Simulate webhook failure and verify recovery
- [ ] Test with expired subscription
- [ ] Test with cancelled subscription

## Implementation Notes

### Webhook Reliability

Razorpay webhooks may be delayed or fail. The system must handle:
- **Delayed webhooks**: Status verification on page load ensures eventual consistency
- **Failed webhooks**: Manual refresh button allows users to trigger sync
- **Duplicate webhooks**: Idempotent handlers prevent double-processing

### Database Transactions

All subscription updates must be atomic:
```python
try:
    usage.tier = 'pro'
    usage.daily_limit = 100
    usage.monthly_limit = 3000
    usage.razorpay_subscription_id = subscription_id
    usage.subscription_status = 'active'
    db.commit()
except Exception as e:
    db.rollback()
    logger.error(f"Failed to update subscription: {e}")
    raise
```

### Logging Standards

All logs must include:
- Timestamp (automatic)
- User ID (when available)
- Event type
- Before/after states (for updates)
- Error details (for failures)

Example:
```python
logger.info(f"Subscription updated - User: {user_id}, Tier: {old_tier} → {new_tier}, Status: {status}")
```

### Frontend State Management

Settings page should:
1. Load usage stats on mount
2. Trigger verification if subscription_id exists
3. Update state when verification completes
4. Provide manual refresh button
5. Show loading indicators during async operations

## Security Considerations

### Webhook Security

- **Signature Verification**: All webhooks must have valid Razorpay signatures
- **HTTPS Only**: Webhook endpoint must use HTTPS in production
- **Rate Limiting**: Implement rate limiting to prevent webhook flooding
- **Payload Validation**: Validate all webhook payload fields before processing

### API Security

- **Authentication**: All status verification requests must include valid Firebase token
- **Authorization**: Users can only verify their own subscription status
- **Input Validation**: Validate all user inputs (user_id, subscription_id)

## Performance Considerations

### Webhook Processing

- **Async Processing**: Webhook handler should return quickly (< 1 second)
- **Database Indexing**: Ensure user_id and razorpay_subscription_id are indexed
- **Connection Pooling**: Use database connection pooling for concurrent webhooks

### Status Verification

- **Caching**: Cache Razorpay API responses for 5 minutes to reduce API calls
- **Timeout**: Set 5-second timeout for Razorpay API calls
- **Fallback**: Always have cached database value as fallback

### Frontend Performance

- **Debouncing**: Debounce manual refresh button (prevent spam)
- **Loading States**: Show loading indicators to improve perceived performance
- **Error Recovery**: Implement exponential backoff for failed API calls

## Deployment Considerations

### Environment Variables

Required environment variables:
- `RAZORPAY_KEY_ID`: Razorpay API key
- `RAZORPAY_KEY_SECRET`: Razorpay API secret
- `RAZORPAY_WEBHOOK_SECRET`: Webhook signature verification secret
- `DATABASE_URL`: PostgreSQL connection string

### Database Migration

No schema changes required. Existing `usage` table has all necessary fields.

### Monitoring

Set up monitoring for:
- Webhook processing success/failure rates
- Subscription status sync frequency
- API error rates
- Database update failures

### Rollback Plan

If issues occur:
1. Disable webhook processing (return 200 OK without processing)
2. Use admin script to manually update user tiers
3. Investigate logs to identify root cause
4. Fix issue and re-enable webhook processing
5. Manually sync any users affected during downtime
