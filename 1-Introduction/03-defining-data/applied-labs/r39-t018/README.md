# Defining data with a failure and recovery example

This lab extends [Defining Data](../../README.md), which introduces data types,
structure and sources. The three fictional records below use its **Structured
Data** and **Sources of Data** sections to discuss how a table, a CSV and an
email source can be described and handled. Each record states an asset, threat,
control and residual risk.

## Run the local examples

Prerequisites: Python 3.7+, its standard library and a local checkout. Run from
the repository root. These are fictional data scenarios and local deterministic
checks; no service is simulated or contacted, and no control is deployed.

```bash
python3 1-Introduction/03-defining-data/applied-labs/r39-t018/example.py
```

Expected default output, exit 0:

```json
{"results": [{"status": "pass", "issues": []}, {"status": "pass", "issues": []}, {"status": "pass", "issues": []}]}
```

The fixture contains:

| ID / lesson section | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| customer-table / Structured Data | Fictional customer table with named columns | `unauthorized_database_read` | `limit_database_access` | An authorized reader could still share an export. |
| sensor-csv / Structured Data | Fictional CSV of hourly sensor readings | `malformed_structured_rows` | `validate_required_columns` | Validly shaped rows may still contain inaccurate readings. |
| email-source / Sources of Data | Fictional email messages used as a data source | `misread_email_metadata` | `preserve_header_fields` | Correctly preserved headers do not prove the body is trustworthy. |

## Failure, then recovery

The first record below is missing `asset`. A missing asset is not an empty string
or a zero value: it means a required piece of scenario information was not
provided. The checker returns `fail` with `missing or invalid: asset`. It still
processes the next record, which supplies the asset and passes. The command exits
1 overall because the sequence contains a failed item, while stdout preserves
both results in order. This demonstrates recovery of processing, not erasure or
correction of the earlier error.

<!-- recovery-command -->
```bash
python3 1-Introduction/03-defining-data/applied-labs/r39-t018/example.py --sequence '[{"threat":"unauthorized_database_read","control":"limit_database_access","residual_risk":"An authorized reader could still share an export."},{"asset":"Fictional customer table with named columns","threat":"unauthorized_database_read","control":"limit_database_access","residual_risk":"An authorized reader could still share an export."}]'
```

<!-- recovery-output -->
```json
{"results": [{"status": "fail", "issues": ["missing or invalid: asset"]}, {"status": "pass", "issues": []}]}
```

Expected exact stdout is the JSON above followed by a newline, stderr is empty,
and exit status is 1. The test suite reads this command and output from this file,
runs the exact argument vector in a fresh process, and compares all three.

The smallest structurally complete object has four nonblank strings. Empty
sequence `[]` is valid and returns no results (exit 0); a sequence that is not a
JSON list or malformed JSON exits 2 with an error and no report. `--case
missing-asset` exercises the same missing field in the standard fixture.

## What the rubric checks

`asset`, `threat`, `control` and `residual_risk` must be nonblank strings. A
missing or invalid required field fails. The exact known threat/control pairs
are listed in the example. A different or unknown pair requests human review;
the checker does not automatically judge it substantively wrong. For a sequence,
each record is checked independently, and later records are processed after
failures. Exit status is 1 if any record fails, 3 if none fail and any need
review, and 0 if all pass. Invalid command input exits 2.

Try the unrelated control case:

```bash
python3 1-Introduction/03-defining-data/applied-labs/r39-t018/example.py --case unrelated-control
```

The first record requests review because `preserve_header_fields` is not the
listed control for `unauthorized_database_read`. A human might discuss broader
uses of this control, but that judgment is not in the rubric. Likewise, the
checker accepts short but nonblank text; it cannot decide if the asset is real,
the control is appropriate in context, or the residual-risk explanation is
convincing. Human review assesses rationale and supporting evidence.

## Checks and scope

```bash
python3 -m unittest discover -s 1-Introduction/03-defining-data/applied-labs/r39-t018 -p "test_*.py"
```

Expected: 10 tests, `OK`, exit 0. To show the regression is meaningful,
temporarily change the final return status in `check_scenario` from `pass` to
`fail`. The documented valid second record will then fail, the regression test
will fail, and unittest exits nonzero. Restore the line afterwards.

These scenarios are fictional examples of discussing structured data and data
sources. They do not simulate a remote service; the checker is local code. It
does not establish security effectiveness, legal compliance, the quality of any
real source, or trained-model performance. Its pass status means only that the
stated structural rubric accepted the record.

Practice: after a missing asset is supplied, what evidence would you still need
before agreeing that the selected control addresses the threat?
