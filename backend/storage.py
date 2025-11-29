"""
JSON-based storage layer for conversation persistence.
"""
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from config import DATA_DIR

logger = logging.getLogger(__name__)


def ensure_data_dir(user_id: Optional[str] = None) -> None:
    """
    Ensure the data directory exists.
    
    Args:
        user_id: Optional user ID to create user-specific directory
    
    Requirements: 8.1
    """
    if user_id:
        user_dir = os.path.join(DATA_DIR, user_id)
        Path(user_dir).mkdir(parents=True, exist_ok=True)
        logger.debug(f"User directory ensured: {user_dir}")
    else:
        Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Data directory ensured: {DATA_DIR}")


def get_conversation_path(conversation_id: str, user_id: Optional[str] = None) -> str:
    """
    Get the file path for a conversation.
    
    Args:
        conversation_id: UUID of the conversation
        user_id: Optional user ID for user-specific path
    
    Returns:
        Full path to the conversation JSON file
    """
    if user_id:
        return os.path.join(DATA_DIR, user_id, f"{conversation_id}.json")
    return os.path.join(DATA_DIR, f"{conversation_id}.json")



import uuid


def create_conversation(user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new conversation JSON file for a specific user.
    
    Args:
        user_id: Firebase user ID
        conversation_id: Optional UUID (generates new one if not provided)
    
    Returns:
        Dictionary with conversation metadata
    
    Requirements: 8.1
    """
    ensure_data_dir(user_id)
    
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())
    
    conversation = {
        "id": conversation_id,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "title": "New Conversation",
        "messages": []
    }
    
    save_conversation(conversation, user_id)
    logger.info(f"Created conversation: {conversation_id} for user: {user_id}")
    
    return conversation


def get_conversation(conversation_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Load conversation from JSON file for a specific user.
    
    Args:
        conversation_id: UUID of the conversation
        user_id: Firebase user ID
    
    Returns:
        Conversation dictionary or None if not found
    
    Requirements: 8.2, 8.4
    """
    path = get_conversation_path(conversation_id, user_id)
    
    if not os.path.exists(path):
        logger.warning(f"Conversation not found: {conversation_id} for user: {user_id}")
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            conversation = json.load(f)
        
        # Verify the conversation belongs to this user
        if conversation.get("user_id") != user_id:
            logger.warning(f"Unauthorized access attempt: {conversation_id} by user: {user_id}")
            return None
            
        logger.debug(f"Loaded conversation: {conversation_id} for user: {user_id}")
        return conversation
    except Exception as e:
        logger.error(f"Error loading conversation {conversation_id}: {str(e)}")
        return None


def save_conversation(conversation: Dict[str, Any], user_id: str) -> bool:
    """
    Save conversation to JSON file for a specific user.
    
    Args:
        conversation: Conversation dictionary
        user_id: Firebase user ID
    
    Returns:
        True if successful, False otherwise
    
    Requirements: 8.2
    """
    ensure_data_dir(user_id)
    
    conversation_id = conversation.get("id")
    if not conversation_id:
        logger.error("Cannot save conversation without ID")
        return False
    
    # Ensure user_id is set in conversation
    conversation["user_id"] = user_id
    
    path = get_conversation_path(conversation_id, user_id)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
        logger.debug(f"Saved conversation: {conversation_id} for user: {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving conversation {conversation_id}: {str(e)}")
        return False


def list_conversations(user_id: str) -> List[Dict[str, Any]]:
    """
    List all conversations for a specific user.
    
    Args:
        user_id: Firebase user ID
    
    Returns:
        List of conversation metadata dicts (id, title, created_at)
    
    Requirements: 8.4
    """
    user_dir = os.path.join(DATA_DIR, user_id)
    ensure_data_dir(user_id)
    
    conversations = []
    
    try:
        if not os.path.exists(user_dir):
            return []
            
        for filename in os.listdir(user_dir):
            if filename.endswith('.json'):
                conversation_id = filename[:-5]  # Remove .json extension
                conversation = get_conversation(conversation_id, user_id)
                
                if conversation:
                    conversations.append({
                        "id": conversation["id"],
                        "title": conversation.get("title", "Untitled"),
                        "created_at": conversation.get("created_at", "")
                    })
        
        # Sort by created_at descending (newest first)
        conversations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        logger.info(f"Listed {len(conversations)} conversations for user: {user_id}")
        return conversations
        
    except Exception as e:
        logger.error(f"Error listing conversations for user {user_id}: {str(e)}")
        return []



def add_user_message(conversation_id: str, content: str, user_id: str) -> bool:
    """
    Add user message to conversation.
    
    Args:
        conversation_id: UUID of the conversation
        content: User message content
    
    Returns:
        True if successful, False otherwise
    
    Requirements: 8.2
    """
    conversation = get_conversation(conversation_id, user_id)
    
    if not conversation:
        logger.error(f"Cannot add user message: conversation {conversation_id} not found")
        return False
    
    message = {
        "role": "user",
        "content": content
    }
    
    conversation["messages"].append(message)
    
    return save_conversation(conversation, user_id)


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
        metadata: Optional metadata (label_to_model, aggregate_rankings)
    
    Returns:
        True if successful, False otherwise
    
    Requirements: 8.2
    """
    conversation = get_conversation(conversation_id, user_id)
    
    if not conversation:
        logger.error(f"Cannot add assistant message: conversation {conversation_id} not found")
        return False
    
    message = {
        "role": "assistant",
        "stage1": stage1,
        "stage2": stage2,
        "stage3": stage3
    }
    
    if metadata:
        message["metadata"] = metadata
    
    conversation["messages"].append(message)
    
    return save_conversation(conversation, user_id)


def update_conversation_title(conversation_id: str, title: str, user_id: str) -> bool:
    """
    Update conversation title.
    
    Args:
        conversation_id: UUID of the conversation
        title: New title
    
    Returns:
        True if successful, False otherwise
    
    Requirements: 8.3
    """
    conversation = get_conversation(conversation_id, user_id)
    
    if not conversation:
        logger.error(f"Cannot update title: conversation {conversation_id} not found")
        return False
    
    conversation["title"] = title
    
    return save_conversation(conversation, user_id)



def delete_conversation(conversation_id: str, user_id: str) -> bool:
    """
    Delete a conversation.
    
    Args:
        conversation_id: UUID of the conversation
    
    Returns:
        True if successful, False otherwise
    """
    path = get_conversation_path(conversation_id, user_id)
    
    if not os.path.exists(path):
        logger.warning(f"Cannot delete: conversation {conversation_id} not found")
        return False
    
    try:
        os.remove(path)
        logger.info(f"Deleted conversation: {conversation_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting conversation {conversation_id}: {str(e)}")
        return False
