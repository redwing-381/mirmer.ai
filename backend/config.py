import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Council Models Configuration
# Using BUDGET PAID models - Most cost-effective with your credits
# Cost: ~$0.012 per query (800+ queries with $10)
# 3 different models for diverse perspectives
COUNCIL_MODELS = [
    "openai/gpt-3.5-turbo",           # Fast, reliable, cheap (~$0.002/call)
    "anthropic/claude-3-haiku",       # Fast, accurate (~$0.001/call)
    "google/gemini-flash-1.5"         # Fast, good quality (~$0.001/call)
]

# Chairman Model - Using cheapest reliable model
# Using Haiku (cheapest) for synthesis to save costs
CHAIRMAN_MODEL = "anthropic/claude-3-haiku"

# Storage Configuration
DATA_DIR = "data/conversations"

# User data directory structure: data/conversations/{user_id}/{conversation_id}.json
