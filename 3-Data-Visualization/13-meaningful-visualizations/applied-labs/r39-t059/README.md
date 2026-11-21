# Chart Data Consistency Scenario Assessment (R39 T059)

## Overview
This lab extends the Making Meaningful Visualizations lesson. In visualization, charts must tell honest visual stories. When categories are filtered, displayed totals must adjust immediately to reflect the new subset.

## The Contract
* Given items ["A", "A", "B", "C", "C", "C"]:
  * Category A = 2
  * Category B = 1
  * Category C = 3
  * Total = 6
* Filtering to A and B:
  * Category A = 2
  * Category B = 1
  * Total = 3

## Three Applied Questions
1. Predict Output: When filtered to categories A and B, the displayed total is predicted to be 3. Checked by check_q1_predict_output.
2. Diagnose Failure: Showing counts [2, 1] with old total 6 fails because the total is stale and does not match the sum of parts. Checked by check_q2_diagnose_failure.
3. Boundary Policy: When displayed totals disagree with category sums, the policy flags the view as inconsistent rather than silently misrepresenting data. Checked by check_q3_boundary_policy.

## How to Run the Example
Run with Python 3:
```bash
python3 3-Data-Visualization/13-meaningful-visualizations/applied-labs/r39-t059/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 3-Data-Visualization/13-meaningful-visualizations/applied-labs/r39-t059 -p "test_*.py"
```

## Scope and Limitations
This is a standard library Python validator that checks numbers before charts are drawn. It does not use browser charting engines or external graphic packages.
