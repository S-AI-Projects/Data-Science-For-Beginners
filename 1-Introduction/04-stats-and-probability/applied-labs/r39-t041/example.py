"""Histogram boundary accounting concept example (R39-T041).

Extends the statistics and probability lesson with explicit half-open bin
accounting where the final bin is right-inclusive.
"""

from __future__ import annotations
import json
from typing import Any, Dict, List, Sequence


def count_histogram_bins(
    values: Sequence[float], bins: Sequence[float]
) -> Dict[str, Any]:
    """Count values in explicit half-open bins with a right-inclusive final bin.

    Bins [b_0, b_1, ..., b_k] define k bins:
      - Bins 0 to k-2: [b_i, b_{i+1})  (left-inclusive, right-exclusive)
      - Final bin k-1: [b_{k-1}, b_k]  (left-inclusive, right-inclusive)

    Values < b_0 are collected in below_range.
    Values > b_k are collected in above_range.
    """
    if len(bins) < 2:
        raise ValueError("At least two bin edges are required to define bins.")
    for i in range(len(bins) - 1):
        if bins[i] >= bins[i + 1]:
            raise ValueError(f"Bin edges must be strictly increasing: {bins[i]} >= {bins[i+1]}")

    num_bins = len(bins) - 1
    counts = [0] * num_bins
    below_range: List[float] = []
    above_range: List[float] = []

    for v in values:
        if v < bins[0]:
            below_range.append(v)
        elif v > bins[-1]:
            above_range.append(v)
        else:
            placed = False
            for i in range(num_bins):
                is_last_bin = (i == num_bins - 1)
                lower = bins[i]
                upper = bins[i + 1]
                if is_last_bin:
                    if lower <= v <= upper:
                        counts[i] += 1
                        placed = True
                        break
                else:
                    if lower <= v < upper:
                        counts[i] += 1
                        placed = True
                        break
            if not placed:
                above_range.append(v)

    return {
        "bins": list(bins),
        "counts": counts,
        "below_range": below_range,
        "above_range": above_range,
        "total_in_range": sum(counts),
        "total_out_of_range": len(below_range) + len(above_range),
    }


def main() -> None:
    bins = [0, 10, 20]
    values = [0, 9, 10, 20]
    result = count_histogram_bins(values, bins)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
