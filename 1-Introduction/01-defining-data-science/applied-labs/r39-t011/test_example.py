"""Tests for example.py. Run from the repository root:

python3 -m unittest discover -s 1-Introduction/01-defining-data-science/applied-labs/r39-t011 -p "test_*.py"
"""
import contextlib
import io
import unittest

import example
from example import FAIL, PASS, REVIEW, check_scenario


class NormalCases(unittest.TestCase):
    def test_each_complete_scenario_passes(self):
        for scenario in example.SCENARIOS:
            with self.subTest(scenario["id"]):
                self.assertEqual(check_scenario(scenario), (PASS, []))

    def test_three_scenarios_cover_three_lesson_sections(self):
        sections = {s["lesson_section"] for s in example.SCENARIOS}
        self.assertEqual(len(example.SCENARIOS), 3)
        self.assertEqual(len(sections), 3)
        self.assertTrue(sections <= example.LESSON_SECTIONS)


class FailureCases(unittest.TestCase):
    def test_scenario_without_asset_fails(self):
        result = check_scenario(example.NO_ASSET)
        self.assertEqual(result.status, FAIL)
        self.assertEqual(result.reasons, ["missing:asset"])

    def test_control_unrelated_to_threat_is_flagged_for_review(self):
        result = check_scenario(example.UNRELATED_CONTROL)
        self.assertEqual(result.status, REVIEW)
        self.assertEqual(result.reasons, ["control_unrelated_to_threat"])


class BoundaryCases(unittest.TestCase):
    def test_whitespace_only_asset_counts_as_missing(self):
        s = dict(example.SCENARIOS[0], asset="   ")
        self.assertEqual(check_scenario(s).reasons, ["missing:asset"])

    def test_absent_key_counts_as_missing(self):
        s = dict(example.SCENARIOS[0])
        del s["asset"]
        self.assertEqual(check_scenario(s).reasons, ["missing:asset"])

    def test_residual_risk_claiming_none_fails(self):
        s = dict(example.SCENARIOS[0], residual_risk="None")
        self.assertEqual(check_scenario(s),
                         (FAIL, ["residual_risk_claims_none"]))

    def test_unknown_lesson_section_fails(self):
        s = dict(example.SCENARIOS[0], lesson_section="Quantum Pizza")
        self.assertEqual(check_scenario(s),
                         (FAIL, ["unknown_lesson_section"]))

    def test_non_dict_input_fails(self):
        self.assertEqual(check_scenario("not a scenario"),
                         (FAIL, ["not_a_scenario"]))

    def test_fail_takes_priority_over_review(self):
        s = dict(example.UNRELATED_CONTROL, asset="")
        self.assertEqual(check_scenario(s).status, FAIL)


class LimitsOfAutomatedGrading(unittest.TestCase):
    def test_structurally_complete_nonsense_still_passes(self):
        # The checker cannot judge meaning: a human reviewer must.
        s = dict(example.SCENARIOS[0], asset="banana", threat="blue",
                 control="tuesday", residual_risk="maybe")
        self.assertEqual(check_scenario(s), (PASS, []))


class CommandLineOutput(unittest.TestCase):
    def test_run_prints_expected_table(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            example.run()
        lines = buf.getvalue().splitlines()
        self.assertEqual(len(lines), 5)
        self.assertEqual([l.split()[1] for l in lines],
                         ["PASS", "PASS", "PASS", "FAIL", "REVIEW"])


if __name__ == "__main__":
    unittest.main()