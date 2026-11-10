# Applied Lab R39-T030: Histogram Refactoring (Extracted Responsibility)

## Overview
This applied lab extends the "Visualizing Distributions" lesson by demonstrating software engineering refactoring principles applied to histogram binning.
It begins with a monolithic baseline implementation and extracts the discrete responsibility of resolving bin membership into an independent helper function: `find_bin_index`.

## Extracted Responsibility & Refactoring
- **Baseline:** `compute_histogram_counts_baseline` interleaves boundary checks, edge traversal, and array updates.
- **Extracted Component:** `find_bin_index(val, bin_edges)` encapsulates the half-open intermediate `[left, right)` and closed terminal `[left, right]` logic in isolation, returning an integer index or `None`.
- **Refactored Aggregator:** `compute_histogram_counts_refactored` delegates bin resolution to `find_bin_index`, achieving clear separation of concerns.

## Equivalence Proof
The unit test suite mathematically and behaviorally proves that for all input permutations, boundary conditions, and out-of-bounds observations:
$$\text{compute\_histogram\_counts\_baseline}(values, edges) \equiv \text{compute\_histogram\_counts\_refactored}(values, edges)$$

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 3-Data-Visualization/10-visualization-distributions/applied-labs/r39-t030 -p "test_*.py" -v
```
