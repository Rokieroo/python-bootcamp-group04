# Week 3 individual work

The CLI reuses the Week 2 CSV loader and the shared ranking and allocation functions. Run:

```powershell
python -m members.man_lpd.w3.cli samples/tasks.csv --hours 2 --today 2026-10-26
python scripts/check.py --member man_lpd --week 3
```

## W3-4 reflection draft

Review and rewrite these lines in your own words before adding them to the PR:

Python's `datetime` module provides date arithmetic directly, without manually tracking month lengths.
Type hints document expected values, but Python does not enforce them like C++ declarations at runtime.
Python's `Counter` and `defaultdict` make grouping and counting simpler than setting up maps manually.

## AI use

OpenAI Codex generated and tested the W3 code and drafted the reflection. Review and understand each
change yourself before submission; see `docs/ai-use-log.md`.
