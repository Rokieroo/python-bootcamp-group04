"""T-W3.2: end-to-end test running the planner CLI on the sample CSV."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_planner(*args):
    return subprocess.run(
        [sys.executable, "-m", "shared.study_planner", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_renders_plan_for_sample_csv():
    result = run_planner("samples/tasks.csv", "--hours", "2", "--today", "2026-10-26")
    assert result.returncode == 0, result.stderr
    assert result.stdout == "Plan (2 h):\n  1. Assignment: 1.5 h\n  2. DS exam: 0.5 h\n"


def test_cli_with_no_hours_schedules_nothing():
    result = run_planner("samples/tasks.csv", "--hours", "0", "--today", "2026-10-26")
    assert result.returncode == 0, result.stderr
    assert result.stdout == "No tasks scheduled.\n"
