"""Security-scenario rubric checker with invariant & state trace (R39-T004).

Extends the Azure ML SDK lesson using small fictional local fixtures and the
Python 3 standard library only (no cloud SDK calls, credentials, or models).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class SecurityScenario:
    scenario_id: str
    asset: Optional[str]
    threat: str
    control: str
    residual_risk: str


# Explicit mapping of threat categories to relevant control terms for the
# fictional Azure ML SDK lesson fixtures (structural rubric only).
THREAT_CONTROL_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    "credential_leak": ("managed identity", "key vault", "secret", "token", "rbac"),
    "data_poisoning": ("dataset", "hash", "validation", "integrity", "immutability"),
    "unauthorized_endpoint": ("authentication", "rbac", "private endpoint", "key"),
}


def _classify_threat(threat_text: str) -> str:
    lowered = threat_text.lower()
    if "credential" in lowered or "secret" in lowered or "key" in lowered:
        return "credential_leak"
    if "poison" in lowered or "tamper" in lowered or "corrupt" in lowered:
        return "data_poisoning"
    if "unauthorized" in lowered or "endpoint" in lowered or "access" in lowered:
        return "unauthorized_endpoint"
    return "unknown"


def evaluate_scenario(scenario: SecurityScenario) -> dict:
    """Evaluate a fictional security scenario and record intermediate state."""
    trace: List[dict] = []

    # Step 1: Check required structural fields (asset, threat, control, residual_risk)
    fields = {
        "asset": scenario.asset,
        "threat": scenario.threat,
        "control": scenario.control,
        "residual_risk": scenario.residual_risk,
    }
    missing_fields = [
        name for name, val in fields.items() if val is None or not str(val).strip()
    ]
    asset_present = "asset" not in missing_fields
    step1_status = "OK" if not missing_fields else "FAIL"
    trace.append(
        {
            "step": "required_fields",
            "asset_present": asset_present,
            "missing_fields": missing_fields,
            "status_after_step": step1_status,
        }
    )

    # Step 2: Check whether control is related to the named threat
    threat_category = _classify_threat(scenario.threat)
    expected_keywords = THREAT_CONTROL_KEYWORDS.get(threat_category, ())
    control_lower = scenario.control.lower()
    matched_keywords = [kw for kw in expected_keywords if kw in control_lower]
    aligned = bool(matched_keywords)
    if step1_status == "FAIL":
        step2_status = "FAIL"
    elif aligned:
        step2_status = "PASS"
    else:
        step2_status = "REVIEW"
    trace.append(
        {
            "step": "threat_control_alignment",
            "threat_category": threat_category,
            "matched_keywords": matched_keywords,
            "aligned": aligned,
            "status_after_step": step2_status,
        }
    )

    # Step 3: Finalize verdict from recorded step states
    if not asset_present or missing_fields:
        verdict = "FAIL"
    elif not aligned:
        verdict = "REVIEW"
    else:
        verdict = "PASS"

    trace.append(
        {
            "step": "finalize_verdict",
            "verdict": verdict,
            "status_after_step": verdict,
        }
    )

    return {
        "scenario": asdict(scenario),
        "verdict": verdict,
        "state_trace": trace,
    }


def verify_state_trace_invariant(result: dict) -> bool:
    """Verify the invariant linking intermediate step states to final verdict."""
    trace = result["state_trace"]
    if [s["step"] for s in trace] != [
        "required_fields",
        "threat_control_alignment",
        "finalize_verdict",
    ]:
        return False

    step1, step2, step3 = trace
    verdict = result["verdict"]
    if step3["verdict"] != verdict:
        return False

    if not step1["asset_present"] or step1["missing_fields"]:
        return verdict == "FAIL"
    if not step2["aligned"]:
        return verdict == "REVIEW"
    return verdict == "PASS"


FICTIONAL_SCENARIOS: Tuple[SecurityScenario, ...] = (
    SecurityScenario(
        scenario_id="fictional_complete_pass",
        asset="Simulated Azure ML Workspace Compute Target",
        threat="Credential leak via hardcoded workspace secret in training script",
        control="Use managed identity and Key Vault secret lookup instead of hardcoded keys",
        residual_risk="Low: compromised identity token still requires RBAC scope limits",
    ),
    SecurityScenario(
        scenario_id="fictional_missing_asset_fail",
        asset="",
        threat="Data poisoning of training dataset before pipeline registration",
        control="Enforce dataset hash validation before training run starts",
        residual_risk="Medium: upstream source corruption prior to hashing",
    ),
    SecurityScenario(
        scenario_id="fictional_unrelated_control_review",
        asset="Simulated Azure ML Inference Endpoint",
        threat="Unauthorized endpoint access from unauthenticated clients",
        control="Enable dark mode theme in local notebook editor",
        residual_risk="High: endpoint remains exposed without authentication",
    ),
)


if __name__ == "__main__":
    for sc in FICTIONAL_SCENARIOS:
        res = evaluate_scenario(sc)
        inv_ok = verify_state_trace_invariant(res)
        print(
            f"{sc.scenario_id}: verdict={res['verdict']} | "
            f"steps={len(res['state_trace'])} | invariant_ok={inv_ok}"
        )
