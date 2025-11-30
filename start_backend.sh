#!/bin/bash
# Start backend with relative imports (matching Railway deployment)
cd backend
source .venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
