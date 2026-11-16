"""Unit & Assessment Verification Suite for R39-T010.

Tests rubric evaluation rules, applied assessment questions, boundary policies,
deliberate wrong-answer failure detection, and fresh subprocess execution.
"""

import os
import subprocess
import sys
import unittest

from example import (
    FIXTURE_SCENARIO_1_PASS,
    FIXTURE_SCENARIO_2_FAIL,
    FIXTURE_SCENARIO_3_REVIEW,
    ASSESSMENT_QUESTIONS,
    SecurityScenario,
    evaluate_scenario,
    verify_assessment_answers,
)


class TestSecurityScenarioRubric(unittest.TestCase):
    """Test suite for security-scenario rubric evaluations and assessment checks."""

    def test_complete_scenario_passes(self):
        """Test 1: Complete, internally consistent scenario passes."""
        res = evaluate_scenario(FIXTURE_SCENARIO_1_PASS)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["reason"], "complete_and_consistent")
        self.assertFalse(res["requires_human_review"])
        self.assertTrue(res["diagnostics"]["matched_control"])

    def test_missing_asset_scenario_fails(self):
        """Test 2: Scenario without an asset fails with diagnostic missing_fields."""
        res = evaluate_scenario(FIXTURE_SCENARIO_2_FAIL)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["reason"], "missing_asset")
        self.assertIn("asset", res["diagnostics"]["missing_fields"])
        self.assertFalse(res["requires_human_review"])

    def test_unrelated_control_scenario_flagged_for_review(self):
        """Test 3: Scenario with a control unrelated to the named threat is flagged for review."""
        res = evaluate_scenario(FIXTURE_SCENARIO_3_REVIEW)
        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")
        self.assertEqual(res["reason"], "unrelated_control_threat_mismatch")
        self.assertTrue(res["requires_human_review"])
        self.assertFalse(res["diagnostics"]["matched_control"])

    def test_scenario_assessment_three_questions_pass(self):
        """Test 4: All three applied assessment questions include rationales and pass executable checks."""
        assessment_res = verify_assessment_answers(evaluate_scenario)
        self.assertEqual(assessment_res["passed"], 3)
        self.assertEqual(assessment_res["total"], 3)
        self.assertTrue(assessment_res["all_passed"])

        for detail in assessment_res["details"]:
            self.assertTrue(detail["has_rationale"], f"Question {detail['question_id']} must have non-empty rationale")
            self.assertTrue(detail["check_passed"], f"Question {detail['question_id']} executable check failed")
            self.assertTrue(detail["is_correct"], f"Question {detail['question_id']} marked incorrect")

    def test_deliberate_wrong_answer_fails_check(self):
        """Test 5: Deliberate wrong factual answer or corrupted rationale causes verification to fail."""
        # 1. Deliberate wrong answer for Q1
        wrong_q1 = {"Q1": "PASS", "Q2": "asset", "Q3": "strip_whitespace_reject_and_flag_unmapped_for_review"}
        res_wrong_q1 = verify_assessment_answers(evaluate_scenario, submitted_answers=wrong_q1)
        self.assertFalse(res_wrong_q1["all_passed"])
        self.assertEqual(res_wrong_q1["passed"], 2)

        # 2. Deliberate wrong answer for Q2 (wrong missing field)
        wrong_q2 = {"Q1": "FLAGGED_FOR_REVIEW", "Q2": "threat", "Q3": "strip_whitespace_reject_and_flag_unmapped_for_review"}
        res_wrong_q2 = verify_assessment_answers(evaluate_scenario, submitted_answers=wrong_q2)
        self.assertFalse(res_wrong_q2["all_passed"])
        self.assertEqual(res_wrong_q2["passed"], 2)

        # 3. Deliberate wrong answer for Q3 (permissive bypass policy)
        wrong_q3 = {"Q1": "FLAGGED_FOR_REVIEW", "Q2": "asset", "Q3": "allow_empty_strings_and_auto_pass"}
        res_wrong_q3 = verify_assessment_answers(evaluate_scenario, submitted_answers=wrong_q3)
        self.assertFalse(res_wrong_q3["all_passed"])
        self.assertEqual(res_wrong_q3["passed"], 2)

    def test_fresh_process_cli_execution(self):
        """Test 6: Running example.py in a fresh Python process exits 0 and produces expected output."""
        example_path = os.path.join(os.path.dirname(__file__), "example.py")
        proc = subprocess.run(
            [sys.executable, example_path],
            capture_output=True,
            text=True,
            check=False
        )
        self.assertEqual(proc.returncode, 0, f"Process failed with stderr: {proc.stderr}")
        stdout = proc.stdout
        self.assertIn("APPLIED LAB R39-T010", stdout)
        self.assertIn("[SIMULATION/MOCK]", stdout)
        self.assertIn("RW-01", stdout)
        self.assertIn("RW-02", stdout)
        self.assertIn("RW-03", stdout)
        self.assertIn("PASS (complete_and_consistent)", stdout)
        self.assertIn("FAIL (missing_asset)", stdout)
        self.assertIn("FLAGGED_FOR_REVIEW (unrelated_control_threat_mismatch)", stdout)
        self.assertIn("ASSESSMENT_CHECKS_PASSED: 3/3", stdout)


if __name__ == "__main__":
    unittest.main()
