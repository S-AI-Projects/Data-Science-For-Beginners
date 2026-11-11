# Applied Lab R39-T027: Proportion Failure Handling & Recovery

## Overview
This applied lab extends the "Visualizing Proportions" lesson by implementing an error-handling and failure-recovery pipeline for proportion calculations.

## Failure Modes & Error Policies
1. **Invalid/Negative Input:**
   - Input containing negative values (e.g. `{"A": -5, "B": 10}`) raises `ValueError`.
   - The stream pipeline traps the error, logs a diagnostic quarantine record (`RECOVERED_ERROR`), and keeps the pipeline live.
2. **Subsequent Recovery Demonstration:**
   - The immediate next record in the stream (`{"A": 2, "B": 3}`) is processed cleanly without state corruption or crash.
   - Normalized proportions `0.4` and `0.6` are computed successfully.
3. **Zero Total Policy:**
   - Inputs with all zero counts return `NO_DATA` status without raising division-by-zero errors.

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t027 -p "test_*.py" -v
```
