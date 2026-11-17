"""Check fictional data-description scenarios with a small local rubric."""

import argparse
from copy import deepcopy
import json


FIELDS = ("asset", "threat", "control", "residual_risk")
PAIRS = {
    "unauthorized_database_read": "limit_database_access",
    "malformed_structured_rows": "validate_required_columns",
    "misread_email_metadata": "preserve_header_fields",
}
SCENARIOS = [
    {
        "id": "customer-table",
        "section": "Structured Data",
        "asset": "Fictional customer table with named columns",
        "threat": "unauthorized_database_read",
        "control": "limit_database_access",
        "residual_risk": "An authorized reader could still share an export.",
    },
    {
        "id": "sensor-csv",
        "section": "Structured Data",
        "asset": "Fictional CSV of hourly sensor readings",
        "threat": "malformed_structured_rows",
        "control": "validate_required_columns",
        "residual_risk": "Validly shaped rows may still contain inaccurate readings.",
    },
    {
        "id": "email-source",
        "section": "Sources of Data",
        "asset": "Fictional email messages used as a data source",
        "threat": "misread_email_metadata",
        "control": "preserve_header_fields",
        "residual_risk": "Correctly preserved headers do not prove the body is trustworthy.",
    },
]


def check_scenario(scenario):
    """Return pass, fail or review for the stated structural requirements."""
    if not isinstance(scenario, dict):
        return {"status": "fail", "issues": ["scenario must be an object"]}
    missing = [field for field in FIELDS
               if not isinstance(scenario.get(field), str)
               or not scenario[field].strip()]
    if missing:
        return {"status": "fail",
                "issues": ["missing or invalid: " + field for field in missing]}
    if PAIRS.get(scenario["threat"]) != scenario["control"]:
        return {"status": "review", "issues": ["unlisted threat/control pair"]}
    return {"status": "pass", "issues": []}


def fixture(case="complete"):
    """Return independent fixtures for the three documented CLI cases."""
    scenarios = deepcopy(SCENARIOS)
    if case == "missing-asset":
        del scenarios[0]["asset"]
    elif case == "unrelated-control":
        scenarios[0]["control"] = "preserve_header_fields"
    elif case != "complete":
        raise ValueError("unknown fixture case")
    return scenarios


def evaluate_sequence(scenarios):
    """Check each input independently, preserving later results after an error."""
    if not isinstance(scenarios, list):
        raise ValueError("sequence must be a JSON list")
    return [check_scenario(scenario) for scenario in scenarios]


def main():
    """Print results for a fixture, one scenario or an ordered input sequence."""
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--case", default="complete",
                        choices=("complete", "missing-asset", "unrelated-control"))
    inputs.add_argument("--scenario", help="one JSON scenario object")
    inputs.add_argument("--sequence", help="JSON list of scenarios, checked in order")
    args = parser.parse_args()
    try:
        if args.sequence is not None:
            results = evaluate_sequence(json.loads(args.sequence))
        elif args.scenario is not None:
            results = [check_scenario(json.loads(args.scenario))]
        else:
            results = evaluate_sequence(fixture(args.case))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps({"results": results}))
    if any(result["status"] == "fail" for result in results):
        return 1
    if any(result["status"] == "review" for result in results):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
