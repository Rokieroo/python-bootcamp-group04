"""Entry point for shared study planner CLI with error handling."""

import argparse
import sys
from datetime import date
from pathlib import Path

from shared.study_planner.allocate import allocate
from shared.study_planner.errors import InfeasiblePlan, check_feasible
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render


def build_parser() -> argparse.ArgumentParser:
    """Build command-line parser for the study planner."""
    parser = argparse.ArgumentParser(description="Shared study planner.")
    parser.add_argument("csv", help="path to the tasks CSV")
    parser.add_argument("--hours", type=float, required=True, help="hours available")
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="YYYY-MM-DD (default: today)",
    )
    parser.add_argument(
        "--check-feasible",
        action="store_true",
        help="check if total task effort is feasible within available hours",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Execute the study planner pipeline with error handling."""
    parser = build_parser()
    args = parser.parse_args(argv)

    path = Path(args.csv)
    if not path.is_file():
        print(f"error: file not found: {args.csv}", file=sys.stderr)
        return 1

    try:
        tasks = parse_csv(path)
    except (ValueError, OSError) as exc:
        print(f"error: failed to parse {args.csv}: {exc}", file=sys.stderr)
        return 1

    if not tasks:
        print(f"error: task file is empty: {args.csv}", file=sys.stderr)
        return 1

    if args.check_feasible:
        try:
            check_feasible(tasks, args.hours)
        except InfeasiblePlan as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    ranked = prioritise(tasks, today=args.today)
    blocks = allocate(ranked, hours=args.hours)
    print(render(blocks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
