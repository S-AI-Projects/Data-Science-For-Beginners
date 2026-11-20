"""Unit tests for R39-T048 parameterized SQLite queries, failure, and recovery."""

import unittest
from example import ItemsDatabase


class TestParameterizedQuery(unittest.TestCase):
    def setUp(self) -> None:
        self.db = ItemsDatabase()
        # Seed stated rows: (tea,drink),(rice,food),(coffee,drink)
        self.db.seed([("tea", "drink"), ("rice", "food"), ("coffee", "drink")])

    def tearDown(self) -> None:
        self.db.close()

    def test_query_category_drink_returns_coffee_and_tea_in_name_order(self) -> None:
        results = self.db.query_by_category("drink")
        self.assertEqual(results, ["coffee", "tea"])

    def test_quote_containing_category_remains_literal_data(self) -> None:
        # SQL injection attempt remains a literal string lookup and matches nothing
        results = self.db.query_by_category("drink' OR '1'='1")
        self.assertEqual(results, [])

        # Literal single quote in category works if matched literally
        self.db.seed([("boba", "special'drink")])
        self.assertEqual(self.db.query_by_category("special'drink"), ["boba"])

    def test_failure_and_recovery_flow(self) -> None:
        # Invalid input fails with documented ValueError
        with self.assertRaises(ValueError) as ctx:
            self.db.query_by_category("")
        self.assertIn("Invalid category parameter", str(ctx.exception))

        with self.assertRaises(ValueError):
            self.db.query_by_category(None)

        # Immediate recovery on next valid query
        recovered = self.db.query_by_category("food")
        self.assertEqual(recovered, ["rice"])

    def test_deliberate_wrong_order_fails(self) -> None:
        results = self.db.query_by_category("drink")
        with self.assertRaises(AssertionError):
            self.assertEqual(results, ["tea", "coffee"])


if __name__ == "__main__":
    unittest.main()
