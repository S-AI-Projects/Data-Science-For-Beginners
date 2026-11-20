# R39-T042: Training-Only Mean Imputation (Boundary-Case Extension)

## Overview
This local applied lab extends [Working with Data: Python and the Pandas Library](../../README.md) with a clean fit/transform separation for missing-value imputation.

- **Fit phase:** Computes the mean strictly on observed training values.
- **Transform phase:** Replaces `None` entries in validation data using the stored training mean without recalculating.
- **Leakage prevention:** Prevents information from validation/test sets from leaking into feature transformations.

## Boundary Decisions
1. **Smallest valid input:** A training set with a single observed value (e.g. `[5]`) correctly produces mean `5.0`.
2. **Boundary cases:** Empty validation inputs (`[]`) return `[]`; all-missing validation inputs (`[None, None]`) receive the stored training mean.
3. **Invalid cases:** All-missing training sets (`[None, None]`) or empty training sets (`[]`) are rejected with `ValueError` because no valid statistical mean can be established.

## Invocation & Output
```bash
python3 2-Working-With-Data/07-python/applied-labs/r39-t042/example.py
```
Output:
```json
{"training_mean": 3.0, "validation": [100.0, 3.0]}
```

Run tests:
```bash
python3 -m unittest discover -s 2-Working-With-Data/07-python/applied-labs/r39-t042 -p "test_*.py"
```
