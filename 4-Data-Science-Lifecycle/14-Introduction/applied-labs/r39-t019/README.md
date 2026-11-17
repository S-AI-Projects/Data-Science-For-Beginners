# Check lifecycle scenarios at three input sizes

The [lifecycle introduction](../../README.md) describes capturing, processing
and maintenance. This lab uses one fictional scenario from each stage and checks
its asset, threat, control and residual risk. It focuses on a narrow structural
rubric: complete fields and a listed threat/control pair. Human review still
judges explanations, evidence and whether a control makes sense in context.

## Run the local fixture

Prerequisites: Python 3.7+, its standard library and a local checkout. Run from
the repository root:

```bash
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019/example.py
```

The three fictional scenarios are:

| ID / section | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| capturing-survey / Capturing | Community survey records | `unclear_data_origin` | `record_source_and_provenance` | Recorded provenance may still be incomplete or incorrect. |
| processing-import / Processing | CSV for a monthly summary | `malformed_records` | `validate_input_schema` | Well-formed rows may still contain inaccurate values. |
| maintenance-table / Maintaining / Managing Data | Shared project table | `unauthorized_edits` | `restrict_data_writers` | An authorized writer could still make an erroneous change. |

Expected result fields for all three scenarios:

```json
{"results": [{"status": "pass", "issues": [], "field_checks": 4}, {"status": "pass", "issues": [], "field_checks": 4}, {"status": "pass", "issues": [], "field_checks": 4}], "size_comparison": [{"scenarios": 1, "expected_statuses": ["pass"], "actual_statuses": ["pass"], "required_field_checks": 4, "correct": true}, {"scenarios": 2, "expected_statuses": ["pass", "pass"], "actual_statuses": ["pass", "pass"], "required_field_checks": 8, "correct": true}, {"scenarios": 3, "expected_statuses": ["pass", "pass", "pass"], "actual_statuses": ["pass", "pass", "pass"], "required_field_checks": 12, "correct": true}]}
```

## Three controlled sizes and observed trade-off

`compare_sizes` takes prefixes of the same fixture: the first 1, first 2, and
all 3 scenarios. The expected status is `pass` for each included scenario.
Correctness means the actual status list exactly matches that expectation.
The work metric is the count of required-field slots checked: four required
fields per scenario. It is a deterministic proxy for rubric work, not elapsed
time, cost, throughput or model accuracy.

| Input size | Expected / actual statuses | Correct | Required-field checks |
| ---: | --- | --- | ---: |
| 1 scenario | `[pass]` / `[pass]` | yes | 4 |
| 2 scenarios | `[pass,pass]` / `[pass,pass]` | yes | 8 |
| 3 scenarios | `[pass,pass,pass]` / `[pass,pass,pass]` | yes | 12 |

For this fixture, correctness stays the same at all three sizes; the counted
field checks grow by four for each added scenario. This follows directly from
the fixed four-field contract, not from a measured timing experiment. It says
nothing about accuracy on real data, model performance, or actual security.

## Failures, review and boundaries

Every required field must be a nonblank string. Missing `asset` returns
`fail`; the exact threat/control pairs are listed in `PAIRS`. An unrelated or
unknown pair returns `review`, leaving its explanation for a person to assess.
The checker accepts short but nonblank text; it does not assess the truth or
quality of an explanation. A non-object scenario fails. Empty input to the
comparison function produces no size rows. The smallest nonempty comparison has
one scenario and four field checks.

```bash
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019/example.py --case missing-asset
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019/example.py --case unrelated-control
```

The first command exits 1 and marks the first scenario `fail` with
`missing or invalid: asset`. The second exits 3 and marks it `review` with
`unlisted threat/control pair`. Other fixture scenarios pass in each report.

These are fictional local inputs and deterministic Python checks; there is no
simulated or mocked service, deployed control, model, provider or hardware. This
example does not establish whether a control is effective or whether the
scenario explanation is supported. Human review is needed for that judgment.

## Checks

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019 -p "test_*.py"
```

Expected: 9 tests, `OK`, exit 0. The tests compare all three configurations to
literal expected results. To demonstrate a wrong result, temporarily change
the `pass` status in `check_scenario` to `review`, rerun the tests, then restore
it. The complete-scenario and size-comparison checks must fail, and unittest
must exit nonzero.

Practice: identify what evidence you would want before deciding that one listed
control addresses the threat in a real project.
