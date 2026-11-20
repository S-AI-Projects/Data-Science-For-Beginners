"""Security-scenario rubric evaluation experiment (R39-T049).

Extends the Defining Data Science lesson. Implements a structural rubric checker
evaluating three fictional scenarios (PASS, FAIL on missing asset, REVIEW on
unrelated control) and benchmarks three controlled batch configurations without
claiming real-world model accuracy.
"""

from __future__ import annotations
from dataclasses import dataclass
import json
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class SecurityScenario:
    scenario_id: str
    asset: Optional[str]
    threat: str
    control: str
    residual_risk: str


KEYWORD_MAPPING: Dict[str, Tuple[str, ...]] = {
    "privacy_leak": ("anonymization", "masking", "differential privacy", "k-anonymity", "rbac"),
    "data_tampering": ("checksum", "hash", "signature", "immutable", "validation"),
    "model_drift": ("monitoring", "retraining", "alerting", "distribution test", "eval"),
}


def _classify_threat(threat_text: str) -> str:
    low = threat_text.lower()
    if "leak" in low or "re-identification" in low or "privacy" in low or "unmasked" in low:
        return "privacy_leak"
    if "tamper" in low or "poison" in low or "integrity" in low:
        return "data_tampering"
    if "drift" in low or "skew" in low:
        return "model_drift"
    return "unknown"


def evaluate_rubric(scenario: SecurityScenario) -> Dict[str, Any]:
    """Check structural rubric criteria."""
    for field in ("asset", "threat", "control", "residual_risk"):
        val = getattr(scenario, field, None)
        if not val or not str(val).strip():
            return {
                "scenario_id": scenario.scenario_id,
                "verdict": "FAIL",
                "reason": f"Missing required field: {field}",
            }

    threat_cat = _classify_threat(scenario.threat)
    expected_kw = KEYWORD_MAPPING.get(threat_cat, ())
    control_low = scenario.control.lower()

    if not any(kw in control_low for kw in expected_kw):
        return {
            "scenario_id": scenario.scenario_id,
            "verdict": "REVIEW",
            "reason": f"Control terms do not match threat category '{threat_cat}'",
        }

    return {
        "scenario_id": scenario.scenario_id,
        "verdict": "PASS",
        "reason": "Complete scenario with relevant control",
    }


FICTIONAL_SCENARIOS = (
    SecurityScenario(
        scenario_id="fictional_complete_pass",
        asset="Aggregated Customer Survey Data",
        threat="Re-identification of respondents via unmasked demographic fields",
        control="Apply k-anonymity aggregation and mask direct identifiers",
        residual_risk="Low: auxiliary datasets could still enable partial attribute inference",
    ),
    SecurityScenario(
        scenario_id="fictional_missing_asset_fail",
        asset=None,  # Missing asset -> FAIL
        threat="Sensor telemetry tampering in raw ingestion bucket",
        control="Enforce cryptographic checksum validation on uploaded batch logs",
        residual_risk="Low: corrupted sensor records rejected at ingestion",
    ),
    SecurityScenario(
        scenario_id="fictional_unrelated_control_review",
        asset="E-commerce Fraud Model Input Features",
        threat="Feature drift in transaction amount distribution",
        control="Upgrade server RAM from 16GB to 32GB",  # Unrelated -> REVIEW
        residual_risk="High: feature drift persists unmonitored",
    ),
)


def run_evaluation_experiment() -> Dict[str, Any]:
    """Compare three small controlled configurations using rubric accuracy and latency metric."""
    configs = {
        "config_single": [FICTIONAL_SCENARIOS[0]],
        "config_triplet": list(FICTIONAL_SCENARIOS),
        "config_batch": list(FICTIONAL_SCENARIOS) * 3,  # 9 items
    }

    expected_verdicts = {
        "fictional_complete_pass": "PASS",
        "fictional_missing_asset_fail": "FAIL",
        "fictional_unrelated_control_review": "REVIEW",
    }

    report = {}
    for name, items in configs.items():
        t0 = time.perf_counter()
        results = [evaluate_rubric(item) for item in items]
        elapsed_us = (time.perf_counter() - t0) * 1_000_000

        correct = sum(1 for r in results if r["verdict"] == expected_verdicts[r["scenario_id"]])
        accuracy = (correct / len(items)) * 100.0

        report[name] = {
            "count": len(items),
            "correctness_pct": accuracy,
            "total_microseconds": round(elapsed_us, 2),
            "us_per_item": round(elapsed_us / len(items), 2),
            "verdicts": [r["verdict"] for r in results],
        }

    return report


def main() -> None:
    exp_report = run_evaluation_experiment()
    print(json.dumps(exp_report, indent=2))


if __name__ == "__main__":
    main()
