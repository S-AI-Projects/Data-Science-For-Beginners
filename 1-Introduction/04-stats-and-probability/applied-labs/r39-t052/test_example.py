"""Unit tests for Task R39-T052."""

import unittest
from example import count_histogram_bins, run_failure_and_recovery_demonstration


class TestHistogramBoundaryAccounting(unittest.TestCase):
    def test_required_contract(self):
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        res = count_histogram_bins(values, bins)
        self.assertEqual(res["counts"], [2, 2])
        self.assertEqual(res["total_in_range"], 4)

    def test_values_outside_range_reported_separately(self):
        bins = [0, 10, 20]
        values = [-5, 0, 9, 10, 20, 25]
        res = count_histogram_bins(values, bins)
        self.assertEqual(res["counts"], [2, 2])
        self.assertEqual(res["below_range"], [-5])
        self.assertEqual(res["above_range"], [25])

    def test_failure_on_missing_data(self):
        bins = [0, 10, 20]
        values = [0, 9, None, 20]
        with self.assertRaises(ValueError):
            count_histogram_bins(values, bins)

    def test_recovery_after_failure(self):
        demo = run_failure_and_recovery_demonstration()
        self.assertTrue(demo["failure_detected"])
        self.assertEqual(demo["recovery_counts"], [2, 2])

    def test_deliberate_wrong_result_fails(self):
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        res = count_histogram_bins(values, bins)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["counts"], [3, 1])


if __name__ == "__main__":
    unittest.main()
