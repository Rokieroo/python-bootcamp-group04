from collections import Counter, defaultdict
import math


def calculate_p95(latencies: list[float]) -> float:
    sorted_lat = sorted(latencies)
    n = len(sorted_lat)

    idx = max(0, math.ceil(0.95 * n) - 1)
    return sorted_lat[idx]

def analyse(pairs: list[tuple[str, float]]) -> dict:
    if not pairs:
        return {"counts": Counter(), "p95": {}, "slowest": None}

    counts = Counter()
    route_latencies = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        route_latencies[route].append(latency)

    p95 = {}
    for route, lats in route_latencies.items():
        p95[route] = calculate_p95(lats)

    slowest_route = max(p95, key = p95.get)

    return {"counts": counts, "p95": p95, "slowest": slowest_route}