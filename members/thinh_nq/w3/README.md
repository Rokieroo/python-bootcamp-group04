# Week 3: Standard Library and Tooling (thinh_nq)

## Overview
This package contains Week 3 deliverables for Nguyen Quoc Thinh (`thinh_nq` / `thinh-nguyen-007`):

- `dates.py`: Human-friendly due date parsing (`parse_due`), supporting ISO dates, relative descriptions (`today`, `tomorrow`, `in N days`), and next-occurrence weekdays.
- `log_stats.py`: Log request count aggregation and 95th-percentile (`p95`) latency computation using the nearest-rank method.
- `cli.py`: Command-line interface planning tonight's study session based on available hours and deadlines.
- `test_w3_thinh.py`: Comprehensive unit tests covering all functions and edge cases.

## C++ vs Python Differences
1. **Date & Time Ergonomics**: In C++, handling human date representations requires external libraries (like `date.h` or `<chrono>`) and manual date math. In Python, `datetime.date` combined with `datetime.timedelta` provides expressive, built-in date calculations with automatic leap year and calendar awareness.
2. **Standard Library Collections**: Python's `collections.Counter` and `defaultdict` eliminate repetitive boilerplate for frequency counting and bucket aggregation compared to C++'s `std::map<Key, Value>` or `std::unordered_map`.
3. **CLI Argument Parsing**: Python's built-in `argparse` standard library handles type conversions (such as `date.fromisoformat`), help generation, and error reporting cleanly without external dependencies.
