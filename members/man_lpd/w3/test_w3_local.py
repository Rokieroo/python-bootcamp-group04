"""Additional edge cases for man_lpd's Week 3 exercises."""

from datetime import date
from pathlib import Path

import pytest

from members.man_lpd.w3.cli import main
from members.man_lpd.w3.dates import parse_due
from members.man_lpd.w3.log_stats import analyse


def test_date_weekday_wrap_and_invalid_date() -> None:
    """Weekday names always select a future occurrence and bad dates fail."""
    assert parse_due("  TUE  ", date(2026, 10, 6)) == date(2026, 10, 13)
    assert parse_due("in 1 day", date(2026, 10, 6)) == date(2026, 10, 7)
    with pytest.raises(ValueError):
        parse_due("2026-02-30", date(2026, 10, 6))


def test_stats_empty_and_nearest_rank() -> None:
    """Empty logs are explicit, and p95 uses the nearest-rank rule."""
    assert analyse([]) == {"counts": {}, "p95": {}, "slowest": None}
    result = analyse([("a", float(n)) for n in range(1, 21)])
    assert result["p95"]["a"] == 19.0
    assert result["slowest"] == "a"


def test_cli_missing_file_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A missing CSV produces a useful error on stderr."""
    assert main([str(tmp_path / "missing.csv"), "--hours", "2"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "not found" in captured.err


def test_cli_prioritizes_and_partially_allocates(capsys: pytest.CaptureFixture[str]) -> None:
    """The sample plan ranks the assignment first and respects the budget."""
    sample = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"
    assert main([str(sample), "--hours", "2", "--today", "2026-10-26"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == ["Tonight (2.0 h):", " 1. Assignment ...... 1.5 h", " 2. DS exam ...... 0.5 h"]
