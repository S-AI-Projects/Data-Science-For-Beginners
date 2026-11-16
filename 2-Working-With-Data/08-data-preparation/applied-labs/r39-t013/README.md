# Fit on training data, fill validation data

This local exercise extends the [data preparation lesson](../../README.md).
The lesson describes detecting, dropping and filling missing values. Here the
replacement value is learned from training observations only, then stored and
reused for validation. Learning it from validation observations would let held-out
data influence preprocessing: a form of data leakage.

## Run the fixture

You need Python 3.7+ and a local checkout. Only the standard library is used;
Pandas and scikit-learn are not required for this lab. From the repository root:

```bash
python3 2-Working-With-Data/08-data-preparation/applied-labs/r39-t013/example.py
```

The synthetic local fixture is training `[2, None, 4]`, validation `[100, None]`.
Expected output (JSON uses `null` for Python's `None` in input arguments):

```json
{"training_mean": 3.0, "validation": [100, 3.0]}
```

The same fixture can be supplied explicitly:

```bash
python3 2-Working-With-Data/08-data-preparation/applied-labs/r39-t013/example.py --training '[2,null,4]' --validation '[100,null]'
```

## Compare the implementation with a calculation by hand

`fit_mean` collects observed training values and divides their sum by their
count. `transform` receives that stored scalar and fills only missing entries;
it never calls `fit_mean`. The independent check below uses explicit arithmetic
and expected results for the **same inputs**, rather than calling the production
functions to generate an answer. `test_example.py` checks this table both through
the functions and through fresh CLI processes.

| Training | Validation | Independent training calculation | Expected validation |
| --- | --- | --- | --- |
| `[2,None,4]` | `[100,None]` | `(2+4)/2 = 3` | `[100,3]` |
| `[2,None,4]` | `[-100,None]` | `(2+4)/2 = 3` | `[-100,3]` |
| `[7]` | `[None]` | `7/1 = 7` | `[7]` |
| `[None,0]` | `[None,8]` | `0/1 = 0` | `[0,8]` |
| `[-2,None,4]` | `[None,-9]` | `(-2+4)/2 = 1` | `[1,-9]` |
| `[1,2]` | `[None]` | `(1+2)/2 = 1.5` | `[1.5]` |
| `[2,None,4]` | `[]` | `(2+4)/2 = 3` | `[]` |
| `[2,None,4]` | `[None,None]` | `(2+4)/2 = 3` | `[3,3]` |
| `[2,None,4]` | `[100,200]` | `(2+4)/2 = 3` | `[100,200]` |

Refitting on the observed validation value would give `100/1 = 100` and
`[100,100]`. That is the deliberately wrong answer for the first row. Changing
validation from 100 to -100 must not change the stored training mean of 3.
Combining training and validation when fitting would also violate this contract.

## Boundaries and invalid inputs

One observed training value is sufficient, including zero. An empty training
list or an all-missing training list is rejected: there is no observed value to
average, so the example does not invent a fallback. Empty validation is valid;
all-missing validation is filled entirely with the stored training mean.

Inputs are lists of finite Python integers/floats or `None`. Booleans, strings,
NaN and infinity are rejected. Only `None` means missing; this intentionally
differs from Pandas' wider missing-value conventions. Arithmetic must produce a
finite mean in Python's numeric range. Input lists are not modified.

Run a boundary and failure case in separate processes:

```bash
python3 2-Working-With-Data/08-data-preparation/applied-labs/r39-t013/example.py --training '[7]' --validation '[null]'
python3 2-Working-With-Data/08-data-preparation/applied-labs/r39-t013/example.py --training '[null,null]'
```

The first exits 0 with `{"training_mean": 7.0, "validation": [7.0]}`.
The second exits 2, prints no report, and ends its stderr usage message with
`error: training must contain at least one observed value`.

## Checks and scope

```bash
python3 -m unittest discover -s 2-Working-With-Data/08-data-preparation/applied-labs/r39-t013 -p "test_*.py"
```

Expected: 9 tests, `OK`, exit 0. An assertion failure exits nonzero. To try a
deliberately wrong expectation, temporarily change the first table result in
`test_example.py` from `[100,3]` to `[100,100]`, run the tests, then restore it.

This is real local preprocessing on synthetic observations, with no simulated
or mocked service. There is no model training, provider, download, GPU or device.
It demonstrates separation of fitting and transformation for one numeric feature;
it does not choose a train/validation split, justify mean imputation for a real
missingness mechanism, handle categorical data, or establish model accuracy.

Practice: explain why validation `[None,None]` can be transformed while training
`[None,None]` cannot be fitted.
