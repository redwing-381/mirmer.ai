"""
SQLAlchemy database models for PostgreSQL storage.
"""
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Text, DateTime, Date, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.database import Base


class Conversation(Base):
    """
    Conversation model - stores conversation metadata.
    Each conversation belongs to a user and contains multiple messages.
    """
    __tablename__ = 'conversations'
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # User association
    user_id = Column(String(128), nullable=False, index=True)
    
    # Conversation metadata
    title = Column(String(500), default='New Conversation', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to messages (cascade delete)
    messages = relationship(
        'Message',
        back_populates='conversation',
        cascade='all, delete-orphan',
        order_by='Message.created_at'
    )
    
    # Composite index for efficient user queries sorted by date
    __table_args__ = (
        Index('idx_conversations_user_created', 'user_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Conversation(id='{self.id}', user_id='{self.user_id}', title='{self.title}')>"


class Message(Base):
    """
    Message model - stores individual messages within conversations.
    Supports both user messages (text) and assistant messages (stage data).
    """
    __tablename__ = 'messages'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to conversation
    conversation_id = Column(
        String(36),
        ForeignKey('conversations.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Message metadata
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # User message content
    content = Column(Text, nullable=True)  # Only for user messages
    
    # Assistant message data (stored as JSON)
    stage1_data = Column(JSON, nullable=True)  # Stage 1: Individual responses
    stage2_data = Column(JSON, nullable=True)  # Stage 2: Rankings
    stage3_data = Column(JSON, nullable=True)  # Stage 3: Chairman synthesis
    metadata = Column(JSON, nullable=True)     # Additional metadata
    
    # Relationship to conversation
    conversation = relationship('Conversation', back_populates='messages')
    
    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id='{self.conversation_id}', role='{self.role}')>"


class Usage(Base):
    """
    Usage model - tracks query usage and limits per user.
    Stores daily, monthly, and total query counts with automatic resets.
    """
    __tablename__ = 'usage'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # User association (unique - one record per user)
    user_id = Column(String(128), unique=True, nullable=False, index=True)
    
    # Subscription tier
    tier = Column(String(20), default='free', nullable=False)  # 'free', 'pro', 'enterprise'
    
    # Usage counters
    daily_used = Column(Integer, default=0, nullable=False)
    daily_limit = Column(Integer, default=10, nullable=False)
    monthly_used = Column(Integer, default=0, nullable=False)
    monthly_limit = Column(Integer, default=100, nullable=False)
    total_queries = Column(Integer, default=0, nullable=False)
    
    # Reset tracking
    last_reset_daily = Column(Date, default=date.today, nullable=False)
    last_reset_monthly = Column(Date, default=date.today, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Usage(user_id='{self.user_id}', tier='{self.tier}', daily={self.daily_used}/{self.daily_limit})>"
