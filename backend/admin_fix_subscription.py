"""
Direct database update script for Railway.
Run this on Railway to manually upgrade a user.

Usage on Railway:
    python admin_fix_subscription.py wwpSnryTr0gAA4lPlSePo1oXsSI2
"""
import sys
import os
from datetime import datetime

# This will work on Railway where DATABASE_URL is set
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not set. This script must run on Railway.")
    sys.exit(1)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create engine directly
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def fix_user(user_id: str):
    """Fix user subscription directly."""
    session = Session()
    
    try:
        # Update using raw SQL for simplicity
        result = session.execute(
            text("""
                UPDATE usage 
                SET tier = 'pro',
                    daily_limit = 100,
                    monthly_limit = 3000,
                    subscription_status = 'active',
                    updated_at = :now
                WHERE user_id = :user_id
                RETURNING tier, daily_limit, monthly_limit, subscription_status
            """),
            {"user_id": user_id, "now": datetime.utcnow()}
        )
        
        row = result.fetchone()
        
        if row:
            session.commit()
            print("=" * 60)
            print("✅ User upgraded successfully!")
            print("=" * 60)
            print(f"User ID: {user_id}")
            print(f"Tier: {row[0]}")
            print(f"Daily Limit: {row[1]}")
            print(f"Monthly Limit: {row[2]}")
            print(f"Status: {row[3]}")
            print("=" * 60)
            return True
        else:
            print(f"❌ User not found: {user_id}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python admin_fix_subscription.py <user_id>")
        print("\nExample:")
        print("  python admin_fix_subscription.py wwpSnryTr0gAA4lPlSePo1oXsSI2")
        sys.exit(1)
    
    user_id = sys.argv[1]
    print("🔧 Fixing subscription for:", user_id)
    
    success = fix_user(user_id)
    sys.exit(0 if success else 1)
