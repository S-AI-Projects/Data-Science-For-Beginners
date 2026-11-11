"""
Client-Consent Sampling State Machine (R39-T025)

Extends lesson 15 (Analyzing) by modeling privacy-preserving client-side model sampling.
Enforces a strict state machine:
- Initial state: PENDING
- Terminal states: APPROVED, DENIED
- Denied consent NEVER invokes the external model adapter.
- Approved consent invokes the model adapter exactly once.
- Once completed (terminal state), requests cannot be transitioned or approved again.
"""

from typing import Any, Callable, Dict, Optional


class MockModelAdapter:
    """
    Deterministic local adapter standing in for an external ML model service.
    Tracks invocation count and returns deterministic synthetic outputs.
    """

    def __init__(self, response_generator: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        self.call_count = 0
        self.response_generator = response_generator or (lambda payload: {"prediction": 0.85, "features": payload})

    def sample(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.call_count += 1
        return self.response_generator(payload)


class SamplingConsentRequest:
    """
    State machine governing client consent for model sampling requests.
    Valid state transitions:
      PENDING -> APPROVED (triggers model adapter invocation)
      PENDING -> DENIED   (aborts with zero adapter invocations)
    """

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"

    def __init__(self, request_id: str, payload: Dict[str, Any], model_adapter: MockModelAdapter):
        self.request_id = request_id
        self.payload = payload
        self.model_adapter = model_adapter
        self.state = self.PENDING
        self.result: Optional[Dict[str, Any]] = None

    def approve(self) -> Dict[str, Any]:
        """
        Approves sampling request. Invokes model adapter once.
        Raises ValueError if request is not PENDING.
        """
        if self.state != self.PENDING:
            raise ValueError(f"Invalid transition: Request {self.request_id} is already in terminal state '{self.state}'.")

        self.state = self.APPROVED
        sample_output = self.model_adapter.sample(self.payload)
        self.result = {
            "status": "APPROVED",
            "request_id": self.request_id,
            "data": sample_output
        }
        return self.result

    def deny(self, reason: str = "Client consent denied") -> Dict[str, Any]:
        """
        Denies sampling request. Never invokes model adapter.
        Raises ValueError if request is not PENDING.
        """
        if self.state != self.PENDING:
            raise ValueError(f"Invalid transition: Request {self.request_id} is already in terminal state '{self.state}'.")

        self.state = self.DENIED
        self.result = {
            "status": "DENIED",
            "request_id": self.request_id,
            "reason": reason
        }
        return self.result


if __name__ == "__main__":
    adapter = MockModelAdapter()
    req = SamplingConsentRequest("REQ-001", {"email_text": "sample text"}, adapter)
    print("Initial state:", req.state)
    result = req.approve()
    print("Approved result:", result)
    print("Adapter calls:", adapter.call_count)
