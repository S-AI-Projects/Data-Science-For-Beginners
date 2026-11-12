"""R39-T011: structural rubric checker for fictional data-science scenarios.

SIMULATION: every scenario below is fictional. Nothing here touches real
students, real logs, real hardware, a cloud service or a trained model.

Lesson link: "Defining Data Science" (1-Introduction/01-defining-data-science).
Each scenario is anchored to a named section of that lesson and is written as
four fields: asset, threat, control, residual_risk.

What the checker verifies (structure only):
  1. asset, threat, control and residual_risk are all present and non-blank.
  2. lesson_section names a real section of the lesson.
  3. residual_risk does not claim the risk is "none" (a control never
     removes risk completely).
  4. threat_type and control_type are known tags.
  5. the control_type is one that addresses the threat_type; if not, the
     scenario is flagged REVIEW for a human instead of being failed.

What it does NOT do: judge whether the explanation is good, true or
well argued. A human reviewer does that.

Run:  python3 example.py
"""
from collections import namedtuple

Result = namedtuple("Result", ["status", "reasons"])

PASS, FAIL, REVIEW = "PASS", "FAIL", "REVIEW"

# Section headings taken from the lesson README.
LESSON_SECTIONS = frozenset({
    "What is Data?",
    "What is Data Science?",
    "Other Related Fields",
    "Types of Data",
    "Where to get Data",
    "What you can do with Data",
    "Digitalization and Digital Transformation",
})

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

# Residual risk wording that claims nothing is left over.
NO_RISK_WORDS = frozenset({"none", "n/a", "na", "nil", "zero", "no risk",
                           "no residual risk"})

# Hand-made simplification: which control types address which threat types.
CONTROLS_FOR_THREAT = {
    "reidentification": frozenset({"aggregation", "anonymisation"}),
    "pii_exposure": frozenset({"anonymisation", "access_control"}),
    "data_corruption": frozenset({"validation"}),
}
KNOWN_CONTROL_TYPES = frozenset().union(*CONTROLS_FOR_THREAT.values())


def _blank(value):
    return not isinstance(value, str) or not value.strip()


def check_scenario(scenario):
    """Return Result(status, reasons) for one scenario dict.

    FAIL   -> a structural rule is broken (missing field, bad tag, ...).
    REVIEW -> structure is fine but the control looks unrelated to the threat;
              a human must decide.
    PASS   -> structure is complete and consistent (says nothing about quality).
    """
    if not isinstance(scenario, dict):
        return Result(FAIL, ["not_a_scenario"])

    fails = []
    for field in REQUIRED_FIELDS:
        if _blank(scenario.get(field)):
            fails.append("missing:" + field)

    if scenario.get("lesson_section") not in LESSON_SECTIONS:
        fails.append("unknown_lesson_section")

    residual = scenario.get("residual_risk")
    if not _blank(residual) and residual.strip().lower() in NO_RISK_WORDS:
        fails.append("residual_risk_claims_none")

    threat_type = scenario.get("threat_type")
    control_type = scenario.get("control_type")
    if _blank(threat_type):
        fails.append("missing:threat_type")
    elif threat_type not in CONTROLS_FOR_THREAT:
        fails.append("unknown_threat_type")
    if _blank(control_type):
        fails.append("missing:control_type")
    elif control_type not in KNOWN_CONTROL_TYPES:
        fails.append("unknown_control_type")

    if fails:
        return Result(FAIL, fails)

    if control_type not in CONTROLS_FOR_THREAT[threat_type]:
        return Result(REVIEW, ["control_unrelated_to_threat"])
    return Result(PASS, [])


# ---------------------------------------------------------------- fixtures
# Three fictional scenarios, each tied to a section of the lesson.
SCENARIOS = [
    {
        "id": "S1-course-timings",
        "lesson_section": "Digitalization and Digital Transformation",
        "asset": "Per-student module completion times and age categories "
                 "from a fictional online data science course",
        "threat": "A small age group lets a reader pick out one student "
                  "(re-identification)",
        "threat_type": "reidentification",
        "control": "Publish only averages for groups of at least 5 students",
        "control_type": "aggregation",
        "residual_risk": "A single extreme outlier can still reveal one "
                         "student's behaviour inside a group of 5",
    },
    {
        "id": "S2-web-logs",
        "lesson_section": "Where to get Data",
        "asset": "Web server logs of the fictional course website",
        "threat": "Logs contain IP addresses that identify visitors",
        "threat_type": "pii_exposure",
        "control": "Replace IP addresses with salted hashes before analysis",
        "control_type": "anonymisation",
        "residual_risk": "Hashed IDs can still be linked to other datasets "
                         "that share the same visitor",
    },
    {
        "id": "S3-quiz-table",
        "lesson_section": "What you can do with Data",
        "asset": "Quiz results table for the fictional course",
        "threat": "Badly formatted scores silently corrupt module averages",
        "threat_type": "data_corruption",
        "control": "Reject rows that break the score schema when loading data",
        "control_type": "validation",
        "residual_risk": "A well-formed but wrong score still passes "
                         "validation",
    },
]

# Negative fixtures: derived from S1 by changing exactly one thing.
NO_ASSET = dict(SCENARIOS[0], id="N1-no-asset", asset="")
UNRELATED_CONTROL = dict(
    SCENARIOS[0],
    id="N2-unrelated-control",
    control="Reject rows that break the score schema when loading data",
    control_type="validation",
)
ALL_FIXTURES = SCENARIOS + [NO_ASSET, UNRELATED_CONTROL]


def run(fixtures=ALL_FIXTURES):
    """Print one line per fixture: id, status, reasons."""
    for scenario in fixtures:
        result = check_scenario(scenario)
        reasons = ",".join(result.reasons) if result.reasons else "-"
        print("{:<22} {:<7} {}".format(scenario["id"], result.status, reasons))


if __name__ == "__main__":
    run()