"""Unit and recovery verification suite for R39-T008 cloud security-scenario rubric."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

# Ensure local lab directory is in sys.path for direct or discovery invocation
_LAB_DIR = os.path.dirname(os.path.abspath(__file__))
if _LAB_DIR not in sys.path:
    sys.path.insert(0, _LAB_DIR)

from example import (  # noqa: E402
    FIXTURES,
    SecurityScenario,
    evaluate_scenario,
    process_scenario_stream,
)


class TestCloudSecurityScenarioRubric(unittest.TestCase):
    """Test suite verifying rubric evaluation, error explanations, and stream recovery."""

    def test_01_complete_consistent_cloud_scenario_passes(self) -> None:
        """Test 1: Complete, internally consistent cloud scenario passes (PASS)."""
        sc = FIXTURES[0]
        res = evaluate_scenario(sc)

        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["missing_fields"], [])
        self.assertTrue(res["alignment_matched"])
        self.assertIsNone(res["error_code"])

    def test_02_missing_asset_boundary_fails_with_explanation(self) -> None:
        """Test 2: Scenario without an asset fails (FAIL) with structured error explanation."""
        sc_empty = FIXTURES[1]  # asset is ""
        res_empty = evaluate_scenario(sc_empty)

        self.assertEqual(res_empty["status"], "FAIL")
        self.assertIn("asset", res_empty["missing_fields"])
        self.assertEqual(res_empty["error_code"], "MISSING_REQUIRED_FIELD")
        self.assertIsNotNone(res_empty["error_explanation"])
        self.assertIn("'asset'", res_empty["error_explanation"])

        # Boundary variation: asset is None
        sc_none = SecurityScenario(
            scenario_id="scenario_none_asset",
            asset=None,
            threat="Man-in-the-middle interception",
            control="Enforce TLS 1.3 encryption",
            residual_risk="Low",
            explanation="Asset omitted entirely as None.",
        )
        res_none = evaluate_scenario(sc_none)
        self.assertEqual(res_none["status"], "FAIL")
        self.assertIn("asset", res_none["missing_fields"])
        self.assertEqual(res_none["error_code"], "MISSING_REQUIRED_FIELD")

    def test_03_unrelated_control_flagged_for_review(self) -> None:
        """Test 3: Scenario with a control unrelated to the cloud threat is flagged for review."""
        sc = FIXTURES[2]
        res = evaluate_scenario(sc)

        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")
        self.assertFalse(res["alignment_matched"])
        self.assertEqual(res["missing_fields"], [])
        self.assertEqual(res["error_code"], "CONTROL_THREAT_MISALIGNMENT")
        self.assertIsNotNone(res["error_explanation"])

    def test_04_failure_and_recovery_stream_pipeline(self) -> None:
        """Test 4: Processing [invalid_scenario, valid_scenario] records error and recovers cleanly."""
        # Sequence: [Scenario 2 (FAIL: missing asset), Scenario 1 (PASS: complete valid)]
        stream = [FIXTURES[1], FIXTURES[0]]
        results = process_scenario_stream(stream)

        self.assertEqual(len(results), 2)

        # First entry: invalid item fails with error
        first = results[0]
        self.assertEqual(first["status"], "FAIL")
        self.assertEqual(first["error_code"], "MISSING_REQUIRED_FIELD")
        self.assertFalse(first["recovered"])
        self.assertFalse(first["recovered_after_failure"])

        # Second entry: valid scenario executes and recovers cleanly
        second = results[1]
        self.assertEqual(second["status"], "PASS")
        self.assertTrue(second["recovered"])
        self.assertTrue(second["recovered_after_failure"])
        self.assertIsNone(second["error_code"])

    def test_05_deliberate_wrong_result_triggers_assertion_failure(self) -> None:
        """Test 5: Deliberate wrong result or failed recovery triggers assertion failure."""
        # Deliberately mark missing-asset scenario as PASS
        res = evaluate_scenario(FIXTURES[1])
        corrupted_status = dict(res)
        corrupted_status["status"] = "PASS"

        with self.assertRaises(AssertionError):
            self.assertEqual(corrupted_status["status"], "FAIL")

        # Deliberately fail recovery on next valid scenario
        stream_results = process_scenario_stream([FIXTURES[1], FIXTURES[0]])
        corrupted_recovery = dict(stream_results[1])
        corrupted_recovery["recovered"] = False

        with self.assertRaises(AssertionError):
            self.assertTrue(corrupted_recovery["recovered"])

    def test_06_fresh_process_cli_execution(self) -> None:
        """Test 6: Running example.py in fresh process exits with code 0 and required tokens."""
        script_path = os.path.join(_LAB_DIR, "example.py")
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        self.assertIn("status=PASS", proc.stdout)
        self.assertIn("status=FAIL", proc.stdout)
        self.assertIn("status=FLAGGED_FOR_REVIEW", proc.stdout)
        self.assertIn("Recovery verified: True", proc.stdout)
        self.assertIn("[SIMULATION/MOCK]", proc.stdout)


if __name__ == "__main__":
    unittest.main()
