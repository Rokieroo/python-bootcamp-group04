"""W3-1: Parse human-friendly due dates."""

import re
from datetime import date, timedelta

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def parse_due(text: str, today: date) -> date:
    """Turn 'YYYY-MM-DD', 'today', 'tomorrow', 'in N days' or a weekday into a date.

    A weekday ('Fri' or 'Friday') means its next occurrence after today, never today.
    Anything else raises ValueError.
    """
    s = text.strip().lower()
    if s == "today":
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if m := re.fullmatch(r"in (\d+) days?", s):
        return today + timedelta(days=int(m[1]))
    for i, name in enumerate(WEEKDAYS):
        if s in (name, name[:3]):
            return today + timedelta(days=(i - today.weekday() - 1) % 7 + 1)
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise ValueError(f"cannot parse due date: {text!r}") from None
