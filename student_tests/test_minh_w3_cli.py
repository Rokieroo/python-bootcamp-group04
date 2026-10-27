"""Exercise the real CLI, file loader and allocation together."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    """Invoke the package entry point from the repository root."""
    return subprocess.run(
        [sys.executable, "-m", "members.minh_vg.w3.cli", *map(str, args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_sample_plan():
    """The urgent Assignment gets 1.5h; the remaining 0.5h goes to DS exam."""
    result = run_cli("samples/tasks.csv", "--hours", "2", "--today", "2026-10-26")
    assert result.returncode == 0, result.stderr
    assert "Assignment: 1.5 h" in result.stdout
    assert "DS exam: 0.5 h" in result.stdout
    assert result.stdout.index("Assignment") < result.stdout.index("DS exam")


def test_missing_csv(tmp_path):
    """Missing files must return the requested code 1 and useful stderr."""
    result = run_cli(tmp_path / "missing.csv", "--hours", "2")
    assert result.returncode == 1
    assert "missing.csv" in result.stderr
    assert "Traceback" not in result.stderr


def test_malformed_csv(tmp_path):
    """CSV validation errors should remain readable CLI errors."""
    path = tmp_path / "bad.csv"
    path.write_text("title,importance,effort_h,deadline\nBad,9,1,2026-10-30\n")
    result = run_cli(path, "--hours", "2")
    assert result.returncode == 1
    assert "line 2" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("hours", ["-1", "nan", "inf", "-inf"])
def test_invalid_budget(hours):
    """Invalid budgets cannot silently produce empty or unlimited plans."""
    result = run_cli("samples/tasks.csv", f"--hours={hours}")
    assert result.returncode != 0
    assert "hours" in result.stderr.lower()
    assert "Traceback" not in result.stderr


def test_invalid_today():
    """Argparse should reject invalid dates before planning."""
    result = run_cli("samples/tasks.csv", "--hours", "2", "--today", "2026-02-30")
    assert result.returncode == 2
    assert "--today" in result.stderr


def test_zero_budget():
    """Zero available hours schedules no tasks."""
    result = run_cli("samples/tasks.csv", "--hours", "0")
    assert result.returncode == 0
    assert "No tasks scheduled" in result.stdout
    assert "Assignment:" not in result.stdout


def test_empty_task_list(tmp_path):
    """A valid header without rows is an empty plan, not a crash."""
    path = tmp_path / "empty.csv"
    path.write_text("title,importance,effort_h,deadline\n")
    result = run_cli(path, "--hours", "2")
    assert result.returncode == 0
    assert "No tasks scheduled" in result.stdout


def test_default_today_and_zero_effort(tmp_path):
    """Default dates work, zero-effort rows do not consume the budget."""
    path = tmp_path / "tasks.csv"
    path.write_text(
        "title,importance,effort_h,deadline\nFree,5,0,2026-01-01\nWork,4,3,2026-01-01\n"
    )
    result = run_cli(path, "--hours", "0.25")
    assert result.returncode == 0
    assert "Work: 0.25 h" in result.stdout
    assert "Free:" not in result.stdout
