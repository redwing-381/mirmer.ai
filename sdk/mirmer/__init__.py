"""
Mirmer AI Python SDK

A Python client library for the Mirmer AI multi-LLM consultation system.
"""

from mirmer._version import __version__
from mirmer.client import Client
from mirmer.async_client import AsyncClient
from mirmer.models import (
    CouncilResponse,
    CouncilUpdate,
    Conversation,
    Message,
    UsageStats,
    ModelResponse,
    ModelRanking,
    AggregateRanking,
    ChairmanSynthesis,
)
from mirmer.exceptions import (
    MirmerError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ConnectionError,
    APIError,
)
from mirmer import auth

__all__ = [
    "__version__",
    "Client",
    "AsyncClient",
    "CouncilResponse",
    "CouncilUpdate",
    "Conversation",
    "Message",
    "UsageStats",
    "ModelResponse",
    "ModelRanking",
    "AggregateRanking",
    "ChairmanSynthesis",
    "MirmerError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "NotFoundError",
    "ConnectionError",
    "APIError",
    "auth",
]
