"""Check the structure of fictional cloud-data risk scenarios.

The checker validates required explanations and a small, explicit
threat-to-control rubric. It does not judge whether an explanation is
persuasive or whether a real deployment is secure; those require human review.
The category pairs are illustrative rubric data, not a cloud-security standard.
"""

from dataclasses import dataclass
from typing import Mapping


THREAT_CONTROLS = {
    "unauthorized_access": {"identity_access_management", "encryption"},
    "data_loss": {"backups", "replication"},
    "service_disruption": {"autoscaling", "failover"},
}


@dataclass(frozen=True)
class CheckResult:
    status: str
    issues: tuple[str, ...]


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_scenario(scenario: Mapping[str, object]) -> CheckResult:
    """Return pass, fail, or review based only on the stated rubric structure."""
    issues = []
    for field in ("asset", "residual_risk"):
        if not _nonempty_text(scenario.get(field)):
            issues.append(f"missing or empty {field}")

    threat = scenario.get("threat")
    if not isinstance(threat, Mapping):
        issues.append("missing or invalid threat")
        threat = {}
    elif not _nonempty_text(threat.get("description")):
        issues.append("missing or empty threat description")

    control = scenario.get("control")
    if not isinstance(control, Mapping):
        issues.append("missing or invalid control")
        control = {}
    elif not _nonempty_text(control.get("rationale")):
        issues.append("missing or empty control rationale")

    if issues:
        return CheckResult("fail", tuple(issues))

    threat_category = threat.get("category")
    control_category = control.get("category")
    if (
        not isinstance(threat_category, str)
        or not threat_category.strip()
        or not isinstance(control_category, str)
        or not control_category.strip()
    ):
        return CheckResult("fail", ("missing or empty threat/control category",))

    relevant_controls = THREAT_CONTROLS.get(threat_category)
    if relevant_controls is None or control_category not in relevant_controls:
        return CheckResult(
            "review",
            ("control category is not listed for this threat; human review required",),
        )

    return CheckResult("pass", ())


SCENARIOS = (
    {
        "name": "Protecting live sentiment data",
        "lesson_section": "Real-time social media sentiment analysis",
        "asset": "Streaming posts and the derived sentiment results",
        "threat": {
            "category": "unauthorized_access",
            "description": "A person without permission reads the analytics output.",
        },
        "control": {
            "category": "identity_access_management",
            "rationale": "Limit the analytics workspace to approved project roles.",
        },
        "residual_risk": "An authorized account could still be compromised.",
    },
    {
        "name": "Retaining research-paper results",
        "lesson_section": "Scientific papers analysis",
        "asset": "",
        "threat": {
            "category": "data_loss",
            "description": "Processed paper annotations could be accidentally deleted.",
        },
        "control": {
            "category": "backups",
            "rationale": "Keep recoverable copies of the processed annotations.",
        },
        "residual_risk": "A recent change might not yet be included in a backup.",
    },
    {
        "name": "Protecting a paper-analysis dashboard",
        "lesson_section": "Scientific papers analysis",
        "asset": "The research-paper dashboard and its stored results",
        "threat": {
            "category": "unauthorized_access",
            "description": "A person without permission views unpublished research results.",
        },
        "control": {
            "category": "autoscaling",
            "rationale": "Add capacity when dashboard traffic increases.",
        },
        "residual_risk": "A permitted user could still share results inappropriately.",
    },
)


def main() -> None:
    for scenario in SCENARIOS:
        result = check_scenario(scenario)
        print(f"{scenario['name']}: {result.status}")
        for issue in result.issues:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
