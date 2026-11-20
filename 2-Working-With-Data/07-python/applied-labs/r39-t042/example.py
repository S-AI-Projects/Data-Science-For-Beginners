"""Training-only mean imputation with boundary cases (R39-T042).

Extends the Python and Pandas lesson by demonstrating fit/transform separation
to prevent data leakage. Learns missing-value mean exclusively from training
observations, then transforms validation data without refitting.
"""

from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Sequence


class TrainingMeanImputer:
    """Imputer that learns a scalar mean from training data and transforms validation data."""

    def __init__(self) -> None:
        self.mean_: Optional[float] = None

    def fit(self, training: Sequence[Optional[float]]) -> TrainingMeanImputer:
        """Fit imputer on training observations only.

        Boundary decision: Rejects empty or all-missing inputs because a valid
        imputation mean cannot be determined without at least one observed value.
        """
        valid = [x for x in training if x is not None]
        if not valid:
            raise ValueError("Cannot fit imputer: all training observations are missing or list is empty.")
        self.mean_ = float(sum(valid) / len(valid))
        return self

    def transform(self, values: Sequence[Optional[float]]) -> List[float]:
        """Apply stored training mean to replace missing values without refitting."""
        if self.mean_ is None:
            raise RuntimeError("Imputer must be fitted before transforming values.")
        return [self.mean_ if x is None else float(x) for x in values]

    def fit_transform(
        self,
        training: Sequence[Optional[float]],
        validation: Sequence[Optional[float]],
    ) -> Dict[str, Any]:
        """Fit on training observations, then transform validation observations."""
        self.fit(training)
        transformed_validation = self.transform(validation)
        return {
            "training_mean": self.mean_,
            "validation": transformed_validation,
        }


def main() -> None:
    # Stated contract fixture: Training [2,None,4] yields mean 3; validation [100,None] becomes [100,3]
    training = [2, None, 4]
    validation = [100, None]
    imputer = TrainingMeanImputer()
    result = imputer.fit_transform(training, validation)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
