import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in the parent directory (project root) first, then current directory
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()  # Fall back to current directory

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Council Models Configuration
# Optimized for 400+ queries with $10 credit (~$0.025 per query)
# Using 4 cost-effective models from different providers for diverse perspectives
COUNCIL_MODELS = [
    "openai/gpt-3.5-turbo",            # OpenAI - Fast & reliable (~$0.002/call)
    "anthropic/claude-3-haiku",        # Anthropic - Efficient & accurate (~$0.001/call)
    "mistralai/mistral-7b-instruct",   # Mistral - Fast & capable (~$0.001/call)
    "meta-llama/llama-3.1-8b-instruct" # Meta - Llama perspective (~$0.001/call)
]

# Chairman Model - Using Haiku for cost-effective synthesis
CHAIRMAN_MODEL = "anthropic/claude-3-haiku"

# Storage Configuration
DATA_DIR = "data/conversations"

# User data directory structure: data/conversations/{user_id}/{conversation_id}.json

# Email Service Configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "noreply@mirmer.ai")
SENDGRID_FROM_NAME = os.getenv("SENDGRID_FROM_NAME", "Mirmer AI")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@mirmer.ai")


def validate_production_config() -> dict:
    """
    Validate required environment variables for production deployment.
    
    Returns:
        dict with 'valid' (bool) and 'errors' (list of error messages)
        
    Raises:
        ValueError: If critical configuration is missing in production mode
    """
    import logging
    logger = logging.getLogger(__name__)
    
    errors = []
    warnings = []
    
    # Check if we're in production (DATABASE_URL is set)
    database_url = os.getenv("DATABASE_URL")
    is_production = bool(database_url)
    
    # Critical: OpenRouter API Key (required for all environments)
    if not OPENROUTER_API_KEY:
        errors.append("OPENROUTER_API_KEY is not set - AI functionality will not work")
    
    # Production-specific checks
    if is_production:
        logger.info("🔍 Running production configuration validation...")
        
        # Database
        if not database_url:
            errors.append("DATABASE_URL is not set - required for production")
        
        # Payment processing (Razorpay)
        razorpay_key_id = os.getenv("RAZORPAY_KEY_ID")
        razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        razorpay_webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")
        
        if not razorpay_key_id:
            warnings.append("RAZORPAY_KEY_ID is not set - payment processing will not work")
        if not razorpay_key_secret:
            warnings.append("RAZORPAY_KEY_SECRET is not set - payment processing will not work")
        if not razorpay_webhook_secret:
            warnings.append("RAZORPAY_WEBHOOK_SECRET is not set - webhook verification will fail")
        
        # Email service (optional but recommended)
        if not SENDGRID_API_KEY:
            warnings.append("SENDGRID_API_KEY is not set - enterprise contact emails will not work")
    else:
        logger.info("🔍 Running development configuration validation...")
        warnings.append("DATABASE_URL not set - using JSON file storage (development mode)")
    
    # Log results
    if errors:
        logger.error("❌ Configuration validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
    
    if warnings:
        logger.warning("⚠️  Configuration warnings:")
        for warning in warnings:
            logger.warning(f"  - {warning}")
    
    if not errors and not warnings:
        logger.info("✅ Configuration validation passed - all required variables set")
    elif not errors:
        logger.info("✅ Configuration validation passed with warnings")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'is_production': is_production
    }
