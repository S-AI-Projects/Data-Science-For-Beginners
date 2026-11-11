"""
Tests for SQLite Parameterized Queries (R39-T028)
"""

import sqlite3
import unittest
from example import create_items_db, evaluate_configurations, query_by_category_parameterized


class TestSQLiteParameterizedQueries(unittest.TestCase):
    def setUp(self):
        self.canonical_rows = [("tea", "drink"), ("rice", "food"), ("coffee", "drink")]
        self.conn = create_items_db(self.canonical_rows)

    def tearDown(self):
        self.conn.close()

    def test_canonical_query_ordering(self):
        """Rows (tea,drink),(rice,food),(coffee,drink): category drink returns coffee and tea in name order."""
        results = query_by_category_parameterized(self.conn, "drink")
        self.assertEqual(results, ["coffee", "tea"])

    def test_literal_quote_handling_and_injection_immunity(self):
        """A quote-containing category remains literal data and prevents SQL injection."""
        # Injection payload must not bypass filter or return all rows
        injection_attempt = "drink' OR '1'='1"
        res_injection = query_by_category_parameterized(self.conn, injection_attempt)
        self.assertEqual(res_injection, [])

        # Inserting a row with literal quotes
        cur = self.conn.cursor()
        cur.execute("INSERT INTO items (name, category) VALUES (?, ?)", ("soup", "chef's special"))
        self.conn.commit()

        # Querying with literal quote works cleanly without syntax error
        res_literal = query_by_category_parameterized(self.conn, "chef's special")
        self.assertEqual(res_literal, ["soup"])

    def test_configuration_benchmarks(self):
        """Compare three controlled configurations (3, 10, 25 rows) and verify metrics."""
        configs = evaluate_configurations()
        self.assertEqual(len(configs), 3)

        # Verify small config
        self.assertEqual(configs[0]["total_rows"], 3)
        self.assertEqual(configs[0]["drink_matches"], 2)

        # Verify medium config
        self.assertEqual(configs[1]["total_rows"], 10)
        self.assertEqual(configs[1]["drink_matches"], 6)

        # Verify scaled config
        self.assertEqual(configs[2]["total_rows"], 25)
        self.assertEqual(configs[2]["drink_matches"], 13)

        for cfg in configs:
            self.assertGreater(cfg["avg_latency_us"], 0.0)

    def test_deliberate_wrong_result_fails(self):
        """Deliberately assert that results are NOT returned in un-ordered insertion order."""
        results = query_by_category_parameterized(self.conn, "drink")
        self.assertNotEqual(results, ["tea", "coffee"], "Query results must be sorted alphabetically by name.")


if __name__ == "__main__":
    unittest.main()
