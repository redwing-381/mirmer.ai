# Implementation Plan

- [x] 1. Set up project structure and packaging
  - Create package directory structure (mirmer/, tests/, examples/)
  - Set up pyproject.toml with project metadata and dependencies
  - Configure build system with modern Python packaging (setuptools or hatchling)
  - Create __init__.py with public API exports
  - Add _version.py for version management
  - _Requirements: 1.1, 1.3, 1.4, 1.5_

- [x] 2. Implement core data models
  - [x] 2.1 Create Pydantic models for all data structures
    - Implement ModelResponse, ModelRanking, AggregateRanking dataclasses
    - Implement ChairmanSynthesis and CouncilResponse dataclasses
    - Implement CouncilUpdate for streaming events
    - Implement Message and Conversation dataclasses
    - Implement UsageStats dataclass
    - Add type hints and validation for all fields
    - _Requirements: 3.2, 4.1, 5.1, 5.2, 7.1, 7.2, 7.3_

- [ ]* 2.2 Write property test for response structure validation
  - **Property 4: Complete response structure**
  - **Validates: Requirements 3.2**

- [ ]* 2.3 Write property test for usage stats structure
  - **Property 12: Usage stats structure**
  - **Validates: Requirements 7.1, 7.2, 7.3**

- [x] 3. Implement exception hierarchy
  - [x] 3.1 Create custom exception classes
    - Implement MirmerError base exception
    - Implement AuthenticationError, RateLimitError, ValidationError
    - Implement NotFoundError, ConnectionError, APIError
    - Add helpful error messages and context attributes
    - _Requirements: 2.3, 2.5, 3.5, 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 3.2 Write property test for error response handling
  - **Property 6: Error response handling**
  - **Validates: Requirements 3.5**

- [ ]* 3.3 Write property test for API error mapping
  - **Property 16: API error mapping**
  - **Validates: Requirements 9.5**

- [x] 4. Implement synchronous Client class
  - [x] 4.1 Create Client class with initialization and configuration
    - Implement __init__ with api_key, base_url, timeout, max_retries parameters
    - Add API key resolution (parameter → environment variable → error)
    - Implement configuration validation
    - Set up httpx client with connection pooling
    - Implement context manager methods (__enter__, __exit__)
    - _Requirements: 2.1, 2.2, 2.3, 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ]* 4.2 Write property test for API key security
  - **Property 1: API key security in client representation**
  - **Validates: Requirements 2.1**

- [ ]* 4.3 Write property test for configuration validation
  - **Property 20: Configuration validation**
  - **Validates: Requirements 12.5**

- [x] 4.4 Implement query method
    - Build request with message content and optional conversation_id
    - Add x-user-id header with API key
    - Handle streaming response and collect all events
    - Parse complete response into CouncilResponse object
    - Implement error handling and exception mapping
    - _Requirements: 2.4, 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 4.5 Write property test for query initiates council process
  - **Property 3: Query initiates council process**
  - **Validates: Requirements 3.1**

- [ ]* 4.6 Write property test for API key header inclusion
  - **Property 2: API key header inclusion**
  - **Validates: Requirements 2.4**

- [ ]* 4.7 Write property test for conversation ID propagation
  - **Property 5: Conversation ID propagation**
  - **Validates: Requirements 3.3**

- [x] 4.8 Implement stream method
    - Build streaming request with SSE connection
    - Parse SSE events and yield CouncilUpdate objects
    - Handle event types: stage1_start, stage1_complete, etc.
    - Implement error event handling
    - Ensure proper connection cleanup
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 4.9 Write property test for streaming yields progressive updates
  - **Property 7: Streaming yields progressive updates**
  - **Validates: Requirements 4.1**

- [x] 5. Implement conversation management methods
  - [x] 5.1 Implement conversation CRUD operations
    - Implement create_conversation method
    - Implement list_conversations method
    - Implement get_conversation method
    - Implement delete_conversation method
    - Add x-user-id header to all requests
    - Parse responses into Conversation objects
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ]* 5.2 Write property test for conversation operations include user context
  - **Property 8: Conversation operations include user context**
  - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

- [ ]* 5.3 Write property test for conversation operation errors
  - **Property 9: Conversation operation errors raise exceptions**
  - **Validates: Requirements 5.5**

- [x] 6. Implement search and usage methods
  - [x] 6.1 Implement search_conversations method
    - Build search request with query parameter
    - Properly URL-encode query string
    - Parse search results into Conversation list
    - Handle empty results and errors
    - _Requirements: 6.1, 6.3, 6.4, 6.5_

- [ ]* 6.2 Write property test for search query parameter encoding
  - **Property 10: Search query parameter encoding**
  - **Validates: Requirements 6.1**

- [ ]* 6.3 Write property test for search error handling
  - **Property 11: Search error handling**
  - **Validates: Requirements 6.5**

- [x] 6.4 Implement get_usage method
    - Build usage request
    - Parse response into UsageStats object
    - Handle errors appropriately
    - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [ ]* 6.5 Write property test for usage retrieval error handling
  - **Property 13: Usage retrieval error handling**
  - **Validates: Requirements 7.5**

- [x] 7. Implement error handling and retry logic
  - [x] 7.1 Add comprehensive error handling
    - Implement HTTP status code to exception mapping
    - Add network error detection and ConnectionError raising
    - Implement parameter validation with ValidationError
    - Add helpful error messages and context
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 7.2 Write property test for network error handling
  - **Property 14: Network error handling**
  - **Validates: Requirements 9.1**

- [ ]* 7.3 Write property test for invalid parameter validation
  - **Property 15: Invalid parameter validation**
  - **Validates: Requirements 9.4**

- [x] 7.4 Implement retry logic with exponential backoff
    - Add retry decorator for transient errors
    - Implement exponential backoff with jitter
    - Configure retryable vs non-retryable errors
    - Respect max_retries configuration
    - _Requirements: 12.4_

- [ ]* 7.5 Write property test for retry policy application
  - **Property 19: Retry policy application**
  - **Validates: Requirements 12.4**

- [x] 8. Implement configuration handling
  - [x] 8.1 Add configuration propagation
    - Ensure timeout is applied to all httpx requests
    - Ensure base_url is used for all API calls
    - Validate configuration parameters in __init__
    - _Requirements: 12.2, 12.3, 12.5_

- [ ]* 8.2 Write property test for timeout configuration propagation
  - **Property 17: Timeout configuration propagation**
  - **Validates: Requirements 12.2**

- [ ]* 8.3 Write property test for base URL configuration
  - **Property 18: Base URL configuration**
  - **Validates: Requirements 12.3**

- [x] 9. Implement AsyncClient class
  - [x] 9.1 Create AsyncClient with async/await support
    - Copy Client interface with async method signatures
    - Use httpx.AsyncClient for non-blocking I/O
    - Implement async context manager (__aenter__, __aexit__)
    - Ensure proper connection cleanup
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 9.2 Implement async query and stream methods
    - Implement async query method
    - Implement async stream method with async generator
    - Ensure async iteration works correctly
    - _Requirements: 8.1, 8.3_

- [x] 9.3 Implement async conversation and utility methods
    - Implement async versions of all conversation methods
    - Implement async search_conversations
    - Implement async get_usage
    - _Requirements: 8.1_

- [x] 10. Add type hints and documentation
  - [x] 10.1 Add comprehensive type annotations
    - Add type hints to all public methods
    - Add type hints to all parameters and return values
    - Ensure dataclasses have typed attributes
    - _Requirements: 10.1, 10.2, 10.4_

- [x] 10.2 Write docstrings for all public APIs
    - Add docstrings to Client and AsyncClient classes
    - Add docstrings to all public methods
    - Include parameter descriptions and return types
    - Add usage examples in docstrings
    - _Requirements: 10.5, 11.3_

- [x] 11. Create examples and documentation
  - [x] 11.1 Create example scripts
    - Create basic_usage.py example
    - Create streaming_example.py example
    - Create async_example.py example
    - Create conversation_management.py example
    - _Requirements: 11.2, 11.5_

- [x] 11.2 Write README.md
    - Add installation instructions
    - Add quickstart guide
    - Add authentication setup
    - Add basic usage examples
    - Add links to full documentation
    - _Requirements: 11.1_

- [x] 12. Set up testing infrastructure
  - [x] 12.1 Configure pytest and testing tools
    - Set up pytest configuration
    - Add pytest-asyncio for async tests
    - Configure hypothesis for property-based testing
    - Set up respx for httpx mocking
    - _Requirements: All testing requirements_

- [x] 12.2 Create test fixtures and utilities
    - Create mock API response fixtures
    - Create test client factory
    - Add SSE event generator for streaming tests
    - _Requirements: All testing requirements_

- [x] 13. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 14. Set up CI/CD and packaging
  - [x] 14.1 Configure package build and distribution
    - Verify pyproject.toml is complete
    - Test package build with `python -m build`
    - Verify package metadata
    - Test installation in clean environment
    - _Requirements: 1.1, 1.2, 1.5_

- [x] 14.2 Add type checking and linting
    - Configure mypy for strict type checking
    - Run mypy on codebase and fix issues
    - Configure ruff for linting
    - Run black for code formatting
    - _Requirements: 10.3_

- [x] 15. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
