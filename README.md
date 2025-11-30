# Mirmer AI - Multi-LLM Consultation System

A multi-LLM consultation system that queries multiple AI models in parallel, has them peer-review each other's responses, and synthesizes a final answer through a 3-stage council process.

## Features

- **Stage 1**: Collect individual responses from multiple AI models in parallel
- **Stage 2**: Anonymous peer review where models rank each other's responses
- **Stage 3**: Chairman synthesis of collective wisdom into a comprehensive answer
- Real-time streaming updates via Server-Sent Events
- **Persistent storage** with PostgreSQL (production) or JSON files (local development)
- User authentication with Firebase Google Sign-In
- **Razorpay payment integration** for Pro subscriptions (India-friendly)
- Usage tracking and rate limiting
- Clean React UI with tabbed interfaces for each stage
- Landing page with pricing tiers

## Prerequisites

- Python 3.10+
- Node.js 18+
- uv (Python package manager)
- OpenRouter API key
- PostgreSQL database (for production) - optional for local development
- Firebase project (for authentication)
- Razorpay account (for payment processing) - optional

## Setup

### 1. Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenRouter API key
# Get your key from: https://openrouter.ai/keys
```

### 3. Install Backend Dependencies

```bash
cd backend
uv sync
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Running the Application

### Quick Start (Recommended)

```bash
./start.sh
```

This will start both backend and frontend servers automatically.

### Manual Start

#### Start Backend (Terminal 1)

```bash
cd backend
uv run uvicorn main:app --reload --port 8001
```

Backend will be available at: http://localhost:8001

#### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## Project Structure

```
mirmer-ai/
├── backend/
│   ├── config.py              # Configuration and model definitions
│   ├── openrouter.py          # OpenRouter API client
│   ├── council.py             # 3-stage council orchestration
│   ├── database.py            # PostgreSQL connection and setup
│   ├── models.py              # SQLAlchemy database models
│   ├── storage.py             # Storage factory (auto-selects backend)
│   ├── storage_postgres.py   # PostgreSQL storage implementation
│   ├── storage_json.py        # JSON file storage implementation
│   ├── usage_postgres.py     # PostgreSQL usage tracking
│   ├── usage_json.py          # JSON usage tracking
│   ├── migrate_to_postgres.py # Migration script for existing data
│   └── main.py                # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── api.js             # API client with SSE support
│   │   ├── firebase.js        # Firebase authentication
│   │   ├── App.jsx            # Main application component
│   │   └── components/        # React components
│   └── package.json
├── data/                      # Local JSON storage (development only)
│   ├── {user_id}/             # User-specific conversations
│   └── usage/                 # Usage statistics
└── .env                       # Environment variables (not in git)
```

## Database

### Local Development (No Database Required)

By default, the application uses JSON file storage for local development. No database setup needed!

### Production (PostgreSQL)

For production deployment, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
```

The application will automatically:
- Use PostgreSQL for all storage operations
- Create required tables on startup
- Handle connection pooling

### Migrating Existing Data

If you have existing JSON data to migrate to PostgreSQL:

```bash
cd backend
python migrate_to_postgres.py --backup --dry-run  # Preview migration
python migrate_to_postgres.py --backup             # Perform migration
```

## API Endpoints

- `POST /api/conversations` - Create new conversation
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/{id}` - Get specific conversation
- `POST /api/conversations/{id}/message/stream` - Send message and stream 3-stage process
- `GET /api/usage` - Get user usage statistics
- `DELETE /api/conversations/{id}` - Delete conversation

## Development

The application uses:
- **Backend**: FastAPI with async/await for parallel model queries
- **Frontend**: React 19 with Vite for fast development
- **Communication**: Server-Sent Events for real-time streaming
- **Storage**: Dual-mode storage system
  - **Production**: PostgreSQL with SQLAlchemy ORM
  - **Local Development**: JSON files (no database required)
  - Automatic backend selection based on `DATABASE_URL` environment variable
- **Authentication**: Firebase Google Sign-In
- **Deployment**: Railway (backend + database) + Vercel (frontend)

## How It Works

### The 3-Stage Council Process

1. **Stage 1: Individual Responses**
   - All council models answer your question independently in parallel
   - Each model provides its unique perspective

2. **Stage 2: Peer Rankings**
   - Responses are anonymized (labeled as "Response A", "Response B", etc.)
   - Each model ranks all responses from best to worst
   - Aggregate rankings show which responses were collectively rated highest

3. **Stage 3: Chairman Synthesis**
   - The chairman model receives all responses and rankings
   - Synthesizes the collective wisdom into a comprehensive final answer
   - Represents the consensus and insights from the entire council

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure you're in the backend directory and run `uv sync`
- **Port already in use**: Change the port in `start.sh` or kill the process using port 8001
- **API key errors**: Ensure your OpenRouter API key is set in `.env`

### Frontend Issues

- **Module not found**: Run `npm install` in the frontend directory
- **Port already in use**: Change the port in `vite.config.js` or kill the process using port 5173

### Model Issues

- **402 Payment Required**: Your OpenRouter account needs credits, or switch to free models in `backend/config.py`
- **404 Model Not Found**: Update model IDs in `backend/config.py` to valid OpenRouter models
- **All models failed**: Check your API key and internet connection

## License

See LICENSE file for details.


## Payment Integration

Mirmer AI includes Razorpay payment integration for Pro subscriptions (₹1,499/month).

### Pricing Tiers

- **Free**: 10 queries per day
- **Pro**: 100 queries per day (₹1,499/month or $19/month)
- **Enterprise**: Unlimited queries (custom pricing)

### Setup Razorpay Payments

For detailed setup instructions, see [RAZORPAY_SETUP.md](RAZORPAY_SETUP.md).

Quick setup:

1. Create a Razorpay account at https://razorpay.com
2. Complete KYC verification
3. Get your API keys from the Razorpay Dashboard
4. Create a subscription plan in Razorpay
5. Add environment variables to `.env`:
   ```bash
   RAZORPAY_KEY_ID=rzp_test_your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   RAZORPAY_PRO_MONTHLY_PLAN_ID=plan_your_plan_id
   ```
6. Run database migration:
   ```bash
   cd backend
   python migrate_add_subscription_fields.py
   ```
7. Test locally with ngrok:
   ```bash
   ngrok http 8001
   ```

### Payment Features

- Secure checkout with Razorpay
- Supports UPI, Cards, NetBanking, Wallets
- Automatic subscription management
- Subscription cancellation
- Webhook handling for subscription events
- Usage limit updates based on subscription tier
- Payment success notifications
- Works in India and internationally

### Test Cards

Use these test cards in Razorpay Checkout (test mode):

- Success: `4111 1111 1111 1111`
- Decline: `4000 0000 0000 0002`
- 3D Secure: `5104 0600 0000 0008` (OTP: 1234)

Use any future expiry date, any 3-digit CVV, and any name.
