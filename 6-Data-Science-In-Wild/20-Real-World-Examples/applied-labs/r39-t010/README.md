# Applied Lab R39-T010: Security-Scenario Rubric & Scenario Assessment

This applied lab extends **Lesson 20: Data Science in the Real World** (`6-Data-Science-In-Wild/20-Real-World-Examples`) with an executable security-scenario rubric checker and an applied three-question assessment module.

## Conceptual Background & Lesson Connection

In real-world data science projects—spanning healthcare informatics, planetary satellite analysis, and IoT agricultural sensors—safeguarding datasets and models against adversarial attacks, data leaks, and spoofing is critical. Threat modeling requires clearly defining four structural elements:
1. **Asset**: The data, model, or telemetry stream requiring protection.
2. **Threat**: The specific attack vector or compromise scenario.
3. **Control**: The technical safeguard implemented to mitigate the threat.
4. **Residual Risk**: The remaining risk exposure accepted by the system owner.

### Automated Rubric vs. Human Review Boundaries
- **Automated Checker Scope**: The automated grader enforces deterministic structural rules—verifying that required fields are present and non-empty (after stripping whitespace) and evaluating known threat-to-control keyword alignments.
- **Human Review Requirement**: Free-text justifications in the `explanation` field, qualitative threat relevance, and organizational risk tolerance cannot be certified solely through automated code checks. Where structural alignment is ambiguous or novel, the rubric routes the scenario to human auditor evaluation (`FLAGGED_FOR_REVIEW`).

### Educational Scope & Simulation Boundaries
> **[SIMULATION/MOCK] Notice**: This lab is a purely local educational simulation implemented exclusively in Python 3 standard library. It does not invoke cloud services, configure real IoT gateways, process live clinical data, or train machine learning models.

---

## Applied Scenario Assessment (Three Questions)

The module implements three applied assessment questions paired with rationales and executable validation checks:

| ID | Type | Prompt Summary | Expected Factual Answer | Executable Check Target |
|:---|:-----|:---------------|:------------------------|:------------------------|
| **Q1** | `predict_output` | Predict status when fields are populated but control is mismatched with threat | `FLAGGED_FOR_REVIEW` | Runs evaluator on mismatched threat/control scenario and asserts `status == "FLAGGED_FOR_REVIEW"` |
| **Q2** | `diagnose_failure` | Diagnose missing field causing Scenario 2 to fail, and verify recovery | `asset` | Verifies `missing_fields == ['asset']`, repairs asset, and asserts transition to `PASS` |
| **Q3** | `choose_boundary_policy` | Deterministic policy for whitespace inputs and novel threat categories | `strip_whitespace_reject_and_flag_unmapped_for_review` | Asserts whitespace asset triggers `FAIL` and unmapped threat triggers `FLAGGED_FOR_REVIEW` |

### Question Rationales
- **Q1 Rationale**: Syntactic completeness does not imply semantic alignment. If an IoT sensor replay threat is paired with a web HTML sanitization control, automated pass would create a false sense of security; routing to human review ensures domain-expert auditing.
- **Q2 Rationale**: Threat modeling requires an identifiable asset. Scenario 2 lacked the `asset` field. Populating `asset="Planetary Computer Satellite Multispectral Imagery Archive"` repairs structural completeness and allows the scenario to pass.
- **Q3 Rationale**: Fail-safe defaults dictate that whitespace-only strings must be rejected as missing (`FAIL`) rather than bypassing checks, and unmapped threat domains must be flagged for human review (`FLAGGED_FOR_REVIEW`) rather than assumed benign.

---

## Fixture Scenarios Summary

| Scenario ID | Name | Threat Category | Expected Status | Reason / Review |
|:------------|:-----|:----------------|:----------------|:----------------|
| **RW-01** | Clinical Healthcare Telemetry Export | Exfiltration | `PASS` | `complete_and_consistent` (Human review not required) |
| **RW-02** | Planetary Earth Observation Pipeline | Adversarial Evasion | `FAIL` | `missing_asset` (Missing mandatory field) |
| **RW-03** | Smart Agriculture LoRaWAN Pipeline | Sensor Spoofing | `FLAGGED_FOR_REVIEW` | `unrelated_control_threat_mismatch` (Human review required) |

---

## Prerequisites & Running Instructions

### Prerequisites
- Python 3.8+ (standard library only; no pip dependencies required)
- Local clone of `Data-Science-For-Beginners`

### Execution

Run the standalone applied lab report:
```bash
python3 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t010/example.py
```

Run the unit and assessment verification suite:
```bash
python3 -m unittest discover -s 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t010 -p "test_*.py" -v
```

### Expected Output Summary
```text
================================================================================
APPLIED LAB R39-T010: SECURITY-SCENARIO RUBRIC & SCENARIO ASSESSMENT
Lesson Reference: 6-Data-Science-In-Wild/20-Real-World-Examples
Environment Scope: [SIMULATION/MOCK] Pure Python standard library demonstration
================================================================================
...
Scenario ID   : RW-01 -> PASS (complete_and_consistent)
Scenario ID   : RW-02 -> FAIL (missing_asset)
Scenario ID   : RW-03 -> FLAGGED_FOR_REVIEW (unrelated_control_threat_mismatch)
...
[Q1] Type: predict_output -> Answer: FLAGGED_FOR_REVIEW | Check: PASSED
[Q2] Type: diagnose_failure -> Answer: asset | Check: PASSED
[Q3] Type: choose_boundary_policy -> Answer: strip_whitespace_reject_and_flag_unmapped_for_review | Check: PASSED
================================================================================
ASSESSMENT_CHECKS_PASSED: 3/3
================================================================================
```
