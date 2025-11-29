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
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "qwen/qwen-2-7b-instruct:free"
]

# Chairman Model
CHAIRMAN_MODEL = "meta-llama/llama-3.2-3b-instruct:free"

# Storage Configuration
DATA_DIR = "data/conversations"
