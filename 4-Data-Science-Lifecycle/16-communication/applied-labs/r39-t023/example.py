"""
Chart-Data Consistency: Two Independent Approaches (R39-T023)

Extends lesson 16 (Communication) by ensuring that category breakdown counts
and aggregate summary totals always refer to the same underlying filtered dataset.
Compares a direct procedural loop against an independent collections.Counter implementation.
"""

from collections import Counter
from typing import Dict, Iterable, Optional, Tuple


def summarize_categories_procedural(
    rows: Iterable[str], allowed_categories: Optional[Iterable[str]] = None
) -> Tuple[Dict[str, int], int]:
    """
    Direct procedural implementation:
    Iterates through rows, applies filter if provided, and accumulates counts into a dict.
    Returns: (category_counts, total_count)
    """
    filter_set = set(allowed_categories) if allowed_categories is not None else None
    counts: Dict[str, int] = {}

    for row in rows:
        if filter_set is not None and row not in filter_set:
            continue
        counts[row] = counts.get(row, 0) + 1

    total = sum(counts.values())
    return counts, total


def summarize_categories_counter(
    rows: Iterable[str], allowed_categories: Optional[Iterable[str]] = None
) -> Tuple[Dict[str, int], int]:
    """
    Independent reference implementation using collections.Counter:
    Pre-filters rows and uses standard Counter for aggregation.
    Returns: (category_counts, total_count)
    """
    filter_set = set(allowed_categories) if allowed_categories is not None else None
    if filter_set is not None:
        filtered = [r for r in rows if r in filter_set]
    else:
        filtered = list(rows)

    c = Counter(filtered)
    counts = dict(c)
    total = sum(counts.values())
    return counts, total


if __name__ == "__main__":
    data = ["A", "A", "B", "C", "C", "C"]
    unfiltered_counts, unfiltered_total = summarize_categories_procedural(data)
    print("Unfiltered:", unfiltered_counts, "Total:", unfiltered_total)

    filtered_counts, filtered_total = summarize_categories_procedural(data, allowed_categories=["A", "B"])
    print("Filtered to A/B:", filtered_counts, "Total:", filtered_total)
