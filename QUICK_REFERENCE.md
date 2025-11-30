# Quick Reference - Mirmer AI Integration

## System Status

| Component | Status | Notes |
|-----------|--------|-------|
| Firebase Auth | ✅ Working | Google Sign-In operational |
| PostgreSQL | ✅ Working | All tables created, migration complete |
| Usage Tracking | ✅ Working | Fixed with subscription fields migration |
| Razorpay | ⚠️ Configured | Needs API keys and testing |

## Environment Variables Checklist

### ✅ Currently Set (Railway):
- `DATABASE_URL` - PostgreSQL connection
- `ADMIN_KEY` - Migration endpoint protection
- `FIREBASE_*` - Firebase configuration
- `OPENROUTER_API_KEY` - AI models

### ⚠️ Needs to be Set (Razorpay):
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `RAZORPAY_WEBHOOK_SECRET`
- `RAZORPAY_PRO_MONTHLY_PLAN_ID`
- `FRONTEND_URL` (for payment redirects)

## Quick Commands

### Test Integration:
```bash
./verify_integration.sh https://mirmerai-production.up.railway.app YOUR_USER_ID
```

### Run Migration (if needed):
```bash
./run_migration.sh https://mirmerai-production.up.railway.app YOUR_ADMIN_KEY
```

### Check PostgreSQL:
```sql
-- View usage stats
SELECT user_id, tier, daily_used, monthly_used, subscription_status 
FROM usage;

-- View conversations
SELECT user_id, COUNT(*) as conv_count 
FROM conversations 
GROUP BY user_id;

-- Check subscription info
SELECT user_id, tier, razorpay_subscription_id, subscription_status 
FROM usage 
WHERE tier = 'pro';
```

## API Endpoints

### Working Endpoints:
- `GET /` - Health check
- `GET /api/usage` - Get usage stats (requires X-User-Id)
- `POST /api/usage/test-increment` - Test usage increment
- `GET /api/conversations` - List conversations
- `POST /api/conversations` - Create conversation
- `POST /api/conversations/{id}/message/stream` - Send message

### Payment Endpoints (needs Razorpay):
- `POST /api/payments/create-subscription` - Create subscription
- `POST /api/payments/cancel-subscription` - Cancel subscription
- `GET /api/payments/subscription` - Get subscription info
- `POST /api/webhooks/razorpay` - Razorpay webhook

## Tier Limits

| Tier | Daily Limit | Monthly Limit | Cost |
|------|-------------|---------------|------|
| Free | 10 | 100 | Free |
| Pro | 100 | 3000 | ₹499/month (configurable) |
| Enterprise | Unlimited | Unlimited | Custom |

## User Flow

1. **Sign In:** Firebase Google Auth → User ID generated
2. **First Request:** PostgreSQL auto-creates usage record (tier: free)
3. **Send Message:** Usage incremented, rate limits checked
4. **Upgrade:** (When Razorpay configured)
   - Click "Upgrade to Pro"
   - Complete payment
   - Webhook updates tier to 'pro'
   - Limits increased automatically

## Troubleshooting

### Usage not incrementing:
✅ **FIXED** - Migration added missing columns

### 404 on page reload:
✅ **FIXED** - SPA routing configured

### Webhook not working:
⚠️ Check:
1. Webhook URL in Razorpay dashboard
2. RAZORPAY_WEBHOOK_SECRET in Railway
3. Railway logs for incoming requests

### Payment not updating tier:
⚠️ Check:
1. Webhook received (Railway logs)
2. user_id in subscription notes
3. PostgreSQL usage table updated

## Files to Reference

- **Integration Guide:** `INTEGRATION_VERIFICATION.md`
- **Status Report:** `INTEGRATION_STATUS.md`
- **Migration Guide:** `MIGRATION_GUIDE.md`
- **Deployment:** `DEPLOYMENT_CHECKLIST.md`

## Next Action Items

1. [ ] Create Razorpay account
2. [ ] Get API keys
3. [ ] Create Pro plan
4. [ ] Configure webhook
5. [ ] Add environment variables to Railway
6. [ ] Test payment flow
7. [ ] Go live!

## Support

- Railway Logs: https://railway.app → Your Project → Deployments
- Razorpay Dashboard: https://dashboard.razorpay.com
- PostgreSQL: Via Railway dashboard → Database tab

---

**Last Updated:** December 1, 2024  
**System Version:** 0.1.0  
**Status:** Production Ready (pending Razorpay configuration)
