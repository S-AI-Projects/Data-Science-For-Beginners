import unittest

from example import MedianImputer, run_example


class MedianImputerTests(unittest.TestCase):
    def test_fit_training_data_then_transform_train_and_test(self):
        imputer = MedianImputer().fit([10.0, None, 30.0])

        self.assertEqual(imputer.median, 20.0)
        self.assertEqual(imputer.transform([10.0, None, 30.0]), [10.0, 20.0, 30.0])
        self.assertEqual(imputer.transform([None, 100.0]), [20.0, 100.0])
        self.assertEqual(imputer.median, 20.0)

    def test_fit_rejects_all_missing_values(self):
        with self.assertRaises(ValueError):
            MedianImputer().fit([None, None])

    def test_transform_requires_fit(self):
        with self.assertRaises(ValueError):
            MedianImputer().transform([None])

    def test_recorded_steps_end_in_final_output(self):
        steps, final_output = run_example()

        self.assertEqual(
            [step["name"] for step in steps],
            ["inputs", "fit", "transform_training", "transform_test"],
        )
        self.assertEqual(steps[1]["state"]["training_median"], 20.0)
        self.assertEqual(
            steps[-1]["state"]["values"],
            final_output,
        )
        self.assertEqual(final_output, [20.0, 100.0])


if __name__ == "__main__":
    unittest.main()
