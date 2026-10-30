"""W1-1: Grade summary."""


def summary(scores: list[float]) -> dict[str, float]:
    """Compute min, max, mean, and median of a list of scores."""
    if not scores:
        raise ValueError("scores list cannot be empty")

    n = len(scores)
    sorted_scores = sorted(scores)

    min_val = sorted_scores[0]
    max_val = sorted_scores[-1]
    mean_val = round(sum(scores) / n, 2)

    mid = n // 2
    if n % 2 == 1:
        median_val = sorted_scores[mid]
    else:
        median_val = (sorted_scores[mid - 1] + sorted_scores[mid]) / 2

    return {"min": min_val, "max": max_val, "mean": mean_val, "median": median_val}


if __name__ == "__main__":
    user_input = input("Please enter a list of numbers separated by spaces: ")
    scores = [float(x) for x in user_input.split()]
    print(summary(scores))