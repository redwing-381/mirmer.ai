"""
Streaming example for Mirmer AI SDK.

This example demonstrates:
- Real-time streaming of council process updates
- Handling different event types
- Progressive UI updates
"""

from mirmer import Client

# Initialize client
client = Client(api_key="your-api-key-here")

print("Streaming council process updates...\n")

# Stream council process updates in real-time
for update in client.stream("Explain quantum computing in simple terms"):
    if update.type == "stage1_start":
        print("🚀 Stage 1: Collecting individual model responses...")

    elif update.type == "stage1_complete":
        print(f"✅ Stage 1 complete: {len(update.data)} responses received\n")
        # Optionally display responses as they arrive
        for response in update.data:
            print(f"  - {response['model']}")

    elif update.type == "stage2_start":
        print("\n🚀 Stage 2: Models ranking each other's responses...")

    elif update.type == "stage2_complete":
        print(f"✅ Stage 2 complete: {len(update.data['rankings'])} rankings received")
        # Display aggregate rankings
        print("\nAggregate Rankings:")
        for agg in update.data.get("aggregate_rankings", []):
            print(f"  {agg['model']}: {agg['average_rank']:.2f}")

    elif update.type == "stage3_start":
        print("\n🚀 Stage 3: Chairman synthesizing final answer...")

    elif update.type == "stage3_complete":
        print("✅ Stage 3 complete\n")
        print("=" * 60)
        print("FINAL ANSWER:")
        print("=" * 60)
        print(update.data["response"])

    elif update.type == "complete":
        print("\n✨ Council process complete!")

    elif update.type == "error":
        print(f"❌ Error: {update.error}")
        break

client.close()
