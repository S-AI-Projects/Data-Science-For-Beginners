
"""Tests for the local cloud-security rubric example."""

import unittest

from example import evaluate_scenario


class TestEvaluateScenario(unittest.TestCase):

    def setUp(self):
        self.valid_scenario = {
            "name": "Test cloud database",
            "asset": "Customer records stored in a cloud database",
            "threat": (
                "An unauthorized user accesses the database "
                "because it is publicly accessible"
            ),
            "control": (
                "Restrict database access using identity-based "
                "permissions and network access rules"
            ),
            "residual_risk": (
                "A compromised authorized account could still "
                "access permitted records"
            ),
        }

    def test_complete_scenario_passes(self):
        result = evaluate_scenario(self.valid_scenario)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["issues"], [])

    def test_missing_asset_fails(self):
        scenario = self.valid_scenario.copy()
        scenario["asset"] = ""

        result = evaluate_scenario(scenario)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "Missing or empty required field: asset",
            result["issues"],
        )

    def test_unrelated_control_requires_review(self):
        scenario = self.valid_scenario.copy()
        scenario["control"] = "Encrypt stored data"

        result = evaluate_scenario(scenario)

        self.assertEqual(result["status"], "REVIEW")
        self.assertTrue(result["issues"])

    def test_missing_residual_risk_fails(self):
        scenario = self.valid_scenario.copy()
        scenario["residual_risk"] = ""

        result = evaluate_scenario(scenario)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "Missing or empty required field: residual_risk",
            result["issues"],
        )


if __name__ == "__main__":
    unittest.main()
