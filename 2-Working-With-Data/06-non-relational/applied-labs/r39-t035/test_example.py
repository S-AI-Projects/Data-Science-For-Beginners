import unittest

from example import (
    FIXTURE_DOCUMENTS,
    LocalDocumentStore,
    run_query,
    validate_person_document,
)


class DocumentStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = LocalDocumentStore(FIXTURE_DOCUMENTS)

    def test_normal_scenario_filters_and_orders_documents(self) -> None:
        """Querying with max_age=40 returns persons under 40 ordered by firstname."""
        results = run_query(self.store, max_age=40)
        self.assertEqual(len(results), 2)
        # Expected ordered by firstname: Christophe (32), then Prema (20)
        self.assertEqual(results[0]["firstname"], "Christophe")
        self.assertEqual(results[0]["age"], 32)
        self.assertEqual(results[1]["firstname"], "Prema")
        self.assertEqual(results[1]["age"], 20)

    def test_boundary_scenario_empty_results_when_no_match(self) -> None:
        """Querying with max_age=15 returns empty list when all ages >= 15."""
        results = run_query(self.store, max_age=15)
        self.assertEqual(results, [])

    def test_boundary_scenario_all_documents_match(self) -> None:
        """Querying with max_age=100 returns all 4 documents ordered by firstname."""
        results = run_query(self.store, max_age=100)
        self.assertEqual(len(results), 4)
        names = [doc["firstname"] for doc in results]
        self.assertEqual(names, ["Christophe", "Eva", "Keisha", "Prema"])

    def test_failure_scenario_invalid_parameter_type(self) -> None:
        """Passing an invalid parameter type (e.g. negative or non-integer) raises ValueError."""
        with self.assertRaises(ValueError):
            run_query(self.store, max_age=-1)

        with self.assertRaises(ValueError):
            run_query(self.store, max_age="invalid")  # type: ignore

    def test_failure_scenario_missing_parameter(self) -> None:
        """Invoking the client without the required max_age parameter raises ValueError."""
        with self.assertRaises(ValueError):
            self.store("SELECT * FROM c WHERE c.age < @max_age", parameters={})

    def test_failure_scenario_invalid_schema_insertion(self) -> None:
        """Attempting to insert a document missing required fields or invalid types raises error."""
        # Non-dict document
        with self.assertRaises(TypeError):
            validate_person_document("not-a-dict")

        # Missing firstname
        with self.assertRaises(ValueError):
            validate_person_document({"age": 25, "id": "1"})

        # Invalid age
        with self.assertRaises(ValueError):
            validate_person_document({"firstname": "Alice", "age": -5, "id": "1"})

        # Missing id
        with self.assertRaises(ValueError):
            validate_person_document({"firstname": "Alice", "age": 25})


if __name__ == "__main__":
    unittest.main()
