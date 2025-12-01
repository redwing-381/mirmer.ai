# Implementation Plan

- [x] 1. Add diagnostic logging to identify root cause
  - Add detailed logging to council.py when saving stage data
  - Add logging to export endpoint showing conversation structure
  - Add logging to storage layer showing retrieved data
  - Create test script to verify database contains stage data
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 2. Implement data validation function
- [x] 2.1 Create validate_conversation_data function in export_service.py
  - Write function that checks for missing stage data
  - Return list of warning messages for missing stages
  - Handle edge cases (empty arrays, null values)
  - _Requirements: 2.3, 2.4_

- [ ]* 2.2 Write property test for validation function
  - **Property 4: Data Retrieval Integrity**
  - **Validates: Requirements 2.3, 2.4**

- [ ]* 2.3 Write unit tests for validation function
  - Test with complete conversation data
  - Test with missing Stage 1 data
  - Test with missing Stage 2 data
  - Test with missing Stage 3 data
  - Test with multiple missing stages
  - _Requirements: 2.3, 2.4_

- [x] 3. Fix council process data persistence (if needed)
- [x] 3.1 Review and fix council.py message saving
  - Verify add_message is called with all stage data
  - Ensure stage data is not lost during SSE streaming
  - Add validation after each stage save
  - Add error handling for save failures
  - _Requirements: 1.1, 1.2, 1.3, 2.2_

- [ ]* 3.2 Write property test for stage data persistence
  - **Property 1: Complete Stage Data Persistence**
  - **Validates: Requirements 1.1, 1.2, 1.3, 2.2**

- [ ]* 3.3 Write unit tests for message persistence
  - Test saving assistant message with all stages
  - Test retrieving message and verifying stages
  - Test with various stage data structures
  - _Requirements: 2.2_

- [x] 4. Enhance export service with validation
- [x] 4.1 Add validation to export_to_pdf function
  - Call validate_conversation_data before rendering
  - Log warnings for missing data
  - Add warning section to PDF if data incomplete
  - Improve error messages for users
  - _Requirements: 2.4, 5.3, 5.4_

- [x] 4.2 Add validation to export_to_markdown function
  - Call validate_conversation_data before rendering
  - Log warnings for missing data
  - Add warning comments in Markdown if data incomplete
  - _Requirements: 3.1, 5.4_

- [x] 4.3 Add validation to export_to_json function
  - Call validate_conversation_data before rendering
  - Log warnings for missing data
  - Include validation warnings in JSON metadata
  - _Requirements: 3.2, 5.4_

- [ ]* 4.4 Write property test for export format consistency
  - **Property 3: Format Consistency**
  - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**

- [ ]* 4.5 Write unit tests for export validation
  - Test PDF export with complete data
  - Test PDF export with missing stages
  - Test Markdown export with missing stages
  - Test JSON export with missing stages
  - Verify warning messages appear correctly
  - _Requirements: 2.4, 5.3, 5.4_

- [x] 5. Improve PDF template rendering
- [x] 5.1 Add conditional warnings in PDF template
  - Add warning section if stage1 is empty
  - Add warning section if stage2 is empty
  - Add warning section if stage3 is empty
  - Style warnings distinctly (yellow background)
  - _Requirements: 4.1, 5.4_

- [x] 5.2 Improve PDF styling for better readability
  - Ensure consistent spacing between stages
  - Improve page break handling for long content
  - Add visual separators between stages
  - Test with various content lengths
  - _Requirements: 1.4, 4.1, 4.2, 4.3, 4.4_

- [ ]* 5.3 Write unit tests for PDF template rendering
  - Test template with complete data
  - Test template with missing stages
  - Verify warning sections appear
  - Test with long content (page breaks)
  - _Requirements: 1.4, 4.1_

- [ ] 6. Update export API endpoints
- [ ] 6.1 Enhance error handling in export endpoints
  - Add try-catch for validation errors
  - Return 400 Bad Request for invalid data
  - Include validation warnings in response headers
  - Log all export attempts with status
  - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [ ] 6.2 Add export success/failure metrics
  - Log export format and success/failure
  - Log conversation ID and user ID
  - Log validation warnings count
  - Add timing metrics for performance monitoring
  - _Requirements: 5.5_

- [ ]* 6.3 Write integration tests for export endpoints
  - Test PDF export endpoint with complete data
  - Test PDF export endpoint with missing data
  - Test Markdown export endpoint
  - Test JSON export endpoint
  - Verify error responses
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 7. Frontend improvements for export feedback
- [ ] 7.1 Add loading indicator during export
  - Show spinner when export is in progress
  - Disable export button during generation
  - Add timeout for long-running exports
  - _Requirements: 5.1_

- [ ] 7.2 Improve export success/error messages
  - Show success toast with file name
  - Show error toast with specific error message
  - Add warning toast if data is incomplete
  - _Requirements: 5.2, 5.3, 5.4_

- [ ]* 7.3 Write unit tests for ExportMenu component
  - Test export button click handlers
  - Test loading state display
  - Test success message display
  - Test error message display
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 8. Checkpoint - Verify all exports work correctly
  - Ensure all tests pass, ask the user if questions arise.
  - Manually test PDF export with real conversation
  - Verify all three stages appear in PDF
  - Compare PDF with Markdown export for consistency
  - Test with conversations that have missing data
  - Verify warning messages appear correctly

- [ ] 9. Documentation and cleanup
- [ ] 9.1 Update API documentation
  - Document export endpoints
  - Document validation behavior
  - Document error responses
  - Add examples of complete exports

- [ ] 9.2 Add code comments and docstrings
  - Document validate_conversation_data function
  - Document export service methods
  - Document expected data structures
  - Add examples in docstrings

- [ ] 9.3 Create troubleshooting guide
  - Document common export issues
  - Explain validation warnings
  - Provide debugging steps
  - Add FAQ section

