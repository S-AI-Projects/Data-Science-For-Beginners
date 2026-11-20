"""Client-consent gate state machine for model sampling (R39-T043).

Extends the Data Science Lifecycle: Analyzing lesson. Models a server request
for client-side model sampling as a local state machine with pending/approved/denied
outcomes. Denied consent never calls the model stub; approved consent calls once;
a completed request cannot be approved again.
"""

from __future__ import annotations
from enum import Enum
import json
from typing import Any, Callable, Dict, List, Optional


class ConsentState(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    COMPLETED = "COMPLETED"


class ModelSamplingRequest:
    """State machine governing client consent and model sampling invocation."""

    def __init__(self, request_id: str) -> None:
        self.request_id = request_id
        self.state = ConsentState.PENDING
        self.sample_result: Optional[Dict[str, Any]] = None
        self.invocation_count = 0

    def approve(self, model_stub: Callable[[str], Dict[str, Any]]) -> Dict[str, Any]:
        """Approve sampling: transitions through APPROVED to COMPLETED and calls stub once."""
        if self.state == ConsentState.COMPLETED:
            raise RuntimeError(f"Request {self.request_id} is already completed and cannot be approved again.")
        if self.state == ConsentState.DENIED:
            raise RuntimeError(f"Request {self.request_id} has been denied and cannot be approved.")

        self.state = ConsentState.APPROVED
        self.invocation_count += 1
        self.sample_result = model_stub(self.request_id)
        self.state = ConsentState.COMPLETED
        return {
            "request_id": self.request_id,
            "state": self.state.value,
            "invocations": self.invocation_count,
            "result": self.sample_result,
        }

    def deny(self) -> Dict[str, Any]:
        """Deny consent: transitions to DENIED without calling the model stub."""
        if self.state in (ConsentState.COMPLETED, ConsentState.DENIED):
            raise RuntimeError(f"Request {self.request_id} cannot be denied from state {self.state.value}.")

        self.state = ConsentState.DENIED
        return {
            "request_id": self.request_id,
            "state": self.state.value,
            "invocations": self.invocation_count,
            "result": None,
        }


def mock_model_stub(request_id: str) -> Dict[str, Any]:
    """Deterministic local model sampling stub."""
    return {"sample_id": f"sample_{request_id}", "prediction": 0.85}


# Explicit reference table of expected outcomes for identical inputs
REFERENCE_OUTCOMES_TABLE = [
    {
        "case": "approval_flow",
        "action": "approve",
        "expected_state": "COMPLETED",
        "expected_invocations": 1,
        "sample_generated": True,
    },
    {
        "case": "denial_flow",
        "action": "deny",
        "expected_state": "DENIED",
        "expected_invocations": 0,
        "sample_generated": False,
    },
    {
        "case": "repeat_approval",
        "action": "approve_again",
        "expected_error": "already completed",
        "expected_invocations": 1,
    },
]


def main() -> None:
    req = ModelSamplingRequest("req_001")
    res = req.approve(mock_model_stub)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
