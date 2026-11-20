"""Unit tests for R39-T041 histogram boundary accounting."""

import unittest
from example import count_histogram_bins


class TestHistogramBoundaryAccounting(unittest.TestCase):
    def test_stated_contract_bins_and_values(self) -> None:
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        result = count_histogram_bins(values, bins)
        self.assertEqual(result["counts"], [2, 2])
        self.assertEqual(result["below_range"], [])
        self.assertEqual(result["above_range"], [])
        self.assertEqual(result["total_in_range"], 4)
        self.assertEqual(result["total_out_of_range"], 0)

    def test_values_outside_range_reported_separately(self) -> None:
        bins = [0, 10, 20]
        values = [-5, 0, 9, 10, 20, 25]
        result = count_histogram_bins(values, bins)
        self.assertEqual(result["counts"], [2, 2])
        self.assertEqual(result["below_range"], [-5])
        self.assertEqual(result["above_range"], [25])
        self.assertEqual(result["total_out_of_range"], 2)

    def test_single_bin_is_right_inclusive(self) -> None:
        bins = [0, 10]
        values = [0, 5, 10]
        result = count_histogram_bins(values, bins)
        self.assertEqual(result["counts"], [3])
        self.assertEqual(result["total_in_range"], 3)

    def test_empty_values_list(self) -> None:
        bins = [0, 10, 20]
        result = count_histogram_bins([], bins)
        self.assertEqual(result["counts"], [0, 0])
        self.assertEqual(result["total_in_range"], 0)

    def test_invalid_bins_raise_value_error(self) -> None:
        with self.assertRaises(ValueError):
            count_histogram_bins([1, 2], [10])
        with self.assertRaises(ValueError):
            count_histogram_bins([1, 2], [20, 10])

    def test_deliberate_wrong_result_fails(self) -> None:
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        result = count_histogram_bins(values, bins)
        with self.assertRaises(AssertionError):
            self.assertEqual(result["counts"], [3, 1])


if __name__ == "__main__":
    unittest.main()
