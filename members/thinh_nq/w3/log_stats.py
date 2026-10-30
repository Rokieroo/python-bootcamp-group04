"""W3-2: Summarize request counts and latency percentiles."""

import math
from collections import Counter, defaultdict


def p95(values: list[float]) -> float:
    """Calculate the 95th percentile using the nearest-rank method."""
    if not values:
        raise ValueError("Cannot calculate p95 of an empty list")
    ordered = sorted(values)
    rank = math.ceil(0.95 * len(ordered))
    return ordered[rank - 1]


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Analyze (endpoint, latency_ms) pairs.

    Returns:
        A dictionary containing:
        - "counts": number of requests per endpoint (dict)
        - "p95": 95th percentile latency per endpoint
        - "slowest": the endpoint with the highest p95 latency
    """
    counts = Counter(route for route, _ in pairs)
    latencies: dict[str, list[float]] = defaultdict(list)
    for route, ms in pairs:
        latencies[route].append(ms)

    p95_stats = {route: p95(vals) for route, vals in latencies.items()}
    slowest_route = max(p95_stats, key=p95_stats.get) if p95_stats else None

    return {
        "counts": dict(counts),
        "p95": p95_stats,
        "slowest": slowest_route,
    }
