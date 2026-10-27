"""Tests for counts and nearest-rank route percentiles."""

from collections import Counter


def test_route_statistics():
    """Grouping must preserve all observations and select highest p95."""
    from members.minh_vg.w3.log_stats import analyse

    result = analyse(iter([("fee", 100), ("fee", 300), ("rag", 900),
                           ("rag", 1100), ("fee", 200)]))
    assert isinstance(result["counts"], Counter)
    assert result == {"counts": {"fee": 3, "rag": 2},
                      "p95": {"fee": 300, "rag": 1100}, "slowest": "rag"}


def test_nearest_rank_percentile():
    """At exactly 20 observations, p95 is the 19th sorted value."""
    from members.minh_vg.w3.log_stats import analyse

    assert analyse(("route", value) for value in range(20, 0, -1))["p95"] == {"route": 19}


def test_singletons_and_ties():
    """One observation remains unchanged and ties choose first-seen route."""
    from members.minh_vg.w3.log_stats import analyse

    assert analyse([("z", 7), ("a", 7)]) == {
        "counts": {"z": 1, "a": 1}, "p95": {"z": 7, "a": 7}, "slowest": "z",
    }


def test_empty_statistics():
    """No observations must not cause max() or indexing errors."""
    from members.minh_vg.w3.log_stats import analyse

    assert analyse([]) == {"counts": {}, "p95": {}, "slowest": None}
