"""Security-scenario rubric checker and refactoring equivalence (R39-T006).

Extends 1-Introduction/03-defining-data (Defining Data) by modeling security
and governance scenarios across structured/quantitative, unstructured/qualitative,
and sensor/semi-structured data assets.

NOTE ON SCOPE & LIMITATIONS [SIMULATION/MOCK]:
- This module is a purely local in-memory simulation using the Python 3 standard library.
- No real cloud service, hardware, credential, or trained model is required or claimed.
- Automated rubric checking verifies structural completeness and threat-control alignment.
- Human review is strictly required to judge the qualitative free-text explanation and
  contextual security rationale.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Sequence, Tuple, Union


@dataclass(frozen=True)
class SecurityScenario:
    """Represents a data governance/security scenario under evaluation.

    Attributes:
        scenario_id: Unique string identifier for the scenario.
        asset: The data asset being protected (structured, unstructured, etc.).
        threat: The security or governance threat directed at the asset.
        control: The proposed mitigation or governance control.
        residual_risk: Expected residual risk after control implementation.
        explanation: Free-text qualitative rationale intended for human review.
    """

    scenario_id: str
    asset: Optional[str]
    threat: str
    control: str
    residual_risk: str
    explanation: str


# Mapping of threat categories to (threat_indicators, control_mitigation_keywords).
# Grounded in data definitions: structured/quantitative DB, qualitative files, sensor streams.
THREAT_CONTROL_ALIGNMENT_RULES: Dict[str, Tuple[Tuple[str, ...], Tuple[str, ...]]] = {
    "sql_injection": (
        ("sql injection", "database injection", "unauthorized query"),
        ("parameterized", "prepared statement", "type validation", "query validation", "sql"),
    ),
    "storage_exposure": (
        ("unencrypted", "storage leak", "storage exposure", "unauthorized extraction", "file leak"),
        ("encryption", "aes", "access control list", "at-rest encryption"),
    ),
    "sensor_tampering": (
        ("spoofing", "tampering", "telemetry corruption", "data poisoning"),
        ("cryptographic", "signing", "hmac", "checksum", "payload verification", "tls", "integrity"),
    ),
}

REQUIRED_FIELDS: Tuple[str, ...] = ("asset", "threat", "control", "residual_risk")


def _get_field(scenario: Union[SecurityScenario, dict], field_name: str) -> Optional[str]:
    """Helper to retrieve field values from either a dataclass or a dict."""
    if isinstance(scenario, dict):
        return scenario.get(field_name)
    return getattr(scenario, field_name, None)


# ==============================================================================
# Extracted Responsibility: Dedicated Pure Helper Function
# ==============================================================================


def check_threat_control_alignment(threat: str, control: str) -> bool:
    """Verify alignment between a security threat and a proposed control.

    Extracted responsibility refactoring:
    Pure helper function isolating threat-to-control heuristic keyword
    alignment from overall scenario validation and structural rubric checks.

    Args:
        threat: Description of the security/governance threat.
        control: Description of the proposed control/mitigation.

    Returns:
        True if the control matches the expected mitigation patterns for the threat;
        False otherwise.
    """
    threat_lower = (threat or "").lower()
    control_lower = (control or "").lower()

    for _category, (threat_terms, control_terms) in THREAT_CONTROL_ALIGNMENT_RULES.items():
        if any(term in threat_lower for term in threat_terms):
            if any(term in control_lower for term in control_terms):
                return True
    return False


# ==============================================================================
# Baseline Rubric Evaluator (Monolithic Teaching Baseline)
# ==============================================================================


def evaluate_scenario_baseline(scenario: Union[SecurityScenario, dict]) -> dict:
    """Evaluate a security scenario using the baseline monolithic rubric implementation.

    NOTE: Human review judges the free-text explanation, whereas the automated
    checker only verifies the stated structural rubric and keyword alignment.

    Args:
        scenario: SecurityScenario or dictionary containing rubric fields.

    Returns:
        Structured evaluation result dict including status ('PASS', 'FAIL', 'FLAGGED_FOR_REVIEW').
    """
    scenario_id = _get_field(scenario, "scenario_id") or "unknown_scenario"
    asset = _get_field(scenario, "asset")
    threat = _get_field(scenario, "threat") or ""
    control = _get_field(scenario, "control") or ""
    residual_risk = _get_field(scenario, "residual_risk") or ""
    explanation = _get_field(scenario, "explanation") or ""

    # Step 1: Structural completeness check
    missing_fields: List[str] = []
    field_map = {
        "asset": asset,
        "threat": threat,
        "control": control,
        "residual_risk": residual_risk,
    }
    for field_name in REQUIRED_FIELDS:
        val = field_map.get(field_name)
        if val is None or not str(val).strip():
            missing_fields.append(field_name)

    # Step 2: Monolithic inline threat-control alignment check
    threat_lower = threat.lower()
    control_lower = control.lower()
    aligned = False
    for _category, (threat_terms, control_terms) in THREAT_CONTROL_ALIGNMENT_RULES.items():
        if any(term in threat_lower for term in threat_terms):
            if any(term in control_lower for term in control_terms):
                aligned = True
                break

    # Step 3: Rubric status determination
    if missing_fields:
        status = "FAIL"
    elif not aligned:
        status = "FLAGGED_FOR_REVIEW"
    else:
        status = "PASS"

    return {
        "scenario_id": scenario_id,
        "status": status,
        "asset": asset,
        "threat": threat,
        "control": control,
        "residual_risk": residual_risk,
        "explanation": explanation,
        "missing_fields": missing_fields,
        "alignment_matched": aligned,
        "rubric_note": (
            "Automated rubric verified structural completeness and threat-control alignment. "
            "Human review is required to judge the qualitative free-text explanation."
        ),
    }


# ==============================================================================
# Refactored Rubric Evaluator (Delegated Architecture)
# ==============================================================================


def evaluate_scenario_refactored(scenario: Union[SecurityScenario, dict]) -> dict:
    """Evaluate a security scenario using the refactored rubric implementation.

    Extracted responsibility:
    Delegates threat-control alignment checking to check_threat_control_alignment.

    NOTE: Human review judges the free-text explanation, whereas the automated
    checker only verifies the stated structural rubric and keyword alignment.

    Args:
        scenario: SecurityScenario or dictionary containing rubric fields.

    Returns:
        Structured evaluation result dict matching the exact contract of baseline.
    """
    scenario_id = _get_field(scenario, "scenario_id") or "unknown_scenario"
    asset = _get_field(scenario, "asset")
    threat = _get_field(scenario, "threat") or ""
    control = _get_field(scenario, "control") or ""
    residual_risk = _get_field(scenario, "residual_risk") or ""
    explanation = _get_field(scenario, "explanation") or ""

    # Step 1: Structural completeness check
    missing_fields: List[str] = []
    field_map = {
        "asset": asset,
        "threat": threat,
        "control": control,
        "residual_risk": residual_risk,
    }
    for field_name in REQUIRED_FIELDS:
        val = field_map.get(field_name)
        if val is None or not str(val).strip():
            missing_fields.append(field_name)

    # Step 2: Delegated threat-control alignment check (pure helper)
    aligned = check_threat_control_alignment(threat, control)

    # Step 3: Rubric status determination
    if missing_fields:
        status = "FAIL"
    elif not aligned:
        status = "FLAGGED_FOR_REVIEW"
    else:
        status = "PASS"

    return {
        "scenario_id": scenario_id,
        "status": status,
        "asset": asset,
        "threat": threat,
        "control": control,
        "residual_risk": residual_risk,
        "explanation": explanation,
        "missing_fields": missing_fields,
        "alignment_matched": aligned,
        "rubric_note": (
            "Automated rubric verified structural completeness and threat-control alignment. "
            "Human review is required to judge the qualitative free-text explanation."
        ),
    }


def run_baseline_suite(fixtures: Sequence[Union[SecurityScenario, dict]]) -> List[dict]:
    """Execute the baseline evaluator across a suite of scenarios."""
    return [evaluate_scenario_baseline(sc) for sc in fixtures]


def run_refactored_suite(fixtures: Sequence[Union[SecurityScenario, dict]]) -> List[dict]:
    """Execute the refactored evaluator across a suite of scenarios."""
    return [evaluate_scenario_refactored(sc) for sc in fixtures]


# ==============================================================================
# Fictional Scenarios Grounded in 03-defining-data
# ==============================================================================

FIXTURES: Tuple[SecurityScenario, ...] = (
    # Scenario 1 (Normal / Complete & Consistent): PASS
    SecurityScenario(
        scenario_id="scenario_1_quantitative_primary_store",
        asset="Customer Transactions Database (Structured Relational Primary Store)",
        threat="SQL injection leading to unauthorized extraction of quantitative financial records",
        control="Enforce parameterized SQL queries and strict column data-type validation",
        residual_risk="Low: Zero-day database engine vulnerabilities remain possible",
        explanation=(
            "Primary transaction records represent quantitative structured data requiring "
            "strict input parameterization to prevent SQL injection and data exfiltration."
        ),
    ),
    # Scenario 2 (Boundary / Missing Asset): FAIL
    SecurityScenario(
        scenario_id="scenario_2_missing_asset_boundary",
        asset="",  # Deliberately empty asset to test structural completeness failure
        threat="Unencrypted secondary survey storage leading to leak of qualitative feedback responses",
        control="Enforce AES-256 at-rest encryption and access control lists for secondary file stores",
        residual_risk="Low: Key rotation failure or compromised credentials",
        explanation=(
            "Qualitative survey comments stored as secondary data must be encrypted at rest, "
            "but asset metadata is missing from the submission."
        ),
    ),
    # Scenario 3 (Review / Unrelated Control): FLAGGED_FOR_REVIEW
    SecurityScenario(
        scenario_id="scenario_3_unstructured_sensor_review",
        asset="Unstructured Environmental Sensor Stream (Primary Semi-Structured JSON Source)",
        threat="Telemetry spoofing and data tampering injecting corrupt temperature readings",
        control="Switch presentation slide theme to high-contrast dark mode",
        residual_risk="High: Corrupted sensor packets still compromise downstream analytical pipelines",
        explanation=(
            "Primary sensor streams can be spoofed, but modifying presentation themes does "
            "not address network payload integrity or telemetry authentication."
        ),
    ),
)


def print_suite_report() -> None:
    """Print structured deterministic report comparing baseline and refactored rubric."""
    print("======================================================================")
    print("[SIMULATION/MOCK] Security-Scenario Rubric Checker (R39-T006)")
    print("Lesson Reference: 1-Introduction/03-defining-data (Defining Data)")
    print("Scope: In-memory educational simulation (No cloud, API, or hardware dependencies)")
    print("======================================================================")
    print("[RUBRIC SCOPE NOTICE]")
    print("Automated rubric evaluation only checks structural completeness and")
    print("threat-control alignment. Human review is strictly required to judge")
    print("the qualitative free-text explanation and contextual security rationale.")
    print("======================================================================")
    print()

    print("--- FIXTURE SCENARIOS (INPUTS) ---")
    for idx, sc in enumerate(FIXTURES, start=1):
        asset_display = sc.asset if sc.asset else "(missing/empty)"
        print(f"[SIMULATION/MOCK] Scenario {idx}:")
        print(f"  ID: {sc.scenario_id}")
        print(f"  Asset: {asset_display}")
        print(f"  Threat: {sc.threat}")
        print(f"  Control: {sc.control}")
        print(f"  Residual Risk: {sc.residual_risk}")
        print(f"  Explanation: {sc.explanation}")
        print()

    # Run baseline and refactored evaluation suites
    baseline_results = run_baseline_suite(FIXTURES)
    refactored_results = run_refactored_suite(FIXTURES)
    equivalence_verified = baseline_results == refactored_results

    print("--- BASELINE VS. REFACTORED EQUIVALENCE ---")
    print(f"Baseline results count: {len(baseline_results)}")
    print(f"Refactored results count: {len(refactored_results)}")
    print(f"EQUIVALENCE_VERIFIED: {equivalence_verified}")
    print()

    print("--- EVALUATION RESULTS ---")
    for res in refactored_results:
        sc_id = res["scenario_id"]
        status = res["status"]
        aligned = res["alignment_matched"]
        missing = res["missing_fields"]
        print(f"[SIMULATION/MOCK] {sc_id}: status={status} | aligned={aligned} | missing={missing}")

    print()
    print("======================================================================")
    print("[SIMULATION/MOCK] Summary: 1 PASS, 1 FAIL, 1 FLAGGED_FOR_REVIEW.")
    print("Verification complete.")
    print("======================================================================")


if __name__ == "__main__":
    print_suite_report()
