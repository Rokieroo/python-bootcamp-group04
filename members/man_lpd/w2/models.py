# W2-1 : Task model

from dataclasses import dataclass
from datetime import date


@dataclass 
class Task:
    """A study task with importance, effort, and a due date."""
    title: str
    importance: int
    effort_h: float
    deadline: date
    
    def __post_init__(self) -> None:
        """Reject importance values outside the one-to-five scale."""
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")

    def days_left(self, today: date) -> int:
        """Return days until the deadline, clamped at zero."""
        diff = (self.deadline - today).days
        return max(diff, 0)
    


