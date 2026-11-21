"""Unit tests for Task R39-T056."""

import unittest
from example import (
    evaluate_scenario_baseline,
    evaluate_scenario_refactored,
    check_equivalence_on_fixture,
    FICTIONAL_SCENARIOS,
)


class TestSecurityRubricRefactoring(unittest.TestCase):
    def test_complete_scenario_passes(self):
        scenario = FICTIONAL_SCENARIOS[0]
        res = evaluate_scenario_refactored(scenario)
        self.assertEqual(res["verdict"], "PASS")

    def test_missing_asset_fails(self):
        scenario = FICTIONAL_SCENARIOS[1]
        res = evaluate_scenario_refactored(scenario)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertIn("asset", res["reason"])

    def test_unrelated_control_requires_review(self):
        scenario = FICTIONAL_SCENARIOS[2]
        res = evaluate_scenario_refactored(scenario)
        self.assertEqual(res["verdict"], "REVIEW")

    def test_equivalence_between_baseline_and_refactored(self):
        self.assertTrue(check_equivalence_on_fixture())
        for sc in FICTIONAL_SCENARIOS:
            self.assertEqual(
                evaluate_scenario_baseline(sc),
                evaluate_scenario_refactored(sc),
            )

    def test_deliberate_wrong_result_fails(self):
        scenario = FICTIONAL_SCENARIOS[0]
        res = evaluate_scenario_refactored(scenario)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
