# Implementation Plan

- [x] 1. Create print view component and styles
  - Create `ConversationPrintView.jsx` component that renders conversation in print-optimized format
  - Add print-specific CSS with `@media print` queries for proper formatting
  - Include all conversation metadata (title, date, ID) in the print view
  - Organize messages by stages with clear visual hierarchy
  - _Requirements: 1.2, 1.3, 3.2, 3.3_

- [ ]* 1.1 Write property test for complete content rendering
  - **Property 2: Complete content rendering**
  - **Validates: Requirements 1.2, 1.3, 3.2, 3.3**

- [x] 2. Implement client-side PDF generation trigger
  - Add function to open print view and trigger browser print dialog
  - Handle print dialog cancellation gracefully
  - Add loading state while preparing print view
  - Implement error handling for browser compatibility issues
  - _Requirements: 1.1, 1.4, 1.5_

- [ ]* 2.1 Write property test for client-side generation
  - **Property 1: Client-side generation succeeds**
  - **Validates: Requirements 1.1**

- [x] 3. Update export button to use client-side generation
  - Modify PDF export button click handler to use new client-side approach
  - Remove server-side API call for PDF generation
  - Add user feedback during PDF generation process
  - Ensure consistent behavior with other export formats (Markdown, JSON)
  - _Requirements: 1.1, 1.4_

- [ ]* 3.1 Write unit tests for export button integration
  - Test export button triggers print view correctly
  - Test error states are displayed properly
  - Test loading states work as expected
  - _Requirements: 1.4, 1.5_

- [x] 4. Update backend PDF endpoint
  - Modify `/api/conversations/{id}/export/pdf` endpoint to return appropriate response
  - Make WeasyPrint import optional with try/except
  - Return helpful error message directing users to client-side export
  - Ensure endpoint doesn't crash when WeasyPrint is unavailable
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ]* 4.1 Write property test for graceful backend handling
  - **Property 3: Graceful backend handling**
  - **Validates: Requirements 2.2, 2.3**

- [x] 5. Clean up dependencies and configuration
  - Make WeasyPrint optional in `requirements.txt`
  - Update `nixpacks.toml` to remove WeasyPrint system dependencies
  - Update documentation to reflect client-side PDF generation
  - Add comments explaining the client-side approach
  - _Requirements: 2.1_

- [x] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
