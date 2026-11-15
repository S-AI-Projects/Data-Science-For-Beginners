# R39-T004: Security-Scenario Rubric (Invariant & State Trace)

## Overview
This local applied lab extends [Data Science in the Cloud: The "Azure ML SDK" way](../../README.md) with a structural rubric checker for three **fictional** security scenarios (`asset`, `threat`, `control`, `residual_risk`) and an explicit **state trace + invariant** check.

- **PASS:** Complete scenario where the control addresses the named threat.
- **FAIL:** Scenario missing an `asset` (or any required field).
- **REVIEW:** Control is unrelated to the named threat (flagged for human review).

## Scope & Limitations
- Uses **fictional local simulation fixtures** and the **Python 3 standard library only**—no Azure subscription, SDK credentials, model downloads, or cloud calls are used.
- Verifies only the stated structural rubric and state-trace invariant; human review is still required to judge explanation quality.

## Invocation & Expected Output

Run the rubric checker:

    python3 5-Data-Science-In-Cloud/19-Azure/applied-labs/r39-t004/example.py

Expected output:

    fictional_complete_pass: verdict=PASS | steps=3 | invariant_ok=True
    fictional_missing_asset_fail: verdict=FAIL | steps=3 | invariant_ok=True
    fictional_unrelated_control_review: verdict=REVIEW | steps=3 | invariant_ok=True

Run the test suite:

    python3 -m unittest discover -s 5-Data-Science-In-Cloud/19-Azure/applied-labs/r39-t004 -p "test_*.py"
