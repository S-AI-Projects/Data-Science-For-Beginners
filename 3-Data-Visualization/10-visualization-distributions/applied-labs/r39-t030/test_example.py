"""
Tests for Histogram Refactoring: Extracted Bin Index Resolution (R39-T030)
"""

import unittest
from example import (
    compute_histogram_counts,
    compute_histogram_counts_baseline,
    compute_histogram_counts_refactored,
    find_bin_index,
)


class TestHistogramRefactoring(unittest.TestCase):
    def setUp(self):
        self.bins = [0, 10, 20]
        self.values = [0, 9, 10, 20]

    def test_canonical_fixture(self):
        """Bins [0,10,20] with [0,9,10,20] yield counts [2,2] and empty out_of_bounds."""
        counts, oob = compute_histogram_counts(self.values, self.bins)
        self.assertEqual(counts, [2, 2])
        self.assertEqual(oob, [])

    def test_extracted_find_bin_index_responsibility(self):
        """Unit test the extracted single-responsibility function find_bin_index."""
        # Bin 0: [0, 10)
        self.assertEqual(find_bin_index(0, self.bins), 0)
        self.assertEqual(find_bin_index(9.999, self.bins), 0)

        # Bin 1: [10, 20] (right-inclusive)
        self.assertEqual(find_bin_index(10, self.bins), 1)
        self.assertEqual(find_bin_index(15, self.bins), 1)
        self.assertEqual(find_bin_index(20, self.bins), 1)

        # Out of bounds
        self.assertIsNone(find_bin_index(-0.01, self.bins))
        self.assertIsNone(find_bin_index(20.01, self.bins))

    def test_before_after_refactoring_equivalence(self):
        """Prove algebraic and behavioral equivalence between baseline and refactored versions."""
        test_cases = [
            ([0, 9, 10, 20], [0, 10, 20]),
            ([-5, 0, 5, 10, 15, 20, 25], [0, 10, 20]),
            ([], [0, 10, 20]),
            ([5, 5, 5], [0, 10, 20, 30]),
            ([10], [0, 10, 20]),
            ([20], [0, 10, 20]),
        ]

        for vals, b_edges in test_cases:
            b_counts, b_oob = compute_histogram_counts_baseline(vals, b_edges)
            r_counts, r_oob = compute_histogram_counts_refactored(vals, b_edges)
            self.assertEqual(b_counts, r_counts, f"Counts mismatch for {vals} with {b_edges}")
            self.assertEqual(b_oob, r_oob, f"OOB mismatch for {vals} with {b_edges}")

    def test_deliberate_wrong_result_fails(self):
        """Deliberately assert that boundary value 10 is not assigned to bin 0."""
        self.assertNotEqual(find_bin_index(10, self.bins), 0, "Boundary 10 must belong to bin 1.")


if __name__ == "__main__":
    unittest.main()
