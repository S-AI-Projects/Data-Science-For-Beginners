"""Security scenario rubric with offline service adapter.
Task R39-T055.
"""

from typing import Dict, Any, Optional, List, Callable


class LocalPolicyAdapter:
    """Deterministic local adapter standing in for an external policy service."""

    def __call__(self, threat: str, control: str) -> bool:
        """Return True if control matches the threat keywords."""
        t = threat.lower()
        c = control.lower()

        keywords = {
            "unauthorized": ["role", "access", "token", "auth", "credential"],
            "tampering": ["signature", "hash", "integrity", "verification"],
            "denial": ["rate limit", "throttle", "firewall", "capacity"],
        }

        for threat_key, control_words in keywords.items():
            if threat_key in t:
                for cw in control_words:
                    if cw in c:
                        return True
                return False

        return False

    @staticmethod
    def get_unestablished_behaviors() -> List[str]:
        """List behaviors this local mock does not establish."""
        return [
            "Live cloud identity and access management calls",
            "Network latency, retries, and timeout handling",
            "Automatic synchronization with real enterprise policy databases",
        ]


def evaluate_scenario(
    scenario: Dict[str, Optional[str]],
    adapter: Optional[Callable[[str, str], bool]] = None,
) -> Dict[str, Any]:
    """Check a scenario using the structural rubric and callable adapter."""
    if adapter is None:
        adapter = LocalPolicyAdapter()

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

    is_relevant = adapter(threat, control)
    if not is_relevant:
        return {
            "scenario_id": scenario_id,
            "verdict": "REVIEW",
            "reason": "Control unrelated to the named threat",
            "note": "Human review judges the explanation",
        }

    return {
        "scenario_id": scenario_id,
        "verdict": "PASS",
        "reason": "Complete scenario with relevant control",
        "note": "Human review judges the explanation",
    }


FICTIONAL_SCENARIOS: List[Dict[str, Optional[str]]] = [
    {
        "scenario_id": "scenario_data_pipeline_pass",
        "asset": "Raw Training Pipeline Dataset",
        "threat": "unauthorized pipeline data extraction",
        "control": "role based access control and token verification",
        "residual_risk": "compromised employee token",
    },
    {
        "scenario_id": "scenario_missing_asset_fail",
        "asset": None,
        "threat": "model container tampering in deployment registry",
        "control": "image cryptographic signature verification",
        "residual_risk": "registry key leak",
    },
    {
        "scenario_id": "scenario_unrelated_control_review",
        "asset": "Production Inference Service",
        "threat": "denial of service on prediction endpoint",
        "control": "change dashboard chart theme to dark mode",
        "residual_risk": "service outage remains untreated",
    },
]


def main() -> None:
    adapter = LocalPolicyAdapter()
    print("Evaluating lifecycle scenarios using local adapter:")
    for sc in FICTIONAL_SCENARIOS:
        res = evaluate_scenario(sc, adapter)
        print(f"Scenario {sc.get('scenario_id')}: {res['verdict']} ({res['reason']})")

    print("\nUnestablished real service behaviors:")
    for b in adapter.get_unestablished_behaviors():
        print("*", b)


if __name__ == "__main__":
    main()
