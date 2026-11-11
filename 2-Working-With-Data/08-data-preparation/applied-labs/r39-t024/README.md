# Applied Lab R39-T024: Training-Only Mean Imputation

## Overview
This applied lab extends the "Working with Data: Data Preparation" lesson by enforcing strict separation between training parameter estimation (`fit`) and inference/validation application (`transform`), preventing data leakage.

## Focus: State Tracing & Invariance
- Imputer calculates and caches the arithmetic mean of observed training values.
- Cached mean is applied to validation records without refitting.
- Records intermediate operation traces to audit state transitions.
- Disallows all-missing training datasets.

## Fixtures & Invariants
- **Training Input:** `[2, None, 4]` &rarr; Stored mean = `3.0`
- **Validation Input:** `[100, None]` &rarr; Transformed to `[100, 3.0]` (never `[100, 100]`)
- **All-Missing Input:** `[None, None]` &rarr; Raises `ValueError`

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 2-Working-With-Data/08-data-preparation/applied-labs/r39-t024 -p "test_*.py" -v
```

## Scope & Limitations
This lab demonstrates deterministic standard-library missing value imputation without external libraries like scikit-learn or pandas.
