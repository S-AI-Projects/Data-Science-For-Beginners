# Applied Lab R39-T028: SQLite Parameterized Queries & Benchmarking

## Overview
This applied lab extends the "Working with Data: Relational Databases" lesson by introducing safe, parameterized querying against an in-memory SQLite database, contrasting parameterized queries against string concatenation vulnerabilities.

## Invariants & Correctness
- **Canonical Rows:** `[("tea", "drink"), ("rice", "food"), ("coffee", "drink")]`
- **Category Query (`drink`):** Returns `["coffee", "tea"]` ordered alphabetically by name.
- **Literal Quotes & Injection Immunity:** Inputs containing SQL fragments or quotes (e.g. `drink' OR '1'='1` or `chef's special`) are treated strictly as literal strings rather than SQL tokens.

## Three Controlled Configurations Comparison
We benchmark three controlled input configurations:
- **Small (N=3):** Baseline canonical dataset.
- **Medium (N=10):** Mixed food and beverage catalog.
- **Scaled (N=25):** Synthetic 25-row items table.

Metrics tracked: match count correctness and average microsecond latency per query execution.

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 2-Working-With-Data/05-relational-databases/applied-labs/r39-t028 -p "test_*.py" -v
```
