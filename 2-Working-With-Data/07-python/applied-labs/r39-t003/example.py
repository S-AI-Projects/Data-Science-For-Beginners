"""Training-only mean imputation lab (R39-T003).

Demonstrates fit/transform separation using only the Python 3 standard library:
fit a missing-value mean on training observations only, then apply that stored
mean to validation observations without refitting. Also provides a simpler
independent calculation and an explicit expected-result table for comparison
on identical inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable, List, Optional, Sequence, Tuple


NumericOrNone = Optional[float]


def _validate_non_bool_number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"Expected int, float, or None; got {type(value).__name__}")
    return float(value)


class TrainingOnlyMeanImputer:
    """Stateful imputer that fits a mean on training data and freezes it."""

    def __init__(self) -> None:
        self.fill_value_: Optional[float] = None

    def fit(self, train_values: Sequence[NumericOrNone]) -> "TrainingOnlyMeanImputer":
        observed = [
            _validate_non_bool_number(v) for v in train_values if v is not None
        ]
        if not observed:
            raise ValueError(
                "Cannot fit mean imputer on empty or all-missing training input."
            )
        self.fill_value_ = sum(observed) / len(observed)
        return self

    def transform(self, values: Sequence[NumericOrNone]) -> List[float]:
        if self.fill_value_ is None:
            raise RuntimeError("Imputer must be fitted before calling transform().")
        result: List[float] = []
        for v in values:
            if v is None:
                result.append(self.fill_value_)
            else:
                result.append(_validate_non_bool_number(v))
        return result

    def fit_transform(self, train_values: Sequence[NumericOrNone]) -> List[float]:
        return self.fit(train_values).transform(train_values)


def independent_reference_impute(
    train_values: Sequence[NumericOrNone],
    target_values: Sequence[NumericOrNone],
) -> Tuple[float, List[float]]:
    """Simpler independent calculation using statistics.mean on training data."""
    observed = [_validate_non_bool_number(v) for v in train_values if v is not None]
    if not observed:
        raise ValueError(
            "Cannot compute reference mean on empty or all-missing training input."
        )
    train_mean = float(mean(observed))
    imputed = [
        train_mean if v is None else _validate_non_bool_number(v)
        for v in target_values
    ]
    return train_mean, imputed


@dataclass(frozen=True)
class ComparisonCase:
    name: str
    train: Tuple[NumericOrNone, ...]
    validation: Tuple[NumericOrNone, ...]
    expected_mean: float
    expected_validation: Tuple[float, ...]


EXPECTED_RESULTS_TABLE: Tuple[ComparisonCase, ...] = (
    ComparisonCase(
        name="leakage_guard_primary_fixture",
        train=(2, None, 4),
        validation=(100, None),
        expected_mean=3.0,
        expected_validation=(100.0, 3.0),
    ),
    ComparisonCase(
        name="all_missing_validation",
        train=(2, None, 4),
        validation=(None, None),
        expected_mean=3.0,
        expected_validation=(3.0, 3.0),
    ),
    ComparisonCase(
        name="no_missing_validation",
        train=(2, 4, 6),
        validation=(10, 20),
        expected_mean=4.0,
        expected_validation=(10.0, 20.0),
    ),
)


def compare_approaches(
    cases: Iterable[ComparisonCase] = EXPECTED_RESULTS_TABLE,
) -> List[dict]:
    """Compare TrainingOnlyMeanImputer against independent calculation and table."""
    rows: List[dict] = []
    for case in cases:
        imputer = TrainingOnlyMeanImputer().fit(case.train)
        direct_out = imputer.transform(case.validation)
        ref_mean, ref_out = independent_reference_impute(case.train, case.validation)
        rows.append(
            {
                "case": case.name,
                "train": list(case.train),
                "validation": list(case.validation),
                "expected_mean": case.expected_mean,
                "direct_mean": imputer.fill_value_,
                "reference_mean": ref_mean,
                "expected_validation": list(case.expected_validation),
                "direct_validation": direct_out,
                "reference_validation": ref_out,
                "all_match": (
                    imputer.fill_value_ == ref_mean == case.expected_mean
                    and direct_out == ref_out == list(case.expected_validation)
                ),
            }
        )
    return rows


if __name__ == "__main__":
    for row in compare_approaches():
        print(
            f"{row['case']}: mean={row['direct_mean']} "
            f"(ref={row['reference_mean']}, expected={row['expected_mean']}) -> "
            f"val={row['direct_validation']} | match={row['all_match']}"
        )
