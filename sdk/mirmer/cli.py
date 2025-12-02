"""
Command-line interface for Mirmer AI SDK.

Provides a CLI tool for interacting with Mirmer AI from the terminal.
"""

import os
import sys
from typing import Optional

import click

from mirmer import Client
from mirmer.auth import ensure_authenticated, clear_credentials, get_token
from mirmer.exceptions import MirmerError


@click.group()
@click.option("--api-key", envvar="MIRMER_API_KEY", help="API key for authentication (or set MIRMER_API_KEY env var)")
@click.option("--api-url", default="https://mirmerai-production.up.railway.app", help="Base URL of Mirmer AI API")
@click.pass_context
def cli(ctx, api_key, api_url):
    """Mirmer AI - Multi-LLM consultation system CLI."""
    ctx.ensure_object(dict)
    ctx.obj["api_key"] = api_key
    ctx.obj["api_url"] = api_url


@cli.command()
@click.pass_context
def login(ctx):
    """Sign in with Google."""
    base_url = ctx.obj["base_url"]
    try:
        from mirmer.auth import login as do_login

        token = do_login(base_url)
        click.echo(click.style("✅ Successfully signed in!", fg="green"))
    except Exception as e:
        click.echo(click.style(f"❌ Login failed: {e}", fg="red"))
        sys.exit(1)


@cli.command()
def logout():
    """Sign out and clear stored credentials."""
    clear_credentials()
    click.echo(click.style("✅ Signed out successfully", fg="green"))


@cli.command()
@click.pass_context
def whoami(ctx):
    """Show current authentication status."""
    token = get_token()
    if token:
        click.echo(click.style("✅ Authenticated", fg="green"))
        click.echo(f"Token: {token[:20]}...")
    else:
        click.echo(click.style("❌ Not authenticated", fg="red"))
        click.echo("Run 'mirmer login' to sign in")


@cli.command()
@click.argument("message")
@click.option("--conversation-id", "-c", help="Conversation ID to continue")
@click.option("--stream/--no-stream", default=True, help="Stream responses in real-time")
@click.pass_context
def query(ctx, message, conversation_id, stream):
    """Send a query to Mirmer AI council."""
    api_key = ctx.obj.get("api_key")
    api_url = ctx.obj["api_url"]

    if not api_key:
        click.echo(click.style("❌ Error: No API key provided", fg="red"))
        click.echo("\nPlease provide an API key using one of these methods:")
        click.echo("  1. Command line: mirmer --api-key YOUR_KEY query \"message\"")
        click.echo("  2. Environment variable: export MIRMER_API_KEY=YOUR_KEY")
        click.echo("\nGet your API key from: https://mirmer-ai.vercel.app")
        sys.exit(1)

    try:
        # Create client
        client = Client(api_key=api_key, base_url=api_url)

        if stream:
            # Stream responses
            click.echo(click.style("\n🚀 Starting council process...\n", fg="cyan", bold=True))

            for update in client.stream(message, conversation_id):
                if update.type == "stage1_start":
                    click.echo(click.style("Stage 1: ", fg="yellow") + "Collecting responses...")
                elif update.type == "stage1_complete":
                    click.echo(
                        click.style("✓ Stage 1: ", fg="green")
                        + f"{len(update.data)} responses received"
                    )
                elif update.type == "stage2_start":
                    click.echo(click.style("Stage 2: ", fg="yellow") + "Peer ranking...")
                elif update.type == "stage2_complete":
                    click.echo(
                        click.style("✓ Stage 2: ", fg="green")
                        + f"{len(update.data['rankings'])} rankings received"
                    )
                elif update.type == "stage3_start":
                    click.echo(click.style("Stage 3: ", fg="yellow") + "Chairman synthesis...")
                elif update.type == "stage3_complete":
                    click.echo(click.style("✓ Stage 3: ", fg="green") + "Complete\n")
                    click.echo(click.style("=" * 60, fg="cyan"))
                    click.echo(click.style("FINAL ANSWER:", fg="cyan", bold=True))
                    click.echo(click.style("=" * 60, fg="cyan"))
                    click.echo(update.data["response"])
                elif update.type == "error":
                    click.echo(click.style(f"❌ Error: {update.error}", fg="red"))
                    sys.exit(1)
        else:
            # Non-streaming
            click.echo("Querying council...")
            response = client.query(message, conversation_id)
            click.echo(click.style("\n" + "=" * 60, fg="cyan"))
            click.echo(click.style("FINAL ANSWER:", fg="cyan", bold=True))
            click.echo(click.style("=" * 60, fg="cyan"))
            click.echo(response.stage3.response)

        client.close()

    except MirmerError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))
        import traceback
        if os.getenv("DEBUG"):
            traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"❌ Unexpected error: {e}", fg="red"))
        import traceback
        if os.getenv("DEBUG"):
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.pass_context
def conversations(ctx):
    """List all conversations."""
    api_key = ctx.obj.get("api_key")
    api_url = ctx.obj["api_url"]

    if not api_key:
        click.echo(click.style("❌ Error: No API key provided", fg="red"))
        click.echo("Set MIRMER_API_KEY environment variable or use --api-key option")
        sys.exit(1)

    try:
        client = Client(api_key=api_key, base_url=api_url)

        convs = client.list_conversations()

        if not convs:
            click.echo("No conversations found")
            return

        click.echo(click.style(f"\n{len(convs)} Conversations:", fg="cyan", bold=True))
        for conv in convs:
            click.echo(f"\n  ID: {conv.id}")
            click.echo(f"  Title: {conv.title}")
            click.echo(f"  Created: {conv.created_at}")
            click.echo(f"  Messages: {len(conv.messages)}")

        client.close()

    except MirmerError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.argument("query_string")
@click.pass_context
def search(ctx, query_string):
    """Search conversations."""
    api_key = ctx.obj.get("api_key")
    api_url = ctx.obj["api_url"]

    if not api_key:
        click.echo(click.style("❌ Error: No API key provided", fg="red"))
        click.echo("Set MIRMER_API_KEY environment variable or use --api-key option")
        sys.exit(1)

    try:
        client = Client(api_key=api_key, base_url=api_url)

        results = client.search_conversations(query_string)

        if not results:
            click.echo("No results found")
            return

        click.echo(click.style(f"\n{len(results)} Results:", fg="cyan", bold=True))
        for conv in results:
            click.echo(f"\n  ID: {conv.id}")
            click.echo(f"  Title: {conv.title}")

        client.close()

    except MirmerError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.pass_context
def usage(ctx):
    """Show API usage statistics."""
    base_url = ctx.obj["base_url"]
    api_url = ctx.obj["api_url"]

    try:
        token = ensure_authenticated(base_url)
        client = Client(api_key=token, base_url=api_url)

        stats = client.get_usage()

        click.echo(click.style("\n📊 Usage Statistics:", fg="cyan", bold=True))
        click.echo(f"  Tier: {stats.tier}")
        click.echo(f"  Used: {stats.queries_used_today}/{stats.daily_limit} queries")
        click.echo(f"  Reset: {stats.reset_time}")

        # Progress bar
        percentage = (stats.queries_used_today / stats.daily_limit) * 100
        bar_length = 30
        filled = int(bar_length * stats.queries_used_today / stats.daily_limit)
        bar = "█" * filled + "░" * (bar_length - filled)
        click.echo(f"  [{bar}] {percentage:.1f}%")

        client.close()

    except MirmerError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))
        sys.exit(1)


def main():
    """Main entry point for CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
