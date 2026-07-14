"""Timetastic tool groups.

Importing this package imports every tool module, which registers each group's
tools on the shared ``mcp`` server via the ``@mcp.tool()`` decorator.
"""

from __future__ import annotations

from . import (
    absences,
    allowances,
    departments,
    holidays,
    leave_types,
    locked_dates,
    public_holidays,
    users,
    webhooks,
)

__all__ = [
    "absences",
    "allowances",
    "departments",
    "holidays",
    "leave_types",
    "locked_dates",
    "public_holidays",
    "users",
    "webhooks",
]
