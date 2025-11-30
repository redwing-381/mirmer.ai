"""
FastAPI backend for Mirmer AI multi-LLM consultation system.
"""
import logging
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mirmer AI",
    description="Multi-LLM consultation system with 3-stage council process",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production to your frontend domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files in production
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    logger.info(f"✓ Serving frontend from {FRONTEND_DIST}")
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")
else:
    logger.warning(f"⚠️  Frontend dist directory not found at {FRONTEND_DIST}")


# Startup event - initialize database if using PostgreSQL
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    import os
    from backend.database import init_db, check_connection
    
    DATABASE_URL = os.getenv('DATABASE_URL')
    IS_PRODUCTION = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('VERCEL')
    
    if not DATABASE_URL:
        if IS_PRODUCTION:
            logger.error("✗ CRITICAL: DATABASE_URL not set in production environment!")
            logger.error("✗ Application cannot start without database configuration")
            raise RuntimeError("DATABASE_URL environment variable is required in production")
        else:
            logger.info("ℹ️  No DATABASE_URL found - using JSON file storage (development mode)")
            return
    
    logger.info("🔧 Initializing PostgreSQL database...")
    
    # Check connection
    if check_connection():
        logger.info("✓ Database connection successful")
        
        # Initialize tables
        if init_db():
            logger.info("✓ Database tables initialized")
        else:
            logger.error("✗ Failed to initialize database tables")
            if IS_PRODUCTION:
                raise RuntimeError("Failed to initialize database tables")
    else:
        logger.error("✗ Database connection failed")
        if IS_PRODUCTION:
            raise RuntimeError("Database connection failed in production")
        else:
            logger.warning("⚠️  Application will continue but database operations may fail")


# Pydantic models for requests/responses
class MessageRequest(BaseModel):
    content: str


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Mirmer AI",
        "version": "0.1.0"
    }


@app.get("/api/usage")
async def get_usage(x_user_id: str = Header(...)):
    """Get user's usage statistics."""
    try:
        stats = usage.get_usage_stats(x_user_id)
        return stats
    except Exception as e:
        logger.error(f"Error getting usage stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get usage stats")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)



from backend import storage
from backend import usage
from backend.payments import PaymentService, RAZORPAY_PLAN_IDS
from fastapi import Request
from backend.database import get_db
import json


@app.post("/api/conversations", response_model=ConversationResponse)
async def create_conversation(x_user_id: str = Header(...)):
    """
    Create a new conversation for a specific user.
    
    Requirements: 8.4, 8.5
    """
    try:
        conversation = storage.create_conversation(user_id=x_user_id)
        return ConversationResponse(
            id=conversation["id"],
            title=conversation["title"],
            created_at=conversation["created_at"]
        )
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create conversation")


@app.get("/api/conversations")
async def list_conversations(x_user_id: str = Header(...)):
    """
    List all conversations for a specific user.
    
    Requirements: 8.4
    """
    try:
        conversations = storage.list_conversations(user_id=x_user_id)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list conversations")


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, x_user_id: str = Header(...)):
    """
    Get specific conversation for a user.
    
    Requirements: 8.5
    """
    try:
        conversation = storage.get_conversation(conversation_id, user_id=x_user_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get conversation")



import json
from fastapi.responses import StreamingResponse
from backend import council


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: MessageRequest, x_user_id: str = Header(...)):
    """
    Send message and stream 3-stage council process via Server-Sent Events.
    
    Requirements: 2.3, 2.4, 3.1, 4.3, 6.2, 9.4
    """
    
    async def event_generator():
        try:
            # Check rate limits
            allowed, error_msg = usage.check_rate_limit(x_user_id)
            if not allowed:
                yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
                return
            
            # Validate conversation exists and belongs to user
            conversation = storage.get_conversation(conversation_id, user_id=x_user_id)
            if not conversation:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Conversation not found'})}\n\n"
                return
            
            # Add user message to conversation
            storage.add_user_message(conversation_id, request.content, user_id=x_user_id)
            
            # Increment usage count
            usage.increment_usage(x_user_id)
            
            # Stage 1: Collect individual responses
            yield f"data: {json.dumps({'type': 'stage1_start'})}\n\n"
            
            stage1_results = await council.stage1_collect_responses(
                user_query=request.content
            )
            
            if not stage1_results:
                yield f"data: {json.dumps({'type': 'error', 'message': 'All models failed in Stage 1'})}\n\n"
                return
            
            yield f"data: {json.dumps({'type': 'stage1_complete', 'data': stage1_results})}\n\n"
            
            # Stage 2: Collect peer rankings
            yield f"data: {json.dumps({'type': 'stage2_start'})}\n\n"
            
            stage2_results, label_to_model = await council.stage2_collect_rankings(
                user_query=request.content,
                stage1_results=stage1_results
            )
            
            if not stage2_results:
                yield f"data: {json.dumps({'type': 'error', 'message': 'All models failed in Stage 2'})}\n\n"
                return
            
            # Calculate aggregate rankings
            aggregate_rankings = council.calculate_aggregate_rankings(
                stage2_results=stage2_results,
                label_to_model=label_to_model
            )
            
            stage2_data = {
                "rankings": stage2_results,
                "label_to_model": label_to_model,
                "aggregate_rankings": aggregate_rankings
            }
            
            yield f"data: {json.dumps({'type': 'stage2_complete', 'data': stage2_data})}\n\n"
            
            # Stage 3: Chairman synthesis
            yield f"data: {json.dumps({'type': 'stage3_start'})}\n\n"
            
            stage3_result = await council.stage3_synthesize_final(
                user_query=request.content,
                stage1_results=stage1_results,
                stage2_results=stage2_results
            )
            
            yield f"data: {json.dumps({'type': 'stage3_complete', 'data': stage3_result})}\n\n"
            
            # Save complete assistant message
            metadata = {
                "label_to_model": label_to_model,
                "aggregate_rankings": aggregate_rankings
            }
            
            storage.add_assistant_message(
                conversation_id=conversation_id,
                stage1=stage1_results,
                stage2=stage2_results,
                stage3=stage3_result,
                user_id=x_user_id,
                metadata=metadata
            )
            
            # Update conversation title if this is the first message
            if len(conversation["messages"]) == 0:
                # Generate simple title from first few words
                title_words = request.content.split()[:8]
                title = " ".join(title_words)
                if len(request.content.split()) > 8:
                    title += "..."
                storage.update_conversation_title(conversation_id, title, user_id=x_user_id)
            
            # Send completion event
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in event generator: {str(e)}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )



@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, x_user_id: str = Header(...)):
    """
    Delete a conversation for a specific user.
    """
    try:
        success = storage.delete_conversation(conversation_id, user_id=x_user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"success": True, "message": "Conversation deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete conversation")


# Payment endpoints
@app.post("/api/payments/create-subscription")
async def create_subscription(x_user_id: str = Header(...), x_user_email: str = Header(...)):
    """
    Create a Razorpay subscription for Pro plan.
    """
    try:
        # Get the frontend URL from environment or use default
        import os
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        
        result = PaymentService.create_subscription(
            user_id=x_user_id,
            user_email=x_user_email,
            plan_id=RAZORPAY_PLAN_IDS['pro_monthly'],
            success_url=f"{frontend_url}/app?payment=success",
            cancel_url=f"{frontend_url}/?payment=cancelled"
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Failed to create subscription'))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create subscription")


@app.post("/api/payments/cancel-subscription")
async def cancel_subscription(x_user_id: str = Header(...)):
    """
    Cancel user's Razorpay subscription.
    """
    try:
        db = next(get_db())
        subscription_info = PaymentService.get_subscription_info(x_user_id, db)
        
        if not subscription_info or not subscription_info.get('subscription_id'):
            raise HTTPException(status_code=404, detail="No active subscription found")
        
        result = PaymentService.cancel_subscription(subscription_info['subscription_id'])
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Failed to cancel subscription'))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel subscription")


@app.get("/api/payments/subscription")
async def get_subscription(x_user_id: str = Header(...)):
    """
    Get user's subscription information.
    """
    try:
        # Check if database is configured
        import os
        if not os.getenv('DATABASE_URL'):
            # No database - return free tier for now
            return {"tier": "free", "status": None}
        
        db = next(get_db())
        subscription_info = PaymentService.get_subscription_info(x_user_id, db)
        
        if not subscription_info:
            return {"tier": "free", "status": None}
        
        return subscription_info
    except Exception as e:
        logger.error(f"Error getting subscription info: {str(e)}")
        # Return free tier on error instead of failing
        return {"tier": "free", "status": None}


@app.post("/api/webhooks/razorpay")
async def razorpay_webhook(request: Request):
    """
    Handle Razorpay webhook events.
    """
    try:
        payload = await request.body()
        sig_header = request.headers.get('x-razorpay-signature')
        
        # Verify webhook signature
        if not PaymentService.verify_webhook_signature(payload, sig_header):
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Parse payload
        event = json.loads(payload.decode('utf-8'))
        event_type = event.get('event')
        
        db = next(get_db())
        
        # Handle different event types
        if event_type == 'subscription.activated':
            PaymentService.handle_payment_authorized(event, db)
        elif event_type == 'subscription.charged':
            PaymentService.handle_payment_authorized(event, db)
        elif event_type == 'subscription.updated':
            PaymentService.handle_subscription_updated(event, db)
        elif event_type == 'subscription.cancelled':
            PaymentService.handle_subscription_cancelled(event, db)
        elif event_type == 'subscription.completed':
            PaymentService.handle_subscription_cancelled(event, db)
        elif event_type == 'subscription.halted':
            PaymentService.handle_subscription_cancelled(event, db)
        
        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook handler failed")


# Catch-all route to serve frontend for SPA routing (must be last)
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve frontend index.html for all non-API routes to support SPA routing.
    This handles page reloads and direct navigation to app routes.
    """
    if FRONTEND_DIST.exists():
        index_file = FRONTEND_DIST / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
    
    # If frontend not found, return 404
    raise HTTPException(status_code=404, detail="Frontend not found")
