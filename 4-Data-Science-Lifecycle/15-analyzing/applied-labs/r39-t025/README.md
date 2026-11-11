# Applied Lab R39-T025: Client-Consent State Machine

## Overview
This applied lab extends the "The Data Science Lifecycle: Analyzing" lesson by modeling privacy-preserving client-side sampling. It implements a local finite state machine to gate model sampling behind explicit user consent.

## Invariants & State Transitions
- **Initial State:** `PENDING`
- **Approved Transition:** `PENDING` &rarr; `APPROVED` (triggers model adapter invocation exactly once).
- **Denied Transition:** `PENDING` &rarr; `DENIED` (guarantees zero adapter invocations).
- **Terminal State Lock:** Once in `APPROVED` or `DENIED`, subsequent transition requests are rejected.

## Mock Limitations & Real-Service Scope
The local adapter (`MockModelAdapter`) provides deterministic responses without external services. It deliberately does **not** model:
- Network round-trip latency, timeouts, or transient network retries.
- Remote server authentication tokens, OAuth scopes, or TLS handshake.
- Distributed consensus or multi-tenant database concurrency.
- Real hardware/GPU memory bottlenecks during inference.

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/15-analyzing/applied-labs/r39-t025 -p "test_*.py" -v
```
