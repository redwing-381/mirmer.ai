"""
Conversation management example for Mirmer AI SDK.

This example demonstrates:
- Creating conversations
- Listing conversations
- Searching conversations
- Getting conversation details
- Deleting conversations
- Checking usage statistics
"""

from mirmer import Client

# Initialize client
client = Client(api_key="your-api-key-here")

# Create a new conversation
print("Creating a new conversation...")
conversation = client.create_conversation(title="AI Discussion")
print(f"Created conversation: {conversation.id}")

# Send messages to the conversation
print("\nSending messages...")
response1 = client.query("What is AI?", conversation_id=conversation.id)
print(f"Response 1: {response1.stage3.response[:100]}...")

response2 = client.query("How does it work?", conversation_id=conversation.id)
print(f"Response 2: {response2.stage3.response[:100]}...")

# List all conversations
print("\n" + "=" * 60)
print("All Conversations:")
print("=" * 60)
conversations = client.list_conversations()
for conv in conversations:
    print(f"- {conv.title} (ID: {conv.id}, Created: {conv.created_at})")
    print(f"  Messages: {len(conv.messages)}")

# Search conversations
print("\n" + "=" * 60)
print("Searching for 'AI':")
print("=" * 60)
results = client.search_conversations("AI")
for conv in results:
    print(f"- {conv.title} (ID: {conv.id})")

# Get specific conversation with all messages
print("\n" + "=" * 60)
print("Getting conversation details:")
print("=" * 60)
full_conversation = client.get_conversation(conversation.id)
print(f"Title: {full_conversation.title}")
print(f"Messages: {len(full_conversation.messages)}")
for i, msg in enumerate(full_conversation.messages, 1):
    print(f"\n{i}. {msg.role.upper()}: {msg.content[:80]}...")
    if msg.role == "assistant" and msg.stage3:
        print(f"   Answer: {msg.stage3.response[:80]}...")

# Check usage statistics
print("\n" + "=" * 60)
print("Usage Statistics:")
print("=" * 60)
usage = client.get_usage()
print(f"Tier: {usage.tier}")
print(f"Queries used today: {usage.queries_used_today}/{usage.daily_limit}")
print(f"Reset time: {usage.reset_time}")

# Delete a conversation
print("\n" + "=" * 60)
print("Deleting conversation:")
print("=" * 60)
success = client.delete_conversation(conversation.id)
if success:
    print(f"✅ Conversation {conversation.id} deleted successfully")
else:
    print(f"❌ Failed to delete conversation")

# Verify deletion
remaining = client.list_conversations()
print(f"\nRemaining conversations: {len(remaining)}")

client.close()
