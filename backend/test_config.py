from pathlib import Path
from dotenv import load_dotenv
import os

# Test path resolution
env_path = Path(__file__).parent.parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f"Exists: {env_path.exists()}")
print(f"Absolute path: {env_path.absolute()}")

# Try loading
load_dotenv(env_path)

# Check if loaded
api_key = os.getenv("SENDGRID_API_KEY")
from_email = os.getenv("SENDGRID_FROM_EMAIL")

print(f"\nSENDGRID_API_KEY: {api_key[:20] if api_key else 'NOT LOADED'}...")
print(f"SENDGRID_FROM_EMAIL: {from_email}")
