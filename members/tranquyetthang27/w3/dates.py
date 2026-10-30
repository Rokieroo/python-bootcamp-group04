from datetime import date, timedelta
import re

def parse_due(text: str, today: date) -> date:
    # Clean up the input string
    text = text.strip().lower()
    
    # 1. Handle ISO format (YYYY-MM-DD)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        try:
            return date.fromisoformat(text)
        except ValueError:
            raise ValueError(f"Invalid date format: {text}")
            
    # 2. Handle "tomorrow"
    if text == "tomorrow":
        return today + timedelta(days=1)
        
    # 3. Handle "in X days"
    match_days = re.match(r"^in\s+(\d+)\s+days?$", text)
    if match_days:
        days = int(match_days.group(1))
        return today + timedelta(days=days)
        
    # 4. Handle weekday names like "Fri" (next occurrence)
    weekdays = {
        "mon": 0, "monday": 0,
        "tue": 1, "tuesday": 1,
        "wed": 2, "wednesday": 2,
        "thu": 3, "thursday": 3,
        "fri": 4, "friday": 4,
        "sat": 5, "saturday": 5,
        "sun": 6, "sunday": 6
    }
    
    if text in weekdays:
        target_weekday = weekdays[text]
        current_weekday = today.weekday()
        
        # Calculate days until the next occurrence (strictly in the future, 1 to 7 days ahead)
        days_ahead = target_weekday - current_weekday
        if days_ahead <= 0:
            days_ahead += 7
            
        return today + timedelta(days=days_ahead)
        
    # 5. Raise ValueError for anything else
    raise ValueError(f"Unknown date instruction: '{text}'")
