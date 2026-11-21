"""Unit tests for Task R39-T053."""

import unittest
from example import (
    calculate_group_metric,
    compare_two_groups,
    verify_both_approaches,
)


class TestGroupMetricComparison(unittest.TestCase):
    def test_group_a_and_group_b_rates_and_counts(self):
        group_a = [1, 0]
        group_b = [1, 1, 0, 0]
        res = compare_two_groups(group_a, group_b)

        self.assertEqual(res["group_a"]["rate"], 0.5)
        self.assertEqual(res["group_a"]["n"], 2)

        self.assertEqual(res["group_b"]["rate"], 0.5)
        self.assertEqual(res["group_b"]["n"], 4)

        self.assertFalse(res["causation_inferred"])

    def test_empty_group_is_undefined(self):
        empty_res = calculate_group_metric([])
        self.assertIsNone(empty_res["rate"])
        self.assertEqual(empty_res["n"], 0)
        self.assertFalse(empty_res["defined"])

    def test_compare_two_approaches(self):
        group_a = [1, 0]
        group_b = [1, 1, 0, 0]
        self.assertTrue(verify_both_approaches(group_a))
        self.assertTrue(verify_both_approaches(group_b))
        self.assertTrue(verify_both_approaches([]))

    def test_deliberate_wrong_result_fails(self):
        group_a = [1, 0]
        res = calculate_group_metric(group_a)
        with self.assertRaises(AssertionError):
            self.assertEqual(res["rate"], 0.99)


if __name__ == "__main__":
    unittest.main()
