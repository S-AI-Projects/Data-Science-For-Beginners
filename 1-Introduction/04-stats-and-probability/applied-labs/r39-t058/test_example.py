"""Unit tests for Task R39-T058."""

import unittest
from example import count_histogram_bins, run_evaluation_experiment


class TestHistogramEvaluationExperiment(unittest.TestCase):
    def test_stated_contract_counts_and_out_of_range(self):
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        res = count_histogram_bins(values, bins)
        self.assertEqual(res["counts"], [2, 2])
        self.assertEqual(res["total_in_range"], 4)
        self.assertEqual(res["total_out_of_range"], 0)

    def test_values_outside_range_reported_separately(self):
        bins = [0, 10, 20]
        values = [-3, 0, 9, 10, 20, 30]
        res = count_histogram_bins(values, bins)
        self.assertEqual(res["counts"], [2, 2])
        self.assertEqual(res["below_range"], [-3])
        self.assertEqual(res["above_range"], [30])

    def test_evaluation_experiment_configurations(self):
        report = run_evaluation_experiment()
        self.assertIn("config_small", report)
        self.assertIn("config_medium", report)
        self.assertIn("config_multibin", report)

        for cfg_name, metrics in report.items():
            self.assertEqual(metrics["correctness_pct"], 100.0)
            self.assertGreater(metrics["input_size"], 0)

    def test_deliberate_wrong_result_fails(self):
        bins = [0, 10, 20]
        values = [0, 9, 10, 20]
        res = count_histogram_bins(values, bins)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["counts"], [4, 0])


if __name__ == "__main__":
    unittest.main()
