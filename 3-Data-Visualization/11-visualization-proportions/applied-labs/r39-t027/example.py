"""
Proportion Pipeline with Failure Handling & Recovery (R39-T027)

Extends lesson 11 (Visualizing Proportions) by introducing robust error handling
and pipeline fault tolerance:
- Rejects negative counts with documented ValueError.
- Handles zero total counts gracefully via explicit NO_DATA response.
- Demonstrates immediate pipeline recovery on subsequent valid inputs following an invalid input.
"""

from typing import Any, Dict, List, Tuple


def compute_proportions(counts: Dict[str, int]) -> Dict[str, Any]:
    """
    Normalizes category counts into proportions with explicit validation.
    Raises ValueError for negative counts.
    Returns NO_DATA status for zero totals.
    """
    for k, v in counts.items():
        if v < 0:
            raise ValueError(f"Invalid count: category '{k}' has negative count {v}.")

    total = sum(counts.values())
    if total == 0:
        return {
            "status": "NO_DATA",
            "proportions": {k: 0.0 for k in counts},
            "total_count": 0,
            "total_proportion": 0.0
        }

    proportions = {k: v / total for k, v in counts.items()}
    return {
        "status": "SUCCESS",
        "proportions": proportions,
        "total_count": total,
        "total_proportion": sum(proportions.values())
    }


class RobustProportionPipeline:
    """
    Batch processor that handles malformed inputs, records error diagnostics,
    and cleanly recovers to process subsequent valid inputs without failure cascade.
    """

    def __init__(self):
        self.error_log: List[Dict[str, Any]] = []

    def process_stream(self, records: List[Dict[str, int]]) -> List[Dict[str, Any]]:
        results = []
        for idx, rec in enumerate(records):
            try:
                res = compute_proportions(rec)
                results.append(res)
            except ValueError as err:
                error_record = {
                    "status": "RECOVERED_ERROR",
                    "record_index": idx,
                    "error_message": str(err),
                    "action": "quarantined_record"
                }
                self.error_log.append(error_record)
                results.append(error_record)
        return results


if __name__ == "__main__":
    pipeline = RobustProportionPipeline()
    batch = [
        {"A": -2, "B": 3},  # Invalid input
        {"A": 2, "B": 3},   # Valid input (recovery)
        {"A": 0, "B": 0}    # Zero count
    ]
    results = pipeline.process_stream(batch)
    for r in results:
        print(r)
