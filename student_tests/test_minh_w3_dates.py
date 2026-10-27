"""Boundary cases for Minh's due-date parser."""

from datetime import date

import pytest


@pytest.mark.parametrize(
    ("text", "today", "expected"),
    [
        ("2026-10-30", date(2026, 10, 6), date(2026, 10, 30)),
        ("tomorrow", date(2026, 10, 6), date(2026, 10, 7)),
        ("in 3 days", date(2026, 10, 6), date(2026, 10, 9)),
        ("Fri", date(2026, 10, 6), date(2026, 10, 9)),
        ("Tue", date(2026, 10, 6), date(2026, 10, 13)),
        ("  FRIDAY  ", date(2026, 10, 9), date(2026, 10, 16)),
        ("tomorrow", date(2026, 12, 31), date(2027, 1, 1)),
        ("in 1 day", date(2028, 2, 28), date(2028, 2, 29)),
        ("in 0 days", date(2026, 10, 6), date(2026, 10, 6)),
    ],
)
def test_due_dates(text, today, expected):
    """Catch off-by-one weekdays and month/year arithmetic errors."""
    from members.minh_vg.w3.dates import parse_due

    assert parse_due(text, today) == expected


@pytest.mark.parametrize(
    "text",
    [
        "someday",
        "",
        "2026-02-30",
        "20261030",
        "2026-W44-5",
        "in -1 days",
        "in 2.5 days",
        "in 999999999999999999999 days",
    ],
)
def test_invalid_due_dates(text):
    """Unknown formats and out-of-range dates must use ValueError."""
    from members.minh_vg.w3.dates import parse_due

    with pytest.raises(ValueError):
        parse_due(text, date(2026, 10, 6))
