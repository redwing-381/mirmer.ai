# Requirements Document

## Introduction

This document outlines the requirements for fixing the PDF export functionality in Mirmer AI. Currently, when users export conversations to PDF, only Stage 1 (individual model responses) are included in the export. The peer rankings (Stage 2) and chairman synthesis (Stage 3) are missing from the exported PDF, even though the template and export service code appear to support all three stages.

## Glossary

- **System**: The Mirmer AI web application (frontend and backend)
- **User**: An authenticated person using the Mirmer AI application
- **Conversation**: A chat session containing user messages and AI responses with three stages
- **Stage 1**: Individual model responses from multiple AI models
- **Stage 2**: Peer rankings where models evaluate each other's responses
- **Stage 3**: Chairman synthesis that combines insights into a final answer
- **Export**: The process of saving conversation data to an external format (PDF, Markdown, JSON)
- **PDF Export**: A formatted PDF document containing the complete conversation

## Requirements

### Requirement 1: Complete PDF Export Content

**User Story:** As a user, I want my PDF exports to include all three stages of the council process (individual responses, peer rankings, and chairman synthesis), so that I have a complete record of the AI consultation.

#### Acceptance Criteria

1. WHEN a user exports a conversation to PDF THEN the System SHALL include all Stage 1 individual model responses in the PDF
2. WHEN a user exports a conversation to PDF THEN the System SHALL include all Stage 2 peer rankings with reasoning in the PDF
3. WHEN a user exports a conversation to PDF THEN the System SHALL include the Stage 3 chairman synthesis in the PDF
4. WHEN the PDF is generated THEN the System SHALL preserve the visual hierarchy with clear section headings for each stage
5. WHEN the PDF contains long responses THEN the System SHALL handle page breaks appropriately without cutting off content

### Requirement 2: Data Integrity Verification

**User Story:** As a developer, I want to verify that conversation data is correctly retrieved and passed to the export service, so that all stages are available for rendering in the PDF.

#### Acceptance Criteria

1. WHEN the export endpoint receives a request THEN the System SHALL retrieve the complete conversation including all message stages
2. WHEN conversation data is loaded from storage THEN the System SHALL verify that stage1, stage2, and stage3 data are present for assistant messages
3. WHEN conversation data is missing any stage THEN the System SHALL log a warning indicating which stages are missing
4. WHEN the export service receives conversation data THEN the System SHALL validate that all expected fields are present before rendering
5. WHEN validation fails THEN the System SHALL return a descriptive error message to the user

### Requirement 3: Export Format Consistency

**User Story:** As a user, I want all export formats (Markdown, PDF, JSON) to contain the same complete conversation data, so that I can choose the format that best suits my needs without losing information.

#### Acceptance Criteria

1. WHEN a user exports to Markdown THEN the System SHALL include all three stages with proper formatting
2. WHEN a user exports to JSON THEN the System SHALL include the complete data structure with all stages
3. WHEN a user exports to PDF THEN the System SHALL include all three stages matching the Markdown content
4. WHEN comparing exports in different formats THEN the System SHALL contain equivalent information across all formats
5. WHEN any stage data is missing THEN the System SHALL handle it gracefully in all export formats

### Requirement 4: PDF Rendering Quality

**User Story:** As a user, I want my PDF exports to be well-formatted and readable, so that I can easily review and share the conversation content.

#### Acceptance Criteria

1. WHEN the PDF is generated THEN the System SHALL apply consistent styling to all three stages
2. WHEN Stage 1 responses are rendered THEN the System SHALL clearly label each model's response
3. WHEN Stage 2 rankings are rendered THEN the System SHALL display each model's rankings with reasoning
4. WHEN Stage 3 synthesis is rendered THEN the System SHALL highlight it as the final answer with distinct styling
5. WHEN the PDF contains code or special characters THEN the System SHALL preserve formatting and escape characters properly

### Requirement 5: Error Handling and User Feedback

**User Story:** As a user, I want clear feedback when export operations succeed or fail, so that I know whether my conversation was successfully exported.

#### Acceptance Criteria

1. WHEN an export request is initiated THEN the System SHALL display a loading indicator
2. WHEN an export succeeds THEN the System SHALL trigger the file download and show a success message
3. WHEN an export fails THEN the System SHALL display an error message explaining what went wrong
4. WHEN conversation data is incomplete THEN the System SHALL warn the user that some content may be missing
5. WHEN the export completes THEN the System SHALL log the operation with conversation ID and format for debugging

