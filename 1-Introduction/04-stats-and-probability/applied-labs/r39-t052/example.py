"""Histogram boundary accounting with failure and recovery example.
Task R39-T052.
"""

from typing import List, Dict, Any, Sequence, Optional


def count_histogram_bins(
    values: Sequence[Optional[float]], bins: Sequence[float]
) -> Dict[str, Any]:
    """Count values into bins where bins are [start, end).

    The final bin is right inclusive [start, end].
    Values outside the bin range are saved separately.
    Raises ValueError on missing data or invalid bin edges.
    """
    if len(bins) < 2:
        raise ValueError("Bins list must have at least two edges")

    for i in range(len(bins) - 1):
        if bins[i] >= bins[i + 1]:
            raise ValueError("Bins must be in strictly increasing order")

    for val in values:
        if val is None:
            raise ValueError("Missing data found in input values list")

    num_bins = len(bins) - 1
    counts = [0] * num_bins
    below_range: List[float] = []
    above_range: List[float] = []

    for val in values:
        if val < bins[0]:
            below_range.append(val)
        elif val > bins[-1]:
            above_range.append(val)
        else:
            placed = False
            for i in range(num_bins):
                is_last_bin = i == num_bins - 1
                if is_last_bin:
                    if bins[i] <= val <= bins[i + 1]:
                        counts[i] += 1
                        placed = True
                        break
                else:
                    if bins[i] <= val < bins[i + 1]:
                        counts[i] += 1
                        placed = True
                        break
            if not placed:
                above_range.append(val)

    return {
        "bins": list(bins),
        "counts": counts,
        "below_range": below_range,
        "above_range": above_range,
        "total_in_range": sum(counts),
    }


def run_failure_and_recovery_demonstration() -> Dict[str, Any]:
    """Demonstrates handling missing data and recovering on valid input."""
    bins = [0, 10, 20]
    bad_values = [0, 9, None, 20]
    good_values = [0, 9, 10, 20]

    failure_message = ""
    try:
        count_histogram_bins(bad_values, bins)
    except ValueError as err:
        failure_message = str(err)

    recovery_result = count_histogram_bins(good_values, bins)

    return {
        "failure_detected": failure_message != "",
        "error_message": failure_message,
        "recovery_counts": recovery_result["counts"],
        "recovery_total": recovery_result["total_in_range"],
    }


def main() -> None:
    bins = [0, 10, 20]
    values = [0, 9, 10, 20]
    result = count_histogram_bins(values, bins)
    print("Normal run counts:", result["counts"])

    demo = run_failure_and_recovery_demonstration()
    print("Failure handled:", demo["failure_detected"])
    print("Error message:", demo["error_message"])
    print("Recovery counts on valid input:", demo["recovery_counts"])


if __name__ == "__main__":
    main()
