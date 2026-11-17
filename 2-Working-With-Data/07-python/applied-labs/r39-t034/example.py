"""Fit a missing-value replacement on training data, then reuse it."""

from typing import Dict, List, Optional, Sequence, Tuple


class MedianImputer:
    """Replace missing numeric values using the median learned during fit."""

    def __init__(self) -> None:
        self.median: Optional[float] = None

    def fit(self, training_values: Sequence[Optional[float]]) -> "MedianImputer":
        observed = sorted(value for value in training_values if value is not None)
        if not observed:
            raise ValueError("cannot fit median imputer without observed values")

        middle = len(observed) // 2
        if len(observed) % 2:
            self.median = observed[middle]
        else:
            self.median = (observed[middle - 1] + observed[middle]) / 2
        return self

    def transform(self, values: Sequence[Optional[float]]) -> List[float]:
        if self.median is None:
            raise ValueError("fit the imputer before transforming values")
        return [
            self.median if value is None else value
            for value in values
        ]


def run_example() -> Tuple[List[Dict[str, object]], List[float]]:
    training_values = [10.0, None, 30.0]
    test_values = [None, 100.0]
    steps = [
        {
            "name": "inputs",
            "state": {"training": training_values, "test": test_values},
        }
    ]

    imputer = MedianImputer().fit(training_values)
    steps.append({"name": "fit", "state": {"training_median": imputer.median}})

    transformed_training = imputer.transform(training_values)
    steps.append(
        {"name": "transform_training", "state": {"values": transformed_training}}
    )

    final_output = imputer.transform(test_values)
    steps.append(
        {"name": "transform_test", "state": {"values": final_output}}
    )
    return steps, final_output


def main() -> None:
    steps, final_output = run_example()
    for step in steps:
        print("{}: {}".format(step["name"], step["state"]))
    print("Final output:", final_output)


if __name__ == "__main__":
    main()
