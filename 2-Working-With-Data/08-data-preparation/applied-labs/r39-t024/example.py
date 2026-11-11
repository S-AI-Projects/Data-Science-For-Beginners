"""
Training-Only Mean Imputation with State Tracing (R39-T024)

Extends lesson 08 (Data Preparation) by enforcing strict separation between
the fit stage (training data) and transform stage (validation/test data).
Prevents data leakage by ensuring validation data never influences the imputed mean.
"""

from typing import Any, Dict, List, Optional


class MeanImputer:
    """
    Imputes missing values (None) using the arithmetic mean computed exclusively
    during the training (fit) phase. Records intermediate states after each operation.
    """

    def __init__(self):
        self.mean_: Optional[float] = None
        self.state_trace: List[Dict[str, Any]] = []

    def fit(self, training_data: List[Optional[float]]) -> "MeanImputer":
        """
        Calculates and stores the mean of non-missing values in training_data.
        Raises ValueError if training_data has no non-missing values.
        """
        valid_values = [v for v in training_data if v is not None]
        if not valid_values:
            raise ValueError("All-missing training input is rejected: cannot fit mean with zero observations.")

        computed_mean = sum(valid_values) / len(valid_values)
        self.mean_ = computed_mean

        self.state_trace.append({
            "step": "fit",
            "total_observed": len(training_data),
            "valid_count": len(valid_values),
            "sum": sum(valid_values),
            "stored_mean": self.mean_
        })
        return self

    def transform(self, data: List[Optional[float]]) -> List[float]:
        """
        Replaces None values with the stored training mean without updating state.
        Raises RuntimeError if transform is called before fit.
        """
        if self.mean_ is None:
            raise RuntimeError("Imputer has not been fitted. Call fit() before transform().")

        imputed_data = []
        imputed_count = 0
        for val in data:
            if val is None:
                imputed_data.append(self.mean_)
                imputed_count += 1
            else:
                imputed_data.append(val)

        self.state_trace.append({
            "step": "transform",
            "total_records": len(data),
            "imputed_count": imputed_count,
            "applied_mean": self.mean_
        })
        return imputed_data

    def fit_transform(self, training_data: List[Optional[float]]) -> List[float]:
        return self.fit(training_data).transform(training_data)


if __name__ == "__main__":
    train = [2, None, 4]
    val = [100, None]

    imputer = MeanImputer()
    train_imputed = imputer.fit_transform(train)
    print("Train imputed:", train_imputed, "Stored mean:", imputer.mean_)

    val_imputed = imputer.transform(val)
    print("Validation imputed:", val_imputed)
    print("State trace:", imputer.state_trace)
