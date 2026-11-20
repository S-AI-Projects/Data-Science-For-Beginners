"""Unit tests for R39-T046 chart-data consistency and refactoring equivalence."""

import unittest
from example import (
    CategoryAggregator,
    summarize_categories_baseline,
    summarize_categories_refactored,
    verify_equivalence,
)


class TestChartDataConsistency(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = ["A", "A", "B", "C", "C", "C"]

    def test_stated_contract_unfiltered(self) -> None:
        # Rows A,A,B,C,C,C yield A=2,B=1,C=3,total=6
        res = summarize_categories_refactored(self.rows)
        self.assertEqual(res["counts"], {"A": 2, "B": 1, "C": 3})
        self.assertEqual(res["total"], 6)
        self.assertEqual(res["labels"], ["A", "B", "C"])

    def test_stated_contract_filtered_ab(self) -> None:
        # Filtering to A/B gives total 3
        res = summarize_categories_refactored(self.rows, filter_categories={"A", "B"})
        self.assertEqual(res["counts"], {"A": 2, "B": 1})
        self.assertEqual(res["total"], 3)
        self.assertEqual(res["labels"], ["A", "B"])

    def test_refactoring_equivalence(self) -> None:
        self.assertTrue(verify_equivalence(self.rows))
        self.assertTrue(verify_equivalence(self.rows, {"A", "B"}))
        self.assertTrue(verify_equivalence(self.rows, {"C"}))
        self.assertTrue(verify_equivalence([], None))

    def test_extracted_aggregator_responsibility(self) -> None:
        tally = CategoryAggregator.aggregate(["X", "Y", "X"])
        self.assertEqual(tally, {"X": 2, "Y": 1})

    def test_deliberate_inconsistency_fails(self) -> None:
        res = summarize_categories_refactored(self.rows)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["total"], 10)


if __name__ == "__main__":
    unittest.main()
