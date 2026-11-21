"""Parameterized local query with state trace.
Task R39-T054.
"""

import sqlite3
from typing import List, Dict, Any, Tuple


class ItemDatabase:
    """Manages an in memory SQLite database and records step by step states."""

    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self.state_trace: List[Dict[str, Any]] = []

    def setup_table(self) -> None:
        """Create the items table and record state."""
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE items (name TEXT, category TEXT)")
        self.conn.commit()
        self.state_trace.append({"step": "setup_table", "table_created": True, "row_count": 0})

    def insert_rows(self, rows: List[Tuple[str, str]]) -> None:
        """Insert rows into items table using parameterized queries."""
        cur = self.conn.cursor()
        cur.executemany("INSERT INTO items (name, category) VALUES (?, ?)", rows)
        self.conn.commit()

        # Count total rows and category frequency for the invariant trace
        cur.execute("SELECT COUNT(*) FROM items")
        total_rows = cur.fetchone()[0]

        category_counts: Dict[str, int] = {}
        cur.execute("SELECT category, COUNT(*) FROM items GROUP BY category")
        for cat, cnt in cur.fetchall():
            category_counts[cat] = cnt

        self.state_trace.append({
            "step": "insert_rows",
            "total_rows": total_rows,
            "category_counts": category_counts,
        })

    def query_category(self, category: str) -> List[str]:
        """Query items by category using parameters and return names in order."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT name FROM items WHERE category = ? ORDER BY name ASC",
            (category,),
        )
        results = [row[0] for row in cur.fetchall()]

        self.state_trace.append({
            "step": "query_category",
            "queried_category": category,
            "result_count": len(results),
            "results": results,
        })
        return results

    def verify_invariant(self, category: str, results: List[str]) -> bool:
        """Check invariant: result count matches intermediate category count."""
        insert_state = next(
            (s for s in self.state_trace if s["step"] == "insert_rows"), None
        )
        if not insert_state:
            return False

        expected_count = insert_state["category_counts"].get(category, 0)
        is_sorted = results == sorted(results)
        return len(results) == expected_count and is_sorted

    def close(self) -> None:
        self.conn.close()


def run_pipeline() -> Dict[str, Any]:
    db = ItemDatabase()
    db.setup_table()
    rows = [("tea", "drink"), ("rice", "food"), ("coffee", "drink")]
    db.insert_rows(rows)
    drinks = db.query_category("drink")
    invariant_passed = db.verify_invariant("drink", drinks)

    # Test quote containing input to prove literal matching
    quote_results = db.query_category("' OR '1'='1")
    db.close()

    return {
        "drinks": drinks,
        "invariant_passed": invariant_passed,
        "quote_results": quote_results,
    }


def main() -> None:
    res = run_pipeline()
    print("Drinks queried in name order:", res["drinks"])
    print("State invariant passed:", res["invariant_passed"])
    print("Malicious quote query results:", res["quote_results"])


if __name__ == "__main__":
    main()
