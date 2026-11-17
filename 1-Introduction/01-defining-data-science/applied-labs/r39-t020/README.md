# Scenario rubric and three applied questions

This lab extends [Defining Data Science](../../README.md), which introduces
data sources, the data journey, and using data to develop useful insights. Its
three fictional scenarios borrow from **Digitalization and Digital
Transformation**, **Data Processing**, and **Internet of Things**. Each lists an
asset, threat, control and residual risk. A small structural rubric checks that
the fields are present and that the threat/control labels are a listed pair.

## Run the fixture

Prerequisites: Python 3.7+, its standard library and a local checkout. Run from
the repository root:

```bash
python3 1-Introduction/01-defining-data-science/applied-labs/r39-t020/example.py
```

The three fictional scenarios are:

| ID / lesson section | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| course-survey / Digitalization and Digital Transformation | Course feedback survey responses | `unclear_survey_provenance` | `record_source_and_consent` | A respondent may still misunderstand how answers are used. |
| site-logs / What you can do with Data: Data Processing | Web server logs for a page-usage summary | `malformed_web_logs` | `validate_log_fields` | Well-formed logs may still record incorrect events. |
| room-sensors / Where to get Data: Internet of Things | Room temperature readings from sensors | `unauthorized_sensor_data_access` | `limit_data_access` | An authorized user could still share an export. |

Expected default output, exit 0:

```json
{"results": [{"status": "pass", "issues": []}, {"status": "pass", "issues": []}, {"status": "pass", "issues": []}]}
```

## Applied questions

Each question has a command that evaluates its local input and a test that
checks the factual result. The rationale explains the rubric decision.

### 1. Predict the output

**Question:** What result does a complete course-survey scenario receive?

```bash
python3 1-Introduction/01-defining-data-science/applied-labs/r39-t020/example.py --question predict
```

Expected result: `pass`, exit 0. All four fields are nonblank, and
`unclear_survey_provenance` pairs with `record_source_and_consent` in the local
rubric. `test_question_predicts_complete_scenario` checks the answer by running
the same scenario through `check_scenario` and comparing the literal expected
status and issue list.

### 2. Diagnose a failure

**Question:** What fails when that scenario omits `asset`?

```bash
python3 1-Introduction/01-defining-data-science/applied-labs/r39-t020/example.py --question diagnose
```

Expected result: `fail`, issue `missing or invalid: asset`, exit 1. The asset
names what is at risk; without it the structural answer is incomplete.
`test_question_diagnoses_missing_asset` executes the scenario and checks that
exact issue.

### 3. Choose a boundary policy

**Question:** How should a complete scenario with an unlisted threat/control
pair be handled?

```bash
python3 1-Introduction/01-defining-data-science/applied-labs/r39-t020/example.py --question boundary
```

Expected result: `review`, issue `unlisted threat/control pair`, exit 3. The
fields are present, but the rubric cannot establish whether a new pair is
appropriate. Human review is preferable to silently passing it or declaring its
explanation substantively wrong. `test_question_chooses_review_at_unknown_pair_boundary`
checks this answer against the actual local checker.

## Rubric, limits and checks

All required fields must be nonblank strings. The three exact pairs in
`PAIRS` pass when complete. Missing or invalid fields fail; an unlisted pair
requests review. Short, vague text can pass, so the checker does not assess
whether evidence supports the explanation, the control will work, or the
residual risk is acceptable. Human review makes those judgments.

These are fictional scenarios evaluated by deterministic local Python code.
They do not simulate a remote service, deploy a control, train a model or claim
real-world performance. The examples simplify data science to a few fields and
one threat/control pair per scenario.

```bash
python3 -m unittest discover -s 1-Introduction/01-defining-data-science/applied-labs/r39-t020 -p "test_*.py"
```

Expected: 12 tests, `OK`, exit 0. Tests run all three questions in fresh
processes. To demonstrate a wrong factual answer, temporarily change the
successful return in `check_scenario` from `pass` to `review`, run the suite,
then restore it. The prediction test and complete-scenario test should fail, and
unittest exits nonzero.

Practice: name evidence you would request before agreeing that the survey's
consent control addresses the stated threat.
