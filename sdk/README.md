# Mirmer AI Python SDK

A Python client library for the Mirmer AI multi-LLM consultation system.

## Installation

```bash
pip install mirmer-ai
```

## Quick Start

```python
from mirmer import Client

# Initialize client with API key
client = Client(api_key="your-api-key")

# Or use environment variable MIRMER_API_KEY
client = Client()

# Send a query and get council response
response = client.query("What is the meaning of life?")

# Access the three stages
print("Stage 1 - Individual Responses:")
for model_response in response.stage1:
    print(f"{model_response.model}: {model_response.response}")

print("\nStage 2 - Peer Rankings:")
for ranking in response.stage2:
    print(f"{ranking.model}: {ranking.parsed_ranking}")

print("\nStage 3 - Chairman Synthesis:")
print(response.stage3.response)
```

## Features

- **3-Stage Council Process**: Query multiple AI models, get peer reviews, and receive synthesized consensus
- **Streaming Support**: Real-time updates as each stage completes
- **Async/Await**: Full async support with `AsyncClient`
- **Conversation Management**: Create, list, search, and delete conversations
- **Usage Tracking**: Monitor your API consumption and limits
- **Type Safety**: Complete type hints for IDE autocomplete and type checking
- **Error Handling**: Comprehensive exception hierarchy for graceful error handling

## Usage Examples

### Streaming Responses

```python
from mirmer import Client

client = Client(api_key="your-api-key")

# Stream council process updates in real-time
for update in client.stream("Explain quantum computing"):
    if update.type == "stage1_complete":
        print(f"Stage 1 complete: {len(update.data['stage1'])} responses")
    elif update.type == "stage3_complete":
        print(f"Final answer: {update.data['response']}")
```

### Async Usage

```python
import asyncio
from mirmer import AsyncClient

async def main():
    async with AsyncClient(api_key="your-api-key") as client:
        response = await client.query("What is machine learning?")
        print(response.stage3.response)

asyncio.run(main())
```

### Conversation Management

```python
from mirmer import Client

client = Client(api_key="your-api-key")

# Create a new conversation
conversation = client.create_conversation(title="AI Discussion")

# Add messages to the conversation
response = client.query("What is AI?", conversation_id=conversation.id)

# List all conversations
conversations = client.list_conversations()

# Search conversations
results = client.search_conversations("machine learning")

# Get specific conversation
conv = client.get_conversation(conversation.id)

# Delete conversation
client.delete_conversation(conversation.id)
```

### Usage Statistics

```python
from mirmer import Client

client = Client(api_key="your-api-key")

# Check your usage
usage = client.get_usage()
print(f"Used: {usage.queries_used_today}/{usage.daily_limit}")
print(f"Tier: {usage.tier}")
```

## Configuration

```python
from mirmer import Client

client = Client(
    api_key="your-api-key",
    base_url="https://api.mirmer.ai",  # Custom API endpoint
    timeout=60.0,                       # Request timeout in seconds
    max_retries=3                       # Max retry attempts for failed requests
)
```

## Error Handling

```python
from mirmer import Client, AuthenticationError, RateLimitError, APIError

client = Client(api_key="your-api-key")

try:
    response = client.query("Hello")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limit exceeded. Reset at: {e.reset_time}")
except APIError as e:
    print(f"API error: {e.message} (status: {e.status_code})")
```

## Requirements

- Python 3.8+
- httpx >= 0.24.0
- pydantic >= 2.0.0
- python-dateutil >= 2.8.0

## License

MIT License - see LICENSE file for details

## Support

- Documentation: https://docs.mirmer.ai
- Issues: https://github.com/mirmer-ai/python-sdk/issues
- Email: support@mirmer.ai
