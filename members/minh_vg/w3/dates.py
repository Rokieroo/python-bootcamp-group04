"""Parse explicit and relative English due dates without external packages."""

import re
from datetime import date, timedelta

WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def parse_due(text: str, today: date) -> date:
    """Accept YYYY-MM-DD, tomorrow, in N days, or the next English weekday.

    Weekdays accept full names or three-letter abbreviations, ignoring case.
    Surrounding whitespace is ignored. Unsupported or out-of-range dates
    raise ValueError; a weekday matching today advances seven days.
    """
    value = text.strip().lower()
    try:
        if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            return date.fromisoformat(value)
        if value == "tomorrow":
            return today + timedelta(days=1)
        relative = re.fullmatch(r"in ([0-9]+) days?", value)
        if relative:
            return today + timedelta(days=int(relative.group(1)))
        for index, name in enumerate(WEEKDAYS):
            if value in (name, name[:3]):
                return today + timedelta(days=(index - today.weekday()) % 7 or 7)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"Invalid due date: {text!r}") from exc
    raise ValueError(f"Unknown due date: {text!r}")
