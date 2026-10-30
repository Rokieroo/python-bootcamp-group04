"""W1-5: Group timetable by day."""


def by_day(items: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day and sort them alphabetically within each day."""
    result = {}
    for course, day in items:
        result.setdefault(day, []).append(course)

    for day, courses in result.items():
        courses.sort()

    return result


if __name__ == "__main__":
    course_days = [
        ("Math", "Monday"),
        ("History", "Wednesday"),
        ("Physics", "Monday"),
        ("Art", "Wednesday"),
    ]
    print(by_day(course_days))
