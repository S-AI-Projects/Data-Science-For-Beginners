"""Check rubric outcomes and deterministic input-size trade-off."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import SCENARIOS, check_scenario, compare_sizes, fixture


EXPECTED_COMPARISON = [
    {"scenarios": 1, "expected_statuses": ["pass"],
     "actual_statuses": ["pass"], "required_field_checks": 4, "correct": True},
    {"scenarios": 2, "expected_statuses": ["pass", "pass"],
     "actual_statuses": ["pass", "pass"], "required_field_checks": 8,
     "correct": True},
    {"scenarios": 3, "expected_statuses": ["pass", "pass", "pass"],
     "actual_statuses": ["pass", "pass", "pass"],
     "required_field_checks": 12, "correct": True},
]


class RubricTests(unittest.TestCase):
    def test_complete_scenarios_pass(self):
        self.assertEqual(len(SCENARIOS), 3)
        self.assertEqual([check_scenario(row)["status"] for row in fixture()],
                         ["pass", "pass", "pass"])

    def test_missing_asset_fails(self):
        self.assertEqual(check_scenario(fixture("missing-asset")[0]), {
            "status": "fail", "issues": ["missing or invalid: asset"],
            "field_checks": 4,
        })

    def test_unrelated_control_requests_review(self):
        self.assertEqual(check_scenario(fixture("unrelated-control")[0]), {
            "status": "review", "issues": ["unlisted threat/control pair"],
            "field_checks": 4,
        })

    def test_required_fields_are_nonblank_strings(self):
        for field in ["asset", "threat", "control", "residual_risk"]:
            for value in [None, "", " \t", 0, True, []]:
                with self.subTest(field=field, value=value):
                    row = {**SCENARIOS[0], field: value}
                    self.assertEqual(check_scenario(row)["status"], "fail")
        self.assertEqual(check_scenario(None)["status"], "fail")

    def test_all_size_comparisons_match_literal_expectations(self):
        self.assertEqual(compare_sizes(fixture()), EXPECTED_COMPARISON)
        self.assertTrue(all(row["correct"] for row in compare_sizes(fixture())))

    def test_input_sizes_grow_checks_linearly(self):
        checks = [row["required_field_checks"] for row in compare_sizes(fixture())]
        self.assertEqual(checks, [4, 8, 12])
        self.assertEqual([b - a for a, b in zip(checks, checks[1:])], [4, 4])

    def test_empty_comparison_has_no_sizes(self):
        self.assertEqual(compare_sizes([]), [])


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
        self.assertEqual([row["status"] for row in report["results"]],
                         ["pass", "pass", "pass"])
        self.assertEqual(report["size_comparison"], EXPECTED_COMPARISON)

    def test_failure_and_review_in_fresh_processes(self):
        for case, code, first_status in [("missing-asset", 1, "fail"),
                                         ("unrelated-control", 3, "review")]:
            with self.subTest(case=case):
                result = self.run_example("--case", case)
                self.assertEqual(result.returncode, code, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["results"][0]["status"], first_status)
                self.assertEqual(report["size_comparison"], EXPECTED_COMPARISON)


if __name__ == "__main__":
    unittest.main()
