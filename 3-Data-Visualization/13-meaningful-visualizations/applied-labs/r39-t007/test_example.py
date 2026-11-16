"""Unit and regression verification suite for R39-T007 chart-data consistency."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

# Ensure local lab directory is in sys.path for direct or discovery invocation
_LAB_DIR = os.path.dirname(os.path.abspath(__file__))
if _LAB_DIR not in sys.path:
    sys.path.insert(0, _LAB_DIR)

from example import (  # noqa: E402
    WORKED_RAW_INPUT,
    ChartDataSummary,
    build_category_summary,
    build_worked_example_trace,
    run_regression_check,
    verify_chart_data_consistency,
)


class TestChartDataConsistency(unittest.TestCase):
    """Test suite verifying chart aggregation, filtering, and consistency validation."""

    def test_01_exact_worked_example_regression(self) -> None:
        """Test 1: Rows ['A', 'A', 'B', 'C', 'C', 'C'] yield exact counts and total == 6."""
        summary = build_category_summary(WORKED_RAW_INPUT)

        self.assertEqual(summary.labels, ("A", "B", "C"))
        self.assertEqual(summary.counts, (2, 1, 3))
        self.assertEqual(summary.displayed_total, 6)

        counts_dict = dict(zip(summary.labels, summary.counts))
        self.assertEqual(counts_dict, {"A": 2, "B": 1, "C": 3})

        is_consistent, errors = verify_chart_data_consistency(summary)
        self.assertTrue(is_consistent)
        self.assertEqual(errors, [])
        self.assertTrue(run_regression_check())

    def test_02_filtered_ab_subset_boundary(self) -> None:
        """Test 2: Filtering ['A', 'A', 'B', 'C', 'C', 'C'] to {'A', 'B'} yields counts A=2, B=1 and total == 3."""
        summary = build_category_summary(WORKED_RAW_INPUT, allowed_categories={"A", "B"})

        self.assertEqual(summary.labels, ("A", "B"))
        self.assertEqual(summary.counts, (2, 1))
        self.assertEqual(summary.displayed_total, 3)

        counts_dict = dict(zip(summary.labels, summary.counts))
        self.assertEqual(counts_dict, {"A": 2, "B": 1})

        is_consistent, errors = verify_chart_data_consistency(summary)
        self.assertTrue(is_consistent)
        self.assertEqual(errors, [])

    def test_03_empty_and_single_category_boundary(self) -> None:
        """Test 3: Empty input yields total == 0 with empty labels/counts; single category yields expected single item."""
        # Empty boundary
        empty_summary = build_category_summary([])
        self.assertEqual(empty_summary.labels, ())
        self.assertEqual(empty_summary.counts, ())
        self.assertEqual(empty_summary.displayed_total, 0)
        is_consistent_empty, errors_empty = verify_chart_data_consistency(empty_summary)
        self.assertTrue(is_consistent_empty)
        self.assertEqual(errors_empty, [])

        # Single category boundary
        single_summary = build_category_summary(["Z", "Z", "Z"])
        self.assertEqual(single_summary.labels, ("Z",))
        self.assertEqual(single_summary.counts, (3,))
        self.assertEqual(single_summary.displayed_total, 3)
        is_consistent_single, errors_single = verify_chart_data_consistency(single_summary)
        self.assertTrue(is_consistent_single)
        self.assertEqual(errors_single, [])

    def test_04_deliberate_wrong_result_and_stale_total_failure(self) -> None:
        """Test 4: Stale unfiltered total (total=6) for filtered subset (sum=3) or mismatched arrays fails consistency check."""
        filtered_summary = build_category_summary(WORKED_RAW_INPUT, allowed_categories={"A", "B"})

        # Stale total failure (sum=3, but displayed_total=6)
        stale_summary = ChartDataSummary(
            labels=filtered_summary.labels,
            counts=filtered_summary.counts,
            displayed_total=6,
        )
        is_consistent, errors = verify_chart_data_consistency(stale_summary)
        self.assertFalse(is_consistent)
        self.assertIn("Sum mismatch", errors[0])

        # Strict mode raises ValueError
        with self.assertRaises(ValueError):
            verify_chart_data_consistency(stale_summary, strict=True)

        # Mismatched labels/counts length failure
        mismatched_summary = ChartDataSummary(
            labels=("A", "B", "C"),
            counts=(2, 1),
            displayed_total=3,
        )
        is_consistent_mismatch, errors_mismatch = verify_chart_data_consistency(mismatched_summary)
        self.assertFalse(is_consistent_mismatch)
        self.assertIn("Label-count misalignment", errors_mismatch[0])

    def test_05_fresh_process_cli_execution(self) -> None:
        """Test 5: Running example.py in fresh process exits with code 0 and required output tokens."""
        script_path = os.path.join(_LAB_DIR, "example.py")
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        self.assertIn("A=2,B=1,C=3,total=6", proc.stdout)
        self.assertIn("total=3", proc.stdout)
        self.assertIn("[SIMULATION/MOCK]", proc.stdout)


if __name__ == "__main__":
    unittest.main()
