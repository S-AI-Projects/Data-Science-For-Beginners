# Applied Lab R39-T029: Category Summary & Applied Assessment Scenarios

## Overview
This applied lab extends the "Visualizing Relationships: All About Honey" lesson by ensuring that categorical visual dimensions and aggregate summary totals remain synchronized. It features three applied diagnostic scenarios:

## Three Applied Assessment Questions
1. **Predict an Output:**
   - Input: `['A', 'B', 'B', 'C']` filtered to `['B']`.
   - Prediction: `{'B': 2}`, `total = 2`.
   - Rationale: Filtering restricts observations to 'B', maintaining synchronization between label counts and total.
2. **Diagnose a Failure:**
   - Defect: Filtered view displays `{'A': 2, 'B': 1}` but total indicator displays `6`.
   - Diagnosis: `STATE_DESYNCHRONIZATION`. Total was computed from raw unfiltered data instead of filtered dataset.
3. **Choose a Boundary Policy:**
   - Policy: When filter categories have zero occurrences in data (e.g. `['D', 'E']`), return empty counts `{}` and `total = 0`.
   - Rationale: Preserves the invariant $\sum \text{counts.values()} == \text{total} == 0$.

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 3-Data-Visualization/12-visualization-relationships/applied-labs/r39-t029 -p "test_*.py" -v
```
