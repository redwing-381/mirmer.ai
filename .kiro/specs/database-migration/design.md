# Database Migration Design Document

## Overview

This design outlines the migration from JSON file-based storage to Railway's PostgreSQL database for persistent data storage. The implementation will use SQLAlchemy ORM for database operations and maintain backward compatibility with the existing storage interface.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│         Backend Application             │
│  ┌───────────────────────────────────┐  │
│  │      Storage Interface            │  │
│  │  (storage.py - unchanged API)     │  │
│  └───────────┬───────────────────────┘  │
│              │                           │
│      ┌───────┴────────┐                 │
│      │                │                 │
│  ┌───▼────┐    ┌─────▼──────┐          │
│  │  JSON  │    │ PostgreSQL │          │
│  │ Storage│    │  Storage   │          │
│  │(local) │    │(production)│          │
│  └────────┘    └─────┬──────┘          │
│                      │                  │
└──────────────────────┼──────────────────┘
                       │
              ┌────────▼─────────┐
              │ Railway          │
              │ PostgreSQL       │
              │ Database         │
              └──────────────────┘
```

### Storage Backend Selection

The system will automatically select the appropriate storage backend:

1. **Check for DATABASE_URL** environment variable
2. **If present**: Use PostgreSQL storage
3. **If absent**: Use JSON file storage (local development)

## Components and Interfaces

### 1. Database Models (models.py)

**Purpose**: Define SQLAlchemy ORM models for database tables

**Tables**:

#### Conversations Table
```python
class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(String(36), primary_key=True)  # UUID
    user_id = Column(String(128), nullable=False, index=True)
    title = Column(String(500), default='New Conversation')
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to messages
    messages = relationship('Message', back_populates='conversation', cascade='all, delete-orphan')
```

#### Messages Table
```python
class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=True)  # For user messages
    stage1_data = Column(JSON, nullable=True)  # For assistant messages
    stage2_data = Column(JSON, nullable=True)
    stage3_data = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship to conversation
    conversation = relationship('Conversation', back_populates='messages')
```

#### Usage Table
```python
class Usage(Base):
    __tablename__ = 'usage'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(128), unique=True, nullable=False, index=True)
    tier = Column(String(20), default='free')  # 'free', 'pro', 'enterprise'
    daily_used = Column(Integer, default=0)
    daily_limit = Column(Integer, default=10)
    monthly_used = Column(Integer, default=0)
    monthly_limit = Column(Integer, default=100)
    total_queries = Column(Integer, default=0)
    last_reset_daily = Column(Date, default=datetime.utcnow().date)
    last_reset_monthly = Column(Date, default=datetime.utcnow().date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 2. Database Connection (database.py)

**Purpose**: Manage database connection and session lifecycle

**Key Components**:

```python
# Database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)
```

**Connection Pooling**:
- Pool size: 5 connections
- Max overflow: 10 additional connections
- Pre-ping: Verify connection health before use
- Automatic reconnection on connection loss

### 3. PostgreSQL Storage Backend (storage_postgres.py)

**Purpose**: Implement storage interface using PostgreSQL

**Key Functions**:

```python
def create_conversation(user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]
def get_conversation(conversation_id: str, user_id: str) -> Optional[Dict[str, Any]]
def save_conversation(conversation: Dict[str, Any], user_id: str) -> bool
def list_conversations(user_id: str) -> List[Dict[str, Any]]
def add_user_message(conversation_id: str, content: str, user_id: str) -> bool
def add_assistant_message(conversation_id: str, stage1, stage2, stage3, user_id: str, metadata=None) -> bool
def update_conversation_title(conversation_id: str, title: str, user_id: str) -> bool
def delete_conversation(conversation_id: str, user_id: str) -> bool
```

**Implementation Pattern**:
```python
def create_conversation(user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    with SessionLocal() as session:
        try:
            if conversation_id is None:
                conversation_id = str(uuid.uuid4())
            
            db_conversation = Conversation(
                id=conversation_id,
                user_id=user_id,
                title='New Conversation'
            )
            
            session.add(db_conversation)
            session.commit()
            session.refresh(db_conversation)
            
            return {
                'id': db_conversation.id,
                'user_id': db_conversation.user_id,
                'title': db_conversation.title,
                'created_at': db_conversation.created_at.isoformat(),
                'messages': []
            }
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating conversation: {e}")
            raise
```

### 4. Storage Factory (storage.py - updated)

**Purpose**: Automatically select and initialize the appropriate storage backend

**Implementation**:

```python
import os
import logging

logger = logging.getLogger(__name__)

# Determine which storage backend to use
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    logger.info("Using PostgreSQL storage backend")
    from backend.storage_postgres import *
else:
    logger.info("Using JSON file storage backend (local development)")
    from backend.storage_json import *
```

**Benefits**:
- Zero code changes in main.py
- Automatic backend selection
- Easy local development (no database required)
- Production uses PostgreSQL automatically

### 5. Migration Script (migrate_to_postgres.py)

**Purpose**: Migrate existing JSON data to PostgreSQL

**Process**:
1. Connect to PostgreSQL database
2. Scan data/ directory for user folders
3. For each user:
   - Read all conversation JSON files
   - Create conversation records in database
   - Create message records for each message
   - Migrate usage statistics
4. Report progress and errors
5. Optionally backup JSON files

**Usage**:
```bash
python migrate_to_postgres.py --backup
```

## Data Models

### Conversation Data Structure

**JSON Format** (current):
```json
{
  "id": "uuid",
  "user_id": "firebase_uid",
  "title": "Conversation title",
  "created_at": "2024-01-01T00:00:00",
  "messages": [
    {
      "role": "user",
      "content": "User message"
    },
    {
      "role": "assistant",
      "stage1": [...],
      "stage2": [...],
      "stage3": {...},
      "metadata": {...}
    }
  ]
}
```

**Database Format**:
- Conversation record in `conversations` table
- Each message as separate record in `messages` table
- JSON columns for stage data (stage1, stage2, stage3, metadata)

### Usage Data Structure

**JSON Format** (current):
```json
{
  "user_id": "firebase_uid",
  "tier": "free",
  "daily_used": 5,
  "daily_limit": 10,
  "monthly_used": 50,
  "monthly_limit": 100,
  "total_queries": 150,
  "last_reset_daily": "2024-01-01",
  "last_reset_monthly": "2024-01-01"
}
```

**Database Format**:
- Single record per user in `usage` table
- Automatic timestamp tracking
- Indexed by user_id for fast lookups

## Error Handling

### Database Connection Errors

**Scenario**: Database is unavailable or connection fails

**Handling**:
1. Log error with full details
2. If in production (DATABASE_URL set), raise exception
3. If in development, fall back to JSON storage
4. Retry connection with exponential backoff

### Transaction Errors

**Scenario**: Database operation fails mid-transaction

**Handling**:
1. Automatic rollback via SQLAlchemy session
2. Log error with context (user_id, conversation_id)
3. Return False or None to indicate failure
4. Preserve data integrity (no partial writes)

### Migration Errors

**Scenario**: Error during JSON to PostgreSQL migration

**Handling**:
1. Continue processing other files
2. Log each error with file path
3. Generate error report at end
4. Keep JSON files intact (no deletion on error)

## Performance Optimization

### Database Indexes

```sql
-- User-based queries
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_usage_user_id ON usage(user_id);

-- Composite index for user conversations sorted by date
CREATE INDEX idx_conversations_user_created ON conversations(user_id, created_at DESC);
```

### Connection Pooling

- **Pool size**: 5 persistent connections
- **Max overflow**: 10 additional connections during peak load
- **Pre-ping**: Verify connection health before use
- **Automatic cleanup**: Close idle connections

### Query Optimization

- **Eager loading**: Load messages with conversations when needed
- **Pagination**: Limit conversation list queries (e.g., 50 most recent)
- **Selective fields**: Only load required columns
- **Prepared statements**: SQLAlchemy automatically uses prepared statements

## Testing Strategy

### Unit Tests

- Test each storage function independently
- Mock database connections
- Test error handling and rollback
- Verify data integrity

### Integration Tests

- Test with real PostgreSQL database (test instance)
- Test migration script with sample data
- Test concurrent access from multiple users
- Test connection pool behavior under load

### Migration Testing

- Create test JSON data
- Run migration script
- Verify all data migrated correctly
- Test application with migrated data
- Verify no data loss

## Deployment Steps

### 1. Add PostgreSQL to Railway

1. Go to Railway project dashboard
2. Click "New" → "Database" → "PostgreSQL"
3. Railway automatically sets `DATABASE_URL` environment variable
4. Note the database credentials (for local testing)

### 2. Update Backend Dependencies

Add to `backend/requirements.txt`:
```
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
```

### 3. Deploy Updated Code

1. Push code with new storage backend
2. Railway automatically redeploys
3. Database tables created automatically on first run
4. Verify logs show "Using PostgreSQL storage backend"

### 4. Migrate Existing Data (if any)

If you have existing JSON data to preserve:
1. Run migration script locally
2. Or run as one-time Railway deployment job

### 5. Test Production

1. Sign in to deployed app
2. Create new conversation
3. Restart Railway service
4. Verify conversation persists

## Backward Compatibility

### Local Development

- No DATABASE_URL → Uses JSON storage
- Developers can work without PostgreSQL
- Same API interface, different backend

### Gradual Migration

- Can run both backends simultaneously
- Migration script can run multiple times safely
- No downtime required

## Security Considerations

### Database Access

- DATABASE_URL contains credentials
- Never log or expose DATABASE_URL
- Use Railway's environment variables (encrypted)
- Restrict database access to Railway network

### SQL Injection Prevention

- SQLAlchemy ORM prevents SQL injection
- All queries use parameterized statements
- No raw SQL queries with user input

### User Data Isolation

- All queries filtered by user_id
- Database-level constraints prevent cross-user access
- Verify user_id in every query

## Monitoring and Logging

### Database Metrics

- Connection pool usage
- Query execution time
- Failed queries
- Connection errors

### Application Logs

- Storage backend selection
- Database initialization
- Migration progress
- Error details with context

### Railway Dashboard

- Database size and growth
- Connection count
- Query performance
- Backup status

## Future Enhancements

1. **Read Replicas**: Add read replicas for scaling
2. **Caching**: Add Redis for frequently accessed data
3. **Full-Text Search**: Add PostgreSQL full-text search for conversations
4. **Backup Automation**: Automated daily backups
5. **Analytics**: Query patterns and usage analytics
6. **Archival**: Move old conversations to cold storage
