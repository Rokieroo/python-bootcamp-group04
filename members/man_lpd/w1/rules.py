def  can_register_thesis(credits: int, gpa: float) -> bool:
    """Check the minimum credit and GPA requirements for thesis registration."""
    if credits < 120:
        return False
    return not gpa < 2.0

def  missing(credits: int, gpa: float) -> list[str]:
    """Describe which thesis-registration requirements remain unmet."""
    miss = []
    if credits < 120:
        crenum = 120 - credits
        syntax = "more credits" if (crenum > 1) else "more credit"
        miss.append(f"need {crenum} {syntax}")
    if gpa < 2.0:
        gpanum = round(2.0 - gpa, 2)
        miss.append(f"need {gpanum} more GPA points")
    return miss


