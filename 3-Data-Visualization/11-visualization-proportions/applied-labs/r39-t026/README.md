# Applied Lab R39-T026: Proportion Table Validation

## Overview
This applied lab extends the "Visualizing Proportions" lesson by converting category counts into relative proportions with a documented zero-total policy and input validation.

## Worked Input-to-Output Explanation
Consider input category counts: `{"A": 2, "B": 3}`.

1. **Validation Phase:**
   - Scan all category counts: `2 >= 0` and `3 >= 0`. No negative values detected.
2. **Summation Phase:**
   - Compute aggregate denominator: `total_count = 2 + 3 = 5`.
3. **Zero-Total Policy Check:**
   - Check if `total_count == 0`. Here `5 != 0`, so proceed with normalization.
4. **Normalization Phase:**
   - Proportion for category `A`: $P(A) = \frac{2}{5} = 0.4$
   - Proportion for category `B`: $P(B) = \frac{3}{5} = 0.6$
5. **Invariant Verification:**
   - Verify sum of proportions: $\sum P = 0.4 + 0.6 = 1.0$.

## Zero-Total & Negative Policies
- **Zero counts (`{"A": 0, "B": 0}`):** Returns `status = "NO_DATA"` with `total_count = 0` and `total_proportion = 0.0` to avoid division-by-zero crashes.
- **Negative counts (`{"A": -1, "B": 3}`):** Rejects invalid data with `ValueError`.

## Running Tests
Run the unit test suite locally:
```bash
python3 -m unittest discover -s 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t026 -p "test_*.py" -v
```
