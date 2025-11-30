# UI Improvements Implementation Tasks

- [x] 1. Fix usage tracking backend
  - Investigate and fix usage counter increment timing
  - Add detailed logging to track increment operations
  - Ensure database commits happen before stats queries
  - Test that counters update correctly after message send
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 1.1 Write property test for usage increment
  - **Property 5: Usage increment consistency**
  - **Validates: Requirements 6.1, 6.2, 6.4**

- [x] 2. Remove usage stats from conversation sidebar
  - Remove UsageStats component from Sidebar.jsx
  - Adjust sidebar layout to use freed space
  - Ensure Settings button remains visible and accessible
  - Test that conversation list has more space
  - _Requirements: 2.1, 2.2, 2.5_

- [x] 2.1 Write property test for usage stats removal
  - **Property 3: Usage stats removal**
  - **Validates: Requirements 2.1**

- [x] 3. Implement collapsible sidebar functionality
  - Add collapse state management in AppPage.jsx
  - Add toggle button to Sidebar.jsx
  - Implement smooth CSS transitions (300ms)
  - Add localStorage persistence for sidebar state
  - Ensure toggle button remains visible when collapsed
  - Test animation smoothness and state persistence
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 3.1 Write property test for sidebar state persistence
  - **Property 2: Sidebar state persistence**
  - **Validates: Requirements 4.5**

- [x] 3.2 Write property test for sidebar collapse animation
  - **Property 6: Sidebar collapse animation**
  - **Validates: Requirements 4.2**

- [x] 4. Enhance in-chat limit warning
  - Update ChatInterface.jsx limit warning styling
  - Make warning more prominent with yellow background
  - Add clear messaging for which limit was reached
  - Ensure input and send button are disabled when over limit
  - Test warning appears correctly for daily and monthly limits
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4.1 Write property test for limit warning visibility
  - **Property 4: Limit warning visibility**
  - **Validates: Requirements 3.1, 3.5**

- [x] 5. Create settings page sidebar navigation
  - Restructure SettingsPage.jsx with sidebar layout
  - Create tab navigation component with Usage, Subscription, Profile tabs
  - Implement tab switching logic
  - Add localStorage persistence for active tab
  - Style tabs with neobrutalism design
  - _Requirements: 1.1, 1.2, 5.1, 5.4, 5.5_

- [x] 5.1 Write property test for settings tab persistence
  - **Property 1: Settings tab persistence**
  - **Validates: Requirements 1.2**

- [x] 5.2 Write property test for settings content display
  - **Property 7: Settings content display**
  - **Validates: Requirements 1.2**

- [x] 6. Implement Usage tab content
  - Create detailed usage statistics display
  - Show daily and monthly progress bars
  - Display query counts and limits
  - Add visual indicators for usage levels
  - Style with neobrutalism design
  - _Requirements: 1.3, 5.1, 5.2_

- [x] 7. Implement Subscription tab content
  - Move current subscription display to tab
  - Show current plan with benefits
  - Display upgrade/cancel options
  - Maintain existing payment integration
  - Style with neobrutalism design
  - _Requirements: 1.4, 5.1, 5.2_

- [x] 8. Implement Profile tab content
  - Create profile information display
  - Show user name, email, and photo
  - Add account settings section
  - Move logout button to profile tab
  - Style with neobrutalism design
  - _Requirements: 1.5, 5.1, 5.2_

- [x] 9. Update frontend to refresh stats after message send
  - Listen for 'complete' SSE event in ChatInterface
  - Trigger stats refresh in AppPage after message completion
  - Maintain existing 500ms delay for consistency
  - Test that stats update correctly in UI
  - _Requirements: 6.4, 6.5_

- [x] 10. Add comprehensive error handling
  - Handle localStorage unavailability gracefully
  - Add error states for usage stats fetch failures
  - Implement retry logic for failed stats updates
  - Add user-friendly error messages
  - Test error scenarios
  - _Requirements: 2.3, 6.3_

- [x] 11. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Add accessibility improvements
  - Add ARIA labels to sidebar toggle and tabs
  - Ensure keyboard navigation works for all interactive elements
  - Test with screen readers
  - Verify color contrast meets WCAG AA standards
  - _Requirements: 5.5_

- [x] 13. Performance optimization
  - Use React.memo for settings tab content
  - Optimize sidebar animation with CSS transforms
  - Minimize localStorage access
  - Test performance with React DevTools
  - _Requirements: 4.2_

- [x] 14. Final integration testing
  - Test complete user flow: send message → stats update → UI reflects change
  - Test sidebar collapse → persist → reload → restore
  - Test settings tabs → switch → persist → reload → restore
  - Test limit warning → appears → blocks input
  - Verify all neobrutalism styling is consistent
  - _Requirements: All_
