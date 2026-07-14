"""Locked date tools — periods where booking time off is blocked."""

from __future__ import annotations

from typing import Any, Literal

from ..server import get_client, mcp

LockedDateRecordType = Literal["Organisation", "Department", "User"]


@mcp.tool()
async def list_locked_dates() -> Any:
    """List all locked dates (periods where booking time off is blocked)."""
    return await get_client().request("GET", "/lockeddates")


@mcp.tool()
async def add_locked_date(
    from_date: str,
    to_date: str,
    reason: str,
    record_type: LockedDateRecordType,
    record_id: int,
) -> Any:
    """Add a locked date period.

    Args:
        from_date: Start of the locked period (ISO 8601 date-time).
        to_date: End of the locked period (ISO 8601 date-time).
        reason: Reason for the lock (1–2000 chars).
        record_type: Scope of the lock: ``Organisation``, ``Department`` or
            ``User``. Higher-level locks supersede lower-level ones.
        record_id: The organisation, department or user ID the lock targets.
    """
    return await get_client().request(
        "POST",
        "/lockeddates",
        json={
            "from": from_date,
            "to": to_date,
            "reason": reason,
            "recordType": record_type,
            "recordId": record_id,
        },
    )


@mcp.tool()
async def delete_locked_date(locked_date_id: int) -> Any:
    """Delete a locked date by ID (admins/authorised managers only)."""
    return await get_client().request("DELETE", f"/lockeddates/{locked_date_id}")
