import os

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Council Models Configuration
COUNCIL_MODELS = [
    "openai/gpt-4-turbo",
    "anthropic/claude-3-sonnet",
    "google/gemini-pro"
]

# Chairman Model
CHAIRMAN_MODEL = "anthropic/claude-3-sonnet"

# Storage Configuration
DATA_DIR = "data/conversations"
