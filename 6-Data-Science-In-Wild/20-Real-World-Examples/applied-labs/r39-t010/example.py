"""Real-World Security-Scenario Rubric & Three Applied Assessment Questions.

Lab Module: R39-T010 (Lesson 20: 6-Data-Science-In-Wild/20-Real-World-Examples)
Scope: [SIMULATION/MOCK] Local educational demonstration using Python 3 standard library only.
No external network calls, paid APIs, GPUs, or actual cloud deployments are performed.

Notice on Grading Boundaries:
Automated grading evaluates structural completeness (asset, threat, control, residual risk)
and known threat-control alignment. Subjective quality, risk tolerance, and free-text
justifications in the 'explanation' field require human review and cannot be certified
purely by automated code checks.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
import sys


# Known threat domains and valid mitigation keywords for automated consistency checking
THREAT_CONTROL_CATALOG: Dict[str, List[str]] = {
    "exfiltration": ["differential privacy", "rbac", "masking", "encryption", "tokenization"],
    "adversarial_evasion": ["smoothing", "adversarial robustness", "input validation", "defensive distillation"],
    "sensor_spoofing": ["cryptographic attestation", "mutual tls", "digital signature", "hmac", "pki"],
}


@dataclass
class SecurityScenario:
    """Represents a data science security scenario under evaluation."""
    scenario_id: str
    name: str
    asset: str
    threat: str
    control: str
    residual_risk: str
    explanation: str


def classify_threat_category(threat_text: str) -> Optional[str]:
    """Classifies a threat into a known category based on key phrases."""
    threat_lower = threat_text.lower()
    if "exfiltration" in threat_lower or "leak" in threat_lower or "breach" in threat_lower:
        return "exfiltration"
    if "evasion" in threat_lower or "adversarial" in threat_lower or "perturbation" in threat_lower:
        return "adversarial_evasion"
    if "spoofing" in threat_lower or "replay" in threat_lower or "rogue" in threat_lower:
        return "sensor_spoofing"
    return None


def evaluate_scenario(scenario: SecurityScenario) -> Dict[str, Any]:
    """Evaluates a SecurityScenario against structural completeness and control relevance.
    
    Rubric Rules:
    1. Structural Completeness: All fields (asset, threat, control, residual_risk) must be
       non-empty after stripping whitespace. If any field is missing, returns status 'FAIL'.
    2. Threat-Control Relevance:
       - If the threat matches a recognized category and the control contains an approved
         mitigation keyword, returns status 'PASS'.
       - If the control belongs to an unrelated category or is unverified/novel, returns
         status 'FLAGGED_FOR_REVIEW'.
    3. Explanation Review: The explanation field is recorded for human auditor review but
       is not certified automatically.
    """
    asset_clean = scenario.asset.strip() if scenario.asset else ""
    threat_clean = scenario.threat.strip() if scenario.threat else ""
    control_clean = scenario.control.strip() if scenario.control else ""
    risk_clean = scenario.residual_risk.strip() if scenario.residual_risk else ""

    missing_fields: List[str] = []
    if not asset_clean:
        missing_fields.append("asset")
    if not threat_clean:
        missing_fields.append("threat")
    if not control_clean:
        missing_fields.append("control")
    if not risk_clean:
        missing_fields.append("residual_risk")

    if missing_fields:
        return {
            "scenario_id": scenario.scenario_id,
            "status": "FAIL",
            "reason": f"missing_{missing_fields[0]}",
            "diagnostics": {
                "missing_fields": missing_fields,
                "message": f"Scenario lacks required structural field(s): {', '.join(missing_fields)}"
            },
            "requires_human_review": False
        }

    threat_cat = classify_threat_category(threat_clean)
    control_lower = control_clean.lower()

    if threat_cat and threat_cat in THREAT_CONTROL_CATALOG:
        valid_keywords = THREAT_CONTROL_CATALOG[threat_cat]
        matches_threat = any(kw in control_lower for kw in valid_keywords)
        if matches_threat:
            return {
                "scenario_id": scenario.scenario_id,
                "status": "PASS",
                "reason": "complete_and_consistent",
                "diagnostics": {
                    "threat_category": threat_cat,
                    "matched_control": True,
                    "message": "All required fields are populated and control matches named threat category."
                },
                "requires_human_review": False
            }
        else:
            return {
                "scenario_id": scenario.scenario_id,
                "status": "FLAGGED_FOR_REVIEW",
                "reason": "unrelated_control_threat_mismatch",
                "diagnostics": {
                    "threat_category": threat_cat,
                    "matched_control": False,
                    "message": "Control does not match recognized mitigation patterns for the threat; human auditor review required."
                },
                "requires_human_review": True
            }

    # Unknown or novel threat category: fail-safe policy routes to human review
    return {
        "scenario_id": scenario.scenario_id,
        "status": "FLAGGED_FOR_REVIEW",
        "reason": "unmapped_threat_category",
        "diagnostics": {
            "threat_category": "unmapped",
            "matched_control": False,
            "message": "Unmapped threat category cannot be validated by automated rubric; requires human review."
        },
        "requires_human_review": True
    }


# Standard Fictional Real-World Scenarios tied to Lesson 20 themes
FIXTURE_SCENARIO_1_PASS = SecurityScenario(
    scenario_id="RW-01",
    name="Clinical Healthcare Telemetry Export (Consistent Protection)",
    asset="Clinical Patient Health Record Telemetry (EHR, vitals, lab panels)",
    threat="Unauthorized Exfiltration of De-identified Patient Health Records",
    control="Enforce Differential Privacy Perturbation and Strict Role-Based Column Masking (RBAC)",
    residual_risk="Low: Mathematical re-identification risk bounded by privacy budget epsilon; audit logs inspected monthly.",
    explanation="Differential privacy and RBAC prevent linkage re-identification attacks when sharing clinical research data."
)

FIXTURE_SCENARIO_2_FAIL = SecurityScenario(
    scenario_id="RW-02",
    name="Planetary Earth Observation Yield Pipeline (Missing Asset)",
    asset="",  # Empty/missing asset triggers FAIL
    threat="Adversarial Model Evasion via Perturbed Satellite Imagery in Crop Health Analysis",
    control="Implement Input Smoothing and Certified Adversarial Robustness Filtering",
    residual_risk="Medium: Smoothing mitigates pixel-level noise, but structural feature poisoning requires continuous retraining.",
    explanation="Adversarial perturbations on agricultural satellite bands can deceive yield estimators; defenses must identify target assets."
)

FIXTURE_SCENARIO_3_REVIEW = SecurityScenario(
    scenario_id="RW-03",
    name="Smart Agriculture LoRaWAN Sensor Pipeline (Control Mismatch)",
    asset="Soil Moisture and Weather Telemetry Sensor Stream",
    threat="Sensor Data Spoofing and Replay Attack by Rogue LoRaWAN Gateway",
    control="Enforce Static HTML Output Encoding and Content-Security-Policy Headers",  # Unrelated web XSS control!
    residual_risk="High: Web sanitization does not protect against physical or wireless sensor replay attacks.",
    explanation="Ingestion pipeline accepts spoofed telemetry; applying web frontend headers does not remediate gateway impersonation."
)

FIXTURE_SCENARIOS: List[SecurityScenario] = [
    FIXTURE_SCENARIO_1_PASS,
    FIXTURE_SCENARIO_2_FAIL,
    FIXTURE_SCENARIO_3_REVIEW,
]


@dataclass
class AssessmentQuestion:
    """Represents an applied scenario assessment question with an executable verification check."""
    question_id: str
    question_type: str  # predict_output, diagnose_failure, choose_boundary_policy
    prompt: str
    expected_factual_answer: str
    rationale: str
    check_fn: Callable[[Callable[[SecurityScenario], Dict[str, Any]], str], bool] = field(repr=False)


def _check_predict_output(eval_fn: Callable[[SecurityScenario], Dict[str, Any]], answer: str) -> bool:
    """Executes live evaluation on a scenario with mismatching threat & control to verify expected status."""
    mismatch_scenario = SecurityScenario(
        scenario_id="TEST-PREDICT",
        name="Telemetry Pipeline with Web Injection Mitigation",
        asset="Epidemiological Sensor Stream",
        threat="Sensor Data Spoofing and Replay Attack by Rogue Ingestion Gateway",
        control="Configure Web Application Firewall HTML Entity Sanitization",
        residual_risk="High: Ineffective against wireless frame injection.",
        explanation="Testing category mismatch between sensor spoofing and web XSS."
    )
    res = eval_fn(mismatch_scenario)
    return res["status"] == answer and answer == "FLAGGED_FOR_REVIEW"


def _check_diagnose_failure(eval_fn: Callable[[SecurityScenario], Dict[str, Any]], answer: str) -> bool:
    """Diagnoses failure on Scenario 2 and verifies populating the identified field yields PASS."""
    res_before = eval_fn(FIXTURE_SCENARIO_2_FAIL)
    if res_before["status"] != "FAIL":
        return False
    if res_before.get("diagnostics", {}).get("missing_fields") != [answer]:
        return False

    # Repair scenario by populating the identified missing field
    repaired_scenario = SecurityScenario(
        scenario_id=FIXTURE_SCENARIO_2_FAIL.scenario_id,
        name=FIXTURE_SCENARIO_2_FAIL.name,
        asset="Planetary Computer Satellite Multispectral Imagery Archive",  # Repaired!
        threat=FIXTURE_SCENARIO_2_FAIL.threat,
        control=FIXTURE_SCENARIO_2_FAIL.control,
        residual_risk=FIXTURE_SCENARIO_2_FAIL.residual_risk,
        explanation=FIXTURE_SCENARIO_2_FAIL.explanation,
    )
    res_after = eval_fn(repaired_scenario)
    return res_after["status"] == "PASS"


def _check_choose_boundary_policy(eval_fn: Callable[[SecurityScenario], Dict[str, Any]], answer: str) -> bool:
    """Verifies the fail-safe boundary policies for blank strings and unmapped threat categories."""
    if answer != "strip_whitespace_reject_and_flag_unmapped_for_review":
        return False

    # Policy 1: Whitespace-only asset must be stripped and rejected as FAIL
    whitespace_scenario = SecurityScenario(
        scenario_id="TEST-WHITESPACE",
        name="Whitespace Blank Asset Test",
        asset="   \t\n   ",
        threat="Unauthorized Exfiltration of Patient Health Records",
        control="Enforce Differential Privacy Perturbation and Strict Role-Based Column Masking (RBAC)",
        residual_risk="Low",
        explanation="Testing whitespace stripping boundary condition."
    )
    res_ws = eval_fn(whitespace_scenario)
    if res_ws["status"] != "FAIL" or "asset" not in res_ws.get("diagnostics", {}).get("missing_fields", []):
        return False

    # Policy 2: Unmapped/novel threat category must be flagged for review rather than blindly passing
    novel_threat_scenario = SecurityScenario(
        scenario_id="TEST-NOVEL",
        name="Emerging Quantum Decryption Threat",
        asset="Long-term Archived Genomics Database",
        threat="Harvest-Now-Decrypt-Later Quantum Cryptanalysis",
        control="Apply Post-Quantum Lattice Cryptography",
        residual_risk="Medium: Emerging NIST standards in transition.",
        explanation="Novel threat pattern not yet encoded in standard regex catalog."
    )
    res_novel = eval_fn(novel_threat_scenario)
    if res_novel["status"] != "FLAGGED_FOR_REVIEW":
        return False

    return True


ASSESSMENT_QUESTIONS: List[AssessmentQuestion] = [
    AssessmentQuestion(
        question_id="Q1",
        question_type="predict_output",
        prompt=(
            "Predict the rubric checker status when all four required fields (asset, threat, control, residual_risk) "
            "are non-empty, but the control belongs to an unrelated threat category than the specified threat."
        ),
        expected_factual_answer="FLAGGED_FOR_REVIEW",
        rationale=(
            "When syntactic completeness is satisfied but the semantic threat-control mapping reveals a domain mismatch "
            "(e.g., applying web HTML entity sanitization against IoT sensor replay), the automated rubric cannot certify "
            "security soundness. Rather than falsely passing or completely rejecting syntactically complete inputs, "
            "the system deterministically routes the scenario to human auditor review with status 'FLAGGED_FOR_REVIEW'."
        ),
        check_fn=_check_predict_output
    ),
    AssessmentQuestion(
        question_id="Q2",
        question_type="diagnose_failure",
        prompt=(
            "Diagnose which required field causes the structural evaluation of Scenario 2 to return 'FAIL', "
            "and verify the outcome when that field is supplied."
        ),
        expected_factual_answer="asset",
        rationale=(
            "Security threat modeling requires an identified target asset. Scenario 2 omitted the 'asset' field (empty string). "
            "The automated structural validator flags this missing mandatory attribute with status 'FAIL'. "
            "When a valid asset ('Planetary Computer Satellite Multispectral Imagery Archive') is provided alongside "
            "its matching adversarial smoothing control, the scenario successfully transitions to 'PASS'."
        ),
        check_fn=_check_diagnose_failure
    ),
    AssessmentQuestion(
        question_id="Q3",
        question_type="choose_boundary_policy",
        prompt=(
            "Choose the deterministic boundary policy for handling whitespace-only inputs and unmapped/novel threat categories."
        ),
        expected_factual_answer="strip_whitespace_reject_and_flag_unmapped_for_review",
        rationale=(
            "A robust security rubric adheres to fail-safe defaults: (1) strings composed solely of whitespace ('   ') "
            "must be stripped and treated as missing, triggering an explicit 'FAIL' to prevent bypassing completeness checks; "
            "and (2) novel or unrecognized threat categories must be flagged for human review ('FLAGGED_FOR_REVIEW') "
            "rather than silently assumed safe or falsely passed."
        ),
        check_fn=_check_choose_boundary_policy
    ),
]


def verify_assessment_answers(
    eval_fn: Callable[[SecurityScenario], Dict[str, Any]] = evaluate_scenario,
    submitted_answers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Verifies assessment answers against rationales and executable checks.
    
    Each question requires:
    1. A submitted answer matching expected_factual_answer.
    2. A non-empty analytical rationale.
    3. An executable check function that passes when invoked against eval_fn.
    """
    answers = submitted_answers or {q.question_id: q.expected_factual_answer for q in ASSESSMENT_QUESTIONS}
    details = []
    passed_count = 0

    for q in ASSESSMENT_QUESTIONS:
        submitted_val = answers.get(q.question_id, "")
        matches_expected = (submitted_val == q.expected_factual_answer)
        has_rationale = bool(q.rationale and q.rationale.strip())

        try:
            check_passed = q.check_fn(eval_fn, submitted_val)
        except Exception:
            check_passed = False

        is_correct = matches_expected and has_rationale and check_passed
        if is_correct:
            passed_count += 1

        details.append({
            "question_id": q.question_id,
            "question_type": q.question_type,
            "submitted_answer": submitted_val,
            "expected_answer": q.expected_factual_answer,
            "has_rationale": has_rationale,
            "check_passed": check_passed,
            "is_correct": is_correct
        })

    return {
        "passed": passed_count,
        "total": len(ASSESSMENT_QUESTIONS),
        "all_passed": (passed_count == len(ASSESSMENT_QUESTIONS)),
        "details": details
    }


def run_report() -> Dict[str, Any]:
    """Runs evaluations on fixture scenarios and executes all scenario assessment checks."""
    print("=" * 80)
    print("APPLIED LAB R39-T010: SECURITY-SCENARIO RUBRIC & SCENARIO ASSESSMENT")
    print("Lesson Reference: 6-Data-Science-In-Wild/20-Real-World-Examples")
    print("Environment Scope: [SIMULATION/MOCK] Pure Python standard library demonstration")
    print("=" * 80)
    print("\n[GRADING BOUNDARY NOTICE]")
    print("Automated checks verify structural completeness and cataloged threat-control pairings.")
    print("Free-text justifications and residual risk appetite require human expert review.\n")

    print("-" * 80)
    print("PART 1: REAL-WORLD SECURITY SCENARIO EVALUATIONS")
    print("-" * 80)
    scenario_results = []
    for sc in FIXTURE_SCENARIOS:
        res = evaluate_scenario(sc)
        scenario_results.append(res)
        print(f"\nScenario ID   : {sc.scenario_id}")
        print(f"Name          : {sc.name}")
        print(f"Asset         : {sc.asset or '<MISSING>'}")
        print(f"Threat        : {sc.threat}")
        print(f"Control       : {sc.control}")
        print(f"Status        : {res['status']} ({res['reason']})")
        print(f"Human Review  : {'Required' if res['requires_human_review'] else 'Not Required'}")
        print(f"Diagnostics   : {res['diagnostics']['message']}")

    print("\n" + "-" * 80)
    print("PART 2: APPLIED SCENARIO ASSESSMENT (3 QUESTIONS)")
    print("-" * 80)
    assessment_res = verify_assessment_answers()
    for q_detail, q_obj in zip(assessment_res["details"], ASSESSMENT_QUESTIONS):
        print(f"\n[{q_detail['question_id']}] Type: {q_detail['question_type']}")
        print(f"Prompt   : {q_obj.prompt}")
        print(f"Answer   : {q_detail['submitted_answer']}")
        print(f"Rationale: {q_obj.rationale}")
        print(f"Check    : {'PASSED' if q_detail['check_passed'] else 'FAILED'}")

    print("\n" + "=" * 80)
    print(f"ASSESSMENT_CHECKS_PASSED: {assessment_res['passed']}/{assessment_res['total']}")
    print("=" * 80)

    return {
        "scenario_results": scenario_results,
        "assessment_results": assessment_res
    }


if __name__ == "__main__":
    report = run_report()
    if not report["assessment_results"]["all_passed"]:
        sys.exit(1)
    sys.exit(0)
