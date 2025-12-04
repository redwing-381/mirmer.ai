"""
OpenRouter API client for querying multiple LLM models.
"""
import httpx
import logging
from typing import Dict, List, Optional, Any
from config import OPENROUTER_API_URL, OPENROUTER_API_KEY
from rate_limiter import get_rate_limiter

logger = logging.getLogger(__name__)


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    api_key: Optional[str] = None,
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via OpenRouter API.
    
    Args:
        model: Model identifier (e.g., "openai/gpt-4-turbo")
        messages: List of message dicts with 'role' and 'content'
        api_key: OpenRouter API key (uses config default if not provided)
        timeout: Request timeout in seconds (default: 120s)
    
    Returns:
        Dictionary with 'content' key containing the response text,
        or None if the request fails.
    
    Requirements: 3.2, 3.3, 9.3
    """
    key = api_key or OPENROUTER_API_KEY
    
    if not key:
        logger.error("No OpenRouter API key provided")
        return None
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages
    }
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            # Update rate limiter with response headers
            rate_limiter = get_rate_limiter()
            rate_limiter.update_from_headers("openrouter", dict(response.headers))
            
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                logger.error(f"Empty response from model {model}")
                return None
            
            return {"content": content}
            
    except httpx.TimeoutException:
        logger.error(f"Timeout querying model {model} after {timeout}s")
        return None
    except httpx.HTTPStatusError as e:
        # Check if it's a rate limit error (429)
        if e.response.status_code == 429:
            logger.warning(f"Rate limit hit for model {model}")
            # Rate limit handling will be done at a higher level
        logger.error(f"HTTP error querying model {model}: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Error querying model {model}: {str(e)}")
        return None


import asyncio


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]],
    api_key: Optional[str] = None,
    timeout: float = 120.0
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel using asyncio.gather().
    
    Args:
        models: List of model identifiers
        messages: List of message dicts with 'role' and 'content'
        api_key: OpenRouter API key (uses config default if not provided)
        timeout: Request timeout in seconds per model (default: 120s)
    
    Returns:
        Dictionary mapping model IDs to their responses.
        Failed requests will have None as their value.
    
    Requirements: 3.1, 3.4
    """
    logger.info(f"Querying {len(models)} models in parallel")
    
    # Create tasks for all models
    tasks = [
        query_model(model, messages, api_key, timeout)
        for model in models
    ]
    
    # Execute all queries concurrently
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Build result dictionary, handling exceptions
    results = {}
    for model, response in zip(models, responses):
        if isinstance(response, Exception):
            logger.error(f"Exception querying model {model}: {str(response)}")
            results[model] = None
        else:
            results[model] = response
    
    # Log summary
    successful = sum(1 for r in results.values() if r is not None)
    logger.info(f"Completed parallel queries: {successful}/{len(models)} successful")
    
    return results
