"""User tools — list, inspect, create, edit, archive and restore users."""

from __future__ import annotations

from typing import Any

from server import get_client, mcp


@mcp.tool()
async def list_users(
    department_id: int | None = None,
    include_archived_users: bool = False,
    only_show_archived_users: bool = False,
) -> Any:
    """List users in the organisation, optionally filtered by department.

    Args:
        department_id: Only users in this department.
        include_archived_users: Include archived users in the results.
        only_show_archived_users: If archived users are included, show ONLY them.
    """
    return await get_client().request(
        "GET",
        "/users",
        params={
            "departmentId": department_id,
            "includeArchivedUsers": include_archived_users,
            "onlyShowArchivedUsers": only_show_archived_users,
        },
    )


@mcp.tool()
async def get_user(user_id: int) -> Any:
    """Get a user by ID, including work schedule and allowance breakdown."""
    return await get_client().request("GET", f"/users/{user_id}")


@mcp.tool()
async def get_user_contact(user_id: int) -> Any:
    """Get a user with contact-tab details (address, phone, emergency contact).

    Requires a Timetastic Pro account.
    """
    return await get_client().request("GET", f"/users/contact/{user_id}")


@mcp.tool()
async def add_user(
    first_name: str,
    last_name: str,
    department_id: int,
    allowance: float,
    email_address: str | None = None,
    start_date: str | None = None,
    leave_year_start: int | None = None,
    send_welcome_email: bool | None = None,
) -> Any:
    """Add a new user to Timetastic.

    Args:
        first_name: The user's first name.
        last_name: The user's last name.
        department_id: The department to place the user in.
        allowance: Annual leave allowance in days (0–366).
        email_address: The user's email address.
        start_date: Start date, ISO 8601 (e.g. ``2022-02-04T00:00:00``).
        leave_year_start: Month the leave year starts (1=Jan … 12=Dec).
        send_welcome_email: Email the user to set a password and get started.
    """
    return await get_client().request(
        "POST",
        "/users/add",
        json={
            "firstName": first_name,
            "lastName": last_name,
            "departmentId": department_id,
            "allowance": allowance,
            "emailAddress": email_address,
            "startDate": start_date,
            "leaveYearStart": leave_year_start,
            "sendWelcomeEmail": send_welcome_email,
        },
    )


@mcp.tool()
async def edit_user(
    user_id: int,
    email_address: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    start_date: str | None = None,
    birthday: str | None = None,
    department_id: int | None = None,
    admin: bool | None = None,
    director: bool | None = None,
    approver_id: int | None = None,
    public_holiday_set_id: int | None = None,
    has_public_holidays: bool | None = None,
    job_title: str | None = None,
    payroll_id: str | None = None,
    address1: str | None = None,
    address2: str | None = None,
    city: str | None = None,
    post_code: str | None = None,
    telephone1: str | None = None,
    telephone2: str | None = None,
    country: str | None = None,
    emergency_contact_name: str | None = None,
    emergency_contact_phone: str | None = None,
) -> Any:
    """Edit a user. Only the fields you supply are changed (partial update).

    Args:
        user_id: The ID of the user to edit.
        email_address: New email. Pass ``""`` to clear an existing address.
        approver_id: The user's approver; set to 0 to default to dept manager.
        public_holiday_set_id: Public holiday set (needs ``has_public_holidays``).
        has_public_holidays: Enable public holidays for this user.
        (Other args map directly to the corresponding user fields.)
    """
    return await get_client().request(
        "POST",
        f"/users/edit/{user_id}",
        json={
            "emailAddress": email_address,
            "firstname": first_name,
            "lastname": last_name,
            "startDate": start_date,
            "birthday": birthday,
            "departmentId": department_id,
            "admin": admin,
            "director": director,
            "approverId": approver_id,
            "publicHolidaySetId": public_holiday_set_id,
            "hasPublicHolidays": has_public_holidays,
            "jobTitle": job_title,
            "payrollId": payroll_id,
            "address1": address1,
            "address2": address2,
            "city": city,
            "postCode": post_code,
            "telephone1": telephone1,
            "telephone2": telephone2,
            "country": country,
            "emergencyContactName": emergency_contact_name,
            "emergencyContactPhone": emergency_contact_phone,
        },
    )


@mcp.tool()
async def archive_user(user_id: int, archive_date: str | None = None) -> Any:
    """Archive a user. They are logged out immediately and cannot log in.

    Args:
        user_id: The ID of the user to archive.
        archive_date: The date the user left (UTC, must be in the past),
            ISO 8601. Shown on their archived profile and in reports.
    """
    return await get_client().request(
        "POST", f"/users/archive/{user_id}", json={"archiveDate": archive_date}
    )


@mcp.tool()
async def restore_user(user_id: int) -> Any:
    """Restore an archived user so they can use Timetastic again."""
    return await get_client().request("POST", f"/users/restore/{user_id}")


@mcp.tool()
async def assign_public_holidays_to_user(
    user_id: int,
    country_code: str | None = None,
    region_code: str | None = None,
) -> Any:
    """Assign a set of public holidays to a user (enabling them if needed).

    Args:
        user_id: The user's ID.
        country_code: ISO 3166-1 alpha-2 country code (e.g. ``"ES"`` for Spain).
        region_code: Full region code (e.g. ``"GB-SCT"`` for Scotland,
            ``"ES-AN"`` for Andalucía).

    If the chosen country/region is already used by your organisation, that
    (possibly customised) set is used; otherwise the standard set is assigned.
    """
    return await get_client().request(
        "PATCH",
        f"/users/{user_id}/publicholidays",
        json={"countryCode": country_code, "regionCode": region_code},
    )
