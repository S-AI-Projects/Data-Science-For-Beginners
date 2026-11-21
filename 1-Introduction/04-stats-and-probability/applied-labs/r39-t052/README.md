# Histogram Boundary Accounting (R39 T052)

## Overview
This lab extends the statistics and probability lesson by demonstrating how to put values into bins correctly.
The first bins are left closed and right open. The final bin includes both edges so the highest boundary value is not lost.

## The Problem and Contract
* Given bins [0, 10, 20] and numbers [0, 9, 10, 20]:
  * 0 and 9 belong to the first bin [0, 10)
  * 10 and 20 belong to the second bin [10, 20]
  * Result counts are [2, 2]
* Numbers below 0 or above 20 are collected into separate lists.

## Failure and Recovery
When missing data like None appears in the input list, the program raises a ValueError. On the next call with clean valid numbers, the function recovers immediately and gives the right counts.

## How to Run the Example
Run the script with Python 3:
```bash
python3 1-Introduction/04-stats-and-probability/applied-labs/r39-t052/example.py
```

## How to Run Tests
Run the unit test command:
```bash
python3 -m unittest discover -s 1-Introduction/04-stats-and-probability/applied-labs/r39-t052 -p "test_*.py"
```

## Scope and Limitations
This is a simple pure Python example. It runs on the local computer and does not require third party libraries like NumPy or pandas.
