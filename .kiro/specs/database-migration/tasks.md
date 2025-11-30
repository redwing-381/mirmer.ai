# Implementation Plan

- [x] 1. Set up database dependencies and configuration
  - Add SQLAlchemy and psycopg2-binary to backend/requirements.txt
  - Create backend/database.py with database connection setup and session management
  - Implement connection pooling with pool_size=5 and max_overflow=10
  - Add DATABASE_URL environment variable support
  - _Requirements: 2.1, 2.5_

- [x] 2. Create database models
  - [x] 2.1 Create backend/models.py with SQLAlchemy Base
    - Define Conversation model with id, user_id, title, created_at, updated_at columns
    - Define Message model with id, conversation_id, role, content, stage1_data, stage2_data, stage3_data, metadata columns
    - Define Usage model with user_id, tier, daily_used, daily_limit, monthly_used, monthly_limit, total_queries columns
    - Set up relationships between Conversation and Message models
    - _Requirements: 1.1, 4.1, 4.2_
  
  - [x] 2.2 Add database indexes for performance
    - Create index on conversations.user_id
    - Create composite index on conversations(user_id, created_at DESC)
    - Create index on messages.conversation_id
    - Create unique index on usage.user_id
    - _Requirements: 6.2_

- [x] 3. Implement PostgreSQL storage backend
  - [x] 3.1 Create backend/storage_postgres.py with database operations
    - Implement create_conversation() function using SQLAlchemy session
    - Implement get_conversation() function with message eager loading
    - Implement list_conversations() function with user_id filtering and date sorting
    - Implement delete_conversation() function with cascade delete
    - _Requirements: 1.1, 1.3, 1.5_
  
  - [x] 3.2 Implement message operations
    - Implement add_user_message() function to create Message records
    - Implement add_assistant_message() function with stage data as JSON columns
    - Implement update_conversation_title() function
    - Add error handling and transaction rollback for all operations
    - _Requirements: 1.4, 2.5_

- [x] 4. Implement usage tracking in PostgreSQL
  - Create backend/usage_postgres.py with database-backed usage functions
  - Implement get_usage_stats() function to query Usage table
  - Implement increment_usage() function with atomic updates
  - Implement check_rate_limit() function with daily/monthly limit checks
  - Add automatic daily and monthly reset logic based on last_reset dates
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 5. Rename existing storage to JSON backend
  - Rename backend/storage.py to backend/storage_json.py
  - Rename backend/usage.py to backend/usage_json.py
  - Keep all existing functions unchanged for backward compatibility
  - _Requirements: 2.2, 2.3_

- [x] 6. Create storage factory with automatic backend selection
  - Create new backend/storage.py that detects DATABASE_URL environment variable
  - Import from storage_postgres when DATABASE_URL is present
  - Import from storage_json when DATABASE_URL is absent
  - Log which storage backend is being used on module import
  - Create new backend/usage.py with same detection logic
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 7. Initialize database on application startup
  - Update backend/main.py to call init_db() on startup when using PostgreSQL
  - Add startup event handler to create tables if they don't exist
  - Log database initialization status
  - Handle database connection errors gracefully
  - _Requirements: 3.1, 3.2, 3.4_

- [x] 8. Add Railway PostgreSQL database
  - Document steps to add PostgreSQL in Railway dashboard
  - Verify DATABASE_URL environment variable is automatically set
  - Update deployment documentation with database setup instructions
  - _Requirements: 2.1_

- [x] 9. Test PostgreSQL storage backend
  - Deploy to Railway with PostgreSQL enabled
  - Test creating conversations and messages
  - Test listing conversations for a user
  - Test deleting conversations
  - Test usage tracking and rate limiting
  - Verify data persists after Railway service restart
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 4.1, 4.4_

- [x] 10. Create migration script for existing data
  - Create backend/migrate_to_postgres.py script
  - Implement function to scan data/ directory for JSON files
  - Implement function to read and parse conversation JSON files
  - Implement function to create Conversation and Message records from JSON data
  - Implement function to migrate usage statistics
  - Add progress reporting and error handling
  - Add --backup flag to backup JSON files before migration
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 11. Update documentation
  - Update README.md with database setup instructions
  - Document environment variables (DATABASE_URL)
  - Add troubleshooting section for database connection issues
  - Document migration script usage
  - _Requirements: 2.4, 3.5_

- [x] 12. Add database monitoring and logging
  - Add slow query logging (queries > 1 second)
  - Log connection pool metrics
  - Add error logging with context (user_id, conversation_id)
  - Document monitoring in Railway dashboard
  - _Requirements: 6.5_
