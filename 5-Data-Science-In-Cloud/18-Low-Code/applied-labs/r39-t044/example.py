"""Security-scenario rubric checker with invariant and state trace (R39-T044).

Extends the Low-Code/No-Code Cloud Data Science lesson with a structural
rubric checker across three fictional scenarios, recording step states and
validating the trace-to-verdict invariant.
"""

from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class SecurityScenario:
    scenario_id: str
    asset: Optional[str]
    threat: str
    control: str
    residual_risk: str


THREAT_CONTROL_MAP: Dict[str, Tuple[str, ...]] = {
    "pipeline_leak": ("rbac", "private endpoint", "access policy", "secret"),
    "data_poisoning": ("checksum", "validation", "schema", "hash", "integrity"),
    "webhook_tampering": ("rate limit", "hmac", "token", "signature", "authentication"),
}


def _classify_threat(threat_text: str) -> str:
    lowered = threat_text.lower()
    if "leak" in lowered or "public" in lowered or "exposure" in lowered:
        return "pipeline_leak"
    if "poison" in lowered or "tamper" in lowered or "corrupt" in lowered:
        return "data_poisoning"
    if "webhook" in lowered or "endpoint" in lowered or "flooding" in lowered:
        return "webhook_tampering"
    return "unknown"


def evaluate_scenario(scenario: SecurityScenario) -> Dict[str, Any]:
    """Evaluate structural security rubric while recording step state trace."""
    state_trace: List[Dict[str, Any]] = []

    # Step 1: Completeness verification (all required fields present and non-empty)
    missing_fields = []
    for field in ("asset", "threat", "control", "residual_risk"):
        val = getattr(scenario, field, None)
        if not val or not str(val).strip():
            missing_fields.append(field)

    step1 = {
        "step": 1,
        "name": "field_completeness",
        "asset_present": bool(scenario.asset and scenario.asset.strip()),
        "missing_fields": missing_fields,
        "complete": len(missing_fields) == 0,
    }
    state_trace.append(step1)

    if not step1["complete"]:
        return {
            "scenario_id": scenario.scenario_id,
            "verdict": "FAIL",
            "state_trace": state_trace,
            "reason": f"Missing required fields: {missing_fields}",
        }

    # Step 2: Relevance check (control keywords match threat category)
    threat_cat = _classify_threat(scenario.threat)
    expected_keywords = THREAT_CONTROL_MAP.get(threat_cat, ())
    control_lower = scenario.control.lower()
    aligned = any(kw in control_lower for kw in expected_keywords)

    step2 = {
        "step": 2,
        "name": "control_relevance",
        "threat_category": threat_cat,
        "control_aligned": aligned,
    }
    state_trace.append(step2)

    if not aligned:
        return {
            "scenario_id": scenario.scenario_id,
            "verdict": "REVIEW",
            "state_trace": state_trace,
            "reason": f"Control not clearly aligned with threat category {threat_cat}",
        }

    # Step 3: Final rubric determination
    step3 = {
        "step": 3,
        "name": "verdict_determination",
        "verdict": "PASS",
    }
    state_trace.append(step3)

    return {
        "scenario_id": scenario.scenario_id,
        "verdict": "PASS",
        "state_trace": state_trace,
        "reason": "Complete scenario with relevant control",
    }


def verify_state_trace_invariant(evaluation_result: Dict[str, Any]) -> bool:
    """Validate invariant linking intermediate state trace to final output."""
    trace = evaluation_result.get("state_trace", [])
    verdict = evaluation_result.get("verdict")

    if not trace:
        return False

    step1 = trace[0]
    if not step1.get("complete"):
        return verdict == "FAIL"

    if len(trace) > 1:
        step2 = trace[1]
        if not step2.get("control_aligned"):
            return verdict == "REVIEW"

    return verdict == "PASS"


FICTIONAL_SCENARIOS = (
    SecurityScenario(
        scenario_id="fictional_complete_pass",
        asset="Low-Code Model Pipeline Definition",
        threat="Pipeline leak exposing training dataset schema",
        control="Enforce workspace RBAC and private endpoint access policy",
        residual_risk="Low: authorized team members retain view access",
    ),
    SecurityScenario(
        scenario_id="fictional_missing_asset_fail",
        asset="",  # Missing asset
        threat="Data poisoning during automated data ingestion",
        control="Apply schema validation and sha256 checksum checks",
        residual_risk="Low: malformed payloads rejected immediately",
    ),
    SecurityScenario(
        scenario_id="fictional_unrelated_control_review",
        asset="Low-Code Prediction Webhook Endpoint",
        threat="Webhook tampering through endpoint flooding",
        control="Adjust visual report color palette to high-contrast theme",  # Unrelated
        residual_risk="High: endpoint remains vulnerable to flooding",
    ),
)


def main() -> None:
    for sc in FICTIONAL_SCENARIOS:
        res = evaluate_scenario(sc)
        inv = verify_state_trace_invariant(res)
        print(f"{sc.scenario_id}: verdict={res['verdict']} | steps={len(res['state_trace'])} | invariant_ok={inv}")


if __name__ == "__main__":
    main()
