"""
Tests for Category Summary and Applied Assessment Scenarios (R39-T029)
"""

import unittest
from example import (
    answer_applied_question_1_predict,
    answer_applied_question_2_diagnose,
    answer_applied_question_3_boundary_policy,
    compute_category_summary,
)


class TestCategorySummaryScenarios(unittest.TestCase):
    def setUp(self):
        self.fixture = ["A", "A", "B", "C", "C", "C"]

    def test_canonical_unfiltered(self):
        """Rows A,A,B,C,C,C yield A=2, B=1, C=3, and total=6."""
        counts, total = compute_category_summary(self.fixture)
        self.assertEqual(counts, {"A": 2, "B": 1, "C": 3})
        self.assertEqual(total, 6)

    def test_canonical_filtered(self):
        """Filtering to ['A', 'B'] gives counts A=2, B=1 and total=3."""
        counts, total = compute_category_summary(self.fixture, allowed_categories=["A", "B"])
        self.assertEqual(counts, {"A": 2, "B": 1})
        self.assertEqual(total, 3)

    def test_question_1_predict_check(self):
        """Executable check for Q1: predicting output under filtered condition."""
        ans = answer_applied_question_1_predict()
        self.assertEqual(ans["predicted_counts"], {"B": 2})
        self.assertEqual(ans["predicted_total"], 2)

    def test_question_2_diagnose_check(self):
        """Executable check for Q2: diagnosing state desynchronization failure."""
        ans = answer_applied_question_2_diagnose()
        self.assertEqual(ans["defect_type"], "STATE_DESYNCHRONIZATION")
        self.assertIn("unfiltered", ans["root_cause"].lower())

    def test_question_3_boundary_policy_check(self):
        """Executable check for Q3: choosing boundary policy for empty matches."""
        ans = answer_applied_question_3_boundary_policy()
        self.assertEqual(ans["chosen_policy"], "EMPTY_DICT_ZERO_TOTAL")
        self.assertEqual(ans["resulting_counts"], {})
        self.assertEqual(ans["resulting_total"], 0)

    def test_deliberate_wrong_result_fails(self):
        """Deliberately assert that filtering to A/B does NOT produce the unfiltered total 6."""
        _, total = compute_category_summary(self.fixture, allowed_categories=["A", "B"])
        self.assertNotEqual(total, 6, "Filtered total must equal 3, not the unfiltered total 6.")


if __name__ == "__main__":
    unittest.main()
