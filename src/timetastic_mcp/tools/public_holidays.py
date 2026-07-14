"""Public holiday tools — list public holidays and available countries."""

from __future__ import annotations

from typing import Any

from ..server import get_client, mcp


@mcp.tool()
async def list_public_holidays(
    country_code: str | None = None,
    year: int | None = None,
    user_id: int | None = None,
    bank_holiday_set_id: int | None = None,
    use_org_leave_year: bool = False,
) -> Any:
    """List public holidays for the organisation.

    Args:
        country_code: Filter to a country code.
        year: Filter to a year.
        user_id: Filter to a user's public holidays.
        bank_holiday_set_id: Filter to a bank holiday set.
        use_org_leave_year: Use the user's leave year instead of calendar year.
    """
    return await get_client().request(
        "GET",
        "/publicholidays",
        params={
            "countryCode": country_code,
            "year": year,
            "userId": user_id,
            "bankHolidaySetId": bank_holiday_set_id,
            "useOrgLeaveYear": use_org_leave_year,
        },
    )


@mcp.tool()
async def get_public_holiday(public_holiday_id: int) -> Any:
    """Get a single public holiday by ID."""
    return await get_client().request("GET", f"/publicholidays/{public_holiday_id}")


@mcp.tool()
async def list_public_holiday_countries() -> Any:
    """List all countries available for public holidays."""
    return await get_client().request("GET", "/publicholidays/countries")
