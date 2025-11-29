# Mirmer AI - Multi-LLM Consultation System

A multi-LLM consultation system that queries multiple AI models in parallel, has them peer-review each other's responses, and synthesizes a final answer through a 3-stage council process.

## Features

- **Stage 1**: Collect individual responses from multiple AI models in parallel
- **Stage 2**: Anonymous peer review where models rank each other's responses
- **Stage 3**: Chairman synthesis of collective wisdom into a comprehensive answer
- Real-time streaming updates via Server-Sent Events
- Conversation history with JSON storage
- Clean React UI with tabbed interfaces for each stage

## Prerequisites

- Python 3.10+
- Node.js 18+
- uv (Python package manager)
- OpenRouter API key

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

### Start Backend (Terminal 1)

```bash
cd backend
uv run uvicorn main:app --reload --port 8001
```

Backend will be available at: http://localhost:8001

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## Project Structure

```
mirmer-ai/
├── backend/
│   ├── config.py          # Configuration and model definitions
│   ├── openrouter.py      # OpenRouter API client
│   ├── council.py         # 3-stage council orchestration
│   ├── storage.py         # JSON conversation storage
│   └── main.py            # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── api.js         # API client with SSE support
│   │   ├── App.jsx        # Main application component
│   │   └── components/    # React components
│   └── package.json
├── data/
│   └── conversations/     # Stored conversations (JSON)
└── .env                   # Environment variables (not in git)
```

## API Endpoints

- `POST /api/conversations` - Create new conversation
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/{id}` - Get specific conversation
- `POST /api/conversations/{id}/message/stream` - Send message and stream 3-stage process

## Development

The application uses:
- **Backend**: FastAPI with async/await for parallel model queries
- **Frontend**: React 19 with Vite for fast development
- **Communication**: Server-Sent Events for real-time streaming
- **Storage**: JSON files for conversation persistence

## License

See LICENSE file for details.
