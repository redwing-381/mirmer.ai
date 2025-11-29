# Implementation Plan

- [x] 1. Set up project structure and environment
  - Create backend/ directory with Python/FastAPI structure
  - Create frontend/ directory with React/Vite structure
  - Set up uv for Python package management
  - Create .env template file
  - Create data/conversations/ directory
  - _Requirements: 1.1, 1.3_

- [x] 2. Implement OpenRouter API client
  - [x] 2.1 Create backend/openrouter.py module
    - Implement async query_model() function using httpx
    - Add 120-second timeout handling
    - Parse OpenRouter response format (choices[0].message.content)
    - Return {'content': str} or None on failure
    - _Requirements: 3.2, 3.3, 9.3_

  - [x] 2.2 Implement parallel query function
    - Create query_models_parallel() using asyncio.gather()
    - Query all models concurrently
    - Return dictionary mapping model IDs to responses
    - Handle partial failures gracefully
    - _Requirements: 3.1, 3.4_

- [x] 3. Implement Stage 1: Individual responses
  - [x] 3.1 Create backend/council.py module
    - Implement stage1_collect_responses() function
    - Build messages list with user query
    - Call query_models_parallel() with COUNCIL_MODELS
    - Filter out None responses
    - Return list of {"model": str, "response": str}
    - _Requirements: 3.1, 3.2, 3.3, 3.5_

- [x] 4. Implement Stage 2: Peer rankings
  - [x] 4.1 Implement anonymization logic
    - Generate labels A, B, C using chr(65 + i)
    - Create label_to_model mapping dictionary
    - Build anonymized responses text for prompt
    - _Requirements: 4.1, 4.5_

  - [x] 4.2 Create ranking prompt
    - Build prompt with user query and anonymized responses
    - Add explicit formatting instructions
    - Include "FINAL RANKING:" marker
    - Add example format in prompt
    - _Requirements: 4.2_

  - [x] 4.3 Implement stage2_collect_rankings() function
    - Send ranking prompt to all council models in parallel
    - Parse each model's ranking using parse_ranking_from_text()
    - Return (stage2_results, label_to_model) tuple
    - _Requirements: 4.3, 4.4_

  - [x] 4.4 Implement parse_ranking_from_text() function
    - Use regex to find "FINAL RANKING:" section
    - Extract numbered list format (1. Response X)
    - Implement fallback: extract all "Response X" patterns
    - Return ordered list of response labels
    - _Requirements: 4.4_

  - [x] 4.5 Implement calculate_aggregate_rankings() function
    - Track positions for each model using defaultdict
    - Calculate average position (lower is better)
    - Sort by average rank
    - Return list with model, average_rank, rankings_count
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 5. Implement Stage 3: Final synthesis
  - [x] 5.1 Build chairman prompt
    - Format all Stage 1 responses with model names
    - Format all Stage 2 rankings with model names
    - Create comprehensive prompt for chairman
    - Emphasize synthesis over summarization
    - _Requirements: 6.1, 6.3_

  - [x] 5.2 Implement stage3_synthesize_final() function
    - Query CHAIRMAN_MODEL with full context
    - Handle None response with error message
    - Return {"model": str, "response": str}
    - _Requirements: 6.2, 6.4, 6.5_

- [x] 6. Implement JSON storage layer
  - [x] 6.1 Create backend/storage.py module
    - Implement ensure_data_dir() to create data/conversations/
    - Implement get_conversation_path() helper
    - _Requirements: 8.1_

  - [x] 6.2 Implement conversation CRUD functions
    - Create create_conversation() with UUID and timestamp
    - Create get_conversation() to load from JSON
    - Create list_conversations() to scan directory
    - Create save_conversation() to write JSON
    - _Requirements: 8.1, 8.2, 8.4_

  - [x] 6.3 Implement message functions
    - Create add_user_message() function
    - Create add_assistant_message() with stage1, stage2, stage3
    - Create update_conversation_title() function
    - _Requirements: 8.2, 8.3_

- [x] 7. Build FastAPI backend
  - [x] 7.1 Create backend/config.py
    - Load OPENROUTER_API_KEY from environment
    - Define COUNCIL_MODELS list (gpt-4-turbo, claude-3-sonnet, gemini-pro)
    - Define CHAIRMAN_MODEL
    - Define OPENROUTER_API_URL and DATA_DIR
    - _Requirements: 1.3, 3.1_

  - [x] 7.2 Create backend/main.py with FastAPI app
    - Initialize FastAPI app
    - Add CORS middleware for localhost:5173
    - Create Pydantic models for requests/responses
    - _Requirements: 1.1_

  - [x] 7.3 Implement conversation endpoints
    - POST /api/conversations - create new conversation
    - GET /api/conversations - list all conversations
    - GET /api/conversations/{id} - get specific conversation
    - _Requirements: 8.4, 8.5_

  - [x] 7.4 Implement streaming message endpoint
    - POST /api/conversations/{id}/message/stream
    - Create async event_generator() function
    - Emit stage1_start event
    - Call stage1_collect_responses() and emit stage1_complete
    - Emit stage2_start event
    - Call stage2_collect_rankings() and emit stage2_complete with metadata
    - Emit stage3_start event
    - Call stage3_synthesize_final() and emit stage3_complete
    - Emit complete event
    - Return StreamingResponse with text/event-stream
    - _Requirements: 2.3, 2.4, 3.1, 4.3, 6.2, 9.4_

  - [x] 7.5 Add error handling
    - Wrap event_generator in try-catch
    - Emit error events on exceptions
    - Log errors with timestamps
    - _Requirements: 9.1, 9.2, 9.5_

- [x] 8. Build React frontend foundation
  - [x] 8.1 Set up Vite + React project
    - Initialize Vite with React template
    - Install dependencies (react, react-dom, react-markdown)
    - Configure Tailwind CSS
    - Create basic App.jsx structure
    - _Requirements: 7.5_

  - [x] 8.2 Create frontend/src/api.js
    - Implement sendMessageStream() with ReadableStream API
    - Parse SSE events (data: {...})
    - Call onEvent callback for each event type
    - Implement createConversation(), listConversations(), getConversation()
    - _Requirements: 2.4_

  - [x] 8.3 Implement App.jsx state management
    - Create conversations state array
    - Create currentConversationId state
    - Create currentConversation state with messages
    - Implement loadConversations() function
    - Implement handleSendMessage() with optimistic updates
    - _Requirements: 8.4, 8.5_

- [x] 9. Build Stage display components
  - [x] 9.1 Create frontend/src/components/Stage1.jsx
    - Build tabbed interface with useState for activeTab
    - Map over responses to create tab buttons
    - Display model name (split by '/' and take [1])
    - Render response with ReactMarkdown
    - Add loading spinner when stage1 loading is true
    - _Requirements: 7.1, 7.5_

  - [x] 9.2 Create frontend/src/components/Stage2.jsx
    - Build tabbed interface for rankings
    - Implement deAnonymizeText() function to replace labels with model names
    - Display ranking text with de-anonymization
    - Show parsed_ranking list
    - Display aggregate rankings leaderboard at bottom
    - Show rank position, model name, average rank, vote count
    - Add loading spinner when stage2 loading is true
    - _Requirements: 7.2, 7.3, 7.5_

  - [x] 9.3 Create frontend/src/components/Stage3.jsx
    - Display chairman model name
    - Render final response with ReactMarkdown
    - Add prominent styling (border, padding)
    - Add loading spinner when stage3 loading is true
    - _Requirements: 7.4, 7.5_

- [x] 10. Build conversation management UI
  - [x] 10.1 Create frontend/src/components/Sidebar.jsx
    - Display list of conversations
    - Show title and created_at for each
    - Add "New Conversation" button
    - Highlight active conversation
    - Implement conversation selection onClick
    - _Requirements: 8.4, 8.5_

  - [x] 10.2 Create frontend/src/components/ChatInterface.jsx
    - Display messages list (user and assistant)
    - Render Stage1, Stage2, Stage3 components for assistant messages
    - Add message input textarea
    - Add submit button
    - Implement Enter key to send (Shift+Enter for newline)
    - Show loading indicator during processing
    - _Requirements: 2.1, 2.2, 2.4_

  - [x] 10.3 Implement title generation
    - Create generate_conversation_title() function in council.py
    - Query a fast model with "Generate a short title for: {query}"
    - Run in parallel with stages using asyncio.create_task()
    - Emit title_complete event
    - Update conversation title in storage
    - _Requirements: 8.3_

- [x] 11. Add styling and polish
  - [x] 11.1 Style Stage components
    - Add CSS for tabs (active state, hover effects)
    - Style markdown content (code blocks, lists, headings)
    - Add loading spinner animations
    - Style aggregate rankings leaderboard
    - Make responsive for mobile
    - _Requirements: 7.5_

  - [x] 11.2 Style chat interface
    - Style message bubbles (user vs assistant)
    - Add smooth transitions between stages
    - Style input textarea and button
    - Add loading indicators
    - Create responsive layout
    - _Requirements: 2.4_

  - [x] 11.3 Style sidebar
    - Style conversation list items
    - Add hover effects
    - Highlight active conversation
    - Style "New Conversation" button
    - Make collapsible on mobile
    - _Requirements: 8.4_

- [x] 12. Add error handling
  - [x] 12.1 Implement frontend error handling
    - Display error messages from SSE error events
    - Add error boundaries for React components
    - Implement retry logic for failed API calls
    - Rollback optimistic updates on error
    - _Requirements: 9.2, 9.4_

  - [x] 12.2 Add input validation
    - Validate query length (10-2000 characters)
    - Show validation errors in UI
    - Disable submit button when invalid
    - _Requirements: 2.2_

- [ ] 13. Integration testing
  - [ ] 13.1 Test complete flow
    - Test with real OpenRouter API key
    - Verify all three stages complete successfully
    - Check conversation is saved correctly
    - Test with various query types
    - _Requirements: All_

  - [ ] 13.2 Test error scenarios
    - Test with invalid API key
    - Test with network failures
    - Test with timeout scenarios
    - Verify graceful degradation
    - _Requirements: 9.1, 9.2, 9.3_

- [x] 14. Create deployment artifacts
  - [x] 14.1 Create start script
    - Create start.sh to run backend and frontend
    - Add instructions for setting OPENROUTER_API_KEY
    - Document port numbers (8001 for backend, 5173 for frontend)
    - _Requirements: All_

  - [x] 14.2 Write documentation
    - Create README with setup instructions
    - Document environment variables
    - Add troubleshooting section
    - Document API endpoints
    - _Requirements: All_

