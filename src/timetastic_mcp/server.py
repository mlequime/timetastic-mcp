"""Shared MCP server instance and API client access.

Every tool module imports `mcp` (to register its tools via `@mcp.tool()`) and
`get_client` (to call the Timetastic API) from here. `main.py` imports the tool
modules to register them, then runs `mcp`.

The API client is created lazily on first use (so importing the tools never
requires a token) and closed cleanly on server shutdown via the FastMCP
lifespan below. Tools call `get_client().request(...)`; any `TimetasticError`
(API or transport failure) or `RuntimeError` (missing token) propagates to
FastMCP, which returns it to the client as a tool error.
"""

from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator

from mcp.server.fastmcp import FastMCP

from .timetastic import TimetasticClient

_CLIENT: TimetasticClient | None = None


def get_client() -> TimetasticClient:
    """Return a lazily-created, shared API client.

    Construction (which validates the token) is deferred to first use so that
    importing the tool modules never fails when the token is unset.
    """
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = TimetasticClient()
    return _CLIENT


@contextlib.asynccontextmanager
async def _lifespan(_server: FastMCP) -> AsyncIterator[None]:
    """Close the shared client's connection pool when the server stops.

    The lifespan runs on the server's event loop: the same loop the client is
    created on during the first tool call.
    """
    global _CLIENT
    try:
        yield
    finally:
        if _CLIENT is not None:
            await _CLIENT.aclose()
            _CLIENT = None


mcp = FastMCP("timetastic", lifespan=_lifespan)
