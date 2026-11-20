# R39-T044: Security-Scenario Rubric (Invariant and State Trace)

## Overview
This local applied lab extends [Data Science in the Cloud: The "Low code/No code" way](../../README.md) with a structural rubric evaluating three fictional security scenarios (`asset`, `threat`, `control`, `residual_risk`).

- **PASS:** Complete scenario where control corresponds to the threat.
- **FAIL:** Scenario missing `asset` (or other required field).
- **REVIEW:** Control is unrelated to the named threat.

## State Trace & Invariant
The rubric records each evaluation step into an explicit `state_trace` list. `verify_state_trace_invariant` rigorously proves that the final verdict strictly derives from the recorded step states.

## Invocation & Output
```bash
python3 5-Data-Science-In-Cloud/18-Low-Code/applied-labs/r39-t044/example.py
```
Output:
```text
fictional_complete_pass: verdict=PASS | steps=3 | invariant_ok=True
fictional_missing_asset_fail: verdict=FAIL | steps=1 | invariant_ok=True
fictional_unrelated_control_review: verdict=REVIEW | steps=2 | invariant_ok=True
```

Run tests:
```bash
python3 -m unittest discover -s 5-Data-Science-In-Cloud/18-Low-Code/applied-labs/r39-t044 -p "test_*.py"
```
