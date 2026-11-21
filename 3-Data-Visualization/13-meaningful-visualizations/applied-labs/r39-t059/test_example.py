"""Unit tests for Task R39-T059."""

import unittest
from example import (
    build_category_summary,
    check_q1_predict_output,
    check_q2_diagnose_failure,
    check_q3_boundary_policy,
    ASSESSMENT_QUESTIONS,
)


class TestChartScenarioAssessment(unittest.TestCase):
    def test_full_and_filtered_counts_and_totals(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        full = build_category_summary(rows)
        self.assertEqual(full["labels"], ["A", "B", "C"])
        self.assertEqual(full["counts"], [2, 1, 3])
        self.assertEqual(full["displayed_total"], 6)
        self.assertTrue(full["consistent"])

        filtered = build_category_summary(rows, filter_categories=["A", "B"])
        self.assertEqual(filtered["labels"], ["A", "B"])
        self.assertEqual(filtered["counts"], [2, 1])
        self.assertEqual(filtered["displayed_total"], 3)
        self.assertTrue(filtered["consistent"])

    def test_applied_question_q1(self):
        self.assertTrue(check_q1_predict_output())
        self.assertEqual(
            ASSESSMENT_QUESTIONS["q1_predict_output"]["predicted_total"], 3
        )

    def test_applied_question_q2(self):
        self.assertTrue(check_q2_diagnose_failure())
        self.assertEqual(
            ASSESSMENT_QUESTIONS["q2_diagnose_failure"]["diagnosed_cause"],
            "stale_unfiltered_total_mismatch",
        )

    def test_applied_question_q3(self):
        self.assertTrue(check_q3_boundary_policy())
        self.assertEqual(
            ASSESSMENT_QUESTIONS["q3_boundary_policy"]["policy_choice"],
            "flag_as_inconsistent",
        )

    def test_deliberate_wrong_result_fails(self):
        rows = ["A", "A", "B", "C", "C", "C"]
        filtered = build_category_summary(rows, filter_categories=["A", "B"])
        with self.assertRaises(AssertionError):
            self.assertEqual(filtered["displayed_total"], 6)


if __name__ == "__main__":
    unittest.main()
