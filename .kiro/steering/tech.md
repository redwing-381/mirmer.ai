---
inclusion: always
---

# Tech Stack

## Backend

- **Framework**: FastAPI with async/await for parallel model queries
- **Language**: Python 3.10+
- **Package Manager**: uv (modern Python package manager)
- **Database**: PostgreSQL with SQLAlchemy ORM (production), JSON files (local dev)
- **AI Integration**: OpenRouter API for multi-model access
- **Payment Processing**: Razorpay SDK
- **Authentication**: Firebase Admin SDK (token verification)

## Frontend

- **Framework**: React 18.3+ with Vite
- **Routing**: React Router DOM v7
- **Styling**: Tailwind CSS with custom components
- **UI Components**: Custom component library in `components/ui/`
- **State Management**: React hooks and context
- **Markdown Rendering**: react-markdown

## Infrastructure

- **Backend Deployment**: Railway (with PostgreSQL database)
- **Frontend Deployment**: Vercel
- **Communication**: Server-Sent Events (SSE) for real-time streaming

## Key Libraries

### Backend
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client for OpenRouter API
- `sqlalchemy` - ORM for PostgreSQL
- `psycopg2-binary` - PostgreSQL adapter
- `razorpay` - Payment processing
- `python-dotenv` - Environment variable management

### Frontend
- `react` & `react-dom` - UI framework
- `react-router-dom` - Client-side routing
- `firebase` - Authentication
- `lucide-react` - Icon library
- `tailwindcss` - Utility-first CSS
- `class-variance-authority` & `clsx` - Component styling utilities

## Common Commands

### Development

```bash
# Start both backend and frontend
./start.sh

# Backend only
cd backend
uv run uvicorn main:app --reload --port 8001

# Frontend only
cd frontend
npm run dev
```

### Setup

```bash
# Install backend dependencies
cd backend
uv sync

# Install frontend dependencies
cd frontend
npm install
```

### Database

```bash
# Migrate JSON data to PostgreSQL
cd backend
python migrate_to_postgres.py --backup --dry-run  # Preview
python migrate_to_postgres.py --backup             # Execute

# Add subscription fields to existing database
python migrate_add_subscription_fields.py
```

### Testing

```bash
# Backend tests
cd backend
python test_usage.py
python test_models.py

# Frontend tests (if configured)
cd frontend
npm test
```

### Production Build

```bash
# Build frontend for production
cd frontend
npm run build

# Start production backend (serves frontend static files)
cd backend
./start_production.sh
```

## Environment Variables

Required variables in `.env`:
- `OPENROUTER_API_KEY` - OpenRouter API access
- `DATABASE_URL` - PostgreSQL connection (production only)
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` - Payment processing
- `RAZORPAY_WEBHOOK_SECRET` - Webhook verification
- `RAZORPAY_PRO_MONTHLY_PLAN_ID` - Subscription plan ID
- Firebase config variables (frontend)
