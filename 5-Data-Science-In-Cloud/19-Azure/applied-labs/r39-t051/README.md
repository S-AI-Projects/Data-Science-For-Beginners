# Security Scenario Rubric (R39 T051)

## Overview
This lab extends the Azure ML SDK lesson with a local scenario checker. It checks whether a security scenario has all needed fields and if the chosen control makes sense for the threat.

## The Three Fictional Scenarios
1. Complete scenario passes: Model endpoint with token auth and api keys passes because all fields exist and the control matches the threat.
2. Missing asset scenario fails: If asset is missing or empty, the checker marks it as FAIL.
3. Unrelated control scenario needs review: A cluster node threat paired with an idle shutdown control gets marked as REVIEW because a human reviewer must check it.

## How to Run the Example
Run the script with Python 3:
```bash
python3 5-Data-Science-In-Cloud/19-Azure/applied-labs/r39-t051/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 5-Data-Science-In-Cloud/19-Azure/applied-labs/r39-t051 -p "test_*.py"
```

## Scope and Limitations
This is a small local Python program using simple dictionaries. It does not connect to real Azure services or make live cloud calls.
