from collections import Counter, defaultdict
import math

def analyse(pairs: list[tuple[str, int | float]]) -> dict:
    """Analyzes chat log latency pairs to compute route statistics.
    
    Args:
        pairs: A list of (route, latency_ms) tuples.
        
    Returns:
        A dictionary containing:
          - "counts": A Counter object with request counts per route.
          - "p95": A dict with the 95th percentile latency per route.
          - "slowest": The string route name with the highest p95 latency.
    """
    if not pairs:
        return {"counts": Counter(), "p95": {}, "slowest": None}

    # 1. Group latencies by route and count requests
    route_latencies = defaultdict(list)
    counts = Counter()
    
    for route, latency in pairs:
        route_latencies[route].append(latency)
        counts[route] += 1

    # 2. Calculate the 95th percentile (p95) for each route
    p95_stats = {}
    for route, latencies in route_latencies.items():
        sorted_latencies = sorted(latencies)
        n = len(sorted_latencies)
        
        # Nearest-rank method for percentiles
        p95_index = math.ceil(n * 0.95) - 1
        p95_stats[route] = sorted_latencies[max(0, p95_index)]

    # 3. Find the route with the highest p95 latency
    slowest_route = max(p95_stats, key=p95_stats.get) if p95_stats else None

    return {
        "counts": counts,
        "p95": p95_stats,
        "slowest": slowest_route
    }
