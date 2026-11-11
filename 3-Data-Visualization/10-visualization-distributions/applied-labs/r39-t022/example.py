"""
Histogram Boundary Accounting (R39-T022)

Extends lesson 10 (Visualizing Distributions) with explicit binning logic:
- Intermediate bins are half-open: [edge_i, edge_{i+1})
- The terminal bin is closed (right-inclusive): [edge_{k-1}, edge_k]
- Values strictly outside [edge_0, edge_k] are reported in out_of_bounds.
"""

from typing import List, Tuple


def compute_histogram_counts(values: List[float], bin_edges: List[float]) -> Tuple[List[int], List[float]]:
    """
    Counts values into explicit bins defined by bin_edges.

    Args:
        values: List of numeric values to be binned.
        bin_edges: Strictly increasing sequence of at least two bin edges.

    Returns:
        Tuple of (bin_counts, out_of_bounds)
    """
    if len(bin_edges) < 2:
        raise ValueError("At least two bin edges are required.")
    for i in range(len(bin_edges) - 1):
        if bin_edges[i] >= bin_edges[i + 1]:
            raise ValueError("Bin edges must be strictly increasing.")

    num_bins = len(bin_edges) - 1
    counts = [0] * num_bins
    out_of_bounds = []

    min_edge = bin_edges[0]
    max_edge = bin_edges[-1]

    for val in values:
        if val < min_edge or val > max_edge:
            out_of_bounds.append(val)
            continue

        placed = False
        for i in range(num_bins):
            left = bin_edges[i]
            right = bin_edges[i + 1]
            is_final_bin = (i == num_bins - 1)

            # Half-open [left, right) for intermediate bins,
            # right-inclusive [left, right] for the terminal bin.
            if (left <= val < right) or (is_final_bin and val == right):
                counts[i] += 1
                placed = True
                break

        if not placed:
            out_of_bounds.append(val)

    return counts, out_of_bounds


if __name__ == "__main__":
    bins = [0, 10, 20]
    vals = [0, 9, 10, 20]
    counts, oob = compute_histogram_counts(vals, bins)
    print(f"Bins: {bins}")
    print(f"Values: {vals}")
    print(f"Counts: {counts}")
    print(f"Out of bounds: {oob}")
