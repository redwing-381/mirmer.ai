#!/usr/bin/env python3
"""
Migration script to move data from JSON files to PostgreSQL database.

Usage:
    python migrate_to_postgres.py [--backup] [--dry-run]

Options:
    --backup    Create backup of JSON files before migration
    --dry-run   Show what would be migrated without actually doing it
"""
import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db, check_connection
from models import Conversation, Message, Usage


def backup_data_directory(data_dir: str = "data") -> str:
    """Create a backup of the data directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{data_dir}_backup_{timestamp}"
    
    print(f"📦 Creating backup: {backup_dir}")
    shutil.copytree(data_dir, backup_dir)
    print(f"✓ Backup created successfully")
    
    return backup_dir


def migrate_conversations(session, user_id: str, user_dir: Path, dry_run: bool = False) -> tuple:
    """
    Migrate conversations for a specific user.
    
    Returns:
        (success_count, error_count, errors)
    """
    success_count = 0
    error_count = 0
    errors = []
    
    # Find all conversation JSON files
    json_files = list(user_dir.glob("*.json"))
    
    if not json_files:
        return 0, 0, []
    
    print(f"\n  Found {len(json_files)} conversations for user {user_id}")
    
    for json_file in json_files:
        try:
            # Read conversation from JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                conv_data = json.load(f)
            
            conversation_id = conv_data.get('id')
            if not conversation_id:
                raise ValueError(f"No ID in conversation file: {json_file}")
            
            if dry_run:
                print(f"    [DRY RUN] Would migrate: {conversation_id} - {conv_data.get('title', 'Untitled')}")
                success_count += 1
                continue
            
            # Check if conversation already exists
            existing = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if existing:
                print(f"    ⊘ Skipping (already exists): {conversation_id}")
                continue
            
            # Create conversation record
            db_conversation = Conversation(
                id=conversation_id,
                user_id=conv_data.get('user_id', user_id),
                title=conv_data.get('title', 'New Conversation'),
                created_at=datetime.fromisoformat(conv_data.get('created_at', datetime.utcnow().isoformat()))
            )
            session.add(db_conversation)
            
            # Migrate messages
            messages = conv_data.get('messages', [])
            for msg in messages:
                if msg.get('role') == 'user':
                    db_message = Message(
                        conversation_id=conversation_id,
                        role='user',
                        content=msg.get('content', '')
                    )
                else:  # assistant
                    db_message = Message(
                        conversation_id=conversation_id,
                        role='assistant',
                        stage1_data=msg.get('stage1', []),
                        stage2_data=msg.get('stage2', []),
                        stage3_data=msg.get('stage3', {}),
                        message_metadata=msg.get('metadata', {})
                    )
                session.add(db_message)
            
            session.commit()
            print(f"    ✓ Migrated: {conversation_id} ({len(messages)} messages)")
            success_count += 1
            
        except Exception as e:
            error_count += 1
            error_msg = f"Error migrating {json_file}: {str(e)}"
            errors.append(error_msg)
            print(f"    ✗ {error_msg}")
            session.rollback()
    
    return success_count, error_count, errors


def migrate_usage(session, user_id: str, usage_file: Path, dry_run: bool = False) -> bool:
    """Migrate usage statistics for a user."""
    try:
        with open(usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)
        
        if dry_run:
            print(f"    [DRY RUN] Would migrate usage for: {user_id}")
            return True
        
        # Check if usage already exists
        existing = session.query(Usage).filter(Usage.user_id == user_id).first()
        if existing:
            print(f"    ⊘ Skipping usage (already exists): {user_id}")
            return True
        
        # Create usage record
        db_usage = Usage(
            user_id=user_id,
            tier=usage_data.get('tier', 'free'),
            daily_used=usage_data.get('daily_count', 0),
            daily_limit=10 if usage_data.get('tier', 'free') == 'free' else 100,
            monthly_used=usage_data.get('monthly_count', 0),
            monthly_limit=100 if usage_data.get('tier', 'free') == 'free' else 3000,
            total_queries=usage_data.get('total_queries', 0)
        )
        session.add(db_usage)
        session.commit()
        
        print(f"    ✓ Migrated usage: {user_id} ({db_usage.total_queries} total queries)")
        return True
        
    except Exception as e:
        print(f"    ✗ Error migrating usage for {user_id}: {str(e)}")
        session.rollback()
        return False


def main():
    parser = argparse.ArgumentParser(description='Migrate JSON data to PostgreSQL')
    parser.add_argument('--backup', action='store_true', help='Create backup before migration')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be migrated without doing it')
    args = parser.parse_args()
    
    print("=" * 60)
    print("PostgreSQL Migration Script")
    print("=" * 60)
    
    # Check if DATABASE_URL is set
    if not os.getenv('DATABASE_URL'):
        print("\n❌ ERROR: DATABASE_URL environment variable not set!")
        print("This script requires a PostgreSQL database connection.")
        print("\nSet DATABASE_URL and try again:")
        print("  export DATABASE_URL='postgresql://user:pass@host:port/db'")
        sys.exit(1)
    
    # Check database connection
    print("\n🔍 Checking database connection...")
    if not check_connection():
        print("❌ ERROR: Cannot connect to database!")
        sys.exit(1)
    print("✓ Database connection successful")
    
    # Initialize database tables
    print("\n🔧 Initializing database tables...")
    if not init_db():
        print("❌ ERROR: Failed to initialize database!")
        sys.exit(1)
    print("✓ Database tables ready")
    
    # Check if data directory exists
    data_dir = Path("data")
    if not data_dir.exists():
        print(f"\n⚠️  No data directory found at: {data_dir}")
        print("Nothing to migrate.")
        sys.exit(0)
    
    # Create backup if requested
    if args.backup and not args.dry_run:
        backup_data_directory(str(data_dir))
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made")
    
    # Start migration
    print("\n" + "=" * 60)
    print("Starting Migration")
    print("=" * 60)
    
    session = SessionLocal()
    total_conversations = 0
    total_errors = 0
    all_errors = []
    
    try:
        # Migrate conversations for each user
        user_dirs = [d for d in data_dir.iterdir() if d.is_dir() and d.name != 'usage']
        
        if not user_dirs:
            print("\n⚠️  No user directories found")
        
        for user_dir in user_dirs:
            user_id = user_dir.name
            print(f"\n👤 Processing user: {user_id}")
            
            # Migrate conversations
            success, errors, error_msgs = migrate_conversations(
                session, user_id, user_dir, args.dry_run
            )
            total_conversations += success
            total_errors += errors
            all_errors.extend(error_msgs)
        
        # Migrate usage statistics
        usage_dir = data_dir / "usage"
        if usage_dir.exists():
            print(f"\n📊 Processing usage statistics...")
            for user_usage_dir in usage_dir.iterdir():
                if user_usage_dir.is_dir():
                    user_id = user_usage_dir.name
                    usage_file = user_usage_dir / "usage.json"
                    if usage_file.exists():
                        migrate_usage(session, user_id, usage_file, args.dry_run)
        
    finally:
        session.close()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Migration Summary")
    print("=" * 60)
    
    if args.dry_run:
        print(f"\n[DRY RUN] Would migrate:")
    else:
        print(f"\n✓ Successfully migrated:")
    
    print(f"  • {total_conversations} conversations")
    
    if total_errors > 0:
        print(f"\n✗ Errors: {total_errors}")
        print("\nError details:")
        for error in all_errors[:10]:  # Show first 10 errors
            print(f"  • {error}")
        if len(all_errors) > 10:
            print(f"  ... and {len(all_errors) - 10} more errors")
    
    if not args.dry_run:
        print("\n✅ Migration complete!")
        print("\nYour data is now in PostgreSQL.")
        print("You can safely keep the JSON files as backup.")
    else:
        print("\n💡 Run without --dry-run to perform actual migration")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
