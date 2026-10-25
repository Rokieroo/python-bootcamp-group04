"""W3-3: print tonight's study plan from a task CSV."""

import argparse
import sys
from datetime import date

from members.dat_vt.w2.io_utils import load_tasks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan tonight's study session.")
    parser.add_argument("csv", help="path to the tasks CSV")
    parser.add_argument("--hours", type=float, required=True, help="hours available")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(),
                        help="YYYY-MM-DD (default: today)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        tasks = load_tasks(args.csv)
    except FileNotFoundError:
        print(f"error: file not found: {args.csv}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    # Earliest deadline first, more important first on ties; fill the hours greedily.
    tasks.sort(key=lambda t: (t.days_left(args.today), -t.importance))
    left = args.hours
    print(f"Tonight ({args.hours:.1f} h):")
    n = 0
    for task in tasks:
        if left <= 0:
            break
        hours = min(task.effort_h, left)
        left -= hours
        n += 1
        print(f"{n:2}. {task.title + ' ':.<17} {hours:.1f} h")
    return 0


if __name__ == "__main__":
    sys.exit(main())
