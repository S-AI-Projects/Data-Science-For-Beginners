"""Unit and process verification suite for R39-T006 security-scenario rubric."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

# Ensure the local lab directory is in sys.path for direct or discovery invocation
_LAB_DIR = os.path.dirname(os.path.abspath(__file__))
if _LAB_DIR not in sys.path:
    sys.path.insert(0, _LAB_DIR)

from example import (  # noqa: E402
    FIXTURES,
    SecurityScenario,
    check_threat_control_alignment,
    evaluate_scenario_baseline,
    evaluate_scenario_refactored,
    run_baseline_suite,
    run_refactored_suite,
)


class TestSecurityScenarioRubric(unittest.TestCase):
    """Test suite verifying rubric evaluation, refactoring equivalence, and CLI execution."""

    def test_01_complete_consistent_scenario_passes(self) -> None:
        """Test 1: Complete, internally consistent scenario passes (PASS)."""
        sc = FIXTURES[0]
        res_baseline = evaluate_scenario_baseline(sc)
        res_refactored = evaluate_scenario_refactored(sc)

        self.assertEqual(res_refactored["status"], "PASS")
        self.assertEqual(res_refactored["missing_fields"], [])
        self.assertTrue(res_refactored["alignment_matched"])
        self.assertEqual(res_baseline["status"], "PASS")

    def test_02_missing_asset_boundary_fails(self) -> None:
        """Test 2: Scenario without an asset fails (FAIL)."""
        sc_empty = FIXTURES[1]  # asset is ""
        res_empty = evaluate_scenario_refactored(sc_empty)
        self.assertEqual(res_empty["status"], "FAIL")
        self.assertIn("asset", res_empty["missing_fields"])

        # Boundary variation: asset is None
        sc_none = SecurityScenario(
            scenario_id="scenario_none_asset_boundary",
            asset=None,
            threat="Unencrypted secondary survey storage leading to leak of qualitative feedback responses",
            control="Enforce AES-256 at-rest encryption and access control lists for secondary file stores",
            residual_risk="Low: Key rotation failure or compromised credentials",
            explanation="Asset field omitted entirely as None.",
        )
        res_none = evaluate_scenario_refactored(sc_none)
        self.assertEqual(res_none["status"], "FAIL")
        self.assertIn("asset", res_none["missing_fields"])

    def test_03_unrelated_control_flagged_for_review(self) -> None:
        """Test 3: Scenario with a control unrelated to the threat is flagged for review."""
        sc = FIXTURES[2]
        res = evaluate_scenario_refactored(sc)

        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")
        self.assertFalse(res["alignment_matched"])
        self.assertEqual(res["missing_fields"], [])
        self.assertFalse(check_threat_control_alignment(sc.threat, sc.control))

    def test_04_baseline_refactored_equivalence_across_fixture(self) -> None:
        """Test 4: Baseline vs. refactored implementation equivalence holds across the fixture."""
        baseline_results = run_baseline_suite(FIXTURES)
        refactored_results = run_refactored_suite(FIXTURES)

        self.assertEqual(len(baseline_results), len(FIXTURES))
        self.assertEqual(len(refactored_results), len(FIXTURES))
        self.assertEqual(baseline_results, refactored_results)

    def test_05_deliberate_wrong_result_triggers_assertion_failure(self) -> None:
        """Test 5: Deliberate wrong result / mutated rubric output triggers an assertion failure."""
        results = run_refactored_suite(FIXTURES)
        mutated_results = [dict(r) for r in results]

        # Mutate the expected status of the passing scenario to FAIL
        mutated_results[0]["status"] = "FAIL"

        with self.assertRaises(AssertionError):
            self.assertEqual(mutated_results, run_baseline_suite(FIXTURES))

        with self.assertRaises(AssertionError):
            self.assertEqual(mutated_results[0]["status"], "PASS")

    def test_06_fresh_process_cli_execution(self) -> None:
        """Test 6: Fresh-process CLI execution verifies normal execution and expected tokens."""
        script_path = os.path.join(_LAB_DIR, "example.py")
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        self.assertIn("EQUIVALENCE_VERIFIED: True", proc.stdout)
        self.assertIn("PASS", proc.stdout)
        self.assertIn("FAIL", proc.stdout)
        self.assertIn("FLAGGED_FOR_REVIEW", proc.stdout)
        self.assertIn("[SIMULATION/MOCK]", proc.stdout)


if __name__ == "__main__":
    unittest.main()
