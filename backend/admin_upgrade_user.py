"""
Admin script to manually upgrade a user to Pro tier.
Useful for testing or manual upgrades.
"""
import sys
from sqlalchemy.orm import Session
from database import get_db, check_connection
from models import Usage
from datetime import datetime

def upgrade_user_to_pro(user_id: str):
    """Upgrade a user to Pro tier."""
    
    if not check_connection():
        print("❌ Database connection failed")
        return False
    
    db = next(get_db())
    
    try:
        usage = db.query(Usage).filter(Usage.user_id == user_id).first()
        
        if not usage:
            print(f"❌ User {user_id} not found")
            return False
        
        print(f"Current tier: {usage.tier}")
        print(f"Current limits: {usage.daily_limit} daily, {usage.monthly_limit} monthly")
        
        # Upgrade to Pro
        usage.tier = 'pro'
        usage.daily_limit = 100
        usage.monthly_limit = 3000
        usage.subscription_status = 'active'
        usage.updated_at = datetime.utcnow()
        
        db.commit()
        
        print(f"✅ User {user_id} upgraded to Pro")
        print(f"New limits: {usage.daily_limit} daily, {usage.monthly_limit} monthly")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def downgrade_user_to_free(user_id: str):
    """Downgrade a user to Free tier."""
    
    if not check_connection():
        print("❌ Database connection failed")
        return False
    
    db = next(get_db())
    
    try:
        usage = db.query(Usage).filter(Usage.user_id == user_id).first()
        
        if not usage:
            print(f"❌ User {user_id} not found")
            return False
        
        print(f"Current tier: {usage.tier}")
        
        # Downgrade to Free
        usage.tier = 'free'
        usage.daily_limit = 10
        usage.monthly_limit = 300
        usage.subscription_status = None
        usage.stripe_customer_id = None
        usage.stripe_subscription_id = None
        usage.updated_at = datetime.utcnow()
        
        db.commit()
        
        print(f"✅ User {user_id} downgraded to Free")
        print(f"New limits: {usage.daily_limit} daily, {usage.monthly_limit} monthly")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Upgrade:   python admin_upgrade_user.py upgrade <user_id>")
        print("  Downgrade: python admin_upgrade_user.py downgrade <user_id>")
        sys.exit(1)
    
    action = sys.argv[1]
    user_id = sys.argv[2]
    
    if action == "upgrade":
        upgrade_user_to_pro(user_id)
    elif action == "downgrade":
        downgrade_user_to_free(user_id)
    else:
        print(f"❌ Unknown action: {action}")
        print("Use 'upgrade' or 'downgrade'")
        sys.exit(1)
