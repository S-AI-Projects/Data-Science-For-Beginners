import unittest
from example import evaluate_security_scenario, CANONICAL_SCENARIOS

class TestSecurityScenarioRubric(unittest.TestCase):
    def test_complete_scenario_passes(self):
        """Rule 1: A complete, consistent scenario must PASS."""
        res = evaluate_security_scenario(CANONICAL_SCENARIOS["complete_pass"])
        self.assertEqual(res["status"], "PASS")
        self.assertIn("structurally consistent", res["reason"])

    def test_missing_asset_fails(self):
        """Rule 2: A scenario missing an asset must FAIL."""
        res = evaluate_security_scenario(CANONICAL_SCENARIOS["missing_asset_fail"])
        self.assertEqual(res["status"], "FAIL")
        self.assertIn("Missing asset", res["reason"])

    def test_unrelated_control_flagged_for_review(self):
        """Rule 3: Control unrelated to named threat must be FLAGGED_FOR_REVIEW."""
        res = evaluate_security_scenario(CANONICAL_SCENARIOS["unrelated_control_review"])
        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")
        self.assertIn("Control unrelated to named threat", res["reason"])

    def test_missing_threat_fails(self):
        """Additional check: Missing threat must FAIL."""
        scenario = {"asset": "Dataset", "threat": "", "control": "TLS", "residual_risk": "Low"}
        res = evaluate_security_scenario(scenario)
        self.assertEqual(res["status"], "FAIL")
        self.assertIn("Missing threat", res["reason"])

    def test_deliberate_wrong_result_fails(self):
        """Deliberate wrong result check: Passing bad scenario must NOT pass."""
        bad_scenario = {"asset": None, "threat": "data leak", "control": "encryption", "residual_risk": "low"}
        res = evaluate_security_scenario(bad_scenario)
        self.assertNotEqual(res["status"], "PASS", "A scenario with None asset must never pass!")

if __name__ == "__main__":
    unittest.main()
