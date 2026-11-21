"""Unit tests for Task R39-T054."""

import unittest
from example import ItemDatabase, run_pipeline


class TestParameterizedQuery(unittest.TestCase):
    def test_drink_query_returns_ordered_names(self):
        db = ItemDatabase()
        db.setup_table()
        rows = [("tea", "drink"), ("rice", "food"), ("coffee", "drink")]
        db.insert_rows(rows)
        drinks = db.query_category("drink")
        self.assertEqual(drinks, ["coffee", "tea"])
        db.close()

    def test_state_trace_and_invariant(self):
        db = ItemDatabase()
        db.setup_table()
        rows = [("tea", "drink"), ("rice", "food"), ("coffee", "drink")]
        db.insert_rows(rows)
        drinks = db.query_category("drink")

        # Verify trace steps exist
        steps = [entry["step"] for entry in db.state_trace]
        self.assertEqual(steps, ["setup_table", "insert_rows", "query_category"])

        # Verify invariant links intermediate state to final output
        self.assertTrue(db.verify_invariant("drink", drinks))
        db.close()

    def test_quote_containing_category_remains_literal(self):
        db = ItemDatabase()
        db.setup_table()
        rows = [("tea", "drink"), ("rice", "food"), ("coffee", "drink")]
        db.insert_rows(rows)

        # SQL injection attempt should return empty list because it is treated literally
        injection_query = db.query_category("' OR '1'='1")
        self.assertEqual(injection_query, [])

        # Inserting a literal row with quotes and querying it
        db.insert_rows([("special_tea", "drink's")])
        quoted_results = db.query_category("drink's")
        self.assertEqual(quoted_results, ["special_tea"])
        db.close()

    def test_pipeline_integration(self):
        res = run_pipeline()
        self.assertEqual(res["drinks"], ["coffee", "tea"])
        self.assertTrue(res["invariant_passed"])
        self.assertEqual(res["quote_results"], [])

    def test_deliberate_wrong_result_fails(self):
        res = run_pipeline()
        with self.assertRaises(AssertionError):
            self.assertEqual(res["drinks"], ["tea", "coffee"])


if __name__ == "__main__":
    unittest.main()
