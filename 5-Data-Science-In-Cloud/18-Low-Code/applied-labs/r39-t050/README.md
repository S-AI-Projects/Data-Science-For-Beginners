# R39-T050: Security-Scenario Rubric (Scenario Assessment)

## Overview
This local applied lab extends [Data Science in the Cloud: The "Low code/No code" way](../../README.md) with three fictional security scenarios and three applied assessment questions (predict an output, diagnose a failure, choose a boundary policy) with rationales and executable checks.

## Scenarios & Verdicts
- `fictional_complete_pass`: Complete scenario with OAuth control $\rightarrow$ `PASS`.
- `fictional_missing_asset_fail`: Asset is `None` $\rightarrow$ `FAIL`.
- `fictional_unrelated_control_review`: Timeout adjustment unrelated to data leakage $\rightarrow$ `REVIEW`.

## Three Applied Questions
1. **Predict Output:** Complete valid scenario yields `PASS`. Check: `check_q1_predict_output()`.
2. **Diagnose Failure:** Missing asset triggers immediate structural failure before control relevance. Check: `check_q2_diagnose_failure()`.
3. **Boundary Policy:** Unmapped controls require human `REVIEW`. Check: `check_q3_boundary_policy()`.

## Invocation & Output
```bash
python3 5-Data-Science-In-Cloud/18-Low-Code/applied-labs/r39-t050/example.py
```

Run tests:
```bash
python3 -m unittest discover -s 5-Data-Science-In-Cloud/18-Low-Code/applied-labs/r39-t050 -p "test_*.py"
```
