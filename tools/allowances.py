"""Allowance tools — annual allowance, TOIL and carry forward."""

from __future__ import annotations

from typing import Any

from server import get_client, mcp


@mcp.tool()
async def list_all_allowances(year: int | None = None) -> Any:
    """List allowances, TOIL and carry-forward for all users.

    Args:
        year: Restrict to a single year. Omit for all years.
    """
    path = "/users/allowances" if year is None else f"/users/allowances/{year}"
    return await get_client().request("GET", path)


@mcp.tool()
async def get_user_allowance(user_id: int, year: int | None = None) -> Any:
    """Get allowances, TOIL and carry-forward for one user.

    Args:
        user_id: The user to query.
        year: Restrict to a single year. Omit for all years.
    """
    path = (
        f"/users/{user_id}/allowances"
        if year is None
        else f"/users/{user_id}/allowances/{year}"
    )
    return await get_client().request("GET", path)


@mcp.tool()
async def update_user_allowance(user_id: int, year: int, amount: float) -> Any:
    """Set a user's annual allowance for a year.

    Args:
        user_id: The user to update.
        year: The year to update.
        amount: The new allowance (0–8784).
    """
    return await get_client().request(
        "PUT", f"/users/{user_id}/allowances/{year}/allowance", json={"amount": amount}
    )


@mcp.tool()
async def update_user_carry_forward(user_id: int, year: int, amount: float) -> Any:
    """Set a user's carry-forward amount for a year (0–5000)."""
    return await get_client().request(
        "PUT",
        f"/users/{user_id}/allowances/{year}/carryforward",
        json={"amount": amount},
    )


@mcp.tool()
async def add_user_toil(
    user_id: int, year: int, amount: float, description: str | None = None
) -> Any:
    """Add a TOIL (time off in lieu) entry for a user in a year.

    Args:
        user_id: The user to add TOIL for.
        year: The year the TOIL applies to.
        amount: TOIL amount (-5000 to 5000).
        description: Optional description (max 1000 chars).

    Returns the ID of the new TOIL entry.
    """
    return await get_client().request(
        "POST",
        f"/users/{user_id}/allowances/{year}/toil",
        json={"amount": amount, "description": description},
    )


@mcp.tool()
async def update_user_toil(
    user_id: int,
    year: int,
    toil_id: int,
    amount: float,
    description: str | None = None,
) -> Any:
    """Update an existing TOIL entry (-5000 to 5000)."""
    return await get_client().request(
        "PUT",
        f"/users/{user_id}/allowances/{year}/toil/{toil_id}",
        json={"amount": amount, "description": description},
    )


@mcp.tool()
async def delete_user_toil(user_id: int, year: int, toil_id: int) -> Any:
    """Delete a user's TOIL entry."""
    return await get_client().request(
        "DELETE", f"/users/{user_id}/allowances/{year}/toil/{toil_id}"
    )
