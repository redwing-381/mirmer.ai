"""
PostgreSQL-based usage tracking for rate limiting and statistics.
"""
import logging
from datetime import date, datetime
from typing import Dict, Tuple
from database import SessionLocal
from models import Usage

logger = logging.getLogger(__name__)

# Tier limits
TIER_LIMITS = {
    'free': {
        'daily': 10,
        'monthly': 100
    },
    'pro': {
        'daily': 100,
        'monthly': 3000
    },
    'enterprise': {
        'daily': 'unlimited',
        'monthly': 'unlimited'
    }
}


def get_or_create_usage(user_id: str) -> Usage:
    """
    Get existing usage record or create new one for user.
    
    Args:
        user_id: Firebase user ID
    
    Returns:
        Usage model instance
    """
    with SessionLocal() as session:
        usage = session.query(Usage).filter(Usage.user_id == user_id).first()
        
        if not usage:
            # Create new usage record
            usage = Usage(
                user_id=user_id,
                tier='free',
                daily_used=0,
                daily_limit=10,
                monthly_used=0,
                monthly_limit=100,
                total_queries=0
            )
            session.add(usage)
            session.commit()
            session.refresh(usage)
            logger.info(f"Created usage record for user: {user_id}")
        
        return usage


def reset_if_needed(usage: Usage, session) -> None:
    """
    Reset daily/monthly counters if needed based on dates.
    
    Args:
        usage: Usage model instance
        session: SQLAlchemy session
    """
    today = date.today()
    modified = False
    
    # Check if daily reset is needed
    if usage.last_reset_daily < today:
        usage.daily_used = 0
        usage.last_reset_daily = today
        modified = True
        logger.info(f"Reset daily usage for user: {usage.user_id}")
    
    # Check if monthly reset is needed (first day of month)
    if usage.last_reset_monthly.month != today.month or usage.last_reset_monthly.year != today.year:
        usage.monthly_used = 0
        usage.last_reset_monthly = today
        modified = True
        logger.info(f"Reset monthly usage for user: {usage.user_id}")
    
    if modified:
        session.commit()


def get_usage_stats(user_id: str) -> Dict:
    """
    Get usage statistics for a user.
    
    Args:
        user_id: Firebase user ID
    
    Returns:
        Dictionary with usage stats
    """
    with SessionLocal() as session:
        try:
            usage = session.query(Usage).filter(Usage.user_id == user_id).first()
            
            if not usage:
                # Create new usage record
                logger.info(f"🆕 Creating new usage record for user: {user_id}")
                usage = Usage(
                    user_id=user_id,
                    tier='free',
                    daily_used=0,
                    daily_limit=10,
                    monthly_used=0,
                    monthly_limit=100,
                    total_queries=0
                )
                session.add(usage)
                session.commit()
                session.refresh(usage)
                logger.info(f"✅ Created usage record for user: {user_id}")
            
            # Reset counters if needed
            reset_if_needed(usage, session)
            
            # Refresh to get updated values
            session.refresh(usage)
            
            stats = {
                'user_id': usage.user_id,
                'tier': usage.tier,
                'daily_used': usage.daily_used,
                'daily_limit': usage.daily_limit if usage.tier == 'free' else 'unlimited',
                'monthly_used': usage.monthly_used,
                'monthly_limit': usage.monthly_limit if usage.tier == 'free' else 'unlimited',
                'total_queries': usage.total_queries
            }
            logger.info(f"📊 Usage stats for {user_id}: daily={stats['daily_used']}/{stats['daily_limit']}, monthly={stats['monthly_used']}/{stats['monthly_limit']}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting usage stats for {user_id}: {e}")
            # Return default stats on error
            return {
                'user_id': user_id,
                'tier': 'free',
                'daily_used': 0,
                'daily_limit': 10,
                'monthly_used': 0,
                'monthly_limit': 100,
                'total_queries': 0
            }


def increment_usage(user_id: str) -> bool:
    """
    Increment usage counters for a user.
    
    Args:
        user_id: Firebase user ID
    
    Returns:
        True if successful, False otherwise
    """
    with SessionLocal() as session:
        try:
            usage = session.query(Usage).filter(Usage.user_id == user_id).first()
            
            if not usage:
                # Create new usage record
                usage = Usage(
                    user_id=user_id,
                    tier='free',
                    daily_used=0,
                    daily_limit=10,
                    monthly_used=0,
                    monthly_limit=100,
                    total_queries=0
                )
                session.add(usage)
            
            # Reset counters if needed
            reset_if_needed(usage, session)
            
            # Increment counters
            usage.daily_used += 1
            usage.monthly_used += 1
            usage.total_queries += 1
            usage.updated_at = datetime.utcnow()
            
            session.commit()
            logger.info(f"✅ Incremented usage for user: {user_id} (daily: {usage.daily_used}, monthly: {usage.monthly_used}, total: {usage.total_queries})")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error incrementing usage for {user_id}: {e}")
            return False


def check_rate_limit(user_id: str) -> Tuple[bool, str]:
    """
    Check if user has exceeded rate limits.
    
    Args:
        user_id: Firebase user ID
    
    Returns:
        Tuple of (allowed: bool, error_message: str)
    """
    with SessionLocal() as session:
        try:
            usage = session.query(Usage).filter(Usage.user_id == user_id).first()
            
            if not usage:
                # New user - create record and allow
                usage = Usage(
                    user_id=user_id,
                    tier='free',
                    daily_used=0,
                    daily_limit=10,
                    monthly_used=0,
                    monthly_limit=100,
                    total_queries=0
                )
                session.add(usage)
                session.commit()
                return (True, "")
            
            # Reset counters if needed
            reset_if_needed(usage, session)
            session.refresh(usage)
            
            # Check limits based on tier
            if usage.tier == 'enterprise':
                return (True, "")
            
            # Check daily limit
            if usage.daily_used >= usage.daily_limit:
                return (False, f"Daily limit reached ({usage.daily_limit} queries/day). Upgrade to Pro for more queries.")
            
            # Check monthly limit
            if usage.monthly_used >= usage.monthly_limit:
                return (False, f"Monthly limit reached ({usage.monthly_limit} queries/month). Upgrade to Pro for more queries.")
            
            return (True, "")
            
        except Exception as e:
            logger.error(f"Error checking rate limit for {user_id}: {e}")
            # Allow on error to avoid blocking users
            return (True, "")


def update_tier(user_id: str, new_tier: str) -> bool:
    """
    Update user's subscription tier.
    
    Args:
        user_id: Firebase user ID
        new_tier: New tier ('free', 'pro', 'enterprise')
    
    Returns:
        True if successful, False otherwise
    """
    if new_tier not in TIER_LIMITS:
        logger.error(f"Invalid tier: {new_tier}")
        return False
    
    with SessionLocal() as session:
        try:
            usage = session.query(Usage).filter(Usage.user_id == user_id).first()
            
            if not usage:
                # Create new usage record with specified tier
                limits = TIER_LIMITS[new_tier]
                usage = Usage(
                    user_id=user_id,
                    tier=new_tier,
                    daily_used=0,
                    daily_limit=limits['daily'] if limits['daily'] != 'unlimited' else 999999,
                    monthly_used=0,
                    monthly_limit=limits['monthly'] if limits['monthly'] != 'unlimited' else 999999,
                    total_queries=0
                )
                session.add(usage)
            else:
                # Update existing record
                usage.tier = new_tier
                limits = TIER_LIMITS[new_tier]
                usage.daily_limit = limits['daily'] if limits['daily'] != 'unlimited' else 999999
                usage.monthly_limit = limits['monthly'] if limits['monthly'] != 'unlimited' else 999999
                usage.updated_at = datetime.utcnow()
            
            session.commit()
            logger.info(f"Updated tier for user {user_id} to {new_tier}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating tier for {user_id}: {e}")
            return False
