# R39-T043: Client-Consent Gate State Machine

## Overview
This local applied lab extends [The Data Science Lifecycle: Analyzing](../../README.md) by implementing a local state machine that controls client-side model sampling through explicit consent verification.

## Contract & States
- `PENDING`: Initial state waiting for client consent.
- `APPROVED`: Consent granted; triggers the model stub exactly once and transitions to `COMPLETED`.
- `DENIED`: Consent refused; never calls the model stub.
- `COMPLETED`: Terminal state; cannot be approved again.

## Focus: Comparison with Reference Table
The lab compares the state machine's direct execution against an independent, explicit reference table across identical test scenarios:
- Approval transition yields `COMPLETED` and exactly 1 invocation.
- Denial transition yields `DENIED` and 0 invocations.
- Re-approval attempts on completed requests raise `RuntimeError` and preserve invocation count at 1.

## Invocation & Output
```bash
python3 4-Data-Science-Lifecycle/15-analyzing/applied-labs/r39-t043/example.py
```
Output:
```json
{"request_id": "req_001", "state": "COMPLETED", "invocations": 1, "result": {"sample_id": "sample_req_001", "prediction": 0.85}}
```

Run tests:
```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/15-analyzing/applied-labs/r39-t043 -p "test_*.py"
```
