# Histogram Boundary Accounting Evaluation Experiment (R39 T058)

## Overview
This lab extends the statistics and probability lesson by running an evaluation experiment across different bin configurations and input sizes. It shows how boundary decisions affect counts and in range proportions.

## The Contract
* Bins [0, 10, 20] with values [0, 9, 10, 20] produce counts [2, 2].
* Values lower than 0 or higher than 20 are reported in separate lists.
* Final bin [10, 20] is right inclusive so that 20 is counted.

## Controlled Experiment Configurations
We test three controlled setups:
1. Small configuration: 4 numbers with 2 bins. 100 percent in range.
2. Medium configuration: 8 numbers including outliers. Shows how out of range tracking separates extreme numbers.
3. Multi bin configuration: 6 numbers with 3 bins. Shows how finer binning partitions numbers into smaller intervals.

## Observed Trade Off
Changing bin widths changes how values are grouped and how many fall outside the range, while maintaining 100 percent binning correctness. This is a local algorithmic accounting experiment and does not claim real world machine learning model performance.

## How to Run the Example
Run with Python 3:
```bash
python3 1-Introduction/04-stats-and-probability/applied-labs/r39-t058/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 1-Introduction/04-stats-and-probability/applied-labs/r39-t058 -p "test_*.py"
```

## Scope and Limitations
This lab is implemented purely in standard Python 3. It runs locally without needing external packages or special computing hardware.
