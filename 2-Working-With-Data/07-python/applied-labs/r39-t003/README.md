# R39-T003: Training-Only Mean Imputation (Compare Two Approaches)

## Overview
This local applied lab extends [Working with Data: Python and the Pandas Library](../../README.md) by demonstrating **fit/transform separation** to prevent data leakage during missing-value imputation.

- **Direct implementation:** `TrainingOnlyMeanImputer` fits a mean on training data only and freezes `fill_value_` for validation transforms.
- **Independent comparison:** `independent_reference_impute` (using `statistics.mean`) and `EXPECTED_RESULTS_TABLE` verify identical outputs on the same local fixtures.

## Scope & Limitations
- Uses **small local Python list fixtures** (`None` for missing values) and the **Python 3 standard library only**—no `pandas`, `numpy`, model downloads, GPUs, or cloud services are required.
- Simplifies real-world tabular pipelines to a 1D numeric sequence; it does not handle multi-column DataFrames, `float('nan')`, or downstream model performance evaluation.

## Invocation & Expected Output

Run the comparison script:

    python3 2-Working-With-Data/07-python/applied-labs/r39-t003/example.py

Expected output for the primary local fixture (`train=[2, None, 4]`, `validation=[100, None]`):

    leakage_guard_primary_fixture: mean=3.0 (ref=3.0, expected=3.0) -> val=[100.0, 3.0] | match=True

Run the test suite:

    python3 -m unittest discover -s 2-Working-With-Data/07-python/applied-labs/r39-t003 -p "test_*.py"
