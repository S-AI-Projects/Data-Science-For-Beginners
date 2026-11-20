"""Unit tests for R39-T045 offline histogram service adapter."""

import unittest
from example import HistogramServiceInterface, LocalOfflineHistogramAdapter


class TestHistogramOfflineAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = LocalOfflineHistogramAdapter()

    def test_implements_interface(self) -> None:
        self.assertIsInstance(self.adapter, HistogramServiceInterface)

    def test_stated_contract_counts(self) -> None:
        # Bins [0,10,20] with values [0,9,10,20] yield counts [2,2]
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        res = self.adapter.compute_histogram(values, bins)
        self.assertEqual(res["counts"], [2, 2])
        self.assertEqual(res["below_range"], [])
        self.assertEqual(res["above_range"], [])
        self.assertEqual(res["total_in_range"], 4)

    def test_out_of_range_reported_separately(self) -> None:
        bins = [0, 10, 20]
        values = [-2, 0, 9, 10, 20, 25]
        res = self.adapter.compute_histogram(values, bins)
        self.assertEqual(res["counts"], [2, 2])
        self.assertEqual(res["below_range"], [-2])
        self.assertEqual(res["above_range"], [25])
        self.assertEqual(res["total_out_of_range"], 2)

    def test_invalid_bins_raise_error(self) -> None:
        with self.assertRaises(ValueError):
            self.adapter.compute_histogram([1], [10])

    def test_deliberate_wrong_result_fails(self) -> None:
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        res = self.adapter.compute_histogram(values, bins)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["counts"], [1, 3])


if __name__ == "__main__":
    unittest.main()
