"""W3-1: Date parsing helper (dates.py)."""

import re
from datetime import date, timedelta

WEEKDAYS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


def parse_due(text: str, today: date) -> date:
    """Parse relative and absolute date strings into a concrete date.

    Supports ISO dates ('YYYY-MM-DD'), 'tomorrow', 'in N days',
             and upcoming weekday names ('Mon', 'Fri', etc. on next occurence).
    Raises ValueError for unrecognised formats.
    """

    text = text.strip()

    try:
        return date.fromisoformat(text)
    except ValueError:
        pass

    if text.lower() == "tomorrow":
        return today + timedelta(days=1)

    match_days = re.match(r"^in (\d+) days?", text, re.IGNORECASE)
    if match_days:
        days = int(match_days.group(1))
        return today + timedelta(days=days)

    cap_text = text.capitalize()
    if cap_text in WEEKDAYS:
        target_day = WEEKDAYS[cap_text]
        days_ahead = (target_day - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    raise ValueError(f"Cannot parse date expression: '{text}'")
