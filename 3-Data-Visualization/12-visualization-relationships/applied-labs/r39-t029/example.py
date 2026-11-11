"""
Category Summary with Applied Assessment Scenarios (R39-T029)

Extends lesson 12 (Visualizing Relationships) by ensuring categorical visualization
counts and total aggregate metrics remain perfectly synchronized.
Includes three applied questions with executable checks:
1. Predict an output under filtering
2. Diagnose a state desynchronization failure
3. Select an explicit boundary policy for missing categories
"""

from typing import Any, Dict, Iterable, Optional, Tuple


def compute_category_summary(
    rows: Iterable[str], allowed_categories: Optional[Iterable[str]] = None
) -> Tuple[Dict[str, int], int]:
    """
    Computes frequency distribution and total count synchronized to the active filter.
    Returns: (category_counts, total_count)
    """
    filter_set = set(allowed_categories) if allowed_categories is not None else None
    counts: Dict[str, int] = {}

    for item in rows:
        if filter_set is not None and item not in filter_set:
            continue
        counts[item] = counts.get(item, 0) + 1

    total = sum(counts.values())
    return counts, total


def answer_applied_question_1_predict() -> Dict[str, Any]:
    """Q1: Predict output for rows ['A', 'B', 'B', 'C'] filtered to ['B']."""
    counts, total = compute_category_summary(["A", "B", "B", "C"], allowed_categories=["B"])
    return {
        "question": "Predict output for rows ['A', 'B', 'B', 'C'] filtered to ['B']",
        "predicted_counts": counts,
        "predicted_total": total,
        "rationale": "Filtering isolates 'B', which appears twice, giving count 2 and aggregate total 2."
    }


def answer_applied_question_2_diagnose() -> Dict[str, Any]:
    """Q2: Diagnose failure where filtered counts are {'A': 2, 'B': 1} but total is 6."""
    return {
        "question": "Diagnose failure where filtered counts are {'A': 2, 'B': 1} but total is 6",
        "defect_type": "STATE_DESYNCHRONIZATION",
        "root_cause": "The summary total was calculated against the raw unfiltered dataset instead of the filtered view.",
        "fix": "Always compute total as sum of filtered category counts."
    }


def answer_applied_question_3_boundary_policy() -> Dict[str, Any]:
    """Q3: Choose boundary policy when filter categories do not match any input rows."""
    counts, total = compute_category_summary(["A", "A", "B", "C", "C", "C"], allowed_categories=["D", "E"])
    return {
        "question": "Choose boundary policy for non-matching filter categories ['D', 'E']",
        "chosen_policy": "EMPTY_DICT_ZERO_TOTAL",
        "resulting_counts": counts,
        "resulting_total": total,
        "rationale": "Empty match returns empty counts {} and total 0, maintaining sum(counts) == total invariant."
    }


if __name__ == "__main__":
    rows = ["A", "A", "B", "C", "C", "C"]
    print("Unfiltered:", compute_category_summary(rows))
    print("Filtered A/B:", compute_category_summary(rows, ["A", "B"]))
    print("Q1:", answer_applied_question_1_predict())
    print("Q2:", answer_applied_question_2_diagnose())
    print("Q3:", answer_applied_question_3_boundary_policy())
