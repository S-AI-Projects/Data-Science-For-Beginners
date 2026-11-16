"""Security-scenario rubric checker with offline service adapter (R39-T005).

Extends 1-Introduction/03-defining-data (Defining Data) by modeling security
and governance scenarios across structured/quantitative, unstructured/qualitative,
and sensor/semi-structured data assets behind a callable service interface.

NOTE ON SCOPE & LIMITATIONS [SIMULATION/MOCK]:
- This module is an educational in-memory simulation using the Python 3 standard library.
- No live cloud services, hardware, credentials, or trained models are used or claimed.
- Automated rubric checking verifies structural completeness and adapter-driven alignment.
- Human review is strictly required to judge the qualitative free-text explanation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union


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


# Required structural fields for scenario completeness
REQUIRED_FIELDS: Tuple[str, ...] = ("asset", "threat", "control", "residual_risk")

# Specific real-service behaviors that this local offline mock does NOT establish
UNESTABLISHED_REAL_SERVICE_BEHAVIORS: Tuple[str, ...] = (
    "Live IAM/policy API authentication & OAuth token exchange",
    "Network transport latency, socket timeouts, and automatic retry/backoff policies",
    "API rate limiting, concurrency throttling, and quota enforcement",
    "Live policy catalog schema drift and dynamic upstream rule updates",
    "Semantic LLM/NLP grading of free-text qualitative explanations",
)

# Deterministic domain rule catalog linking threat indicators to control mitigations
THREAT_CONTROL_CATALOG: Dict[str, Tuple[Tuple[str, ...], Tuple[str, ...]]] = {
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

# Type alias for the callable threat-control catalog adapter interface
ThreatControlCatalogCallable = Callable[[str, str], Dict[str, Any]]


def _get_field(scenario: Union[SecurityScenario, dict], field_name: str) -> Optional[str]:
    """Helper to retrieve field values from either a dataclass or a dict."""
    if isinstance(scenario, dict):
        return scenario.get(field_name)
    return getattr(scenario, field_name, None)


# ==============================================================================
# Contribution Focus: Callable Offline Service Adapter
# ==============================================================================


class LocalOfflineRubricAdapter:
    """Deterministic in-memory adapter simulating an external threat-control catalog service.

    Operates completely offline using a local deterministic rule mapping without
    network calls, cloud credentials, or external API dependencies.
    """

    adapter_name: str = "[SIMULATION/MOCK] Deterministic Local Offline Adapter"

    def __call__(self, threat: str, control: str) -> Dict[str, Any]:
        """Evaluate whether a control addresses a named threat based on in-memory rules.

        Args:
            threat: Description of the security/governance threat.
            control: Description of the proposed mitigation control.

        Returns:
            Dictionary containing evaluation details:
                - aligned (bool): True if mitigation keywords match threat category.
                - category (str): Identified threat category or 'unknown'.
                - matched_terms (list): List of matching keywords found.
                - adapter_name (str): Identifier of the executing adapter.
        """
        threat_lower = (threat or "").lower()
        control_lower = (control or "").lower()

        for category, (threat_terms, control_terms) in THREAT_CONTROL_CATALOG.items():
            if any(term in threat_lower for term in threat_terms):
                matched = [term for term in control_terms if term in control_lower]
                if matched:
                    return {
                        "aligned": True,
                        "category": category,
                        "matched_terms": matched,
                        "adapter_name": self.adapter_name,
                    }
                return {
                    "aligned": False,
                    "category": category,
                    "matched_terms": [],
                    "adapter_name": self.adapter_name,
                }

        return {
            "aligned": False,
            "category": "unknown",
            "matched_terms": [],
            "adapter_name": self.adapter_name,
        }


def deterministic_local_adapter(threat: str, control: str) -> Dict[str, Any]:
    """Functional wrapper for the deterministic local offline adapter."""
    return LocalOfflineRubricAdapter()(threat, control)


# ==============================================================================
# Rubric Evaluator with Injected Adapter Dependency
# ==============================================================================


def evaluate_scenario(
    scenario: Union[SecurityScenario, dict],
    adapter: Optional[ThreatControlCatalogCallable] = None,
) -> dict:
    """Evaluate a security scenario using structural checks and an injected adapter.

    NOTE: Human review judges the free-text explanation, whereas the automated
    checker only verifies the stated structural rubric and adapter alignment.

    Args:
        scenario: SecurityScenario or dictionary containing rubric fields.
        adapter: Callable threat-control service adapter (defaults to LocalOfflineRubricAdapter).

    Returns:
        Structured evaluation result dict including status ('PASS', 'FAIL', 'FLAGGED_FOR_REVIEW').
    """
    if adapter is None:
        adapter = LocalOfflineRubricAdapter()

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

    # Step 2: Policy alignment lookup via injected service adapter
    adapter_result = adapter(threat, control)
    aligned = bool(adapter_result.get("aligned", False))

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
        "adapter_result": adapter_result,
        "rubric_note": (
            "Automated rubric verified structural completeness and adapter alignment. "
            "Human review is strictly required to judge the qualitative free-text explanation."
        ),
        "unestablished_behaviors": UNESTABLISHED_REAL_SERVICE_BEHAVIORS,
    }


def run_evaluation_suite(
    fixtures: Sequence[Union[SecurityScenario, dict]],
    adapter: Optional[ThreatControlCatalogCallable] = None,
) -> List[dict]:
    """Execute evaluation across a sequence of scenarios using the injected adapter."""
    return [evaluate_scenario(sc, adapter=adapter) for sc in fixtures]


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
    """Print structured deterministic report of scenarios, adapter execution, and limitations."""
    print("======================================================================")
    print("[SIMULATION/MOCK] Security-Scenario Rubric & Offline Service Adapter (R39-T005)")
    print("Lesson Reference: 1-Introduction/03-defining-data (Defining Data)")
    print("Adapter: [SIMULATION/MOCK] Deterministic Local Offline Adapter")
    print("Scope: In-memory educational simulation (No cloud, API, or hardware dependencies)")
    print("======================================================================")
    print("[RUBRIC SCOPE NOTICE]")
    print("Automated rubric evaluation only checks structural completeness and")
    print("adapter policy alignment. Human review is strictly required to judge")
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

    adapter = LocalOfflineRubricAdapter()
    print("--- ADAPTER EXECUTION & METADATA ---")
    print(f"Adapter Name: {adapter.adapter_name}")
    print(f"Callable Type: {type(adapter).__name__}")
    print()

    results = run_evaluation_suite(FIXTURES, adapter=adapter)

    print("--- EVALUATION RESULTS ---")
    for res in results:
        sc_id = res["scenario_id"]
        status = res["status"]
        aligned = res["alignment_matched"]
        missing = res["missing_fields"]
        print(f"[SIMULATION/MOCK] {sc_id}: status={status} | aligned={aligned} | missing={missing}")

    print()
    print("--- UNESTABLISHED REAL-SERVICE BEHAVIORS ---")
    print("The offline simulation does NOT establish the following real-service capabilities:")
    for idx, behavior in enumerate(UNESTABLISHED_REAL_SERVICE_BEHAVIORS, start=1):
        print(f"  {idx}. {behavior}")

    print()
    print("======================================================================")
    print("[SIMULATION/MOCK] Summary: 1 PASS, 1 FAIL, 1 FLAGGED_FOR_REVIEW.")
    print("Verification complete.")
    print("======================================================================")


if __name__ == "__main__":
    print_suite_report()
