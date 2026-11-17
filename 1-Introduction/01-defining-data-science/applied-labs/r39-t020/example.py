"""Check fictional data science scenarios and three applied questions."""

import argparse
from copy import deepcopy
import json


FIELDS = ("asset", "threat", "control", "residual_risk")
PAIRS = {
    "unclear_survey_provenance": "record_source_and_consent",
    "malformed_web_logs": "validate_log_fields",
    "unauthorized_sensor_data_access": "limit_data_access",
}
SCENARIOS = [
    {
        "id": "course-survey",
        "section": "Digitalization and Digital Transformation",
        "asset": "Fictional course feedback survey responses",
        "threat": "unclear_survey_provenance",
        "control": "record_source_and_consent",
        "residual_risk": "A respondent may still misunderstand how answers are used.",
    },
    {
        "id": "site-logs",
        "section": "What you can do with Data / Data Processing",
        "asset": "Fictional web server logs used for a page-usage summary",
        "threat": "malformed_web_logs",
        "control": "validate_log_fields",
        "residual_risk": "Well-formed logs may still record incorrect events.",
    },
    {
        "id": "room-sensors",
        "section": "Where to get Data / Internet of Things",
        "asset": "Fictional room temperature readings from sensors",
        "threat": "unauthorized_sensor_data_access",
        "control": "limit_data_access",
        "residual_risk": "An authorized user could still share an export.",
    },
]

QUESTIONS = {
    "predict": {
        "question": "What result does a complete course-survey scenario receive?",
        "scenario": SCENARIOS[0],
        "rationale": "All four fields are nonblank and the threat/control labels form a listed pair.",
    },
    "diagnose": {
        "question": "What fails when the course-survey scenario omits its asset?",
        "scenario": {key: value for key, value in SCENARIOS[0].items()
                      if key != "asset"},
        "rationale": "An asset names what is at risk; the checker reports the missing required field.",
    },
    "boundary": {
        "question": "How should a complete scenario with an unlisted threat/control pair be handled?",
        "scenario": {**SCENARIOS[0], "control": "encrypt_archive"},
        "rationale": "An unlisted pair needs human review; the structural checker should not guess whether it is appropriate.",
    },
}


def check_scenario(scenario):
    """Check required field structure and exact pair consistency only."""
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
    """Return fresh scenario fixtures for normal, missing and review cases."""
    scenarios = deepcopy(SCENARIOS)
    if case == "missing-asset":
        del scenarios[0]["asset"]
    elif case == "unrelated-control":
        scenarios[0]["control"] = "encrypt_archive"
    elif case != "complete":
        raise ValueError("unknown fixture case")
    return scenarios


def answer_question(question_id):
    """Evaluate one applied question from its fixture and return its rationale."""
    if question_id not in QUESTIONS:
        raise ValueError("unknown question")
    prompt = QUESTIONS[question_id]
    return {"id": question_id, "question": prompt["question"],
            "answer": check_scenario(prompt["scenario"]),
            "rationale": prompt["rationale"]}


def main():
    """Print fixture or question results; fail/review use distinct exit codes."""
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--case", default="complete",
                        choices=("complete", "missing-asset", "unrelated-control"))
    choice.add_argument("--question", choices=tuple(QUESTIONS))
    args = parser.parse_args()
    if args.question:
        results = [answer_question(args.question)["answer"]]
    else:
        results = [check_scenario(scenario) for scenario in fixture(args.case)]
    print(json.dumps({"results": results}))
    if any(result["status"] == "fail" for result in results):
        return 1
    if any(result["status"] == "review" for result in results):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
