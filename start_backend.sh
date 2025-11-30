#!/bin/bash
# Start backend from project root so Python can find the backend module
source backend/.venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
