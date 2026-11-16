# Applied Lab R39-T007: Chart-Data Consistency & Worked Example

## Overview & Lesson Connection

This applied lab extends the [Making Meaningful Visualizations](../../README.md) lesson (`3-Data-Visualization/13-meaningful-visualizations/README.md`) by addressing a subtle but prevalent form of deceptive charting: **inconsistent or stale summary metrics**.

In lesson 13, learners study how charts can easily deceive audiences—not only through reversed axes or manipulated color palettes, but also through misleading proportions and aggregated summaries. A common failure mode occurs when:
1. Interactive filters are applied to a chart view (e.g., selecting only categories `A` and `B`).
2. The series bars or pie slices update to reflect the filtered items.
3. The chart title, subtitle, or summary badge displays a **stale unfiltered total** computed prior to filtering, misleading viewers about proportions and baseline denominators.

This lab builds a deterministic, standard-library validator that ensures chart `labels`, `counts`, and the `displayed_total` remain mathematically aligned and synchronized.

### Scope & Limitations [SIMULATION/MOCK]
- **Standard Library In-Memory Validation:** Implemented entirely using the Python 3 standard library.
- **Data-Level Integrity:** Focuses strictly on data aggregation and summary consistency before chart rendering. No browser engines, GUI libraries, cloud BI dashboards, or trained machine learning models are used or claimed.

---

## Contribution Focus: Worked Input-to-Output Trace

The core contribution is a step-by-step worked input-to-output trace executed as a deterministic regression check:

1. **Step 1: Raw Observation Rows**  
   Input data: `["A", "A", "B", "C", "C", "C"]` (6 raw categorical observations).
2. **Step 2: Unfiltered Aggregation**  
   Grouped counts: `A=2, B=1, C=3` with `total=6`.  
   Labels: `["A", "B", "C"]`, Counts: `[2, 1, 3]`.  
   Consistency Check: `sum(counts) == displayed_total` (6 == 6) &rarr; `consistent=True`.
3. **Step 3: Filtered Subset (`A/B`) with Recomputed Total**  
   Filter applied: allowed categories `{"A", "B"}`.  
   Grouped counts: `A=2, B=1` with recomputed `total=3`.  
   Labels: `["A", "B"]`, Counts: `[2, 1]`.  
   Consistency Check: `sum(counts) == displayed_total` (3 == 3) &rarr; `consistent=True`.
4. **Step 4: Deceptive Mismatch Scenario (Stale Total)**  
   Filtered counts: `A=2, B=1` (sum = 3), but `displayed_total` incorrectly remains `6`.  
   Consistency Check: `sum(counts) != displayed_total` (3 != 6) &rarr; `consistent=False`.

---

## Scenario Summary

| Scenario | Input Rows | Filter | Labels & Counts | Displayed Total | Consistent? | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Normal (Full Fixture)** | `["A", "A", "B", "C", "C", "C"]` | None | `A=2, B=1, C=3` | 6 | `True` | Complete consistent dataset |
| **Boundary (Filtered A/B)** | `["A", "A", "B", "C", "C", "C"]` | `{"A", "B"}` | `A=2, B=1` | 3 | `True` | Filtered subset with recomputed total |
| **Failure (Stale Total)** | `["A", "A", "B", "C", "C", "C"]` | `{"A", "B"}` | `A=2, B=1` | 6 | `False` | Deceptive pattern: stale unfiltered total |

---

## Prerequisites

- **Python:** Python 3.7+ (standard library only; no external pip dependencies).
- **Environment:** Local checkout of `Data-Science-For-Beginners`.

---

## Invocation & Expected Output

### Running the Worked Example & Consistency Validator

Execute the script from the repository root:

```bash
python3 3-Data-Visualization/13-meaningful-visualizations/applied-labs/r39-t007/example.py
```

Expected output:

```text
======================================================================
[SIMULATION/MOCK] Chart-Data Consistency & Worked Example (R39-T007)
Lesson Reference: 3-Data-Visualization/13-meaningful-visualizations
Scope: Local standard-library chart consistency validator
No GUI/rendering hardware, cloud BI service, or ML models claimed.
======================================================================

--- WORKED INPUT-TO-OUTPUT TRACE ---
Step 1 [raw_input]: Raw observational categorical stream
  Consistent: N/A

Step 2 [full_unfiltered_aggregation]: Grouped counts across all observed categories
  Summary: A=2,B=1,C=3,total=6
  Consistent: True

Step 3 [filtered_subset_recomputed]: Filtered to A/B with dynamically recomputed total
  Summary: A=2,B=1,total=3
  Consistent: True

Step 4 [deceptive_stale_total]: Filtered chart displaying stale unfiltered total (deceptive pattern)
  Consistency Errors: ['Sum mismatch: sum of counts (3) != displayed_total (6)']
  Consistent: False

--- REGRESSION VERIFICATION SUMMARY ---
Unfiltered breakdown: A=2,B=1,C=3,total=6
Filtered A/B: total=3
Regression check passed: True

--- STATUS OF EVALUATED SCENARIOS ---
[SIMULATION/MOCK] Scenario 1 (Normal / Full Fixture): consistent=True (A=2,B=1,C=3,total=6)
[SIMULATION/MOCK] Scenario 2 (Boundary / Filtered A/B): consistent=True (A=2,B=1,total=3)
[SIMULATION/MOCK] Scenario 3 (Failure / Stale Total Mismatch): consistent=False (sum=3 != total=6)

======================================================================
[SIMULATION/MOCK] Verification complete.
======================================================================
```

### Running the Test Suite

Execute the regression and boundary tests:

```bash
python3 -m unittest discover -s 3-Data-Visualization/13-meaningful-visualizations/applied-labs/r39-t007 -p "test_*.py" -v
```

Expected test runner output:

```text
test_01_exact_worked_example_regression (test_example.TestChartDataConsistency.test_01_exact_worked_example_regression)
Test 1: Rows ['A', 'A', 'B', 'C', 'C', 'C'] yield exact counts and total == 6. ... ok
test_02_filtered_ab_subset_boundary (test_example.TestChartDataConsistency.test_02_filtered_ab_subset_boundary)
Test 2: Filtering ['A', 'A', 'B', 'C', 'C', 'C'] to {'A', 'B'} yields counts A=2, B=1 and total == 3. ... ok
test_03_empty_and_single_category_boundary (test_example.TestChartDataConsistency.test_03_empty_and_single_category_boundary)
Test 3: Empty input yields total == 0 with empty labels/counts; single category yields expected single item. ... ok
test_04_deliberate_wrong_result_and_stale_total_failure (test_example.TestChartDataConsistency.test_04_deliberate_wrong_result_and_stale_total_failure)
Test 4: Stale unfiltered total (total=6) for filtered subset (sum=3) or mismatched arrays fails consistency check. ... ok
test_05_fresh_process_cli_execution (test_example.TestChartDataConsistency.test_05_fresh_process_cli_execution)
Test 5: Running example.py in fresh process exits with code 0 and required output tokens. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.018s

OK
```
