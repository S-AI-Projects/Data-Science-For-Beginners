"""Security scenario rubric checker for Azure ML SDK lesson.
Task R39-T051.
"""

from typing import Dict, Any, Optional, List


def classify_threat(threat_text: str) -> str:
    """Find the category for a threat."""
    t = threat_text.lower()
    if "api" in t or "unauthorized" in t or "access" in t:
        return "unauthorized_access"
    if "tamper" in t or "integrity" in t or "poison" in t:
        return "data_tampering"
    if "leak" in t or "transit" in t or "exposure" in t:
        return "data_leakage"
    return "unknown"


def check_control_matches_threat(threat_category: str, control_text: str) -> bool:
    """Check if the control is relevant to the threat category."""
    c = control_text.lower()
    keywords = {
        "unauthorized_access": ["token", "key", "rbac", "auth", "credential"],
        "data_tampering": ["integrity", "hash", "checksum", "validation"],
        "data_leakage": ["encryption", "tls", "masking", "private link"],
    }
    expected_words = keywords.get(threat_category, [])
    for word in expected_words:
        if word in c:
            return True
    return False


def evaluate_scenario(scenario: Dict[str, Optional[str]]) -> Dict[str, Any]:
    """Check a scenario against the structural rubric.

    Returns PASS, FAIL, or REVIEW.
    """
    scenario_id = scenario.get("scenario_id", "unknown")
    required_fields = ["asset", "threat", "control", "residual_risk"]

    for field in required_fields:
        val = scenario.get(field)
        if not val or not str(val).strip():
            return {
                "scenario_id": scenario_id,
                "verdict": "FAIL",
                "reason": f"Missing required field: {field}",
            }

    threat = str(scenario.get("threat"))
    control = str(scenario.get("control"))

    category = classify_threat(threat)
    if not check_control_matches_threat(category, control):
        return {
            "scenario_id": scenario_id,
            "verdict": "REVIEW",
            "reason": f"Control unrelated to threat category '{category}'",
        }

    return {
        "scenario_id": scenario_id,
        "verdict": "PASS",
        "reason": "Complete scenario with relevant control",
    }


FICTIONAL_SCENARIOS: List[Dict[str, Optional[str]]] = [
    {
        "scenario_id": "scenario_complete_pass",
        "asset": "Azure ML Model Endpoint",
        "threat": "unauthorized api access to prediction service",
        "control": "require token auth and api key headers",
        "residual_risk": "compromised client tokens",
    },
    {
        "scenario_id": "scenario_missing_asset_fail",
        "asset": None,
        "threat": "data leakage in transit across public networks",
        "control": "enforce tls encryption on endpoints",
        "residual_risk": "endpoint misconfiguration",
    },
    {
        "scenario_id": "scenario_unrelated_control_review",
        "asset": "Azure ML Training Cluster",
        "threat": "unauthorized api access to cluster node",
        "control": "increase idle node shutdown timeout to 30 minutes",
        "residual_risk": "high idle compute cost",
    },
]


def main() -> None:
    print("Evaluating fictional scenarios:")
    for sc in FICTIONAL_SCENARIOS:
        res = evaluate_scenario(sc)
        print(f"Scenario {sc.get('scenario_id')}: {res['verdict']} ({res['reason']})")


if __name__ == "__main__":
    main()
