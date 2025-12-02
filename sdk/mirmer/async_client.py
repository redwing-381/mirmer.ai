"""Asynchronous client for Mirmer AI API."""

import os
from typing import AsyncIterator, List, Optional
from urllib.parse import quote, urljoin

import httpx

from mirmer.exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from mirmer.models import (
    Conversation,
    CouncilResponse,
    CouncilUpdate,
    UsageStats,
)


class AsyncClient:
    """Asynchronous client for Mirmer AI API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://mirmerai-production.up.railway.app",
        timeout: float = 60.0,
        max_retries: int = 3,
    ):
        """
        Initialize async client with authentication and configuration.

        Args:
            api_key: Mirmer AI API key. If not provided, reads from MIRMER_API_KEY environment variable.
            base_url: Base URL for the Mirmer AI API.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts for failed requests.

        Raises:
            AuthenticationError: If no API key is provided or found in environment.
            ValidationError: If configuration parameters are invalid.
        """
        # Validate configuration
        if timeout <= 0:
            raise ValidationError("Timeout must be greater than 0")
        if max_retries < 0:
            raise ValidationError("Max retries must be non-negative")

        # Validate base URL format
        if not base_url.startswith(("http://", "https://")):
            raise ValidationError("Base URL must start with http:// or https://")

        # Resolve API key
        self._api_key = api_key or os.getenv("MIRMER_API_KEY")
        if not self._api_key:
            raise AuthenticationError(
                "No API key provided. Pass api_key parameter or set MIRMER_API_KEY environment variable."
            )

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

        # Initialize async HTTP client
        self._client = httpx.AsyncClient(
            timeout=timeout,
            transport=httpx.AsyncHTTPTransport(retries=max_retries),
        )

    def __repr__(self) -> str:
        """Return string representation without exposing API key."""
        return f"AsyncClient(base_url='{self._base_url}', timeout={self._timeout})"

    def __str__(self) -> str:
        """Return string representation without exposing API key."""
        return f"Mirmer AI AsyncClient (base_url={self._base_url})"

    def _get_headers(self) -> dict:
        """Get headers for API requests including authentication."""
        return {
            "x-user-id": self._api_key,
            "Content-Type": "application/json",
        }

    def _build_url(self, path: str) -> str:
        """Build full URL from path."""
        return urljoin(self._base_url, path)

    def _handle_response_error(self, response: httpx.Response) -> None:
        """
        Handle HTTP error responses and raise appropriate exceptions.

        Args:
            response: HTTP response object

        Raises:
            AuthenticationError: For 401/403 status codes
            NotFoundError: For 404 status code
            RateLimitError: For 429 status code
            ValidationError: For 400 status code
            APIError: For other error status codes
        """
        if response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError("Invalid API key or unauthorized access")
        elif response.status_code == 404:
            raise NotFoundError("Resource not found")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded. Please try again later.")
        elif response.status_code == 400:
            try:
                error_data = response.json()
                message = error_data.get("detail", "Invalid request parameters")
            except Exception:
                message = "Invalid request parameters"
            raise ValidationError(message)
        elif response.status_code >= 500:
            raise APIError(
                f"Server error: {response.status_code}",
                status_code=response.status_code,
            )
        else:
            raise APIError(
                f"API error: {response.status_code}",
                status_code=response.status_code,
            )

    async def close(self) -> None:
        """Close HTTP connections."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit with cleanup."""
        await self.close()

    # Query and streaming methods
    async def query(
        self,
        message: str,
        conversation_id: Optional[str] = None,
    ) -> CouncilResponse:
        """
        Send a query and wait for complete council response.

        Args:
            message: The query message to send
            conversation_id: Optional conversation ID to add message to existing conversation.
                           If not provided, a new conversation will be created.

        Returns:
            CouncilResponse with all three stages completed

        Raises:
            ValidationError: If message is empty or invalid
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit is exceeded
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        # Validate parameters
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")

        # Create conversation if not provided
        if not conversation_id:
            conv = await self.create_conversation()
            conversation_id = conv.id

        # Collect all streaming updates
        stage1_data = None
        stage2_data = None
        stage3_data = None
        aggregate_rankings = None
        label_to_model = None

        async for update in self.stream(message, conversation_id):
            if update.type == "stage1_complete" and update.data:
                stage1_data = update.data
            elif update.type == "stage2_complete" and update.data:
                stage2_data = update.data
                aggregate_rankings = update.data.get("aggregate_rankings", [])
                label_to_model = update.data.get("label_to_model", {})
            elif update.type == "stage3_complete" and update.data:
                stage3_data = update.data
            elif update.type == "error":
                raise APIError(update.error or "Unknown error occurred")

        # Build response
        from mirmer.models import (
            AggregateRanking,
            ChairmanSynthesis,
            ModelRanking,
            ModelResponse,
        )

        return CouncilResponse(
            conversation_id=conversation_id,
            stage1=[ModelResponse(**item) for item in stage1_data] if stage1_data else [],
            stage2=[
                ModelRanking(**item) for item in stage2_data.get("rankings", [])
            ]
            if stage2_data
            else [],
            stage3=ChairmanSynthesis(**stage3_data) if stage3_data else ChairmanSynthesis(model="", response=""),
            aggregate_rankings=[AggregateRanking(**item) for item in aggregate_rankings]
            if aggregate_rankings
            else [],
            label_to_model=label_to_model or {},
        )

    async def stream(
        self,
        message: str,
        conversation_id: Optional[str] = None,
    ) -> AsyncIterator[CouncilUpdate]:
        """
        Stream council process updates in real-time.

        Args:
            message: The query message to send
            conversation_id: Optional conversation ID to add message to existing conversation.
                           If not provided, a new conversation will be created.

        Yields:
            CouncilUpdate objects as each stage progresses

        Raises:
            ValidationError: If message is empty or invalid
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit is exceeded
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        # Validate parameters
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")

        # Create conversation if not provided
        if not conversation_id:
            conv = await self.create_conversation()
            conversation_id = conv.id

        # Build request
        url = self._build_url(f"/api/conversations/{conversation_id}/message/stream")
        headers = self._get_headers()
        payload = {"content": message}

        try:
            # Open SSE stream
            async with self._client.stream(
                "POST",
                url,
                headers=headers,
                json=payload,
            ) as response:
                # Check for errors
                if response.status_code != 200:
                    self._handle_response_error(response)

                # Parse SSE events
                import json

                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue

                    # SSE format: "data: {json}"
                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix
                        try:
                            event_data = json.loads(data_str)
                            yield CouncilUpdate(**event_data)
                        except json.JSONDecodeError:
                            # Skip malformed JSON
                            continue

        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except httpx.TimeoutException:
            raise ConnectionError("Request timed out")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error occurred: {str(e)}")

    # Conversation management methods
    async def create_conversation(self, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation.

        Args:
            title: Optional title for the conversation. If not provided, a default title will be used.

        Returns:
            Conversation object with the new conversation details

        Raises:
            AuthenticationError: If API key is invalid
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        url = self._build_url("/api/conversations")
        headers = self._get_headers()

        try:
            response = await self._client.post(url, headers=headers)

            if response.status_code != 200:
                self._handle_response_error(response)

            data = response.json()
            # Convert to full Conversation object
            return Conversation(
                id=data["id"],
                title=data.get("title", "New Conversation"),
                created_at=data["created_at"],
                messages=[],
            )

        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except httpx.TimeoutException:
            raise ConnectionError("Request timed out")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error occurred: {str(e)}")

    async def list_conversations(self) -> List[Conversation]:
        """
        List all conversations for the authenticated user.

        Returns:
            List of Conversation objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        url = self._build_url("/api/conversations")
        headers = self._get_headers()

        try:
            response = await self._client.get(url, headers=headers)

            if response.status_code != 200:
                self._handle_response_error(response)

            data = response.json()
            conversations = data.get("conversations", [])

            return [Conversation(**conv) for conv in conversations]

        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except httpx.TimeoutException:
            raise ConnectionError("Request timed out")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error occurred: {str(e)}")

    async def get_conversation(self, conversation_id: str) -> Conversation:
        """
        Get a specific conversation with all messages.

        Args:
            conversation_id: ID of the conversation to retrieve

        Returns:
            Conversation object with all messages

        Raises:
            ValidationError: If conversation_id is empty
            NotFoundError: If conversation is not found
            AuthenticationError: If API key is invalid
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        if not conversation_id or not conversation_id.strip():
            raise ValidationError("Conversation ID cannot be empty")

        url = self._build_url(f"/api/conversations/{conversation_id}")
        headers = self._get_headers()

        try:
            response = await self._client.get(url, headers=headers)

            if response.status_code != 200:
                self._handle_response_error(response)

            data = response.json()
            return Conversation(**data)

        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except httpx.TimeoutException:
            raise ConnectionError("Request timed out")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error occurred: {str(e)}")

    async def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.

        Args:
            conversation_id: ID of the conversation to delete

        Returns:
            True if deletion was successful

        Raises:
            ValidationError: If conversation_id is empty
            NotFoundError: If conversation is not found
            AuthenticationError: If API key is invalid
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        if not conversation_id or not conversation_id.strip():
            raise ValidationError("Conversation ID cannot be empty")

        url = self._build_url(f"/api/conversations/{conversation_id}")
        headers = self._get_headers()

        try:
            response = await self._client.delete(url, headers=headers)

            if response.status_code != 200:
                self._handle_response_error(response)

            data = response.json()
            return data.get("success", False)

        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except httpx.TimeoutException:
            raise ConnectionError("Request timed out")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error occurred: {str(e)}")

    # Search and usage methods
    async def search_conversations(self, query: str) -> List[Conversation]:
        """
        Search conversations by title and content.

        Args:
            query: Search query string

        Returns:
            List of matching Conversation objects. Returns empty list if no matches found.

        Raises:
            ValidationError: If query is None (empty strings are allowed and return all conversations)
            AuthenticationError: If API key is invalid
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        if query is None:
            raise ValidationError("Query cannot be None")

        # Empty query returns all conversations per requirements
        if not query.strip():
            return await self.list_conversations()

        # URL encode the query parameter
        encoded_query = quote(query)
        url = self._build_url(f"/api/conversations/search?q={encoded_query}")
        headers = self._get_headers()

        try:
            response = await self._client.get(url, headers=headers)

            if response.status_code != 200:
                self._handle_response_error(response)

            data = response.json()
            results = data.get("results", [])

            return [Conversation(**conv) for conv in results]

        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except httpx.TimeoutException:
            raise ConnectionError("Request timed out")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error occurred: {str(e)}")

    async def get_usage(self) -> UsageStats:
        """
        Get current usage statistics.

        Returns:
            UsageStats object with queries used, daily limit, tier, and reset time

        Raises:
            AuthenticationError: If API key is invalid
            APIError: For other API errors
            ConnectionError: If network connection fails
        """
        url = self._build_url("/api/usage")
        headers = self._get_headers()

        try:
            response = await self._client.get(url, headers=headers)

            if response.status_code != 200:
                self._handle_response_error(response)

            data = response.json()
            return UsageStats(**data)

        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except httpx.TimeoutException:
            raise ConnectionError("Request timed out")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error occurred: {str(e)}")
