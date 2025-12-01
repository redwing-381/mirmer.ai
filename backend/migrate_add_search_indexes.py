"""
Database migration to add full-text search indexes for conversation search.

This migration adds:
1. GIN index on conversation titles for fast text search
2. GIN index on message content for searching within messages
3. Composite index for efficient user-specific searches

Run with: python migrate_add_search_indexes.py
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not set. This migration only works with PostgreSQL.")
    print("For local JSON storage, search will work without indexes.")
    exit(1)

print("🔍 Adding full-text search indexes to conversations...")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    try:
        # Add GIN index for full-text search on conversation titles
        print("  → Adding GIN index on conversations.title...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_conversations_title_search 
            ON conversations USING GIN (to_tsvector('english', title))
        """))
        
        # Add GIN index for full-text search on message content
        print("  → Adding GIN index on messages.content...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_messages_content_search 
            ON messages USING GIN (to_tsvector('english', COALESCE(content, '')))
        """))
        
        # Add index for efficient conversation lookups by user
        print("  → Adding index for user-conversation lookups...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation_user 
            ON messages (conversation_id)
        """))
        
        conn.commit()
        print("✅ Search indexes added successfully!")
        print("\nIndexes created:")
        print("  - idx_conversations_title_search (GIN on title)")
        print("  - idx_messages_content_search (GIN on content)")
        print("  - idx_messages_conversation_user (conversation_id)")
        
    except Exception as e:
        print(f"❌ Error adding indexes: {e}")
        conn.rollback()
        raise

print("\n🎉 Migration complete!")
