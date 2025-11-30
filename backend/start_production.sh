#!/bin/bash
# Production startup script for Railway deployment
# This script ensures Python can find the backend module

# Get the parent directory (project root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Add project root to PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

echo "🚀 Starting Mirmer AI Backend"
echo "📁 Project root: ${PROJECT_ROOT}"
echo "🐍 PYTHONPATH: ${PYTHONPATH}"

# Initialize database
echo "🔧 Initializing database..."
cd "${PROJECT_ROOT}/backend"
python init_database.py

# Start uvicorn
echo "✅ Starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8001}
