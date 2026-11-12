import unittest

from example import (
    aggregate_yearly_production,
    boundary_fixture,
    invalid_fixture,
    local_fixture,
    minimal_valid_fixture,
)


class YearlyHoneyProductionTests(unittest.TestCase):
    def test_fixture_groups_states_into_yearly_production_totals(self):
        result = aggregate_yearly_production(local_fixture())

        self.assertEqual(result["labels"], [1998, 1999])
        self.assertEqual(result["values"], [30, 5])

    def test_smallest_valid_input_produces_one_aligned_label_value_pair(self):
        result = aggregate_yearly_production(minimal_valid_fixture())

        self.assertEqual(list(zip(result["labels"], result["values"])), [(1998, 10)])

    def test_empty_input_boundary_returns_empty_chart_series(self):
        self.assertEqual(aggregate_yearly_production([]), {"labels": [], "values": []})

    def test_zero_production_boundary_is_included_in_the_year_total(self):
        self.assertEqual(
            aggregate_yearly_production(boundary_fixture()),
            {"labels": [1998], "values": [0]},
        )

    def test_missing_required_field_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "missing required field 'totalprod'"):
            aggregate_yearly_production(invalid_fixture())

    def test_non_integer_total_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "non-integer totalprod"):
            aggregate_yearly_production(
                [{"state": "AL", "year": 1998, "totalprod": 1.5}]
            )


if __name__ == "__main__":
    unittest.main()
