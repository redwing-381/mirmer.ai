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

# Model Tier Configuration
# Select performance tier via MODEL_TIER environment variable: speed, balanced, or cost
MODEL_TIER = os.getenv("MODEL_TIER", "balanced")

# Model configurations by tier
MODEL_TIERS = {
    "ultra": {
        "council": [
            "openai/gpt-4o",                         # OpenAI - Fastest flagship (~$0.015/call)
            "anthropic/claude-3-5-sonnet",           # Anthropic - Fastest (~$0.015/call)
            "openai/gpt-4-turbo",                    # OpenAI - Very fast (~$0.030/call)
            "anthropic/claude-3-opus"                # Anthropic - Most capable (~$0.075/call)
        ],
        "chairman": "openai/gpt-4o",                 # Fastest synthesis (~$0.015/call)
        "expected_latency": 6,  # seconds
        "cost_per_query": 0.150  # Premium pricing
    },
    "premium": {
        "council": [
            "openai/gpt-4o-mini",                    # OpenAI - Very fast (~$0.004/call)
            "google/gemini-2.0-flash-001",           # Google - Ultra fast (~$0.003/call)
            "openai/gpt-3.5-turbo",                  # OpenAI - Ultra fast (~$0.002/call)
            "anthropic/claude-3-5-haiku"             # Anthropic - Latest fast (~$0.004/call)
        ],
        "chairman": "anthropic/claude-3-5-haiku",    # Fast synthesis (~$0.004/call)
        "expected_latency": 10,  # seconds
        "cost_per_query": 0.017
    },
    "speed": {
        "council": [
            "google/gemini-2.0-flash-exp:free",      # Google - Very fast & FREE
            "openai/gpt-oss-20b",                    # OpenAI OSS - Fast
            "arcee-ai/trinity-mini:free",            # Arcee - Fast & FREE
            "tngtech/tng-r1t-chimera:free"           # TNG - Fast & FREE
        ],
        "chairman": "google/gemini-2.0-flash-lite-001",  # Google - Fast synthesis
        "expected_latency": 10,  # seconds
        "cost_per_query": 0.005
    },
    "balanced": {
        "council": [
            "arcee-ai/trinity-mini",                 # Arcee - Fast & capable
            "allenai/olmo-3-7b-instruct",            # AllenAI - Good balance
            "openai/gpt-oss-20b",                    # OpenAI OSS - Fast
            "google/gemini-2.0-flash-lite-001"       # Google - Very fast
        ],
        "chairman": "google/gemini-2.0-flash-lite-001",  # Google - Fast synthesis
        "expected_latency": 12,  # seconds
        "cost_per_query": 0.008
    },
    "cost": {
        "council": [
            "google/gemini-2.0-flash-exp:free",      # Google - FREE
            "arcee-ai/trinity-mini:free",            # Arcee - FREE
            "tngtech/tng-r1t-chimera:free",          # TNG - FREE
            "amazon/nova-2-lite-v1:free"             # Amazon - FREE
        ],
        "chairman": "allenai/olmo-3-32b-think:free",  # AllenAI - FREE synthesis
        "expected_latency": 20,  # seconds
        "cost_per_query": 0.000  # All FREE!
    }
}


def get_model_config():
    """
    Get model configuration for the selected tier.
    
    Returns:
        dict: Model configuration with 'council', 'chairman', 'expected_latency', and 'cost_per_query'
    
    Validates MODEL_TIER and falls back to 'balanced' if invalid.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    tier = MODEL_TIER.lower()
    
    if tier not in MODEL_TIERS:
        logger.warning(f"Invalid MODEL_TIER '{MODEL_TIER}', defaulting to 'balanced'. Valid options: ultra, premium, speed, balanced, cost")
        tier = "balanced"
    
    config = MODEL_TIERS[tier]
    logger.info(f"Using '{tier}' model tier - Expected latency: {config['expected_latency']}s, Cost: ${config['cost_per_query']:.3f}/query")
    
    return config


# Get current tier configuration
_model_config = get_model_config()
COUNCIL_MODELS = _model_config["council"]
CHAIRMAN_MODEL = _model_config["chairman"]

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
