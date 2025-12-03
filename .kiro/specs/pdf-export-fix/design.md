# Design Document: Client-Side PDF Export

## Overview

This design replaces the server-side WeasyPrint PDF generation with a client-side approach using the browser's native print functionality. This eliminates system dependency issues and provides a more reliable, platform-independent solution.

## Architecture

### Current Architecture (Problematic)
```
User clicks PDF → Frontend calls /api/export/pdf → Backend uses WeasyPrint → Returns PDF bytes
                                                    ↓
                                            Requires system libs (pango, cairo, etc.)
                                            Fails on Railway
```

### New Architecture (Reliable)
```
User clicks PDF → Frontend renders print-optimized view → Browser print API → PDF download
                                                          ↓
                                                   No server dependencies
                                                   Works everywhere
```

## Components and Interfaces

### 1. Frontend: ConversationPrintView Component

A new React component that renders a print-optimized version of the conversation:

```typescript
interface ConversationPrintViewProps {
  conversation: Conversation;
  onClose: () => void;
}

// Component renders in a hidden iframe or modal
// Styled specifically for print media
// Triggers browser print dialog automatically
```

### 2. Frontend: Print Styles

CSS media queries for print-specific formatting:

```css
@media print {
  /* Hide navigation, buttons, etc. */
  /* Optimize typography for print */
  /* Handle page breaks */
  /* Ensure proper margins */
}
```

### 3. Backend: Export Endpoint Modification

Update the PDF export endpoint to return an error or redirect to client-side generation:

```python
@app.get("/api/conversations/{conversation_id}/export/pdf")
async def export_pdf(conversation_id: str, user_id: str):
    # Option 1: Return 501 Not Implemented with message
    # Option 2: Return conversation data for client-side rendering
    # Option 3: Keep WeasyPrint as optional fallback
```

## Data Models

No changes to existing data models. The conversation structure remains the same:

```python
{
  "id": str,
  "title": str,
  "created_at": str,
  "messages": [
    {
      "role": "user" | "assistant",
      "content": str,
      "stage1": [...],  # For assistant messages
      "stage2": [...],
      "stage3": {...}
    }
  ]
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Acceptance Criteria Testing Prework

1.1 WHEN a user clicks the PDF export button THEN the system SHALL generate a PDF of the conversation without server-side dependencies
  Thoughts: This is testing that PDF generation works across all conversations without requiring server-side libraries. We can test this by generating random conversations and ensuring the client-side generation succeeds.
  Testable: yes - property

1.2 WHEN PDF generation is triggered THEN the system SHALL format the conversation with all three stages
  Thoughts: This is testing that the formatted output contains all required sections. We can generate random conversations and verify the rendered HTML contains stage1, stage2, and stage3 sections.
  Testable: yes - property

1.3 WHEN the PDF is generated THEN the system SHALL include conversation metadata
  Thoughts: This is testing that metadata fields are present in the output. We can generate random conversations and verify title, date, and ID appear in the rendered content.
  Testable: yes - property

1.4 WHEN PDF generation completes THEN the system SHALL automatically download the file
  Thoughts: This is a UI interaction that triggers browser download. We can test that the print function is called.
  Testable: yes - example

1.5 WHEN PDF generation fails THEN the system SHALL display a clear error message
  Thoughts: This is testing error handling for specific failure cases.
  Testable: yes - example

2.1 WHEN the application is deployed to Railway THEN the PDF export SHALL function without requiring system-level dependencies
  Thoughts: This is about deployment environment, not a functional property we can test in code.
  Testable: no

2.2 WHEN the PDF export is triggered THEN the system SHALL not cause server errors or crashes
  Thoughts: This is testing that the endpoint handles requests gracefully. We can test that the endpoint returns appropriate responses.
  Testable: yes - property

2.3 WHEN the backend receives an export request THEN the system SHALL handle it gracefully regardless of available dependencies
  Thoughts: This is testing error handling when WeasyPrint is not available.
  Testable: yes - example

2.4 WHEN WeasyPrint is not available THEN the system SHALL fall back to client-side generation
  Thoughts: This is testing the fallback behavior, which is a specific scenario.
  Testable: yes - example

3.1 WHEN the PDF is generated THEN the system SHALL apply consistent styling and formatting
  Thoughts: This is about visual consistency, which is subjective and not easily testable programmatically.
  Testable: no

3.2 WHEN displaying messages THEN the system SHALL clearly distinguish between user and assistant messages
  Thoughts: This is testing that the rendered HTML contains distinguishing markers. We can verify CSS classes or data attributes are present.
  Testable: yes - property

3.3 WHEN displaying assistant responses THEN the system SHALL organize content by stage with clear headings
  Thoughts: This is testing that stage headings are present in the rendered output.
  Testable: yes - property

3.4 WHEN the PDF contains long content THEN the system SHALL handle page breaks appropriately
  Thoughts: This is about CSS page-break properties being applied, which we can verify are present in the styles.
  Testable: yes - example

3.5 WHEN the PDF is viewed THEN the system SHALL use readable fonts and appropriate spacing
  Thoughts: This is subjective visual design that can't be programmatically tested.
  Testable: no

### Property Reflection

After reviewing the properties:
- Properties 1.2 and 1.3 both test that rendered content contains required elements - these can be combined
- Properties 3.2 and 3.3 both test HTML structure and can be combined into one comprehensive property
- Property 2.2 is redundant with 2.3 - both test graceful error handling

Consolidated properties:
- Property 1: Client-side PDF generation works for all conversations
- Property 2: Rendered content includes all required sections and metadata
- Property 3: Backend handles export requests gracefully

### Correctness Properties

Property 1: Client-side generation succeeds
*For any* valid conversation with messages, triggering client-side PDF generation should successfully render the print view without errors
**Validates: Requirements 1.1**

Property 2: Complete content rendering
*For any* conversation, the rendered print view should contain all message content, stage sections (stage1, stage2, stage3), and metadata (title, date, ID)
**Validates: Requirements 1.2, 1.3, 3.2, 3.3**

Property 3: Graceful backend handling
*For any* export request to the backend, the endpoint should return a valid response (either success or appropriate error) without causing server crashes
**Validates: Requirements 2.2, 2.3**

## Error Handling

### Client-Side Errors

1. **Browser doesn't support print API**: Show error message with fallback instructions
2. **Conversation data incomplete**: Display warning and proceed with available data
3. **Rendering fails**: Catch errors and show user-friendly message

### Backend Errors

1. **WeasyPrint not available**: Return 501 with message directing to client-side export
2. **Conversation not found**: Return 404 with clear error message
3. **Authentication failure**: Return 401 with authentication error

## Testing Strategy

### Unit Tests

- Test ConversationPrintView component renders correctly with sample data
- Test print styles are applied correctly
- Test error handling for missing data
- Test backend endpoint returns appropriate responses

### Property-Based Tests

We'll use a JavaScript property testing library (fast-check) for frontend tests:

- **Property 1**: Generate random conversations and verify print view renders without errors
- **Property 2**: Generate random conversations and verify all required sections appear in rendered HTML
- **Property 3**: Test backend endpoint with various inputs and verify no crashes

Each property-based test will run a minimum of 100 iterations. Tests will be tagged with:
`**Feature: pdf-export-fix, Property {number}: {property_text}**`

### Integration Tests

- Test full flow: click export → render view → trigger print
- Test with conversations of varying sizes
- Test with incomplete conversation data

## Implementation Approach

### Phase 1: Create Print View Component
1. Create `ConversationPrintView.jsx` component
2. Add print-specific CSS styles
3. Implement automatic print dialog trigger

### Phase 2: Update Export Button
1. Modify export button to use client-side generation
2. Remove server-side PDF endpoint call
3. Add loading states and error handling

### Phase 3: Backend Cleanup
1. Update PDF export endpoint to return appropriate response
2. Make WeasyPrint optional dependency
3. Update documentation

### Phase 4: Testing
1. Write unit tests for print view component
2. Write property-based tests for rendering
3. Test across different browsers
4. Verify works in production

## Migration Strategy

1. Deploy new client-side implementation
2. Keep backend endpoint but return "use client-side" message
3. Monitor for any issues
4. Eventually remove WeasyPrint dependency entirely

## Benefits of This Approach

1. **No system dependencies**: Works on any platform (Railway, Vercel, local)
2. **Better browser compatibility**: Uses native browser print functionality
3. **Faster**: No server round-trip for PDF generation
4. **More maintainable**: Less complex dependency chain
5. **Better print quality**: Browser's print engine is highly optimized
