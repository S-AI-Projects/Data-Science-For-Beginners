"""Normalize small local category counts with an explicit zero-total policy."""

import argparse
import json
import math


FIXTURE = {"A": 2, "B": 3}


def validate_counts(counts):
    """Require nonblank category labels and nonnegative integer counts."""
    if not isinstance(counts, dict):
        raise ValueError("counts must be an object")
    for label, count in counts.items():
        if not isinstance(label, str) or not label.strip():
            raise ValueError("labels must be nonblank strings")
        if type(count) is not int or count < 0:
            raise ValueError("counts must be nonnegative integers")


def proportions(counts):
    """Return labelled proportions, or an explicit no-data report."""
    validate_counts(counts)
    count_total = sum(counts.values())
    if count_total == 0:
        return {"status": "no-data", "count_total": 0,
                "proportions": {}, "total": None}
    shares = {label: counts[label] / count_total for label in sorted(counts)}
    return {"status": "ok", "count_total": count_total,
            "proportions": shares, "total": math.fsum(shares.values())}


def main():
    """Print a JSON report; malformed or invalid counts exit 2."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counts", default=json.dumps(FIXTURE),
                        help="JSON object mapping category labels to counts")
    args = parser.parse_args()
    try:
        result = proportions(json.loads(args.counts))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
