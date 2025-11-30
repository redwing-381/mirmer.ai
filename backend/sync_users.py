#!/usr/bin/env python3
"""
Script to sync Firebase users to PostgreSQL.
This ensures all Firebase users have a usage record in the database.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Usage
from datetime import datetime

def sync_user_to_db(user_id: str, email: str = None):
    """
    Create or update a user's usage record in PostgreSQL.
    
    Args:
        user_id: Firebase user ID
        email: Optional user email for logging
    """
    with SessionLocal() as session:
        try:
            # Check if user already exists
            usage = session.query(Usage).filter(Usage.user_id == user_id).first()
            
            if usage:
                print(f"✓ User {user_id} ({email}) already exists in database")
                return True
            
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
            
            print(f"✅ Created usage record for user {user_id} ({email})")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error syncing user {user_id}: {e}")
            return False


def main():
    """
    Main function to sync users.
    You can either:
    1. Provide user IDs as command line arguments
    2. Or manually add them in this script
    """
    print("🔄 Syncing Firebase users to PostgreSQL...")
    print()
    
    # Option 1: Get user IDs from command line
    if len(sys.argv) > 1:
        user_ids = sys.argv[1:]
        print(f"Syncing {len(user_ids)} users from command line arguments...")
        for user_id in user_ids:
            sync_user_to_db(user_id)
    
    # Option 2: Manually add user IDs here
    else:
        print("No user IDs provided.")
        print()
        print("Usage:")
        print("  python sync_users.py <user_id1> <user_id2> ...")
        print()
        print("Example:")
        print("  python sync_users.py abc123 def456 ghi789")
        print()
        print("Or edit this script and add user IDs to the manual_user_ids list below:")
        print()
        
        # Add your user IDs here:
        manual_user_ids = [
            # "user_id_1",
            # "user_id_2",
            # "user_id_3",
        ]
        
        if manual_user_ids:
            print(f"Syncing {len(manual_user_ids)} users from manual list...")
            for user_id in manual_user_ids:
                sync_user_to_db(user_id)
        else:
            print("No manual user IDs configured.")
            return
    
    print()
    print("✅ Sync complete!")


if __name__ == "__main__":
    main()
