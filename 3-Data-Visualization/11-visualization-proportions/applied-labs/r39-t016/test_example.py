"""Literal expectations and a frozen pre-extraction teaching baseline."""

import json
import math
from pathlib import Path
import subprocess
import sys
import unittest

from example import proportions


def baseline_proportions(counts):
    """Original inline implementation, kept to check before/after equivalence."""
    if not isinstance(counts, dict):
        raise ValueError("counts must be an object")
    for label, count in counts.items():
        if not isinstance(label, str) or not label.strip():
            raise ValueError("labels must be nonblank strings")
        if type(count) is not int or count < 0:
            raise ValueError("counts must be nonnegative integers")
    count_total = sum(counts.values())
    if count_total == 0:
        return {"status": "no-data", "count_total": 0,
                "proportions": {}, "total": None}
    shares = {label: counts[label] / count_total for label in sorted(counts)}
    return {"status": "ok", "count_total": count_total,
            "proportions": shares, "total": math.fsum(shares.values())}


CASES = [
    ({"A": 2, "B": 3}, {"status": "ok", "count_total": 5,
                        "proportions": {"A": 0.4, "B": 0.6}, "total": 1.0}),
    ({"A": 1}, {"status": "ok", "count_total": 1,
                "proportions": {"A": 1.0}, "total": 1.0}),
    ({"A": 0, "B": 3}, {"status": "ok", "count_total": 3,
                        "proportions": {"A": 0.0, "B": 1.0}, "total": 1.0}),
    ({"A": 0, "B": 0}, {"status": "no-data", "count_total": 0,
                        "proportions": {}, "total": None}),
    ({}, {"status": "no-data", "count_total": 0,
          "proportions": {}, "total": None}),
]
INVALID = [None, [], "counts", {"A": -1}, {"A": True}, {"A": 1.0},
           {"A": None}, {"A": "2"}, {"": 2}, {" ": 0}, {1: 2}]


class ProportionTests(unittest.TestCase):
    def test_literal_results_and_before_after_equivalence(self):
        for counts, expected in CASES:
            with self.subTest(counts=counts):
                self.assertEqual(baseline_proportions(counts), expected)
                self.assertEqual(proportions(counts), expected)
                self.assertEqual(proportions(counts), baseline_proportions(counts))

    def test_invalid_inputs_keep_exception_contract(self):
        for counts in INVALID:
            with self.subTest(counts=counts):
                with self.assertRaises(ValueError) as before:
                    baseline_proportions(counts)
                with self.assertRaises(ValueError) as after:
                    proportions(counts)
                self.assertEqual(str(before.exception), str(after.exception))

    def test_sorting_keeps_labels_attached_to_values(self):
        result = proportions({"B": 3, "A": 2})
        self.assertEqual(list(result["proportions"].items()),
                         [("A", 0.4), ("B", 0.6)])

    def test_nonterminating_fractions_sum_to_one_with_tolerance(self):
        counts = {"A": 1, "B": 1, "C": 1}
        result = proportions(counts)
        self.assertEqual(result, baseline_proportions(counts))
        for share in result["proportions"].values():
            self.assertAlmostEqual(share, 1 / 3)
        self.assertTrue(math.isclose(result["total"], 1.0, abs_tol=1e-12))

    def test_zero_total_is_not_a_set_of_zero_proportions(self):
        for counts in [{}, {"A": 0}, {"A": 0, "B": 0}]:
            with self.subTest(counts=counts):
                result = proportions(counts)
                self.assertEqual(result["status"], "no-data")
                self.assertEqual(result["proportions"], {})
                self.assertIsNone(result["total"])

    def test_input_is_unchanged(self):
        counts = {"B": 3, "A": 2}
        proportions(counts)
        self.assertEqual(list(counts.items()), [("B", 3), ("A", 2)])


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py")), *args],
            capture_output=True, text=True, check=False,
        )

    def test_default_fixture_in_fresh_process(self):
        result = self.run_example()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), CASES[0][1])
        self.assertEqual(result.stderr, "")

    def test_boundaries_in_fresh_processes(self):
        for counts, expected in CASES:
            with self.subTest(counts=counts):
                result = self.run_example("--counts", json.dumps(counts))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), expected)

    def test_failures_in_fresh_processes(self):
        for raw in ['{"A":-1}', '{"A":null}', '{"A":true}', "null", "{"]:
            with self.subTest(raw=raw):
                result = self.run_example("--counts", raw)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
