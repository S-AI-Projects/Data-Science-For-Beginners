"""Check every prefix state and its link to the final group report."""

from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import summarize_group


class RateTests(unittest.TestCase):
    def check_trace_invariant(self, outcomes, report):
        trace = report["trace"]
        self.assertEqual(len(trace), len(outcomes) + 1)
        for step, state in enumerate(trace):
            with self.subTest(step=step, outcomes=outcomes):
                # Compute the oracle from the original prefix, not the trace.
                prefix = outcomes[:step]
                expected_n = len(prefix)
                expected_successes = sum(prefix)
                expected_rate = (expected_successes / expected_n
                                 if expected_n else None)
                self.assertEqual(state, {"n": expected_n,
                                         "successes": expected_successes,
                                         "rate": expected_rate})
                self.assertLessEqual(0, state["successes"])
                self.assertLessEqual(state["successes"], state["n"])
                if step:
                    self.assertEqual(state["n"], trace[step - 1]["n"] + 1)
                    self.assertEqual(state["successes"],
                                     trace[step - 1]["successes"]
                                     + outcomes[step - 1])
        self.assertEqual({key: report[key] for key in ("n", "successes", "rate")},
                         trace[-1])

    def test_fixture_rates_keep_distinct_denominators(self):
        a = summarize_group([1, 0])
        b = summarize_group([1, 1, 0, 0])
        self.assertEqual((a["n"], a["successes"], a["rate"]), (2, 1, 0.5))
        self.assertEqual((b["n"], b["successes"], b["rate"]), (4, 2, 0.5))
        self.check_trace_invariant([1, 0], a)
        self.check_trace_invariant([1, 1, 0, 0], b)

    def test_exact_fixture_trace(self):
        self.assertEqual(summarize_group([1, 0])["trace"], [
            {"n": 0, "successes": 0, "rate": None},
            {"n": 1, "successes": 1, "rate": 1.0},
            {"n": 2, "successes": 1, "rate": 0.5},
        ])

    def test_invariant_for_all_short_binary_sequences(self):
        for length in range(5):
            for sequence in product((0, 1), repeat=length):
                outcomes = list(sequence)
                self.check_trace_invariant(outcomes, summarize_group(outcomes))

    def test_empty_is_undefined_and_zero_is_observed(self):
        self.assertEqual(summarize_group([]), {
            "n": 0, "successes": 0, "rate": None,
            "trace": [{"n": 0, "successes": 0, "rate": None}],
        })
        self.assertEqual(summarize_group([0])["rate"], 0.0)
        self.assertEqual(summarize_group([1])["rate"], 1.0)

    def test_inputs_are_not_modified(self):
        outcomes = [1, 0]
        summarize_group(outcomes)
        self.assertEqual(outcomes, [1, 0])

    def test_invalid_outcomes(self):
        for outcomes in [None, "10", {}, [None], [True], [False], [0.0],
                         ["1"], [-1], [2], [1, 0, None]]:
            with self.subTest(outcomes=outcomes):
                with self.assertRaises(ValueError):
                    summarize_group(outcomes)


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py")), *args],
            capture_output=True, text=True, check=False,
        )

    def test_default_fixture_in_fresh_process(self):
        result = self.run_example()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        for group, n, successes in [("A", 2, 1), ("B", 4, 2)]:
            self.assertEqual(report[group]["n"], n)
            self.assertEqual(report[group]["successes"], successes)
            self.assertEqual(report[group]["rate"], 0.5)
        self.assertEqual(result.stderr, "")

    def test_boundaries_in_fresh_processes(self):
        for a, b, expected_rates in [([], [], (None, None)),
                                     ([0], [1], (0.0, 1.0))]:
            with self.subTest(a=a, b=b):
                result = self.run_example("--a", json.dumps(a),
                                          "--b", json.dumps(b))
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                for group, values, rate in [("A", a, expected_rates[0]),
                                            ("B", b, expected_rates[1])]:
                    self.assertEqual(report[group]["n"], len(values))
                    self.assertEqual(report[group]["rate"], rate)

    def test_invalid_inputs_in_fresh_processes(self):
        for args in [["--a", "[2]"], ["--b", "[null]"],
                     ["--a", "[true]"], ["--a", "null"], ["--b", "["]]:
            with self.subTest(args=args):
                result = self.run_example(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
