"""Compare the implementation with explicit, independently calculated results."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import fit_mean, transform


# Hand-calculated expectations: no production helper computes the oracle.
# training, validation, mean, transformed validation
CASES = [
    ([2, None, 4], [100, None], 3, [100, 3]),
    ([2, None, 4], [-100, None], 3, [-100, 3]),
    ([7], [None], 7, [7]),
    ([None, 0], [None, 8], 0, [0, 8]),
    ([-2, None, 4], [None, -9], 1, [1, -9]),
    ([1, 2], [None], 1.5, [1.5]),
    ([2, None, 4], [], 3, []),
    ([2, None, 4], [None, None], 3, [3, 3]),
    ([2, None, 4], [100, 200], 3, [100, 200]),
]


class ImputationTests(unittest.TestCase):
    def test_against_explicit_expected_table(self):
        for training, validation, expected_mean, expected_values in CASES:
            with self.subTest(training=training, validation=validation):
                mean = fit_mean(training)
                self.assertEqual(mean, expected_mean)
                self.assertEqual(transform(validation, mean), expected_values)

    def test_transform_reuses_mean_without_refitting(self):
        mean = fit_mean([2, None, 4])
        self.assertEqual(transform([100, None], mean), [100, 3])
        self.assertEqual(transform([1000, None], mean), [1000, 3])
        self.assertEqual(transform([None], mean), [3])
        self.assertEqual(mean, 3)

    def test_inputs_are_not_changed(self):
        training = [2, None, 4]
        validation = [100, None]
        result = transform(validation, fit_mean(training))
        self.assertEqual(training, [2, None, 4])
        self.assertEqual(validation, [100, None])
        self.assertIsNot(result, validation)

    def test_no_observed_training_values(self):
        for training in [[], [None], [None, None]]:
            with self.subTest(training=training):
                with self.assertRaisesRegex(ValueError, "at least one observed"):
                    fit_mean(training)

    def test_invalid_values(self):
        for values in [None, "2", {}, ["2"], [True], [float("nan")],
                       [float("inf")], [float("-inf")]]:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    fit_mean(values)
                with self.assertRaises(ValueError):
                    transform(values, 3)

    def test_invalid_stored_mean(self):
        for mean in [None, True, "3", float("nan"), float("inf")]:
            with self.subTest(mean=mean):
                with self.assertRaises(ValueError):
                    transform([None], mean)


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py")), *args],
            capture_output=True, text=True, check=False,
        )

    def test_default_fixture_in_fresh_process(self):
        result = self.run_example()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout),
                         {"training_mean": 3, "validation": [100, 3]})

    def test_table_in_fresh_processes(self):
        for training, validation, mean, expected in CASES:
            with self.subTest(training=training, validation=validation):
                result = self.run_example("--training", json.dumps(training),
                                          "--validation", json.dumps(validation))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout),
                                 {"training_mean": mean, "validation": expected})
                self.assertEqual(result.stderr, "")

    def test_failures_in_fresh_processes(self):
        for args in [["--training", "[null,null]"], ["--training", "[]"],
                     ["--training", '["2"]'], ["--validation", "[true]"],
                     ["--training", "["], ["--validation", "null"]]:
            with self.subTest(args=args):
                result = self.run_example(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
