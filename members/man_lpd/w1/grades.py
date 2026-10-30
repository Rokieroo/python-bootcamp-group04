def summary(scores: list[float]) -> dict[str, float]:
    """Return the minimum, maximum, mean, and median of nonempty scores."""
    n = len(scores)
    if n == 0:
        raise ValueError("Empty list!")
    ordered = sorted(scores)
    return {
        "min": ordered[0],
        "max": ordered[n-1],
        "mean": round(sum(ordered)/n, 2),
        "median": round((ordered[(n-1)//2] + ordered[n//2])/2, 2)
    }
