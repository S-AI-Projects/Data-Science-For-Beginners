"""Unit tests for the R39-T002 training-only mean imputation fixture."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from example import TrainingOnlyMeanImputer, run_fixture  # noqa: E402


class TestTrainingOnlyMeanImputer(unittest.TestCase):
    def test_training_only_mean_prevents_validation_leakage(self) -> None:
        imputer = TrainingOnlyMeanImputer()
        train_imputed = imputer.fit_transform([2, None, 4])
        val_imputed = imputer.transform([100, None])

        self.assertEqual(imputer.fitted_mean_, 3.0)
        self.assertEqual(train_imputed, [2.0, 3.0, 4.0])
        self.assertEqual(val_imputed, [100.0, 3.0])
        self.assertNotEqual(val_imputed, [100.0, 100.0])

    def test_boundary_single_observed_training_and_all_missing_validation(self) -> None:
        imputer = TrainingOnlyMeanImputer().fit([None, 5, None])

        self.assertEqual(imputer.fitted_mean_, 5.0)
        self.assertEqual(imputer.transform([None, None]), [5.0, 5.0])
        self.assertEqual(imputer.transform([]), [])

    def test_boundary_no_missing_values_preserves_inputs(self) -> None:
        imputer = TrainingOnlyMeanImputer().fit([1, 3])

        self.assertEqual(imputer.fitted_mean_, 2.0)
        self.assertEqual(imputer.transform([10, 20]), [10.0, 20.0])

    def test_invalid_all_missing_and_empty_training_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TrainingOnlyMeanImputer().fit([None, None])

        with self.assertRaises(ValueError):
            TrainingOnlyMeanImputer().fit([])

    def test_transform_before_fit_rejected(self) -> None:
        with self.assertRaises(RuntimeError):
            TrainingOnlyMeanImputer().transform([1, None])

    def test_run_fixture_contract(self) -> None:
        summary = run_fixture()

        self.assertTrue(summary["simulation"])
        self.assertEqual(summary["fitted_mean"], 3.0)
        self.assertEqual(summary["validation_imputed"], [100.0, 3.0])
        self.assertTrue(summary["all_missing_rejected"])


if __name__ == "__main__":
    unittest.main()
