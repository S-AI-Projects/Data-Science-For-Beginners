"""Chart-data consistency verifier and worked example (R39-T007).

Extends 3-Data-Visualization/13-meaningful-visualizations by demonstrating
how deceptive charting occurs when labels, category counts, and displayed totals
become desynchronized after filtering, and provides a deterministic consistency validator.

NOTE ON SCOPE & LIMITATIONS [SIMULATION/MOCK]:
- This module is an educational in-memory standard-library validator.
- No GUI/browser rendering, visualization engine, cloud BI tool, or trained model is claimed.
- Focuses on tabular/chart aggregate integrity before visual encoding.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple


@dataclass(frozen=True)
class ChartDataSummary:
    """Represents a category breakdown prepared for chart rendering.

    Attributes:
        labels: Tuple of category labels in display order.
        counts: Tuple of frequency counts aligned index-for-index with labels.
        displayed_total: The total count displayed on the chart legend/title.
        filter_applied: Optional tuple of allowed categories if filtered.
    """

    labels: Tuple[str, ...]
    counts: Tuple[int, ...]
    displayed_total: int
    filter_applied: Optional[Tuple[str, ...]] = None

    def as_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary representation."""
        return {
            "labels": list(self.labels),
            "counts": list(self.counts),
            "displayed_total": self.displayed_total,
            "filter_applied": list(self.filter_applied) if self.filter_applied else None,
        }


def build_category_summary(
    rows: Sequence[str],
    allowed_categories: Optional[Set[str]] = None,
) -> ChartDataSummary:
    """Aggregate raw category rows into an aligned chart summary.

    Args:
        rows: Sequence of category values (e.g. ['A', 'A', 'B', 'C', ...]).
        allowed_categories: Optional set of categories to filter against.

    Returns:
        ChartDataSummary with sorted labels, matching counts, and computed total.
    """
    if allowed_categories is not None:
        filtered_rows = [r for r in rows if r in allowed_categories]
        filter_tuple: Optional[Tuple[str, ...]] = tuple(sorted(allowed_categories))
    else:
        filtered_rows = list(rows)
        filter_tuple = None

    counts_map = Counter(filtered_rows)
    sorted_labels = sorted(counts_map.keys())
    counts_tuple = tuple(counts_map[label] for label in sorted_labels)
    total = sum(counts_tuple)

    return ChartDataSummary(
        labels=tuple(sorted_labels),
        counts=counts_tuple,
        displayed_total=total,
        filter_applied=filter_tuple,
    )


def verify_chart_data_consistency(
    summary: ChartDataSummary,
    strict: bool = False,
) -> Tuple[bool, List[str]]:
    """Validate that labels, counts, and displayed_total form an internally consistent chart.

    Checks:
        1. Alignment: len(labels) == len(counts)
        2. Non-negative: all count values >= 0
        3. Sum integrity: sum(counts) == displayed_total

    Args:
        summary: ChartDataSummary instance to validate.
        strict: If True, raises ValueError on inconsistency instead of returning False.

    Returns:
        Tuple of (consistent: bool, error_messages: List[str]).

    Raises:
        ValueError: If strict=True and inconsistency is found.
    """
    errors: List[str] = []

    if len(summary.labels) != len(summary.counts):
        errors.append(
            f"Label-count misalignment: {len(summary.labels)} labels != {len(summary.counts)} counts"
        )

    for label, count in zip(summary.labels, summary.counts):
        if count < 0:
            errors.append(f"Negative count detected for category '{label}': {count}")

    computed_sum = sum(summary.counts)
    if computed_sum != summary.displayed_total:
        errors.append(
            f"Sum mismatch: sum of counts ({computed_sum}) != displayed_total ({summary.displayed_total})"
        )

    is_consistent = len(errors) == 0

    if not is_consistent and strict:
        raise ValueError("; ".join(errors))

    return is_consistent, errors


# ==============================================================================
# Worked Example: Input-to-Output Trace
# ==============================================================================

WORKED_RAW_INPUT: Tuple[str, ...] = ("A", "A", "B", "C", "C", "C")


def build_worked_example_trace() -> List[Dict[str, Any]]:
    """Generate step-by-step worked trace showing category aggregation and filtering.

    Trace sequence:
        Step 1: Raw inputs -> ('A', 'A', 'B', 'C', 'C', 'C')
        Step 2: Full aggregation -> A=2, B=1, C=3, total=6 (consistent)
        Step 3: Filtered subset A/B -> A=2, B=1, total=3 (recomputed, consistent)
        Step 4: Deceptive stale total -> A=2, B=1, displayed_total=6 (inconsistent)

    Returns:
        List of trace dictionaries describing each transformation step.
    """
    trace: List[Dict[str, Any]] = []

    # Step 1: Raw rows input
    trace.append({
        "step": 1,
        "name": "raw_input",
        "description": "Raw observational categorical stream",
        "raw_data": list(WORKED_RAW_INPUT),
        "count_raw_records": len(WORKED_RAW_INPUT),
    })

    # Step 2: Unfiltered aggregation
    full_summary = build_category_summary(WORKED_RAW_INPUT)
    consistent_full, errors_full = verify_chart_data_consistency(full_summary)
    breakdown_full = dict(zip(full_summary.labels, full_summary.counts))
    formatted_full = ",".join(f"{k}={v}" for k, v in sorted(breakdown_full.items())) + f",total={full_summary.displayed_total}"

    trace.append({
        "step": 2,
        "name": "full_unfiltered_aggregation",
        "description": "Grouped counts across all observed categories",
        "summary": full_summary.as_dict(),
        "breakdown_string": formatted_full,
        "consistent": consistent_full,
        "errors": errors_full,
    })

    # Step 3: Filtered subset (A/B only) with recomputed total
    allowed = {"A", "B"}
    filtered_summary = build_category_summary(WORKED_RAW_INPUT, allowed_categories=allowed)
    consistent_filtered, errors_filtered = verify_chart_data_consistency(filtered_summary)
    breakdown_filtered = dict(zip(filtered_summary.labels, filtered_summary.counts))
    formatted_filtered = ",".join(f"{k}={v}" for k, v in sorted(breakdown_filtered.items())) + f",total={filtered_summary.displayed_total}"

    trace.append({
        "step": 3,
        "name": "filtered_subset_recomputed",
        "description": "Filtered to A/B with dynamically recomputed total",
        "summary": filtered_summary.as_dict(),
        "breakdown_string": formatted_filtered,
        "consistent": consistent_filtered,
        "errors": errors_filtered,
    })

    # Step 4: Deceptive mismatch scenario (stale total preserved from unfiltered dataset)
    stale_summary = ChartDataSummary(
        labels=filtered_summary.labels,
        counts=filtered_summary.counts,
        displayed_total=full_summary.displayed_total,  # Stale total 6 instead of 3
        filter_applied=filtered_summary.filter_applied,
    )
    consistent_stale, errors_stale = verify_chart_data_consistency(stale_summary)

    trace.append({
        "step": 4,
        "name": "deceptive_stale_total",
        "description": "Filtered chart displaying stale unfiltered total (deceptive pattern)",
        "summary": stale_summary.as_dict(),
        "consistent": consistent_stale,
        "errors": errors_stale,
    })

    return trace


def run_regression_check() -> bool:
    """Execute worked example as a deterministic regression test.

    Returns:
        True if all worked example invariants hold.
    """
    trace = build_worked_example_trace()

    # Invariant 1: Step 2 must match A=2,B=1,C=3,total=6
    step2 = trace[1]
    if step2["breakdown_string"] != "A=2,B=1,C=3,total=6" or not step2["consistent"]:
        return False

    # Invariant 2: Step 3 must match A=2,B=1,total=3
    step3 = trace[2]
    if step3["breakdown_string"] != "A=2,B=1,total=3" or not step3["consistent"]:
        return False

    # Invariant 3: Step 4 stale total must fail consistency check
    step4 = trace[3]
    if step4["consistent"]:
        return False

    return True


def print_suite_report() -> None:
    """Print deterministic formatted report for CLI execution."""
    print("======================================================================")
    print("[SIMULATION/MOCK] Chart-Data Consistency & Worked Example (R39-T007)")
    print("Lesson Reference: 3-Data-Visualization/13-meaningful-visualizations")
    print("Scope: Local standard-library chart consistency validator")
    print("No GUI/rendering hardware, cloud BI service, or ML models claimed.")
    print("======================================================================")
    print()

    print("--- WORKED INPUT-TO-OUTPUT TRACE ---")
    trace = build_worked_example_trace()
    for item in trace:
        step_num = item["step"]
        name = item["name"]
        desc = item["description"]
        consistent = item.get("consistent", "N/A")
        print(f"Step {step_num} [{name}]: {desc}")
        if "breakdown_string" in item:
            print(f"  Summary: {item['breakdown_string']}")
        if "errors" in item and item["errors"]:
            print(f"  Consistency Errors: {item['errors']}")
        print(f"  Consistent: {consistent}")
        print()

    # Exact regression token outputs
    full_str = trace[1]["breakdown_string"]  # A=2,B=1,C=3,total=6
    filtered_total = trace[2]["summary"]["displayed_total"]  # 3

    print("--- REGRESSION VERIFICATION SUMMARY ---")
    print(f"Unfiltered breakdown: {full_str}")
    print(f"Filtered A/B: total={filtered_total}")

    regression_ok = run_regression_check()
    print(f"Regression check passed: {regression_ok}")
    print()

    print("--- STATUS OF EVALUATED SCENARIOS ---")
    print("[SIMULATION/MOCK] Scenario 1 (Normal / Full Fixture): consistent=True (A=2,B=1,C=3,total=6)")
    print(f"[SIMULATION/MOCK] Scenario 2 (Boundary / Filtered A/B): consistent=True (A=2,B=1,total={filtered_total})")
    print("[SIMULATION/MOCK] Scenario 3 (Failure / Stale Total Mismatch): consistent=False (sum=3 != total=6)")
    print()
    print("======================================================================")
    print("[SIMULATION/MOCK] Verification complete.")
    print("======================================================================")


if __name__ == "__main__":
    print_suite_report()
