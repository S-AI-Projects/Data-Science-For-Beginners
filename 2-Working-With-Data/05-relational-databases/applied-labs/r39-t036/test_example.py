import sqlite3
import unittest

from example import (
    QueryBuilder,
    create_schema,
    populate_fixture,
    rainfall_for_year,
    rainfall_for_year_baseline,
)


class RainfallRelationalDatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        create_schema(self.connection)
        populate_fixture(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    # --- Normal Scenarios ---
    def test_normal_filter_by_year_and_order_asc(self) -> None:
        expected = [("Atlanta", 1111), ("Auckland", 942), ("Tokyo", 1874)]
        actual = rainfall_for_year(self.connection, 2019, order_desc=False)
        self.assertEqual(actual, expected)

    def test_normal_filter_by_year_and_order_desc(self) -> None:
        expected = [("Tokyo", 1874), ("Auckland", 942), ("Atlanta", 1111)]
        actual = rainfall_for_year(self.connection, 2019, order_desc=True)
        self.assertEqual(actual, expected)

    # --- Boundary Scenarios ---
    def test_boundary_no_matching_year(self) -> None:
        # Year 2018 exists in neither rainfall entry for our 2019/2020 fixture
        self.assertEqual(rainfall_for_year(self.connection, 2018), [])

    def test_boundary_single_match_year(self) -> None:
        # Year 2020 has exactly 1 record (Tokyo: 1690)
        self.assertEqual(rainfall_for_year(self.connection, 2020), [("Tokyo", 1690)])

    # --- Failure Scenarios ---
    def test_failure_negative_year(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            rainfall_for_year(self.connection, -1)
        self.assertIn("Year must be non-negative", str(ctx.exception))

    def test_failure_invalid_type_year(self) -> None:
        with self.assertRaises(TypeError) as ctx:
            rainfall_for_year(self.connection, "2019")  # type: ignore[arg-type]
        self.assertIn("Year must be an integer", str(ctx.exception))

        with self.assertRaises(TypeError) as ctx_bool:
            rainfall_for_year(self.connection, True)  # type: ignore[arg-type]
        self.assertIn("Year must be an integer", str(ctx_bool.exception))

    def test_failure_invalid_type_order_desc(self) -> None:
        with self.assertRaises(TypeError) as ctx:
            rainfall_for_year(self.connection, 2019, order_desc="yes")  # type: ignore[arg-type]
        self.assertIn("order_desc must be a boolean", str(ctx.exception))

    def test_failure_foreign_key_constraint_enforced(self) -> None:
        # Inserting a rainfall row referencing non-existent city_id 99 should fail
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO rainfall (rainfall_id, city_id, year, amount) "
                "VALUES (?, ?, ?, ?)",
                (10, 99, 2019, 500),
            )

    # --- Equivalence Proof: Baseline vs Refactored (Extracted Responsibility) ---
    def test_baseline_and_refactored_equivalence_on_fixture(self) -> None:
        test_cases = [
            (2019, False),
            (2019, True),
            (2020, False),
            (2020, True),
            (2018, False),
            (0, False),
        ]
        for year, order_desc in test_cases:
            baseline_result = rainfall_for_year_baseline(self.connection, year, order_desc=order_desc)
            refactored_result = rainfall_for_year(self.connection, year, order_desc=order_desc)
            self.assertEqual(
                refactored_result,
                baseline_result,
                "Mismatch between baseline and refactored for year={}, order_desc={}".format(
                    year, order_desc
                ),
            )

    def test_baseline_and_refactored_error_equivalence(self) -> None:
        error_cases = [
            (-5, False, ValueError),
            ("2019", False, TypeError),
            (True, False, TypeError),
            (2019, "invalid", TypeError),
        ]
        for year, order_desc, exc_type in error_cases:
            with self.assertRaises(exc_type):
                rainfall_for_year_baseline(self.connection, year, order_desc=order_desc)  # type: ignore[arg-type]
            with self.assertRaises(exc_type):
                rainfall_for_year(self.connection, year, order_desc=order_desc)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
