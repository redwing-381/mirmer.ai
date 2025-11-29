# Requirements Document

## Introduction

Mirmer AI is a multi-LLM consultation system that queries multiple AI models in parallel, has them peer-review each other's responses, and synthesizes a final answer. The system follows a 3-stage council process where models provide independent responses, anonymously rank each other's answers, and a chairman model synthesizes the collective wisdom into a comprehensive final answer.

## Glossary

- **Mirmer AI Platform**: The system that orchestrates the 3-stage council process
- **Council Members**: List of LLM models that participate in all stages
- **Chairman Model**: Special model that synthesizes the final response from all context
- **User**: A person who provides an OpenRouter API key and submits queries
- **OpenRouter API Key**: Authentication credential for accessing multiple AI models through OpenRouter
- **OpenRouter**: Unified API gateway that provides access to multiple AI model providers
- **Stage 1**: Individual response collection phase where all models answer the query
- **Stage 2**: Peer review phase where models rank anonymized responses
- **Stage 3**: Final synthesis phase where chairman creates comprehensive answer
- **Anonymization**: Process of labeling responses as "Response A", "Response B", etc.
- **Aggregate Rankings**: Combined peer review scores showing "street cred"
- **Conversation**: A stored session containing user queries and council responses

## Requirements

### Requirement 1

**User Story:** As a user, I want to provide my OpenRouter API key, so that I can access multiple AI models for consultation

#### Acceptance Criteria

1. THE Mirmer AI Platform SHALL provide an interface for users to input an OpenRouter API key
2. THE Mirmer AI Platform SHALL store the OpenRouter API key securely in the session
3. THE Mirmer AI Platform SHALL validate that the OpenRouter API key is provided before allowing query submission
4. WHEN a user session ends, THE Mirmer AI Platform SHALL clear the stored OpenRouter API key
5. THE Mirmer AI Platform SHALL use the OpenRouter API key for all model queries within the session

### Requirement 2

**User Story:** As a user, I want to submit a query and see progressive updates, so that I can follow the council process in real-time

#### Acceptance Criteria

1. THE Mirmer AI Platform SHALL provide an interface for users to submit a text query
2. THE Mirmer AI Platform SHALL accept queries with a minimum length of 10 characters and maximum length of 2000 characters
3. WHEN a user submits a query, THE Mirmer AI Platform SHALL initiate the 3-stage council process
4. THE Mirmer AI Platform SHALL stream progressive updates using Server-Sent Events as each stage completes
5. THE Mirmer AI Platform SHALL display loading indicators for each stage while processing

### Requirement 3

**User Story:** As the system, I want to collect individual responses from all council members in parallel, so that I can gather diverse perspectives efficiently

#### Acceptance Criteria

1. WHEN Stage 1 starts, THE Mirmer AI Platform SHALL query all council models in parallel using asyncio.gather
2. THE Mirmer AI Platform SHALL send the same user query to each council model through OpenRouter
3. THE Mirmer AI Platform SHALL use the user-provided OpenRouter API key for authentication
4. IF a model request fails, THEN THE Mirmer AI Platform SHALL log the error and continue with remaining models
5. THE Mirmer AI Platform SHALL return all successfully generated responses with model identifiers

### Requirement 4

**User Story:** As the system, I want models to peer-review each other's responses anonymously, so that I can get unbiased quality assessments

#### Acceptance Criteria

1. WHEN Stage 2 starts, THE Mirmer AI Platform SHALL anonymize all Stage 1 responses using labels like "Response A", "Response B", etc.
2. THE Mirmer AI Platform SHALL create a ranking prompt that includes all anonymized responses
3. THE Mirmer AI Platform SHALL send the ranking prompt to all council models in parallel
4. THE Mirmer AI Platform SHALL parse each model's ranking using regex patterns with fallback strategies
5. THE Mirmer AI Platform SHALL maintain a label-to-model mapping for UI display

### Requirement 5

**User Story:** As the system, I want to calculate aggregate rankings, so that users can see which responses were collectively rated highest

#### Acceptance Criteria

1. WHEN Stage 2 completes, THE Mirmer AI Platform SHALL calculate aggregate rankings across all peer reviews
2. THE Mirmer AI Platform SHALL track the position each response received in each ranking
3. THE Mirmer AI Platform SHALL calculate the average position for each response (lower is better)
4. THE Mirmer AI Platform SHALL sort responses by average rank to show "street cred"
5. THE Mirmer AI Platform SHALL include vote counts with each aggregate ranking

### Requirement 6

**User Story:** As the system, I want the chairman to synthesize a final answer with full context, so that users receive comprehensive wisdom from the council

#### Acceptance Criteria

1. WHEN Stage 3 starts, THE Mirmer AI Platform SHALL build a chairman prompt containing all Stage 1 responses and Stage 2 rankings
2. THE Mirmer AI Platform SHALL query the designated chairman model with the comprehensive context
3. THE Mirmer AI Platform SHALL emphasize synthesis over summarization in the chairman prompt
4. THE Mirmer AI Platform SHALL return the chairman's response as the final answer
5. IF the chairman query fails, THEN THE Mirmer AI Platform SHALL return an error message

### Requirement 7

**User Story:** As a user, I want to see all three stages of results in a clear interface, so that I can understand the council's deliberation process

#### Acceptance Criteria

1. WHEN Stage 1 completes, THE Mirmer AI Platform SHALL display individual responses in a tabbed interface
2. WHEN Stage 2 completes, THE Mirmer AI Platform SHALL display peer rankings with de-anonymized model names
3. THE Mirmer AI Platform SHALL display aggregate rankings showing which responses were collectively rated best
4. WHEN Stage 3 completes, THE Mirmer AI Platform SHALL display the chairman's final synthesized answer prominently
5. THE Mirmer AI Platform SHALL render all responses using markdown formatting

### Requirement 8

**User Story:** As a user, I want conversations to be saved, so that I can review past council consultations

#### Acceptance Criteria

1. THE Mirmer AI Platform SHALL create a new conversation when a user starts a session
2. THE Mirmer AI Platform SHALL save each user query and complete council response to JSON files
3. THE Mirmer AI Platform SHALL generate a conversation title from the first user query
4. THE Mirmer AI Platform SHALL list all conversations in a sidebar with titles and timestamps
5. THE Mirmer AI Platform SHALL allow users to view past conversations with all three stages intact

### Requirement 9

**User Story:** As a developer, I want the platform to handle errors gracefully, so that users have a reliable experience

#### Acceptance Criteria

1. IF a model request fails, THEN THE Mirmer AI Platform SHALL log the error and continue with remaining models
2. IF all models fail in a stage, THEN THE Mirmer AI Platform SHALL display an error message to the user
3. THE Mirmer AI Platform SHALL implement a 120-second timeout per model request
4. THE Mirmer AI Platform SHALL stream error events to the frontend via Server-Sent Events
5. THE Mirmer AI Platform SHALL log all errors with timestamps and model identifiers for debugging
