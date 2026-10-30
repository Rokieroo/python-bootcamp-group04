"""W3-2: Summarise (endpoint, latency_ms) pairs from a request log."""

import math
from collections import Counter, defaultdict


def p95(values: list[float]) -> float:
    """95th percentile by the nearest-rank method."""
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Return per-endpoint counts, per-endpoint p95 latency, and the slowest endpoint by p95."""
    counts = Counter(name for name, _ in pairs)
    latencies: dict[str, list[float]] = defaultdict(list)
    for name, ms in pairs:
        latencies[name].append(ms)
    p95s = {name: p95(ms) for name, ms in latencies.items()}
    return {
        "counts": dict(counts),
        "p95": p95s,
        "slowest": max(p95s, key=p95s.get) if p95s else None,
    }
