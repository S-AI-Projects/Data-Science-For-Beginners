"""Unit and process verification suite for R39-T005 security-scenario rubric."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from typing import Any, Dict

# Ensure local lab directory is in sys.path for direct or discovery invocation
_LAB_DIR = os.path.dirname(os.path.abspath(__file__))
if _LAB_DIR not in sys.path:
    sys.path.insert(0, _LAB_DIR)

from example import (  # noqa: E402
    FIXTURES,
    UNESTABLISHED_REAL_SERVICE_BEHAVIORS,
    LocalOfflineRubricAdapter,
    SecurityScenario,
    deterministic_local_adapter,
    evaluate_scenario,
    run_evaluation_suite,
)


class TestSecurityScenarioRubric(unittest.TestCase):
    """Test suite verifying rubric rules, callable adapter contract, and CLI execution."""

    def test_01_complete_consistent_scenario_passes(self) -> None:
        """Test 1: Complete, internally consistent scenario passes (PASS)."""
        sc = FIXTURES[0]
        res = evaluate_scenario(sc)

        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["missing_fields"], [])
        self.assertTrue(res["alignment_matched"])
        self.assertEqual(res["adapter_result"]["category"], "sql_injection")

    def test_02_missing_asset_boundary_fails(self) -> None:
        """Test 2: Scenario without an asset fails (FAIL)."""
        sc_empty = FIXTURES[1]  # asset is ""
        res_empty = evaluate_scenario(sc_empty)
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
        res_none = evaluate_scenario(sc_none)
        self.assertEqual(res_none["status"], "FAIL")
        self.assertIn("asset", res_none["missing_fields"])

    def test_03_unrelated_control_flagged_for_review(self) -> None:
        """Test 3: Scenario with a control unrelated to the threat is flagged for review."""
        sc = FIXTURES[2]
        res = evaluate_scenario(sc)

        self.assertEqual(res["status"], "FLAGGED_FOR_REVIEW")
        self.assertFalse(res["alignment_matched"])
        self.assertEqual(res["missing_fields"], [])

    def test_04_callable_interface_injection_and_unestablished_behaviors(self) -> None:
        """Test 4: Callable interface injection works with default and custom adapters and reports unestablished behaviors."""
        # 1. Default adapter execution
        res_default = evaluate_scenario(FIXTURES[0])
        self.assertEqual(res_default["status"], "PASS")
        self.assertIn("[SIMULATION/MOCK]", res_default["adapter_result"]["adapter_name"])

        # 2. Functional adapter verification
        res_func = evaluate_scenario(FIXTURES[0], adapter=deterministic_local_adapter)
        self.assertEqual(res_func["status"], "PASS")

        # 3. Custom injected callable adapter
        def custom_injected_adapter(threat: str, control: str) -> Dict[str, Any]:
            return {
                "aligned": True,
                "category": "custom_override_category",
                "matched_terms": ["custom_rule"],
                "adapter_name": "MockCustomInjectedAdapter",
            }

        # Normally scenario 3 is FLAGGED_FOR_REVIEW; with custom adapter it should PASS
        res_custom = evaluate_scenario(FIXTURES[2], adapter=custom_injected_adapter)
        self.assertEqual(res_custom["status"], "PASS")
        self.assertTrue(res_custom["alignment_matched"])
        self.assertEqual(res_custom["adapter_result"]["adapter_name"], "MockCustomInjectedAdapter")

        # 4. Explicitly verify unestablished real-service behaviors
        self.assertEqual(res_default["unestablished_behaviors"], UNESTABLISHED_REAL_SERVICE_BEHAVIORS)
        self.assertIn(
            "Live IAM/policy API authentication & OAuth token exchange",
            res_default["unestablished_behaviors"],
        )
        self.assertIn(
            "Semantic LLM/NLP grading of free-text qualitative explanations",
            res_default["unestablished_behaviors"],
        )

    def test_05_deliberate_wrong_result_triggers_assertion_failure(self) -> None:
        """Test 5: Deliberate wrong result from a faulty injected adapter makes the test fail."""
        def faulty_adapter(threat: str, control: str) -> Dict[str, Any]:
            # Faulty adapter returns aligned=False for all queries
            return {
                "aligned": False,
                "category": "broken",
                "matched_terms": [],
                "adapter_name": "FaultyBrokenAdapter",
            }

        res_faulty = evaluate_scenario(FIXTURES[0], adapter=faulty_adapter)
        # Should be FLAGGED_FOR_REVIEW due to faulty adapter
        self.assertEqual(res_faulty["status"], "FLAGGED_FOR_REVIEW")
        with self.assertRaises(AssertionError):
            self.assertEqual(res_faulty["status"], "PASS")

        # Also verify mutated rubric check status failure
        corrupted = dict(evaluate_scenario(FIXTURES[0]))
        corrupted["status"] = "FAIL"
        with self.assertRaises(AssertionError):
            self.assertEqual(corrupted["status"], "PASS")

    def test_06_fresh_process_cli_execution(self) -> None:
        """Test 6: Fresh-process CLI execution verifies normal execution and expected stdout markers."""
        script_path = os.path.join(_LAB_DIR, "example.py")
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        self.assertIn("[SIMULATION/MOCK] Deterministic Local Offline Adapter", proc.stdout)
        self.assertIn("PASS", proc.stdout)
        self.assertIn("FAIL", proc.stdout)
        self.assertIn("FLAGGED_FOR_REVIEW", proc.stdout)
        self.assertIn("UNESTABLISHED REAL-SERVICE BEHAVIORS", proc.stdout)
        self.assertIn("Semantic LLM/NLP grading of free-text qualitative explanations", proc.stdout)


if __name__ == "__main__":
    unittest.main()
