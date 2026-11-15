"""Unit tests for R39-T003 training-only mean imputation lab."""

import unittest

from example import (
    EXPECTED_RESULTS_TABLE,
    TrainingOnlyMeanImputer,
    compare_approaches,
    independent_reference_impute,
)


class TestTrainingOnlyMeanImputer(unittest.TestCase):
    def test_primary_fixture_prevents_validation_leakage(self) -> None:
        imputer = TrainingOnlyMeanImputer().fit([2, None, 4])
        self.assertEqual(imputer.fill_value_, 3.0)

        transformed = imputer.transform([100, None])
        self.assertEqual(transformed, [100.0, 3.0])
        # Deliberately verify it does NOT refit on validation data ([100, 100]).
        self.assertNotEqual(transformed, [100.0, 100.0])

    def test_boundary_cases(self) -> None:
        # Single non-missing training value
        imputer = TrainingOnlyMeanImputer().fit([None, 5, None])
        self.assertEqual(imputer.fill_value_, 5.0)
        self.assertEqual(imputer.transform([None, 12]), [5.0, 12.0])

        # All-missing validation input is valid once fitted
        fitted = TrainingOnlyMeanImputer().fit([2, None, 4])
        self.assertEqual(fitted.transform([None, None]), [3.0, 3.0])

        # No-missing validation input passes through unchanged
        self.assertEqual(fitted.transform([10, 20]), [10.0, 20.0])

    def test_failure_cases_reject_all_missing_and_unfitted(self) -> None:
        with self.assertRaises(ValueError):
            TrainingOnlyMeanImputer().fit([None, None])

        with self.assertRaises(ValueError):
            TrainingOnlyMeanImputer().fit([])

        with self.assertRaises(RuntimeError):
            TrainingOnlyMeanImputer().transform([100, None])

        with self.assertRaises(ValueError):
            independent_reference_impute([None, None], [100, None])

    def test_compare_direct_against_independent_and_table(self) -> None:
        rows = compare_approaches(EXPECTED_RESULTS_TABLE)
        self.assertEqual(len(rows), len(EXPECTED_RESULTS_TABLE))
        for row in rows:
            self.assertTrue(row["all_match"], msg=f"Mismatch in case {row['case']}")


if __name__ == "__main__":
    unittest.main()
