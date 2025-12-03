# Design Document

## Overview

This design document outlines the approach for making the Mirmer AI conversation and settings pages fully responsive across all device sizes. The solution leverages Tailwind CSS responsive utilities to adapt layouts for mobile (< 768px), tablet (768px - 1024px), and desktop (> 1024px) devices while maintaining the existing brutalist design aesthetic.

The key challenge is transforming the fixed-width sidebar layout and desktop-optimized components into flexible, touch-friendly interfaces that work seamlessly on smaller screens without sacrificing functionality or visual identity.

## Architecture

### Responsive Strategy

The responsive design follows a mobile-first approach with progressive enhancement:

1. **Base styles**: Optimized for mobile devices (320px - 767px)
2. **Tablet breakpoint (md:)**: Enhanced layout for tablets (768px - 1023px)
3. **Desktop breakpoint (lg:)**: Full desktop experience (1024px+)

### Component Hierarchy

```
AppPage (Responsive Container)
├── Sidebar (Mobile: Overlay, Desktop: Fixed)
│   ├── Header (Responsive padding)
│   ├── SearchBar (Full width on mobile)
│   ├── ConversationList (Scrollable)
│   └── SettingsButton (Touch-friendly)
├── ChatInterface (Flexible layout)
│   ├── Header (Responsive with hamburger menu)
│   ├── MessagesArea (Adaptive padding)
│   │   ├── Stage1 (Stacked on mobile)
│   │   ├── Stage2 (Stacked on mobile)
│   │   └── Stage3 (Full width)
│   └── InputArea (Touch-optimized)
└── ExportMenu (Repositioned for mobile)

SettingsPage (Responsive Container)
├── Header (Responsive with back button)
└── Content
    ├── TabNavigation (Horizontal on mobile, Sidebar on desktop)
    └── TabContent (Full width on mobile, Constrained on desktop)
```


## Components and Interfaces

### 1. AppPage Component

**Responsive Behavior:**
- Mobile: Sidebar as full-screen overlay, hamburger menu in header
- Tablet: Narrower sidebar (240px) or overlay based on preference
- Desktop: Fixed 320px sidebar

**Key Changes:**
- Add hamburger menu button for mobile
- Implement overlay backdrop for mobile sidebar
- Adjust margin-left based on sidebar state and screen size
- Make header stack vertically on mobile

### 2. Sidebar Component

**Responsive Behavior:**
- Mobile: Full-screen overlay (z-index: 50), slide-in animation
- Tablet: 240px fixed or overlay
- Desktop: 320px fixed

**Key Changes:**
- Add mobile overlay mode with backdrop
- Implement close button for mobile
- Adjust conversation list item sizing for touch
- Make search bar full-width on all sizes

### 3. ChatInterface Component

**Responsive Behavior:**
- Mobile: Full-width messages, reduced padding, stacked layout
- Tablet: Moderate padding, optimized message width
- Desktop: Current layout with max-width constraints

**Key Changes:**
- Reduce padding on mobile (p-2 instead of p-4)
- Stack user info and logout button on mobile
- Make input area stack vertically on very small screens
- Adjust textarea height for mobile keyboards

### 4. Stage Components (Stage1, Stage2, Stage3)

**Responsive Behavior:**
- Mobile: Single column, full-width cards
- Tablet: Two columns where appropriate
- Desktop: Current multi-column layout

**Key Changes:**
- Use responsive grid (grid-cols-1 md:grid-cols-2 lg:grid-cols-3)
- Adjust card padding for mobile
- Make tabs scrollable horizontally on mobile if needed
- Ensure code blocks scroll horizontally on overflow

### 5. SettingsPage Component

**Responsive Behavior:**
- Mobile: Stacked layout, tabs at top
- Tablet: Sidebar navigation with narrower content
- Desktop: Current sidebar + content layout

**Key Changes:**
- Convert sidebar to horizontal tabs on mobile
- Stack all content vertically on mobile
- Make buttons full-width on mobile
- Adjust card padding for smaller screens


## Data Models

No new data models are required. This feature only modifies the presentation layer using existing data structures.

### Existing Models Used:
- Conversation objects (id, title, created_at, messages)
- Message objects (role, content, stage1, stage2, stage3)
- UsageStats objects (tier, daily_limit, daily_queries_used, etc.)
- User objects (uid, displayName, email, photoURL)

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Acceptance Criteria Testing Prework:

1.1 WHEN a user accesses the conversation page on a mobile device THEN the system SHALL display the sidebar as an overlay that can be toggled
Thoughts: This is about UI behavior on mobile devices. We can test this by setting viewport width to mobile size and checking if sidebar has overlay classes and toggle functionality works.
Testable: yes - example

1.2 WHEN the sidebar is open on mobile THEN the system SHALL overlay the chat interface and provide a close button or backdrop
Thoughts: This is testing specific UI state on mobile. We can verify the presence of overlay, backdrop, and close button when sidebar is open.
Testable: yes - example

1.3 WHEN a user views messages on mobile THEN the system SHALL display them in a single column with appropriate padding and font sizes
Thoughts: This is about layout behavior across all messages on mobile. We can test that all messages use single-column layout.
Testable: yes - property

1.4 WHEN a user types a message on mobile THEN the system SHALL provide a touch-friendly input area with adequate size for mobile keyboards
Thoughts: This is testing that input elements meet minimum size requirements. We can verify dimensions meet touch target guidelines.
Testable: yes - example

1.5 WHEN the header is displayed on mobile THEN the system SHALL show essential elements only and hide or collapse secondary information
Thoughts: This is about responsive visibility of header elements. We can test that certain elements are hidden on mobile viewport.
Testable: yes - example

2.1 WHEN a user accesses the settings page on a mobile device THEN the system SHALL display the sidebar navigation as a horizontal tab bar or stacked layout
Thoughts: This is testing layout transformation on mobile. We can verify the navigation changes from sidebar to horizontal/stacked.
Testable: yes - example

2.2 WHEN viewing usage statistics on mobile THEN the system SHALL display progress bars and metrics in a vertical stack with readable font sizes
Thoughts: This is about layout of usage stats on mobile. We can verify vertical stacking and minimum font sizes.
Testable: yes - example

2.3 WHEN viewing subscription information on mobile THEN the system SHALL display plan details and upgrade buttons in a mobile-optimized layout
Thoughts: This is testing mobile layout of subscription section. We can verify layout adapts appropriately.
Testable: yes - example

2.4 WHEN the user profile section is displayed on mobile THEN the system SHALL show account information in a vertical layout with appropriate spacing
Thoughts: This is testing profile section layout on mobile. We can verify vertical stacking and spacing.
Testable: yes - example

2.5 WHEN navigation elements are displayed on mobile THEN the system SHALL provide touch-friendly buttons with minimum 44px touch targets
Thoughts: This is a rule that should apply to all navigation buttons. We can test that all buttons meet minimum size.
Testable: yes - property

3.1 WHEN a user accesses the application on a tablet device THEN the system SHALL display a layout optimized for medium-sized screens
Thoughts: This is testing overall layout at tablet breakpoint. We can verify appropriate styles are applied.
Testable: yes - example

3.2 WHEN the sidebar is displayed on tablet THEN the system SHALL show it as a narrower panel or collapsible overlay based on orientation
Thoughts: This is testing sidebar behavior on tablet. We can verify width and behavior at tablet breakpoint.
Testable: yes - example

3.3 WHEN viewing conversations on tablet THEN the system SHALL adjust message widths and spacing for optimal readability
Thoughts: This is testing message layout on tablet. We can verify appropriate widths and spacing.
Testable: yes - example

3.4 WHEN viewing settings on tablet THEN the system SHALL display content in a two-column layout where appropriate
Thoughts: This is testing settings layout on tablet. We can verify column layout at tablet breakpoint.
Testable: yes - example

3.5 WHEN touch interactions occur on tablet THEN the system SHALL provide adequate touch targets for all interactive elements
Thoughts: This is a rule for all interactive elements on tablet. We can test minimum touch target sizes.
Testable: yes - property

4.1 WHEN a user performs any action on mobile THEN the system SHALL provide the same functionality as desktop with adapted UI
Thoughts: This is about functional equivalence across devices. We can test that all features work on mobile.
Testable: yes - property

4.2 WHEN responsive breakpoints are triggered THEN the system SHALL smoothly transition between layouts without losing state
Thoughts: This is about state preservation during resize. We can test that component state persists across breakpoints.
Testable: yes - property

4.3 WHEN the viewport is resized THEN the system SHALL dynamically adjust the layout in real-time
Thoughts: This is testing responsive behavior during resize. We can verify layout updates on viewport changes.
Testable: yes - property

4.4 WHEN touch gestures are used THEN the system SHALL respond appropriately to swipes, taps, and long-presses where applicable
Thoughts: This is about touch interaction support. This is more about user experience than testable behavior.
Testable: no

4.5 WHEN the device orientation changes THEN the system SHALL adapt the layout to the new orientation
Thoughts: This is testing orientation change handling. We can verify layout adapts to portrait/landscape.
Testable: yes - example

5.1 WHEN action buttons are displayed on mobile THEN the system SHALL position them accessibly without overlapping content
Thoughts: This is a rule for all action buttons on mobile. We can test positioning doesn't cause overlaps.
Testable: yes - property

5.2 WHEN the export menu is opened on mobile THEN the system SHALL display options in a mobile-friendly format
Thoughts: This is testing export menu on mobile. We can verify mobile-optimized display.
Testable: yes - example

5.3 WHEN multiple buttons are present on mobile THEN the system SHALL stack or group them appropriately for touch interaction
Thoughts: This is a rule for button layout on mobile. We can test that buttons are properly stacked/grouped.
Testable: yes - property

5.4 WHEN the user scrolls on mobile THEN the system SHALL keep critical action buttons accessible via fixed positioning or easy reach
Thoughts: This is testing button accessibility during scroll. We can verify buttons remain accessible.
Testable: yes - example

5.5 WHEN buttons are displayed on mobile THEN the system SHALL ensure minimum 44px height for touch targets
Thoughts: This is a rule for all buttons on mobile. We can test minimum height requirement.
Testable: yes - property

6.1 WHEN Stage 1 responses are displayed on mobile THEN the system SHALL show individual model responses in a vertically stacked layout
Thoughts: This is testing Stage 1 layout on mobile. We can verify vertical stacking.
Testable: yes - example

6.2 WHEN Stage 2 rankings are displayed on mobile THEN the system SHALL present peer review information in a mobile-optimized format
Thoughts: This is testing Stage 2 layout on mobile. We can verify mobile-optimized display.
Testable: yes - example

6.3 WHEN Stage 3 synthesis is displayed on mobile THEN the system SHALL display the final answer with appropriate text wrapping and spacing
Thoughts: This is testing Stage 3 layout on mobile. We can verify text wrapping and spacing.
Testable: yes - example

6.4 WHEN tabs are used to switch between stages on mobile THEN the system SHALL provide touch-friendly tab controls
Thoughts: This is testing tab controls on mobile. We can verify touch-friendly sizing.
Testable: yes - example

6.5 WHEN code blocks or formatted content appear in responses THEN the system SHALL enable horizontal scrolling for overflow content
Thoughts: This is a rule for all code blocks. We can test that overflow content scrolls horizontally.
Testable: yes - property

7.1 WHEN implementing responsive layouts THEN the system SHALL use Tailwind CSS responsive prefixes (sm:, md:, lg:, xl:)
Thoughts: This is about implementation approach, not functional behavior.
Testable: no

7.2 WHEN defining breakpoints THEN the system SHALL follow Tailwind's default breakpoint system
Thoughts: This is about implementation standards, not functional behavior.
Testable: no

7.3 WHEN hiding or showing elements responsively THEN the system SHALL use Tailwind's display utilities (hidden, block, flex)
Thoughts: This is about implementation approach, not functional behavior.
Testable: no

7.4 WHEN adjusting spacing on different screens THEN the system SHALL use Tailwind's responsive spacing utilities
Thoughts: This is about implementation approach, not functional behavior.
Testable: no

7.5 WHEN implementing the mobile UI THEN the system SHALL maintain the existing brutalist design aesthetic with borders and shadows
Thoughts: This is about design consistency, which is subjective and not automatically testable.
Testable: no


### Property Reflection

Reviewing all testable properties to eliminate redundancy:

**Touch Target Properties (2.5, 3.5, 5.5):**
- 2.5: Navigation elements minimum 44px
- 3.5: All interactive elements adequate touch targets on tablet
- 5.5: Buttons minimum 44px height on mobile
- **Decision**: These can be combined into one comprehensive property about minimum touch target sizes across all interactive elements

**Button Layout Properties (5.1, 5.3):**
- 5.1: Action buttons positioned without overlapping
- 5.3: Multiple buttons stacked/grouped appropriately
- **Decision**: These are related but test different aspects - keep both

**Functional Equivalence Properties (4.1, 4.2, 4.3):**
- 4.1: Same functionality on mobile as desktop
- 4.2: State preserved during breakpoint transitions
- 4.3: Layout adjusts dynamically on resize
- **Decision**: These test different aspects of responsive behavior - keep all three

**Code Block Property (6.5):**
- Stands alone as a specific requirement for overflow handling
- **Decision**: Keep as is

After reflection, we'll consolidate the touch target properties into one comprehensive property and keep the rest as they provide unique validation value.

### Correctness Properties

Property 1: Touch target minimum size
*For any* interactive element (button, link, input, tab) on mobile or tablet viewports, the touch target should have minimum dimensions of 44px x 44px to ensure accessibility
**Validates: Requirements 2.5, 3.5, 5.5**

Property 2: Single column message layout on mobile
*For any* message displayed on mobile viewport (< 768px), the layout should use a single column with full width
**Validates: Requirements 1.3**

Property 3: Functional equivalence across devices
*For any* feature available on desktop, the same functionality should be accessible on mobile and tablet devices with adapted UI
**Validates: Requirements 4.1**

Property 4: State preservation during responsive transitions
*For any* component state (form inputs, conversation selection, tab selection), resizing the viewport across breakpoints should preserve the state without data loss
**Validates: Requirements 4.2**

Property 5: Dynamic layout adjustment
*For any* viewport resize event, the layout should dynamically update to match the appropriate breakpoint styles in real-time
**Validates: Requirements 4.3**

Property 6: Action button positioning
*For any* action button on mobile viewport, the positioning should not cause overlap with content or other interactive elements
**Validates: Requirements 5.1**

Property 7: Button grouping on mobile
*For any* set of multiple buttons on mobile viewport, they should be stacked vertically or grouped horizontally with adequate spacing for touch interaction
**Validates: Requirements 5.3**

Property 8: Code block horizontal scrolling
*For any* code block or pre-formatted content that exceeds container width, horizontal scrolling should be enabled to prevent layout breaking
**Validates: Requirements 6.5**


## Error Handling

### Viewport Detection Errors
- **Issue**: Browser doesn't support viewport queries
- **Handling**: Fallback to desktop layout with warning in console

### Touch Event Errors
- **Issue**: Touch events not supported on device
- **Handling**: Gracefully degrade to mouse events, maintain functionality

### Orientation Change Errors
- **Issue**: Layout doesn't update on orientation change
- **Handling**: Add event listener for orientation change, force re-render if needed

### Sidebar State Persistence Errors
- **Issue**: localStorage not available or quota exceeded
- **Handling**: Catch errors, use in-memory state as fallback, log warning

### Responsive Image Loading Errors
- **Issue**: Images fail to load on mobile network
- **Handling**: Provide fallback placeholder, retry mechanism

## Testing Strategy

### Unit Testing

Unit tests will verify specific responsive behaviors and component rendering:

1. **Sidebar Component Tests**
   - Test sidebar renders as overlay on mobile viewport
   - Test sidebar toggle functionality
   - Test backdrop click closes sidebar on mobile
   - Test sidebar width at different breakpoints

2. **AppPage Component Tests**
   - Test hamburger menu appears on mobile
   - Test header layout stacks on mobile
   - Test margin adjustment based on sidebar state and viewport

3. **ChatInterface Component Tests**
   - Test message layout on different viewports
   - Test input area stacking on mobile
   - Test export button positioning on mobile

4. **SettingsPage Component Tests**
   - Test tab navigation switches from sidebar to horizontal on mobile
   - Test content layout adapts to viewport
   - Test button sizing on mobile

5. **Stage Components Tests**
   - Test grid columns adjust based on viewport
   - Test card padding on mobile
   - Test tab controls on mobile

### Visual Regression Testing

Visual tests will capture screenshots at different viewports to ensure layout integrity:

1. **Viewport Testing**
   - Mobile portrait (375px x 667px)
   - Mobile landscape (667px x 375px)
   - Tablet portrait (768px x 1024px)
   - Tablet landscape (1024px x 768px)
   - Desktop (1440px x 900px)

2. **Component States**
   - Sidebar open/closed on mobile
   - Messages with different content types
   - Settings page with all tabs
   - Loading states on mobile

### Manual Testing Checklist

1. **Touch Interaction Testing**
   - Verify all buttons are easily tappable
   - Test swipe gestures if implemented
   - Verify no accidental clicks on adjacent elements

2. **Keyboard Testing**
   - Test input focus on mobile keyboards
   - Verify viewport doesn't zoom on input focus
   - Test keyboard dismissal behavior

3. **Orientation Testing**
   - Test portrait to landscape transition
   - Verify layout adapts correctly
   - Test state preservation during rotation

4. **Cross-Browser Testing**
   - Test on Safari iOS
   - Test on Chrome Android
   - Test on Firefox mobile
   - Test on Samsung Internet

5. **Performance Testing**
   - Verify smooth animations on mobile
   - Test scroll performance with many messages
   - Verify no layout thrashing during resize

### Property-Based Testing

Property-based tests will use React Testing Library with viewport manipulation to verify universal properties:

**Testing Framework**: React Testing Library with Jest
**Viewport Manipulation**: Using `window.matchMedia` mocks and resize events

1. **Property Test: Touch Target Sizes**
   - Generate random sets of interactive elements
   - Render at mobile/tablet viewports
   - Verify all elements meet 44px minimum
   - **Validates: Property 1**

2. **Property Test: Message Layout**
   - Generate random message content
   - Render at mobile viewport
   - Verify single-column layout for all messages
   - **Validates: Property 2**

3. **Property Test: Functional Equivalence**
   - Generate random user interactions
   - Execute on both mobile and desktop viewports
   - Verify same outcomes achieved
   - **Validates: Property 3**

4. **Property Test: State Preservation**
   - Generate random component states
   - Trigger viewport resize across breakpoints
   - Verify state remains unchanged
   - **Validates: Property 4**

5. **Property Test: Dynamic Layout**
   - Generate random viewport sizes
   - Trigger resize events
   - Verify appropriate styles applied
   - **Validates: Property 5**

6. **Property Test: Button Positioning**
   - Generate random button configurations
   - Render at mobile viewport
   - Verify no overlapping bounding boxes
   - **Validates: Property 6**

7. **Property Test: Button Grouping**
   - Generate random sets of multiple buttons
   - Render at mobile viewport
   - Verify vertical stacking or horizontal grouping with spacing
   - **Validates: Property 7**

8. **Property Test: Code Block Scrolling**
   - Generate random code blocks with varying widths
   - Render in constrained containers
   - Verify horizontal scroll enabled for overflow
   - **Validates: Property 8**

Each property-based test will run a minimum of 100 iterations to ensure comprehensive coverage across different input combinations.

