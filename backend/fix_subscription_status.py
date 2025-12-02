"""
Admin script to manually fix subscription status for a user.
This is a temporary fix until the webhook handler improvements are deployed.

Usage:
    uv run python fix_subscription_status.py <user_id> <subscription_id>
"""
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import Usage


def fix_user_subscription(user_id: str, subscription_id: str = None):
    """
    Manually upgrade a user to Pro tier.
    
    Args:
        user_id: Firebase user ID
        subscription_id: Razorpay subscription ID (optional)
    """
    if not SessionLocal:
        print("❌ Database not configured. Set DATABASE_URL environment variable.")
        return False
    
    db = SessionLocal()
    
    try:
        # Find user
        usage = db.query(Usage).filter(Usage.user_id == user_id).first()
        
        if not usage:
            print(f"❌ User not found: {user_id}")
            return False
        
        print(f"📊 Current status:")
        print(f"   User ID: {user_id}")
        print(f"   Tier: {usage.tier}")
        print(f"   Daily Limit: {usage.daily_limit}")
        print(f"   Monthly Limit: {usage.monthly_limit}")
        print(f"   Subscription ID: {usage.razorpay_subscription_id}")
        print(f"   Status: {usage.subscription_status}")
        
        # Update to Pro
        print(f"\n🔄 Upgrading to Pro tier...")
        usage.tier = 'pro'
        usage.daily_limit = 100
        usage.monthly_limit = 3000
        usage.subscription_status = 'active'
        
        if subscription_id:
            usage.razorpay_subscription_id = subscription_id
        
        usage.updated_at = datetime.utcnow()
        
        db.commit()
        
        print(f"\n✅ User upgraded successfully!")
        print(f"   New Tier: {usage.tier}")
        print(f"   New Daily Limit: {usage.daily_limit}")
        print(f"   New Monthly Limit: {usage.monthly_limit}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python fix_subscription_status.py <user_id> [subscription_id]")
        print("\nExample:")
        print("  uv run python fix_subscription_status.py abc123xyz")
        print("  uv run python fix_subscription_status.py abc123xyz sub_MjQxNzY4NzY4")
        sys.exit(1)
    
    user_id = sys.argv[1]
    subscription_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 60)
    print("🔧 Mirmer AI - Manual Subscription Fix")
    print("=" * 60)
    
    success = fix_user_subscription(user_id, subscription_id)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Done! User should now see Pro tier in the app.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Failed to update user subscription.")
        print("=" * 60)
        sys.exit(1)
