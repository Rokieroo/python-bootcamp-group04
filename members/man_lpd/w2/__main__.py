from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    """Load and print the sample W2 tasks."""
    csv_path = Path(__file__).with_name("tasks.csv")
    tasks = load_tasks(csv_path)

    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()
