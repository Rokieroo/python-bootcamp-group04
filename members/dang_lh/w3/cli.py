import argparse
from datetime import date
from pathlib import Path
import sys

from members.dang_lh.w2.io_utils import load_tasks
from members.dang_lh.w2.models import Task

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description = "Plan tonight's study session.")
    parser.add_argument("csv", help = "path to the tasks CSV")
    parser.add_argument("--hours", type = float, required = True, help = "hours available")
    parser.add_argument("--today", type = date.fromisoformat, default = date.today(), help = "YYYY-MM-DD (default: today)",)


    return parser

def prioritise_tasks(tasks: list[Task], today: date) -> list[Task]:
    tasks = sorted(tasks, key = lambda t: t.importance / max(1, t.days_left(today)), reverse = True)
    return tasks

def allocate_hours(tasks: list[Task], hours: float) -> list[tuple[Task, float]]:
    allocated = []
    remaining = hours

    for t in tasks:
        if remaining <= 0: 
            break
        take = min(t.effort_h, remaining)
        if take > 0:
            allocated.append((t, take))
            remaining -= take

    return allocated

def render_plan(plan: list[tuple[Task, float]], total_hours: float) -> str:
    lines = [f"Tonight ({total_hours:.1f} h):"]

    for i, (task, h) in enumerate(plan, 1):
        prefix = f" {i}. {task.title} "
        suffix = f" {h:.1f} h"
        dots_count = max(1, 24 - len(prefix) - len(suffix))
        lines.append(f"{prefix}{'.' * dots_count}{suffix}")
    
    return "\n".join(lines)

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"Error: file not found '{args.csv}'", file = sys.stderr)
        return 1

    try:
        tasks = load_tasks(csv_path)
    except Exception as exc:
        print(f"Error loading CSV: {exc}", file = sys.stderr)
        return 1
    
    ranked = prioritise_tasks(tasks, args.today)
    plan = allocate_hours(ranked, args.hours)

    print(render_plan(plan, args.hours))
    return 0

if __name__ == "__main__":
    sys.exit(main())
            
    