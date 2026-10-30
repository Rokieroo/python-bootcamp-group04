"""W3-3: print tonight's study plan from a task CSV."""

import argparse
import sys
from datetime import date
from pathlib import Path

from members.man_lpd.w2.io_utils import load_tasks
from shared.contract import Task
from shared.study_planner.allocate import allocate
from shared.study_planner.prioritise import prioritise


def build_parser() -> argparse.ArgumentParser:
    """Define the CSV path, available hours, and optional reference date."""
    parser = argparse.ArgumentParser(description="Plan tonight's study session.")
    parser.add_argument("csv", help="path to the tasks CSV")
    parser.add_argument("--hours", type=float, required=True, help="hours available")
    parser.add_argument("--today", type=date.fromisoformat, default=None, help="YYYY-MM-DD (default: today)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Load W2 tasks, rank and allocate them, then print tonight's plan."""
    args = build_parser().parse_args(argv)
    today = args.today if args.today is not None else date.today()
    try:
        own_tasks = load_tasks(Path(args.csv))
        tasks = [Task(t.title, t.importance, t.effort_h, t.deadline) for t in own_tasks]
        blocks = allocate(prioritise(tasks, today), args.hours)
    except FileNotFoundError:
        print(f"error: task file not found: {args.csv}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Tonight ({sum(block.hours for block in blocks):.1f} h):")
    for number, block in enumerate(blocks, 1):
        print(f" {number}. {block.task.title} ...... {block.hours:g} h")
    if not blocks:
        print("No tasks scheduled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
