"""Unit tests for R39-T043 client-consent gate state machine."""

import unittest
from example import (
    ConsentState,
    ModelSamplingRequest,
    REFERENCE_OUTCOMES_TABLE,
    mock_model_stub,
)


class TestClientConsentGate(unittest.TestCase):
    def test_approved_consent_calls_model_once(self) -> None:
        req = ModelSamplingRequest("req_appr")
        self.assertEqual(req.state, ConsentState.PENDING)
        res = req.approve(mock_model_stub)
        self.assertEqual(res["state"], "COMPLETED")
        self.assertEqual(res["invocations"], 1)
        self.assertIsNotNone(res["result"])

    def test_denied_consent_never_calls_model(self) -> None:
        call_tracker = {"calls": 0}

        def custom_stub(rid: str):
            call_tracker["calls"] += 1
            return {}

        req = ModelSamplingRequest("req_deny")
        res = req.deny()
        self.assertEqual(res["state"], "DENIED")
        self.assertEqual(res["invocations"], 0)
        self.assertIsNone(res["result"])
        self.assertEqual(call_tracker["calls"], 0)

    def test_completed_request_cannot_be_approved_again(self) -> None:
        req = ModelSamplingRequest("req_double")
        req.approve(mock_model_stub)
        self.assertEqual(req.state, ConsentState.COMPLETED)
        with self.assertRaises(RuntimeError):
            req.approve(mock_model_stub)
        self.assertEqual(req.invocation_count, 1)

    def test_compare_with_reference_table(self) -> None:
        # Evaluates state machine directly against the explicit expected-result reference table
        for row in REFERENCE_OUTCOMES_TABLE:
            if row["case"] == "approval_flow":
                r = ModelSamplingRequest("table_appr")
                res = r.approve(mock_model_stub)
                self.assertEqual(res["state"], row["expected_state"])
                self.assertEqual(res["invocations"], row["expected_invocations"])
                self.assertTrue(bool(res["result"]) == row["sample_generated"])
            elif row["case"] == "denial_flow":
                r = ModelSamplingRequest("table_deny")
                res = r.deny()
                self.assertEqual(res["state"], row["expected_state"])
                self.assertEqual(res["invocations"], row["expected_invocations"])
                self.assertTrue(bool(res["result"]) == row["sample_generated"])
            elif row["case"] == "repeat_approval":
                r = ModelSamplingRequest("table_repeat")
                r.approve(mock_model_stub)
                with self.assertRaises(RuntimeError) as ctx:
                    r.approve(mock_model_stub)
                self.assertIn(row["expected_error"], str(ctx.exception))
                self.assertEqual(r.invocation_count, row["expected_invocations"])

    def test_deliberate_wrong_invocation_fails(self) -> None:
        req = ModelSamplingRequest("req_fail")
        req.approve(mock_model_stub)
        with self.assertRaises(AssertionError):
            self.assertEqual(req.invocation_count, 2)


if __name__ == "__main__":
    unittest.main()
