"""Thin async HTTP client for the Timetastic API.

Wraps `httpx` to handle authentication, the base URL, JSON (de)serialisation,
rate-limit retries and error formatting so the MCP tools in `main.py` can stay
declarative.

Authentication uses an organisation API token (admin users only). Get or renew
yours at https://app.timetastic.co.uk/api and expose it via the
`TIMETASTIC_API_TOKEN` environment variable.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx

BASE_URL = "https://app.timetastic.co.uk/api"
TOKEN_ENV_VAR = "TIMETASTIC_API_TOKEN"

# Identify ourselves to Timetastic (they ask integrations to do this for metrics).
_USER_AGENT = "timetastic-mcp/0.1"
_CLIENT_ID = "timetastic-mcp"


class TimetasticError(Exception):
    """Raised when the Timetastic API returns a non-success response."""

    def __init__(self, status_code: int, message: str, detail: Any = None) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Timetastic API error {status_code}: {message}")


class TimetasticClient:
    """A small async wrapper around the Timetastic REST API.

    Usage::

        async with TimetasticClient() as client:
            users = await client.get("/users")
    """

    def __init__(
        self,
        token: str | None = None,
        *,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 1,
    ) -> None:
        token = token or os.environ.get(TOKEN_ENV_VAR)
        if not token:
            raise RuntimeError(
                f"No Timetastic API token found. Set the {TOKEN_ENV_VAR} "
                "environment variable to an admin API token from "
                "https://app.timetastic.co.uk/api"
            )
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "User-Agent": _USER_AGENT,
                "X-Client-ID": _CLIENT_ID,
            },
        )

    # -- lifecycle ---------------------------------------------------------

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "TimetasticClient":
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.aclose()

    # -- core request ------------------------------------------------------

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Send a request and return the parsed JSON body.

        `None` values in `params` and `json` are stripped so callers can pass
        optional arguments through without building conditional payloads. This
        also means partial updates only send the fields you actually set.
        """
        clean_params = _drop_none(params) if params else None
        clean_json = _drop_none(json) if json else None

        attempt = 0
        while True:
            try:
                response = await self._client.request(
                    method, path, params=clean_params, json=clean_json
                )
            except httpx.RequestError as exc:
                # Transport-level failure (timeout, connection reset, DNS): no
                # HTTP response exists, so surface it through the same error
                # contract as HTTP failures, using status 0 to mark "no response".
                raise TimetasticError(
                    0, f"could not reach Timetastic ({type(exc).__name__}: {exc})"
                ) from exc

            # Respect the documented rate limits (5 req/s; 1 req/s for absences).
            if response.status_code == 429 and attempt < self._max_retries:
                await asyncio.sleep(_retry_after_seconds(response))
                attempt += 1
                continue

            # A redirect (we don't follow them) almost always means the token is
            # missing/expired and we're being bounced to the login page.
            if 300 <= response.status_code < 400:
                raise TimetasticError(
                    response.status_code,
                    "unexpected redirect — check your API token is valid and "
                    "belongs to an admin user",
                )

            if response.status_code >= 400:
                raise TimetasticError(
                    response.status_code,
                    _error_message(response),
                    detail=_safe_json(response),
                )

            return _safe_json(response)

    # -- verb helpers ------------------------------------------------------

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request("POST", path, params=params, json=json)

    async def put(self, path: str, *, json: dict[str, Any] | None = None) -> Any:
        return await self.request("PUT", path, json=json)

    async def patch(self, path: str, *, json: dict[str, Any] | None = None) -> Any:
        return await self.request("PATCH", path, json=json)

    async def delete(self, path: str) -> Any:
        return await self.request("DELETE", path)


def _drop_none(data: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def _safe_json(response: httpx.Response) -> Any:
    """Parse the body as JSON, tolerating empty bodies (e.g. 200 with no content)."""
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _error_message(response: httpx.Response) -> str:
    body = _safe_json(response)
    if isinstance(body, dict):
        for key in ("errorMessage", "detail", "title", "message"):
            if body.get(key):
                return str(body[key])
    if isinstance(body, str) and body:
        return body
    return response.reason_phrase or "request failed"


def _retry_after_seconds(response: httpx.Response) -> float:
    retry_after = response.headers.get("Retry-After")
    if retry_after and retry_after.isdigit():
        return float(retry_after)
    return 1.0
