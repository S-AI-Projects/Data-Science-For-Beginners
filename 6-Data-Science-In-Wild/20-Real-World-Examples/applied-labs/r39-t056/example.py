"""Security scenario rubric with refactoring example.
Task R39-T056.
"""

from typing import Dict, Any, Optional, List


# ----------------------------------------------------------------------
# Baseline Monolithic Implementation
# ----------------------------------------------------------------------
def evaluate_scenario_baseline(scenario: Dict[str, Optional[str]]) -> Dict[str, Any]:
    """Baseline monolithic implementation evaluating structure and alignment."""
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

    threat = str(scenario.get("threat")).lower()
    control = str(scenario.get("control")).lower()

    # Monolithic inline keyword check
    aligned = False
    if "spoofing" in threat and ("sensor" in control or "tls" in control or "auth" in control):
        aligned = True
    elif "leak" in threat and ("encrypt" in control or "mask" in control or "access" in control):
        aligned = True
    elif "tamper" in threat and ("integrity" in control or "signature" in control or "hash" in control):
        aligned = True

    if not aligned:
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


# ----------------------------------------------------------------------
# Refactored Implementation (Extracted Responsibility: ControlAlignmentValidator)
# ----------------------------------------------------------------------
class ControlAlignmentValidator:
    """Extracted named responsibility: evaluates relevance between threat and control."""

    def __init__(self) -> None:
        self.rules = {
            "spoofing": ["sensor", "tls", "auth"],
            "leak": ["encrypt", "mask", "access"],
            "tamper": ["integrity", "signature", "hash"],
        }

    def is_aligned(self, threat: str, control: str) -> bool:
        t = threat.lower()
        c = control.lower()
        for threat_key, control_words in self.rules.items():
            if threat_key in t:
                for word in control_words:
                    if word in c:
                        return True
                return False
        return False


def evaluate_scenario_refactored(
    scenario: Dict[str, Optional[str]],
    validator: Optional[ControlAlignmentValidator] = None,
) -> Dict[str, Any]:
    """Refactored implementation delegating alignment check to extracted validator."""
    if validator is None:
        validator = ControlAlignmentValidator()

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

    if not validator.is_aligned(threat, control):
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
        "scenario_id": "real_world_healthcare_pass",
        "asset": "Hospital Patient Records Database",
        "threat": "data leak through unencrypted backups",
        "control": "enforce aes encrypt at rest and role based access",
        "residual_risk": "insider credentials leak",
    },
    {
        "scenario_id": "real_world_missing_asset_fail",
        "asset": None,
        "threat": "smart farm sensor telemetry spoofing",
        "control": "sensor device mutual tls auth",
        "residual_risk": "physical device theft",
    },
    {
        "scenario_id": "real_world_finance_review",
        "asset": "Credit Scoring Inference Endpoint",
        "threat": "tamper with scoring model weights",
        "control": "change application color scheme to dark mode",
        "residual_risk": "unauthorized weight alterations remain possible",
    },
]


def check_equivalence_on_fixture() -> bool:
    """Verifies that baseline and refactored versions give identical outputs."""
    for sc in FICTIONAL_SCENARIOS:
        baseline = evaluate_scenario_baseline(sc)
        refactored = evaluate_scenario_refactored(sc)
        if baseline != refactored:
            return False
    return True


def main() -> None:
    print("Checking baseline vs refactored equivalence:", check_equivalence_on_fixture())
    print("\nRefactored evaluation outputs:")
    for sc in FICTIONAL_SCENARIOS:
        res = evaluate_scenario_refactored(sc)
        print(f"Scenario {sc.get('scenario_id')}: {res['verdict']} ({res['reason']})")


if __name__ == "__main__":
    main()
