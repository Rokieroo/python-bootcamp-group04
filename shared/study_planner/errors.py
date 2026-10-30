"""Error types and feasibility checks for study planner."""

from math import isclose, isfinite

from shared.contract import Task


class InfeasiblePlan(Exception):
    """Raised when the total effort of tasks exceeds the available study hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        return f"Plan needs {self.needed_h:g} h; only {self.available_h:g} h available"


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Validate that tasks can be completed within available_h."""
    if not isfinite(available_h) or available_h < 0:
        raise ValueError("available_h must be finite and nonnegative")
    needed = sum(task.effort_h for task in tasks)
    if needed > available_h and not isclose(needed, available_h, rel_tol=1e-12, abs_tol=0):
        raise InfeasiblePlan(needed, available_h)
