"""Chart data consistency with scenario assessment questions.
Task R39-T059.
"""

from typing import List, Dict, Any, Optional, Sequence


def build_category_summary(
    rows: Sequence[str],
    filter_categories: Optional[Sequence[str]] = None,
    displayed_total_override: Optional[int] = None,
) -> Dict[str, Any]:
    """Calculate category counts and verify consistency with the displayed total."""
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
            f"Total mismatch: sum of counts ({actual_sum}) != displayed total ({displayed_total})"
        )

    return {
        "labels": labels,
        "counts": counts,
        "displayed_total": displayed_total,
        "actual_sum": actual_sum,
        "consistent": is_consistent,
        "error_message": error_message,
    }


ASSESSMENT_QUESTIONS: Dict[str, Dict[str, Any]] = {
    "q1_predict_output": {
        "question": "What is the total count when rows A,A,B,C,C,C are filtered to categories A and B?",
        "predicted_total": 3,
        "rationale": "Category A has 2 items and category B has 1 item, making the sum 3.",
    },
    "q2_diagnose_failure": {
        "question": "Why does a chart showing counts [2, 1] with displayed total 6 fail validation?",
        "diagnosed_cause": "stale_unfiltered_total_mismatch",
        "rationale": "The displayed total 6 is left over from the unfiltered dataset instead of matching the filtered sum 3.",
    },
    "q3_boundary_policy": {
        "question": "What policy should be adopted when a displayed total does not match the sum of slice counts?",
        "policy_choice": "flag_as_inconsistent",
        "rationale": "Charts must never present misleading totals that contradict the underlying category components.",
    },
}


def check_q1_predict_output() -> bool:
    """Executable check for Question 1: predict filtered total."""
    rows = ["A", "A", "B", "C", "C", "C"]
    summary = build_category_summary(rows, filter_categories=["A", "B"])
    expected = ASSESSMENT_QUESTIONS["q1_predict_output"]["predicted_total"]
    return summary["displayed_total"] == expected and summary["consistent"]


def check_q2_diagnose_failure() -> bool:
    """Executable check for Question 2: diagnose stale total mismatch."""
    rows = ["A", "A", "B", "C", "C", "C"]
    summary = build_category_summary(
        rows, filter_categories=["A", "B"], displayed_total_override=6
    )
    return not summary["consistent"] and summary["actual_sum"] == 3


def check_q3_boundary_policy() -> bool:
    """Executable check for Question 3: policy flags mismatch."""
    rows = ["A", "A", "B", "C", "C", "C"]
    summary = build_category_summary(rows, displayed_total_override=99)
    return not summary["consistent"] and summary["error_message"] is not None


def main() -> None:
    rows = ["A", "A", "B", "C", "C", "C"]
    full = build_category_summary(rows)
    print("Full summary (total 6):", full["counts"], "total:", full["displayed_total"])

    filtered = build_category_summary(rows, filter_categories=["A", "B"])
    print("Filtered summary (total 3):", filtered["counts"], "total:", filtered["displayed_total"])

    print("\nApplied questions executable checks:")
    print("Q1 (predict output):", check_q1_predict_output())
    print("Q2 (diagnose failure):", check_q2_diagnose_failure())
    print("Q3 (boundary policy):", check_q3_boundary_policy())


if __name__ == "__main__":
    main()
