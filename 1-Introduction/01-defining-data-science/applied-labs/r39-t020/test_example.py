"""Execute rubric scenarios and verify each applied question's factual answer."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import (FIELDS, QUESTIONS, SCENARIOS, answer_question,
                     check_scenario, fixture)


LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[3]


class RubricTests(unittest.TestCase):
    def test_three_complete_scenarios_pass(self):
        self.assertEqual(len(SCENARIOS), 3)
        self.assertEqual([check_scenario(row)["status"] for row in fixture()],
                         ["pass", "pass", "pass"])

    def test_missing_asset_fails_with_reason(self):
        self.assertEqual(check_scenario(fixture("missing-asset")[0]), {
            "status": "fail", "issues": ["missing or invalid: asset"],
        })

    def test_all_required_fields_must_be_nonblank_strings(self):
        for field in FIELDS:
            for value in [None, "", " \t", 0, True, []]:
                with self.subTest(field=field, value=value):
                    self.assertEqual(check_scenario({**SCENARIOS[0], field: value})["status"],
                                     "fail")
        self.assertEqual(check_scenario({}), {
            "status": "fail", "issues": ["missing or invalid: " + name for name in FIELDS],
        })
        for scenario in [None, "scenario", []]:
            self.assertEqual(check_scenario(scenario)["status"], "fail")

    def test_unrelated_or_unknown_pair_is_review(self):
        for update in [{"control": "encrypt_archive"}, {"threat": "unknown"},
                       {"control": "unknown"}]:
            with self.subTest(update=update):
                self.assertEqual(check_scenario({**SCENARIOS[0], **update}), {
                    "status": "review", "issues": ["unlisted threat/control pair"],
                })

    def test_question_predicts_complete_scenario(self):
        result = answer_question("predict")
        self.assertEqual(result["answer"], {"status": "pass", "issues": []})
        self.assertIn("four fields", result["rationale"])
        self.assertEqual(result["scenario"] if "scenario" in result else
                         check_scenario(QUESTIONS["predict"]["scenario"]), result["answer"])

    def test_question_diagnoses_missing_asset(self):
        result = answer_question("diagnose")
        self.assertEqual(result["answer"], {
            "status": "fail", "issues": ["missing or invalid: asset"],
        })
        self.assertIn("asset names what is at risk", result["rationale"])
        self.assertEqual(check_scenario(QUESTIONS["diagnose"]["scenario"]), result["answer"])

    def test_question_chooses_review_at_unknown_pair_boundary(self):
        result = answer_question("boundary")
        self.assertEqual(result["answer"], {
            "status": "review", "issues": ["unlisted threat/control pair"],
        })
        self.assertIn("human review", result["rationale"])
        self.assertEqual(check_scenario(QUESTIONS["boundary"]["scenario"]), result["answer"])

    def test_question_identifier_errors(self):
        with self.assertRaisesRegex(ValueError, "unknown question"):
            answer_question("not-a-question")

    def test_fixture_copies_do_not_mutate_source(self):
        original = json.loads(json.dumps(SCENARIOS))
        fixture("missing-asset")
        fixture("unrelated-control")
        self.assertEqual(SCENARIOS, original)


class CommandTests(unittest.TestCase):
    def run_example(self, *args):
        return subprocess.run([sys.executable, str(LAB / "example.py"), *args],
                              cwd=ROOT, capture_output=True, text=True, check=False)

    def test_default_fixture_in_fresh_process(self):
        result = self.run_example()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"results": [
            {"status": "pass", "issues": []},
            {"status": "pass", "issues": []},
            {"status": "pass", "issues": []},
        ]})

    def test_failure_and_review_cases_in_fresh_processes(self):
        for case, expected_status, exit_code in [
            ("missing-asset", "fail", 1), ("unrelated-control", "review", 3),
        ]:
            with self.subTest(case=case):
                result = self.run_example("--case", case)
                self.assertEqual(result.returncode, exit_code, result.stderr)
                self.assertEqual(json.loads(result.stdout)["results"][0]["status"],
                                 expected_status)

    def test_all_questions_execute_in_fresh_processes(self):
        for question, status, exit_code in [("predict", "pass", 0),
                                            ("diagnose", "fail", 1),
                                            ("boundary", "review", 3)]:
            with self.subTest(question=question):
                result = self.run_example("--question", question)
                self.assertEqual(result.returncode, exit_code, result.stderr)
                self.assertEqual(json.loads(result.stdout)["results"][0]["status"], status)


if __name__ == "__main__":
    unittest.main()
