"""Unit tests for R39-T004 security-scenario rubric and state trace."""

import unittest

from example import (
    FICTIONAL_SCENARIOS,
    SecurityScenario,
    evaluate_scenario,
    verify_state_trace_invariant,
)


class TestSecurityScenarioRubric(unittest.TestCase):
    def test_three_fictional_scenarios_verdicts_and_invariants(self) -> None:
        results = {sc.scenario_id: evaluate_scenario(sc) for sc in FICTIONAL_SCENARIOS}

        self.assertEqual(results["fictional_complete_pass"]["verdict"], "PASS")
        self.assertEqual(results["fictional_missing_asset_fail"]["verdict"], "FAIL")
        self.assertEqual(
            results["fictional_unrelated_control_review"]["verdict"], "REVIEW"
        )

        for res in results.values():
            self.assertTrue(verify_state_trace_invariant(res))

    def test_missing_asset_none_fails_and_records_state(self) -> None:
        scenario = SecurityScenario(
            scenario_id="none_asset_boundary",
            asset=None,
            threat="Unauthorized endpoint access",
            control="Require RBAC authentication",
            residual_risk="Low",
        )
        res = evaluate_scenario(scenario)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertFalse(res["state_trace"][0]["asset_present"])
        self.assertIn("asset", res["state_trace"][0]["missing_fields"])
        self.assertTrue(verify_state_trace_invariant(res))

    def test_deliberate_wrong_verdict_violates_invariant(self) -> None:
        res = evaluate_scenario(FICTIONAL_SCENARIOS[1])  # missing asset -> FAIL
        corrupted = dict(res)
        corrupted["verdict"] = "PASS"
        self.assertFalse(verify_state_trace_invariant(corrupted))


if __name__ == "__main__":
    unittest.main()
