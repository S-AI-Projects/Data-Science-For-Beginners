import sqlite3
import unittest

from example import create_schema, rainfall_for_year


class RainfallQueryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        create_schema(self.connection)
        self.connection.executemany(
            "INSERT INTO cities (city_id, city, country) VALUES (?, ?, ?)",
            [
                (1, "Tokyo", "Japan"),
                (2, "Atlanta", "United States"),
                (3, "Auckland", "New Zealand"),
            ],
        )
        self.connection.executemany(
            "INSERT INTO rainfall (rainfall_id, city_id, year, amount) "
            "VALUES (?, ?, ?, ?)",
            [
                (1, 1, 2019, 1874),
                (2, 2, 2019, 1111),
                (3, 3, 2019, 942),
                (4, 1, 2020, 1690),
            ],
        )

    def tearDown(self) -> None:
        self.connection.close()

    def test_filters_by_year_and_orders_by_city(self) -> None:
        self.assertEqual(
            rainfall_for_year(self.connection, 2019),
            [("Atlanta", 1111), ("Auckland", 942), ("Tokyo", 1874)],
        )

    def test_returns_empty_list_when_year_has_no_rows(self) -> None:
        self.assertEqual(rainfall_for_year(self.connection, 2018), [])

    def test_rainfall_requires_an_existing_city(self) -> None:
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO rainfall (rainfall_id, city_id, year, amount) "
                "VALUES (?, ?, ?, ?)",
                (5, 99, 2019, 500),
            )


if __name__ == "__main__":
    unittest.main()
