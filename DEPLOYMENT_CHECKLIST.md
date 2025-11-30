# Deployment Checklist for Usage Tracking Fix

## Issue
Usage tracking works in localhost but not in production (Railway/PostgreSQL).

## Changes Made

### 1. Backend Fixes (`backend/usage_postgres.py`)
- Added `session.flush()` before commit to ensure data is written
- Added `session.refresh()` after increment to verify changes
- Added detailed error logging with full tracebacks
- Added missing `daily_queries_used` and `monthly_queries_used` fields to error responses
- Enhanced logging at every step of the increment process

### 2. Test Endpoint (`backend/main.py`)
- Added `/api/usage/test-increment` endpoint for manual testing
- Can be used to verify increment works in production

## Deployment Steps

### 1. Commit and Push Changes
```bash
git add .
git commit -m "fix: Enhanced usage tracking with better error handling and logging"
git push
```

### 2. Verify Deployment
- Wait for Railway to deploy the changes
- Check Railway logs for any deployment errors

### 3. Test in Production

#### Option A: Use Test Endpoint
```bash
# Get your user ID from Firebase (check browser console after login)
curl -X POST https://your-app.railway.app/api/usage/test-increment \
  -H "X-User-Id: YOUR_USER_ID"
```

#### Option B: Send a Real Message
1. Go to your deployed app
2. Send a message in a conversation
3. Check Settings → Usage tab
4. Should see the counter increment

### 4. Check Railway Logs
Look for these log messages:
- `🔄 Starting usage increment for user:`
- `📈 Before increment - daily: X, monthly: Y, total: Z`
- `✅ Incremented usage for user:`

If you see errors:
- `❌ Error incrementing usage`
- Check the full traceback in logs
- Verify DATABASE_URL is set correctly
- Verify database tables exist

## Common Issues

### Issue: Database tables don't exist
**Solution:** Run database initialization
```bash
# SSH into Railway or run locally with production DATABASE_URL
python backend/init_database.py
```

### Issue: User record doesn't exist
**Solution:** The code now auto-creates records, but you can manually create:
```python
from backend.database import SessionLocal
from backend.models import Usage

with SessionLocal() as session:
    usage = Usage(
        user_id="YOUR_USER_ID",
        tier="free",
        daily_used=0,
        daily_limit=10,
        monthly_used=0,
        monthly_limit=100,
        total_queries=0
    )
    session.add(usage)
    session.commit()
```

### Issue: Stats show 0 but increment logs show success
**Solution:** Check if frontend is using correct field names
- Frontend expects: `daily_queries_used`, `monthly_queries_used`
- Backend now returns both old and new field names

## Verification Checklist

- [ ] Changes deployed to Railway
- [ ] No deployment errors in Railway logs
- [ ] Can send messages successfully
- [ ] Usage counter increments after sending message
- [ ] Settings page shows correct usage stats
- [ ] Increment logs appear in Railway logs
- [ ] No error messages in logs

## Rollback Plan

If issues persist:
```bash
git revert HEAD
git push
```

## Next Steps After Fix

1. Monitor logs for 24 hours
2. Verify multiple users' usage tracking
3. Test limit enforcement (send 10 messages as free user)
4. Remove test endpoint `/api/usage/test-increment` (optional, for security)
