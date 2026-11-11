# Applied Lab R39-T022: Histogram Boundary Accounting

## Overview
This applied lab extends the "Visualizing Distributions" lesson by demonstrating how continuous numeric values are partitioned into discrete histogram bins with explicit boundary semantics:
- Intermediate bins are half-open intervals: `[edge_i, edge_{i+1})`
- The terminal bin is closed on both sides: `[edge_{k-1}, edge_k]`
- Values falling outside the total domain `[edge_0, edge_k]` are segregated into an `out_of_bounds` list.

## Fixture & Contract
- **Bin Edges:** `[0, 10, 20]`
- **Input Values:** `[0, 9, 10, 20]`
- **Expected Counts:** `[2, 2]`
  - Bin 0 `[0, 10)` contains `0` and `9` (count: 2).
  - Bin 1 `[10, 20]` contains `10` and `20` (count: 2).
- **Out of Bounds:** Values `< 0` or `> 20` reported separately.

## How to Run Tests
Run the unit test suite locally using the standard library:
```bash
python3 -m unittest discover -s 3-Data-Visualization/10-visualization-distributions/applied-labs/r39-t022 -p "test_*.py" -v
```

## Limitations & Simplifications
This lab is a purely algorithmic demonstration of boundary interval logic using Python's standard library. It does not generate Matplotlib or Seaborn graphics or interface with external data sources.
