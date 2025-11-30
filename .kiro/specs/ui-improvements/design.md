# UI Improvements Design Document

## Overview

This design document outlines the implementation of UI improvements for the Mirmer AI application, focusing on better settings organization, collapsible sidebar functionality, improved limit messaging, and fixing usage tracking issues. The improvements will enhance user experience by providing clearer navigation, more screen space for conversations, and accurate usage statistics.

## Architecture

The implementation follows a component-based architecture with clear separation between:

1. **Frontend Components** - React components for UI elements
2. **State Management** - Local state and localStorage for persistence
3. **Backend API** - FastAPI endpoints for usage tracking
4. **Database Layer** - PostgreSQL for persistent storage

### Component Hierarchy

```
AppPage
├── Sidebar (collapsible)
│   ├── Conversation List
│   └── Settings Button
├── ChatInterface
│   ├── Messages Display
│   └── Input Area (with limit warning)
└── SettingsPage
    ├── Settings Sidebar (tabs)
    │   ├── Usage Tab
    │   ├── Subscription Tab
    │   └── Profile Tab
    └── Content Area
```

## Components and Interfaces

### 1. Settings Page with Sidebar Navigation

**Component**: `SettingsPage.jsx`

The settings page will be restructured to use a sidebar navigation pattern with three main sections:

**Interface**:
```javascript
// State structure
{
  activeTab: 'usage' | 'subscription' | 'profile',
  user: FirebaseUser,
  usageStats: UsageStats,
  loading: boolean
}

// Tab configuration
const SETTINGS_TABS = [
  { id: 'usage', label: 'Usage', icon: BarChart },
  { id: 'subscription', label: 'Subscription', icon: CreditCard },
  { id: 'profile', label: 'Profile', icon: User }
]
```

**Layout Structure**:
- Left sidebar (250px fixed width) with vertical tab navigation
- Main content area (flex-1) displaying selected tab content
- Neobrutalism styling with bold borders and shadows

### 2. Collapsible Conversation Sidebar

**Component**: `Sidebar.jsx`

Add collapse/expand functionality to the conversation sidebar:

**Interface**:
```javascript
// Props
{
  conversations: Conversation[],
  currentConversationId: string,
  onSelectConversation: (id: string) => void,
  onNewConversation: () => void,
  onDeleteConversation: (id: string) => void,
  userId: string,
  user: FirebaseUser,
  isCollapsed: boolean,  // NEW
  onToggleCollapse: () => void  // NEW
}

// State in parent (AppPage)
{
  sidebarCollapsed: boolean  // persisted in localStorage
}
```

**Behavior**:
- Toggle button positioned at the edge of sidebar
- Smooth CSS transition (300ms) for collapse/expand
- When collapsed: sidebar width = 0, toggle button remains visible
- When expanded: sidebar width = 320px (w-80)
- State persisted in localStorage with key `mirmer_sidebar_collapsed`

### 3. Usage Stats Removal from Sidebar

**Changes to**: `Sidebar.jsx`

Remove the `<UsageStats>` component from the sidebar to provide more space for conversations.

**Before**:
```jsx
<div className="p-4 border-b-4 border-black">
  <UsageStats userId={userId} user={user} />
</div>
```

**After**: Remove this section entirely

### 4. In-Chat Limit Warning

**Component**: `ChatInterface.jsx`

The limit warning is already partially implemented. We'll enhance it to be more prominent:

**Interface**:
```javascript
// Props
{
  conversation: Conversation,
  onSendMessage: (content: string) => void,
  loading: boolean,
  usageStats: UsageStats  // includes daily_used, daily_limit, monthly_used, monthly_limit
}

// Computed values
const isOverDailyLimit = usageStats.daily_used >= usageStats.daily_limit
const isOverMonthlyLimit = usageStats.monthly_used >= usageStats.monthly_limit
const isOverLimit = isOverDailyLimit || isOverMonthlyLimit
```

**Warning Display**:
- Positioned above the input area
- Yellow background (#FFE66D) with black border
- Clear message indicating which limit was reached
- "Upgrade to Pro" button with benefits
- Input field and send button disabled when over limit

### 5. Usage Tracking Fix

**Backend Files**: `usage_postgres.py`, `main.py`, `council.py`

**Issue Analysis**:
The usage tracking appears to be implemented correctly, but there may be timing issues or race conditions. The current flow is:

1. User sends message → `send_message_stream` endpoint
2. Check rate limit → `check_rate_limit()`
3. Add user message → `storage.add_user_message()`
4. **Increment usage** → `usage.increment_usage()`
5. Process council stages
6. Save assistant message

**Potential Issues**:
- Frontend may be fetching stats before backend increments
- Database transaction not committed before stats query
- No explicit refresh trigger after message send

**Solution**:
1. Add explicit commit after increment
2. Add logging to track timing
3. Frontend should refetch stats after receiving 'complete' event
4. Add small delay if needed to ensure consistency

## Data Models

### UsageStats Interface (Frontend)

```typescript
interface UsageStats {
  user_id: string
  tier: 'free' | 'pro' | 'enterprise'
  daily_used: number
  daily_limit: number | 'unlimited'
  monthly_used: number
  monthly_limit: number | 'unlimited'
  total_queries: number
}
```

### Sidebar State (localStorage)

```typescript
interface SidebarState {
  collapsed: boolean
}
// Stored as: localStorage.getItem('mirmer_sidebar_collapsed')
```

### Settings Tab State (localStorage)

```typescript
interface SettingsState {
  activeTab: 'usage' | 'subscription' | 'profile'
}
// Stored as: localStorage.getItem('mirmer_settings_tab')
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Settings tab persistence
*For any* settings tab selection, when a user navigates away and returns to settings, the previously selected tab should still be active
**Validates: Requirements 1.2**

### Property 2: Sidebar state persistence
*For any* sidebar collapse state, when a user reloads the page, the sidebar should restore to the same collapsed/expanded state
**Validates: Requirements 4.5**

### Property 3: Usage stats removal
*For any* conversation page view, the sidebar should not contain a usage stats widget
**Validates: Requirements 2.1**

### Property 4: Limit warning visibility
*For any* user state where daily_used >= daily_limit OR monthly_used >= monthly_limit, the chat interface should display a warning message and disable input
**Validates: Requirements 3.1, 3.5**

### Property 5: Usage increment consistency
*For any* successful message send, the backend should increment usage counters and the frontend should reflect the updated count after completion
**Validates: Requirements 6.1, 6.2, 6.4**

### Property 6: Sidebar collapse animation
*For any* toggle action, the sidebar should transition smoothly between collapsed and expanded states within 300ms
**Validates: Requirements 4.2**

### Property 7: Settings content display
*For any* selected tab in settings, only the content for that specific tab should be visible in the main area
**Validates: Requirements 1.2**

## Error Handling

### Frontend Error Handling

1. **localStorage Failures**
   - Gracefully handle when localStorage is unavailable
   - Fall back to default states (sidebar expanded, usage tab active)
   - Log errors to console for debugging

2. **Usage Stats Fetch Failures**
   - Display loading state while fetching
   - Show error message if fetch fails
   - Provide retry button
   - Don't block UI functionality

3. **State Synchronization**
   - Handle race conditions between message send and stats update
   - Implement retry logic with exponential backoff
   - Show stale data indicator if stats are outdated

### Backend Error Handling

1. **Database Connection Failures**
   - Log detailed error messages
   - Return default free tier stats on error
   - Don't block user from using the app

2. **Usage Increment Failures**
   - Log error with full context
   - Rollback transaction on failure
   - Return error to frontend for user notification

3. **Concurrent Updates**
   - Use database transactions to prevent race conditions
   - Implement proper locking if needed
   - Log all increment operations for debugging

## Testing Strategy

### Unit Testing

We'll write focused unit tests for specific functionality:

1. **Settings Tab Navigation**
   - Test tab switching updates activeTab state
   - Test localStorage persistence on tab change
   - Test initial tab load from localStorage

2. **Sidebar Collapse Logic**
   - Test toggle function updates state correctly
   - Test localStorage persistence
   - Test initial state restoration

3. **Limit Detection**
   - Test isOverLimit calculation with various usage values
   - Test warning message display logic
   - Test input disable logic

4. **Usage Stats Parsing**
   - Test handling of 'unlimited' values
   - Test percentage calculations
   - Test tier detection

### Property-Based Testing

We'll use property-based testing to verify universal behaviors:

**Testing Framework**: We'll use `@fast-check/vitest` for JavaScript/React property-based testing.

**Configuration**: Each property test should run a minimum of 100 iterations.

**Test Tagging**: Each property-based test will be tagged with a comment referencing the design document property.

### Integration Testing

1. **End-to-End Flow**
   - User sends message → usage increments → stats update → UI reflects change
   - User collapses sidebar → state persists → page reload → state restored
   - User switches settings tabs → content updates → state persists

2. **Backend API Testing**
   - Test `/api/usage` endpoint returns correct stats
   - Test usage increment happens on message send
   - Test rate limit check blocks over-limit users

### Manual Testing Checklist

1. Settings page displays three tabs correctly
2. Clicking each tab shows appropriate content
3. Tab selection persists across page reloads
4. Sidebar collapses smoothly with animation
5. Sidebar state persists across page reloads
6. Usage stats removed from conversation sidebar
7. Limit warning appears when limit reached
8. Input disabled when limit reached
9. Usage stats update after sending message
10. All neobrutalism styling consistent

## Implementation Notes

### CSS Transitions

For smooth sidebar collapse:

```css
.sidebar {
  transition: width 300ms ease-in-out, transform 300ms ease-in-out;
}

.sidebar.collapsed {
  width: 0;
  transform: translateX(-100%);
}
```

### localStorage Keys

Standardize localStorage keys with prefix:

- `mirmer_sidebar_collapsed`: boolean
- `mirmer_settings_tab`: string ('usage' | 'subscription' | 'profile')

### API Timing

To fix usage tracking:

1. Backend: Ensure `session.commit()` is called after increment
2. Backend: Add detailed logging with timestamps
3. Frontend: Wait for 'complete' SSE event before refetching stats
4. Frontend: Add 500ms delay before stats refresh (already implemented)

### Neobrutalism Design Tokens

Maintain consistency with existing design:

```javascript
const DESIGN_TOKENS = {
  colors: {
    primary: '#4ECDC4',
    secondary: '#FFE66D',
    accent: '#FF6B6B',
    background: '#f5f5f5',
    border: '#000000'
  },
  borders: {
    standard: '4px solid black',
    thin: '2px solid black'
  },
  shadows: {
    standard: '4px 4px 0px 0px rgba(0,0,0,1)',
    large: '8px 8px 0px 0px rgba(0,0,0,1)',
    hover: '6px 6px 0px 0px rgba(0,0,0,1)'
  }
}
```

## Performance Considerations

1. **Sidebar Animation**: Use CSS transforms instead of width changes for better performance
2. **Usage Stats Polling**: Don't poll continuously, only fetch after message send
3. **localStorage Access**: Minimize reads/writes, batch updates when possible
4. **Component Re-renders**: Use React.memo for settings tab content to prevent unnecessary re-renders

## Accessibility

1. **Keyboard Navigation**: Ensure all tabs and buttons are keyboard accessible
2. **Screen Readers**: Add proper ARIA labels to sidebar toggle and tab navigation
3. **Focus Management**: Maintain focus when toggling sidebar or switching tabs
4. **Color Contrast**: Ensure all text meets WCAG AA standards

## Security Considerations

1. **localStorage**: Don't store sensitive data (only UI preferences)
2. **User ID Validation**: Always validate user_id in backend endpoints
3. **Rate Limiting**: Ensure rate limit checks can't be bypassed
4. **Input Sanitization**: Sanitize all user inputs before storage

## Deployment Considerations

1. **Database Migrations**: No schema changes required
2. **Environment Variables**: No new environment variables needed
3. **Backward Compatibility**: Changes are additive, no breaking changes
4. **Feature Flags**: Consider adding flag for collapsible sidebar if needed

## Future Enhancements

1. **Keyboard Shortcuts**: Add shortcuts for sidebar toggle (e.g., Cmd+B)
2. **Responsive Design**: Optimize for mobile with automatic sidebar collapse
3. **Usage Analytics**: Track which settings tabs are most used
4. **Customization**: Allow users to customize sidebar width
5. **Animations**: Add more delightful micro-interactions
