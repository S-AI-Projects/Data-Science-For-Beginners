"""
Histogram Refactoring: Extracted Bin Index Resolution (R39-T030)

Extends lesson 10 (Visualizing Distributions) by establishing a baseline binning implementation
and refactoring it by extracting the bin index lookup responsibility into a standalone helper:
`find_bin_index(val, bin_edges)`.

Contract:
- Intermediate bins are half-open: [edge_i, edge_{i+1})
- Final bin is right-inclusive: [edge_{k-1}, edge_k]
- Values outside [edge_0, edge_k] return None (out of bounds).
"""

from typing import List, Optional, Tuple


def compute_histogram_counts_baseline(values: List[float], bin_edges: List[float]) -> Tuple[List[int], List[float]]:
    """
    Monolithic baseline implementation: combines boundary checking, interval searching,
    and frequency counting in a single loop.
    """
    if len(bin_edges) < 2:
        raise ValueError("At least two bin edges required.")
    for i in range(len(bin_edges) - 1):
        if bin_edges[i] >= bin_edges[i + 1]:
            raise ValueError("Bin edges must be strictly increasing.")

    num_bins = len(bin_edges) - 1
    counts = [0] * num_bins
    out_of_bounds = []

    for val in values:
        if val < bin_edges[0] or val > bin_edges[-1]:
            out_of_bounds.append(val)
            continue

        placed = False
        for i in range(num_bins):
            left = bin_edges[i]
            right = bin_edges[i + 1]
            is_final = (i == num_bins - 1)

            if (left <= val < right) or (is_final and val == right):
                counts[i] += 1
                placed = True
                break

        if not placed:
            out_of_bounds.append(val)

    return counts, out_of_bounds


# ============================================================================
# REFACTORED IMPLEMENTATION (Extracted Responsibility: find_bin_index)
# ============================================================================


def find_bin_index(val: float, bin_edges: List[float]) -> Optional[int]:
    """
    Extracted single-responsibility function:
    Resolves the exact bin index for a given value using half-open intermediate intervals
    and a right-inclusive final bin. Returns None if value is out of bounds.
    """
    if val < bin_edges[0] or val > bin_edges[-1]:
        return None

    num_bins = len(bin_edges) - 1
    for i in range(num_bins):
        left = bin_edges[i]
        right = bin_edges[i + 1]
        is_final = (i == num_bins - 1)

        if (left <= val < right) or (is_final and val == right):
            return i

    return None


def compute_histogram_counts_refactored(values: List[float], bin_edges: List[float]) -> Tuple[List[int], List[float]]:
    """
    Refactored counting function utilizing extracted find_bin_index helper.
    """
    if len(bin_edges) < 2:
        raise ValueError("At least two bin edges required.")
    for i in range(len(bin_edges) - 1):
        if bin_edges[i] >= bin_edges[i + 1]:
            raise ValueError("Bin edges must be strictly increasing.")

    num_bins = len(bin_edges) - 1
    counts = [0] * num_bins
    out_of_bounds = []

    for val in values:
        bin_idx = find_bin_index(val, bin_edges)
        if bin_idx is None:
            out_of_bounds.append(val)
        else:
            counts[bin_idx] += 1

    return counts, out_of_bounds


# Standard contract export
compute_histogram_counts = compute_histogram_counts_refactored


if __name__ == "__main__":
    bins = [0, 10, 20]
    vals = [0, 9, 10, 20]
    b_counts, b_oob = compute_histogram_counts_baseline(vals, bins)
    r_counts, r_oob = compute_histogram_counts_refactored(vals, bins)
    print("Baseline:", b_counts, b_oob)
    print("Refactored:", r_counts, r_oob)
    print("Equivalence verified:", (b_counts, b_oob) == (r_counts, r_oob))
