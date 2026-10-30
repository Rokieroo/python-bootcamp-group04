"""Behavioral tests for thinh_nq week 3 deliverables."""

from datetime import date, timedelta
import pytest

from members.thinh_nq.w3.dates import parse_due
from members.thinh_nq.w3.log_stats import analyse, p95
from members.thinh_nq.w3.cli import build_parser, main


def test_parse_due_dates():
    today = date(2026, 10, 6)  # Tuesday
    assert parse_due("today", today) == today
    assert parse_due("tomorrow", today) == date(2026, 10, 7)
    assert parse_due("in 1 day", today) == date(2026, 10, 7)
    assert parse_due("in 5 days", today) == date(2026, 10, 11)
    assert parse_due("2026-12-25", today) == date(2026, 12, 25)

    # Weekday check: next occurrence, never today
    assert parse_due("Tue", today) == today + timedelta(days=7)
    assert parse_due("Tuesday", today) == today + timedelta(days=7)
    assert parse_due("Wed", today) == date(2026, 10, 7)
    assert parse_due("Fri", today) == date(2026, 10, 9)
    assert parse_due("Mon", today) == date(2026, 10, 12)

    with pytest.raises(ValueError):
        parse_due("someday", today)
    with pytest.raises(ValueError):
        parse_due("invalid-date-format", today)


def test_log_stats_percentiles():
    pairs = [
        ("api/login", 50),
        ("api/login", 100),
        ("api/search", 200),
        ("api/search", 800),
        ("api/search", 300),
    ]
    res = analyse(pairs)
    assert res["counts"]["api/login"] == 2
    assert res["counts"]["api/search"] == 3
    assert res["slowest"] == "api/search"
    assert res["p95"]["api/login"] == 100
    assert res["p95"]["api/search"] == 800


def test_p95_empty():
    with pytest.raises(ValueError):
        p95([])


def test_cli_parser():
    parser = build_parser()
    args = parser.parse_args(["tasks.csv", "--hours", "3.5", "--today", "2026-11-01"])
    assert args.csv == "tasks.csv"
    assert args.hours == 3.5
    assert args.today == date(2026, 11, 1)


def test_cli_missing_file(capsys):
    ret = main(["nonexistent_file_xyz.csv", "--hours", "2"])
    assert ret == 1
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()
