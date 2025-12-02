"""Data models for Mirmer AI SDK."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelResponse(BaseModel):
    """Individual model response from Stage 1."""

    model: str = Field(..., description="Model identifier")
    response: str = Field(..., description="Model's response text")


class ModelRanking(BaseModel):
    """Model ranking from Stage 2."""

    model: str = Field(..., description="Model identifier")
    ranking: str = Field(..., description="Full ranking text from the model")
    parsed_ranking: List[str] = Field(
        default_factory=list, description="Parsed list of response labels in ranked order"
    )


class AggregateRanking(BaseModel):
    """Aggregate ranking result."""

    model: str = Field(..., description="Model identifier")
    average_rank: float = Field(..., description="Average position across all rankings (lower is better)")
    rankings_count: int = Field(..., description="Number of times this model was ranked")


class ChairmanSynthesis(BaseModel):
    """Chairman synthesis from Stage 3."""

    model: str = Field(..., description="Chairman model identifier")
    response: str = Field(..., description="Synthesized final answer")


class CouncilResponse(BaseModel):
    """Complete council response with all three stages."""

    conversation_id: str = Field(..., description="ID of the conversation")
    stage1: List[ModelResponse] = Field(..., description="Individual model responses from Stage 1")
    stage2: List[ModelRanking] = Field(..., description="Peer rankings from Stage 2")
    stage3: ChairmanSynthesis = Field(..., description="Chairman synthesis from Stage 3")
    aggregate_rankings: List[AggregateRanking] = Field(
        ..., description="Aggregate rankings across all peer reviews"
    )
    label_to_model: Dict[str, str] = Field(
        ..., description="Mapping from response labels to model names"
    )


class CouncilUpdate(BaseModel):
    """Real-time update from streaming council process."""

    type: str = Field(
        ...,
        description="Event type: stage1_start, stage1_complete, stage2_start, stage2_complete, stage3_start, stage3_complete, complete, error",
    )
    data: Optional[Any] = Field(None, description="Event data payload (can be dict, list, or other types)")
    error: Optional[str] = Field(None, description="Error message if type is 'error'")


class Message(BaseModel):
    """A single message in a conversation."""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content text")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    stage1: Optional[List[ModelResponse]] = Field(None, description="Stage 1 responses (assistant only)")
    stage2: Optional[List[ModelRanking]] = Field(None, description="Stage 2 rankings (assistant only)")
    stage3: Optional[ChairmanSynthesis] = Field(None, description="Stage 3 synthesis (assistant only)")


class Conversation(BaseModel):
    """A conversation with messages."""

    id: str = Field(..., description="Conversation ID")
    title: str = Field(..., description="Conversation title")
    created_at: str = Field(..., description="ISO 8601 timestamp of creation")
    messages: List[Message] = Field(default_factory=list, description="List of messages in the conversation")


class UsageStats(BaseModel):
    """User's API usage statistics."""

    queries_used_today: int = Field(..., description="Number of queries used today")
    daily_limit: int = Field(..., description="Daily query limit")
    tier: str = Field(..., description="Subscription tier: 'free', 'pro', or 'enterprise'")
    reset_time: str = Field(..., description="ISO 8601 timestamp when usage resets")
