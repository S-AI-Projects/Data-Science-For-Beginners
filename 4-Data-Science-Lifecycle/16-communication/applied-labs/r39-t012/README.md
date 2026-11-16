# Local category summary: labels, counts and total

This exercise applies the [communication lesson](../../README.md): precise labels
and a clearly stated filter help an audience interpret a report. Pairing labels
with counts prevents a label/value ordering mismatch. Recomputing the total after
filtering prevents a subset from being presented with the full dataset's total.
Filtering here is an explicit demonstration, not evidence that omitted categories
are unimportant; disclose the filter when communicating the result.

## Run locally

Prerequisites: Python 3.7+ (standard library only) and a local checkout. Run from
the repository root. The synthetic local fixture is `A,A,B,C,C,C`; no service,
model, GPU, credentials or physical device is used. The aggregation is real local
code, not mocked service behavior. This is not a population study, visualization,
data-cleaning pipeline or claim about trained-model performance.

```bash
python3 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012/example.py
python3 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012/example.py --include '["A","B"]'
```

Expected output, respectively:

```json
{"counts": {"A": 2, "B": 1, "C": 3}, "total": 6}
{"counts": {"A": 2, "B": 1}, "total": 3}
```

## Exact boundary decision

Inputs are JSON lists of nonblank strings. Each row contributes one count.
Labels are case-sensitive and preserved exactly, including surrounding spaces;
no trimming or merging occurs. Output keys are sorted by label, and categories
with no retained rows are omitted. Duplicate filter labels do not duplicate rows.
The API's `include=None` (CLI: omit `--include`) means all rows; `include=[]`
means no rows. Unknown filter labels match nothing, rather than inventing a zero
count category. All rows are validated **before** filtering.

The empty list is a valid dataset: no observations means no categories and total
zero. The smallest **nonempty** valid fixture is one nonblank label. This places
the boundary between an empty collection (valid) and an empty category label
(invalid), rather than between zero and one observations. Invalid rows raise
`ValueError`; the CLI reports an error on stderr and exits 2 without a report.

| Case | Rows | Include | Expected counts; total |
| --- | --- | --- | --- |
| Normal | `["A","A","B","C","C","C"]` | omitted | `A=2,B=1,C=3; 6` |
| Filtered | same | `["A","B"]` | `A=2,B=1; 3` |
| Smallest nonempty | `["A"]` | omitted | `A=1; 1` |
| Empty data boundary | `[]` | omitted | `{}; 0` |
| Empty filter boundary | `["A"]` | `[]` | `{}; 0` |
| No matches | same normal fixture | `["Z"]` | `{}; 0` |
| Invalid label | `[""]`, `[" "]`, `[null]`, or `[1]` | any | error |
| Invalid container | `null` or `"A"` | omitted | error |
| Hidden invalid row | `["A",""]` | `["A"]` | error |

Try the boundaries and failure in separate processes:

```bash
python3 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012/example.py --rows '["A"]'
python3 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012/example.py --rows '[]'
python3 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012/example.py --include '[]'
python3 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012/example.py --rows '[""]'
```

The first three exit 0 and return the table's reports. The last exits 2 with
`error: rows must be a list of nonblank strings` (after argparse's usage text).
An explicit CLI `--include 'null'` is also invalid; omit the flag for no filter.

## Checks

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012 -p "test_*.py"
```

Expected: 9 tests, `OK`, exit 0. Tests compare complete label/count mappings and
totals against literal expectations, including fresh-process CLI runs. Unittest
exits nonzero if an assertion fails. To see this, temporarily change the expected
filtered total from 3 to 6 in `test_example.py`, rerun, and restore it. The test
must fail: a displayed subset cannot retain the unfiltered total.

Practice: before applying the A/B filter, predict which labels disappear and
explain why showing total 6 beside A=2 and B=1 would mislead the audience.
