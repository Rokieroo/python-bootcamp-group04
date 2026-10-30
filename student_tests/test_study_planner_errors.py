"""Tests for T-W3.3: study planner error handling and CLI integration."""

from datetime import date
from pathlib import Path
import pytest

from shared.contract import Task
from shared.study_planner.__main__ import main
from shared.study_planner.errors import InfeasiblePlan, check_feasible

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "samples" / "tasks.csv"


def test_missing_file_error(capsys, tmp_path: Path):
    nonexistent = tmp_path / "does_not_exist.csv"
    ret = main([str(nonexistent), "--hours", "2"])
    assert ret != 0
    captured = capsys.readouterr()
    assert "not found" in captured.err.lower()


def test_empty_file_error(capsys, tmp_path: Path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")
    ret = main([str(empty_csv), "--hours", "2"])
    assert ret != 0
    captured = capsys.readouterr()
    assert "empty" in captured.err.lower()


def test_infeasible_plan_check():
    tasks = [
        Task("Task 1", 3, 2.0, date(2026, 11, 1)),
        Task("Task 2", 4, 3.5, date(2026, 11, 2)),
    ]
    # Total effort is 5.5h. 5.0h is infeasible.
    with pytest.raises(InfeasiblePlan) as exc_info:
        check_feasible(tasks, available_h=5.0)
    assert exc_info.value.needed_h == 5.5
    assert exc_info.value.available_h == 5.0
    assert "Plan needs 5.5 h; only 5 h available" in str(exc_info.value)

    # 5.5h or more is feasible
    check_feasible(tasks, available_h=5.5)
    check_feasible(tasks, available_h=10.0)


def test_cli_infeasible_option(capsys, tmp_path: Path):
    tasks_csv = tmp_path / "heavy_tasks.csv"
    tasks_csv.write_text(
        "title,importance,effort_h,deadline\nBig Project,5,10.0,2026-11-01\n",
        encoding="utf-8",
    )
    ret = main([str(tasks_csv), "--hours", "2", "--check-feasible"])
    assert ret != 0
    captured = capsys.readouterr()
    assert "plan needs 10 h" in captured.err.lower()


def test_cli_successful_run(capsys):
    ret = main([str(SAMPLE_CSV), "--hours", "2", "--today", "2026-10-26"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Plan" in captured.out
    assert "Assignment" in captured.out
