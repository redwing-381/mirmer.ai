#!/usr/bin/env python3
"""
Quick test to verify all imports work correctly after fixes.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Testing imports after fixes...\n")

try:
    print("1. Testing backend.storage...")
    from backend import storage
    print("   ✅ backend.storage imported successfully")
    
    print("\n2. Testing backend.usage...")
    from backend import usage
    print("   ✅ backend.usage imported successfully")
    
    print("\n3. Testing backend.database...")
    from backend import database
    print("   ✅ backend.database imported successfully")
    
    print("\n4. Testing backend.models...")
    from backend import models
    print("   ✅ backend.models imported successfully")
    
    print("\n5. Testing backend.council...")
    from backend import council
    print("   ✅ backend.council imported successfully")
    
    print("\n6. Testing backend.config...")
    from backend import config
    print("   ✅ backend.config imported successfully")
    
    print("\n7. Testing backend.openrouter...")
    from backend import openrouter
    print("   ✅ backend.openrouter imported successfully")
    
    print("\n8. Testing backend.payments...")
    from backend import payments
    print("   ✅ backend.payments imported successfully")
    
    print("\n" + "="*50)
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("="*50)
    print("\nThe fixes are working correctly. All modules can be imported.")
    print("\nNext steps:")
    print("1. Install dependencies: cd backend && source .venv/bin/activate && pip install -r requirements.txt")
    print("2. Start backend: uvicorn main:app --reload --port 8001")
    print("3. Start frontend: cd frontend && npm run dev")
    
except ImportError as e:
    print(f"\n❌ Import failed: {e}")
    print("\nThis might be because dependencies aren't installed.")
    print("Try: cd backend && source .venv/bin/activate && pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    sys.exit(1)
