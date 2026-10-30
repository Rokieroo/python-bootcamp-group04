"""Print tonight's plan using Minh's W2 task model and CSV loader."""

import argparse
import sys
from datetime import date
from math import isfinite

from members.minh_vg.w2.io_utils import load_tasks


def build_parser() -> argparse.ArgumentParser:
    """Describe the CSV input, finite hour budget and optional reference date."""
    parser = argparse.ArgumentParser(description="Plan tonight's study session.")
    parser.add_argument("csv", help="path to the tasks CSV")
    parser.add_argument("--hours", type=float, required=True, help="hours available")
    parser.add_argument("--today", type=date.fromisoformat, help="YYYY-MM-DD (default: today)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Rank tasks by urgency, fill the budget and report readable input errors."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if not isfinite(args.hours) or args.hours < 0:
        parser.error("--hours must be finite and nonnegative")
    today = args.today if args.today is not None else date.today()
    try:
        tasks = load_tasks(args.csv)
    except (OSError, ValueError) as exc:
        print(f"Cannot load {args.csv}: {exc}", file=sys.stderr)
        return 1

    ranked = sorted(
        tasks,
        key=lambda task: task.importance / max(1, task.days_left(today)),
        reverse=True,
    )
    remaining = args.hours
    lines = []
    for task in ranked:
        if remaining <= 0:
            break
        used = min(task.effort_h, remaining)
        if used > 0:
            lines.append(f" {len(lines) + 1}. {task.title}: {used:g} h")
            remaining -= used
    print(f"Tonight ({args.hours:g} h):")
    print("\n".join(lines) if lines else "No tasks scheduled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
