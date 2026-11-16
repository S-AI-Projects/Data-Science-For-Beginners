"""Summarize a small local category fixture using only the standard library."""

import argparse
from collections import Counter
import json


FIXTURE = ["A", "A", "B", "C", "C", "C"]


def validate_labels(labels, name):
    """Require a list of nonblank strings, without silently cleaning labels."""
    if not isinstance(labels, list):
        raise ValueError(name + " must be a list of nonblank strings")
    if any(not isinstance(label, str) or not label.strip() for label in labels):
        raise ValueError(name + " must be a list of nonblank strings")


def summarize(rows, include=None):
    """Return sorted label/count pairs and the total for exactly those pairs.

    None includes every category; an empty inclusion list includes none.
    Labels match exactly (case and surrounding spaces are significant).
    Validate all input before filtering so invalid rows cannot be hidden.
    """
    validate_labels(rows, "rows")
    if include is not None:
        validate_labels(include, "include")
    allowed = None if include is None else set(include)
    counts = Counter(row for row in rows if allowed is None or row in allowed)
    counts = dict(sorted(counts.items()))
    return {"counts": counts, "total": sum(counts.values())}


def main():
    """Print a JSON report, or exit 2 for malformed or invalid input."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", default=json.dumps(FIXTURE),
                        help="JSON list of category strings (default: local fixture)")
    parser.add_argument("--include", help="JSON list of categories to retain")
    args = parser.parse_args()
    try:
        rows = json.loads(args.rows)
        include = None
        if args.include is not None:
            include = json.loads(args.include)
            # An omitted filter is different from an explicitly invalid null.
            validate_labels(include, "include")
        result = summarize(rows, include)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result))


if __name__ == "__main__":
    main()
