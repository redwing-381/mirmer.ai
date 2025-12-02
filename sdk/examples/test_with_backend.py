"""
Test the SDK with your local Mirmer AI backend.

This example shows how to use the SDK with your existing backend.
"""

from mirmer import Client

# IMPORTANT: Your backend uses Firebase authentication
# The "API key" is actually a Firebase ID token from an authenticated user

# For testing with your local backend:
# 1. Start your backend: cd backend && uv run uvicorn main:app --reload --port 8001
# 2. Get a Firebase ID token from your frontend (check browser dev tools)
# 3. Use that token here

# Example with local backend
client = Client(
    api_key="your-firebase-id-token-here",  # Get this from your authenticated frontend
    base_url="http://localhost:8001",  # Your local backend
)

try:
    # Test creating a conversation
    print("Creating conversation...")
    conversation = client.create_conversation()
    print(f"✅ Created: {conversation.id}")
    
    # Test sending a query
    print("\nSending query...")
    response = client.query(
        "What is 2+2?",
        conversation_id=conversation.id
    )
    print(f"✅ Got response with {len(response.stage1)} models")
    print(f"\nFinal answer: {response.stage3.response[:200]}...")
    
    # Test listing conversations
    print("\nListing conversations...")
    conversations = client.list_conversations()
    print(f"✅ Found {len(conversations)} conversations")
    
    # Test usage stats
    print("\nChecking usage...")
    usage = client.get_usage()
    print(f"✅ Used {usage.queries_used_today}/{usage.daily_limit} queries")
    print(f"   Tier: {usage.tier}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure:")
    print("1. Backend is running: cd backend && uv run uvicorn main:app --reload --port 8001")
    print("2. You have a valid Firebase ID token")
    print("3. The token is set in the api_key parameter")

finally:
    client.close()
