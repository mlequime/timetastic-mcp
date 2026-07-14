"""Leave type tools — list, inspect, create, update and delete leave types."""

from __future__ import annotations

from typing import Any, Literal

from server import get_client, mcp

CalendarVisibility = Literal["Busy", "Available", "OutOfOffice"]


@mcp.tool()
async def list_leave_types(include_inactive: bool = False) -> Any:
    """List leave types for the organisation.

    Args:
        include_inactive: Also return inactive (deleted) leave types.
    """
    return await get_client().request(
        "GET", "/leavetypes", params={"includeInactive": include_inactive}
    )


@mcp.tool()
async def get_leave_type(leave_type_id: int) -> Any:
    """Get a single leave type by ID."""
    return await get_client().request("GET", f"/leavetypes/{leave_type_id}")


@mcp.tool()
async def list_leave_type_colors() -> Any:
    """List the valid colour hex codes for leave types."""
    return await get_client().request("GET", "/leavetypes/colors")


@mcp.tool()
async def list_leave_type_icons() -> Any:
    """List the valid icon names for leave types (empty string = no icon)."""
    return await get_client().request("GET", "/leavetypes/icons")


@mcp.tool()
async def create_leave_type(
    name: str,
    deducted: bool | None = None,
    requires_approval: bool | None = None,
    include_max_off: bool | None = None,
    is_private: bool | None = None,
    color: str | None = None,
    icon: str | None = None,
    calendar_visibility: CalendarVisibility | None = None,
    limit_hours: float | None = None,
    limit_days: float | None = None,
) -> Any:
    """Create a new leave type (admins only).

    Args:
        name: Name of the leave type (1–50 chars).
        deducted: Whether it deducts from the user's allowance.
        requires_approval: Whether bookings need approval.
        include_max_off: Whether it counts toward max-absent limits.
        is_private: Whether the leave type is private.
        color: A hex colour (see ``list_leave_type_colors``).
        icon: An icon name (see ``list_leave_type_icons``).
        calendar_visibility: ``Busy``, ``Available`` or ``OutOfOffice``.
        limit_hours: Optional limit in hours.
        limit_days: Optional limit in days.

    Returns the ID of the new leave type.
    """
    return await get_client().request(
        "POST",
        "/leavetypes",
        json={
            "name": name,
            "deducted": deducted,
            "requiresApproval": requires_approval,
            "includeMaxOff": include_max_off,
            "isPrivate": is_private,
            "color": color,
            "icon": icon,
            "calendarVisibility": calendar_visibility,
            "limitHours": limit_hours,
            "limitDays": limit_days,
        },
    )


@mcp.tool()
async def update_leave_type(
    leave_type_id: int,
    name: str,
    deducted: bool | None = None,
    requires_approval: bool | None = None,
    include_max_off: bool | None = None,
    is_private: bool | None = None,
    color: str | None = None,
    icon: str | None = None,
    calendar_visibility: CalendarVisibility | None = None,
    limit_hours: float | None = None,
    limit_days: float | None = None,
) -> Any:
    """Update an existing leave type (admins only). ``name`` is required."""
    return await get_client().request(
        "PUT",
        f"/leavetypes/{leave_type_id}",
        json={
            "name": name,
            "deducted": deducted,
            "requiresApproval": requires_approval,
            "includeMaxOff": include_max_off,
            "isPrivate": is_private,
            "color": color,
            "icon": icon,
            "calendarVisibility": calendar_visibility,
            "limitHours": limit_hours,
            "limitDays": limit_days,
        },
    )


@mcp.tool()
async def delete_leave_type(leave_type_id: int) -> Any:
    """Delete (deactivate) a leave type. Cannot delete the last active one."""
    return await get_client().request("DELETE", f"/leavetypes/{leave_type_id}")
