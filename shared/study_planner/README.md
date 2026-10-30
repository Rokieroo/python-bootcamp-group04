# Study Planner

A modular task scheduling tool using greedy time allocation.

## Architecture

The planning pipeline runs through four composable steps:
1. `parse_csv(path)`: Loads tasks from a CSV file into `Task` instances.
2. `prioritise(tasks, today)`: Ranks tasks descending by `importance / max(1, days_left)`.
3. `allocate(tasks, hours)`: Greedily consumes available hours across tasks, allowing a partial split on the final task.
4. `render(blocks)`: Formats scheduled task blocks into a plain-text plan.

## CSV Format

The file must include this exact header on line 1:

```csv
title,importance,effort_h,deadline
```

Fields:
- `title`: Non-empty string.
- `importance`: Integer.
- `effort_h`: Float.
- `deadline`: ISO-8601 date (`YYYY-MM-DD`).

## Usage

```python
from datetime import date
from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render

tasks = parse_csv("tasks.csv")
ranked = prioritise(tasks, today=date.today())
blocks = allocate(ranked, hours=6.0)
print(render(blocks))
```