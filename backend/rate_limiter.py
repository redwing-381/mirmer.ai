"""
Adaptive rate limiter for OpenRouter API calls.

Manages rate limiting with adaptive delays based on API responses,
exponential backoff for rate limit errors, and jitter to prevent thundering herd.
"""
import asyncio
import logging
import random
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class AdaptiveRateLimiter:
    """
    Manages rate limiting with adaptive delays based on API responses.
    
    Features:
    - Provider-specific rate limit tracking
    - Exponential backoff with jitter for rate limit errors
    - Rate limit header parsing and adaptive delays
    - Prevents thundering herd with randomized jitter
    """
    
    def __init__(self):
        """Initialize the rate limiter with empty tracking dictionaries."""
        self.last_request_time: Dict[str, float] = {}
        self.rate_limit_info: Dict[str, Dict] = {}
        self.min_delay = 0.1  # Minimum delay between requests (100ms)
    
    async def wait_if_needed(self, provider: str) -> None:
        """
        Wait if necessary to respect rate limits for a provider.
        
        Uses actual rate limit headers when available, otherwise uses minimal delay.
        
        Args:
            provider: The API provider (e.g., "openrouter", "openai", "anthropic")
        """
        current_time = time.time()
        
        # Check if we have rate limit info for this provider
        if provider in self.rate_limit_info:
            info = self.rate_limit_info[provider]
            
            # Check if we're close to the rate limit
            if info.get("requests_remaining") is not None:
                remaining = info["requests_remaining"]
                limit = info.get("requests_limit", 100)
                
                # If we're below 10% of limit, add adaptive delay
                if remaining < limit * 0.1:
                    delay = 1.0 + random.uniform(0, 0.5)  # 1-1.5 seconds
                    logger.warning(
                        f"Rate limit low for {provider}: {remaining}/{limit} remaining. "
                        f"Adding {delay:.2f}s delay"
                    )
                    await asyncio.sleep(delay)
                    return
        
        # Ensure minimum delay between requests to same provider
        if provider in self.last_request_time:
            elapsed = current_time - self.last_request_time[provider]
            if elapsed < self.min_delay:
                wait_time = self.min_delay - elapsed
                await asyncio.sleep(wait_time)
        
        self.last_request_time[provider] = time.time()
    
    def update_from_headers(self, provider: str, headers: dict) -> None:
        """
        Update rate limit info from API response headers.
        
        Parses common rate limit headers:
        - X-RateLimit-Remaining / RateLimit-Remaining
        - X-RateLimit-Limit / RateLimit-Limit
        - X-RateLimit-Reset / RateLimit-Reset
        
        Args:
            provider: The API provider
            headers: Response headers dictionary
        """
        # Try different header formats (X- prefix and without)
        remaining = (
            headers.get("x-ratelimit-remaining") or
            headers.get("ratelimit-remaining") or
            headers.get("X-RateLimit-Remaining") or
            headers.get("RateLimit-Remaining")
        )
        
        limit = (
            headers.get("x-ratelimit-limit") or
            headers.get("ratelimit-limit") or
            headers.get("X-RateLimit-Limit") or
            headers.get("RateLimit-Limit")
        )
        
        reset = (
            headers.get("x-ratelimit-reset") or
            headers.get("ratelimit-reset") or
            headers.get("X-RateLimit-Reset") or
            headers.get("RateLimit-Reset")
        )
        
        # Update rate limit info if we found any headers
        if remaining is not None or limit is not None or reset is not None:
            self.rate_limit_info[provider] = {
                "requests_remaining": int(remaining) if remaining else None,
                "requests_limit": int(limit) if limit else None,
                "reset_time": float(reset) if reset else None,
                "last_updated": time.time()
            }
            
            if remaining is not None:
                logger.debug(
                    f"Rate limit update for {provider}: {remaining}/{limit} remaining"
                )
    
    async def handle_rate_limit_error(
        self, 
        provider: str, 
        retry_count: int,
        max_retries: int = 5
    ) -> bool:
        """
        Handle rate limit errors with exponential backoff and jitter.
        
        Implements exponential backoff: 1s, 2s, 4s, 8s, 16s
        Adds random jitter to prevent thundering herd.
        
        Args:
            provider: The API provider
            retry_count: Current retry attempt (0-indexed)
            max_retries: Maximum number of retries (default: 5)
        
        Returns:
            bool: True if should retry, False if max retries exceeded
        """
        if retry_count >= max_retries:
            logger.error(
                f"Max retries ({max_retries}) exceeded for {provider}. Giving up."
            )
            return False
        
        # Exponential backoff: 2^retry_count seconds
        base_delay = 2 ** retry_count
        
        # Add jitter: random value between 0 and base_delay/2
        jitter = random.uniform(0, base_delay / 2)
        
        total_delay = base_delay + jitter
        
        logger.warning(
            f"Rate limit hit for {provider}. Retry {retry_count + 1}/{max_retries}. "
            f"Waiting {total_delay:.2f}s (base: {base_delay}s + jitter: {jitter:.2f}s)"
        )
        
        await asyncio.sleep(total_delay)
        
        return True


# Global rate limiter instance
_rate_limiter = AdaptiveRateLimiter()


def get_rate_limiter() -> AdaptiveRateLimiter:
    """
    Get the global rate limiter instance.
    
    Returns:
        AdaptiveRateLimiter: The global rate limiter
    """
    return _rate_limiter
