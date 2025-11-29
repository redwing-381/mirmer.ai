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


def ensure_data_dir() -> None:
    """
    Ensure the data directory exists.
    
    Requirements: 8.1
    """
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Data directory ensured: {DATA_DIR}")


def get_conversation_path(conversation_id: str) -> str:
    """
    Get the file path for a conversation.
    
    Args:
        conversation_id: UUID of the conversation
    
    Returns:
        Full path to the conversation JSON file
    """
    return os.path.join(DATA_DIR, f"{conversation_id}.json")



import uuid


def create_conversation(conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new conversation JSON file.
    
    Args:
        conversation_id: Optional UUID (generates new one if not provided)
    
    Returns:
        Dictionary with conversation metadata
    
    Requirements: 8.1
    """
    ensure_data_dir()
    
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())
    
    conversation = {
        "id": conversation_id,
        "created_at": datetime.utcnow().isoformat(),
        "title": "New Conversation",
        "messages": []
    }
    
    save_conversation(conversation)
    logger.info(f"Created conversation: {conversation_id}")
    
    return conversation


def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Load conversation from JSON file.
    
    Args:
        conversation_id: UUID of the conversation
    
    Returns:
        Conversation dictionary or None if not found
    
    Requirements: 8.2, 8.4
    """
    path = get_conversation_path(conversation_id)
    
    if not os.path.exists(path):
        logger.warning(f"Conversation not found: {conversation_id}")
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            conversation = json.load(f)
        logger.debug(f"Loaded conversation: {conversation_id}")
        return conversation
    except Exception as e:
        logger.error(f"Error loading conversation {conversation_id}: {str(e)}")
        return None


def save_conversation(conversation: Dict[str, Any]) -> bool:
    """
    Save conversation to JSON file.
    
    Args:
        conversation: Conversation dictionary
    
    Returns:
        True if successful, False otherwise
    
    Requirements: 8.2
    """
    ensure_data_dir()
    
    conversation_id = conversation.get("id")
    if not conversation_id:
        logger.error("Cannot save conversation without ID")
        return False
    
    path = get_conversation_path(conversation_id)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
        logger.debug(f"Saved conversation: {conversation_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving conversation {conversation_id}: {str(e)}")
        return False


def list_conversations() -> List[Dict[str, Any]]:
    """
    List all conversations with metadata.
    
    Returns:
        List of conversation metadata dicts (id, title, created_at)
    
    Requirements: 8.4
    """
    ensure_data_dir()
    
    conversations = []
    
    try:
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                conversation_id = filename[:-5]  # Remove .json extension
                conversation = get_conversation(conversation_id)
                
                if conversation:
                    conversations.append({
                        "id": conversation["id"],
                        "title": conversation.get("title", "Untitled"),
                        "created_at": conversation.get("created_at", "")
                    })
        
        # Sort by created_at descending (newest first)
        conversations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        logger.info(f"Listed {len(conversations)} conversations")
        return conversations
        
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        return []



def add_user_message(conversation_id: str, content: str) -> bool:
    """
    Add user message to conversation.
    
    Args:
        conversation_id: UUID of the conversation
        content: User message content
    
    Returns:
        True if successful, False otherwise
    
    Requirements: 8.2
    """
    conversation = get_conversation(conversation_id)
    
    if not conversation:
        logger.error(f"Cannot add user message: conversation {conversation_id} not found")
        return False
    
    message = {
        "role": "user",
        "content": content
    }
    
    conversation["messages"].append(message)
    
    return save_conversation(conversation)


def add_assistant_message(
    conversation_id: str,
    stage1: List[Dict],
    stage2: List[Dict],
    stage3: Dict,
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
    conversation = get_conversation(conversation_id)
    
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
    
    return save_conversation(conversation)


def update_conversation_title(conversation_id: str, title: str) -> bool:
    """
    Update conversation title.
    
    Args:
        conversation_id: UUID of the conversation
        title: New title
    
    Returns:
        True if successful, False otherwise
    
    Requirements: 8.3
    """
    conversation = get_conversation(conversation_id)
    
    if not conversation:
        logger.error(f"Cannot update title: conversation {conversation_id} not found")
        return False
    
    conversation["title"] = title
    
    return save_conversation(conversation)
