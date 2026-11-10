# Applied Lab R39-T023: Chart-Data Consistency

## Overview
This applied lab extends the "The Data Science Lifecycle: Communication" lesson by ensuring that categorical visual components (labels and counts) and aggregate indicator metrics (total count) stay strictly synchronized across data filtering operations.

## Focus: Comparison of Two Approaches
We evaluate two independent aggregation strategies:
1. **Procedural Direct Accumulator:** Iterates through records, conditionally filters, and updates a dictionary.
2. **Standard Library Counter Reference:** Uses Python's `collections.Counter` on a pre-filtered list.

Both approaches are verified for algebraic and behavioural equivalence across unfiltered and filtered scenarios.

## Fixtures & Expected Results
- **Dataset:** `['A', 'A', 'B', 'C', 'C', 'C']`
- **Unfiltered:** `{'A': 2, 'B': 1, 'C': 3}`, `total = 6`
- **Filtered to `['A', 'B']`:** `{'A': 2, 'B': 1}`, `total = 3`

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t023 -p "test_*.py" -v
```

## Scope & Limitations
This lab is a purely local aggregation consistency check using Python standard library data structures. It does not interface with front-end charting frameworks or external databases.
