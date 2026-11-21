"""Unit tests for Task R39-T057."""

import unittest
from example import build_category_summary, run_worked_example_regression


class TestChartDataConsistency(unittest.TestCase):
    def test_unfiltered_category_counts_and_total(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = build_category_summary(rows)
        self.assertEqual(res["labels"], ["A", "B", "C"])
        self.assertEqual(res["counts"], [2, 1, 3])
        self.assertEqual(res["displayed_total"], 6)
        self.assertTrue(res["consistent"])

    def test_filtered_subset_total_is_three(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = build_category_summary(rows, filter_categories=["A", "B"])
        self.assertEqual(res["labels"], ["A", "B"])
        self.assertEqual(res["counts"], [2, 1])
        self.assertEqual(res["displayed_total"], 3)
        self.assertTrue(res["consistent"])

    def test_stale_total_fails_consistency_check(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = build_category_summary(
            rows, filter_categories=["A", "B"], displayed_total_override=6
        )
        self.assertFalse(res["consistent"])
        self.assertIn("Total mismatch", res["error_message"])

    def test_worked_example_regression(self):
        trace = run_worked_example_regression()
        self.assertEqual(trace["unfiltered"]["counts"], [2, 1, 3])
        self.assertEqual(trace["unfiltered"]["displayed_total"], 6)
        self.assertEqual(trace["filtered"]["counts"], [2, 1])
        self.assertEqual(trace["filtered"]["displayed_total"], 3)
        self.assertFalse(trace["stale_view"]["consistent"])

    def test_deliberate_wrong_result_fails(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = build_category_summary(rows)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["displayed_total"], 999)


if __name__ == "__main__":
    unittest.main()
