"""Local fixture demonstrating training-only mean imputation (R39-T002).

This is a small, deterministic Python standard-library simulation of
fit/transform separation to prevent validation data leakage.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class TrainingOnlyMeanImputer:
    """Fits a missing-value mean on training observations only."""

    fitted_mean_: Optional[float] = None

    def fit(self, train_values: Iterable[Optional[float]]) -> "TrainingOnlyMeanImputer":
        observed = [float(x) for x in train_values if x is not None]
        if not observed:
            raise ValueError(
                "Training input must contain at least one non-missing observation; "
                "all-missing or empty training data is rejected."
            )
        self.fitted_mean_ = sum(observed) / len(observed)
        return self

    def transform(self, values: Iterable[Optional[float]]) -> list[float]:
        if self.fitted_mean_ is None:
            raise RuntimeError("Imputer must be fitted on training data before transform().")
        return [
            self.fitted_mean_ if x is None else float(x)
            for x in values
        ]

    def fit_transform(self, train_values: Iterable[Optional[float]]) -> list[float]:
        train_list = list(train_values)
        return self.fit(train_list).transform(train_list)


def run_fixture() -> dict[str, object]:
    """Run the smallest valid, boundary, and invalid fixture scenarios."""
    train_sample = [2, None, 4]
    val_sample = [100, None]

    imputer = TrainingOnlyMeanImputer()
    train_imputed = imputer.fit_transform(train_sample)
    val_imputed = imputer.transform(val_sample)

    # Boundary case: single non-missing training value + all-missing validation
    boundary_imputer = TrainingOnlyMeanImputer().fit([None, 5, None])
    boundary_val = boundary_imputer.transform([None, None])

    # Invalid case: all-missing training input must be rejected
    invalid_error = None
    try:
        TrainingOnlyMeanImputer().fit([None, None])
    except ValueError as exc:
        invalid_error = str(exc)

    return {
        "simulation": True,
        "train_input": train_sample,
        "fitted_mean": imputer.fitted_mean_,
        "train_imputed": train_imputed,
        "validation_input": val_sample,
        "validation_imputed": val_imputed,
        "boundary_validation_imputed": boundary_val,
        "all_missing_rejected": invalid_error is not None,
        "invalid_error": invalid_error,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_fixture(), indent=2))
