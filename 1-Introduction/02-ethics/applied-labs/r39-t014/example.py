"""Trace descriptive outcome rates for two fictional groups."""

import argparse
import json


GROUP_A = [1, 0]
GROUP_B = [1, 1, 0, 0]


def summarize_group(outcomes):
    """Record initial state and a snapshot after each binary observation.

    Only integer 0 and 1 are accepted. An empty group has an undefined rate,
    represented by None, rather than an observed rate of zero.
    """
    if not isinstance(outcomes, list) or any(
        type(outcome) is not int or outcome not in (0, 1)
        for outcome in outcomes
    ):
        raise ValueError("outcomes must be a list of integer 0 or 1 values")

    n = 0
    successes = 0
    trace = [{"n": 0, "successes": 0, "rate": None}]
    for outcome in outcomes:
        n += 1
        successes += outcome
        trace.append({"n": n, "successes": successes, "rate": successes / n})

    final = dict(trace[-1])
    return {**final, "trace": trace}


def main():
    """Print the local fixture report, or exit 2 for invalid inputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", default=json.dumps(GROUP_A),
                        help="JSON list of binary outcomes for group A")
    parser.add_argument("--b", default=json.dumps(GROUP_B),
                        help="JSON list of binary outcomes for group B")
    args = parser.parse_args()
    try:
        report = {"A": summarize_group(json.loads(args.a)),
                  "B": summarize_group(json.loads(args.b))}
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(report, allow_nan=False))


if __name__ == "__main__":
    main()
