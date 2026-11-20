"""Unit tests for R39-T042 training-only mean imputation boundary cases."""

import unittest
from example import TrainingMeanImputer


class TestTrainingMeanImputer(unittest.TestCase):
    def test_stated_contract_training_and_validation(self) -> None:
        # Training [2,None,4] yields mean 3; validation [100,None] becomes [100,3], not [100,100]
        imputer = TrainingMeanImputer()
        result = imputer.fit_transform([2, None, 4], [100, None])
        self.assertEqual(result["training_mean"], 3.0)
        self.assertEqual(result["validation"], [100.0, 3.0])

    def test_smallest_valid_training_input(self) -> None:
        # Smallest valid case: single observed value
        imputer = TrainingMeanImputer()
        result = imputer.fit_transform([5], [None])
        self.assertEqual(result["training_mean"], 5.0)
        self.assertEqual(result["validation"], [5.0])

    def test_boundary_empty_and_all_missing_validation(self) -> None:
        imputer = TrainingMeanImputer()
        imputer.fit([2, None, 4])
        # Empty validation
        self.assertEqual(imputer.transform([]), [])
        # All-missing validation
        self.assertEqual(imputer.transform([None, None]), [3.0, 3.0])

    def test_invalid_all_missing_training_rejected(self) -> None:
        imputer = TrainingMeanImputer()
        with self.assertRaises(ValueError):
            imputer.fit([None, None])
        with self.assertRaises(ValueError):
            imputer.fit([])

    def test_transform_before_fit_raises_runtime_error(self) -> None:
        imputer = TrainingMeanImputer()
        with self.assertRaises(RuntimeError):
            imputer.transform([1, None])

    def test_deliberate_validation_refit_fails(self) -> None:
        # Simulates leakage where validation is refitted yielding [100, 100] instead of [100, 3]
        imputer = TrainingMeanImputer()
        result = imputer.fit_transform([2, None, 4], [100, None])
        with self.assertRaises(AssertionError):
            self.assertEqual(result["validation"], [100.0, 100.0])


if __name__ == "__main__":
    unittest.main()
