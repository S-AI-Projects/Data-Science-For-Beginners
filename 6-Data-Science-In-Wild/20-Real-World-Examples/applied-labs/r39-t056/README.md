# Security Scenario Rubric and Refactoring (R39 T056)

## Overview
This lab extends the Data Science in the Real World lesson. It demonstrates checking security scenarios across healthcare, agriculture, and finance use cases, while showing how to refactor monolithic code into clean modular components.

## The Contract and Scenarios
* Complete scenario passes: Hospital patient records protected by encryption and access control passes rubric checks.
* Missing asset fails: Farm sensor scenario missing the asset field is marked as FAIL.
* Unrelated control needs review: Model tampering threat paired with changing color themes gets marked as REVIEW.
* Human review judges explanations while the automated checker verifies structural completeness.

## Refactoring the Teaching Example
We first build a monolithic baseline function that combines field checks with keyword matching. Then we extract the alignment validation into a dedicated class named ControlAlignmentValidator. We run tests to prove both versions produce identical outputs across all test cases.

## How to Run the Example
Run with Python 3:
```bash
python3 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t056/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t056 -p "test_*.py"
```

## Scope and Limitations
This is a local Python educational example. It does not use live enterprise infrastructure, real patient records, or remote API endpoints.
