"""Timetastic MCP server — entry point.

Exposes the Timetastic API (https://app.timetastic.co.uk/api) as MCP tools,
grouped by resource under the ``tools`` package: absences, holidays (leave
bookings), users, departments, leave types, allowances, locked dates, public
holidays and webhooks.

Importing ``tools`` registers every tool on the shared ``mcp`` server defined
in ``server.py``. Set the ``TIMETASTIC_API_TOKEN`` environment variable to an
admin API token before running, then run with ``uv run main.py``.
"""

from __future__ import annotations

import tools  # noqa: F401 — imported for its tool-registration side effects
from server import mcp


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
