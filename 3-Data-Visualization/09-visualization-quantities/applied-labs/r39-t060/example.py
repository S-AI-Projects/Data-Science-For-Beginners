"""Chart data consistency runnable concept example.
Task R39-T060.
"""

from typing import List, Dict, Any, Optional, Sequence


def summarize_quantities(
    rows: Sequence[str],
    filter_categories: Optional[Sequence[str]] = None,
    displayed_total_override: Optional[int] = None,
) -> Dict[str, Any]:
    """Calculate category counts and verify consistency with the displayed total.

    Connects inputs and outputs directly to visualizing quantities concepts:
    - labels: category axis ticks
    - counts: bar heights representing quantities
    - displayed_total: summary quantity badge or headline number
    """
    filtered_rows = [
        r for r in rows if (filter_categories is None or r in filter_categories)
    ]

    counts_map: Dict[str, int] = {}
    for item in filtered_rows:
        counts_map[item] = counts_map.get(item, 0) + 1

    labels = sorted(counts_map.keys())
    counts = [counts_map[lbl] for lbl in labels]
    actual_sum = sum(counts)
    displayed_total = (
        actual_sum if displayed_total_override is None else displayed_total_override
    )

    is_consistent = actual_sum == displayed_total and len(labels) == len(counts)
    error_message = None
    if not is_consistent:
        error_message = (
            f"Quantity mismatch: bar sum ({actual_sum}) != displayed total ({displayed_total})"
        )

    return {
        "labels": labels,
        "counts": counts,
        "displayed_total": displayed_total,
        "actual_sum": actual_sum,
        "consistent": is_consistent,
        "error_message": error_message,
        "concept_mapping": {
            "labels": "Category axes and series tick marks",
            "counts": "Bar heights representing discrete quantities",
            "displayed_total": "Aggregate quantity summary metric",
        },
    }


def main() -> None:
    rows = ["A", "A", "B", "C", "C", "C"]
    full_summary = summarize_quantities(rows)
    print("Full quantities summary:")
    print("Labels:", full_summary["labels"])
    print("Counts:", full_summary["counts"])
    print("Total:", full_summary["displayed_total"])
    print("Consistent:", full_summary["consistent"])

    filtered_summary = summarize_quantities(rows, filter_categories=["A", "B"])
    print("\nFiltered A/B quantities summary:")
    print("Labels:", filtered_summary["labels"])
    print("Counts:", filtered_summary["counts"])
    print("Total:", filtered_summary["displayed_total"])
    print("Consistent:", filtered_summary["consistent"])


if __name__ == "__main__":
    main()
