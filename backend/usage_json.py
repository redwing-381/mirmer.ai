"""
Usage tracking and rate limiting for users (JSON-based).
"""
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

USAGE_DIR = "data/usage"

# Usage limits
FREE_TIER_DAILY_LIMIT = 10  # 10 queries per day for free users
FREE_TIER_MONTHLY_LIMIT = 100  # 100 queries per month for free users


def ensure_usage_dir(user_id: str) -> None:
    """Ensure the usage directory exists for a user."""
    user_dir = os.path.join(USAGE_DIR, user_id)
    Path(user_dir).mkdir(parents=True, exist_ok=True)


def get_usage_path(user_id: str) -> str:
    """Get the path to user's usage file."""
    return os.path.join(USAGE_DIR, user_id, "usage.json")


def get_user_usage(user_id: str) -> Dict:
    """
    Get user's usage statistics.
    
    Returns:
        Dict with daily_count, monthly_count, last_reset, etc.
    """
    ensure_usage_dir(user_id)
    path = get_usage_path(user_id)
    
    if not os.path.exists(path):
        # Initialize usage tracking
        usage = {
            "user_id": user_id,
            "daily_count": 0,
            "monthly_count": 0,
            "last_daily_reset": datetime.utcnow().date().isoformat(),
            "last_monthly_reset": datetime.utcnow().replace(day=1).date().isoformat(),
            "total_queries": 0,
            "tier": "free"  # free, pro, enterprise
        }
        save_usage(user_id, usage)
        return usage
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            usage = json.load(f)
        
        # Reset daily count if it's a new day
        today = datetime.utcnow().date().isoformat()
        if usage.get("last_daily_reset") != today:
            usage["daily_count"] = 0
            usage["last_daily_reset"] = today
        
        # Reset monthly count if it's a new month
        month_start = datetime.utcnow().replace(day=1).date().isoformat()
        if usage.get("last_monthly_reset") != month_start:
            usage["monthly_count"] = 0
            usage["last_monthly_reset"] = month_start
        
        return usage
    except Exception as e:
        logger.error(f"Error loading usage for user {user_id}: {str(e)}")
        return {
            "user_id": user_id,
            "daily_count": 0,
            "monthly_count": 0,
            "last_daily_reset": datetime.utcnow().date().isoformat(),
            "last_monthly_reset": datetime.utcnow().replace(day=1).date().isoformat(),
            "total_queries": 0,
            "tier": "free"
        }


def save_usage(user_id: str, usage: Dict) -> bool:
    """Save user's usage statistics."""
    ensure_usage_dir(user_id)
    path = get_usage_path(user_id)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(usage, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving usage for user {user_id}: {str(e)}")
        return False


def increment_usage(user_id: str) -> Dict:
    """
    Increment user's usage count.
    
    Returns:
        Updated usage dict
    """
    usage = get_user_usage(user_id)
    
    usage["daily_count"] += 1
    usage["monthly_count"] += 1
    usage["total_queries"] += 1
    
    save_usage(user_id, usage)
    logger.info(f"User {user_id} usage: {usage['daily_count']}/day, {usage['monthly_count']}/month")
    
    return usage


def check_rate_limit(user_id: str) -> tuple[bool, Optional[str]]:
    """
    Check if user has exceeded rate limits.
    
    Returns:
        (allowed: bool, error_message: Optional[str])
    """
    usage = get_user_usage(user_id)
    tier = usage.get("tier", "free")
    
    if tier == "free":
        # Check daily limit
        if usage["daily_count"] >= FREE_TIER_DAILY_LIMIT:
            return False, f"Daily limit reached ({FREE_TIER_DAILY_LIMIT} queries/day). Upgrade to Pro for unlimited queries."
        
        # Check monthly limit
        if usage["monthly_count"] >= FREE_TIER_MONTHLY_LIMIT:
            return False, f"Monthly limit reached ({FREE_TIER_MONTHLY_LIMIT} queries/month). Upgrade to Pro for unlimited queries."
    
    # Pro and enterprise tiers have no limits (for now)
    return True, None


def get_usage_stats(user_id: str) -> Dict:
    """
    Get user's usage statistics for display.
    
    Returns:
        Dict with usage info and limits
    """
    usage = get_user_usage(user_id)
    tier = usage.get("tier", "free")
    
    if tier == "free":
        return {
            "tier": "free",
            "daily_queries_used": usage["daily_count"],  # Frontend expects this field name
            "daily_used": usage["daily_count"],  # Keep for backward compatibility
            "daily_limit": FREE_TIER_DAILY_LIMIT,
            "monthly_queries_used": usage["monthly_count"],  # Frontend expects this field name
            "monthly_used": usage["monthly_count"],  # Keep for backward compatibility
            "monthly_limit": FREE_TIER_MONTHLY_LIMIT,
            "total_queries": usage["total_queries"]
        }
    
    return {
        "tier": tier,
        "daily_queries_used": usage["daily_count"],  # Frontend expects this field name
        "daily_used": usage["daily_count"],  # Keep for backward compatibility
        "daily_limit": "unlimited",
        "monthly_queries_used": usage["monthly_count"],  # Frontend expects this field name
        "monthly_used": usage["monthly_count"],  # Keep for backward compatibility
        "monthly_limit": "unlimited",
        "total_queries": usage["total_queries"]
    }
