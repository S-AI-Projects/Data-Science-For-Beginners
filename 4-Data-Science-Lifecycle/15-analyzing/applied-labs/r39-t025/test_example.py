"""
Tests for Client-Consent Sampling State Machine (R39-T025)
"""

import unittest
from example import MockModelAdapter, SamplingConsentRequest


class TestSamplingConsentStateMachine(unittest.TestCase):
    def setUp(self):
        self.adapter = MockModelAdapter()
        self.payload = {"query": "sample data"}

    def test_approved_consent_calls_model_once(self):
        """Approved consent calls the model stub exactly once and transitions state to APPROVED."""
        req = SamplingConsentRequest("REQ-101", self.payload, self.adapter)
        self.assertEqual(req.state, SamplingConsentRequest.PENDING)

        res = req.approve()
        self.assertEqual(req.state, SamplingConsentRequest.APPROVED)
        self.assertEqual(res["status"], "APPROVED")
        self.assertEqual(self.adapter.call_count, 1)

    def test_denied_consent_never_calls_model(self):
        """Denied consent never calls the model stub; transitions state to DENIED."""
        req = SamplingConsentRequest("REQ-102", self.payload, self.adapter)
        res = req.deny("User opted out")
        self.assertEqual(req.state, SamplingConsentRequest.DENIED)
        self.assertEqual(res["status"], "DENIED")
        self.assertEqual(self.adapter.call_count, 0)

    def test_terminal_state_cannot_be_approved_again(self):
        """A completed request cannot be approved again; transitions out of terminal states raise ValueError."""
        # Test approval on already approved request
        req1 = SamplingConsentRequest("REQ-103", self.payload, self.adapter)
        req1.approve()
        with self.assertRaises(ValueError):
            req1.approve()

        # Test approval on already denied request
        req2 = SamplingConsentRequest("REQ-104", self.payload, self.adapter)
        req2.deny()
        with self.assertRaises(ValueError):
            req2.approve()

    def test_terminal_state_cannot_be_denied_again(self):
        """A completed request cannot be denied again."""
        req = SamplingConsentRequest("REQ-105", self.payload, self.adapter)
        req.approve()
        with self.assertRaises(ValueError):
            req.deny()

    def test_deliberate_wrong_result_fails(self):
        """Assert that denied consent does NOT trigger any model calls (leakage check)."""
        req = SamplingConsentRequest("REQ-106", self.payload, self.adapter)
        req.deny()
        self.assertNotEqual(self.adapter.call_count, 1, "Denied request must never execute model adapter.")


if __name__ == "__main__":
    unittest.main()
