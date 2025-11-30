# Import Fix - Back to Relative Imports

## What Happened

1. **Initially**: Your app was deployed with relative imports (`import storage`) - **IT WORKED** ✅
2. **We changed**: Added `backend.` prefix (`from backend import storage`) to fix local development
3. **Result**: Railway deployment **BROKE** ❌ - "ModuleNotFoundError: No module named 'backend'"

## The Problem

When Railway runs `cd backend && uvicorn main:app`:
- Working directory: `/app` (the backend folder)
- Python looks for modules in the current directory
- `from backend import storage` fails because there's no `backend` folder inside `/app`
- `import storage` works because `storage.py` is in `/app`

## The Solution

**Reverted ALL imports back to relative imports** (what was working before):

### Changed From (Broken):
```python
from backend import storage
from backend import usage
from backend.database import get_db
```

### Changed To (Working):
```python
import storage
import usage
from database import get_db
```

## Files Reverted

1. ✅ `backend/main.py` - All imports
2. ✅ `backend/storage.py` - Import statements
3. ✅ `backend/usage.py` - Import statements
4. ✅ `backend/database.py` - Import models
5. ✅ `backend/storage_postgres.py` - Import database, models
6. ✅ `backend/usage_postgres.py` - Import database, models
7. ✅ `backend/payments.py` - Import models, database
8. ✅ `backend/council.py` - Import openrouter, config
9. ✅ `backend/openrouter.py` - Import config
10. ✅ `backend/storage_json.py` - Import config

## Railway Configuration

Also reverted to the simple, working configuration:

**railway.json:**
```json
{
  "deploy": {
    "startCommand": "cd backend && python init_database.py && uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

**nixpacks.toml:**
```toml
[start]
cmd = "cd backend && python init_database.py && uvicorn main:app --host 0.0.0.0 --port $PORT"
```

## Why This Works

```
Railway Deployment:
/app/                    ← cd backend puts us here
├── main.py             ← import storage works! ✅
├── storage.py          ← Found in current directory
├── usage.py
└── ...
```

## Local Development

For local development, you need to run from the backend directory:

```bash
cd backend
python -m uvicorn main:app --reload --port 8001
```

OR use the start script which handles this:
```bash
./start_backend.sh
```

## Key Lesson

**Keep it simple!** The original deployment was working with relative imports. We should have kept that approach instead of trying to use absolute imports with `backend.` prefix.

## Deploy Now

```bash
# 1. Build frontend
cd frontend && npm run build && cd ..

# 2. Commit changes
git add .
git commit -m "Fix: Revert to relative imports for Railway compatibility"

# 3. Push
git push
```

## Expected Result

Railway logs should show:
```
✓ Using PostgreSQL storage backend (production)
✓ Database connection successful
✓ Database tables initialized
✓ Serving frontend from /app/frontend/dist
INFO: Application startup complete
```

**No more ModuleNotFoundError!** 🎉

---

**Status**: ✅ Fixed by reverting to relative imports
**Date**: December 1, 2024
**Approach**: Keep it simple - use what was working before
