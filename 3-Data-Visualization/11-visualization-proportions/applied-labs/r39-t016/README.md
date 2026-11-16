# Normalize counts before visualizing proportions

The [proportions lesson](../../README.md) groups mushroom observations into
categories and stresses keeping labels in the right order. This local example
makes the denominator explicit before drawing a chart, and shows a small
refactor that leaves the result unchanged. It uses synthetic category counts,
not the mushroom dataset.

## Run locally

Prerequisites: Python 3.7+ (standard library only) and a checkout. No Pandas,
Matplotlib, PyWaffle, model download, provider, GPU or device is needed. From the
repository root:

```bash
python3 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016/example.py
```

The local fixture is `{"A":2,"B":3}`. Expected output, exit 0:

```json
{"status": "ok", "count_total": 5, "proportions": {"A": 0.4, "B": 0.6}, "total": 1.0}
```

The denominator is `2+3=5`, so A is `2/5=0.4` and B is `3/5=0.6`.
`count_total` counts observations; `total` sums the resulting proportions.
Labels remain paired with their values and are sorted in the output.

## Baseline, then extract one responsibility

The first implementation kept validation inside `proportions`. It was run and
tested before the refactor. The final implementation moves only that validation
into **`validate_counts`**. It checks the container, labels and counts before
normalization. The denominator, zero-total decision, output shape, exception type
and error messages remain unchanged.

`baseline_proportions` in `test_example.py` preserves the original inline
implementation without calling the extracted helper. Tests run the same inputs
through both versions and compare their full results with literal expectations:

| Counts | Expected status | Count total | Proportions | Proportion total |
| --- | --- | --- | --- | --- |
| `A=2,B=3` | `ok` | 5 | `A=0.4,B=0.6` | 1.0 |
| `A=1` | `ok` | 1 | `A=1.0` | 1.0 |
| `A=0,B=3` | `ok` | 3 | `A=0.0,B=1.0` | 1.0 |
| `A=0,B=0` | `no-data` | 0 | `{}` | `null` |
| empty object | `no-data` | 0 | `{}` | `null` |

For invalid inputs both versions must raise `ValueError` with the same message.
This is a behavior-preserving extraction, not a claim about faster execution.
Tests also compare thirds with a floating-point tolerance rather than rounding
each share prematurely; `math.fsum` computes the displayed proportion total.

## Zero-total policy and invalid counts

Counts must be nonnegative integers with nonblank string labels. Floats,
booleans, strings and missing values such as `None` are rejected. Missing counts
are not silently replaced with zero. Labels retain their spelling and case.

The smallest positive dataset is one category with count 1. Empty and all-zero
objects are valid inputs but contain no observations to normalize: `0/0` is
undefined. They return `no-data`, an empty proportion object and `total: null`,
not a chart of zero shares or a made-up total of 1. A zero count is a defined
share of 0 only when at least one other count makes the denominator positive.

Run boundary and failure cases in fresh processes:

```bash
python3 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016/example.py --counts '{"A":0,"B":0}'
python3 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016/example.py --counts '{"A":-1,"B":3}'
```

The first exits 0 with:

```json
{"status": "no-data", "count_total": 0, "proportions": {}, "total": null}
```

The second exits 2, prints no report, and ends stderr's usage message with
`error: counts must be nonnegative integers`. Malformed JSON also exits 2.

## Checks and limits

```bash
python3 -m unittest discover -s 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016 -p "test_*.py"
```

Expected: 9 tests, `OK`, exit 0. To prove a wrong result fails, temporarily change
the normalization denominator from `count_total` to `(count_total + 1)`, rerun
the tests, then restore it. The fixture would yield 2/6 and 3/6, violating both
the expected values and before/after equivalence. Unittest must exit nonzero.

This is real arithmetic on synthetic data, with no simulation or mocked service.
It does not render a chart, establish that a dataset covers all categories, handle
weighted counts, choose a missing-data strategy, or claim population proportions
or trained-model performance. Chart selection and data quality still need context.

Practice: explain why `A=0,B=3` can include A=0.0, but `A=0,B=0` cannot be
normalized under this policy.
