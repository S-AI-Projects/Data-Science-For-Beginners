"""Chart-data consistency refactoring teaching example (R39-T046).

Extends the Visualizing Quantities lesson. Builds a category summary and
verifies that labels, counts, and displayed total consistently refer to the
exact same underlying data. Demonstrates refactoring by extracting category
aggregation into a dedicated component while preserving contract equivalence.
"""

from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Sequence, Set


def summarize_categories_baseline(
    rows: Sequence[str], filter_categories: Optional[Set[str]] = None
) -> Dict[str, Any]:
    """Baseline monolithic implementation calculating counts and total."""
    filtered_rows = [r for r in rows if filter_categories is None or r in filter_categories]
    counts: Dict[str, int] = {}
    for item in filtered_rows:
        counts[item] = counts.get(item, 0) + 1

    total = len(filtered_rows)
    # Verification check: displayed total must equal sum of category counts
    if sum(counts.values()) != total:
        raise ValueError("Consistency violation: counts sum does not match total.")

    return {
        "labels": sorted(counts.keys()),
        "counts": counts,
        "total": total,
    }


class CategoryAggregator:
    """Extracted named responsibility: manages category frequency tallying."""

    @staticmethod
    def aggregate(items: Sequence[str]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        return counts


def summarize_categories_refactored(
    rows: Sequence[str], filter_categories: Optional[Set[str]] = None
) -> Dict[str, Any]:
    """Refactored implementation delegating tallying to CategoryAggregator."""
    filtered_rows = [r for r in rows if filter_categories is None or r in filter_categories]
    counts = CategoryAggregator.aggregate(filtered_rows)
    total = sum(counts.values())

    return {
        "labels": sorted(counts.keys()),
        "counts": counts,
        "total": total,
    }


def verify_equivalence(
    rows: Sequence[str], filter_categories: Optional[Set[str]] = None
) -> bool:
    """Prove before/after equivalence between baseline and refactored versions."""
    base = summarize_categories_baseline(rows, filter_categories)
    refac = summarize_categories_refactored(rows, filter_categories)
    return base == refac


def main() -> None:
    # Stated fixture: Rows A,A,B,C,C,C yield A=2,B=1,C=3,total=6; filtering to A/B gives total 3.
    data = ["A", "A", "B", "C", "C", "C"]
    full_res = summarize_categories_refactored(data)
    filtered_res = summarize_categories_refactored(data, filter_categories={"A", "B"})

    print("Full summary:", json.dumps(full_res))
    print("Filtered summary:", json.dumps(filtered_res))
    print("Equivalence verified:", verify_equivalence(data))
    print("Filtered equivalence verified:", verify_equivalence(data, {"A", "B"}))


if __name__ == "__main__":
    main()
