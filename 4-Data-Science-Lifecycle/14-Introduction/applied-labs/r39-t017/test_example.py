"""Literal rubric expectations and execution of the exact documented example."""

from copy import deepcopy
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import unittest

from example import FIELDS, SCENARIOS, check_scenario, fixture


LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[3]
WORKED_INPUT = {
    "asset": "Fictional community survey dataset",
    "threat": "departed_account_access",
    "control": "revoke_departed_access",
    "residual_risk": "Previously downloaded copies may still exist.",
}


class RubricTests(unittest.TestCase):
    def test_three_complete_scenarios_pass(self):
        self.assertEqual(len(SCENARIOS), 3)
        for scenario in fixture():
            with self.subTest(scenario=scenario["id"]):
                self.assertEqual(scenario["section"], "Maintaining / Securing the Data")
                self.assertEqual(check_scenario(scenario),
                                 {"status": "pass", "issues": []})

    def test_missing_asset_fails(self):
        self.assertEqual(check_scenario(fixture("missing-asset")[0]),
                         {"status": "fail", "issues": ["missing or invalid: asset"]})

    def test_required_fields_are_nonblank_strings(self):
        for field in FIELDS:
            for value in [None, "", " \t", 0, True, []]:
                with self.subTest(field=field, value=value):
                    scenario = {**WORKED_INPUT, field: value}
                    self.assertEqual(check_scenario(scenario)["status"], "fail")
        self.assertEqual(check_scenario({}), {
            "status": "fail", "issues": ["missing or invalid: " + field
                                         for field in FIELDS],
        })
        for value in [None, "scenario", []]:
            self.assertEqual(check_scenario(value),
                             {"status": "fail", "issues": ["scenario must be an object"]})

    def test_unrelated_or_unknown_pair_needs_review(self):
        for changes in [{"control": "encrypt_storage"}, {"threat": "unknown"},
                        {"control": "unknown"}, {"threat": "Departed_account_access"}]:
            with self.subTest(changes=changes):
                self.assertEqual(check_scenario({**WORKED_INPUT, **changes}), {
                    "status": "review", "issues": ["unlisted threat/control pair"],
                })

    def test_minimal_text_does_not_mean_good_explanation(self):
        scenario = {**WORKED_INPUT, "asset": "x", "residual_risk": "x"}
        self.assertEqual(check_scenario(scenario), {"status": "pass", "issues": []})

    def test_input_and_fixture_are_not_changed(self):
        before = deepcopy(SCENARIOS)
        check_scenario(SCENARIOS[0])
        fixture("missing-asset")
        fixture("unrelated-control")
        self.assertEqual(SCENARIOS, before)


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run([sys.executable, str(LAB / "example.py"), *args],
                              cwd=ROOT, capture_output=True, text=True, check=False)

    def test_exact_readme_worked_example_is_a_regression(self):
        readme = (LAB / "README.md").read_text()

        def block(name, language):
            pattern = r"<!-- " + name + r" -->\s*```" + language + r"\n(.*?)\n```"
            match = re.search(pattern, readme, re.S)
            self.assertIsNotNone(match, "Missing worked-example block: " + name)
            return match.group(1)

        documented_input = json.loads(block("worked-input", "json"))
        self.assertEqual(documented_input, WORKED_INPUT)
        command = shlex.split(block("worked-command", "bash"))
        self.assertEqual(command[:3], ["python3", str((LAB / "example.py").relative_to(ROOT)),
                                       "--scenario"])
        self.assertEqual(len(command), 4)
        self.assertEqual(json.loads(command[3]), WORKED_INPUT)
        expected_stdout = block("worked-output", "json") + "\n"
        self.assertEqual(json.loads(expected_stdout),
                         {"results": [{"status": "pass", "issues": []}]})
        # Execute the published argv directly, including python3; no shell rewrite.
        actual = subprocess.run(command, cwd=ROOT, capture_output=True,
                                text=True, check=False)
        self.assertEqual(actual.returncode, 0, actual.stderr)
        self.assertEqual(actual.stdout, expected_stdout)
        self.assertEqual(actual.stderr, "")

    def test_fixture_cases_in_fresh_processes(self):
        for case, code, statuses in [
            ("complete", 0, ["pass", "pass", "pass"]),
            ("missing-asset", 1, ["fail", "pass", "pass"]),
            ("unrelated-control", 3, ["review", "pass", "pass"]),
        ]:
            with self.subTest(case=case):
                result = self.run_example("--case", case)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual([item["status"] for item in json.loads(result.stdout)["results"]],
                                 statuses)

    def test_boundaries_and_invalid_json_in_fresh_processes(self):
        for scenario, status, code in [({}, "fail", 1), (None, "fail", 1),
                                      ({**WORKED_INPUT, "asset": "x",
                                        "residual_risk": "x"}, "pass", 0)]:
            with self.subTest(scenario=scenario):
                result = self.run_example("--scenario", json.dumps(scenario))
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(json.loads(result.stdout)["results"][0]["status"], status)
        result = self.run_example("--scenario", "{")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
