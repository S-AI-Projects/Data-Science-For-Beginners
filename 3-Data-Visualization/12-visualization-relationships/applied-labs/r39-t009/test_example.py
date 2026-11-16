"""Unit and evaluation experiment verification suite for R39-T009 chart consistency."""

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
    FIXTURE_6,
    ChartDataSummary,
    build_category_summary,
    run_evaluation_experiment,
    verify_chart_data_consistency,
)


class TestChartDataConsistencyExperiment(unittest.TestCase):
    """Test suite verifying category aggregation, 3-config experiment, and failure modes."""

    def test_01_normal_fixture_unfiltered_breakdown(self) -> None:
        """Test 1: Normal fixture ['A', 'A', 'B', 'C', 'C', 'C'] yields A=2, B=1, C=3, total=6."""
        summary = build_category_summary(FIXTURE_6)

        self.assertEqual(summary.labels, ("A", "B", "C"))
        self.assertEqual(summary.counts, (2, 1, 3))
        self.assertEqual(summary.displayed_total, 6)

        counts_dict = dict(zip(summary.labels, summary.counts))
        self.assertEqual(counts_dict, {"A": 2, "B": 1, "C": 3})

        is_consistent, errors = verify_chart_data_consistency(summary)
        self.assertTrue(is_consistent)
        self.assertEqual(errors, [])

    def test_02_boundary_filtered_ab_subset(self) -> None:
        """Test 2: Boundary filtered subset {'A', 'B'} yields A=2, B=1, total=3."""
        summary = build_category_summary(FIXTURE_6, allowed_categories={"A", "B"})

        self.assertEqual(summary.labels, ("A", "B"))
        self.assertEqual(summary.counts, (2, 1))
        self.assertEqual(summary.displayed_total, 3)

        counts_dict = dict(zip(summary.labels, summary.counts))
        self.assertEqual(counts_dict, {"A": 2, "B": 1})

        is_consistent, errors = verify_chart_data_consistency(summary)
        self.assertTrue(is_consistent)
        self.assertEqual(errors, [])

    def test_03_evaluation_experiment_three_configurations(self) -> None:
        """Test 3: run_evaluation_experiment() compares three configurations and checks metrics/trade-offs."""
        results = run_evaluation_experiment()

        self.assertEqual(len(results), 3)

        # Config 1: Baseline Small (N=6)
        c1 = results[0]
        self.assertEqual(c1["input_size"], 6)
        self.assertTrue(c1["consistency_correctness"])
        self.assertEqual(c1["discrepancy"], 0)
        self.assertEqual(c1["rows_scanned"], 6)
        self.assertEqual(c1["validation_operations"], 3)
        self.assertIn("A=2,B=1,C=3,total=6", c1["unfiltered_breakdown"])

        # Config 2: Medium Scaled (N=60)
        c2 = results[1]
        self.assertEqual(c2["input_size"], 60)
        self.assertTrue(c2["consistency_correctness"])
        self.assertEqual(c2["discrepancy"], 0)
        self.assertEqual(c2["rows_scanned"], 60)
        self.assertEqual(c2["validation_operations"], 3)

        # Config 3: Cached/Stale-Total Fast-Path (N=6)
        c3 = results[2]
        self.assertEqual(c3["input_size"], 6)
        self.assertFalse(c3["consistency_correctness"])  # Intentionally fails consistency check
        self.assertEqual(c3["discrepancy"], 3)  # 6 - 3 = 3
        self.assertIn("proves recomputing totals is mandatory", c3["trade_off_notes"])

    def test_04_deliberate_wrong_result_failure(self) -> None:
        """Test 4: Stale total or mismatched arrays causes consistency verification failure."""
        # Stale unfiltered total (6) with filtered counts (2+1 = 3)
        stale_summary = ChartDataSummary(
            labels=("A", "B"),
            counts=(2, 1),
            displayed_total=6,
        )
        is_consistent, errors = verify_chart_data_consistency(stale_summary)
        self.assertFalse(is_consistent)
        self.assertIn("Sum mismatch", errors[0])

        with self.assertRaises(ValueError):
            verify_chart_data_consistency(stale_summary, strict=True)

        # Mismatched labels and counts length
        mismatched_summary = ChartDataSummary(
            labels=("A", "B", "C"),
            counts=(2, 1),
            displayed_total=3,
        )
        is_mismatched, err_mismatched = verify_chart_data_consistency(mismatched_summary)
        self.assertFalse(is_mismatched)
        self.assertIn("Label-count misalignment", err_mismatched[0])

    def test_05_fresh_process_cli_execution(self) -> None:
        """Test 5: Fresh-process CLI execution exits with returncode == 0 and expected tokens."""
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
        self.assertIn("THREE-CONFIGURATION EVALUATION EXPERIMENT", proc.stdout)
        self.assertIn("OBSERVED EXPERIMENTAL TRADE-OFF", proc.stdout)


if __name__ == "__main__":
    unittest.main()
