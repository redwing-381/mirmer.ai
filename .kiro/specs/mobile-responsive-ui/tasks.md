# Implementation Plan

- [x] 1. Add mobile hamburger menu and responsive header to AppPage
  - Add hamburger menu button that appears on mobile (< 768px)
  - Make header stack vertically on mobile with user info and logout
  - Add state management for mobile menu toggle
  - Implement responsive classes for header layout (flex-col md:flex-row)
  - _Requirements: 1.5_

- [x] 2. Implement mobile overlay mode for Sidebar component
  - Add mobile overlay mode with full-screen display
  - Implement backdrop that closes sidebar when clicked
  - Add slide-in animation for mobile sidebar
  - Update toggle button positioning for mobile
  - Add close button visible only on mobile
  - Adjust z-index for proper layering (sidebar: z-50, backdrop: z-40)
  - _Requirements: 1.1, 1.2_

- [x] 3. Make ChatInterface responsive for mobile devices
  - Reduce padding on mobile (p-2 md:p-4)
  - Adjust message container max-width for mobile
  - Make input area stack vertically on very small screens
  - Adjust textarea rows for mobile (rows="2" on mobile, rows="3" on desktop)
  - Update export button positioning for mobile (bottom-16 md:bottom-24)
  - _Requirements: 1.3, 1.4_

- [x] 4. Update Stage components (Stage1, Stage2, Stage3) for mobile layout
  - Implement responsive grid (grid-cols-1 md:grid-cols-2 lg:grid-cols-3)
  - Reduce card padding on mobile (p-4 md:p-6)
  - Make tabs scrollable horizontally on mobile if needed
  - Ensure code blocks have horizontal scroll on overflow
  - Adjust font sizes for mobile readability
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 5. Transform SettingsPage navigation for mobile
  - Convert sidebar navigation to horizontal tabs on mobile
  - Implement responsive tab bar at top for mobile (< 768px)
  - Keep sidebar navigation for tablet and desktop (>= 768px)
  - Update tab button styling for mobile (full-width, stacked)
  - Adjust content area to full width on mobile
  - _Requirements: 2.1_

- [x] 6. Make SettingsPage content responsive
  - Stack usage statistics vertically on mobile
  - Make subscription cards full-width on mobile
  - Adjust progress bar sizing for mobile
  - Make buttons full-width on mobile (w-full md:w-auto)
  - Update profile section for vertical layout on mobile
  - Ensure minimum touch target sizes (min-h-[44px])
  - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [x] 7. Implement tablet-specific optimizations
  - Add tablet breakpoint styles (md:) for medium screens
  - Adjust sidebar width for tablet (w-60 md:w-64 lg:w-80)
  - Optimize message widths for tablet readability
  - Implement two-column layout for settings on tablet where appropriate
  - Test and adjust spacing for tablet viewport
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 8. Add viewport meta tag and prevent zoom on input focus
  - Ensure viewport meta tag is properly configured in index.html
  - Add font-size: 16px minimum to inputs to prevent iOS zoom
  - Test input focus behavior on mobile devices
  - _Requirements: 1.4_

- [x] 9. Update ExportMenu component for mobile
  - Reposition export menu for mobile (fixed bottom-16 right-4)
  - Make export options menu mobile-friendly
  - Ensure dropdown doesn't overflow viewport on mobile
  - Add touch-friendly spacing between options
  - _Requirements: 5.1, 5.2_

- [x] 10. Add responsive utility classes and ensure touch targets
  - Audit all interactive elements for minimum 44px touch targets
  - Add responsive padding/margin utilities throughout
  - Ensure all buttons meet accessibility guidelines
  - Add hover states that work on touch devices
  - _Requirements: 2.5, 3.5, 5.5_

- [ ]* 11. Write unit tests for responsive components
  - Write tests for Sidebar mobile overlay mode
  - Write tests for AppPage hamburger menu
  - Write tests for ChatInterface mobile layout
  - Write tests for SettingsPage tab navigation
  - Write tests for Stage components responsive grid
  - _Requirements: All_

- [ ]* 12. Write property-based tests for responsive behavior
  - **Property 1: Touch target minimum size**
  - **Validates: Requirements 2.5, 3.5, 5.5**

- [ ]* 12.1 Write property test for touch target sizes
  - **Property 1: Touch target minimum size**
  - **Validates: Requirements 2.5, 3.5, 5.5**

- [ ]* 12.2 Write property test for message layout
  - **Property 2: Single column message layout on mobile**
  - **Validates: Requirements 1.3**

- [ ]* 12.3 Write property test for functional equivalence
  - **Property 3: Functional equivalence across devices**
  - **Validates: Requirements 4.1**

- [ ]* 12.4 Write property test for state preservation
  - **Property 4: State preservation during responsive transitions**
  - **Validates: Requirements 4.2**

- [ ]* 12.5 Write property test for dynamic layout
  - **Property 5: Dynamic layout adjustment**
  - **Validates: Requirements 4.3**

- [ ]* 12.6 Write property test for button positioning
  - **Property 6: Action button positioning**
  - **Validates: Requirements 5.1**

- [ ]* 12.7 Write property test for button grouping
  - **Property 7: Button grouping on mobile**
  - **Validates: Requirements 5.3**

- [ ]* 12.8 Write property test for code block scrolling
  - **Property 8: Code block horizontal scrolling**
  - **Validates: Requirements 6.5**

- [ ] 13. Manual testing and refinement
  - Test on actual mobile devices (iOS and Android)
  - Test orientation changes
  - Verify touch interactions feel natural
  - Test on different screen sizes (small phones to tablets)
  - Verify performance on mobile devices
  - _Requirements: All_

- [ ] 14. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
