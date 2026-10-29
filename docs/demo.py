"""Short demo showing the study planner pipeline execution."""

from datetime import date
from pathlib import Path
import tempfile

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render

SAMPLE_CSV = """title,importance,effort_h,deadline
Prepare Report,5,3.0,2026-10-30
Review Pull Requests,3,2.0,2026-10-31
Update Documentation,2,2.0,2026-11-02
"""


def main() -> None:
    with tempfile.NamedTemporaryFile("w+", suffix=".csv", delete=False) as tmp:
        tmp.write(SAMPLE_CSV)
        tmp_path = Path(tmp.name)

    try:
        tasks = parse_csv(tmp_path)
        today = date(2026, 10, 29)
        ranked = prioritise(tasks, today=today)
        blocks = allocate(ranked, hours=4.0)
        print(render(blocks))
    finally:
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()