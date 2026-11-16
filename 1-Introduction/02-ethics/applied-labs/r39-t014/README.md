# Outcome rates with counts and a state trace

This lab applies the [ethics lesson](../../README.md), particularly data quality,
dataset bias and misrepresentation. Showing a rate without its denominator can
hide how little data is available. These fictional groups have the same observed
rate but different sample counts: A has one positive outcome among two, while B
has two among four. Equal rates do not establish fairness or equal uncertainty.
Different rates would not establish causation either.

## Run locally

Prerequisites: Python 3.7+ (standard library only) and a local checkout. Run from
the repository root:

```bash
python3 1-Introduction/02-ethics/applied-labs/r39-t014/example.py
```

The synthetic fixture is A `[1,0]`, B `[1,1,0,0]`. Here 1 simply denotes the
counted outcome; the labels do not describe real people or a trained model.
The local arithmetic is real, with no simulated or mocked service or hardware.

Expected JSON output, wrapped here for readability (the CLI prints one line):

```json
{
  "A": {
    "n": 2, "successes": 1, "rate": 0.5,
    "trace": [
      {"n": 0, "successes": 0, "rate": null},
      {"n": 1, "successes": 1, "rate": 1.0},
      {"n": 2, "successes": 1, "rate": 0.5}
    ]
  },
  "B": {
    "n": 4, "successes": 2, "rate": 0.5,
    "trace": [
      {"n": 0, "successes": 0, "rate": null},
      {"n": 1, "successes": 1, "rate": 1.0},
      {"n": 2, "successes": 2, "rate": 1.0},
      {"n": 3, "successes": 2, "rate": 0.6666666666666666},
      {"n": 4, "successes": 2, "rate": 0.5}
    ]
  }
}
```

## State invariant

The function validates the entire input, records an initial state, then records
a new snapshot after consuming each observation. Nothing is silently dropped.
Each snapshot includes the count `n`, positive count `successes` and prefix rate.
After step `k`:

- `n == k == len(outcomes[:k])`.
- `successes == sum(outcomes[:k])`, with `0 <= successes <= n`.
- When `n > 0`, `rate == successes / n`; otherwise `rate is None`.
- The final report's `n`, `successes` and `rate` equal the last snapshot.

For A, the states are `(0,0,undefined)`, `(1,1,1.0)`, `(2,1,0.5)`.
For B, they are `(0,0,undefined)`, `(1,1,1.0)`, `(2,2,1.0)`,
`(3,2,2/3)`, `(4,2,0.5)`. The trace is an audit of this calculation, not a
time trend or evidence of a causal process. Its length is `len(outcomes) + 1`.
Tests independently reconstruct each prefix from the original inputs and check
the invariant for all 31 binary sequences of lengths zero through four.

## Boundaries and invalid data

Only lists of integer 0 or 1 are accepted. Missing values, strings, floats,
booleans and values outside that set are rejected with `ValueError` in the API.
The CLI exits 2, writes an error to stderr and emits no report. An empty list is
valid: it has no observed rate, represented by Python `None` / JSON `null`.
This differs from `[0]`, which has one observation and a defined rate of 0.0.
The smallest nonempty group is `[0]` or `[1]`.

Run boundary and invalid cases in fresh processes:

```bash
python3 1-Introduction/02-ethics/applied-labs/r39-t014/example.py --a '[]' --b '[0]'
python3 1-Introduction/02-ethics/applied-labs/r39-t014/example.py --a '[2]'
```

The first exits 0: A has n=0, successes=0, rate=null and just its initial
snapshot; B has n=1, successes=0, rate=0.0 and two snapshots. The second exits 2
with `error: outcomes must be a list of integer 0 or 1 values`, after usage text.

```bash
python3 -m unittest discover -s 1-Introduction/02-ethics/applied-labs/r39-t014 -p "test_*.py"
```

Expected: 9 tests, `OK`, exit 0. To demonstrate a failing invariant, temporarily
insert `final["n"] += 1` after `final = dict(trace[-1])` in `example.py` and run
the tests, then restore the file. The final count will disagree with the trace
and original observations, and unittest must exit nonzero.

## Limits

These are descriptive proportions for tiny fictional lists. Counts help expose
the evidence behind a rate but do not quantify uncertainty by themselves. The
example provides no confidence intervals, significance test, sampling design,
causal analysis or fairness verdict. It cannot establish population rates or
trained-model performance, and uses no model, provider, GPU or physical device.
Real group comparisons need context about collection, missingness, selection and
possible alternative explanations.

Practice: explain why replacing an empty group's `null` with 0.0 would change
the meaning of the report even though its positive count remains zero.
