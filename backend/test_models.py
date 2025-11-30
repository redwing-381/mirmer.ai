"""
Quick test script to check which models are responding.
"""
import asyncio
import logging
from openrouter import query_model
from config import COUNCIL_MODELS, OPENROUTER_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_all_models():
    """Test each model individually to see which ones work."""
    test_message = [{"role": "user", "content": "Say 'Hello' in one word."}]
    
    print(f"\nTesting {len(COUNCIL_MODELS)} models...\n")
    
    for model in COUNCIL_MODELS:
        print(f"Testing {model}...")
        try:
            response = await query_model(
                model=model,
                messages=test_message,
                api_key=OPENROUTER_API_KEY,
                timeout=30.0
            )
            
            if response and response.get("content"):
                print(f"✓ {model}: SUCCESS - {response['content'][:50]}")
            else:
                print(f"✗ {model}: FAILED - No response")
        except Exception as e:
            print(f"✗ {model}: ERROR - {str(e)}")
        
        # Small delay between requests
        await asyncio.sleep(1)
    
    print("\nTest complete!")


if __name__ == "__main__":
    asyncio.run(test_all_models())
