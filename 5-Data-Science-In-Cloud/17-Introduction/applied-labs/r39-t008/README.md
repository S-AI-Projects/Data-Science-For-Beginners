# Applied Lab R39-T008: Cloud Security-Scenario Rubric & Failure-and-Recovery Pipeline

## Overview & Lesson Connection

This applied lab extends the [Introduction to Data Science in the Cloud](../../README.md) lesson (`5-Data-Science-In-Cloud/17-Introduction/README.md`) by modeling cloud security and governance checks across core cloud data-science architectures:
- **Cloud Storage Accounts:** Data lake containers storing sensitive raw training datasets.
- **Shared Compute Clusters:** Multi-tenant virtual machine nodes performing distributed model training.
- **Real-Time Data Ingestion:** Streaming event hubs collecting high-velocity telemetry.

In cloud data-science workflows, automated policy evaluation pipelines frequently encounter malformed, partial, or missing submissions. If an evaluator crashes on a missing field or enters an unrecoverable error state, subsequent valid submissions are blocked. This lab implements a robust **failure-and-recovery pipeline** that captures and explains structured errors without crashing and recovers cleanly on the next valid input.

### Structured Grading vs. Unstructured Human Review
- **Automated Structural Rubric:** Programmatically validates schema completeness (`asset`, `threat`, `control`, `residual_risk`) and tests keyword alignment between threats and controls.
- **Qualitative Human Review:** Free-text explanations capture organizational risk context that automated rules cannot verify. The rubric explicitly flags that human review is required for the `explanation` field.

### Scope & Limitations [SIMULATION/MOCK]
- **Local In-Memory Standard-Library Execution:** Implemented purely with the Python 3 standard library.
- **Zero Cloud/Hardware Claims:** No real cloud subscriptions (Azure/AWS/GCP), IAM credentials, GPU nodes, or trained models are used or claimed.

---

## Contribution Focus: Failure and Recovery Pipeline

The core contribution demonstrates resilient stream processing across valid and invalid inputs:

1. **Structured Error Explanation (`error_code` & `error_explanation`):**  
   When an invalid submission (such as Scenario 2 with a missing `asset`) is evaluated:
   - `status` is marked `FAIL`.
   - `error_code` is set to `"MISSING_REQUIRED_FIELD"`.
   - `error_explanation` provides a human-readable diagnosis identifying which field is missing and why it is required.
2. **Stream State Isolation:**  
   The stream processor (`process_scenario_stream`) isolates the error, preventing batch corruption or unhandled exceptions.
3. **Clean Recovery on Next Valid Input (`recovered_after_failure: True`):**  
   When the very next valid input is processed, the evaluator resets its error tracking and returns a successful status (`PASS` or `FLAGGED_FOR_REVIEW`) with `recovered_after_failure = True`.

---

## Fixture Scenarios

| Scenario ID | Cloud Asset Target | Threat | Control | Status | Error Code |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cloud_storage_bucket_pass` | Data Lake Storage Account (Raw Training Datasets) | Public internet exposure & data exfiltration | Private endpoints, disable public blob access, IAM RBAC | `PASS` | `None` |
| `cloud_ingestion_pipeline_missing_asset` | Missing / empty asset field | Man-in-the-middle stream interception & tampering | TLS 1.3 encryption in transit & mutual authentication | `FAIL` | `MISSING_REQUIRED_FIELD` |
| `shared_compute_cluster_review` | Shared Cloud VM Compute Cluster | Privilege escalation & root shell access | Watermark logo on PDF reports (unrelated) | `FLAGGED_FOR_REVIEW` | `CONTROL_THREAT_MISALIGNMENT` |

---

## Prerequisites

- **Python:** Python 3.7+ (standard library only; no external packages).
- **Environment:** Local checkout of `Data-Science-For-Beginners`.

---

## Invocation & Expected Output

### Running the Rubric Checker & Stream Pipeline

Execute the script from the repository root:

```bash
python3 5-Data-Science-In-Cloud/17-Introduction/applied-labs/r39-t008/example.py
```

Expected output:

```text
======================================================================
[SIMULATION/MOCK] Cloud Security-Scenario Rubric & Recovery Pipeline (R39-T008)
Lesson Reference: 5-Data-Science-In-Cloud/17-Introduction
Scope: Local standard-library cloud security rubric & stream recovery
No live cloud provider (Azure/AWS/GCP), hardware, or models claimed.
======================================================================
[RUBRIC SCOPE NOTICE]
Automated rubric evaluation only checks structural completeness and
cloud threat-control alignment. Human review is strictly required to judge
the qualitative free-text explanation and contextual security rationale.
======================================================================

--- 1. CORE RUBRIC SCENARIOS ---
[SIMULATION/MOCK] cloud_storage_bucket_pass: status=PASS
  Asset: Cloud Data Lake Storage Account (Raw Training Datasets)
  Threat: Public internet exposure and unauthenticated data exfiltration of sensitive training datasets
  Control: Enforce private endpoints, disable public blob access, and mandate RBAC IAM roles

[SIMULATION/MOCK] cloud_ingestion_pipeline_missing_asset: status=FAIL
  Asset: (missing/empty)
  Threat: Man-in-the-middle interception and data tampering in real-time stream ingestion
  Control: Enforce TLS 1.3 encryption in transit and mutual certificate authentication
  Error Explanation: Validation failed: required field(s) 'asset' missing or empty. A complete cloud security submission must explicitly name the target asset, threat, control, and residual risk before automated policy validation.

[SIMULATION/MOCK] shared_compute_cluster_review: status=FLAGGED_FOR_REVIEW
  Asset: Shared Cloud VM Compute Cluster (Distributed Model Training)
  Threat: Privilege escalation and unauthorized root shell access on shared training nodes
  Control: Update corporate logo watermark on exported PDF reports
  Error Explanation: Review required: proposed control does not contain recognized mitigation patterns addressing the specified cloud threat. Forwarding to human expert for context analysis.

--- 2. FAILURE AND RECOVERY STREAM PIPELINE ---
Simulating stream: [Scenario 1 (Valid) -> Scenario 2 (Invalid/Missing) -> Scenario 3 (Valid Review)]
[SIMULATION/MOCK] Stream Step: id=cloud_storage_bucket_pass | status=PASS | error_code=None | recovered_after_failure=False
[SIMULATION/MOCK] Stream Step: id=cloud_ingestion_pipeline_missing_asset | status=FAIL | error_code=MISSING_REQUIRED_FIELD | recovered_after_failure=False
[SIMULATION/MOCK] Stream Step: id=shared_compute_cluster_review | status=FLAGGED_FOR_REVIEW | error_code=CONTROL_THREAT_MISALIGNMENT | recovered_after_failure=True

--- RECOVERY VERIFICATION SUMMARY ---
Step 2 failed with error code: MISSING_REQUIRED_FIELD
Step 3 recovered cleanly on next valid input: True
Recovery verified: True

======================================================================
[SIMULATION/MOCK] Summary: 1 PASS, 1 FAIL, 1 FLAGGED_FOR_REVIEW.
Verification complete.
======================================================================
```

### Running the Test Suite

Execute the unit and recovery tests:

```bash
python3 -m unittest discover -s 5-Data-Science-In-Cloud/17-Introduction/applied-labs/r39-t008 -p "test_*.py" -v
```

Expected test runner output:

```text
test_01_complete_consistent_cloud_scenario_passes (test_example.TestCloudSecurityScenarioRubric.test_01_complete_consistent_cloud_scenario_passes)
Test 1: Complete, internally consistent cloud scenario passes (PASS). ... ok
test_02_missing_asset_boundary_fails_with_explanation (test_example.TestCloudSecurityScenarioRubric.test_02_missing_asset_boundary_fails_with_explanation)
Test 2: Scenario without an asset fails (FAIL) with structured error explanation. ... ok
test_03_unrelated_control_flagged_for_review (test_example.TestCloudSecurityScenarioRubric.test_03_unrelated_control_flagged_for_review)
Test 3: Scenario with a control unrelated to the cloud threat is flagged for review. ... ok
test_04_failure_and_recovery_stream_pipeline (test_example.TestCloudSecurityScenarioRubric.test_04_failure_and_recovery_stream_pipeline)
Test 4: Processing [invalid_scenario, valid_scenario] records error and recovers cleanly. ... ok
test_05_deliberate_wrong_result_triggers_assertion_failure (test_example.TestCloudSecurityScenarioRubric.test_05_deliberate_wrong_result_triggers_assertion_failure)
Test 5: Deliberate wrong result or failed recovery triggers assertion failure. ... ok
test_06_fresh_process_cli_execution (test_example.TestCloudSecurityScenarioRubric.test_06_fresh_process_cli_execution)
Test 6: Running example.py in fresh process exits with code 0 and required tokens. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.018s

OK
```
