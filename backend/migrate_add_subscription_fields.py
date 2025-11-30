"""
Migration script to add subscription fields to the usage table.
Run this after updating the models.py file.
"""
import os
from sqlalchemy import text
from database import engine, check_connection

def migrate():
    """Add subscription fields to usage table."""
    
    if not check_connection():
        print("❌ Database connection failed")
        return False
    
    print("🔧 Adding subscription fields to usage table...")
    
    migrations = [
        "ALTER TABLE usage ADD COLUMN IF NOT EXISTS razorpay_subscription_id VARCHAR(128)",
        "ALTER TABLE usage ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20)",
        "CREATE INDEX IF NOT EXISTS idx_usage_razorpay_subscription ON usage(razorpay_subscription_id)",
    ]
    
    try:
        with engine.connect() as conn:
            for migration_sql in migrations:
                print(f"  Executing: {migration_sql[:60]}...")
                conn.execute(text(migration_sql))
                conn.commit()
        
        print("✅ Migration completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    migrate()
