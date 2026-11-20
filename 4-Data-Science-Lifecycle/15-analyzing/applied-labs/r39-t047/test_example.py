"""Unit tests and regression checks for R39-T047 client-consent gate."""

import unittest
from example import (
    ModelSamplingConsentGate,
    RequestState,
    WORKED_EXAMPLE_STEPS,
    default_model_stub,
    run_worked_example,
)


class TestClientConsentGateWorkedExample(unittest.TestCase):
    def test_approved_consent_calls_model_once(self) -> None:
        gate = ModelSamplingConsentGate("req_test_1")
        res = gate.approve(default_model_stub)
        self.assertEqual(res["state"], "COMPLETED")
        self.assertEqual(res["invocations"], 1)
        self.assertIsNotNone(res["result"])

    def test_denied_consent_never_calls_model(self) -> None:
        call_count = [0]

        def stub(rid: str):
            call_count[0] += 1
            return {}

        gate = ModelSamplingConsentGate("req_test_2")
        res = gate.deny()
        self.assertEqual(res["state"], "DENIED")
        self.assertEqual(res["invocations"], 0)
        self.assertIsNone(res["result"])
        self.assertEqual(call_count[0], 0)

    def test_completed_request_cannot_be_approved_again(self) -> None:
        gate = ModelSamplingConsentGate("req_test_3")
        gate.approve(default_model_stub)
        with self.assertRaises(RuntimeError):
            gate.approve(default_model_stub)
        self.assertEqual(gate.invocations, 1)

    def test_worked_example_regression_verification(self) -> None:
        """Execute the exact published worked example and verify step-by-step match."""
        trace = run_worked_example()
        self.assertEqual(len(trace), 3)

        # Step 1 verification
        self.assertEqual(trace[0]["step"], WORKED_EXAMPLE_STEPS[0]["step"])
        self.assertEqual(trace[0]["state"], WORKED_EXAMPLE_STEPS[0]["expected_state"])
        self.assertEqual(trace[0]["invocations"], WORKED_EXAMPLE_STEPS[0]["expected_invocations"])

        # Step 2 verification
        self.assertEqual(trace[1]["step"], WORKED_EXAMPLE_STEPS[1]["step"])
        self.assertEqual(trace[1]["state"], WORKED_EXAMPLE_STEPS[1]["expected_state"])
        self.assertEqual(trace[1]["invocations"], WORKED_EXAMPLE_STEPS[1]["expected_invocations"])

        # Step 3 verification
        self.assertEqual(trace[2]["step"], WORKED_EXAMPLE_STEPS[2]["step"])
        self.assertIn(WORKED_EXAMPLE_STEPS[2]["expected_exception"], trace[2]["caught_error"])
        self.assertEqual(trace[2]["invocations"], WORKED_EXAMPLE_STEPS[2]["expected_invocations"])

    def test_deliberate_wrong_call_fails(self) -> None:
        gate = ModelSamplingConsentGate("req_fail")
        gate.approve(default_model_stub)
        with self.assertRaises(AssertionError):
            self.assertEqual(gate.invocations, 0)


if __name__ == "__main__":
    unittest.main()
