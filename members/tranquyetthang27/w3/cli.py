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
    parser.add_argument("filename", type=str, help="Path to the tasks CSV file")
    parser.add_argument("--hours", type=float, default=2.0, help="Target total hours for tonight")
    parser.add_argument("--today", type=parse_date, default=date.today(), help="Reference date")
    
    args = parser.parse_args()
    
    # 2. Check if file exists
    csv_path = Path(args.filename)
    if not csv_path.is_file():
        print(f"Error: The file '{args.filename}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    # 3. Dynamic and Robust CSV Parsing
    tasks = []
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Dynamically locate the task name/title column
                name = None
                for key in ["task", "name", "title", "todo", "item"]:
                    if key in row:
                        name = row[key]
                        break
                if name is None and row:  # Fallback to the first column if no match found
                    name = list(row.values())[0]
                
                # Dynamically locate the hours/duration column
                hours = None
                for key in ["hours", "hour", "duration", "time"]:
                    if key in row:
                        try:
                            hours = float(row[key])
                            break
                        except ValueError:
                            continue
                if hours is None and row:  # Fallback to the last column if no match found
                    try:
                        hours = float(list(row.values())[-1])
                    except ValueError:
                        hours = 0.0

                if name:
                    tasks.append({
                        "name": name,
                        "hours": hours
                    })
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Print the formatted output
    print(f"Tonight ({args.hours:.1f} h):")
    
    for i, task in enumerate(tasks, start=1):
        name_part = f"  {i}. {task['name']} "
        hours_part = f" {task['hours']:.1f} h"
        
        # Dot padding up to 30 characters wide
        dotted_line = name_part.ljust(30, ".") + hours_part
        print(dotted_line)

if __name__ == "__main__":
    main()
