"""W3-2: summarize route counts and latency from chat logs."""

from collections import Counter, defaultdict
from math import ceil
from typing import TypedDict


class LogStats(TypedDict):
    """Counts and nearest-rank p95 values for each route."""

    counts: dict[str, int]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: list[tuple[str, float]]) -> LogStats:
    """Count routes and return their nearest-rank p95 and highest-p95 route."""
    counts: Counter[str] = Counter()
    latencies: defaultdict[str, list[float]] = defaultdict(list)
    for route, latency_ms in pairs:
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95 = {
        route: sorted(values)[ceil(0.95 * len(values)) - 1]
        for route, values in latencies.items()
    }
    slowest = max(p95, key=p95.__getitem__, default=None)
    return {"counts": dict(counts), "p95": p95, "slowest": slowest}
