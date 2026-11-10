"""
Tests for Proportion Failure Handling and Recovery (R39-T027)
"""

import unittest
from example import RobustProportionPipeline, compute_proportions


class TestProportionFailureRecovery(unittest.TestCase):
    def test_canonical_counts(self):
        """Counts A=2, B=3 give 0.4, 0.6 and total 1.0."""
        res = compute_proportions({"A": 2, "B": 3})
        self.assertEqual(res["status"], "SUCCESS")
        self.assertAlmostEqual(res["proportions"]["A"], 0.4)
        self.assertAlmostEqual(res["proportions"]["B"], 0.6)
        self.assertAlmostEqual(res["total_proportion"], 1.0)

    def test_zero_total_policy(self):
        """Zero counts produce an explicit no-data result."""
        res = compute_proportions({"A": 0, "B": 0})
        self.assertEqual(res["status"], "NO_DATA")
        self.assertEqual(res["total_count"], 0)

    def test_negative_counts_rejected(self):
        """Negative counts are rejected with ValueError."""
        with self.assertRaises(ValueError):
            compute_proportions({"A": -1, "B": 2})

    def test_fault_tolerance_and_recovery(self):
        """Exercise invalid case, explain the error, and demonstrate recovery on next valid input."""
        pipeline = RobustProportionPipeline()
        stream = [
            {"A": -5, "B": 10},  # Case 1: Invalid negative count
            {"A": 2, "B": 3},    # Case 2: Valid input (demonstrates recovery)
        ]

        results = pipeline.process_stream(stream)

        # Verify first record resulted in handled error
        self.assertEqual(results[0]["status"], "RECOVERED_ERROR")
        self.assertEqual(len(pipeline.error_log), 1)
        self.assertIn("negative count", pipeline.error_log[0]["error_message"])

        # Verify second record cleanly succeeded with correct proportions
        self.assertEqual(results[1]["status"], "SUCCESS")
        self.assertAlmostEqual(results[1]["proportions"]["A"], 0.4)
        self.assertAlmostEqual(results[1]["proportions"]["B"], 0.6)

    def test_deliberate_wrong_result_fails(self):
        """Deliberately assert that negative count is NOT silently accepted."""
        pipeline = RobustProportionPipeline()
        res = pipeline.process_stream([{"A": -10, "B": 20}])[0]
        self.assertNotEqual(res["status"], "SUCCESS", "Negative counts must never produce a SUCCESS status.")


if __name__ == "__main__":
    unittest.main()
