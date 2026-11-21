# Chart Data Consistency Worked Example (R39 T057)

## Overview
This lab extends the Data Science Lifecycle Communication lesson. In data communication, presenting a chart with numbers that do not add up to the displayed total can confuse or mislead people. This lab shows how to verify that labels, counts, and displayed totals refer to the exact same filtered data.

## The Problem and Contract
* Input rows: ["A", "A", "B", "C", "C", "C"]
* Unfiltered result: A=2, B=1, C=3, and displayed total is 6.
* Filtered result for A and B: A=2, B=1, and displayed total is 3.
* If a dashboard filters to A and B but mistakenly shows the old total 6, the consistency validator flags it as inconsistent.

## Worked Input to Output Explanation
1. Step 1: Count raw observations for each distinct label.
2. Step 2: Sum the individual counts to compute the actual total.
3. Step 3: Compare the calculated sum with the displayed total.
4. Step 4: When a filter is chosen, recompute both the counts and the total simultaneously so that proportions remain truthful.

## How to Run the Example
Run with Python 3:
```bash
python3 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t057/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t057 -p "test_*.py"
```

## Scope and Limitations
This is a standard library Python validator that checks numbers before plotting. It does not require charting libraries like Matplotlib or web rendering engines.
