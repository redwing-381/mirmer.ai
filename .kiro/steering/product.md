---
inclusion: always
---

# Product Overview

Mirmer AI is a multi-LLM consultation system that queries multiple AI models in parallel, facilitates peer review, and synthesizes consensus answers through a 3-stage council process.

## Core Functionality

**Stage 1**: Multiple AI models respond to user queries independently and in parallel
**Stage 2**: Models anonymously peer-review and rank each other's responses
**Stage 3**: A chairman model synthesizes the collective wisdom into a comprehensive final answer

## Key Features

- Real-time streaming updates via Server-Sent Events (SSE)
- User authentication with Firebase (Google Sign-In)
- Razorpay payment integration for Pro subscriptions (India-friendly)
- Usage tracking and rate limiting (Free: 10 queries/day, Pro: 100 queries/day)
- Persistent conversation storage with dual-mode backend (PostgreSQL for production, JSON for local dev)
- Clean React UI with tabbed interfaces for each stage
- Landing page with pricing tiers

## Business Model

- **Free Tier**: 10 queries per day
- **Pro Tier**: 100 queries per day (₹1,499/month or $19/month)
- **Enterprise**: Unlimited queries (custom pricing)
