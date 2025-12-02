"""
Authentication utilities for Mirmer AI SDK.

Provides CLI authentication flow with browser-based Google Sign-In.
"""

import json
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse


class AuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""

    token = None

    def do_GET(self):
        """Handle GET request from OAuth callback."""
        # Parse the callback URL
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if "token" in params:
            AuthCallbackHandler.token = params["token"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_response = """
                <html>
                <head><title>Authentication Successful</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1>&#x2705; Authentication Successful!</h1>
                    <p>You can close this window and return to your terminal.</p>
                </body>
                </html>
                """
            self.wfile.write(html_response.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authentication Failed</h1></body></html>")

    def log_message(self, format, *args):
        """Suppress log messages."""
        pass


def get_config_dir() -> Path:
    """Get the configuration directory for storing credentials."""
    config_dir = Path.home() / ".mirmer"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_credentials_file() -> Path:
    """Get the path to the credentials file."""
    return get_config_dir() / "credentials.json"


def save_credentials(token: str, user_email: Optional[str] = None) -> None:
    """
    Save credentials to local file.

    Args:
        token: Firebase ID token
        user_email: User's email address (optional)
    """
    credentials = {"token": token}
    if user_email:
        credentials["email"] = user_email

    creds_file = get_credentials_file()
    with open(creds_file, "w") as f:
        json.dump(credentials, f)

    # Set file permissions to user-only
    os.chmod(creds_file, 0o600)


def load_credentials() -> Optional[dict]:
    """
    Load credentials from local file.

    Returns:
        Dictionary with 'token' and optionally 'email', or None if not found
    """
    creds_file = get_credentials_file()
    if not creds_file.exists():
        return None

    try:
        with open(creds_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def clear_credentials() -> None:
    """Clear stored credentials."""
    creds_file = get_credentials_file()
    if creds_file.exists():
        creds_file.unlink()


def login(base_url: str = "https://mirmer-ai.vercel.app", port: int = 8765) -> str:
    """
    Authenticate user via browser-based Google Sign-In.

    Opens a browser window for the user to sign in with Google,
    then captures the Firebase token via callback.

    Args:
        base_url: Base URL of the Mirmer AI application
        port: Local port for OAuth callback (default: 8765)

    Returns:
        Firebase ID token

    Raises:
        RuntimeError: If authentication fails
    """
    print("🔐 Authenticating with Mirmer AI...")
    print(f"Opening browser for Google Sign-In...")

    # Start local server for callback
    server = HTTPServer(("localhost", port), AuthCallbackHandler)

    # Build auth URL
    callback_url = f"http://localhost:{port}/callback"
    auth_url = f"{base_url}/auth/cli?callback={callback_url}"

    # Open browser
    webbrowser.open(auth_url)

    print(f"Waiting for authentication...")
    print(f"If browser doesn't open, visit: {auth_url}")

    # Wait for callback (with timeout)
    server.timeout = 120  # 2 minutes
    server.handle_request()

    if AuthCallbackHandler.token:
        token = AuthCallbackHandler.token
        save_credentials(token)
        print("✅ Authentication successful!")
        return token
    else:
        raise RuntimeError("Authentication failed or timed out")


def get_token() -> Optional[str]:
    """
    Get authentication token.

    Checks in order:
    1. MIRMER_API_KEY environment variable (takes precedence for testing/override)
    2. Stored credentials file

    Returns:
        Token string or None if not found
    """
    # Check environment variable first (allows override)
    env_token = os.getenv("MIRMER_API_KEY")
    if env_token:
        return env_token

    # Check stored credentials
    creds = load_credentials()
    if creds and "token" in creds:
        return creds["token"]

    return None


def ensure_authenticated(base_url: str = "https://mirmer-ai.vercel.app") -> str:
    """
    Ensure user is authenticated, prompting for login if needed.

    Args:
        base_url: Base URL of the Mirmer AI application

    Returns:
        Firebase ID token

    Raises:
        RuntimeError: If authentication fails
    """
    token = get_token()
    if token:
        return token

    print("No authentication found. Please sign in.")
    return login(base_url)
