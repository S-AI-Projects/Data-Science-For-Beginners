"""Fit a mean on local training data, then reuse it for missing values."""

import argparse
import json
import math


TRAINING = [2, None, 4]
VALIDATION = [100, None]


def is_finite_number(value):
    """Accept finite Python int/float values, excluding booleans."""
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def validate_values(values):
    """Only None represents missing data in this small example."""
    if not isinstance(values, list) or any(
        value is not None and not is_finite_number(value) for value in values
    ):
        raise ValueError("values must be a list of finite numbers or None")


def fit_mean(training):
    """Learn one replacement value from observed training values only."""
    validate_values(training)
    observed = [value for value in training if value is not None]
    if not observed:
        raise ValueError("training must contain at least one observed value")
    try:
        mean = sum(observed) / len(observed)
    except OverflowError as error:
        raise ValueError(
            "training mean is outside the supported numeric range"
        ) from error
    if not is_finite_number(mean):
        raise ValueError("training mean is outside the supported numeric range")
    return mean


def transform(values, training_mean):
    """Fill missing entries with a stored mean, without fitting or mutation."""
    validate_values(values)
    if not is_finite_number(training_mean):
        raise ValueError("training_mean must be a finite number")
    return [training_mean if value is None else value for value in values]


def main():
    """Run the fixture or JSON lists supplied on the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--training", default=json.dumps(TRAINING))
    parser.add_argument("--validation", default=json.dumps(VALIDATION))
    args = parser.parse_args()
    try:
        training = json.loads(args.training)
        validation = json.loads(args.validation)
        training_mean = fit_mean(training)
        result = {"training_mean": training_mean,
                  "validation": transform(validation, training_mean)}
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
