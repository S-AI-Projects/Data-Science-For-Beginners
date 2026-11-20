# R39-T049: Security-Scenario Rubric (Evaluation Experiment)

## Overview
This local applied lab extends [Defining Data Science](../../README.md) by implementing a structural rubric evaluating three fictional data science security scenarios and executing a controlled performance experiment across three input sizes.

## Structural Rubric Outcomes
- **Complete Passing:** `fictional_complete_pass` evaluates to `PASS`.
- **Missing Asset Failing:** `fictional_missing_asset_fail` evaluates to `FAIL`.
- **Unrelated Control:** `fictional_unrelated_control_review` evaluates to `REVIEW`.

## Controlled Experiment & Trade-off
Compares three batch configurations:
1. `config_single`: 1 scenario (focused single evaluation)
2. `config_triplet`: 3 scenarios (standard suite)
3. `config_batch`: 9 scenarios (triplicate batch)

### Observed Trade-off
- **Correctness:** 100% across all configurations.
- **Latency / Throughput:** Microseconds per item decreases slightly as fixed interpreter overhead amortizes across larger batches.
- **Caveat:** Evaluates purely deterministic local rubric checker efficiency; makes no claim about real-world machine learning model accuracy.

## Invocation & Output
```bash
python3 1-Introduction/01-defining-data-science/applied-labs/r39-t049/example.py
```

Run tests:
```bash
python3 -m unittest discover -s 1-Introduction/01-defining-data-science/applied-labs/r39-t049 -p "test_*.py"
```
