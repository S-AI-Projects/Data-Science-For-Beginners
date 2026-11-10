"""
Tests for Training-Only Mean Imputation with State Tracing (R39-T024)
"""

import unittest
from example import MeanImputer


class TestMeanImputer(unittest.TestCase):
    def test_training_fit_and_validation_transform(self):
        """Training [2,None,4] yields mean 3; validation [100,None] becomes [100,3], not [100,100]."""
        train = [2, None, 4]
        val = [100, None]

        imputer = MeanImputer()
        imputer.fit(train)
        self.assertEqual(imputer.mean_, 3.0)

        imputed_val = imputer.transform(val)
        self.assertEqual(imputed_val, [100, 3.0])

    def test_all_missing_training_rejected(self):
        """All-missing training input is rejected with ValueError."""
        imputer = MeanImputer()
        with self.assertRaises(ValueError):
            imputer.fit([None, None, None])

    def test_state_trace_and_invariance(self):
        """Record intermediate state after each step and verify invariant linking state to final output."""
        imputer = MeanImputer()
        imputer.fit([2, None, 4])
        self.assertEqual(len(imputer.state_trace), 1)
        self.assertEqual(imputer.state_trace[0]["step"], "fit")
        self.assertEqual(imputer.state_trace[0]["stored_mean"], 3.0)

        imputer.transform([100, None])
        self.assertEqual(len(imputer.state_trace), 2)
        self.assertEqual(imputer.state_trace[1]["step"], "transform")
        self.assertEqual(imputer.state_trace[1]["applied_mean"], 3.0)
        self.assertEqual(imputer.state_trace[1]["imputed_count"], 1)

    def test_transform_before_fit_raises(self):
        """Calling transform before fitting must raise RuntimeError."""
        imputer = MeanImputer()
        with self.assertRaises(RuntimeError):
            imputer.transform([1, None])

    def test_deliberate_wrong_result_fails(self):
        """A data-leakage result (refitting on validation to give [100, 100]) must fail assertion."""
        imputer = MeanImputer()
        imputer.fit([2, None, 4])
        val = [100, None]
        imputed_val = imputer.transform(val)
        self.assertNotEqual(imputed_val, [100, 100], "Validation data must not be imputed with validation mean.")


if __name__ == "__main__":
    unittest.main()
