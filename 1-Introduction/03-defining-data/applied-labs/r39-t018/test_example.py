"""Test the rubric and demonstrate process recovery after a failed record."""

from copy import deepcopy
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import unittest

from example import FIELDS, SCENARIOS, check_scenario, evaluate_sequence, fixture


LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[3]
INVALID = {
    "threat": "unauthorized_database_read",
    "control": "limit_database_access",
    "residual_risk": "An authorized reader could still share an export.",
}
RECOVERY = {
    "asset": "Fictional customer table with named columns",
    **INVALID,
}


class RubricTests(unittest.TestCase):
    def test_three_complete_data_definition_scenarios_pass(self):
        self.assertEqual(len(SCENARIOS), 3)
        for scenario in fixture():
            with self.subTest(section=scenario["section"]):
                self.assertEqual(check_scenario(scenario),
                                 {"status": "pass", "issues": []})

    def test_missing_asset_reports_a_specific_failure(self):
        self.assertEqual(check_scenario(INVALID),
                         {"status": "fail", "issues": ["missing or invalid: asset"]})

    def test_invalid_record_does_not_block_next_valid_record(self):
        results = evaluate_sequence([INVALID, RECOVERY])
        self.assertEqual(results, [
            {"status": "fail", "issues": ["missing or invalid: asset"]},
            {"status": "pass", "issues": []},
        ])

    def test_fields_must_be_nonblank_strings(self):
        for field in FIELDS:
            for value in [None, "", " \t", 1, True, []]:
                with self.subTest(field=field, value=value):
                    scenario = {**RECOVERY, field: value}
                    self.assertEqual(check_scenario(scenario)["status"], "fail")
        self.assertEqual(check_scenario({}), {
            "status": "fail", "issues": ["missing or invalid: " + field
                                         for field in FIELDS],
        })
        for value in [None, [], "record"]:
            self.assertEqual(check_scenario(value)["status"], "fail")

    def test_unrelated_and_unknown_pairs_request_review(self):
        for change in [{"control": "preserve_header_fields"},
                       {"threat": "unknown"}, {"control": "unknown"}]:
            with self.subTest(change=change):
                self.assertEqual(check_scenario({**RECOVERY, **change}), {
                    "status": "review", "issues": ["unlisted threat/control pair"],
                })

    def test_minimal_text_pass_is_not_an_explanation_judgment(self):
        self.assertEqual(check_scenario({"asset": "x", "threat": "malformed_structured_rows",
                                         "control": "validate_required_columns",
                                         "residual_risk": "x"}),
                         {"status": "pass", "issues": []})

    def test_inputs_and_fixture_are_not_mutated(self):
        before = deepcopy(SCENARIOS)
        check_scenario(SCENARIOS[0])
        fixture("missing-asset")
        fixture("unrelated-control")
        self.assertEqual(SCENARIOS, before)


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run([sys.executable, str(LAB / "example.py"), *args],
                              cwd=ROOT, capture_output=True, text=True, check=False)

    def test_documented_invalid_then_valid_sequence_recovers(self):
        readme = (LAB / "README.md").read_text()

        def block(name, language):
            match = re.search(r"<!-- " + name + r" -->\s*```" + language
                              + r"\n(.*?)\n```", readme, re.S)
            self.assertIsNotNone(match, "Missing documented block: " + name)
            return match.group(1)

        command = shlex.split(block("recovery-command", "bash"))
        self.assertEqual(command[:3], ["python3", str((LAB / "example.py").relative_to(ROOT)),
                                       "--sequence"])
        self.assertEqual(len(command), 4)
        expected_input = [INVALID, RECOVERY]
        self.assertEqual(json.loads(command[3]), expected_input)
        expected_stdout = block("recovery-output", "json") + "\n"
        self.assertEqual(json.loads(expected_stdout), {"results": [
            {"status": "fail", "issues": ["missing or invalid: asset"]},
            {"status": "pass", "issues": []},
        ]})
        result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                text=True, check=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout, expected_stdout)
        self.assertEqual(result.stderr, "")

    def test_fresh_process_normal_boundary_and_failure_cases(self):
        for case, code, statuses in [
            ("complete", 0, ["pass", "pass", "pass"]),
            ("missing-asset", 1, ["fail", "pass", "pass"]),
            ("unrelated-control", 3, ["review", "pass", "pass"]),
        ]:
            with self.subTest(case=case):
                result = self.run_example("--case", case)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual([item["status"] for item in
                                  json.loads(result.stdout)["results"]], statuses)

    def test_empty_sequence_and_malformed_input_in_fresh_processes(self):
        result = self.run_example("--sequence", "[]")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {"results": []})
        for args in [["--sequence", "{}"], ["--sequence", "["],
                     ["--scenario", "{"]]:
            with self.subTest(args=args):
                result = self.run_example(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
