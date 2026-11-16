# Applied Lab R39-T006: Security-Scenario Rubric & Teaching Example Refactoring

## Overview & Lesson Connection

This applied lab extends the [Defining Data](../../README.md) lesson (`1-Introduction/03-defining-data/README.md`) by providing a deterministic, Python 3 standard-library rubric checker for data governance and security scenarios.

In the *Defining Data* curriculum, data is classified along several axes:
- **Quantitative vs. Qualitative:** Numerical measurements (e.g., financial transaction amounts) vs. subjective descriptive content (e.g., free-text customer feedback).
- **Structured vs. Unstructured vs. Semi-Structured:** Rigorous tabular schemas (e.g., relational databases) vs. unstructured media/text vs. flexible hierarchical formats (e.g., JSON sensor telemetry).
- **Primary vs. Secondary Sources:** Data collected directly from origin sensors/users vs. aggregated datasets reused across teams.

This lab models these data classifications within three security/governance scenarios, evaluating each scenario across four structured attributes (`asset`, `threat`, `control`, `residual_risk`) alongside a free-text `explanation` field.

### Structured vs. Unstructured Evaluation
- **Structured Automated Grading:** Programmatic checks can rapidly verify structural completeness (ensuring no required field is empty) and test heuristic keyword alignment between threats and controls.
- **Unstructured Human Review:** Free-text explanations capture subjective rationale, context, and qualitative nuances that cannot be validated reliably by simple keyword scripts. Therefore, the automated rubric explicitly flags that human expert review is required for the explanation.

### Scope & Simplifications [SIMULATION/MOCK]
- **Pure Local Simulation:** All data fixtures are local in-memory records. No live databases, cloud credentials, GPUs, or trained machine learning models are used or claimed.
- **Rubric Boundaries:** Automated verification covers structural presence and keyword alignment. It does not replace comprehensive threat modeling or human architectural reviews.

---

## Contribution Focus: Refactoring the Teaching Example

The core contribution of this lab is demonstrating clean code refactoring within a teaching example while preserving exact functional equivalence:

1. **Baseline Evaluator (`evaluate_scenario_baseline` / `run_baseline_suite`):**
   A monolithic implementation that validates required fields and executes inline threat-control keyword matching within a single function.
2. **Extracted Pure Helper (`check_threat_control_alignment`):**
   Extracts threat-control alignment heuristics into a dedicated, pure helper function with zero side effects.
3. **Refactored Evaluator (`evaluate_scenario_refactored` / `run_refactored_suite`):**
   Delegates alignment decisions to the pure helper function while maintaining the identical input/output contract.
4. **Equivalence Invariant:**
   `run_baseline_suite(FIXTURES) == run_refactored_suite(FIXTURES)` evaluates to `True` across all fixture scenarios (`EQUIVALENCE_VERIFIED: True`).

---

## Fixture Scenarios

The lab defines three fictional scenarios grounded in the lesson:

| Scenario ID | Asset Type & Source | Threat | Control | Status |
| :--- | :--- | :--- | :--- | :--- |
| `scenario_1_quantitative_primary_store` | Structured quantitative relational database (Primary) | SQL injection extracting financial transaction records | Parameterized SQL queries & column data-type validation | `PASS` |
| `scenario_2_missing_asset_boundary` | Missing / empty asset field (Boundary condition) | Unencrypted secondary storage leaking qualitative survey responses | AES-256 at-rest encryption & access control lists | `FAIL` |
| `scenario_3_unstructured_sensor_review` | Semi-structured JSON sensor telemetry (Primary) | Telemetry spoofing and temperature sensor tampering | Switch presentation slide theme to high-contrast dark mode | `FLAGGED_FOR_REVIEW` |

---

## Prerequisites

- **Python:** Python 3.7+ (standard library only; no external pip dependencies).
- **Environment:** Local git checkout of `Data-Science-For-Beginners`.

---

## Invocation & Expected Output

### Running the Rubric Checker

Execute the standalone script from repository root:

```bash
python3 1-Introduction/03-defining-data/applied-labs/r39-t006/example.py
```

Expected output:

```text
======================================================================
[SIMULATION/MOCK] Security-Scenario Rubric Checker (R39-T006)
Lesson Reference: 1-Introduction/03-defining-data (Defining Data)
Scope: In-memory educational simulation (No cloud, API, or hardware dependencies)
======================================================================
[RUBRIC SCOPE NOTICE]
Automated rubric evaluation only checks structural completeness and
threat-control alignment. Human review is strictly required to judge
the qualitative free-text explanation and contextual security rationale.
======================================================================

--- FIXTURE SCENARIOS (INPUTS) ---
[SIMULATION/MOCK] Scenario 1:
  ID: scenario_1_quantitative_primary_store
  Asset: Customer Transactions Database (Structured Relational Primary Store)
  Threat: SQL injection leading to unauthorized extraction of quantitative financial records
  Control: Enforce parameterized SQL queries and strict column data-type validation
  Residual Risk: Low: Zero-day database engine vulnerabilities remain possible
  Explanation: Primary transaction records represent quantitative structured data requiring strict input parameterization to prevent SQL injection and data exfiltration.

[SIMULATION/MOCK] Scenario 2:
  ID: scenario_2_missing_asset_boundary
  Asset: (missing/empty)
  Threat: Unencrypted secondary survey storage leading to leak of qualitative feedback responses
  Control: Enforce AES-256 at-rest encryption and access control lists for secondary file stores
  Residual Risk: Low: Key rotation failure or compromised credentials
  Explanation: Qualitative survey comments stored as secondary data must be encrypted at rest, but asset metadata is missing from the submission.

[SIMULATION/MOCK] Scenario 3:
  ID: scenario_3_unstructured_sensor_review
  Asset: Unstructured Environmental Sensor Stream (Primary Semi-Structured JSON Source)
  Threat: Telemetry spoofing and data tampering injecting corrupt temperature readings
  Control: Switch presentation slide theme to high-contrast dark mode
  Residual Risk: High: Corrupted sensor packets still compromise downstream analytical pipelines
  Explanation: Primary sensor streams can be spoofed, but modifying presentation themes does not address network payload integrity or telemetry authentication.

--- BASELINE VS. REFACTORED EQUIVALENCE ---
Baseline results count: 3
Refactored results count: 3
EQUIVALENCE_VERIFIED: True

--- EVALUATION RESULTS ---
[SIMULATION/MOCK] scenario_1_quantitative_primary_store: status=PASS | aligned=True | missing=[]
[SIMULATION/MOCK] scenario_2_missing_asset_boundary: status=FAIL | aligned=True | missing=['asset']
[SIMULATION/MOCK] scenario_3_unstructured_sensor_review: status=FLAGGED_FOR_REVIEW | aligned=False | missing=[]

======================================================================
[SIMULATION/MOCK] Summary: 1 PASS, 1 FAIL, 1 FLAGGED_FOR_REVIEW.
Verification complete.
======================================================================
```

### Running the Test Suite

Execute the test discovery command:

```bash
python3 -m unittest discover -s 1-Introduction/03-defining-data/applied-labs/r39-t006 -p "test_*.py" -v
```

Expected test runner output:

```text
test_01_complete_consistent_scenario_passes (test_example.TestSecurityScenarioRubric.test_01_complete_consistent_scenario_passes)
Test 1: Complete, internally consistent scenario passes (PASS). ... ok
test_02_missing_asset_boundary_fails (test_example.TestSecurityScenarioRubric.test_02_missing_asset_boundary_fails)
Test 2: Scenario without an asset fails (FAIL). ... ok
test_03_unrelated_control_flagged_for_review (test_example.TestSecurityScenarioRubric.test_03_unrelated_control_flagged_for_review)
Test 3: Scenario with a control unrelated to the threat is flagged for review. ... ok
test_04_baseline_refactored_equivalence_across_fixture (test_example.TestSecurityScenarioRubric.test_04_baseline_refactored_equivalence_across_fixture)
Test 4: Baseline vs. refactored implementation equivalence holds across the fixture. ... ok
test_05_deliberate_wrong_result_triggers_assertion_failure (test_example.TestSecurityScenarioRubric.test_05_deliberate_wrong_result_triggers_assertion_failure)
Test 5: Deliberate wrong result / mutated rubric output triggers an assertion failure. ... ok
test_06_fresh_process_cli_execution (test_example.TestSecurityScenarioRubric.test_06_fresh_process_cli_execution)
Test 6: Fresh-process CLI execution verifies normal execution and expected tokens. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.020s

OK
```
