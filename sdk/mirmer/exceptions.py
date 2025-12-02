"""Exception classes for Mirmer AI SDK."""

from datetime import datetime
from typing import Optional


class MirmerError(Exception):
    """Base exception for all Mirmer SDK errors."""

    pass


class AuthenticationError(MirmerError):
    """Raised when API key is invalid or missing."""

    def __init__(self, message: str = "Authentication failed. Please check your API key."):
        super().__init__(message)


class RateLimitError(MirmerError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, reset_time: Optional[datetime] = None):
        super().__init__(message)
        self.reset_time = reset_time


class ValidationError(MirmerError):
    """Raised when request parameters are invalid."""

    def __init__(self, message: str = "Invalid request parameters."):
        super().__init__(message)


class NotFoundError(MirmerError):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found."):
        super().__init__(message)


class ConnectionError(MirmerError):
    """Raised when network connection fails."""

    def __init__(
        self,
        message: str = "Network connection failed. Please check your internet connection and try again.",
    ):
        super().__init__(message)


class APIError(MirmerError):
    """Raised for general API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
