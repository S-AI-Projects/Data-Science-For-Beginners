import unittest

from example import annual_production_totals


class AnnualProductionTotalsTests(unittest.TestCase):
    def test_sums_rows_by_year_and_keeps_years_aligned_with_totals(self):
        records = [
            ("CA", 2019, 12),
            ("ND", 2019, 8),
            ("CA", 2018, 10),
            ("SD", 2019, 5),
            ("ND", 2018, 4),
        ]

        self.assertEqual(
            [(2018, 14), (2019, 25)],
            annual_production_totals(records),
        )

    def test_smallest_valid_fixture_keeps_zero_total_for_observed_year(self):
        self.assertEqual([(2019, 0)], annual_production_totals([("CA", 2019, 0)]))

    def test_empty_fixture_has_no_observed_years_and_returns_no_totals(self):
        self.assertEqual([], annual_production_totals([]))

    def test_malformed_record_raises_value_error(self):
        with self.assertRaises(ValueError):
            annual_production_totals([("CA", 2019)])

    def test_negative_production_raises_value_error(self):
        with self.assertRaises(ValueError):
            annual_production_totals([("CA", 2019, -1)])


if __name__ == "__main__":
    unittest.main()
