"""Webhook tools — inspect recent webhook events."""

from __future__ import annotations

from typing import Any

from server import get_client, mcp


@mcp.tool()
async def list_webhook_events(days_history: int = 1) -> Any:
    """List recent webhook events (up to 30 days of history are retained).

    Args:
        days_history: How many days of history to return (defaults to 1).
    """
    return await get_client().request("GET", f"/webhooks/list/{days_history}")
