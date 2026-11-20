"""Unit tests for R39-T044 security-scenario rubric and state trace invariant."""

import unittest
from example import (
    FICTIONAL_SCENARIOS,
    SecurityScenario,
    evaluate_scenario,
    verify_state_trace_invariant,
)


class TestSecurityScenarioRubric(unittest.TestCase):
    def test_three_fictional_scenarios_verdicts(self) -> None:
        results = {sc.scenario_id: evaluate_scenario(sc) for sc in FICTIONAL_SCENARIOS}
        self.assertEqual(results["fictional_complete_pass"]["verdict"], "PASS")
        self.assertEqual(results["fictional_missing_asset_fail"]["verdict"], "FAIL")
        self.assertEqual(results["fictional_unrelated_control_review"]["verdict"], "REVIEW")

        for res in results.values():
            self.assertTrue(verify_state_trace_invariant(res))

    def test_missing_asset_none_fails(self) -> None:
        sc = SecurityScenario(
            scenario_id="boundary_none_asset",
            asset=None,
            threat="Pipeline leak of credentials",
            control="Enforce secret manager access policy",
            residual_risk="Low",
        )
        res = evaluate_scenario(sc)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertTrue(verify_state_trace_invariant(res))

    def test_deliberate_wrong_verdict_violates_invariant(self) -> None:
        sc = FICTIONAL_SCENARIOS[1]  # missing asset -> FAIL
        res = evaluate_scenario(sc)
        tampered = dict(res)
        tampered["verdict"] = "PASS"
        self.assertFalse(verify_state_trace_invariant(tampered))


if __name__ == "__main__":
    unittest.main()
