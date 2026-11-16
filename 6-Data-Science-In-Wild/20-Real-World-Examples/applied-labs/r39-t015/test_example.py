"""Check the structural rubric, callable seam and offline CLI cases."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import FIELDS, SCENARIOS, check_scenario, fixture, local_relation


class RubricTests(unittest.TestCase):
    def test_complete_fictional_scenarios_pass(self):
        self.assertEqual(len(SCENARIOS), 3)
        for scenario in fixture():
            with self.subTest(section=scenario["section"]):
                self.assertEqual(check_scenario(scenario),
                                 {"status": "pass", "issues": []})

    def test_missing_asset_fails_before_adapter_call(self):
        def unexpected_call(threat, control):
            self.fail("incomplete scenarios must not reach the adapter")

        self.assertEqual(check_scenario(fixture("missing-asset")[0], unexpected_call),
                         {"status": "fail", "issues": ["missing or invalid: asset"]})

    def test_every_required_field_is_nonblank_text(self):
        for field in FIELDS:
            for value in [None, "", " \t", 0, [], True]:
                with self.subTest(field=field, value=value):
                    scenario = deepcopy(SCENARIOS[0])
                    scenario[field] = value
                    self.assertEqual(check_scenario(scenario)["status"], "fail")
        self.assertEqual(check_scenario({})["status"], "fail")
        for value in [None, [], "scenario"]:
            self.assertEqual(check_scenario(value)["status"], "fail")

    def test_minimal_complete_and_unrelated_control(self):
        minimal = {"asset": "x", "threat": "data_loss", "control": "backups",
                   "residual_risk": "x"}
        self.assertEqual(check_scenario(minimal)["status"], "pass")
        # A structural pass cannot establish that "x" is a good explanation.
        self.assertEqual(check_scenario(fixture("unrelated-control")[0]),
                         {"status": "review",
                          "issues": ["threat/control pair not listed"]})

    def test_exact_local_mapping_and_unknown_labels(self):
        pairs = [("unauthorized_access", "access_review"),
                 ("data_loss", "backups"),
                 ("tampered_readings", "integrity_checks")]
        for threat, control in pairs:
            self.assertIs(local_relation(threat, control), True)
        self.assertIs(local_relation("unauthorized_access", "backups"), False)
        self.assertIsNone(local_relation("Data_loss", "backups"))
        self.assertIsNone(local_relation("data_loss", "restore copies"))

    def test_callable_receives_exact_inputs_and_response_is_used(self):
        calls = []

        def adapter(threat, control):
            calls.append((threat, control))
            return False

        self.assertEqual(check_scenario(SCENARIOS[0], adapter)["status"], "review")
        self.assertEqual(calls, [("unauthorized_access", "access_review")])
        for response in [None, "true", 1, {}, []]:
            with self.subTest(response=response):
                self.assertEqual(check_scenario(
                    SCENARIOS[0], lambda threat, control: response
                )["status"], "review")

    def test_unavailable_adapter_requests_review(self):
        def unavailable(threat, control):
            raise TimeoutError("fictional timeout; no network request")

        self.assertEqual(check_scenario(SCENARIOS[0], unavailable),
                         {"status": "review", "issues": ["relation adapter unavailable"]})

    def test_fixture_and_inputs_are_not_mutated(self):
        before = deepcopy(SCENARIOS)
        check_scenario(SCENARIOS[0])
        fixture("missing-asset")
        fixture("unrelated-control")
        self.assertEqual(SCENARIOS, before)


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py")), *args],
            capture_output=True, text=True, check=False,
        )

    def test_fixture_cases_in_fresh_processes(self):
        for case, expected_exit, statuses in [
            ("complete", 0, ["pass", "pass", "pass"]),
            ("missing-asset", 1, ["fail", "pass", "pass"]),
            ("unrelated-control", 3, ["review", "pass", "pass"]),
        ]:
            with self.subTest(case=case):
                actual = self.run_example("--case", case)
                self.assertEqual(actual.returncode, expected_exit, actual.stderr)
                report = json.loads(actual.stdout)
                self.assertEqual(report["adapter"], "deterministic-local-mock")
                self.assertEqual([item["status"] for item in report["results"]],
                                 statuses)
                self.assertEqual(actual.stderr, "")

    def test_custom_boundaries_and_invalid_json_in_fresh_processes(self):
        for scenario, status, code in [({}, "fail", 1), (None, "fail", 1),
                                      (SCENARIOS[0], "pass", 0),
                                      ({**SCENARIOS[0], "threat": "unknown"},
                                       "review", 3)]:
            with self.subTest(scenario=scenario):
                result = self.run_example("--scenario", json.dumps(scenario))
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(json.loads(result.stdout)["results"][0]["status"],
                                 status)
        invalid = self.run_example("--scenario", "{")
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(invalid.stdout, "")
        self.assertIn("error:", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
