"""
Proportion Table Validation: Worked Example (R39-T026)

Extends lesson 11 (Visualizing Proportions) by converting raw category frequency counts
into normalized proportion distributions with a documented zero-total policy:
- Rejects negative counts with ValueError.
- Handles zero total count by returning an explicit NO_DATA status.
- Converts valid counts into proportions summing to 1.0.
"""

from typing import Any, Dict


def compute_proportions(counts: Dict[str, int]) -> Dict[str, Any]:
    """
    Converts category counts into proportions with documented zero-total policy.

    Args:
        counts: Dictionary mapping category keys to non-negative integer counts.

    Returns:
        Dictionary with keys:
          - "status": "SUCCESS" or "NO_DATA"
          - "proportions": Dict mapping category to float proportion
          - "total_count": Sum of input counts
          - "total_proportion": Sum of computed proportions (1.0 on SUCCESS, 0.0 on NO_DATA)
    """
    for cat, count in counts.items():
        if count < 0:
            raise ValueError(f"Negative counts are rejected: category '{cat}' has count {count}.")

    total_count = sum(counts.values())

    # Documented zero-total policy: return explicit NO_DATA result
    if total_count == 0:
        return {
            "status": "NO_DATA",
            "proportions": {k: 0.0 for k in counts},
            "total_count": 0,
            "total_proportion": 0.0
        }

    proportions = {cat: count / total_count for cat, count in counts.items()}
    total_prop = sum(proportions.values())

    return {
        "status": "SUCCESS",
        "proportions": proportions,
        "total_count": total_count,
        "total_proportion": total_prop
    }


if __name__ == "__main__":
    canonical = {"A": 2, "B": 3}
    result = compute_proportions(canonical)
    print("Counts:", canonical)
    print("Result:", result)
