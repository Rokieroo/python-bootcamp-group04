"""W3-1: parse absolute and relative due dates."""

import re
from datetime import date, timedelta

WEEKDAYS = {name: index for index, name in enumerate(("mon", "tue", "wed", "thu", "fri", "sat", "sun"))}


def parse_due(text: str, today: date) -> date:
    """Parse ISO dates, tomorrow, positive relative days, or the next weekday."""
    value = text.strip().lower()
    if value == "tomorrow":
        return today + timedelta(days=1)
    if value in WEEKDAYS:
        days_ahead = (WEEKDAYS[value] - today.weekday()) % 7 or 7
        return today + timedelta(days=days_ahead)
    if match := re.fullmatch(r"in (\d+) days?", value):
        return today + timedelta(days=int(match.group(1)))
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Unknown due date: {text}") from exc
