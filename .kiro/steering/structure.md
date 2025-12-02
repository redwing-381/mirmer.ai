---
inclusion: always
---

# Project Structure

## Root Layout

```
mirmer-ai/
├── backend/           # FastAPI backend application
├── frontend/          # React frontend application
├── sdk/               # Python SDK package
├── data/              # Local JSON storage (development only)
├── .env               # Environment variables (not in git)
├── .env.example       # Environment template
└── start.sh           # Quick start script for both services
```

## Backend Structure

```
backend/
├── main.py                    # FastAPI app entry point, API routes
├── config.py                  # Configuration and model definitions
├── council.py                 # 3-stage council orchestration logic
├── openrouter.py              # OpenRouter API client
├── database.py                # PostgreSQL connection and setup
├── models.py                  # SQLAlchemy database models
├── storage.py                 # Storage factory (auto-selects backend)
├── storage_postgres.py        # PostgreSQL storage implementation
├── storage_json.py            # JSON file storage implementation
├── usage.py                   # Usage tracking factory
├── usage_postgres.py          # PostgreSQL usage tracking
├── usage_json.py              # JSON usage tracking
├── payments.py                # Razorpay payment integration
├── migrate_to_postgres.py     # Data migration script
├── migrate_add_subscription_fields.py  # Schema migration
├── admin_upgrade_user.py      # Admin utility for user upgrades
├── requirements.txt           # Python dependencies
├── pyproject.toml             # uv project configuration
└── data/                      # Local JSON storage directory
```

## SDK Structure

```
sdk/
├── mirmer/
│   ├── __init__.py            # Package initialization
│   ├── client.py              # Synchronous client
│   ├── async_client.py        # Asynchronous client
│   ├── models.py              # Pydantic data models
│   ├── auth.py                # Authentication utilities
│   └── cli.py                 # CLI tool implementation
├── examples/
│   ├── basic_usage.py         # Basic SDK usage examples
│   ├── streaming_example.py   # Streaming response examples
│   ├── conversation_management.py  # Conversation CRUD examples
│   └── test_with_backend.py   # Integration test with backend
├── pyproject.toml             # Package configuration
├── README.md                  # SDK documentation
└── PUBLISH_NOW.sh             # Publishing script
```

## Frontend Structure

```
frontend/
├── public/
│   └── cli-auth.html          # CLI authentication page (popup-based)
├── src/
│   ├── main.jsx               # React app entry point
│   ├── App.jsx                # Main app component with routing
│   ├── api.js                 # API client with SSE support
│   ├── firebase.js            # Firebase authentication setup
│   ├── components/
│   │   ├── ChatInterface.jsx  # Main chat UI with 3-stage tabs
│   │   ├── Sidebar.jsx        # Conversation list sidebar with search
│   │   ├── SearchBar.jsx      # Search input with debouncing
│   │   ├── Stage1.jsx         # Stage 1 individual responses display
│   │   ├── Stage2.jsx         # Stage 2 peer rankings display
│   │   ├── Stage3.jsx         # Stage 3 chairman synthesis display
│   │   ├── Auth.jsx           # Authentication component
│   │   ├── AuthModal.jsx      # Sign-in modal
│   │   ├── UsageStats.jsx     # Usage tracking display
│   │   ├── UpgradeModal.jsx   # Pro subscription upgrade modal
│   │   ├── SubscriptionManager.jsx  # Subscription management
│   │   ├── EnterpriseContactModal.jsx  # Enterprise inquiry form
│   │   ├── landing/           # Landing page components
│   │   │   ├── HeroSection.jsx
│   │   │   ├── FeaturesSection.jsx
│   │   │   ├── PricingSection.jsx
│   │   │   ├── ComparisonSection.jsx
│   │   │   ├── UseCasesSection.jsx
│   │   │   ├── FAQSection.jsx
│   │   │   ├── Navigation.jsx
│   │   │   └── Footer.jsx
│   │   └── ui/                # Reusable UI components
│   │       ├── Button.jsx
│   │       ├── Card.jsx
│   │       ├── Input.jsx
│   │       ├── Badge.jsx
│   │       ├── Toast.jsx
│   │       └── AlertDialog.jsx
│   ├── pages/
│   │   ├── LandingPage.jsx    # Public landing page
│   │   ├── AppPage.jsx        # Main application page (authenticated)
│   │   └── SettingsPage.jsx   # User settings and subscription
│   └── lib/
│       └── utils.js           # Utility functions (cn for classnames)
├── index.html                 # HTML entry point
├── package.json               # npm dependencies and scripts
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind CSS configuration
└── postcss.config.js          # PostCSS configuration
```

## Architecture Patterns

### Dual-Mode Storage
The backend uses a factory pattern to automatically select storage backend:
- **Production** (DATABASE_URL set): PostgreSQL via `storage_postgres.py`
- **Development** (no DATABASE_URL): JSON files via `storage_json.py`
- Import from `storage.py` to get the correct implementation automatically

### API Communication
- REST endpoints for CRUD operations
- Server-Sent Events (SSE) for streaming 3-stage council process
- Firebase ID tokens in `x-user-id` header for authentication

### Component Organization
- **Pages**: Top-level route components
- **Components**: Feature components (Chat, Sidebar, Auth, etc.)
- **Components/ui**: Reusable UI primitives
- **Components/landing**: Landing page sections

### State Management
- Firebase auth state managed in `App.jsx`
- Conversation state managed in `AppPage.jsx`
- Search state managed in `Sidebar.jsx` with debounced API calls
- Local component state with React hooks
- No global state management library (Redux, Zustand, etc.)

### Search Implementation
- **Frontend**: SearchBar component with 300ms debounce
- **Backend**: Full-text search through conversation titles and message content
- **API**: `GET /api/conversations/search?q={query}`
- **Storage**: Implemented in both `storage_json.py` and `storage_postgres.py`

## Data Flow

### Web Application
1. User sends message via `ChatInterface.jsx`
2. Frontend calls `/api/conversations/{id}/message/stream` via `api.js`
3. Backend orchestrates 3-stage council process in `council.py`
4. Real-time updates streamed back via SSE
5. Frontend updates UI progressively as each stage completes
6. Final conversation saved to storage backend (PostgreSQL or JSON)

### CLI/SDK Authentication
1. User runs `mirmer login` command
2. CLI opens browser to `/auth/cli?callback=http://localhost:8765/callback`
3. User clicks "Sign in with Google" button
4. Firebase popup opens for Google authentication
5. After sign-in, popup closes and page gets Firebase ID token
6. Page redirects to `http://localhost:8765/callback?token=...&email=...`
7. CLI local server receives token and saves to `~/.mirmer/credentials.json`
8. CLI uses token for subsequent API requests via `x-user-id` header
