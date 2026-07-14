"""Holiday tools — leave bookings (any absence, despite the legacy name)."""

from __future__ import annotations

from typing import Any, Literal

from server import get_client, mcp

HolidayStatus = Literal[
    "PendingOrApproved", "Pending", "Approved", "Cancelled", "Declined", "Any"
]
HolidayUpdateAction = Literal["Approve", "Decline", "Delete", "DeleteGroup"]
BookFor = Literal["User", "Department", "Everyone"]


@mcp.tool()
async def list_holidays(
    start: str | None = None,
    end: str | None = None,
    status: HolidayStatus | None = None,
    user_ids: str | None = None,
    exclusion_user_ids: str | None = None,
    department_id: int | None = None,
    leave_type_id: int | None = None,
    approver_id: int | None = None,
    my_team_only: int | None = None,
    my_favourites_only: int | None = None,
    department_managers_only: bool | None = None,
    non_archived_users_only: bool | None = None,
    transaction_year: int | None = None,
    page_number: int | None = None,
) -> Any:
    """Query leave bookings ("holidays") for the organisation.

    All filters are optional. Results are paginated at 100 per page — use
    ``page_number`` and read ``totalRecords``/``nextPageLink`` in the response.

    Args:
        start: Include holidays on or after this date-time (ISO 8601).
        end: Include holidays before and including this date-time (ISO 8601).
        status: Filter by status. Defaults to pending + approved if omitted.
        user_ids: Comma-separated user IDs to include (e.g. ``"12,34"``).
        exclusion_user_ids: Comma-separated user IDs to exclude.
        department_id: Only holidays for this department.
        leave_type_id: Only holidays of this leave type.
        approver_id: Only holidays approved by this user.
        my_team_only: Restrict to the team of this user ID.
        my_favourites_only: Restrict to the favourite users of this user ID.
        department_managers_only: Only holidays for department managers.
        non_archived_users_only: Exclude archived users.
        transaction_year: Filter to this transaction year.
        page_number: Page to fetch (defaults to 1).
    """
    return await get_client().request(
        "GET",
        "/holidays",
        params={
            "Start": start,
            "End": end,
            "Status": status,
            "UserIds": user_ids,
            "ExclusionUserIds": exclusion_user_ids,
            "DepartmentId": department_id,
            "LeaveTypeId": leave_type_id,
            "ApproverId": approver_id,
            "MyTeamOnly": my_team_only,
            "MyFavouritesOnly": my_favourites_only,
            "DepartmentManagersOnly": department_managers_only,
            "NonArchivedUsersOnly": non_archived_users_only,
            "TransactionYear": transaction_year,
            "PageNumber": page_number,
        },
    )


@mcp.tool()
async def get_holiday(holiday_id: int, filter: str = "") -> Any:
    """Get a single holiday (leave booking) by its ID."""
    return await get_client().request(
        "GET",
        f"/holidays/{holiday_id}",
        params={"filter": filter} if filter else None,
    )


@mcp.tool()
async def book_holiday(
    from_date: str,
    to_date: str,
    leave_type_id: int,
    book_for: BookFor = "User",
    user_or_department_id: int | None = None,
    from_time: str | None = None,
    to_time: str | None = None,
    reason: str | None = None,
    suppress_emails: bool | None = None,
    book_as_requestee: bool | None = None,
    override: bool | None = None,
    override_locked_days: bool | None = None,
    override_accrued_allowance: bool | None = None,
    attachment_id: int | None = None,
) -> Any:
    """Submit a leave request (book time off).

    Args:
        from_date: Start date ``YYYY-MM-DD`` (no time component).
        to_date: End date ``YYYY-MM-DD`` (no time component).
        leave_type_id: The leave type to book (see ``list_leave_types``).
        book_for: ``User``, ``Department`` or ``Everyone``.
        user_or_department_id: ID of the user/department to book for (with
            ``book_for``). Omit to book for yourself.
        from_time: Part of the start day: ``"AM"``, ``"PM"``, or minutes since
            midnight for an hourly booking.
        to_time: Part of the end day: ``"AM"``, ``"PM"``, or minutes since
            midnight for an hourly booking.
        reason: Optional reason for the request.
        suppress_emails: Admins only — suppress notification emails.
        book_as_requestee: Admins only — book as if the requestee made it so the
            normal approval flow runs (default is auto-approved by the admin).
        override: Admins only — bypass the department max-off limit.
        override_locked_days: Admins only — book over locked dates.
        override_accrued_allowance: Admins only — bypass accrued-allowance check.
        attachment_id: Attach a previously uploaded attachment by ID.
    """
    return await get_client().request(
        "POST",
        "/holidays",
        json={
            "from": from_date,
            "to": to_date,
            "leaveTypeId": leave_type_id,
            "bookFor": book_for,
            "userOrDepartmentId": user_or_department_id,
            "fromTime": from_time,
            "toTime": to_time,
            "reason": reason,
            "suppressEmails": suppress_emails,
            "bookAsRequestee": book_as_requestee,
            "override": override,
            "overrideLockedDays": override_locked_days,
            "overrideAccruedAllowance": override_accrued_allowance,
            "attachmentId": attachment_id,
        },
    )


@mcp.tool()
async def action_holiday(
    holiday_id: str,
    action: HolidayUpdateAction,
    reason: str | None = None,
    suppress_emails: bool | None = None,
) -> Any:
    """Approve, decline or cancel a holiday.

    Args:
        holiday_id: The holiday ID (or a holiday token).
        action: ``Approve``, ``Decline``, ``Delete`` (cancel this booking) or
            ``DeleteGroup`` (cancel the whole group booking).
        reason: Optional reason, typically used when declining/cancelling.
        suppress_emails: Suppress notification emails when actioning.

    Raises a webhook event if webhooks are configured.
    """
    return await get_client().request(
        "POST",
        f"/holidays/{holiday_id}",
        params={"holidayUpdateAction": action},
        json={"reason": reason, "suppressEmails": suppress_emails},
    )
