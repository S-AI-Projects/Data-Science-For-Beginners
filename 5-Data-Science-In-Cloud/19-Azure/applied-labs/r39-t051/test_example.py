"""Unit tests for Task R39-T051."""

import unittest
from example import evaluate_scenario, FICTIONAL_SCENARIOS


class TestSecurityScenarioRubric(unittest.TestCase):
    def test_complete_scenario_passes(self):
        scenario = FICTIONAL_SCENARIOS[0]
        res = evaluate_scenario(scenario)
        self.assertEqual(res["verdict"], "PASS")

    def test_missing_asset_fails(self):
        scenario = FICTIONAL_SCENARIOS[1]
        res = evaluate_scenario(scenario)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertIn("asset", res["reason"])

    def test_unrelated_control_needs_review(self):
        scenario = FICTIONAL_SCENARIOS[2]
        res = evaluate_scenario(scenario)
        self.assertEqual(res["verdict"], "REVIEW")

    def test_deliberate_wrong_result_fails(self):
        scenario = FICTIONAL_SCENARIOS[0]
        res = evaluate_scenario(scenario)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
