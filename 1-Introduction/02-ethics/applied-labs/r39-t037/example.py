"""Audit subgroup accuracy metric claims for uncertainty and subgroup representation.

Illustrates the ethical principles of Fairness, Data Quality, Algorithm Fairness,
and Misrepresentation discussed in 1-Introduction/02-ethics/README.md.
"""

from dataclasses import dataclass
import math
from typing import Mapping, Sequence, Tuple


@dataclass(frozen=True)
class GroupEvaluation:
    group_name: str
    sample_size: int
    correct_count: int
    accuracy: float
    ci_lower: float
    ci_upper: float
    is_adequately_powered: bool
    warning: str


@dataclass(frozen=True)
class AuditReport:
    overall_accuracy: float
    overall_sample_size: int
    group_evaluations: Tuple[GroupEvaluation, ...]
    unsupported_claim_detected: bool
    findings: Tuple[str, ...]


def wilson_score_interval(correct: int, total: int, z: float = 1.96) -> Tuple[float, float]:
    """Compute the Wilson score confidence interval for a binomial proportion.

    Used to quantify uncertainty around metric claims, especially with small denominators.
    """
    if total <= 0:
        raise ValueError("Total must be a positive integer, got {}".format(total))
    if correct < 0 or correct > total:
        raise ValueError("Correct count must be between 0 and total ({}), got {}".format(total, correct))

    p = correct / total
    denominator = 1.0 + (z**2) / total
    center = (p + (z**2) / (2.0 * total)) / denominator
    half_width = (z * math.sqrt((p * (1.0 - p) / total) + (z**2) / (4.0 * (total**2)))) / denominator

    lower = max(0.0, center - half_width)
    upper = min(1.0, center + half_width)
    return round(lower, 4), round(upper, 4)


def evaluate_metric_claims(
    groups: Sequence[Mapping[str, object]],
    claimed_accuracy_threshold: float = 0.90,
    min_subgroup_sample_size: int = 30,
) -> AuditReport:
    """Evaluate subgroup accuracy claims against group denominators and confidence intervals.

    Checks:
    1. Input validation (types, bounds, completeness).
    2. Group denominator sample size against minimum threshold.
    3. Binomial confidence intervals (uncertainty).
    4. Unsupported claims: when overall accuracy is high or claimed threshold is met overall,
       but specific subgroup sample sizes are too small to support confident claims, or
       subgroup lower confidence bounds fall below acceptable thresholds.
    """
    if not isinstance(claimed_accuracy_threshold, (int, float)) or isinstance(claimed_accuracy_threshold, bool):
        raise TypeError("claimed_accuracy_threshold must be a float or int")
    if not (0.0 <= claimed_accuracy_threshold <= 1.0):
        raise ValueError("claimed_accuracy_threshold must be between 0.0 and 1.0")

    if not isinstance(min_subgroup_sample_size, int) or isinstance(min_subgroup_sample_size, bool):
        raise TypeError("min_subgroup_sample_size must be an integer")
    if min_subgroup_sample_size <= 0:
        raise ValueError("min_subgroup_sample_size must be positive")

    if not isinstance(groups, Sequence) or isinstance(groups, (str, bytes)):
        raise TypeError("groups must be a sequence of mappings")
    if len(groups) == 0:
        raise ValueError("groups sequence cannot be empty")

    total_samples = 0
    total_correct = 0
    group_evals = []
    findings = []
    unsupported_claim = False

    for idx, grp in enumerate(groups):
        if not isinstance(grp, Mapping):
            raise TypeError("Group item at index {} must be a mapping".format(idx))

        name = grp.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Group item at index {} missing non-empty 'name'".format(idx))

        sample_size = grp.get("sample_size")
        if not isinstance(sample_size, int) or isinstance(sample_size, bool):
            raise TypeError("Group '{}' sample_size must be an integer".format(name))
        if sample_size <= 0:
            raise ValueError("Group '{}' sample_size must be positive".format(name))

        correct_count = grp.get("correct_count")
        if not isinstance(correct_count, int) or isinstance(correct_count, bool):
            raise TypeError("Group '{}' correct_count must be an integer".format(name))
        if correct_count < 0 or correct_count > sample_size:
            raise ValueError("Group '{}' correct_count must be between 0 and sample_size".format(name))

        accuracy = round(correct_count / sample_size, 4)
        ci_lower, ci_upper = wilson_score_interval(correct_count, sample_size)
        adequately_powered = sample_size >= min_subgroup_sample_size

        warning = ""
        if not adequately_powered:
            warning = "Sample size {} is below minimum power threshold ({}): high uncertainty (CI: [{:.2f}, {:.2f}])".format(
                sample_size, min_subgroup_sample_size, ci_lower, ci_upper
            )
            findings.append("Subgroup '{}': {}".format(name, warning))
            unsupported_claim = True
        elif ci_lower < claimed_accuracy_threshold:
            warning = "Lower confidence bound ({:.2f}) falls below claimed threshold ({:.2f})".format(
                ci_lower, claimed_accuracy_threshold
            )
            findings.append("Subgroup '{}': {}".format(name, warning))
            unsupported_claim = True

        total_samples += sample_size
        total_correct += correct_count

        group_evals.append(
            GroupEvaluation(
                group_name=name,
                sample_size=sample_size,
                correct_count=correct_count,
                accuracy=accuracy,
                ci_lower=ci_lower,
                ci_upper=ci_upper,
                is_adequately_powered=adequately_powered,
                warning=warning,
            )
        )

    overall_accuracy = round(total_correct / total_samples, 4)
    if overall_accuracy >= claimed_accuracy_threshold and unsupported_claim:
        findings.append(
            "Overall accuracy claim ({:.1f}%) conceals high uncertainty or disparity in subgroup metric claims.".format(
                overall_accuracy * 100
            )
        )

    return AuditReport(
        overall_accuracy=overall_accuracy,
        overall_sample_size=total_samples,
        group_evaluations=tuple(group_evals),
        unsupported_claim_detected=unsupported_claim,
        findings=tuple(findings),
    )


# Standard small local fixtures inspired by Gender Shades & Street Bump case studies
FIXTURES = (
    {
        "name": "Subgroup A (Majority)",
        "sample_size": 950,
        "correct_count": 903,  # 95.05%
    },
    {
        "name": "Subgroup B (Adequate Minority)",
        "sample_size": 120,
        "correct_count": 109,  # 90.83%
    },
    {
        "name": "Subgroup C (Under-sampled Minority)",
        "sample_size": 10,
        "correct_count": 9,  # 90.00% point estimate, but wide CI [59.6%, 98.2%]
    },
)


def main() -> None:
    report = evaluate_metric_claims(FIXTURES, claimed_accuracy_threshold=0.90, min_subgroup_sample_size=30)
    print("Aggregate Evaluation:")
    print("  Total Samples: {}".format(report.overall_sample_size))
    print("  Overall Accuracy: {:.2f}%".format(report.overall_accuracy * 100))
    print("Subgroup Metric Audit:")
    for ge in report.group_evaluations:
        status = "ADEQUATE" if ge.is_adequately_powered else "UNDERPOWERED"
        print(
            "  - {}: n={}, accuracy={:.2f}%, 95% CI=[{:.2f}%, {:.2f}%] [{}]".format(
                ge.group_name,
                ge.sample_size,
                ge.accuracy * 100,
                ge.ci_lower * 100,
                ge.ci_upper * 100,
                status,
            )
        )
    print("Claim Audit:")
    print("  Unsupported claims detected: {}".format(report.unsupported_claim_detected))
    for finding in report.findings:
        print("  * {}".format(finding))


if __name__ == "__main__":
    main()
