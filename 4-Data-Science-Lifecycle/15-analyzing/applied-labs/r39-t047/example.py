"""Client-consent gate worked example with regression checks (R39-T047).

Extends the Data Science Lifecycle: Analyzing lesson. Models a server request
for client-side model sampling as a local state machine with pending/approved/denied
outcomes. Denied consent never calls the model stub; approved consent calls once;
a completed request cannot be approved again.
"""

from __future__ import annotations
from enum import Enum
import json
from typing import Any, Callable, Dict, List, Optional


class RequestState(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    COMPLETED = "COMPLETED"


class ModelSamplingConsentGate:
    """State machine governing model sampling authorization."""

    def __init__(self, request_id: str) -> None:
        self.request_id = request_id
        self.state = RequestState.PENDING
        self.invocations = 0
        self.result: Optional[Dict[str, Any]] = None

    def approve(self, stub: Callable[[str], Dict[str, Any]]) -> Dict[str, Any]:
        """Approve sampling: executes stub exactly once and marks COMPLETED."""
        if self.state == RequestState.COMPLETED:
            raise RuntimeError(f"Request {self.request_id} has already been completed.")
        if self.state == RequestState.DENIED:
            raise RuntimeError(f"Request {self.request_id} was denied and cannot be approved.")

        self.state = RequestState.APPROVED
        self.invocations += 1
        self.result = stub(self.request_id)
        self.state = RequestState.COMPLETED
        return self.to_dict()

    def deny(self) -> Dict[str, Any]:
        """Deny sampling: transitions to DENIED without invoking stub."""
        if self.state in (RequestState.COMPLETED, RequestState.DENIED):
            raise RuntimeError(f"Request {self.request_id} is already finalized.")

        self.state = RequestState.DENIED
        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "state": self.state.value,
            "invocations": self.invocations,
            "result": self.result,
        }


def default_model_stub(req_id: str) -> Dict[str, Any]:
    """Deterministic local client model sampling stub."""
    return {"status": "success", "feature_sample": [0.12, 0.45, 0.78]}


# Published worked input-to-output explanation sequence
WORKED_EXAMPLE_STEPS = [
    {
        "step": 1,
        "action": "initialize",
        "expected_state": "PENDING",
        "expected_invocations": 0,
        "note": "Initial request created in PENDING state; 0 model invocations.",
    },
    {
        "step": 2,
        "action": "approve",
        "expected_state": "COMPLETED",
        "expected_invocations": 1,
        "note": "Client consent granted; stub invoked once; state becomes COMPLETED.",
    },
    {
        "step": 3,
        "action": "approve_again",
        "expected_exception": "already been completed",
        "expected_invocations": 1,
        "note": "Second approval rejected; invocation count remains 1.",
    },
]


def run_worked_example() -> List[Dict[str, Any]]:
    """Execute the exact published worked example and record step outcomes."""
    gate = ModelSamplingConsentGate("req_worked_demo")
    trace = []

    # Step 1: Initial
    trace.append({
        "step": 1,
        "state": gate.state.value,
        "invocations": gate.invocations,
    })

    # Step 2: Approve
    res = gate.approve(default_model_stub)
    trace.append({
        "step": 2,
        "state": gate.state.value,
        "invocations": gate.invocations,
        "output": res,
    })

    # Step 3: Repeated approve attempt
    try:
        gate.approve(default_model_stub)
        error = None
    except RuntimeError as e:
        error = str(e)

    trace.append({
        "step": 3,
        "state": gate.state.value,
        "invocations": gate.invocations,
        "caught_error": error,
    })

    return trace


def main() -> None:
    results = run_worked_example()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
