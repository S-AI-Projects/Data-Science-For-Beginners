"""Security-scenario rubric with applied scenario assessment questions (R39-T050).

Extends the Low-Code/No-Code Cloud Data Science lesson with three fictional
security scenarios and three applied assessment questions with rationales and
executable checks.
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


THREAT_CONTROL_TERMS: Dict[str, Tuple[str, ...]] = {
    "unauthorized_api_access": ("api key", "rbac", "oauth", "managed identity", "token"),
    "model_tampering": ("integrity", "hash", "checksum", "artifact validation"),
    "data_leakage": ("encryption", "masking", "private link", "tls"),
}


def _classify_threat(threat_text: str) -> str:
    t = threat_text.lower()
    if "api" in t or "unauthorized" in t or "endpoint" in t:
        return "unauthorized_api_access"
    if "tamper" in t or "poison" in t or "artifact" in t:
        return "model_tampering"
    if "leak" in t or "exfiltration" in t or "exposure" in t:
        return "data_leakage"
    return "unknown"


def evaluate_scenario(sc: SecurityScenario) -> Dict[str, Any]:
    """Evaluate scenario against structural rubric."""
    for field in ("asset", "threat", "control", "residual_risk"):
        v = getattr(sc, field, None)
        if not v or not str(v).strip():
            return {
                "scenario_id": sc.scenario_id,
                "verdict": "FAIL",
                "reason": f"Missing required field: {field}",
            }

    cat = _classify_threat(sc.threat)
    terms = THREAT_CONTROL_TERMS.get(cat, ())
    control_low = sc.control.lower()

    if not any(term in control_low for term in terms):
        return {
            "scenario_id": sc.scenario_id,
            "verdict": "REVIEW",
            "reason": f"Control unrelated to threat category '{cat}'",
        }

    return {
        "scenario_id": sc.scenario_id,
        "verdict": "PASS",
        "reason": "Complete scenario with relevant control",
    }


FICTIONAL_SCENARIOS = (
    SecurityScenario(
        scenario_id="fictional_complete_pass",
        asset="Low-Code Prediction Endpoint",
        threat="Unauthorized API access to model scoring endpoint",
        control="Enforce OAuth token authentication and RBAC authorization",
        residual_risk="Low: valid client tokens restricted to read-only scoring",
    ),
    SecurityScenario(
        scenario_id="fictional_missing_asset_fail",
        asset=None,  # Missing asset -> FAIL
        threat="Model tampering during low-code pipeline artifact publishing",
        control="Apply artifact validation and SHA256 checksum verification",
        residual_risk="Low: unverified artifacts rejected",
    ),
    SecurityScenario(
        scenario_id="fictional_unrelated_control_review",
        asset="Low-Code Feature Store Table",
        threat="Data leakage via unencrypted network transit",
        control="Increase pipeline timeout limit from 10 to 30 minutes",  # Unrelated -> REVIEW
        residual_risk="High: traffic remains exposed to network interception",
    ),
)


# --- Applied Assessment Questions ---

ASSESSMENT_QUESTIONS = {
    "q1_predict_output": {
        "question": "What is the verdict for fictional_complete_pass?",
        "predicted_output": "PASS",
        "rationale": "All four required fields are non-empty and the OAuth control corresponds directly to the unauthorized API access threat.",
    },
    "q2_diagnose_failure": {
        "question": "Why does fictional_missing_asset_fail produce a FAIL verdict?",
        "diagnosed_cause": "asset_field_none",
        "rationale": "The structural rubric strictly requires a non-empty asset; a None asset triggers immediate failure before control relevance is evaluated.",
    },
    "q3_boundary_policy": {
        "question": "What policy applies when a control cannot be matched to known threat terms?",
        "policy_choice": "flag_for_review",
        "rationale": "Automated rubrics must flag ambiguous or unmapped controls for human REVIEW rather than silently guessing or failing the submission.",
    },
}


def check_q1_predict_output() -> bool:
    """Executable check for Q1: output prediction."""
    res = evaluate_scenario(FICTIONAL_SCENARIOS[0])
    return res["verdict"] == ASSESSMENT_QUESTIONS["q1_predict_output"]["predicted_output"]


def check_q2_diagnose_failure() -> bool:
    """Executable check for Q2: failure diagnosis."""
    res = evaluate_scenario(FICTIONAL_SCENARIOS[1])
    return res["verdict"] == "FAIL" and "asset" in res["reason"]


def check_q3_boundary_policy() -> bool:
    """Executable check for Q3: boundary review policy."""
    res = evaluate_scenario(FICTIONAL_SCENARIOS[2])
    return res["verdict"] == "REVIEW"


def main() -> None:
    for sc in FICTIONAL_SCENARIOS:
        print(f"{sc.scenario_id}: {evaluate_scenario(sc)}")
    print()
    print("Applied Questions Execution:")
    print("Q1 (predict):", check_q1_predict_output())
    print("Q2 (diagnose):", check_q2_diagnose_failure())
    print("Q3 (boundary):", check_q3_boundary_policy())


if __name__ == "__main__":
    main()
