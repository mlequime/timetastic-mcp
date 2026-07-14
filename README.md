# Timetastic MCP

An unofficial [MCP](https://modelcontextprotocol.io) server for
[Timetastic](https://timetastic.co.uk), exposing the Timetastic API to
agentic clients so they can query and manage absence & leave data.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

You need an **admin** API token, generated at
<https://app.timetastic.co.uk/api>. The server reads it from the
`TIMETASTIC_API_TOKEN` environment variable.

```bash
export TIMETASTIC_API_TOKEN="your-token-here"
uv run main.py
```

## Client configuration

Add the server to your MCP client (e.g. Claude Desktop / Claude Code):

```json
{
  "mcpServers": {
    "timetastic": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/timetastic-mcp", "run", "main.py"],
      "env": { "TIMETASTIC_API_TOKEN": "your-token-here" }
    }
  }
}
```

## Tools

Tools are grouped by resource and named `<verb>_<resource>`.

| Group | Tools |
| --- | --- |
| **Absences** | `list_absences` |
| **Holidays** (leave bookings) | `list_holidays`, `get_holiday`, `book_holiday`, `action_holiday` |
| **Users** | `list_users`, `get_user`, `get_user_contact`, `add_user`, `edit_user`, `archive_user`, `restore_user`, `assign_public_holidays_to_user` |
| **Departments** | `list_departments`, `get_department`, `add_department`, `edit_department`, `delete_department` |
| **Leave types** | `list_leave_types`, `get_leave_type`, `list_leave_type_colors`, `list_leave_type_icons`, `create_leave_type`, `update_leave_type`, `delete_leave_type` |
| **Allowances** | `list_all_allowances`, `get_user_allowance`, `update_user_allowance`, `update_user_carry_forward`, `add_user_toil`, `update_user_toil`, `delete_user_toil` |
| **Locked dates** | `list_locked_dates`, `add_locked_date`, `delete_locked_date` |
| **Public holidays** | `list_public_holidays`, `get_public_holiday`, `list_public_holiday_countries` |
| **Webhooks** | `list_webhook_events` |

> **Note:** Timetastic calls all leave bookings "holidays" for historical
> reasons — the *Holidays* tools cover any kind of absence, not just annual
> leave.

## Layout

- [`timetastic.py`](timetastic.py) — async HTTP client (auth, base URL,
  rate-limit retries, error handling).
- [`server.py`](server.py) — the shared `FastMCP` instance and `get_client()`,
  the lazily-created API client the tools call.
- [`tools/`](tools/) — one module per resource area, each registering its tools
  on the shared server: `absences`, `holidays`, `users`, `departments`,
  `leave_types`, `allowances`, `locked_dates`, `public_holidays`, `webhooks`.
- [`main.py`](main.py) — entry point; imports `tools` to register everything,
  then runs the server.

## Notes

- The API is rate limited to 5 requests/second per token (1/second for
  `list_absences`); the client retries once on a `429`.
- Write and admin operations require appropriate permissions on the token's
  user account.
