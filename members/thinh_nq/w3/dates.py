"""W3-1: Parse human-friendly due dates."""

import re
from datetime import date, timedelta

WEEKDAYS = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def parse_due(text: str, today: date) -> date:
    """Turn 'YYYY-MM-DD', 'today', 'tomorrow', 'in N days' or a weekday into a date.

    A weekday ('Fri' or 'Friday') means its next occurrence after today, never today.
    Raises ValueError for unrecognized formats.
    """
    cleaned = text.strip()
    lower = cleaned.lower()

    if lower == "today":
        return today

    if lower == "tomorrow":
        return today + timedelta(days=1)

    if match := re.fullmatch(r"in\s+(\d+)\s+days?", lower):
        return today + timedelta(days=int(match.group(1)))

    if lower in WEEKDAYS:
        target_weekday = WEEKDAYS[lower]
        days_ahead = (target_weekday - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    try:
        return date.fromisoformat(cleaned)
    except ValueError:
        raise ValueError(f"Cannot parse due date from {text!r}") from None
