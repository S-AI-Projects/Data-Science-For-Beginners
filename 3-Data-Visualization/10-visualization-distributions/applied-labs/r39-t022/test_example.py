"""
Tests for Histogram Boundary Accounting (R39-T022)
"""

import unittest
from example import compute_histogram_counts


class TestHistogramBoundaryAccounting(unittest.TestCase):
    def test_canonical_fixture(self):
        """Bins [0,10,20] with [0,9,10,20] must yield counts [2,2] and empty out_of_bounds."""
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        counts, oob = compute_histogram_counts(values, bins)
        self.assertEqual(counts, [2, 2])
        self.assertEqual(oob, [])

    def test_boundary_points(self):
        """Verify boundary placement: left edge, interior boundary, and terminal right edge."""
        bins = [0, 10, 20]
        # Interior boundary 10 must belong to bin 1 [10, 20], not bin 0 [0, 10)
        counts_10, _ = compute_histogram_counts([10], bins)
        self.assertEqual(counts_10, [0, 1])

        # Terminal boundary 20 must be included in the right-inclusive final bin
        counts_20, _ = compute_histogram_counts([20], bins)
        self.assertEqual(counts_20, [0, 1])

        # Minimum boundary 0 must belong to bin 0 [0, 10)
        counts_0, _ = compute_histogram_counts([0], bins)
        self.assertEqual(counts_0, [1, 0])

    def test_out_of_bounds(self):
        """Values strictly outside the bin range must be reported separately."""
        bins = [0, 10, 20]
        values = [-5, -0.01, 20.01, 100]
        counts, oob = compute_histogram_counts(values, bins)
        self.assertEqual(counts, [0, 0])
        self.assertEqual(oob, [-5, -0.01, 20.01, 100])

    def test_smallest_valid_case(self):
        """Smallest valid fixture: 2 edges (1 bin) and 1 value."""
        bins = [0, 10]
        values = [5]
        counts, oob = compute_histogram_counts(values, bins)
        self.assertEqual(counts, [1])
        self.assertEqual(oob, [])

    def test_invalid_bin_edges(self):
        """Ensure invalid bin configurations raise ValueError."""
        with self.assertRaises(ValueError):
            compute_histogram_counts([1, 2], [10])  # fewer than 2 edges
        with self.assertRaises(ValueError):
            compute_histogram_counts([1, 2], [10, 5])  # decreasing edges
        with self.assertRaises(ValueError):
            compute_histogram_counts([1, 2], [5, 5])  # equal edges

    def test_deliberate_wrong_result_fails(self):
        """A deliberate wrong result (placing 10 in bin 0 giving [3, 1]) must fail assertion."""
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        counts, _ = compute_histogram_counts(values, bins)
        self.assertNotEqual(counts, [3, 1], "Boundary value 10 must not be counted in the first bin.")


if __name__ == "__main__":
    unittest.main()
