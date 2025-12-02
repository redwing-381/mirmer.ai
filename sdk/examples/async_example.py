"""
Async usage example for Mirmer AI SDK.

This example demonstrates:
- Using AsyncClient with async/await
- Async streaming
- Concurrent requests
"""

import asyncio
from mirmer import AsyncClient


async def basic_async_query():
    """Basic async query example."""
    async with AsyncClient(api_key="your-api-key-here") as client:
        response = await client.query("What is machine learning?")
        print("Chairman's answer:")
        print(response.stage3.response)


async def async_streaming():
    """Async streaming example."""
    async with AsyncClient(api_key="your-api-key-here") as client:
        print("Streaming updates...\n")

        async for update in client.stream("Explain neural networks"):
            if update.type == "stage1_complete":
                print(f"✅ Stage 1: {len(update.data)} responses")
            elif update.type == "stage2_complete":
                print(f"✅ Stage 2: {len(update.data['rankings'])} rankings")
            elif update.type == "stage3_complete":
                print("✅ Stage 3: Final answer ready")
                print(f"\n{update.data['response'][:200]}...")


async def concurrent_queries():
    """Make multiple queries concurrently."""
    async with AsyncClient(api_key="your-api-key-here") as client:
        # Create multiple queries concurrently
        queries = [
            "What is AI?",
            "What is machine learning?",
            "What is deep learning?",
        ]

        # Execute all queries concurrently
        tasks = [client.query(q) for q in queries]
        responses = await asyncio.gather(*tasks)

        # Display results
        for query, response in zip(queries, responses):
            print(f"\nQuery: {query}")
            print(f"Answer: {response.stage3.response[:150]}...")


async def main():
    """Run all examples."""
    print("=" * 60)
    print("1. Basic Async Query")
    print("=" * 60)
    await basic_async_query()

    print("\n" + "=" * 60)
    print("2. Async Streaming")
    print("=" * 60)
    await async_streaming()

    print("\n" + "=" * 60)
    print("3. Concurrent Queries")
    print("=" * 60)
    await concurrent_queries()


if __name__ == "__main__":
    asyncio.run(main())
