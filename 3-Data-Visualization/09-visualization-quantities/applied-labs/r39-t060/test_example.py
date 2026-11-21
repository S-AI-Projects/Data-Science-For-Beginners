"""Unit tests for Task R39-T060."""

import unittest
from example import summarize_quantities


class TestVisualizingQuantitiesConsistency(unittest.TestCase):
    def test_full_categories_summary(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = summarize_quantities(rows)
        self.assertEqual(res["labels"], ["A", "B", "C"])
        self.assertEqual(res["counts"], [2, 1, 3])
        self.assertEqual(res["displayed_total"], 6)
        self.assertTrue(res["consistent"])

    def test_filtered_subset_total_is_three(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = summarize_quantities(rows, filter_categories=["A", "B"])
        self.assertEqual(res["labels"], ["A", "B"])
        self.assertEqual(res["counts"], [2, 1])
        self.assertEqual(res["displayed_total"], 3)
        self.assertTrue(res["consistent"])

    def test_mismatched_total_fails_consistency(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = summarize_quantities(
            rows, filter_categories=["A", "B"], displayed_total_override=6
        )
        self.assertFalse(res["consistent"])
        self.assertIn("Quantity mismatch", res["error_message"])

    def test_lesson_concept_mapping_present(self):
        rows = ["A", "B"]
        res = summarize_quantities(rows)
        self.assertIn("labels", res["concept_mapping"])
        self.assertIn("counts", res["concept_mapping"])
        self.assertIn("displayed_total", res["concept_mapping"])

    def test_deliberate_wrong_result_fails(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        res = summarize_quantities(rows)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["displayed_total"], 999)


if __name__ == "__main__":
    unittest.main()
