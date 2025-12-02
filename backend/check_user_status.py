"""
Check a user's current subscription status in the database.

Usage:
    uv run python check_user_status.py <user_id>
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Usage


def check_user(user_id: str):
    """Check user's current status."""
    db = SessionLocal()
    
    try:
        usage = db.query(Usage).filter(Usage.user_id == user_id).first()
        
        if not usage:
            print(f"❌ User not found: {user_id}")
            return
        
        print("=" * 60)
        print(f"📊 User Status for: {user_id}")
        print("=" * 60)
        print(f"Tier: {usage.tier}")
        print(f"Subscription Status: {usage.subscription_status}")
        print(f"Subscription ID: {usage.razorpay_subscription_id}")
        print(f"Daily Limit: {usage.daily_limit}")
        print(f"Monthly Limit: {usage.monthly_limit}")
        print(f"Daily Used: {usage.daily_used}")
        print(f"Monthly Used: {usage.monthly_used}")
        print(f"Total Queries: {usage.total_queries}")
        print(f"Created: {usage.created_at}")
        print(f"Updated: {usage.updated_at}")
        print("=" * 60)
        
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python check_user_status.py <user_id>")
        sys.exit(1)
    
    check_user(sys.argv[1])
