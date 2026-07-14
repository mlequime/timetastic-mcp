"""Tests for the holiday status bitmask used by ``list_holidays``."""

from __future__ import annotations

from tools.holidays import _STATUS_BITS, calculate_status_value


def test_single_statuses_are_distinct_powers_of_two() -> None:
    """The four primitive statuses must occupy separate bits so they combine
    cleanly with OR."""
    assert _STATUS_BITS["Pending"] == 1
    assert _STATUS_BITS["Approved"] == 2
    assert _STATUS_BITS["Cancelled"] == 4
    assert _STATUS_BITS["Declined"] == 8


def test_pending_or_approved_is_the_or_of_its_parts() -> None:
    assert (
        _STATUS_BITS["PendingOrApproved"]
        == _STATUS_BITS["Pending"] | _STATUS_BITS["Approved"]
    )


def test_any_is_the_or_of_every_primitive_status() -> None:
    assert _STATUS_BITS["Any"] == (
        _STATUS_BITS["Pending"]
        | _STATUS_BITS["Approved"]
        | _STATUS_BITS["Cancelled"]
        | _STATUS_BITS["Declined"]
    )


def test_combining_statuses_matches_documented_example() -> None:
    """``["Declined", "Cancelled"]`` should OR to 12, per the module comment."""
    combined = _STATUS_BITS["Declined"] | _STATUS_BITS["Cancelled"]
    assert combined == 12


def test_calculate_status_value_single() -> None:
    assert calculate_status_value(["Approved"]) == 2


def test_calculate_status_value_ors_multiple() -> None:
    """``["Declined", "Cancelled"]`` OR to 12, per the module comment."""
    assert calculate_status_value(["Declined", "Cancelled"]) == 12


def test_calculate_status_value_empty_is_zero() -> None:
    assert calculate_status_value([]) == 0


def test_calculate_status_value_ignores_duplicates() -> None:
    """OR is idempotent, so repeating a status doesn't change the result."""
    assert calculate_status_value(["Pending", "Pending"]) == _STATUS_BITS["Pending"]
