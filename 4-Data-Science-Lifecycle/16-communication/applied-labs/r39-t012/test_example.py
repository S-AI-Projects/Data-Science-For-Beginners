"""Contract checks, including fresh-process command-line checks."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import FIXTURE, summarize


class SummaryTests(unittest.TestCase):
    def test_full_fixture_and_label_alignment(self):
        expected = {"counts": {"A": 2, "B": 1, "C": 3}, "total": 6}
        self.assertEqual(summarize(FIXTURE), expected)
        self.assertEqual(summarize(list(reversed(FIXTURE))), expected)
        self.assertEqual(list(summarize(FIXTURE)["counts"]), ["A", "B", "C"])

    def test_filter_changes_counts_and_total_together(self):
        expected = {"counts": {"A": 2, "B": 1}, "total": 3}
        self.assertEqual(summarize(FIXTURE, ["B", "A"]), expected)
        self.assertEqual(summarize(FIXTURE, ["A", "A", "B"]), expected)

    def test_smallest_nonempty_fixture(self):
        self.assertEqual(summarize(["A"]), {"counts": {"A": 1}, "total": 1})

    def test_empty_boundaries(self):
        for rows, include in [([], None), ([], ["A"]), (["A"], []),
                              (FIXTURE, ["Z"])]:
            with self.subTest(rows=rows, include=include):
                self.assertEqual(summarize(rows, include),
                                 {"counts": {}, "total": 0})

    def test_labels_match_exactly(self):
        self.assertEqual(summarize(["A", "a", " A "], ["A"]),
                         {"counts": {"A": 1}, "total": 1})

    def test_invalid_rows_even_when_filtered_out(self):
        for rows in [None, "A", {}, [""], [" \t"], [None], [1], [True],
                     ["A", ""]]:
            with self.subTest(rows=rows):
                with self.assertRaises(ValueError):
                    summarize(rows, ["A"])

    def test_invalid_filter(self):
        for include in ["A", {}, [""], [" "], [None], [1]]:
            with self.subTest(include=include):
                with self.assertRaises(ValueError):
                    summarize(FIXTURE, include)


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py")), *args],
            capture_output=True, text=True, check=False,
        )

    def test_fresh_process_normal_and_boundaries(self):
        cases = [
            ([], {"counts": {"A": 2, "B": 1, "C": 3}, "total": 6}),
            (["--include", '["A","B"]'],
             {"counts": {"A": 2, "B": 1}, "total": 3}),
            (["--rows", '["A"]'], {"counts": {"A": 1}, "total": 1}),
            (["--rows", "[]"], {"counts": {}, "total": 0}),
            (["--include", "[]"], {"counts": {}, "total": 0}),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                result = self.run_example(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), expected)
                self.assertEqual(result.stderr, "")

    def test_fresh_process_invalid_inputs(self):
        for args in [["--rows", '[""]'], ["--rows", "null"],
                     ["--rows", "["], ["--include", "null"],
                     ["--rows", '["A", ""]', "--include", '["A"]']]:
            with self.subTest(args=args):
                result = self.run_example(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
