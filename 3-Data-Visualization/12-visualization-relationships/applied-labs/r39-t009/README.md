# Applied Lab R39-T009: Chart-Data Consistency & Three-Configuration Evaluation Experiment

## Overview & Lesson Connection

This applied lab extends the [Visualizing Relationships: All About Honey 🍯](../../README.md) lesson (`3-Data-Visualization/12-visualization-relationships/README.md`) by exploring how multi-category groupings and filtered relational views must maintain strict data consistency between category labels, counts, and displayed totals.

In lesson 12, learners use Seaborn scatterplots, line charts, and facet grids to explore relationships across U.S. states and years in the USDA honey dataset. In interactive or faceted visualizations:
1. Users filter datasets to examine specific subsets (e.g., comparing only states `A` and `B`).
2. The chart updates the category labels and data series.
3. If the displayed total or summary badge fails to re-aggregate dynamically, viewers encounter a **stale total discrepancy**, leading to misleading interpretations of proportions and relative relationships.

This lab implements a local, standard-library category summary builder and consistency verifier, and executes a **three-configuration evaluation experiment** to assess the trade-offs between eager re-aggregation correctness and computational operation cost.

### Scope & Limitations [SIMULATION/MOCK]
- **Standard Library In-Memory Experiment:** Implemented entirely using Python 3 standard library primitives (`collections.Counter`, dataclasses).
- **Tabular/Aggregate Verification:** Focuses on pre-rendering aggregate integrity. No GUI rendering engines, cloud BI dashboards, or trained machine learning models are used or claimed.

---

## Contribution Focus: Three-Configuration Evaluation Experiment

The lab runs `run_evaluation_experiment()`, comparing three controlled configurations across deterministic metrics (`rows_scanned`, `validation_operations`, `coverage_ratio`, `consistency_correctness`, and `discrepancy`):

| Configuration | Input Size (N) | Strategy | Rows Scanned | Correctness | Discrepancy | Trade-off Analysis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Config 1 — Baseline Small Fixture** | `N=6` | Full scan + strict re-aggregation | 6 | `True` | 0 | Guaranteed consistency across full and filtered views; minimal computational cost on small inputs. |
| **Config 2 — Medium Scaled Fixture** | `N=60` | 10x scaled pattern + full re-aggregation | 60 | `True` | 0 | Linear scan scaling O(N); guarantees mathematical integrity as dataset grows. |
| **Config 3 — Cached/Stale-Total Fast-Path** | `N=6` | Cached unfiltered total reused on filter | 6 | `False` | 3 | Bypasses summation pass but introduces a deceptive discrepancy of 3; demonstrates recomputation is mandatory. |

### Observed Experimental Trade-off
Eager full-scan re-aggregation requires $O(N)$ row operations as input grows from $N=6$ to $N=60$, but guarantees that category slices and displayed totals remain mathematically synchronized. Attempting to bypass recomputation via cached fast-paths (Config 3) saves trivial CPU cycles but immediately compromises visualization accuracy.

---

## Core Fixture Summary

- **Unfiltered Observations:** `["A", "A", "B", "C", "C", "C"]` &rarr; `A=2, B=1, C=3`, `total=6`, `consistent=True`.
- **Filtered Subset (`A/B`):** Restricting to `{"A", "B"}` &rarr; `A=2, B=1`, recomputed `total=3`, `consistent=True`.
- **Failure Mismatch:** Paired with stale unfiltered total `6` &rarr; `consistent=False` (`sum=3 != total=6`).

---

## Prerequisites

- **Python:** Python 3.7+ (standard library only; no external dependencies).
- **Environment:** Local checkout of `Data-Science-For-Beginners`.

---

## Invocation & Expected Output

### Running the Evaluation Experiment

Execute the standalone script:

```bash
python3 3-Data-Visualization/12-visualization-relationships/applied-labs/r39-t009/example.py
```

Expected output:

```text
======================================================================
[SIMULATION/MOCK] Chart-Data Consistency Evaluation Experiment (R39-T009)
Lesson Reference: 3-Data-Visualization/12-visualization-relationships
Scope: Local standard-library chart-data consistency & configuration benchmark
No GUI/rendering hardware, cloud BI service, or ML model accuracy claimed.
======================================================================

--- CORE CONTRACT SUMMARY ---
Unfiltered breakdown: A=2,B=1,C=3,total=6
Filtered A/B: A=2,B=1,total=3
Filtered A/B: total=3

--- THREE-CONFIGURATION EVALUATION EXPERIMENT ---
Configuration: Config 1 — Baseline Small Fixture (N=6, Full Scan + Strict Re-aggregation)
  Input Size (N): 6
  Rows Scanned: 6
  Validation Checks: 3
  Coverage Ratio: 1.0
  Correctness (Consistent): True
  Discrepancy: 0
  Trade-off Analysis: Guaranteed consistency across all categories and filtered views; minimal computational overhead on small datasets.

Configuration: Config 2 — Medium Scaled Fixture (N=60, 10x Scaled + Full Re-aggregation)
  Input Size (N): 60
  Rows Scanned: 60
  Validation Checks: 3
  Coverage Ratio: 1.0
  Correctness (Consistent): True
  Discrepancy: 0
  Trade-off Analysis: Linear scan operations scale with input size (60 rows); full re-aggregation maintains mathematical consistency and prevents deceptive proportions at scale.

Configuration: Config 3 — Cached/Stale-Total Fast-Path (N=6, Unrecomputed Total on Filter)
  Input Size (N): 6
  Rows Scanned: 6
  Validation Checks: 3
  Coverage Ratio: 0.5
  Correctness (Consistent): False
  Discrepancy: 3
  Trade-off Analysis: Saves 1 summation pass by reusing cached total, but introduces deceptive stale total (discrepancy=3); proves recomputing totals is mandatory.

--- OBSERVED EXPERIMENTAL TRADE-OFF ---
Trade-off Summary: Eager full-scan re-aggregation requires O(N) operations (N=6 -> N=60),
but guarantees mathematical consistency across all filtered views. Attempting to bypass
recomputation (Config 3) saves trivial CPU cycles but produces a deceptive discrepancy of 3,
confirming that total re-aggregation is strictly required for meaningful visualization.

======================================================================
[SIMULATION/MOCK] Verification complete.
======================================================================
```

### Running the Test Suite

Execute the unit and experiment verification tests:

```bash
python3 -m unittest discover -s 3-Data-Visualization/12-visualization-relationships/applied-labs/r39-t009 -p "test_*.py" -v
```

Expected test runner output:

```text
test_01_normal_fixture_unfiltered_breakdown (test_example.TestChartDataConsistencyExperiment.test_01_normal_fixture_unfiltered_breakdown)
Test 1: Normal fixture ['A', 'A', 'B', 'C', 'C', 'C'] yields A=2, B=1, C=3, total=6. ... ok
test_02_boundary_filtered_ab_subset (test_example.TestChartDataConsistencyExperiment.test_02_boundary_filtered_ab_subset)
Test 2: Boundary filtered subset {'A', 'B'} yields A=2, B=1, total=3. ... ok
test_03_evaluation_experiment_three_configurations (test_example.TestChartDataConsistencyExperiment.test_03_evaluation_experiment_three_configurations)
Test 3: run_evaluation_experiment() compares three configurations and checks metrics/trade-offs. ... ok
test_04_deliberate_wrong_result_failure (test_example.TestChartDataConsistencyExperiment.test_04_deliberate_wrong_result_failure)
Test 4: Stale total or mismatched arrays causes consistency verification failure. ... ok
test_05_fresh_process_cli_execution (test_example.TestChartDataConsistencyExperiment.test_05_fresh_process_cli_execution)
Test 5: Fresh-process CLI execution exits with returncode == 0 and expected tokens. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.025s

OK
```
