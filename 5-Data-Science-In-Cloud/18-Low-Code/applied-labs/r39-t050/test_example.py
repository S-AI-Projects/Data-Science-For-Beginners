"""Unit tests for R39-T050 security-scenario rubric and applied questions."""

import unittest
from example import (
    ASSESSMENT_QUESTIONS,
    FICTIONAL_SCENARIOS,
    check_q1_predict_output,
    check_q2_diagnose_failure,
    check_q3_boundary_policy,
    evaluate_scenario,
)


class TestSecurityScenarioAssessment(unittest.TestCase):
    def test_three_fictional_scenarios_verdicts(self) -> None:
        results = {s.scenario_id: evaluate_scenario(s) for s in FICTIONAL_SCENARIOS}
        self.assertEqual(results["fictional_complete_pass"]["verdict"], "PASS")
        self.assertEqual(results["fictional_missing_asset_fail"]["verdict"], "FAIL")
        self.assertEqual(results["fictional_unrelated_control_review"]["verdict"], "REVIEW")

    def test_applied_question_q1_predict_output(self) -> None:
        self.assertTrue(check_q1_predict_output())
        self.assertEqual(ASSESSMENT_QUESTIONS["q1_predict_output"]["predicted_output"], "PASS")

    def test_applied_question_q2_diagnose_failure(self) -> None:
        self.assertTrue(check_q2_diagnose_failure())
        self.assertEqual(ASSESSMENT_QUESTIONS["q2_diagnose_failure"]["diagnosed_cause"], "asset_field_none")

    def test_applied_question_q3_boundary_policy(self) -> None:
        self.assertTrue(check_q3_boundary_policy())
        self.assertEqual(ASSESSMENT_QUESTIONS["q3_boundary_policy"]["policy_choice"], "flag_for_review")

    def test_deliberate_wrong_answer_fails(self) -> None:
        with self.assertRaises(AssertionError):
            self.assertEqual(evaluate_scenario(FICTIONAL_SCENARIOS[0])["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
