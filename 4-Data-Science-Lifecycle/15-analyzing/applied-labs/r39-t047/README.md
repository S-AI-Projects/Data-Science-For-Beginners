# R39-T047: Client-Consent Gate (Worked Example & Checks)

## Overview
This local applied lab extends [The Data Science Lifecycle: Analyzing](../../README.md) with a clear, step-by-step worked example representing a client-side model sampling request as a local state machine.

## Published Worked Input-to-Output Trace
1. **Initialization:** Request created with ID `req_worked_demo`. State: `PENDING`, Model Invocations: `0`.
2. **Consent Approval:** `approve(stub)` called. State transitions `PENDING` $\rightarrow$ `APPROVED` $\rightarrow$ `COMPLETED`. Model stub called exactly `1` time.
3. **Repeated Consent Attempt:** Second `approve(stub)` attempted. Throws `RuntimeError("Request req_worked_demo has already been completed.")`. Model invocations remain strictly `1`.
4. **Denial Scenario:** Separate request denied directly. State transitions to `DENIED`. Model stub is called `0` times.

## Invocation & Output
```bash
python3 4-Data-Science-Lifecycle/15-analyzing/applied-labs/r39-t047/example.py
```
Output:
```json
[
  {
    "step": 1,
    "state": "PENDING",
    "invocations": 0
  },
  {
    "step": 2,
    "state": "COMPLETED",
    "invocations": 1,
    "output": {
      "request_id": "req_worked_demo",
      "state": "COMPLETED",
      "invocations": 1,
      "result": {"status": "success", "feature_sample": [0.12, 0.45, 0.78]}
    }
  },
  {
    "step": 3,
    "state": "COMPLETED",
    "invocations": 1,
    "caught_error": "Request req_worked_demo has already been completed."
  }
]
```

Run tests:
```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/15-analyzing/applied-labs/r39-t047 -p "test_*.py"
```
