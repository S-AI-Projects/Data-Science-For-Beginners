"""
Tests for Proportion Table Validation (R39-T026)
"""

import unittest
from example import compute_proportions


class TestProportionTableValidation(unittest.TestCase):
    def test_canonical_counts(self):
        """Counts A=2, B=3 give proportions 0.4, 0.6 and total proportion 1.0."""
        counts = {"A": 2, "B": 3}
        res = compute_proportions(counts)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertAlmostEqual(res["proportions"]["A"], 0.4)
        self.assertAlmostEqual(res["proportions"]["B"], 0.6)
        self.assertEqual(res["total_count"], 5)
        self.assertAlmostEqual(res["total_proportion"], 1.0)

    def test_zero_total_policy(self):
        """Zero counts produce an explicit no-data result."""
        res_zeros = compute_proportions({"A": 0, "B": 0})
        self.assertEqual(res_zeros["status"], "NO_DATA")
        self.assertEqual(res_zeros["total_count"], 0)
        self.assertEqual(res_zeros["total_proportion"], 0.0)

        res_empty = compute_proportions({})
        self.assertEqual(res_empty["status"], "NO_DATA")
        self.assertEqual(res_empty["total_count"], 0)

    def test_negative_counts_rejected(self):
        """Negative counts must be rejected with ValueError."""
        with self.assertRaises(ValueError):
            compute_proportions({"A": -1, "B": 3})
        with self.assertRaises(ValueError):
            compute_proportions({"A": 2, "B": -5})

    def test_deliberate_wrong_result_fails(self):
        """Deliberately assert that total proportion of valid input is NOT 0.5."""
        counts = {"A": 2, "B": 3}
        res = compute_proportions(counts)
        self.assertNotEqual(res["total_proportion"], 0.5, "Normalized proportions must sum to 1.0, not 0.5.")


if __name__ == "__main__":
    unittest.main()
