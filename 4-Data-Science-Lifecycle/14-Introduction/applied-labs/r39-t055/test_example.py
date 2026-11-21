"""Unit tests for Task R39-T055."""

import unittest
from example import (
    LocalPolicyAdapter,
    evaluate_scenario,
    FICTIONAL_SCENARIOS,
)


class TestSecurityRubricAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = LocalPolicyAdapter()

    def test_complete_scenario_passes(self):
        scenario = FICTIONAL_SCENARIOS[0]
        res = evaluate_scenario(scenario, self.adapter)
        self.assertEqual(res["verdict"], "PASS")

    def test_missing_asset_fails(self):
        scenario = FICTIONAL_SCENARIOS[1]
        res = evaluate_scenario(scenario, self.adapter)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertIn("asset", res["reason"])

    def test_unrelated_control_requires_review(self):
        scenario = FICTIONAL_SCENARIOS[2]
        res = evaluate_scenario(scenario, self.adapter)
        self.assertEqual(res["verdict"], "REVIEW")

    def test_adapter_callable_and_unestablished_behaviors(self):
        behaviors = self.adapter.get_unestablished_behaviors()
        self.assertIsInstance(behaviors, list)
        self.assertTrue(len(behaviors) >= 3)
        # Verify custom adapter injection
        dummy_adapter = lambda threat, control: True
        res = evaluate_scenario(FICTIONAL_SCENARIOS[2], dummy_adapter)
        self.assertEqual(res["verdict"], "PASS")

    def test_deliberate_wrong_result_fails(self):
        scenario = FICTIONAL_SCENARIOS[0]
        res = evaluate_scenario(scenario, self.adapter)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
