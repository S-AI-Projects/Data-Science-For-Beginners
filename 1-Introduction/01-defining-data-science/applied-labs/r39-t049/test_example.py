"""Unit tests for R39-T049 security-scenario rubric evaluation experiment."""

import unittest
from example import (
    FICTIONAL_SCENARIOS,
    SecurityScenario,
    evaluate_rubric,
    run_evaluation_experiment,
)


class TestSecurityScenarioEvaluationExperiment(unittest.TestCase):
    def test_three_fictional_scenarios_rubric_verdicts(self) -> None:
        results = {s.scenario_id: evaluate_rubric(s) for s in FICTIONAL_SCENARIOS}
        self.assertEqual(results["fictional_complete_pass"]["verdict"], "PASS")
        self.assertEqual(results["fictional_missing_asset_fail"]["verdict"], "FAIL")
        self.assertEqual(results["fictional_unrelated_control_review"]["verdict"], "REVIEW")

    def test_missing_asset_string_fails(self) -> None:
        sc = SecurityScenario(
            scenario_id="empty_asset_str",
            asset="   ",
            threat="Re-identification of survey respondents",
            control="Apply k-anonymity aggregation",
            residual_risk="Low",
        )
        res = evaluate_rubric(sc)
        self.assertEqual(res["verdict"], "FAIL")

    def test_evaluation_experiment_correctness_and_tradeoff(self) -> None:
        report = run_evaluation_experiment()
        self.assertIn("config_single", report)
        self.assertIn("config_triplet", report)
        self.assertIn("config_batch", report)

        for cfg_name, metrics in report.items():
            self.assertEqual(metrics["correctness_pct"], 100.0)
            self.assertGreater(metrics["count"], 0)
            self.assertGreater(metrics["total_microseconds"], 0)

    def test_deliberate_wrong_metric_fails(self) -> None:
        report = run_evaluation_experiment()
        with self.assertRaises(AssertionError):
            self.assertEqual(report["config_triplet"]["correctness_pct"], 50.0)


if __name__ == "__main__":
    unittest.main()
