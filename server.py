"""Shared MCP server instance and API client access.

Every tool module imports `mcp` (to register its tools via `@mcp.tool()`) and
`get_client` (to call the Timetastic API) from here. `main.py` imports the tool
modules to register them, then runs `mcp`.

Tools call `get_client().request(...)` directly; any `TimetasticError` (API
failure) or `RuntimeError` (missing token) propagates to FastMCP, which returns
it to the client as a tool error.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from timetastic import TimetasticClient

mcp = FastMCP("timetastic")

_client: TimetasticClient | None = None


def get_client() -> TimetasticClient:
    """Return a lazily-created, shared API client.

    Construction (which validates the token) is deferred to first use so that
    importing the tool modules never fails when the token is unset.
    """
    global _client
    if _client is None:
        _client = TimetasticClient()
    return _client
