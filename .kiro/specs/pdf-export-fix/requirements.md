# Requirements Document

## Introduction

The PDF export feature currently fails in production with a 500 internal server error due to WeasyPrint system dependency issues on Railway. This feature needs to be reimplemented using a client-side approach that is more reliable and platform-independent.

## Glossary

- **Client-Side PDF Generation**: PDF generation that occurs in the user's browser rather than on the server
- **Print API**: Browser's native print functionality that can generate PDFs
- **Export Service**: Backend service responsible for generating conversation exports

## Requirements

### Requirement 1

**User Story:** As a user, I want to export my conversations to PDF format, so that I can save and share them offline.

#### Acceptance Criteria

1. WHEN a user clicks the PDF export button THEN the system SHALL generate a PDF of the conversation without server-side dependencies
2. WHEN PDF generation is triggered THEN the system SHALL format the conversation with all three stages (individual responses, peer rankings, chairman synthesis)
3. WHEN the PDF is generated THEN the system SHALL include conversation metadata (title, date, ID)
4. WHEN PDF generation completes THEN the system SHALL automatically download the file to the user's device
5. WHEN PDF generation fails THEN the system SHALL display a clear error message to the user

### Requirement 2

**User Story:** As a developer, I want the PDF export to work reliably across all deployment platforms, so that users have a consistent experience.

#### Acceptance Criteria

1. WHEN the application is deployed to Railway THEN the PDF export SHALL function without requiring system-level dependencies
2. WHEN the PDF export is triggered THEN the system SHALL not cause server errors or crashes
3. WHEN the backend receives an export request THEN the system SHALL handle it gracefully regardless of available dependencies
4. WHEN WeasyPrint is not available THEN the system SHALL fall back to client-side generation

### Requirement 3

**User Story:** As a user, I want the exported PDF to be well-formatted and readable, so that I can easily review the conversation content.

#### Acceptance Criteria

1. WHEN the PDF is generated THEN the system SHALL apply consistent styling and formatting
2. WHEN displaying messages THEN the system SHALL clearly distinguish between user and assistant messages
3. WHEN displaying assistant responses THEN the system SHALL organize content by stage with clear headings
4. WHEN the PDF contains long content THEN the system SHALL handle page breaks appropriately
5. WHEN the PDF is viewed THEN the system SHALL use readable fonts and appropriate spacing
