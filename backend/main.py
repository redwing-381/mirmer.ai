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
    """Initialize database and validate configuration on application startup."""
    import os
    from database import init_db, check_connection
    from config import validate_production_config
    from firebase_auth import initialize_firebase
    
    # Initialize Firebase Admin SDK
    initialize_firebase()
    
    # Validate configuration
    logger.info("=" * 60)
    logger.info("🚀 Mirmer AI Backend Starting...")
    logger.info("=" * 60)
    
    config_result = validate_production_config()
    
    if not config_result['valid']:
        logger.error("=" * 60)
        logger.error("❌ CONFIGURATION VALIDATION FAILED")
        logger.error("=" * 60)
        for error in config_result['errors']:
            logger.error(f"  ❌ {error}")
        logger.error("=" * 60)
        raise RuntimeError("Configuration validation failed. Please check environment variables.")
    
    if config_result['warnings']:
        logger.warning("⚠️  Configuration has warnings but will continue...")
    
    DATABASE_URL = os.getenv('DATABASE_URL')
    IS_PRODUCTION = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('VERCEL')
    
    if not DATABASE_URL:
        if IS_PRODUCTION:
            logger.error("✗ CRITICAL: DATABASE_URL not set in production environment!")
            logger.error("✗ Application cannot start without database configuration")
            raise RuntimeError("DATABASE_URL environment variable is required in production")
        else:
            logger.info("ℹ️  No DATABASE_URL found - using JSON file storage (development mode)")
            logger.info("=" * 60)
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


@app.post("/api/usage/test-increment")
async def test_increment(x_user_id: str = Header(...)):
    """Test endpoint to manually increment usage (for debugging)."""
    try:
        logger.info(f"🧪 TEST: Incrementing usage for user: {x_user_id}")
        success = usage.increment_usage(x_user_id)
        stats = usage.get_usage_stats(x_user_id)
        return {
            "success": success,
            "stats": stats,
            "message": "Increment test completed"
        }
    except Exception as e:
        logger.error(f"Error in test increment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/migrate-subscription-fields")
async def migrate_subscription_fields(admin_key: str = Header(None, alias="x-admin-key")):
    """Admin endpoint to run database migration for subscription fields."""
    # Simple admin key check (set ADMIN_KEY environment variable)
    expected_key = os.getenv('ADMIN_KEY')
    if not expected_key or admin_key != expected_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        logger.info("🔧 Running subscription fields migration...")
        from migrate_add_subscription_fields import migrate
        success = migrate()
        
        if success:
            return {
                "success": True,
                "message": "Migration completed successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Migration failed - check logs")
    except Exception as e:
        logger.error(f"Error running migration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/fix-user-subscription")
async def fix_user_subscription(
    user_id: str,
    admin_key: str = Header(None, alias="x-admin-key")
):
    """Admin endpoint to manually upgrade a user to Pro tier."""
    # Simple admin key check (set ADMIN_KEY environment variable)
    expected_key = os.getenv('ADMIN_KEY')
    if not expected_key or admin_key != expected_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        from models import Usage
        from datetime import datetime
        
        db = next(get_db())
        
        # Find user
        usage = db.query(Usage).filter(Usage.user_id == user_id).first()
        
        if not usage:
            raise HTTPException(status_code=404, detail=f"User not found: {user_id}")
        
        # Log before state
        logger.info(f"📊 Before: User {user_id} - Tier: {usage.tier}, Limits: {usage.daily_limit}/{usage.monthly_limit}")
        
        # Update to Pro
        usage.tier = 'pro'
        usage.daily_limit = 100
        usage.monthly_limit = 3000
        usage.subscription_status = 'active'
        usage.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Log after state
        logger.info(f"✅ After: User {user_id} - Tier: {usage.tier}, Limits: {usage.daily_limit}/{usage.monthly_limit}")
        
        return {
            "success": True,
            "message": "User upgraded to Pro successfully",
            "user_id": user_id,
            "tier": usage.tier,
            "daily_limit": usage.daily_limit,
            "monthly_limit": usage.monthly_limit
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fixing user subscription: {str(e)}")
        if db:
            db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)



import storage
import usage
from payments import PaymentService, RAZORPAY_PLAN_IDS
from fastapi import Request
from fastapi.responses import Response
from database import get_db
import json
from export_service import ExportService, generate_export_filename
from firebase_auth import extract_user_id


@app.post("/api/conversations", response_model=ConversationResponse)
async def create_conversation(x_user_id: str = Header(...)):
    """
    Create a new conversation for a specific user.
    
    Requirements: 8.4, 8.5
    """
    from firebase_auth import extract_user_id
    user_id = extract_user_id(x_user_id)
    
    try:
        conversation = storage.create_conversation(user_id=user_id)
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
    user_id = extract_user_id(x_user_id)
    try:
        conversations = storage.list_conversations(user_id=user_id)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list conversations")


@app.get("/api/conversations/search")
async def search_conversations(q: str, x_user_id: str = Header(...)):
    """
    Search conversations by title and message content.
    
    Args:
        q: Search query string
        x_user_id: Firebase user ID from header
    
    Returns:
        List of matching conversations with snippets
    
    Requirements: 2.1
    """
    try:
        if not q or not q.strip():
            return {"results": []}
        
        results = storage.search_conversations(user_id=x_user_id, query=q)
        return {"results": results, "query": q, "count": len(results)}
        
    except Exception as e:
        logger.error(f"Error searching conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")


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
import council


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: MessageRequest, x_user_id: str = Header(...)):
    """
    Send message and stream 3-stage council process via Server-Sent Events.
    
    Requirements: 2.3, 2.4, 3.1, 4.3, 6.2, 9.4
    """
    user_id = extract_user_id(x_user_id)
    
    async def event_generator():
        try:
            # Check rate limits
            allowed, error_msg = usage.check_rate_limit(user_id)
            if not allowed:
                yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
                return
            
            # Validate conversation exists and belongs to user
            conversation = storage.get_conversation(conversation_id, user_id=user_id)
            if not conversation:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Conversation not found'})}\n\n"
                return
            
            # Add user message to conversation
            storage.add_user_message(conversation_id, request.content, user_id=user_id)
            
            # Increment usage count
            logger.info(f"📊 Incrementing usage for user: {user_id}")
            increment_success = usage.increment_usage(user_id)
            if increment_success:
                logger.info(f"✅ Usage increment successful for user: {user_id}")
            else:
                logger.error(f"❌ Usage increment failed for user: {user_id}")
            
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
            
            # DIAGNOSTIC: Log stage data before saving
            logger.info(f"💾 Saving assistant message for conversation {conversation_id}")
            logger.info(f"  Stage 1: {len(stage1_results)} responses")
            logger.info(f"  Stage 2: {len(stage2_results)} rankings")
            logger.info(f"  Stage 3: {len(stage3_result.get('response', ''))} chars")
            logger.debug(f"  Stage 1 data: {stage1_results}")
            logger.debug(f"  Stage 2 data: {stage2_results}")
            logger.debug(f"  Stage 3 data: {stage3_result}")
            
            storage.add_assistant_message(
                conversation_id=conversation_id,
                stage1=stage1_results,
                stage2=stage2_results,
                stage3=stage3_result,
                user_id=user_id,
                metadata=metadata
            )
            
            logger.info(f"✅ Assistant message saved successfully")
            
            # Update conversation title if this is the first message
            if len(conversation["messages"]) == 0:
                # Generate simple title from first few words
                title_words = request.content.split()[:8]
                title = " ".join(title_words)
                if len(request.content.split()) > 8:
                    title += "..."
                storage.update_conversation_title(conversation_id, title, user_id=user_id)
            
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


@app.get("/api/conversations/{conversation_id}/export/markdown")
async def export_conversation_markdown(conversation_id: str, x_user_id: str = Header(...)):
    """
    Export conversation to Markdown format.
    
    Requirements: 3.2
    """
    try:
        # Get conversation
        conversation = storage.get_conversation(conversation_id, user_id=x_user_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Generate Markdown
        markdown_content = ExportService.export_to_markdown(conversation)
        
        # Generate filename
        filename = generate_export_filename(conversation, 'markdown')
        
        # Return as downloadable file
        return Response(
            content=markdown_content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting conversation to Markdown: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to export conversation")


@app.get("/api/conversations/{conversation_id}/export/json")
async def export_conversation_json(conversation_id: str, x_user_id: str = Header(...)):
    """
    Export conversation to JSON format.
    
    Requirements: 3.4
    """
    try:
        # Get conversation
        conversation = storage.get_conversation(conversation_id, user_id=x_user_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Generate JSON
        json_content = ExportService.export_to_json(conversation)
        
        # Generate filename
        filename = generate_export_filename(conversation, 'json')
        
        # Return as downloadable file
        return Response(
            content=json_content,
            media_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting conversation to JSON: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to export conversation")


@app.get("/api/conversations/{conversation_id}/export/pdf")
async def export_conversation_pdf(conversation_id: str, x_user_id: str = Header(...)):
    """
    Export conversation to PDF format.
    
    Requirements: 3.3
    """
    try:
        # Get conversation
        logger.info(f"📄 Export: Retrieving conversation {conversation_id} for PDF export")
        conversation = storage.get_conversation(conversation_id, user_id=x_user_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # DIAGNOSTIC: Log conversation structure
        logger.info(f"📄 Export: Retrieved conversation with {len(conversation.get('messages', []))} messages")
        for i, msg in enumerate(conversation.get('messages', [])):
            if msg.get('role') == 'assistant':
                has_stage1 = bool(msg.get('stage1'))
                has_stage2 = bool(msg.get('stage2'))
                has_stage3 = bool(msg.get('stage3'))
                logger.info(f"  Message {i}: Assistant - Stage1: {has_stage1}, Stage2: {has_stage2}, Stage3: {has_stage3}")
                if has_stage1:
                    logger.info(f"    Stage 1: {len(msg.get('stage1', []))} responses")
                if has_stage2:
                    logger.info(f"    Stage 2: {len(msg.get('stage2', []))} rankings")
                if has_stage3:
                    logger.info(f"    Stage 3: {len(msg.get('stage3', {}).get('response', ''))} chars")
                logger.debug(f"    Full message data: {msg}")
        
        # Generate PDF
        try:
            pdf_bytes = ExportService.export_to_pdf(conversation)
        except ValueError as e:
            # User-friendly error for PDF generation issues
            logger.error(f"PDF generation failed for {conversation_id}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
        except ImportError as e:
            # Missing dependency error
            logger.error(f"PDF export dependency missing: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="PDF export is not available. Please contact support.")
        except Exception as e:
            logger.error(f"Unexpected error during PDF generation: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="An unexpected error occurred during PDF export")
        
        # Generate filename
        filename = generate_export_filename(conversation, 'pdf')
        
        logger.info(f"✅ PDF export completed successfully for {conversation_id} ({len(pdf_bytes)} bytes)")
        
        # Return as downloadable file
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting conversation to PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to export conversation")


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


@app.get("/api/payments/verify-subscription")
async def verify_subscription_status(x_user_id: str = Header(...)):
    """
    Verify subscription status with Razorpay and sync with local database.
    
    This endpoint fetches the subscription from Razorpay API and compares it with
    the local database. If there's a mismatch, it updates the local database.
    
    Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
    """
    try:
        db = next(get_db())
        result = PaymentService.verify_and_sync_subscription(x_user_id, db)
        
        return result
        
    except RuntimeError as e:
        # Database not configured
        if "Database not configured" in str(e):
            return {
                "success": True,
                "synced": False,
                "tier": "free",
                "status": None,
                "message": "Database not configured"
            }
        raise
        
    except Exception as e:
        logger.error(f"Error verifying subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to verify subscription")


@app.post("/api/webhooks/razorpay")
async def razorpay_webhook(request: Request):
    """
    Handle Razorpay webhook events with comprehensive logging and error handling.
    """
    db = None
    try:
        # Get raw payload and signature
        payload = await request.body()
        sig_header = request.headers.get('x-razorpay-signature')
        
        logger.info("=" * 60)
        logger.info("📥 Razorpay webhook received")
        logger.info(f"Signature header present: {bool(sig_header)}")
        logger.info(f"Payload size: {len(payload)} bytes")
        
        # Verify webhook signature
        signature_valid = PaymentService.verify_webhook_signature(payload, sig_header)
        logger.info(f"Signature verification result: {'✓ VALID' if signature_valid else '✗ INVALID'}")
        
        if not signature_valid:
            logger.error("❌ Webhook signature verification failed")
            logger.error(f"Request IP: {request.client.host if request.client else 'unknown'}")
            logger.error(f"Headers: {dict(request.headers)}")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Parse payload
        event = json.loads(payload.decode('utf-8'))
        event_type = event.get('event')
        
        logger.info(f"Event type: {event_type}")
        logger.info(f"Event payload: {json.dumps(event, indent=2)}")
        
        # Extract user_id with fallback logic
        subscription_entity = event.get('payload', {}).get('subscription', {}).get('entity', {})
        notes = subscription_entity.get('notes', {})
        user_id = notes.get('user_id')
        subscription_id = subscription_entity.get('id')
        
        logger.info(f"Extracted user_id from notes: {user_id}")
        logger.info(f"Extracted subscription_id: {subscription_id}")
        
        # Get database session
        db = next(get_db())
        
        # If user_id not in notes, try to find by subscription_id
        if not user_id and subscription_id:
            logger.warning("⚠️  user_id not found in webhook notes, attempting fallback lookup by subscription_id")
            from models import Usage
            usage = db.query(Usage).filter(Usage.razorpay_subscription_id == subscription_id).first()
            if usage:
                user_id = usage.user_id
                logger.info(f"✓ Found user_id via subscription_id lookup: {user_id}")
            else:
                logger.error(f"❌ Could not find user with subscription_id: {subscription_id}")
        
        if not user_id:
            logger.error("❌ Unable to extract user_id from webhook payload")
            logger.error(f"Event: {event_type}, Subscription ID: {subscription_id}")
            raise HTTPException(status_code=400, detail="Missing user_id in webhook payload")
        
        # Log before state
        from models import Usage
        usage_before = db.query(Usage).filter(Usage.user_id == user_id).first()
        if usage_before:
            logger.info(f"📊 Before state - User: {user_id}, Tier: {usage_before.tier}, "
                       f"Status: {usage_before.subscription_status}, "
                       f"Limits: {usage_before.daily_limit}/{usage_before.monthly_limit}")
        else:
            logger.info(f"📊 Before state - User {user_id} not found in database (will be created)")
        
        # Handle different event types with transaction management
        success = False
        try:
            if event_type == 'subscription.activated':
                logger.info(f"🔄 Processing subscription.activated for user {user_id}")
                success = PaymentService.handle_payment_authorized(event, db)
            elif event_type == 'subscription.charged':
                logger.info(f"🔄 Processing subscription.charged for user {user_id}")
                success = PaymentService.handle_payment_authorized(event, db)
            elif event_type == 'subscription.updated':
                logger.info(f"🔄 Processing subscription.updated for user {user_id}")
                success = PaymentService.handle_subscription_updated(event, db)
            elif event_type == 'subscription.cancelled':
                logger.info(f"🔄 Processing subscription.cancelled for user {user_id}")
                success = PaymentService.handle_subscription_cancelled(event, db)
            elif event_type == 'subscription.completed':
                logger.info(f"🔄 Processing subscription.completed for user {user_id}")
                success = PaymentService.handle_subscription_cancelled(event, db)
            elif event_type == 'subscription.halted':
                logger.info(f"🔄 Processing subscription.halted for user {user_id}")
                success = PaymentService.handle_subscription_cancelled(event, db)
            else:
                logger.warning(f"⚠️  Unhandled event type: {event_type}")
                return {"status": "ignored", "event_type": event_type}
            
            if not success:
                logger.error(f"❌ Handler returned False for event {event_type}")
                db.rollback()
                raise HTTPException(status_code=500, detail="Handler failed to process event")
            
            # Log after state
            usage_after = db.query(Usage).filter(Usage.user_id == user_id).first()
            if usage_after:
                logger.info(f"📊 After state - User: {user_id}, Tier: {usage_after.tier}, "
                           f"Status: {usage_after.subscription_status}, "
                           f"Limits: {usage_after.daily_limit}/{usage_after.monthly_limit}")
                logger.info(f"✅ Subscription update successful for user {user_id}")
            else:
                logger.error(f"❌ User {user_id} not found after update")
            
            logger.info("=" * 60)
            return {"status": "success", "event_type": event_type, "user_id": user_id}
            
        except Exception as handler_error:
            logger.error(f"❌ Error in event handler: {str(handler_error)}")
            logger.error(f"Event type: {event_type}, User: {user_id}")
            if db:
                db.rollback()
                logger.info("🔄 Database transaction rolled back")
            raise
            
    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        logger.error(f"❌ Failed to parse webhook payload as JSON: {str(e)}")
        logger.error(f"Payload: {payload.decode('utf-8', errors='replace')[:500]}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        logger.error(f"❌ Unexpected error handling webhook: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        if db:
            db.rollback()
            logger.info("🔄 Database transaction rolled back")
        raise HTTPException(status_code=500, detail="Webhook handler failed")
    finally:
        if db:
            db.close()


# Enterprise contact endpoint
class EnterpriseInquiry(BaseModel):
    name: str
    email: str
    company: str
    companySize: str
    phone: Optional[str] = None
    message: str
    useCase: Optional[str] = None


@app.post("/api/enterprise/contact")
async def submit_enterprise_inquiry(inquiry: EnterpriseInquiry):
    """
    Handle enterprise contact form submissions.
    Sends confirmation email to submitter and notification to admin.
    """
    try:
        from email_service import email_service
        
        logger.info(f"Received enterprise inquiry from {inquiry.email} at {inquiry.company}")
        
        # Send confirmation email to submitter
        confirmation_sent = email_service.send_enterprise_inquiry_confirmation(
            email=inquiry.email,
            name=inquiry.name
        )
        
        # Send notification to admin
        admin_notified = email_service.send_enterprise_inquiry_notification(
            name=inquiry.name,
            email=inquiry.email,
            company=inquiry.company,
            company_size=inquiry.companySize,
            phone=inquiry.phone,
            message=inquiry.message,
            use_case=inquiry.useCase
        )
        
        logger.info(f"Enterprise inquiry processed - Confirmation: {confirmation_sent}, Admin notified: {admin_notified}")
        
        return {
            "status": "success",
            "message": "Thank you for your inquiry. We'll be in touch soon!"
        }
        
    except Exception as e:
        logger.error(f"Error processing enterprise inquiry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process inquiry")


class ContactRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str


@app.post("/api/contact")
async def submit_contact_request(contact: ContactRequest):
    """
    Handle general contact form submissions.
    Sends confirmation email to submitter and notification to admin.
    """
    try:
        from email_service import email_service
        
        logger.info(f"Received contact request from {contact.email}")
        
        # Send notification to admin
        admin_notified = email_service.send_contact_notification(
            name=contact.name,
            email=contact.email,
            subject=contact.subject,
            message=contact.message
        )
        
        # Send confirmation to user
        confirmation_sent = email_service.send_contact_confirmation(
            email=contact.email,
            name=contact.name
        )
        
        logger.info(f"Contact request processed - Confirmation: {confirmation_sent}, Admin notified: {admin_notified}")
        
        return {
            "status": "success",
            "message": "Thank you for contacting us. We'll respond within 24 hours!"
        }
        
    except Exception as e:
        logger.error(f"Error processing contact request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send message")


class SubscriptionSupportRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str


@app.post("/api/subscription/support")
async def submit_subscription_support(request: SubscriptionSupportRequest, x_user_id: str = Header(...)):
    """
    Handle subscription support requests.
    Sends email to admin with user's support request.
    """
    try:
        from email_service import email_service
        
        logger.info(f"Received subscription support request from {request.email} - Subject: {request.subject}")
        
        # Send notification to admin
        admin_notified = email_service.send_subscription_support_notification(
            name=request.name,
            email=request.email,
            user_id=x_user_id,
            subject=request.subject,
            message=request.message
        )
        
        logger.info(f"Subscription support request processed - Admin notified: {admin_notified}")
        
        return {
            "status": "success",
            "message": "Your support request has been received. We'll respond within 24 hours."
        }
        
    except Exception as e:
        logger.error(f"Error processing subscription support request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process support request")


@app.get("/auth/cli")
async def cli_auth(callback: str):
    """
    CLI authentication page.
    Opens Firebase auth, then redirects to callback with token.
    
    Args:
        callback: The local callback URL where the CLI is listening
    
    Returns:
        HTML page that handles Firebase authentication
    """
    # Try to serve from backend/static (for Railway deployment)
    static_cli_auth = Path(__file__).parent / "static" / "cli-auth.html"
    if static_cli_auth.exists():
        return FileResponse(static_cli_auth)
    
    # Try to serve from dist (production with frontend build)
    dist_cli_auth = FRONTEND_DIST / "cli-auth.html"
    if dist_cli_auth.exists():
        return FileResponse(dist_cli_auth)
    
    # Fallback: serve from public (development)
    cli_auth_file = Path(__file__).parent.parent / "frontend" / "public" / "cli-auth.html"
    if cli_auth_file.exists():
        return FileResponse(cli_auth_file)
        
    raise HTTPException(status_code=404, detail="CLI auth page not found. Run 'npm run build' in frontend directory.")


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
