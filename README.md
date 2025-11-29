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
