# Applied Lab R39-T002: Training-Only Mean Imputation

> **Note:** This is a local, deterministic Python standard-library simulation/fixture. It does not use external datasets, cloud services, GPUs, or a trained ML model.

## How This Illustrates the Lesson
In `08-data-preparation`, handling missing values is a core step before modeling. If imputation statistics are computed across the whole dataset—or refitted separately on validation data—validation observations leak into preprocessing.

`TrainingOnlyMeanImputer` separates `fit()` (which computes the mean from training observations only) from `transform()` (which applies that stored mean to validation observations without refitting):
- Training `[2, None, 4]` fits mean `3.0`.
- Validation `[100, None]` transforms to `[100.0, 3.0]`, not `[100.0, 100.0]`.

### Where Simplifications Stop
This fixture intentionally uses a single 1D Python list with `None` as the missing-value marker so the fit/transform contract is easy to inspect. Unlike a production `pandas.DataFrame` or scikit-learn `Pipeline`, it does not handle multi-column tables, `NaN`/mixed dtypes, or downstream model evaluation.

## Fixture Cases & Exact Boundary Decision
The boundary between valid and invalid training data is **having at least one non-missing (`not None`) training observation**:
- **Smallest valid case:** Train `[2, None, 4]` -> mean `3.0`; validation `[100, None]` -> `[100.0, 3.0]`.
- **Boundary cases:**
  - Train `[None, 5, None]` (exactly 1 observed value) -> valid, mean `5.0`.
  - Validation `[None, None]` or `[]` -> valid, because `transform()` only reuses the stored training mean and never refits (`[None, None]` becomes `[5.0, 5.0]`).
- **Invalid cases:**
  - Train `[None, None]` (all-missing) or `[]` (empty) -> rejected with `ValueError` (no observed sample exists to compute a mean).
  - Calling `transform()` before `fit()` -> rejected with `RuntimeError`.

## Prerequisites & Commands
- **Prerequisites:** Python 3 standard library and a local checkout of this repository.
- **Run the fixture:**
  `python3 2-Working-With-Data/08-data-preparation/applied-labs/r39-t002/example.py`
- **Run the unit tests:**
  `python3 -m unittest discover -s 2-Working-With-Data/08-data-preparation/applied-labs/r39-t002 -p "test_*.py"`
