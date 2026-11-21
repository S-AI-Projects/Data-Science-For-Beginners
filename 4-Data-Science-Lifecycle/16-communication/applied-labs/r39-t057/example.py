"""Chart data consistency worked example and regression check.
Task R39-T057.
"""

from typing import List, Dict, Any, Optional, Sequence


def build_category_summary(
    rows: Sequence[str],
    filter_categories: Optional[Sequence[str]] = None,
    displayed_total_override: Optional[int] = None,
) -> Dict[str, Any]:
    """Summarize category counts and verify that labels, counts, and total agree."""
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
            f"Total mismatch: sum of counts ({actual_sum}) does not match displayed total ({displayed_total})"
        )

    return {
        "labels": labels,
        "counts": counts,
        "displayed_total": displayed_total,
        "actual_sum": actual_sum,
        "consistent": is_consistent,
        "error_message": error_message,
    }


def run_worked_example_regression() -> Dict[str, Any]:
    """Execute the worked step by step trace from the assignment."""
    raw_data = ["A", "A", "B", "C", "C", "C"]

    # Step 1: Unfiltered category summary
    unfiltered = build_category_summary(raw_data)

    # Step 2: Filtered subset restricted to A and B
    filtered = build_category_summary(raw_data, filter_categories=["A", "B"])

    # Step 3: Deceptive chart simulation where filtered counts show stale total 6
    stale_view = build_category_summary(
        raw_data, filter_categories=["A", "B"], displayed_total_override=6
    )

    return {
        "unfiltered": unfiltered,
        "filtered": filtered,
        "stale_view": stale_view,
    }


def main() -> None:
    res = run_worked_example_regression()
    print("Unfiltered summary:", res["unfiltered"])
    print("Filtered A/B summary:", res["filtered"])
    print("Stale view consistent:", res["stale_view"]["consistent"])


if __name__ == "__main__":
    main()
