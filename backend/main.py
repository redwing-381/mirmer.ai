"""
FastAPI backend for Mirmer AI multi-LLM consultation system.
"""
import logging
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
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
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)



import storage


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
import council


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: MessageRequest, x_user_id: str = Header(...)):
    """
    Send message and stream 3-stage council process via Server-Sent Events.
    
    Requirements: 2.3, 2.4, 3.1, 4.3, 6.2, 9.4
    """
    
    async def event_generator():
        try:
            # Validate conversation exists and belongs to user
            conversation = storage.get_conversation(conversation_id, user_id=x_user_id)
            if not conversation:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Conversation not found'})}\n\n"
                return
            
            # Add user message to conversation
            storage.add_user_message(conversation_id, request.content, user_id=x_user_id)
            
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
