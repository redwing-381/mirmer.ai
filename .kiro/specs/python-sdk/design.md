# Design Document

## Overview

The Mirmer AI Python SDK provides a clean, Pythonic interface for developers to integrate the multi-LLM council system into their applications. The SDK wraps the Mirmer AI REST API and Server-Sent Events (SSE) streaming endpoints, offering both synchronous and asynchronous clients with comprehensive error handling, type safety, and developer-friendly abstractions.

The SDK will be distributed via PyPI as `mirmer-ai` and will support Python 3.8+. It follows modern Python best practices including type hints, dataclasses for structured responses, and context managers for resource cleanup.

## Architecture

### Package Structure

```
mirmer-ai/
├── mirmer/
│   ├── __init__.py           # Public API exports
│   ├── client.py             # Synchronous Client class
│   ├── async_client.py       # Asynchronous AsyncClient class
│   ├── models.py             # Pydantic models for requests/responses
│   ├── exceptions.py         # Custom exception classes
│   ├── streaming.py          # SSE streaming utilities
│   └── _version.py           # Version information
├── tests/
│   ├── test_client.py
│   ├── test_async_client.py
│   ├── test_models.py
│   └── test_streaming.py
├── examples/
│   ├── basic_usage.py
│   ├── streaming_example.py
│   ├── async_example.py
│   └── conversation_management.py
├── pyproject.toml            # Modern Python packaging
├── README.md
└── LICENSE


### Client Architecture

The SDK provides two client classes:

1. **Client** (Synchronous): Uses `httpx` synchronous client for blocking operations
2. **AsyncClient** (Asynchronous): Uses `httpx` async client for non-blocking operations

Both clients share the same interface and method signatures, differing only in their execution model (blocking vs async/await).

### Authentication Flow

```
Developer instantiates Client
    ↓
API key provided via constructor or MIRMER_API_KEY env var
    ↓
API key stored in client instance
    ↓
All requests include x-user-id header with API key
    ↓
Backend validates Firebase token and returns data
```

### Request/Response Flow

```
Developer calls client method (e.g., query())
    ↓
Client validates parameters locally
    ↓
Client constructs HTTP request with proper headers
    ↓
Request sent to Mirmer AI API
    ↓
Response parsed into typed Python objects
    ↓
Errors mapped to custom exceptions
    ↓
Structured data returned to developer
```

### Streaming Architecture

For real-time council updates, the SDK uses Server-Sent Events (SSE):

```
Developer calls client.stream()
    ↓
Client opens SSE connection to /api/conversations/{id}/message/stream
    ↓
Client yields CouncilUpdate objects as events arrive
    ↓
Events: stage1_start, stage1_complete, stage2_start, stage2_complete, 
        stage3_start, stage3_complete, complete, error
    ↓
Connection automatically closed on completion or error
```

## Components and Interfaces

### 1. Client Class (Synchronous)

```python
class Client:
    """Synchronous client for Mirmer AI API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.mirmer.ai",
        timeout: float = 60.0,
        max_retries: int = 3
    ):
        """Initialize client with authentication and configuration."""
        
    def query(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> CouncilResponse:
        """Send a query and wait for complete council response."""
        
    def stream(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Iterator[CouncilUpdate]:
        """Stream council process updates in real-time."""
        
    def create_conversation(self, title: Optional[str] = None) -> Conversation:
        """Create a new conversation."""
        
    def list_conversations(self) -> List[Conversation]:
        """List all conversations for the authenticated user."""
        
    def get_conversation(self, conversation_id: str) -> Conversation:
        """Get a specific conversation with all messages."""
        
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        
    def search_conversations(self, query: str) -> List[Conversation]:
        """Search conversations by title and content."""
        
    def get_usage(self) -> UsageStats:
        """Get current usage statistics."""
        
    def close(self):
        """Close HTTP connections."""
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.close()
```

### 2. AsyncClient Class (Asynchronous)

```python
class AsyncClient:
    """Asynchronous client for Mirmer AI API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.mirmer.ai",
        timeout: float = 60.0,
        max_retries: int = 3
    ):
        """Initialize async client with authentication and configuration."""
        
    async def query(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> CouncilResponse:
        """Send a query and wait for complete council response."""
        
    async def stream(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> AsyncIterator[CouncilUpdate]:
        """Stream council process updates in real-time."""
        
    async def create_conversation(self, title: Optional[str] = None) -> Conversation:
        """Create a new conversation."""
        
    async def list_conversations(self) -> List[Conversation]:
        """List all conversations."""
        
    async def get_conversation(self, conversation_id: str) -> Conversation:
        """Get a specific conversation."""
        
    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        
    async def search_conversations(self, query: str) -> List[Conversation]:
        """Search conversations."""
        
    async def get_usage(self) -> UsageStats:
        """Get usage statistics."""
        
    async def close(self):
        """Close HTTP connections."""
        
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
```

### 3. Exception Hierarchy

```python
class MirmerError(Exception):
    """Base exception for all Mirmer SDK errors."""
    pass

class AuthenticationError(MirmerError):
    """Raised when API key is invalid or missing."""
    pass

class RateLimitError(MirmerError):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str, reset_time: Optional[datetime] = None):
        super().__init__(message)
        self.reset_time = reset_time

class ValidationError(MirmerError):
    """Raised when request parameters are invalid."""
    pass

class NotFoundError(MirmerError):
    """Raised when a resource is not found."""
    pass

class ConnectionError(MirmerError):
    """Raised when network connection fails."""
    pass

class APIError(MirmerError):
    """Raised for general API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
```

## Data Models

All data models use Pydantic for validation and serialization:

### CouncilResponse

```python
@dataclass
class ModelResponse:
    """Individual model response from Stage 1."""
    model: str
    response: str

@dataclass
class ModelRanking:
    """Model ranking from Stage 2."""
    model: str
    ranking: str
    parsed_ranking: List[str]

@dataclass
class AggregateRanking:
    """Aggregate ranking result."""
    model: str
    average_rank: float
    rankings_count: int

@dataclass
class ChairmanSynthesis:
    """Chairman synthesis from Stage 3."""
    model: str
    response: str

@dataclass
class CouncilResponse:
    """Complete council response with all three stages."""
    conversation_id: str
    stage1: List[ModelResponse]
    stage2: List[ModelRanking]
    stage3: ChairmanSynthesis
    aggregate_rankings: List[AggregateRanking]
    label_to_model: Dict[str, str]
```

### CouncilUpdate (Streaming)

```python
@dataclass
class CouncilUpdate:
    """Real-time update from streaming council process."""
    type: str  # stage1_start, stage1_complete, stage2_start, etc.
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
```

### Conversation

```python
@dataclass
class Message:
    """A single message in a conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    stage1: Optional[List[ModelResponse]] = None
    stage2: Optional[List[ModelRanking]] = None
    stage3: Optional[ChairmanSynthesis] = None

@dataclass
class Conversation:
    """A conversation with messages."""
    id: str
    title: str
    created_at: str
    messages: List[Message]
```

### UsageStats

```python
@dataclass
class UsageStats:
    """User's API usage statistics."""
    queries_used_today: int
    daily_limit: int
    tier: str  # "free", "pro", "enterprise"
    reset_time: str
```



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: API key security in client representation
*For any* Client instance with an API key, the string representation and repr should not expose the API key value
**Validates: Requirements 2.1**

### Property 2: API key header inclusion
*For any* API request made by the client, the x-user-id header should contain the configured API key
**Validates: Requirements 2.4**

### Property 3: Query initiates council process
*For any* valid message string, calling the query method should result in a POST request to the streaming endpoint with the message content
**Validates: Requirements 3.1**

### Property 4: Complete response structure
*For any* successful council response, the returned CouncilResponse object should contain non-empty stage1, stage2, and stage3 data
**Validates: Requirements 3.2**

### Property 5: Conversation ID propagation
*For any* query call with a conversation_id parameter, the request should include that conversation_id in the URL path
**Validates: Requirements 3.3**

### Property 6: Error response handling
*For any* API error response (4xx or 5xx status), the client should raise an appropriate exception subclass of MirmerError
**Validates: Requirements 3.5**

### Property 7: Streaming yields progressive updates
*For any* streaming request, the stream method should yield CouncilUpdate objects in the order: stage1_start, stage1_complete, stage2_start, stage2_complete, stage3_start, stage3_complete, complete
**Validates: Requirements 4.1**

### Property 8: Conversation operations include user context
*For any* conversation management method (list, get, create, delete), the request should include the x-user-id header for authentication
**Validates: Requirements 5.1, 5.2, 5.3, 5.4**

### Property 9: Conversation operation errors raise exceptions
*For any* failed conversation operation (404, 403, 500), the client should raise an appropriate exception with the error details
**Validates: Requirements 5.5**

### Property 10: Search query parameter encoding
*For any* search query string, the search_conversations method should properly URL-encode the query parameter
**Validates: Requirements 6.1**

### Property 11: Search error handling
*For any* search request that fails, the client should raise an exception with error details
**Validates: Requirements 6.5**

### Property 12: Usage stats structure
*For any* successful get_usage call, the returned UsageStats object should contain queries_used_today, daily_limit, and tier fields
**Validates: Requirements 7.1, 7.2, 7.3**

### Property 13: Usage retrieval error handling
*For any* failed usage request, the client should raise an exception with error details
**Validates: Requirements 7.5**

### Property 14: Network error handling
*For any* network connection failure, the client should raise a ConnectionError with a descriptive message
**Validates: Requirements 9.1**

### Property 15: Invalid parameter validation
*For any* method call with invalid parameters (empty strings, None where required, invalid types), the client should raise a ValidationError before making HTTP requests
**Validates: Requirements 9.4**

### Property 16: API error mapping
*For any* API response with an error status code, the client should raise an APIError with the status code and response message
**Validates: Requirements 9.5**

### Property 17: Timeout configuration propagation
*For any* Client instantiated with a custom timeout value, all HTTP requests should use that timeout
**Validates: Requirements 12.2**

### Property 18: Base URL configuration
*For any* Client instantiated with a custom base_url, all API requests should be made to that base URL
**Validates: Requirements 12.3**

### Property 19: Retry policy application
*For any* Client configured with retry settings, failed requests should be retried according to the policy
**Validates: Requirements 12.4**

### Property 20: Configuration validation
*For any* Client instantiation with invalid configuration (negative timeout, invalid URL format), the constructor should raise a ValidationError
**Validates: Requirements 12.5**

## Error Handling

### Error Mapping Strategy

The SDK maps HTTP status codes and error conditions to specific exception types:

| Condition | Exception | HTTP Status |
|-----------|-----------|-------------|
| Missing/invalid API key | AuthenticationError | 401, 403 |
| Rate limit exceeded | RateLimitError | 429 |
| Resource not found | NotFoundError | 404 |
| Invalid parameters | ValidationError | 400 |
| Network failure | ConnectionError | N/A |
| Server error | APIError | 500, 502, 503 |
| Unknown error | APIError | Other |

### Retry Strategy

The SDK implements exponential backoff for transient errors:

- **Retryable errors**: 429 (rate limit), 500, 502, 503 (server errors), network timeouts
- **Non-retryable errors**: 400 (bad request), 401/403 (auth), 404 (not found)
- **Backoff formula**: `delay = base_delay * (2 ** attempt)` with jitter
- **Max retries**: Configurable (default: 3)

### Error Context

All exceptions include:
- Original error message from API
- HTTP status code (when applicable)
- Request details (method, endpoint)
- Suggestions for resolution (when possible)

## Testing Strategy

### Unit Testing

Unit tests will cover:

- **Client initialization**: API key handling, environment variable fallback, configuration validation
- **Request construction**: Header inclusion, URL building, parameter encoding
- **Response parsing**: JSON deserialization, dataclass instantiation, error handling
- **Exception mapping**: Status code to exception type mapping
- **Configuration**: Timeout, base URL, retry policy application

Unit tests will use `pytest` with `httpx` mock responses to simulate API behavior without making real network calls.

### Property-Based Testing

Property-based tests will use **Hypothesis** to verify universal properties across many inputs:

- **API key security**: Generate random API keys and verify they're never exposed in string representations
- **Header inclusion**: Generate random messages and verify x-user-id header is always present
- **URL encoding**: Generate random search queries with special characters and verify proper encoding
- **Error handling**: Generate random error responses and verify appropriate exceptions are raised
- **Configuration validation**: Generate random configuration values and verify validation works correctly
- **Streaming order**: Verify streaming events always arrive in the correct order
- **Response structure**: Verify all response objects have required fields regardless of API response content

Each property-based test will run a minimum of 100 iterations to ensure comprehensive coverage.

### Integration Testing

Integration tests will:

- Test against a mock Mirmer AI API server
- Verify end-to-end flows (authentication → query → response parsing)
- Test streaming with simulated SSE events
- Verify async/sync client parity
- Test context manager resource cleanup

### Test Tagging

Each property-based test will be tagged with a comment referencing the design document:

```python
def test_api_key_security(api_key):
    """Feature: python-sdk, Property 1: API key security in client representation"""
    # Test implementation
```

## Dependencies

### Required Dependencies

- **httpx** (≥0.24.0): Modern HTTP client with sync/async support and HTTP/2
- **pydantic** (≥2.0.0): Data validation and serialization
- **python-dateutil** (≥2.8.0): Date/time parsing for timestamps

### Development Dependencies

- **pytest** (≥7.0.0): Testing framework
- **pytest-asyncio** (≥0.21.0): Async test support
- **hypothesis** (≥6.0.0): Property-based testing
- **mypy** (≥1.0.0): Static type checking
- **black** (≥23.0.0): Code formatting
- **ruff** (≥0.1.0): Fast linting
- **respx** (≥0.20.0): httpx mocking for tests

## Deployment and Distribution

### PyPI Package

The SDK will be published to PyPI as `mirmer-ai`:

```bash
pip install mirmer-ai
```

### Versioning

The SDK follows Semantic Versioning (SemVer):
- **Major**: Breaking API changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

### Release Process

1. Update version in `_version.py`
2. Update CHANGELOG.md
3. Run full test suite (unit + property + integration)
4. Run mypy type checking
5. Build distribution: `python -m build`
6. Upload to PyPI: `twine upload dist/*`
7. Tag release in git: `git tag v1.0.0`

### Documentation

Documentation will be hosted on Read the Docs with:
- Quickstart guide
- API reference (auto-generated from docstrings)
- Usage examples
- Error handling guide
- Migration guides for version updates

## Security Considerations

### API Key Storage

- API keys stored in memory only (never written to disk by SDK)
- No logging of API keys
- API keys excluded from string representations
- Recommendation to use environment variables

### HTTPS Enforcement

- All requests use HTTPS by default
- Certificate verification enabled
- No option to disable SSL verification (security by design)

### Input Validation

- All user inputs validated before making requests
- SQL injection not applicable (REST API, not database)
- XSS not applicable (no HTML rendering in SDK)
- Path traversal not applicable (no file operations)

## Performance Considerations

### Connection Pooling

- httpx maintains connection pool for request reuse
- Configurable pool size (default: 10 connections)
- Automatic connection cleanup on client close

### Streaming Efficiency

- SSE events processed incrementally
- No buffering of entire response
- Memory-efficient for long-running streams

### Async Performance

- AsyncClient uses non-blocking I/O
- Suitable for high-concurrency applications
- No thread overhead (uses asyncio event loop)

## Future Enhancements

Potential future additions (not in initial release):

1. **Caching**: Optional response caching for repeated queries
2. **Batch operations**: Send multiple queries in one request
3. **Webhooks**: Register callbacks for async notifications
4. **CLI tool**: Command-line interface for quick testing
5. **Retry callbacks**: Custom hooks for retry logic
6. **Request middleware**: Custom request/response processing
7. **Metrics**: Built-in metrics collection for monitoring
8. **Rate limit handling**: Automatic backoff and retry for rate limits
