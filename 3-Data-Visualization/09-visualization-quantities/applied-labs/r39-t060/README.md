# Visualizing Quantities Consistency (R39 T060)

## Overview
This lab extends the Visualizing Quantities lesson. When presenting bar charts and quantity distributions, the displayed categories, bar values, and total summary numbers must always agree.

## The Contract
* Given items ["A", "A", "B", "C", "C", "C"]:
  * Category A = 2
  * Category B = 1
  * Category C = 3
  * Total = 6
* When filtered to categories A and B:
  * Category A = 2
  * Category B = 1
  * Total = 3

## Connection to Lesson Concepts
* Labels represent the category axis tick marks on a bar chart.
* Counts represent the bar heights measuring each discrete quantity.
* Displayed Total represents the aggregate headline number or summary badge.
* The consistency check verifies that the headline total equals the sum of the individual bar heights so viewers are not misled.

## How to Run the Example
Run with Python 3:
```bash
python3 3-Data-Visualization/09-visualization-quantities/applied-labs/r39-t060/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 3-Data-Visualization/09-visualization-quantities/applied-labs/r39-t060 -p "test_*.py"
```

## Scope and Limitations
This is a standard Python 3 script that validates numbers before charting. It does not use live rendering engines or external graphics packages like Matplotlib or Seaborn.
