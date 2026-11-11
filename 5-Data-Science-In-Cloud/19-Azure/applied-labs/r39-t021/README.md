# Applied Lab R39-T021: Security-Scenario Rubric Checker

This lab extends the lesson [Data Science in the Cloud: The "Azure ML SDK" way](../../README.md) with a local structural rubric checker for cloud security threat modeling.

## Concept Overview
When operating machine learning workflows in the cloud (such as Azure ML SDK), practitioners must evaluate security risks across four structural dimensions:
1. **Asset:** The resource to protect (e.g., training datasets, model weights, API endpoints).
2. **Threat:** The anticipated security risk (e.g., exfiltration, unauthorized access, data poisoning).
3. **Control:** The mitigation measure (e.g., TLS encryption, RBAC, OAuth2 authentication).
4. **Residual Risk:** The remaining risk after control application.

## Automated Rubric Rules
- **PASS:** Complete scenario where the control addresses the named threat.
- **FAIL:** Missing required structural fields (e.g., missing asset).
- **FLAGGED_FOR_REVIEW:** Control is unrelated to the named threat (requires human review).

## Scope and Limitations
- **Local Fixture:** Runs entirely within the Python standard library.
- **No Cloud Dependencies:** Does not require Azure credentials, active subscriptions, or GPU hardware.
- **Structural Validation:** Automates structural rubric checks; domain explanations are judged by human review.

## Running Tests
Run the test suite locally using `unittest`:
```bash
python3 -m unittest discover -s . -p "test_*.py" -v
```
