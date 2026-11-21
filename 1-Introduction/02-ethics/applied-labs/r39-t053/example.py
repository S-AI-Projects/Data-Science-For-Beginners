"""Group metric comparison lab for ethics lesson.
Task R39-T053.
"""

from typing import List, Dict, Any, Optional, Sequence


def calculate_group_metric(outcomes: Sequence[int]) -> Dict[str, Any]:
    """Calculate the outcome rate and sample count for a group.

    An empty group has an undefined rate represented by None.
    """
    n = len(outcomes)
    if n == 0:
        return {
            "n": 0,
            "rate": None,
            "defined": False,
        }

    positive_count = sum(outcomes)
    rate = positive_count / n
    return {
        "n": n,
        "rate": rate,
        "defined": True,
    }


def compare_two_groups(
    group_a: Sequence[int], group_b: Sequence[int]
) -> Dict[str, Any]:
    """Compare rates and counts between two groups without inferring causation."""
    metric_a = calculate_group_metric(group_a)
    metric_b = calculate_group_metric(group_b)

    return {
        "group_a": metric_a,
        "group_b": metric_b,
        "causation_inferred": False,
        "note": "Equal rates with different sample sizes require careful interpretation",
    }


def reference_metric_calculation(outcomes: Sequence[int]) -> Dict[str, Any]:
    """Independent simple calculation used to cross check results."""
    count = 0
    total = 0
    for val in outcomes:
        count += 1
        total += val
    if count == 0:
        return {"n": 0, "rate": None, "defined": False}
    return {"n": count, "rate": total / count, "defined": True}


def verify_both_approaches(outcomes: Sequence[int]) -> bool:
    """Check that direct implementation matches the reference calculation."""
    res1 = calculate_group_metric(outcomes)
    res2 = reference_metric_calculation(outcomes)
    return res1["n"] == res2["n"] and res1["rate"] == res2["rate"]


def main() -> None:
    group_a = [1, 0]
    group_b = [1, 1, 0, 0]

    comparison = compare_two_groups(group_a, group_b)
    print("Group A:", comparison["group_a"])
    print("Group B:", comparison["group_b"])
    print("Empty group:", calculate_group_metric([]))
    print("Approaches match on A:", verify_both_approaches(group_a))
    print("Approaches match on B:", verify_both_approaches(group_b))


if __name__ == "__main__":
    main()
