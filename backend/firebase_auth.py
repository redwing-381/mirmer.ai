"""
Firebase authentication utilities for backend.
Decodes Firebase JWT tokens to extract user IDs.
"""
import logging
import hashlib
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import auth, credentials
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logger.warning("Firebase Admin SDK not available. Using fallback authentication.")


# Initialize Firebase Admin (only once)
_firebase_initialized = False

def initialize_firebase():
    """Initialize Firebase Admin SDK if not already initialized."""
    global _firebase_initialized
    
    if _firebase_initialized or not FIREBASE_AVAILABLE:
        return
    
    try:
        # Try to initialize with default credentials
        # This works on Google Cloud and with GOOGLE_APPLICATION_CREDENTIALS env var
        firebase_admin.initialize_app()
        _firebase_initialized = True
        logger.info("✓ Firebase Admin SDK initialized")
    except Exception as e:
        logger.warning(f"Could not initialize Firebase Admin SDK: {e}")
        logger.info("Using fallback authentication (hashed tokens)")


def extract_user_id(token: str) -> str:
    """
    Extract user ID from Firebase JWT token.
    
    If Firebase Admin SDK is available, verifies and decodes the token.
    Otherwise, creates a stable hash of the token to use as user ID.
    
    Args:
        token: Firebase JWT token or simple API key
        
    Returns:
        User ID (Firebase UID or hashed token)
    """
    # If token is short (< 100 chars), assume it's a simple API key for testing
    if len(token) < 100:
        return token
    
    # Try to decode Firebase JWT
    if FIREBASE_AVAILABLE and _firebase_initialized:
        try:
            decoded_token = auth.verify_id_token(token)
            user_id = decoded_token.get('uid')
            if user_id:
                logger.debug(f"Decoded Firebase token for user: {user_id}")
                return user_id
        except Exception as e:
            logger.warning(f"Failed to decode Firebase token: {e}")
    
    # Fallback: Create a stable hash of the token
    # This ensures the same token always maps to the same user ID
    token_hash = hashlib.sha256(token.encode()).hexdigest()[:32]
    logger.debug(f"Using hashed token as user ID: {token_hash}")
    return token_hash


def get_user_id_from_header(x_user_id: str) -> str:
    """
    Get user ID from x-user-id header.
    
    This is a convenience function that can be used as a FastAPI dependency.
    
    Args:
        x_user_id: Value from x-user-id header (JWT token or API key)
        
    Returns:
        Extracted user ID
    """
    return extract_user_id(x_user_id)
