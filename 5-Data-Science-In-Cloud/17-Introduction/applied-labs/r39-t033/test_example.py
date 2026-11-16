import unittest

from example import SCENARIOS, check_scenario


class ScenarioRubricTests(unittest.TestCase):
    def test_checker_matches_explicit_expected_results(self):
        expected = {
            "Protecting live sentiment data": ("pass", ()),
            "Retaining research-paper results": ("fail", ("missing or empty asset",)),
            "Protecting a paper-analysis dashboard": (
                "review",
                ("control category is not listed for this threat; human review required",),
            ),
        }
        inputs = SCENARIOS
        actual = {}
        for scenario in inputs:
            result = check_scenario(scenario)
            actual[scenario["name"]] = (result.status, result.issues)

        self.assertEqual(actual, expected)

    def test_checker_does_not_pass_when_residual_risk_is_missing(self):
        complete_scenario = SCENARIOS[0].copy()
        complete_scenario["residual_risk"] = " "

        result = check_scenario(complete_scenario)

        self.assertEqual(result.status, "fail")
        self.assertIn("missing or empty residual_risk", result.issues)


if __name__ == "__main__":
    unittest.main()
