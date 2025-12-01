# Design Document

## Overview

This document outlines the design for fixing the PDF export functionality in Mirmer AI. The current implementation has the correct template and export service code to render all three stages of the council process, but users are reporting that only Stage 1 (individual responses) appear in the exported PDF. This design identifies the root cause and provides a solution to ensure complete conversation data is included in all export formats.

## Architecture

The export functionality follows this flow:

```
User clicks Export → Frontend calls API → Backend retrieves conversation → 
Export Service generates file → File returned to user
```

### Current Components

1. **Frontend (ExportMenu.jsx)**: Provides UI for export format selection
2. **Backend API (main.py)**: Export endpoints for each format
3. **Storage Layer (storage_postgres.py / storage_json.py)**: Retrieves conversation data
4. **Export Service (export_service.py)**: Generates formatted output
5. **PDF Template (conversation_pdf.html)**: Jinja2 template for PDF rendering

## Root Cause Analysis

After reviewing the code, the implementation appears correct at all layers:

1. **Storage Layer** (`storage_postgres.py` lines 85-95): Correctly retrieves all stage data
   ```python
   messages.append({
       'role': 'assistant',
       'stage1': msg.stage1_data or [],
       'stage2': msg.stage2_data or [],
       'stage3': msg.stage3_data or {},
       'metadata': msg.message_metadata or {}
   })
   ```

2. **Export Service** (`export_service.py`): Correctly passes data to template
3. **PDF Template** (`conversation_pdf.html`): Correctly renders all three stages with conditional blocks

### Potential Issues

The most likely causes are:

1. **Data Not Being Saved**: Stage 2 and Stage 3 data may not be persisted to the database during the council process
2. **Timing Issue**: Export may be triggered before all stages complete
3. **Data Structure Mismatch**: The data structure saved may not match what the template expects
4. **Empty Data**: Stage data exists but contains empty arrays/objects

## Components and Interfaces

### 1. Council Process Data Flow

The council process should save data at each stage:

```python
# Stage 1: Individual responses
stage1_data = [
    {"model": "gpt-4", "response": "..."},
    {"model": "claude-3", "response": "..."}
]

# Stage 2: Peer rankings
stage2_data = [
    {
        "model": "gpt-4",
        "rankings": [
            {"label": "Best", "reasoning": "..."},
            {"label": "Good", "reasoning": "..."}
        ]
    }
]

# Stage 3: Chairman synthesis
stage3_data = {
    "final_answer": "...",
    "model": "gpt-4"
}
```

### 2. Storage Interface

The storage layer must persist all three stages:

```python
def add_message(conversation_id: str, role: str, user_id: str, **kwargs) -> bool:
    """
    Add message with stage data.
    
    For assistant messages:
    - stage1: List of individual responses
    - stage2: List of peer rankings
    - stage3: Dict with final synthesis
    """
```

### 3. Export Service Interface

```python
@staticmethod
def export_to_pdf(conversation: Dict[str, Any]) -> bytes:
    """
    Generate PDF with validation.
    
    Should verify:
    - All messages have expected structure
    - Assistant messages contain stage data
    - Log warnings for missing data
    """
```

## Data Models

### Conversation Structure

```python
{
    "id": "uuid",
    "user_id": "firebase_uid",
    "title": "Conversation Title",
    "created_at": "2024-01-01T00:00:00",
    "messages": [
        {
            "role": "user",
            "content": "User question"
        },
        {
            "role": "assistant",
            "stage1": [...],  # Must be present
            "stage2": [...],  # Must be present
            "stage3": {...},  # Must be present
            "metadata": {}
        }
    ]
}
```

### Message Model (Database)

```python
class Message(Base):
    id: int
    conversation_id: str
    role: str  # 'user' or 'assistant'
    content: str  # For user messages
    stage1_data: JSON  # For assistant messages
    stage2_data: JSON  # For assistant messages
    stage3_data: JSON  # For assistant messages
    message_metadata: JSON
    created_at: datetime
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Complete Stage Data Persistence

*For any* assistant message saved to the database, all three stage fields (stage1_data, stage2_data, stage3_data) should contain non-null values after the council process completes.

**Validates: Requirements 1.1, 1.2, 1.3, 2.2**

### Property 2: Export Data Completeness

*For any* conversation exported to PDF, if the conversation contains assistant messages with stage data in the database, then the exported PDF should contain all three stages rendered in the document.

**Validates: Requirements 1.1, 1.2, 1.3, 3.3**

### Property 3: Format Consistency

*For any* conversation, exporting to Markdown, PDF, and JSON should produce outputs that contain equivalent stage data (same number of stages, same models, same content).

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

### Property 4: Data Retrieval Integrity

*For any* conversation ID and user ID, calling `storage.get_conversation()` should return a dictionary where assistant messages contain stage1, stage2, and stage3 keys matching the database values.

**Validates: Requirements 2.1, 2.2, 2.3**

### Property 5: Template Rendering Completeness

*For any* conversation with complete stage data, rendering the PDF template should produce HTML that contains sections for Stage 1, Stage 2, and Stage 3 with visible content.

**Validates: Requirements 1.4, 4.1, 4.2, 4.3, 4.4**

## Error Handling

### 1. Missing Stage Data

```python
def validate_conversation_data(conversation: Dict[str, Any]) -> List[str]:
    """
    Validate conversation has complete data.
    
    Returns:
        List of warning messages for missing data
    """
    warnings = []
    
    for i, msg in enumerate(conversation.get('messages', [])):
        if msg.get('role') == 'assistant':
            if not msg.get('stage1'):
                warnings.append(f"Message {i}: Missing Stage 1 data")
            if not msg.get('stage2'):
                warnings.append(f"Message {i}: Missing Stage 2 data")
            if not msg.get('stage3'):
                warnings.append(f"Message {i}: Missing Stage 3 data")
    
    return warnings
```

### 2. Export Failure Handling

- Log detailed error messages with conversation ID
- Return user-friendly error messages
- Provide partial export if some data is available
- Include warning in PDF if data is incomplete

### 3. Database Query Errors

- Catch and log SQLAlchemy exceptions
- Return None for not found conversations
- Validate user ownership before export

## Testing Strategy

### Unit Tests

1. **Test Storage Layer**
   - Verify `get_conversation()` returns all stage data
   - Test with conversations that have complete stage data
   - Test with conversations missing some stages

2. **Test Export Service**
   - Verify Markdown export includes all stages
   - Verify JSON export includes all stages
   - Verify PDF generation with complete data
   - Test error handling for missing data

3. **Test Data Validation**
   - Verify validation function detects missing stages
   - Test warning message generation
   - Test with various incomplete data scenarios

### Property-Based Tests

We will use **Hypothesis** (Python's property-based testing library) for testing universal properties.

#### Property Test 1: Stage Data Round-Trip

**Property 1: Complete Stage Data Persistence**

```python
from hypothesis import given, strategies as st
import hypothesis.strategies as st

@given(
    stage1=st.lists(st.fixed_dictionaries({
        'model': st.text(min_size=1),
        'response': st.text(min_size=1)
    }), min_size=1),
    stage2=st.lists(st.fixed_dictionaries({
        'model': st.text(min_size=1),
        'rankings': st.lists(st.fixed_dictionaries({
            'label': st.text(min_size=1),
            'reasoning': st.text(min_size=1)
        }), min_size=1)
    }), min_size=1),
    stage3=st.fixed_dictionaries({
        'final_answer': st.text(min_size=1),
        'model': st.text(min_size=1)
    })
)
def test_stage_data_persistence(stage1, stage2, stage3):
    """
    Property: For any valid stage data, saving and retrieving a message
    should preserve all three stages.
    
    Validates: Requirements 2.2
    """
    # Create conversation and add assistant message
    conv_id = create_test_conversation()
    add_message(conv_id, 'assistant', stage1=stage1, stage2=stage2, stage3=stage3)
    
    # Retrieve conversation
    conversation = get_conversation(conv_id)
    
    # Verify all stages are present
    assert len(conversation['messages']) > 0
    msg = conversation['messages'][-1]
    assert msg['stage1'] == stage1
    assert msg['stage2'] == stage2
    assert msg['stage3'] == stage3
```

#### Property Test 2: Export Format Consistency

**Property 3: Format Consistency**

```python
@given(
    conversation=st.fixed_dictionaries({
        'id': st.uuids().map(str),
        'title': st.text(min_size=1, max_size=100),
        'messages': st.lists(
            st.one_of(
                # User message
                st.fixed_dictionaries({
                    'role': st.just('user'),
                    'content': st.text(min_size=1)
                }),
                # Assistant message
                st.fixed_dictionaries({
                    'role': st.just('assistant'),
                    'stage1': st.lists(st.fixed_dictionaries({
                        'model': st.text(min_size=1),
                        'response': st.text(min_size=1)
                    }), min_size=1),
                    'stage2': st.lists(st.fixed_dictionaries({
                        'model': st.text(min_size=1),
                        'rankings': st.lists(st.fixed_dictionaries({
                            'label': st.text(min_size=1),
                            'reasoning': st.text(min_size=1)
                        }), min_size=1)
                    }), min_size=1),
                    'stage3': st.fixed_dictionaries({
                        'final_answer': st.text(min_size=1)
                    })
                })
            ),
            min_size=1
        )
    })
)
def test_export_format_consistency(conversation):
    """
    Property: For any conversation, all export formats should contain
    the same stage data.
    
    Validates: Requirements 3.1, 3.2, 3.3, 3.4
    """
    # Export to all formats
    markdown = ExportService.export_to_markdown(conversation)
    json_str = ExportService.export_to_json(conversation)
    pdf_bytes = ExportService.export_to_pdf(conversation)
    
    # Parse JSON export
    json_data = json.loads(json_str)
    
    # Verify JSON contains all messages
    assert len(json_data['messages']) == len(conversation['messages'])
    
    # For each assistant message, verify all stages in all formats
    for msg in conversation['messages']:
        if msg['role'] == 'assistant':
            # Check Markdown contains stage headers
            assert 'Stage 1: Individual Model Responses' in markdown
            assert 'Stage 2: Peer Rankings' in markdown
            assert 'Stage 3: Chairman Synthesis' in markdown
            
            # Check JSON contains stage data
            assert any(m.get('stage1') for m in json_data['messages'])
            assert any(m.get('stage2') for m in json_data['messages'])
            assert any(m.get('stage3') for m in json_data['messages'])
            
            # Check PDF was generated (non-empty)
            assert len(pdf_bytes) > 0
```

#### Property Test 3: Data Validation Accuracy

**Property 4: Data Retrieval Integrity**

```python
@given(
    has_stage1=st.booleans(),
    has_stage2=st.booleans(),
    has_stage3=st.booleans()
)
def test_validation_detects_missing_stages(has_stage1, has_stage2, has_stage3):
    """
    Property: For any combination of present/missing stages, the validation
    function should correctly identify which stages are missing.
    
    Validates: Requirements 2.3, 2.4
    """
    # Create message with conditional stages
    message = {'role': 'assistant'}
    if has_stage1:
        message['stage1'] = [{'model': 'test', 'response': 'test'}]
    if has_stage2:
        message['stage2'] = [{'model': 'test', 'rankings': []}]
    if has_stage3:
        message['stage3'] = {'final_answer': 'test'}
    
    conversation = {
        'id': 'test',
        'messages': [message]
    }
    
    # Validate
    warnings = validate_conversation_data(conversation)
    
    # Check warnings match missing stages
    if not has_stage1:
        assert any('Stage 1' in w for w in warnings)
    if not has_stage2:
        assert any('Stage 2' in w for w in warnings)
    if not has_stage3:
        assert any('Stage 3' in w for w in warnings)
    
    # If all stages present, no warnings
    if has_stage1 and has_stage2 and has_stage3:
        assert len(warnings) == 0
```

### Integration Tests

1. **End-to-End Export Test**
   - Create conversation with council process
   - Wait for all stages to complete
   - Export to PDF
   - Verify PDF contains all three stages

2. **Database Integration Test**
   - Save message with all stages
   - Retrieve from database
   - Verify data integrity
   - Export and verify content

### Manual Testing

1. Create a new conversation
2. Send a message and wait for full council process
3. Export to PDF
4. Open PDF and verify:
   - Stage 1 shows all model responses
   - Stage 2 shows all peer rankings
   - Stage 3 shows chairman synthesis
5. Compare with Markdown export for consistency

## Implementation Plan

### Phase 1: Diagnosis (Investigation)

1. Add detailed logging to council process
2. Log when each stage data is saved
3. Add logging to export endpoint
4. Log conversation data structure before export
5. Verify database contains stage data

### Phase 2: Fix Data Persistence (If Needed)

1. Review `council.py` to ensure all stages are saved
2. Add validation after each stage save
3. Ensure SSE streaming doesn't skip database saves
4. Add transaction handling for message saves

### Phase 3: Add Data Validation

1. Implement `validate_conversation_data()` function
2. Add validation before export
3. Log warnings for missing data
4. Return user-friendly error messages

### Phase 4: Improve Export Service

1. Add data validation in export service
2. Handle missing stages gracefully
3. Add warning messages in PDF for incomplete data
4. Improve error messages

### Phase 5: Testing

1. Write unit tests for validation
2. Write property-based tests
3. Test with real conversations
4. Verify all export formats

### Phase 6: Documentation

1. Update API documentation
2. Add troubleshooting guide
3. Document expected data structure
4. Add examples of complete exports

## Deployment Considerations

1. **Database Migration**: No schema changes needed
2. **Backward Compatibility**: Fix should work with existing data
3. **Monitoring**: Add metrics for export success/failure rates
4. **Logging**: Enhanced logging for debugging
5. **Testing**: Comprehensive test coverage before deployment

## Success Criteria

1. All three stages appear in PDF exports
2. Export formats (Markdown, PDF, JSON) contain equivalent data
3. Clear error messages when data is incomplete
4. Validation catches missing stage data
5. Property-based tests pass with 100+ iterations
6. Manual testing confirms complete exports

