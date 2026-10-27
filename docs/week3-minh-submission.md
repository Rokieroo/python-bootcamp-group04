# Minh Week 3 submission

Issue: [#48](https://github.com/Rokieroo/python-bootcamp-group04/issues/48).
Branch: `py/w3-MikaelVo639`, based on main `3e2b326`.
Assigned reviewer: hdang-207. Human approval, merge and weekly tag are pending.

## Implementation

- `dates.parse_due(text, today)` handles strict YYYY-MM-DD, tomorrow, in N
  days and English weekday names/abbreviations. Weekdays always advance;
  unsupported or out-of-range dates raise ValueError.
- `log_stats.analyse(pairs)` returns Counter counts, nearest-rank p95 values
  and the route with highest p95. Ties choose the first observed route;
  empty input returns empty mappings and `slowest=None`.
- CLI reuses Minh's W2 CSV loader and task model, ranks tasks by importance
  divided by remaining days (minimum one), and permits a partial final task.
  Missing/invalid files return 1; invalid arguments return 2 without a traceback.
- Missing annotations and docstrings were completed in Minh's W1/W2 functions.
  Instructor tests and teammates' source files were not changed.

## Verification on 2026-10-27

Commands use `.venv/Scripts/python.exe` on this Windows checkout.

| Command (after the Python executable) | Result |
|---|---|
| `scripts/check.py --member minh_vg --week 3` | Ruff clean; 3 instructor tests passed |
| `-m pytest -q tests/test_w1.py tests/test_w2.py tests/test_w3.py --member minh_vg --variant 2` | 11 passed |
| `-m pytest -q student_tests/test_minh_w3_dates.py student_tests/test_minh_w3_log_stats.py student_tests/test_minh_w3_cli.py` | 32 passed; all first observed failing before implementation |
| `-m pytest -q members/minh_vg/w1/test_exercises.py members/minh_vg/w2/tests_for_thang.py student_tests` | 141 passed, 1,543 graph subtests passed |
| `-m ruff check .` | All checks passed |

Local pytest uses a unique `--basetemp=.pytest_tmp/<run-name>` to keep temporary
files in the writable workspace. The initial default temporary-directory
permission error was resolved with that command-line option.

Sample:

```console
python -m members.minh_vg.w3.cli samples/tasks.csv --hours 2 --today 2026-10-26
Tonight (2 h):
 1. Assignment: 1.5 h
 2. DS exam: 0.5 h
```

## Existing full-suite failures

Both commands were run against this branch and a separate extracted snapshot
of unchanged main `3e2b326`. Results reproduce on the baseline:

- Default full pytest: five collection errors due to W2 packages sharing the
  import name `w2`: Man's `test_io_utils.py` and `tests_for_dat_vt.py`, Minh's
  `tests_for_thang.py`, Thinh's `tests_for_man.py`, and Thang's
  `tests_for_MikaelVo639.py`.
- Full pytest with `--import-mode=importlib`: branch has 256 passed, 11 skipped,
  1,543 subtests passed, and two failures; baseline has 224 passed, 11 skipped,
  1,543 subtests passed, and the same two failures:
  - `members/man_lpd/w2/test_io_utils.py::test_invalid_row_reports_line_three[,3,1,2026-10-30]`:
    Man's loader accepts an empty title instead of raising ValueError.
  - `members/man_lpd/w2/tests_for_dat_vt.py::test_summary_roundingCase`:
    Dat's median is 4.444 where the peer test expects 4.44.

These are recorded rather than modifying teammates' work. The CI-selected
student suite and Minh's instructor suites pass. Remote CI is checked after
PR creation; local results alone do not establish remote success.

## Review handoff

At the submission check the only open PR was Dat W3 (#55). Thang's W3 issue
#46 and team issues #49-52 had no matching open PR. Minh's assigned review of
Thang and suggested team reviews remain pending until those PRs exist.
An AI code review of this branch does not substitute for hdang-207's approval.

## Reflection draft (W3-4)

Python's `Counter` and dictionaries group route statistics without declaring C++ container templates.
Type hints document interfaces while Python still evaluates values dynamically at runtime.
`argparse`, `datetime` and exceptions provide reusable parsing and error reporting with little boilerplate.

## AI use and hours

OpenAI Codex using Superpowers prepared the implementation, behavioral tests,
documentation and submission, and ran the commands above. The reflection is
an AI-assisted draft for the student to review; personal understanding or
student verification is not asserted. Estimated and actual student hours
were not supplied and remain unspecified.
