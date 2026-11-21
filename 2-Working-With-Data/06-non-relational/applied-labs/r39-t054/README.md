# Parameterized Local Query (R39 T054)

## Overview
This lab extends the non relational data lesson by showing how to safely query tabular data using parameterized queries in SQLite. Parameterized queries make sure inputs are always treated as values rather than executable code.

## The Contract
* An in memory SQLite table items is created with columns name and category.
* Three rows are inserted: (tea, drink), (rice, food), (coffee, drink).
* Querying category drink returns tea and coffee in name order (coffee, tea).
* A query with special characters like quotes stays literal data and avoids SQL injection.

## State Trace and Invariant
Each step in the process records its intermediate state:
1. Setting up the table records an empty table.
2. Inserting rows records the total count and count per category.
3. Querying records the returned list and matches it against the intermediate count to verify the invariant.

## How to Run the Example
Run with Python 3:
```bash
python3 2-Working-With-Data/06-non-relational/applied-labs/r39-t054/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 2-Working-With-Data/06-non-relational/applied-labs/r39-t054 -p "test_*.py"
```

## Scope and Limitations
This lab uses the Python standard library sqlite3 module in memory. No external database servers or network connections are needed.
