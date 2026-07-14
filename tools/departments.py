"""Department tools — list, inspect, create, edit and delete departments."""

from __future__ import annotations

from typing import Any

from server import get_client, mcp


@mcp.tool()
async def list_departments() -> Any:
    """List all departments in the organisation."""
    return await get_client().request("GET", "/departments")


@mcp.tool()
async def get_department(department_id: int) -> Any:
    """Get a single department by ID."""
    return await get_client().request("GET", f"/departments/{department_id}")


@mcp.tool()
async def add_department(name: str, manager_id: int, max_off: int | None = None) -> Any:
    """Create a new department.

    Args:
        name: The department name.
        manager_id: User ID of the department manager.
        max_off: Max number of users off at once (0 = no limit).
    """
    return await get_client().request(
        "POST",
        "/departments/add",
        json={"name": name, "managerId": manager_id, "maxOff": max_off},
    )


@mcp.tool()
async def edit_department(
    department_id: int,
    name: str | None = None,
    manager_id: int | None = None,
    max_off: int | None = None,
) -> Any:
    """Edit a department. Only the fields you supply are changed.

    Args:
        department_id: The department to edit.
        name: New department name.
        manager_id: User ID of the department manager.
        max_off: Max users off at once (0 disables the limit; range 0–20).
    """
    return await get_client().request(
        "POST",
        f"/departments/edit/{department_id}",
        json={"name": name, "managerId": manager_id, "maxOff": max_off},
    )


@mcp.tool()
async def delete_department(department_id: int) -> Any:
    """Delete a department. It must be empty (reassign any users first)."""
    return await get_client().request("POST", f"/departments/delete/{department_id}")
