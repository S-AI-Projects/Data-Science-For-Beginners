"""Check the structure of fictional lifecycle security scenarios locally."""

import argparse
from copy import deepcopy
import json


FIELDS = ("asset", "threat", "control", "residual_risk")
PAIRS = {
    "departed_account_access": "revoke_departed_access",
    "unauthorized_changes": "restrict_writers",
    "exposed_storage": "encrypt_storage",
}
SCENARIOS = [
    {
        "id": "departed-analyst",
        "section": "Maintaining / Securing the Data",
        "asset": "Fictional community survey dataset",
        "threat": "departed_account_access",
        "control": "revoke_departed_access",
        "residual_risk": "Previously downloaded copies may still exist.",
    },
    {
        "id": "report-edit",
        "section": "Maintaining / Securing the Data",
        "asset": "Fictional shared dataset used for a monthly report",
        "threat": "unauthorized_changes",
        "control": "restrict_writers",
        "residual_risk": "An authorized writer could still make an incorrect edit.",
    },
    {
        "id": "stored-survey",
        "section": "Maintaining / Securing the Data",
        "asset": "Fictional stored survey export",
        "threat": "exposed_storage",
        "control": "encrypt_storage",
        "residual_risk": "A user with decryption access could still disclose data.",
    },
]


def check_scenario(scenario):
    """Fail incomplete fields, pass listed label pairs, review other pairs.

    A pass applies only to this structural rubric. Human review must assess
    the explanation and evidence; no semantic or security assessment is made.
    """
    if not isinstance(scenario, dict):
        return {"status": "fail", "issues": ["scenario must be an object"]}
    missing = [field for field in FIELDS
               if not isinstance(scenario.get(field), str)
               or not scenario[field].strip()]
    if missing:
        return {"status": "fail",
                "issues": ["missing or invalid: " + field for field in missing]}
    expected_control = PAIRS.get(scenario["threat"])
    if expected_control is None or scenario["control"] != expected_control:
        return {"status": "review", "issues": ["unlisted threat/control pair"]}
    return {"status": "pass", "issues": []}


def fixture(case="complete"):
    """Return fresh local scenarios, optionally with one deliberate defect."""
    scenarios = deepcopy(SCENARIOS)
    if case == "missing-asset":
        del scenarios[0]["asset"]
    elif case == "unrelated-control":
        scenarios[0]["control"] = "encrypt_storage"
    elif case != "complete":
        raise ValueError("unknown fixture case")
    return scenarios


def main():
    """Run local JSON inputs; exit 0/pass, 1/fail, 3/review or 2/CLI error."""
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--case", default="complete",
                        choices=("complete", "missing-asset", "unrelated-control"))
    inputs.add_argument("--scenario", help="one JSON object instead of the fixture")
    args = parser.parse_args()
    try:
        scenarios = ([json.loads(args.scenario)] if args.scenario is not None
                     else fixture(args.case))
    except ValueError as error:
        parser.error(str(error))
    results = [check_scenario(scenario) for scenario in scenarios]
    print(json.dumps({"results": results}))
    if any(result["status"] == "fail" for result in results):
        return 1
    if any(result["status"] == "review" for result in results):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
