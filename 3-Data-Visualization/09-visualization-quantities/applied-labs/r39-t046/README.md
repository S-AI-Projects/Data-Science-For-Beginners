# R39-T046: Chart-Data Consistency (Refactoring Teaching Example)

## Overview
This local applied lab extends [Visualizing Quantities](../../README.md) by demonstrating how to maintain strict consistency across chart labels, counts, and displayed totals, and how to safely refactor code by extracting a named responsibility.

## Contract & Fixture
- **Input Data:** `["A", "A", "B", "C", "C", "C"]`
- **Unfiltered Summary:** `A=2, B=1, C=3`, `total=6`
- **Filtered Summary (categories `{"A", "B"}`):** `A=2, B=1`, `total=3`

## Refactoring & Equivalence
- **Extracted Responsibility:** `CategoryAggregator.aggregate()` extracts frequency counting from the presentation formatting.
- **Equivalence:** `verify_equivalence()` mathematically proves that the baseline and refactored implementations produce identical output on all fixtures.

## Invocation & Output
```bash
python3 3-Data-Visualization/09-visualization-quantities/applied-labs/r39-t046/example.py
```
Output:
```text
Full summary: {"labels": ["A", "B", "C"], "counts": {"A": 2, "B": 1, "C": 3}, "total": 6}
Filtered summary: {"labels": ["A", "B"], "counts": {"A": 2, "B": 1}, "total": 3}
Equivalence verified: True
Filtered equivalence verified: True
```

Run tests:
```bash
python3 -m unittest discover -s 3-Data-Visualization/09-visualization-quantities/applied-labs/r39-t046 -p "test_*.py"
```
