import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Council Models Configuration
# Using FREE models available on OpenRouter
COUNCIL_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "x-ai/grok-beta:free",
    "mistralai/mistral-7b-instruct:free"
]

# Chairman Model - Using Gemini as it performed well
CHAIRMAN_MODEL = "google/gemini-2.0-flash-exp:free"

# Storage Configuration
DATA_DIR = "data/conversations"

# User data directory structure: data/conversations/{user_id}/{conversation_id}.json
