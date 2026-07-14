"""Absence tools — "who is off"."""

from __future__ import annotations

from typing import Any, Literal

from server import get_client, mcp

AbsenceQueryType = Literal["AllEvents", "AllAbsences", "Bookings", "PublicHolidays"]


@mcp.tool()
async def list_absences(
    start: str,
    end: str,
    query_type: AbsenceQueryType = "AllAbsences",
) -> Any:
    """Get a chronological list of who is off between two dates.

    The single best endpoint for "who is off on/around a given day" — it merges
    bookings, non-working days, public holidays and (optionally) other events
    without needing multiple queries.

    Args:
        start: Start date, ISO format ``YYYY-MM-DD``.
        end: End date, ISO format ``YYYY-MM-DD``. Max 31 days after start.
        query_type: What to include. ``AllAbsences`` (bookings, public holidays
            and non-working days), ``Bookings``, ``PublicHolidays`` or
            ``AllEvents`` (also birthdays, work anniversaries and locked dates).

    Rate limited to 1 request per second; limited to a 31-day range.
    """
    return await get_client().request(
        "GET",
        "/absences",
        params={"Start": start, "End": end, "AbsenceQueryType": query_type},
    )
