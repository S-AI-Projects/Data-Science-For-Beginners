"""Check fictional lifecycle scenarios and compare small input sizes."""

import argparse
from copy import deepcopy
import json


FIELDS = ("asset", "threat", "control", "residual_risk")
PAIRS = {
    "unclear_data_origin": "record_source_and_provenance",
    "malformed_records": "validate_input_schema",
    "unauthorized_edits": "restrict_data_writers",
}
SCENARIOS = [
    {
        "id": "capturing-survey",
        "section": "Capturing",
        "asset": "Fictional community survey records",
        "threat": "unclear_data_origin",
        "control": "record_source_and_provenance",
        "residual_risk": "Recorded provenance may still be incomplete or incorrect.",
    },
    {
        "id": "processing-import",
        "section": "Processing",
        "asset": "Fictional CSV used to prepare a monthly summary",
        "threat": "malformed_records",
        "control": "validate_input_schema",
        "residual_risk": "Well-formed rows may still contain inaccurate values.",
    },
    {
        "id": "maintenance-table",
        "section": "Maintaining / Managing Data",
        "asset": "Fictional shared project table",
        "threat": "unauthorized_edits",
        "control": "restrict_data_writers",
        "residual_risk": "An authorized writer could still make an erroneous change.",
    },
]


def check_scenario(scenario):
    """Check four nonblank fields and the fixture's exact threat/control pair."""
    if not isinstance(scenario, dict):
        return {"status": "fail", "issues": ["scenario must be an object"],
                "field_checks": 0}
    missing = [field for field in FIELDS
               if not isinstance(scenario.get(field), str)
               or not scenario[field].strip()]
    if missing:
        return {"status": "fail",
                "issues": ["missing or invalid: " + field for field in missing],
                "field_checks": len(FIELDS)}
    if PAIRS.get(scenario["threat"]) != scenario["control"]:
        return {"status": "review", "issues": ["unlisted threat/control pair"],
                "field_checks": len(FIELDS)}
    return {"status": "pass", "issues": [], "field_checks": len(FIELDS)}


def fixture(case="complete"):
    """Return a fresh three-scenario fixture with optional first-record defect."""
    scenarios = deepcopy(SCENARIOS)
    if case == "missing-asset":
        del scenarios[0]["asset"]
    elif case == "unrelated-control":
        scenarios[0]["control"] = "restrict_data_writers"
    elif case != "complete":
        raise ValueError("unknown fixture case")
    return scenarios


def compare_sizes(scenarios):
    """Compare prefixes of sizes 1, 2 and 3 using field checks as work proxy."""
    comparison = []
    for size in range(1, min(3, len(scenarios)) + 1):
        actual = [check_scenario(scenario) for scenario in scenarios[:size]]
        expected = ["pass"] * size
        actual_statuses = [result["status"] for result in actual]
        comparison.append({
            "scenarios": size,
            "expected_statuses": expected,
            "actual_statuses": actual_statuses,
            "required_field_checks": sum(item["field_checks"] for item in actual),
            "correct": actual_statuses == expected,
        })
    return comparison


def main():
    """Print rubric results and a deterministic input-size comparison."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="complete",
                        choices=("complete", "missing-asset", "unrelated-control"))
    args = parser.parse_args()
    scenarios = fixture(args.case)
    results = [check_scenario(scenario) for scenario in scenarios]
    comparison = compare_sizes(fixture())
    print(json.dumps({"results": results, "size_comparison": comparison}))
    if any(result["status"] == "fail" for result in results):
        return 1
    if any(result["status"] == "review" for result in results):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
