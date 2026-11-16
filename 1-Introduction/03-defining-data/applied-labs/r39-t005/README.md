# Applied Lab R39-T005: Security-Scenario Rubric & Offline Service Adapter

## Overview & Lesson Connection

This applied lab extends the [Defining Data](../../README.md) lesson (`1-Introduction/03-defining-data/README.md`) by implementing a deterministic, standard-library security and governance rubric checker decoupled from external dependencies via a **callable service adapter interface**.

In the *Defining Data* curriculum, data is categorized along foundational dimensions:
- **Quantitative vs. Qualitative Data:** Objective numerical observations (e.g., financial ledger balances) versus descriptive subjective data (e.g., customer survey feedback).
- **Structured vs. Unstructured vs. Semi-Structured Data:** Rigorously typed schema tables (e.g., relational databases) versus unstructured free text versus flexible self-describing structures (e.g., JSON sensor telemetry).
- **Primary vs. Secondary Sources:** Primary data originating directly from user interactions/sensors versus secondary datasets aggregated for secondary analysis.

This lab applies these data concepts to evaluate three security/governance scenarios against four structured rubric fields (`asset`, `threat`, `control`, `residual_risk`) alongside a qualitative `explanation` field.

### Structured Rubric vs. Unstructured Human Review
- **Structured Automated Grading:** Programmatic checks evaluate structured schema presence (verifying that required attributes like `asset` are populated) and delegate threat-control policy alignment to an injected catalog service.
- **Unstructured Qualitative Review:** Automated keyword matching cannot judge the nuanced security rationale of free-text explanations. The rubric evaluator explicitly notes that human expert review is required for the `explanation` field.

### Scope & Limitations [SIMULATION/MOCK]
- **Pure Local In-Memory Simulation:** All fixtures and policy tables are maintained in-memory using only the Python 3 standard library.
- **Zero Cloud/Hardware Claims:** No cloud subscriptions, live IAM APIs, GPUs, or trained models are used or claimed.

---

## Contribution Focus: Callable Offline Service Adapter

To decouple rubric evaluation logic from external threat catalogs, this lab introduces a clean callable interface pattern:

1. **Callable Interface (`ThreatControlCatalogCallable`):**
   Defined as `Callable[[str, str], dict[str, Any]]`. The rubric evaluator `evaluate_scenario(scenario, adapter=...)` accepts any callable implementing this contract.
2. **Deterministic Local Offline Adapter (`LocalOfflineRubricAdapter` / `deterministic_local_adapter`):**
   An in-memory implementation providing deterministic threat-to-control alignment checks against structured data classifications without external HTTP/cloud calls.
3. **Pluggable Architecture:**
   Enables injecting custom adapters (e.g., for test doubles, alternative catalogs, or strict audit policies) without modifying core evaluation logic.

### Unestablished Real-Service Behaviors
The offline mock explicitly documents that it does **not** establish the following real-service capabilities:
1. Live IAM/policy API authentication & OAuth token exchange
2. Network transport latency, socket timeouts, and automatic retry/backoff policies
3. API rate limiting, concurrency throttling, and quota enforcement
4. Live policy catalog schema drift and dynamic upstream rule updates
5. Semantic LLM/NLP grading of free-text qualitative explanations

---

## Fixture Scenarios

| Scenario ID | Asset Type & Source | Threat | Control | Status |
| :--- | :--- | :--- | :--- | :--- |
| `scenario_1_quantitative_primary_store` | Structured quantitative relational database (Primary) | SQL injection extracting financial transaction records | Parameterized SQL queries & column data-type validation | `PASS` |
| `scenario_2_missing_asset_boundary` | Missing / empty asset field (Boundary condition) | Unencrypted secondary storage leaking qualitative survey responses | AES-256 at-rest encryption & access control lists | `FAIL` |
| `scenario_3_unstructured_sensor_review` | Semi-structured JSON sensor telemetry (Primary) | Telemetry spoofing and temperature sensor tampering | Switch presentation slide theme to high-contrast dark mode | `FLAGGED_FOR_REVIEW` |

---

## Prerequisites

- **Python:** Python 3.7+ (standard library only; no external packages required).
- **Environment:** Local checkout of `Data-Science-For-Beginners`.

---

## Invocation & Expected Output

### Running the Rubric Checker

Execute the standalone script:

```bash
python3 1-Introduction/03-defining-data/applied-labs/r39-t005/example.py
```

Expected output:

```text
======================================================================
[SIMULATION/MOCK] Security-Scenario Rubric & Offline Service Adapter (R39-T005)
Lesson Reference: 1-Introduction/03-defining-data (Defining Data)
Adapter: [SIMULATION/MOCK] Deterministic Local Offline Adapter
Scope: In-memory educational simulation (No cloud, API, or hardware dependencies)
======================================================================
[RUBRIC SCOPE NOTICE]
Automated rubric evaluation only checks structural completeness and
adapter policy alignment. Human review is strictly required to judge
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

--- ADAPTER EXECUTION & METADATA ---
Adapter Name: [SIMULATION/MOCK] Deterministic Local Offline Adapter
Callable Type: LocalOfflineRubricAdapter

--- EVALUATION RESULTS ---
[SIMULATION/MOCK] scenario_1_quantitative_primary_store: status=PASS | aligned=True | missing=[]
[SIMULATION/MOCK] scenario_2_missing_asset_boundary: status=FAIL | aligned=True | missing=['asset']
[SIMULATION/MOCK] scenario_3_unstructured_sensor_review: status=FLAGGED_FOR_REVIEW | aligned=False | missing=[]

--- UNESTABLISHED REAL-SERVICE BEHAVIORS ---
The offline simulation does NOT establish the following real-service capabilities:
  1. Live IAM/policy API authentication & OAuth token exchange
  2. Network transport latency, socket timeouts, and automatic retry/backoff policies
  3. API rate limiting, concurrency throttling, and quota enforcement
  4. Live policy catalog schema drift and dynamic upstream rule updates
  5. Semantic LLM/NLP grading of free-text qualitative explanations

======================================================================
[SIMULATION/MOCK] Summary: 1 PASS, 1 FAIL, 1 FLAGGED_FOR_REVIEW.
Verification complete.
======================================================================
```

### Running the Test Suite

Execute standard unit test discovery:

```bash
python3 -m unittest discover -s 1-Introduction/03-defining-data/applied-labs/r39-t005 -p "test_*.py" -v
```

Expected test runner output:

```text
test_01_complete_consistent_scenario_passes (test_example.TestSecurityScenarioRubric.test_01_complete_consistent_scenario_passes)
Test 1: Complete, internally consistent scenario passes (PASS). ... ok
test_02_missing_asset_boundary_fails (test_example.TestSecurityScenarioRubric.test_02_missing_asset_boundary_fails)
Test 2: Scenario without an asset fails (FAIL). ... ok
test_03_unrelated_control_flagged_for_review (test_example.TestSecurityScenarioRubric.test_03_unrelated_control_flagged_for_review)
Test 3: Scenario with a control unrelated to the threat is flagged for review. ... ok
test_04_callable_interface_injection_and_unestablished_behaviors (test_example.TestSecurityScenarioRubric.test_04_callable_interface_injection_and_unestablished_behaviors)
Test 4: Callable interface injection works with default and custom adapters and reports unestablished behaviors. ... ok
test_05_deliberate_wrong_result_triggers_assertion_failure (test_example.TestSecurityScenarioRubric.test_05_deliberate_wrong_result_triggers_assertion_failure)
Test 5: Deliberate wrong result from a faulty injected adapter makes the test fail. ... ok
test_06_fresh_process_cli_execution (test_example.TestSecurityScenarioRubric.test_06_fresh_process_cli_execution)
Test 6: Fresh-process CLI execution verifies normal execution and expected stdout markers. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.018s

OK
```
