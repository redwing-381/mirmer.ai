"""
PostgreSQL-based storage layer for conversation persistence.
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models import Conversation, Message

logger = logging.getLogger(__name__)


def create_conversation(user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new conversation in the database.
    
    Args:
        user_id: Firebase user ID
        conversation_id: Optional UUID (generates new one if not provided)
    
    Returns:
        Dictionary with conversation metadata
    """
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
            
            logger.info(f"Created conversation: {conversation_id} for user: {user_id}")
            
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


def get_conversation(conversation_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Load conversation from database with all messages.
    
    Args:
        conversation_id: UUID of the conversation
        user_id: Firebase user ID
    
    Returns:
        Conversation dictionary or None if not found
    """
    with SessionLocal() as session:
        try:
            # Query with eager loading of messages
            db_conversation = session.query(Conversation).options(
                joinedload(Conversation.messages)
            ).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            
            if not db_conversation:
                logger.warning(f"Conversation not found: {conversation_id} for user: {user_id}")
                return None
            
            # Convert to dictionary
            messages = []
            for msg in db_conversation.messages:
                if msg.role == 'user':
                    messages.append({
                        'role': 'user',
                        'content': msg.content
                    })
                else:  # assistant
                    # DIAGNOSTIC: Log what we're retrieving from DB
                    logger.info(f"📖 Storage: Retrieved assistant message from DB")
                    logger.info(f"  Stage 1 from DB: type={type(msg.stage1_data)}, length={len(msg.stage1_data) if msg.stage1_data else 0}")
                    logger.info(f"  Stage 2 from DB: type={type(msg.stage2_data)}, length={len(msg.stage2_data) if msg.stage2_data else 0}")
                    logger.info(f"  Stage 3 from DB: type={type(msg.stage3_data)}, keys={list(msg.stage3_data.keys()) if msg.stage3_data else []}")
                    logger.debug(f"  Stage 1 DB content: {msg.stage1_data}")
                    logger.debug(f"  Stage 2 DB content: {msg.stage2_data}")
                    logger.debug(f"  Stage 3 DB content: {msg.stage3_data}")
                    
                    messages.append({
                        'role': 'assistant',
                        'stage1': msg.stage1_data or [],
                        'stage2': msg.stage2_data or [],
                        'stage3': msg.stage3_data or {},
                        'metadata': msg.message_metadata or {}
                    })
            
            logger.info(f"📖 Storage: Loaded conversation {conversation_id} with {len(messages)} messages")
            
            return {
                'id': db_conversation.id,
                'user_id': db_conversation.user_id,
                'title': db_conversation.title,
                'created_at': db_conversation.created_at.isoformat(),
                'messages': messages
            }
            
        except Exception as e:
            logger.error(f"Error loading conversation {conversation_id}: {e}")
            return None


def save_conversation(conversation: Dict[str, Any], user_id: str) -> bool:
    """
    Save/update conversation in database.
    Note: This is mainly for compatibility. Use specific functions for updates.
    
    Args:
        conversation: Conversation dictionary
        user_id: Firebase user ID
    
    Returns:
        True if successful, False otherwise
    """
    with SessionLocal() as session:
        try:
            conversation_id = conversation.get('id')
            if not conversation_id:
                logger.error("Cannot save conversation without ID")
                return False
            
            db_conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            
            if db_conversation:
                # Update existing conversation
                db_conversation.title = conversation.get('title', db_conversation.title)
                db_conversation.updated_at = datetime.utcnow()
                session.commit()
                logger.debug(f"Updated conversation: {conversation_id}")
                return True
            else:
                logger.warning(f"Conversation not found for save: {conversation_id}")
                return False
                
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving conversation {conversation_id}: {e}")
            return False


def list_conversations(user_id: str) -> List[Dict[str, Any]]:
    """
    List all conversations for a specific user.
    
    Args:
        user_id: Firebase user ID
    
    Returns:
        List of conversation metadata dicts (id, title, created_at)
    """
    with SessionLocal() as session:
        try:
            db_conversations = session.query(Conversation).filter(
                Conversation.user_id == user_id
            ).order_by(
                Conversation.created_at.desc()
            ).all()
            
            conversations = [
                {
                    'id': conv.id,
                    'title': conv.title,
                    'created_at': conv.created_at.isoformat()
                }
                for conv in db_conversations
            ]
            
            logger.info(f"Listed {len(conversations)} conversations for user: {user_id}")
            return conversations
            
        except Exception as e:
            logger.error(f"Error listing conversations for user {user_id}: {e}")
            return []


def delete_conversation(conversation_id: str, user_id: str) -> bool:
    """
    Delete a conversation and all its messages.
    
    Args:
        conversation_id: UUID of the conversation
        user_id: Firebase user ID
    
    Returns:
        True if successful, False otherwise
    """
    with SessionLocal() as session:
        try:
            db_conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            
            if not db_conversation:
                logger.warning(f"Cannot delete: conversation {conversation_id} not found")
                return False
            
            session.delete(db_conversation)
            session.commit()
            
            logger.info(f"Deleted conversation: {conversation_id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting conversation {conversation_id}: {e}")
            return False


# Helper function for compatibility
def ensure_data_dir(user_id: Optional[str] = None) -> None:
    """
    Compatibility function - not needed for PostgreSQL.
    """
    pass


def get_conversation_path(conversation_id: str, user_id: Optional[str] = None) -> str:
    """
    Compatibility function - not needed for PostgreSQL.
    Returns empty string.
    """
    return ""



def add_user_message(conversation_id: str, content: str, user_id: str) -> bool:
    """
    Add user message to conversation.
    
    Args:
        conversation_id: UUID of the conversation
        content: User message content
        user_id: Firebase user ID
    
    Returns:
        True if successful, False otherwise
    """
    with SessionLocal() as session:
        try:
            # Verify conversation exists and belongs to user
            db_conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            
            if not db_conversation:
                logger.error(f"Cannot add user message: conversation {conversation_id} not found")
                return False
            
            # Create message
            db_message = Message(
                conversation_id=conversation_id,
                role='user',
                content=content
            )
            
            session.add(db_message)
            
            # Update conversation timestamp
            db_conversation.updated_at = datetime.utcnow()
            
            session.commit()
            logger.debug(f"Added user message to conversation: {conversation_id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding user message to {conversation_id}: {e}")
            return False


def add_assistant_message(
    conversation_id: str,
    stage1: List[Dict],
    stage2: List[Dict],
    stage3: Dict,
    user_id: str,
    metadata: Optional[Dict] = None
) -> bool:
    """
    Add complete assistant message with all 3 stages.
    
    Args:
        conversation_id: UUID of the conversation
        stage1: Stage 1 results (individual responses)
        stage2: Stage 2 results (rankings)
        stage3: Stage 3 result (chairman synthesis)
        user_id: Firebase user ID
        metadata: Optional metadata (label_to_model, aggregate_rankings)
    
    Returns:
        True if successful, False otherwise
    """
    with SessionLocal() as session:
        try:
            # Verify conversation exists and belongs to user
            db_conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            
            if not db_conversation:
                logger.error(f"Cannot add assistant message: conversation {conversation_id} not found")
                return False
            
            # DIAGNOSTIC: Log what we're about to save
            logger.info(f"💾 Storage: Saving assistant message to DB")
            logger.info(f"  Conversation: {conversation_id}")
            logger.info(f"  Stage 1 type: {type(stage1)}, length: {len(stage1) if stage1 else 0}")
            logger.info(f"  Stage 2 type: {type(stage2)}, length: {len(stage2) if stage2 else 0}")
            logger.info(f"  Stage 3 type: {type(stage3)}, keys: {list(stage3.keys()) if stage3 else []}")
            logger.debug(f"  Stage 1 content: {stage1}")
            logger.debug(f"  Stage 2 content: {stage2}")
            logger.debug(f"  Stage 3 content: {stage3}")
            
            # Create message
            db_message = Message(
                conversation_id=conversation_id,
                role='assistant',
                stage1_data=stage1,
                stage2_data=stage2,
                stage3_data=stage3,
                message_metadata=metadata
            )
            
            session.add(db_message)
            
            # Update conversation timestamp
            db_conversation.updated_at = datetime.utcnow()
            
            session.commit()
            logger.info(f"✅ Storage: Assistant message saved to DB successfully")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding assistant message to {conversation_id}: {e}")
            return False


def update_conversation_title(conversation_id: str, title: str, user_id: str) -> bool:
    """
    Update conversation title.
    
    Args:
        conversation_id: UUID of the conversation
        title: New title
        user_id: Firebase user ID
    
    Returns:
        True if successful, False otherwise
    """
    with SessionLocal() as session:
        try:
            db_conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            
            if not db_conversation:
                logger.error(f"Cannot update title: conversation {conversation_id} not found")
                return False
            
            db_conversation.title = title
            db_conversation.updated_at = datetime.utcnow()
            
            session.commit()
            logger.debug(f"Updated title for conversation: {conversation_id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating title for {conversation_id}: {e}")
            return False


def search_conversations(user_id: str, query: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Search conversations by title and message content using PostgreSQL full-text search.
    
    Args:
        user_id: Firebase user ID
        query: Search query string
        limit: Maximum number of results to return
    
    Returns:
        List of matching conversations with snippets
    """
    with SessionLocal() as session:
        try:
            from sqlalchemy import func, or_
            
            # Sanitize query for tsquery
            search_query = query.strip()
            if not search_query:
                return []
            
            # Create tsquery-compatible search term
            # Replace spaces with & for AND search
            ts_query = ' & '.join(search_query.split())
            
            # Search in conversation titles and message content
            results = session.query(Conversation).filter(
                Conversation.user_id == user_id
            ).filter(
                or_(
                    # Search in conversation title
                    func.to_tsvector('english', Conversation.title).op('@@')(
                        func.to_tsquery('english', ts_query)
                    ),
                    # Search in messages
                    Conversation.id.in_(
                        session.query(Message.conversation_id).filter(
                            func.to_tsvector('english', func.coalesce(Message.content, '')).op('@@')(
                                func.to_tsquery('english', ts_query)
                            )
                        )
                    )
                )
            ).options(
                joinedload(Conversation.messages)
            ).order_by(
                Conversation.updated_at.desc()
            ).limit(limit).all()
            
            # Format results with snippets
            formatted_results = []
            for conv in results:
                # Find matching message snippet
                snippet = None
                for msg in conv.messages:
                    if msg.content and query.lower() in msg.content.lower():
                        # Extract snippet around match
                        content_lower = msg.content.lower()
                        query_lower = query.lower()
                        match_pos = content_lower.find(query_lower)
                        
                        start = max(0, match_pos - 50)
                        end = min(len(msg.content), match_pos + len(query) + 50)
                        
                        snippet = msg.content[start:end]
                        if start > 0:
                            snippet = '...' + snippet
                        if end < len(msg.content):
                            snippet = snippet + '...'
                        break
                
                formatted_results.append({
                    'id': conv.id,
                    'title': conv.title,
                    'created_at': conv.created_at.isoformat(),
                    'updated_at': conv.updated_at.isoformat(),
                    'snippet': snippet or conv.title,
                    'match_in_title': query.lower() in conv.title.lower()
                })
            
            logger.info(f"Search for '{query}' returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching conversations: {e}")
            # Fallback to simple LIKE search if full-text search fails
            try:
                results = session.query(Conversation).filter(
                    Conversation.user_id == user_id,
                    Conversation.title.ilike(f'%{query}%')
                ).order_by(
                    Conversation.updated_at.desc()
                ).limit(limit).all()
                
                return [{
                    'id': conv.id,
                    'title': conv.title,
                    'created_at': conv.created_at.isoformat(),
                    'updated_at': conv.updated_at.isoformat(),
                    'snippet': conv.title,
                    'match_in_title': True
                } for conv in results]
            except Exception as fallback_error:
                logger.error(f"Fallback search also failed: {fallback_error}")
                return []
