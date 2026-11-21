# Group Metric Comparison (R39 T053)

## Overview
This lab extends the data ethics lesson by showing how to compare outcome rates across different groups without jumping to false conclusions about causation.

## The Contract
* Group A has outcomes [1, 0] with sample size 2 and rate 0.5.
* Group B has outcomes [1, 1, 0, 0] with sample size 4 and rate 0.5.
* Both groups have the exact same rate of 0.5, but different sample sizes n.
* An empty group [] is undefined (represented by None), not a rate of 0.
* We explicitly avoid inferring causation between observed differences.

## Comparing Two Approaches
We implement the rate calculation using a direct function and also cross check it against an independent manual accumulation function. Both produce identical outputs on all test inputs.

## How to Run the Example
Run with Python 3:
```bash
python3 1-Introduction/02-ethics/applied-labs/r39-t053/example.py
```

## How to Run Tests
Run the unit test discovery command:
```bash
python3 -m unittest discover -s 1-Introduction/02-ethics/applied-labs/r39-t053 -p "test_*.py"
```

## Scope and Limitations
This is a local Python script for learning statistical fairness concepts. It does not use external libraries or real world demographic databases.
