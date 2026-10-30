"""Summarize request counts and nearest-rank p95 latency per route."""

from collections import Counter, defaultdict
from collections.abc import Iterable


def analyse(pairs: Iterable[tuple[str, float]]) -> dict:
    """Return counts, p95 latencies and the route with highest p95.

    Ties select the first observed route. Empty input returns empty mappings
    and slowest=None. Latencies are expected to be finite, nonnegative values.
    """
    counts: Counter[str] = Counter()
    latencies: dict[str, list[float]] = defaultdict(list)
    for route, latency in pairs:
        counts[route] += 1
        latencies[route].append(latency)
    p95 = {
        route: sorted(values)[(95 * len(values) + 99) // 100 - 1]
        for route, values in latencies.items()
    }
    slowest = max(p95, key=p95.get) if p95 else None
    return {"counts": counts, "p95": p95, "slowest": slowest}
