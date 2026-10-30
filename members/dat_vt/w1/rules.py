"""W1-3: Thesis eligibility rules."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Return True if credits >= 120 and gpa >= 2.0."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Return a list of human-readable reasons for unmet requirements."""
    reasons = []
    if credits < 120:
        needed = 120 - credits
        reasons.append(f"need {needed} more credits")
    if gpa < 2.0:
        reasons.append("need a GPA of at least 2.0")
    return reasons


if __name__ == "__main__":
    c = int(input("Please enter your credits: "))
    g = float(input("Please enter your GPA: "))
    if can_register_thesis(c, g):
        print("Can register thesis!")
    else:
        print(missing(c, g))
