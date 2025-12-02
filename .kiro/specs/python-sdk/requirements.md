taqtas# Requirements Document

## Introduction

The Mirmer AI Python SDK provides developers with a simple, Pythonic interface to integrate the multi-LLM council system into their applications. The SDK enables developers to leverage the 3-stage council process (parallel model queries, peer review, and chairman synthesis) programmatically, with support for both synchronous and asynchronous operations, streaming responses, and comprehensive error handling.

## Glossary

- **SDK**: Software Development Kit - a library that provides programmatic access to Mirmer AI's council system
- **Council Process**: The 3-stage system where multiple AI models respond, peer-review, and synthesize consensus answers
- **Client**: The main SDK class that developers instantiate to interact with the Mirmer AI API
- **Streaming**: Real-time delivery of council process updates as they occur via Server-Sent Events (SSE)
- **API Key**: Authentication credential that identifies and authorizes SDK users
- **Conversation**: A persistent chat session containing multiple messages and their council responses
- **Stage**: One of three phases in the council process (Stage 1: individual responses, Stage 2: peer rankings, Stage 3: synthesis)
- **Usage Tracking**: Monitoring of API calls against user's daily query limits

## Requirements

### Requirement 1

**User Story:** As a Python developer, I want to install the SDK via pip, so that I can quickly add Mirmer AI to my project with standard Python tooling.

#### Acceptance Criteria

1. WHEN a developer runs `pip install mirmer-ai` THEN the SDK SHALL install with all required dependencies
2. WHEN the SDK is installed THEN the system SHALL support Python 3.8 and above
3. WHEN the SDK is imported THEN the system SHALL expose a clean public API through the main module
4. WHEN dependencies are resolved THEN the SDK SHALL require only essential packages (httpx, pydantic)
5. WHEN the package is published THEN the system SHALL include proper metadata (version, author, license, description)

### Requirement 2

**User Story:** As a developer, I want to authenticate with my API key, so that I can securely access the Mirmer AI service.

#### Acceptance Criteria

1. WHEN a Client is instantiated with an API key THEN the system SHALL store the credential securely
2. WHEN an API key is not provided THEN the system SHALL attempt to read from the MIRMER_API_KEY environment variable
3. WHEN no API key is available THEN the system SHALL raise a clear authentication error before making requests
4. WHEN API requests are made THEN the system SHALL include the API key in the x-user-id header
5. WHEN an invalid API key is used THEN the system SHALL raise an authentication error with a helpful message

### Requirement 3

**User Story:** As a developer, I want to send queries and receive council responses, so that I can integrate multi-model consensus into my application.

#### Acceptance Criteria

1. WHEN a developer calls the query method with a message THEN the system SHALL initiate the 3-stage council process
2. WHEN the council process completes THEN the system SHALL return a response object containing all three stages
3. WHEN a conversation ID is provided THEN the system SHALL add the message to that existing conversation
4. WHEN no conversation ID is provided THEN the system SHALL create a new conversation automatically
5. WHEN the API returns an error THEN the system SHALL raise a descriptive exception with the error details

### Requirement 4

**User Story:** As a developer, I want to stream council updates in real-time, so that I can provide progressive feedback to my users.

#### Acceptance Criteria

1. WHEN a developer calls the stream method THEN the system SHALL yield updates as each stage progresses
2. WHEN Stage 1 completes THEN the system SHALL yield an event containing all individual model responses
3. WHEN Stage 2 completes THEN the system SHALL yield an event containing peer rankings
4. WHEN Stage 3 completes THEN the system SHALL yield an event containing the chairman synthesis
5. WHEN streaming encounters an error THEN the system SHALL yield an error event with details

### Requirement 5

**User Story:** As a developer, I want to manage conversations programmatically, so that I can organize and retrieve chat sessions.

#### Acceptance Criteria

1. WHEN a developer calls list_conversations THEN the system SHALL return all conversations for the authenticated user
2. WHEN a developer calls get_conversation with an ID THEN the system SHALL return the full conversation with all messages
3. WHEN a developer calls create_conversation with a title THEN the system SHALL create a new conversation and return its ID
4. WHEN a developer calls delete_conversation with an ID THEN the system SHALL remove the conversation permanently
5. WHEN a conversation operation fails THEN the system SHALL raise an exception with the failure reason

### Requirement 6

**User Story:** As a developer, I want to search through conversations, so that I can find relevant past discussions.

#### Acceptance Criteria

1. WHEN a developer calls search_conversations with a query string THEN the system SHALL return matching conversations
2. WHEN search results are returned THEN the system SHALL include conversations matching titles or message content
3. WHEN the search query is empty THEN the system SHALL return all conversations
4. WHEN no matches are found THEN the system SHALL return an empty list
5. WHEN search encounters an error THEN the system SHALL raise an exception with error details

### Requirement 7

**User Story:** As a developer, I want to check my usage statistics, so that I can monitor my API consumption and limits.

#### Acceptance Criteria

1. WHEN a developer calls get_usage THEN the system SHALL return current usage statistics
2. WHEN usage data is returned THEN the system SHALL include queries used today and daily limit
3. WHEN usage data is returned THEN the system SHALL include subscription tier information
4. WHEN the daily limit is reached THEN the system SHALL indicate this in the usage response
5. WHEN usage retrieval fails THEN the system SHALL raise an exception with error details

### Requirement 8

**User Story:** As a developer, I want async/await support, so that I can use the SDK in asynchronous Python applications.

#### Acceptance Criteria

1. WHEN a developer instantiates AsyncClient THEN the system SHALL provide async versions of all methods
2. WHEN async methods are called THEN the system SHALL use non-blocking I/O operations
3. WHEN async streaming is used THEN the system SHALL yield updates via async iteration
4. WHEN async operations complete THEN the system SHALL properly close HTTP connections
5. WHEN async and sync clients are used together THEN the system SHALL maintain separate connection pools

### Requirement 9

**User Story:** As a developer, I want comprehensive error handling, so that I can gracefully handle failures in my application.

#### Acceptance Criteria

1. WHEN network errors occur THEN the system SHALL raise a ConnectionError with retry suggestions
2. WHEN authentication fails THEN the system SHALL raise an AuthenticationError with clear guidance
3. WHEN rate limits are exceeded THEN the system SHALL raise a RateLimitError with reset time information
4. WHEN invalid parameters are provided THEN the system SHALL raise a ValidationError before making requests
5. WHEN the API returns unexpected errors THEN the system SHALL raise an APIError with status code and message

### Requirement 10

**User Story:** As a developer, I want type hints and IDE support, so that I can write correct code with autocomplete and type checking.

#### Acceptance Criteria

1. WHEN the SDK is imported THEN the system SHALL provide complete type annotations for all public methods
2. WHEN developers use IDEs THEN the system SHALL enable autocomplete for methods and parameters
3. WHEN type checkers run THEN the system SHALL pass mypy strict mode validation
4. WHEN response objects are accessed THEN the system SHALL provide typed attributes with proper hints
5. WHEN the SDK is documented THEN the system SHALL include type information in docstrings

### Requirement 11

**User Story:** As a developer, I want clear documentation and examples, so that I can quickly learn how to use the SDK.

#### Acceptance Criteria

1. WHEN developers visit the documentation THEN the system SHALL provide a quickstart guide with installation steps
2. WHEN developers read the docs THEN the system SHALL include code examples for common use cases
3. WHEN developers need API reference THEN the system SHALL provide complete method documentation
4. WHEN developers encounter errors THEN the system SHALL provide troubleshooting guidance
5. WHEN developers want advanced features THEN the system SHALL include examples for streaming and async usage

### Requirement 12

**User Story:** As a developer, I want to configure SDK behavior, so that I can customize timeouts, retries, and base URLs for my environment.

#### Acceptance Criteria

1. WHEN a Client is instantiated THEN the system SHALL accept optional configuration parameters
2. WHEN timeout is configured THEN the system SHALL apply it to all HTTP requests
3. WHEN base_url is configured THEN the system SHALL use it instead of the default API endpoint
4. WHEN retry configuration is provided THEN the system SHALL retry failed requests according to the policy
5. WHEN configuration is invalid THEN the system SHALL raise a validation error with helpful messages
