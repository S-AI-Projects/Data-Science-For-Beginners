"""Query non-relational document data with schema validation and ordering.

This module provides a local simulation of querying a document collection
(such as Azure Cosmos DB Persons container from Lesson 06), illustrating
schema definition, parameterized filtering, and result ordering without
external dependencies or live database instances.
"""

from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence


# Type alias for a document representing a person
PersonDocument = Dict[str, Any]


class DocumentStoreClient(Protocol):
    """Callable interface for querying documents from an external store."""

    def __call__(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[PersonDocument]:
        """Execute a parameterized query and return matching documents."""
        ...


def validate_person_document(doc: Any) -> PersonDocument:
    """Validate that a document satisfies the expected Person schema.

    Schema:
      - Must be a dictionary.
      - 'firstname': non-empty string.
      - 'age': non-negative integer.
      - 'id': non-empty string.
      - Metadata fields (e.g. '_rid', '_self', '_etag', '_attachments', '_ts')
        are accepted if present (illustrating NoSQL flexible document schema).

    Raises:
        TypeError: If doc is not a dictionary.
        ValueError: If required fields are missing or have invalid types/values.
    """
    if not isinstance(doc, dict):
        raise TypeError(f"Document must be a dict, got {type(doc).__name__}")

    if "firstname" not in doc or not isinstance(doc["firstname"], str) or not doc["firstname"].strip():
        raise ValueError("Document missing or invalid 'firstname': must be a non-empty string")

    if "age" not in doc or isinstance(doc["age"], bool) or not isinstance(doc["age"], int) or doc["age"] < 0:
        raise ValueError("Document missing or invalid 'age': must be a non-negative integer")

    if "id" not in doc or not isinstance(doc["id"], str) or not doc["id"].strip():
        raise ValueError("Document missing or invalid 'id': must be a non-empty string")

    return doc


class LocalDocumentStore:
    """Deterministic local in-memory adapter implementing DocumentStoreClient.

    Simulates the Cosmos DB query behavior for documents matching:
    SELECT * FROM c WHERE c.age < @max_age ORDER BY c.firstname ASC
    """

    def __init__(self, initial_documents: Optional[Sequence[PersonDocument]] = None) -> None:
        self._documents: List[PersonDocument] = []
        if initial_documents:
            for doc in initial_documents:
                self.insert_document(doc)

    def insert_document(self, doc: PersonDocument) -> None:
        """Validate and insert a document into the store."""
        validated = validate_person_document(doc)
        self._documents.append(dict(validated))

    def query_persons_under_age(
        self,
        max_age: int,
        order_by: str = "firstname",
        descending: bool = False,
    ) -> List[PersonDocument]:
        """Filter persons where age < max_age and order results.

        Parameters:
            max_age: Upper bound on age (exclusive).
            order_by: Field name to sort by (default: "firstname").
            descending: Sort order direction.

        Raises:
            ValueError: If max_age is not an integer or is negative.
        """
        if isinstance(max_age, bool) or not isinstance(max_age, int) or max_age < 0:
            raise ValueError("max_age parameter must be a non-negative integer")

        if order_by not in ("firstname", "age", "id"):
            raise ValueError(f"Unsupported order_by field: {order_by}")

        filtered = [doc for doc in self._documents if doc["age"] < max_age]
        sorted_docs = sorted(
            filtered,
            key=lambda d: d[order_by],
            reverse=descending,
        )
        return sorted_docs

    def __call__(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[PersonDocument]:
        """Callable interface conforming to DocumentStoreClient."""
        params = parameters or {}
        max_age = params.get("max_age")
        if max_age is None:
            raise ValueError("Query parameter 'max_age' is required")
        order_by = params.get("order_by", "firstname")
        descending = params.get("descending", False)
        return self.query_persons_under_age(max_age, order_by=order_by, descending=descending)


# Small local fixture modeled after Lesson 06 (Eva document and PersonsData.json)
FIXTURE_DOCUMENTS: List[PersonDocument] = [
    {
        "firstname": "Eva",
        "age": 44,
        "id": "8c74a315-aebf-4a16-bb38-2430a9896ce5",
        "_rid": "bHwDAPQz8s0BAAAAAAAAAA==",
        "_self": "dbs/bHwDAA==/colls/bHwDAPQz8s0=/docs/bHwDAPQz8s0BAAAAAAAAAA==/",
        "_etag": "\"00000000-0000-0000-9f95-010a691e01d7\"",
        "_attachments": "attachments/",
        "_ts": 1630544034,
    },
    {
        "firstname": "Christophe",
        "age": 32,
        "id": "doc-002",
    },
    {
        "firstname": "Prema",
        "age": 20,
        "id": "doc-003",
    },
    {
        "firstname": "Keisha",
        "age": 84,
        "id": "doc-004",
    },
]


def run_query(
    client: DocumentStoreClient,
    max_age: int,
) -> List[PersonDocument]:
    """Execute a parameterized query using the DocumentStoreClient interface."""
    return client(
        "SELECT * FROM c WHERE c.age < @max_age ORDER BY c.firstname ASC",
        parameters={"max_age": max_age, "order_by": "firstname", "descending": False},
    )


def main() -> None:
    """Run the local applied example and print the ordered results."""
    store = LocalDocumentStore(FIXTURE_DOCUMENTS)
    results = run_query(store, max_age=40)
    for doc in results:
        print(f"{doc['firstname']}: age {doc['age']} (id: {doc['id']})")


if __name__ == "__main__":
    main()
