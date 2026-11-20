# R39-T041: Histogram Boundary Accounting

## Overview
This local applied lab extends [A Brief Introduction to Statistics and Probability](../../README.md) with explicit half-open bin accounting where the final bin is right-inclusive.

- Bins $[b_0, b_1, \dots, b_k]$ define $k$ bins:
  - Bins $0$ through $k-2$: $[b_i, b_{i+1})$ (left-inclusive, right-exclusive)
  - Final bin $k-1$: $[b_{k-1}, b_k]$ (left-inclusive, right-inclusive)
- Values outside the range ($< b_0$ or $> b_k$) are recorded in separate underflow/overflow collections.

## Contract & Fixture
- **Input Bins:** `[0, 10, 20]`
- **Input Values:** `[0, 9, 10, 20]`
- **Result Counts:** `[2, 2]`
  - `0` and `9` fall into $[0, 10)$
  - `10` and `20` fall into $[10, 20]$
- Values outside range reported separately in `below_range` and `above_range`.

## Scope & Limitations
- Pure Python 3 standard library implementation without external dependencies (no NumPy or cloud services required).
- Minimal local runnable concept example focusing on boundary precision.

## Invocation & Output
```bash
python3 1-Introduction/04-stats-and-probability/applied-labs/r39-t041/example.py
```
Output:
```json
{"bins": [0, 10, 20], "counts": [2, 2], "below_range": [], "above_range": [], "total_in_range": 4, "total_out_of_range": 0}
```

Run tests:
```bash
python3 -m unittest discover -s 1-Introduction/04-stats-and-probability/applied-labs/r39-t041 -p "test_*.py"
```
