import subprocess
import sys
import unittest

from example import FIXTURES, evaluate_metric_claims, wilson_score_interval


class MetricClaimsAuditTests(unittest.TestCase):
    # --- Normal Scenarios ---
    def test_normal_evaluation_with_fixtures(self) -> None:
        report = evaluate_metric_claims(FIXTURES, claimed_accuracy_threshold=0.90, min_subgroup_sample_size=30)
        self.assertEqual(report.overall_sample_size, 1080)
        self.assertAlmostEqual(report.overall_accuracy, 0.9454, places=4)
        self.assertTrue(report.unsupported_claim_detected)

        # Subgroup evaluations check
        self.assertEqual(len(report.group_evaluations), 3)

        subgroup_a = report.group_evaluations[0]
        self.assertEqual(subgroup_a.group_name, "Subgroup A (Majority)")
        self.assertEqual(subgroup_a.sample_size, 950)
        self.assertEqual(subgroup_a.correct_count, 903)
        self.assertTrue(subgroup_a.is_adequately_powered)
        self.assertEqual(subgroup_a.warning, "")

        subgroup_b = report.group_evaluations[1]
        self.assertEqual(subgroup_b.group_name, "Subgroup B (Adequate Minority)")
        self.assertEqual(subgroup_b.sample_size, 120)
        self.assertTrue(subgroup_b.is_adequately_powered)
        self.assertIn("falls below claimed threshold", subgroup_b.warning)

        subgroup_c = report.group_evaluations[2]
        self.assertEqual(subgroup_c.group_name, "Subgroup C (Under-sampled Minority)")
        self.assertEqual(subgroup_c.sample_size, 10)
        self.assertFalse(subgroup_c.is_adequately_powered)
        self.assertIn("below minimum power threshold", subgroup_c.warning)

    def test_normal_fully_supported_claim(self) -> None:
        well_powered_fixtures = [
            {"name": "Group 1", "sample_size": 200, "correct_count": 195},  # 97.5%
            {"name": "Group 2", "sample_size": 200, "correct_count": 196},  # 98.0%
        ]
        report = evaluate_metric_claims(well_powered_fixtures, claimed_accuracy_threshold=0.90, min_subgroup_sample_size=50)
        self.assertFalse(report.unsupported_claim_detected)
        self.assertEqual(len(report.findings), 0)
        self.assertTrue(all(g.is_adequately_powered for g in report.group_evaluations))

    # --- Boundary Scenarios ---
    def test_boundary_exact_minimum_sample_size(self) -> None:
        boundary_fixture = [
            {"name": "Boundary Group", "sample_size": 30, "correct_count": 30}
        ]
        report = evaluate_metric_claims(boundary_fixture, claimed_accuracy_threshold=0.85, min_subgroup_sample_size=30)
        self.assertTrue(report.group_evaluations[0].is_adequately_powered)

    def test_boundary_zero_and_perfect_accuracy(self) -> None:
        extreme_fixtures = [
            {"name": "Zero Correct", "sample_size": 50, "correct_count": 0},
            {"name": "All Correct", "sample_size": 50, "correct_count": 50},
        ]
        report = evaluate_metric_claims(extreme_fixtures, claimed_accuracy_threshold=0.50, min_subgroup_sample_size=30)
        self.assertEqual(report.group_evaluations[0].accuracy, 0.0)
        self.assertEqual(report.group_evaluations[0].ci_lower, 0.0)
        self.assertEqual(report.group_evaluations[1].accuracy, 1.0)
        self.assertEqual(report.group_evaluations[1].ci_upper, 1.0)

    # --- Failure Scenarios ---
    def test_failure_invalid_threshold_types_and_bounds(self) -> None:
        with self.assertRaises(TypeError):
            evaluate_metric_claims(FIXTURES, claimed_accuracy_threshold="0.90")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            evaluate_metric_claims(FIXTURES, claimed_accuracy_threshold=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            evaluate_metric_claims(FIXTURES, claimed_accuracy_threshold=-0.1)
        with self.assertRaises(ValueError):
            evaluate_metric_claims(FIXTURES, claimed_accuracy_threshold=1.5)

    def test_failure_invalid_min_sample_size(self) -> None:
        with self.assertRaises(TypeError):
            evaluate_metric_claims(FIXTURES, min_subgroup_sample_size="30")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            evaluate_metric_claims(FIXTURES, min_subgroup_sample_size=0)
        with self.assertRaises(ValueError):
            evaluate_metric_claims(FIXTURES, min_subgroup_sample_size=-5)

    def test_failure_invalid_groups_structure(self) -> None:
        with self.assertRaises(TypeError):
            evaluate_metric_claims("invalid")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            evaluate_metric_claims([])
        with self.assertRaises(TypeError):
            evaluate_metric_claims([1, 2, 3])  # type: ignore[list-item]

    def test_failure_invalid_group_fields(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_metric_claims([{"name": "", "sample_size": 10, "correct_count": 5}])
        with self.assertRaises(ValueError):
            evaluate_metric_claims([{"name": "G", "sample_size": -5, "correct_count": 0}])
        with self.assertRaises(ValueError):
            evaluate_metric_claims([{"name": "G", "sample_size": 10, "correct_count": 15}])
        with self.assertRaises(ValueError):
            evaluate_metric_claims([{"name": "G", "sample_size": 10, "correct_count": -1}])

    def test_failure_wilson_interval_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            wilson_score_interval(5, 0)
        with self.assertRaises(ValueError):
            wilson_score_interval(-1, 10)
        with self.assertRaises(ValueError):
            wilson_score_interval(11, 10)

    # --- Regression Test: Exact Output Execution ---
    def test_regression_exact_example_execution(self) -> None:
        expected_output = (
            "Aggregate Evaluation:\n"
            "  Total Samples: 1080\n"
            "  Overall Accuracy: 94.54%\n"
            "Subgroup Metric Audit:\n"
            "  - Subgroup A (Majority): n=950, accuracy=95.05%, 95% CI=[93.48%, 96.26%] [ADEQUATE]\n"
            "  - Subgroup B (Adequate Minority): n=120, accuracy=90.83%, 95% CI=[84.33%, 94.80%] [ADEQUATE]\n"
            "  - Subgroup C (Under-sampled Minority): n=10, accuracy=90.00%, 95% CI=[59.58%, 98.21%] [UNDERPOWERED]\n"
            "Claim Audit:\n"
            "  Unsupported claims detected: True\n"
            "  * Subgroup 'Subgroup B (Adequate Minority)': Lower confidence bound (0.84) falls below claimed threshold (0.90)\n"
            "  * Subgroup 'Subgroup C (Under-sampled Minority)': Sample size 10 is below minimum power threshold (30): high uncertainty (CI: [0.60, 0.98])\n"
            "  * Overall accuracy claim (94.5%) conceals high uncertainty or disparity in subgroup metric claims.\n"
        )
        proc = subprocess.run(
            [sys.executable, "1-Introduction/02-ethics/applied-labs/r39-t037/example.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(proc.stdout, expected_output)


if __name__ == "__main__":
    unittest.main()
