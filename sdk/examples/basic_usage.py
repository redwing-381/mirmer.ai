"""
Basic usage example for Mirmer AI SDK.

This example demonstrates:
- Initializing the client
- Sending a query
- Accessing the three stages of the council response
"""

from mirmer import Client

# Initialize client with API key
# You can also set MIRMER_API_KEY environment variable
client = Client(api_key="your-api-key-here")

# Or use context manager for automatic cleanup
with Client(api_key="your-api-key-here") as client:
    # Send a query and get complete council response
    response = client.query("What is the meaning of life?")

    # Access Stage 1 - Individual model responses
    print("=" * 60)
    print("STAGE 1: Individual Model Responses")
    print("=" * 60)
    for model_response in response.stage1:
        print(f"\n{model_response.model}:")
        print(model_response.response[:200] + "...")  # First 200 chars

    # Access Stage 2 - Peer rankings
    print("\n" + "=" * 60)
    print("STAGE 2: Peer Rankings")
    print("=" * 60)
    for ranking in response.stage2:
        print(f"\n{ranking.model}:")
        print(f"Ranking: {ranking.parsed_ranking}")

    # Access aggregate rankings
    print("\n" + "=" * 60)
    print("AGGREGATE RANKINGS")
    print("=" * 60)
    for agg in response.aggregate_rankings:
        print(f"{agg.model}: avg rank {agg.average_rank:.2f} ({agg.rankings_count} votes)")

    # Access Stage 3 - Chairman synthesis
    print("\n" + "=" * 60)
    print("STAGE 3: Chairman Synthesis")
    print("=" * 60)
    print(response.stage3.response)

    # Continue conversation
    print("\n" + "=" * 60)
    print("CONTINUING CONVERSATION")
    print("=" * 60)
    followup = client.query(
        "Can you elaborate on that?",
        conversation_id=response.conversation_id
    )
    print(followup.stage3.response)
