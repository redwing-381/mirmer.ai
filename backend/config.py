import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
