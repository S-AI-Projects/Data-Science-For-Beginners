"""Check a small scenario rubric through a deterministic offline adapter."""

import argparse
from copy import deepcopy
import json


FIELDS = ("asset", "threat", "control", "residual_risk")
PAIRS = {
    "unauthorized_access": "access_review",
    "data_loss": "backups",
    "tampered_readings": "integrity_checks",
}
SCENARIOS = [
    {
        "id": "clinic-access",
        "section": "Data Science + Industry",
        "asset": "Fictional clinic appointment dataset used for demand analysis",
        "threat": "unauthorized_access",
        "control": "access_review",
        "residual_risk": "An approved account could still misuse its access.",
    },
    {
        "id": "poetry-archive",
        "section": "Data Science + Humanities",
        "asset": "Fictional archive of transcribed poems and annotation history",
        "threat": "data_loss",
        "control": "backups",
        "residual_risk": "Edits since the last backup could still be lost.",
    },
    {
        "id": "habitat-feed",
        "section": "Data Science + Sustainability",
        "asset": "Fictional habitat sensor readings used in a dashboard",
        "threat": "tampered_readings",
        "control": "integrity_checks",
        "residual_risk": "A faulty sensor may send authentic but inaccurate data.",
    },
]


def local_relation(threat, control):
    """Mock relation service: exact labels only; unknown labels return None.

    Callable contract: (threat: str, control: str) -> True, False or None.
    True means listed pair; False means known labels but a different pair;
    None means unsupported labels. This does not evaluate free-text rationale.
    """
    if threat not in PAIRS or control not in PAIRS.values():
        return None
    return PAIRS[threat] == control


def check_scenario(scenario, relation_check=local_relation):
    """Check completeness and delegate the label relation to a callable.

    Fail incomplete structure; send mismatches, unknowns and unavailable
    adapters for review. Human explanation quality is outside this rubric.
    """
    if not isinstance(scenario, dict):
        return {"status": "fail", "issues": ["scenario must be an object"]}
    missing = [field for field in FIELDS
               if not isinstance(scenario.get(field), str)
               or not scenario[field].strip()]
    if missing:
        return {"status": "fail",
                "issues": ["missing or invalid: " + field for field in missing]}
    try:
        relation = relation_check(scenario["threat"], scenario["control"])
    except OSError:
        return {"status": "review", "issues": ["relation adapter unavailable"]}
    if relation is True:
        return {"status": "pass", "issues": []}
    if relation is False:
        return {"status": "review", "issues": ["threat/control pair not listed"]}
    return {"status": "review", "issues": ["relation unknown or invalid response"]}


def fixture(case="complete"):
    """Return independent fixture copies, including deliberate rubric defects."""
    scenarios = deepcopy(SCENARIOS)
    if case == "missing-asset":
        del scenarios[0]["asset"]
    elif case == "unrelated-control":
        scenarios[0]["control"] = "backups"
    elif case != "complete":
        raise ValueError("unknown fixture case")
    return scenarios


def main():
    """Run fixtures or one JSON scenario; exit 0/pass, 1/fail, 3/review."""
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--case", default="complete",
                        choices=("complete", "missing-asset", "unrelated-control"))
    inputs.add_argument("--scenario", help="one JSON scenario instead of the fixture")
    args = parser.parse_args()
    try:
        scenarios = ([json.loads(args.scenario)] if args.scenario is not None
                     else fixture(args.case))
    except ValueError as error:
        parser.error(str(error))
    results = [check_scenario(scenario) for scenario in scenarios]
    print(json.dumps({"adapter": "deterministic-local-mock", "results": results}))
    if any(result["status"] == "fail" for result in results):
        return 1
    if any(result["status"] == "review" for result in results):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
