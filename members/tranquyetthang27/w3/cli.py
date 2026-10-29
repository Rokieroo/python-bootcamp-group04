import argparse
import csv
from datetime import date
import sys
from pathlib import Path

def parse_date(date_str: str) -> date:
    """Helper to parse the --today argument."""
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD.")

def main():
    # 1. Setup argparse
    parser = argparse.ArgumentParser(description="Task analyzer command-line tool.")
    
    # Positional argument for the CSV file
    parser.add_argument("filename", type=str, help="Path to the tasks CSV file")
    
    # Optional arguments
    parser.add_argument("--hours", type=float, default=2.0, help="Target total hours for tonight")
    parser.add_argument("--today", type=parse_date, default=date.today(), 
                        help="Reference date in YYYY-MM-DD format (default: today)")
    
    args = parser.parse_args()
    
    # 2. Check if file exists using pathlib (as requested in study topics)
    csv_path = Path(args.filename)
    if not csv_path.is_file():
        print(f"Error: The file '{args.filename}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    # 3. Read and parse the CSV file (Simulating reuse of W2 logic)
    tasks = []
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Expected CSV columns: task, due, hours
                tasks.append({
                    "name": row["task"],
                    "due": row["due"],
                    "hours": float(row["hours"])
                })
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Print the formatted output match the example
    print(f"Tonight ({args.hours:.1f} h):")
    
    # Print tasks with dot padding for alignment
    for i, task in enumerate(tasks, start=1):
        name_part = f"  {i}. {task['name']} "
        hours_part = f" {task['hours']:.1f} h"
        
        # Adjust total width (e.g., 30 chars) to dynamically fill with dots
        dotted_line = name_part.ljust(30, ".") + hours_part
        print(dotted_line)

if __name__ == "__main__":
    main()
