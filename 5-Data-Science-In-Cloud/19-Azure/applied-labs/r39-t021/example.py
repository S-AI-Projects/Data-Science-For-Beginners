"""
Rubric Checker for Azure Cloud Security Scenarios (R39-T021)
Evaluates whether a fictional cloud security threat-model scenario is structurally sound.

Contract:
- asset: identifies the asset being protected.
- threat: describes the named threat.
- control: specified mitigation mechanism.
- residual_risk: assessment of risk remaining after control is applied.

Outcomes:
- PASS: Complete and control relates to named threat.
- FAIL: Missing required field (e.g., missing asset).
- FLAGGED_FOR_REVIEW: Control is unrelated to the named threat.
"""

def evaluate_security_scenario(scenario: dict) -> dict:
    """
    Evaluates a single security scenario against the structural rubric.
    Required keys: asset, threat, control, residual_risk.
    """
    asset = scenario.get("asset")
    threat = scenario.get("threat")
    control = scenario.get("control")
    residual_risk = scenario.get("residual_risk")

    # 1. Structural completeness checks
    if not asset or not str(asset).strip():
        return {"status": "FAIL", "reason": "Missing asset: An asset must be identified"}
    if not threat or not str(threat).strip():
        return {"status": "FAIL", "reason": "Missing threat: A specific threat must be identified"}
    if not control or not str(control).strip():
        return {"status": "FAIL", "reason": "Missing control: A security control must be specified"}
    if not residual_risk or not str(residual_risk).strip():
        return {"status": "FAIL", "reason": "Missing residual_risk: Residual risk must be evaluated"}

    # 2. Semantic alignment check: Does the control address the threat?
    threat_lower = str(threat).lower()
    control_lower = str(control).lower()

    threat_words = set(threat_lower.replace("-", " ").split())
    control_words = set(control_lower.replace("-", " ").split())

    # Filter out common English stopwords from keyword overlap check
    stopwords = {"and", "or", "the", "a", "an", "in", "on", "at", "for", "of", "to", "with", "by", "from", "is", "it"}
    meaningful_threat_words = {w for w in threat_words if w not in stopwords and len(w) > 2}
    meaningful_control_words = {w for w in control_words if w not in stopwords and len(w) > 2}

    has_keyword_overlap = bool(meaningful_threat_words & meaningful_control_words)
    is_cloud_leak_control = ("leak" in threat_lower or "exfiltration" in threat_lower) and \
                            ("encrypt" in control_lower or "firewall" in control_lower or "tls" in control_lower)
    is_access_control = ("unauthorized" in threat_lower or "breach" in threat_lower or "access" in threat_lower) and \
                        ("rbac" in control_lower or "iam" in control_lower or "mfa" in control_lower or "token" in control_lower or "auth" in control_lower)
    is_tampering_control = ("tamper" in threat_lower or "poison" in threat_lower) and \
                           ("signature" in control_lower or "hash" in control_lower or "digest" in control_lower)

    if not (has_keyword_overlap or is_cloud_leak_control or is_access_control or is_tampering_control):
        return {"status": "FLAGGED_FOR_REVIEW", "reason": "Control unrelated to named threat: Manual review required"}

    return {"status": "PASS", "reason": "Scenario complete and structurally consistent"}


# The 3 canonical fixture scenarios requested by the task
CANONICAL_SCENARIOS = {
    "complete_pass": {
        "asset": "Azure Blob Training Dataset (PII)",
        "threat": "Data leakage during cloud upload",
        "control": "TLS 1.3 in transit and Customer-Managed Keys (CMK) encryption at rest",
        "residual_risk": "Low (insider threat with administrative key access remains)"
    },
    "missing_asset_fail": {
        "asset": "",  # Deliberately empty asset
        "threat": "Unauthorized API model inference access",
        "control": "Azure Active Directory OAuth2 bearer token authentication",
        "residual_risk": "Low"
    },
    "unrelated_control_review": {
        "asset": "Trained ResNet-50 Model Artifact",
        "threat": "Unauthorized access and theft of proprietary weights",
        "control": "Weekly unit test for inference latency and throughput",  # Unrelated!
        "residual_risk": "High"
    }
}
