"""
Tests for Chart-Data Consistency (R39-T023)
"""

import unittest
from example import summarize_categories_procedural, summarize_categories_counter


class TestChartDataConsistency(unittest.TestCase):
    def setUp(self):
        self.fixture = ["A", "A", "B", "C", "C", "C"]

    def test_unfiltered_summary(self):
        """Rows A,A,B,C,C,C yield A=2, B=1, C=3, and total=6."""
        counts, total = summarize_categories_procedural(self.fixture)
        self.assertEqual(counts, {"A": 2, "B": 1, "C": 3})
        self.assertEqual(total, 6)
        self.assertEqual(sum(counts.values()), total)

    def test_filtered_summary(self):
        """Filtering to ['A', 'B'] yields A=2, B=1, and total=3."""
        counts, total = summarize_categories_procedural(self.fixture, allowed_categories=["A", "B"])
        self.assertEqual(counts, {"A": 2, "B": 1})
        self.assertEqual(total, 3)
        self.assertEqual(sum(counts.values()), total)

    def test_two_approaches_equivalence(self):
        """Verify that procedural and Counter implementations yield identical results."""
        for filter_opt in [None, ["A", "B"], ["C"], ["D"], []]:
            p_counts, p_total = summarize_categories_procedural(self.fixture, allowed_categories=filter_opt)
            c_counts, c_total = summarize_categories_counter(self.fixture, allowed_categories=filter_opt)
            self.assertEqual(p_counts, c_counts)
            self.assertEqual(p_total, c_total)

    def test_empty_input(self):
        """Empty input yields empty counts and total=0."""
        counts, total = summarize_categories_procedural([])
        self.assertEqual(counts, {})
        self.assertEqual(total, 0)

    def test_deliberate_wrong_result_fails(self):
        """A desynchronized report (e.g. filtered counts but unfiltered total=6) must fail assertion."""
        counts, total = summarize_categories_procedural(self.fixture, allowed_categories=["A", "B"])
        # Deliberately assert that total does NOT equal the unfiltered total
        self.assertNotEqual(total, 6, "Filtered total must reflect filtered rows, never unfiltered count.")


if __name__ == "__main__":
    unittest.main()
