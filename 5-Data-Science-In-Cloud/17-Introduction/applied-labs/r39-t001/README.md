
# Cloud Security Scenario Checker

## Overview

This project is a small Python-based educational example that demonstrates a structural rubric for evaluating fictional cloud-security scenarios.

It checks whether each scenario contains the required information and whether the stated security control appears to address the named threat.

The example uses three fictional scenarios:

1. Cloud customer database
2. Cloud data processing
3. Real-time sentiment analysis

## Features

- Checks whether the asset, threat, control, and residual-risk fields are present and non-empty.
- Returns `PASS` when the required fields are complete and the threat and control categories match.
- Returns `FAIL` when one or more required fields are missing or empty.
- Returns `REVIEW` when the control may not address the named threat.
- Displays the results in JSON format.

## Requirements

- Python 3.7 or later
- Python standard library only

No external services, cloud accounts, machine-learning models, or GPU are required.

## Project Files

- `example.py` – Contains the fictional scenarios and evaluation logic.
- `test_example.py` – Contains automated unit tests.
- `README.md` – Explains the project and how to run it.

## How to Run

Open a terminal in this directory and execute:

```bash
python3 example.py
```

The program prints the evaluation results in JSON format.

## How to Run Tests

Execute:

```bash
python3 -m unittest -v test_example.py
```

The tests check complete scenarios, missing required fields, and potentially unrelated controls.

## Expected Results

| Scenario | Expected Status | Reason |
|---|---|---|
| Cloud customer database | PASS | Required fields are complete and the control matches the threat category. |
| Cloud data processing | FAIL | The asset field is missing. |
| Real-time sentiment analysis | REVIEW | Encryption of stored data may not address exposed API credentials. |

## Limitations

This is a simplified educational demonstration. It uses predefined keyword categories and does not perform a real security assessment.

A `PASS` result does not guarantee that a cloud environment is secure. A `REVIEW` result requires human judgement to determine whether the control is appropriate.

The checker evaluates only the stated structural rubric and does not connect to or assess real cloud infrastructure.
