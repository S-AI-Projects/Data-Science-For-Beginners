"""Cloud security-scenario rubric and failure-and-recovery stream processor (R39-T008).

Extends 5-Data-Science-In-Cloud/17-Introduction (Introduction to Data Science in the Cloud)
by modeling cloud security/governance scenarios (cloud storage buckets, shared compute
clusters, streaming data ingestion) with robust error explanations and stream recovery.

NOTE ON SCOPE & LIMITATIONS [SIMULATION/MOCK]:
- This module is an educational in-memory standard-library simulation.
- No live cloud accounts (AWS/Azure/GCP), SDK credentials, hardware, or models are required or claimed.
- Automated checks verify structural schema presence and heuristic threat-control alignment.
- Human review is strictly required to evaluate the qualitative free-text explanation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


@dataclass(frozen=True)
class SecurityScenario:
    """Represents a cloud data-science governance/security scenario under evaluation.

    Attributes:
        scenario_id: Unique string identifier for the scenario.
        asset: The cloud data science asset (e.g., storage account, compute cluster).
        threat: Cloud security threat directed at the asset.
        control: Proposed mitigation or cloud governance control.
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

# Threat categories and expected mitigation keywords for cloud data-science assets
CLOUD_ALIGNMENT_RULES: Dict[str, Tuple[Tuple[str, ...], Tuple[str, ...]]] = {
    "cloud_storage_exposure": (
        ("exfiltration", "public internet", "exposure", "data leak", "blob access"),
        ("private endpoint", "disable public", "rbac", "iam", "access tier", "encryption"),
    ),
    "stream_interception": (
        ("interception", "tampering", "man-in-the-middle", "spoofing", "injection"),
        ("tls", "certificate", "mutual authentication", "token", "mtls"),
    ),
    "compute_privilege_escalation": (
        ("privilege escalation", "root access", "breakout", "unauthorized shell", "node compromise"),
        ("least privilege", "isolation", "rootless", "hardening", "rbac", "seccomp"),
    ),
}


def _get_field(scenario: Union[SecurityScenario, dict], field_name: str) -> Optional[str]:
    """Helper to extract field values from either a dataclass or a dict."""
    if isinstance(scenario, dict):
        return scenario.get(field_name)
    return getattr(scenario, field_name, None)


def check_threat_control_alignment(threat: str, control: str) -> bool:
    """Verify alignment between cloud threat and proposed control."""
    threat_lower = (threat or "").lower()
    control_lower = (control or "").lower()

    for _category, (threat_terms, control_terms) in CLOUD_ALIGNMENT_RULES.items():
        if any(term in threat_lower for term in threat_terms):
            if any(term in control_lower for term in control_terms):
                return True
    return False


def evaluate_scenario(scenario: Union[SecurityScenario, dict]) -> Dict[str, Any]:
    """Evaluate a single cloud security scenario against the structural rubric.

    NOTE: Human review judges the free-text explanation, whereas the automated
    checker only verifies the stated structural rubric and keyword alignment.

    Args:
        scenario: SecurityScenario or dictionary containing rubric fields.

    Returns:
        Structured evaluation result dict including status ('PASS', 'FAIL', 'FLAGGED_FOR_REVIEW'),
        missing_fields, error_code, error_explanation, and human review notes.
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

    # Step 2: Alignment check
    aligned = check_threat_control_alignment(threat, control)

    # Step 3: Status determination and structured error explanation
    error_code: Optional[str] = None
    error_explanation: Optional[str] = None

    if missing_fields:
        status = "FAIL"
        error_code = "MISSING_REQUIRED_FIELD"
        missing_list_str = ", ".join(f"'{f}'" for f in missing_fields)
        error_explanation = (
            f"Validation failed: required field(s) {missing_list_str} missing or empty. "
            "A complete cloud security submission must explicitly name the target asset, threat, "
            "control, and residual risk before automated policy validation."
        )
    elif not aligned:
        status = "FLAGGED_FOR_REVIEW"
        error_code = "CONTROL_THREAT_MISALIGNMENT"
        error_explanation = (
            "Review required: proposed control does not contain recognized mitigation patterns "
            "addressing the specified cloud threat. Forwarding to human expert for context analysis."
        )
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
        "error_code": error_code,
        "error_explanation": error_explanation,
        "recovered_after_failure": False,
        "recovered": False,
        "rubric_note": (
            "Automated rubric verified structural completeness and threat-control alignment. "
            "Human review is strictly required to judge the qualitative free-text explanation."
        ),
    }


def process_scenario_stream(
    scenarios: Sequence[Union[SecurityScenario, dict]],
) -> List[Dict[str, Any]]:
    """Process a stream or batch of scenarios, demonstrating failure isolation and recovery.

    When an invalid or missing-data item fails, the error is recorded with a structured
    explanation without crashing the pipeline, and the very next valid input recovers
    cleanly with recovered_after_failure=True.

    Args:
        scenarios: Sequence of scenarios to evaluate sequentially.

    Returns:
        List of structured result dictionaries with recovery annotations.
    """
    results: List[Dict[str, Any]] = []
    consecutive_failure = False

    for item in scenarios:
        try:
            res = evaluate_scenario(item)
        except Exception as exc:  # Malformed payload fallback
            item_id = str(item.get("scenario_id", "malformed_item")) if isinstance(item, dict) else "malformed_item"
            res = {
                "scenario_id": item_id,
                "status": "FAIL",
                "asset": None,
                "threat": "",
                "control": "",
                "residual_risk": "",
                "explanation": "",
                "missing_fields": ["payload"],
                "alignment_matched": False,
                "error_code": "MALFORMED_PAYLOAD",
                "error_explanation": f"Malformed scenario payload caused unhandled parsing error: {exc}",
                "recovered_after_failure": False,
                "recovered": False,
                "rubric_note": "Malformed input rejected safely without crashing pipeline.",
            }

        if res["status"] == "FAIL":
            consecutive_failure = True
            res["recovered_after_failure"] = False
            res["recovered"] = False
        else:
            if consecutive_failure:
                res["recovered_after_failure"] = True
                res["recovered"] = True
                consecutive_failure = False
            else:
                res["recovered_after_failure"] = False
                res["recovered"] = False

        results.append(res)

    return results


# ==============================================================================
# Fictional Scenarios Grounded in 5-Data-Science-In-Cloud/17-Introduction
# ==============================================================================

FIXTURES: Tuple[SecurityScenario, ...] = (
    # Scenario 1 (Normal / Complete & Consistent): PASS
    SecurityScenario(
        scenario_id="cloud_storage_bucket_pass",
        asset="Cloud Data Lake Storage Account (Raw Training Datasets)",
        threat="Public internet exposure and unauthenticated data exfiltration of sensitive training datasets",
        control="Enforce private endpoints, disable public blob access, and mandate RBAC IAM roles",
        residual_risk="Low: Compromised credential with granted RBAC permissions",
        explanation=(
            "Cloud data lake stores raw training datasets; disabling public internet exposure and "
            "mandating private endpoints and IAM RBAC ensures strict boundary defenses."
        ),
    ),
    # Scenario 2 (Boundary / Missing Asset — Documented Invalid/Missing-Data Case): FAIL
    SecurityScenario(
        scenario_id="cloud_ingestion_pipeline_missing_asset",
        asset="",  # Empty/missing asset field triggers structured failure
        threat="Man-in-the-middle interception and data tampering in real-time stream ingestion",
        control="Enforce TLS 1.3 encryption in transit and mutual certificate authentication",
        residual_risk="Low: Endpoint configuration drift during auto-scaling events",
        explanation=(
            "Streaming telemetry requires mutual TLS in transit, but the submission lacks an asset definition."
        ),
    ),
    # Scenario 3 (Review / Unrelated Control): FLAGGED_FOR_REVIEW
    SecurityScenario(
        scenario_id="shared_compute_cluster_review",
        asset="Shared Cloud VM Compute Cluster (Distributed Model Training)",
        threat="Privilege escalation and unauthorized root shell access on shared training nodes",
        control="Update corporate logo watermark on exported PDF reports",
        residual_risk="High: Compute nodes remain vulnerable to privilege escalation and container breakout",
        explanation=(
            "Shared training compute requires container hardening and non-root policies; modifying "
            "report watermarks provides zero protection against node privilege escalation."
        ),
    ),
)


def print_suite_report() -> None:
    """Print deterministic formatted report showing rubric results and recovery pipeline."""
    print("======================================================================")
    print("[SIMULATION/MOCK] Cloud Security-Scenario Rubric & Recovery Pipeline (R39-T008)")
    print("Lesson Reference: 5-Data-Science-In-Cloud/17-Introduction")
    print("Scope: Local standard-library cloud security rubric & stream recovery")
    print("No live cloud provider (Azure/AWS/GCP), hardware, or models claimed.")
    print("======================================================================")
    print("[RUBRIC SCOPE NOTICE]")
    print("Automated rubric evaluation only checks structural completeness and")
    print("cloud threat-control alignment. Human review is strictly required to judge")
    print("the qualitative free-text explanation and contextual security rationale.")
    print("======================================================================")
    print()

    print("--- 1. CORE RUBRIC SCENARIOS ---")
    for sc in FIXTURES:
        res = evaluate_scenario(sc)
        asset_str = sc.asset if sc.asset else "(missing/empty)"
        print(f"[SIMULATION/MOCK] {res['scenario_id']}: status={res['status']}")
        print(f"  Asset: {asset_str}")
        print(f"  Threat: {sc.threat}")
        print(f"  Control: {sc.control}")
        if res["error_explanation"]:
            print(f"  Error Explanation: {res['error_explanation']}")
        print()

    print("--- 2. FAILURE AND RECOVERY STREAM PIPELINE ---")
    print("Simulating stream: [Scenario 1 (Valid) -> Scenario 2 (Invalid/Missing) -> Scenario 3 (Valid Review)]")
    stream_results = process_scenario_stream(FIXTURES)
    for res in stream_results:
        sc_id = res["scenario_id"]
        status = res["status"]
        recovered = res["recovered_after_failure"]
        err = res.get("error_code") or "None"
        print(f"[SIMULATION/MOCK] Stream Step: id={sc_id} | status={status} | error_code={err} | recovered_after_failure={recovered}")

    print()
    print("--- RECOVERY VERIFICATION SUMMARY ---")
    step2 = stream_results[1]
    step3 = stream_results[2]
    print(f"Step 2 failed with error code: {step2['error_code']}")
    print(f"Step 3 recovered cleanly on next valid input: {step3['recovered_after_failure']}")
    print("Recovery verified: True")
    print()
    print("======================================================================")
    print("[SIMULATION/MOCK] Summary: 1 PASS, 1 FAIL, 1 FLAGGED_FOR_REVIEW.")
    print("Verification complete.")
    print("======================================================================")


if __name__ == "__main__":
    print_suite_report()
