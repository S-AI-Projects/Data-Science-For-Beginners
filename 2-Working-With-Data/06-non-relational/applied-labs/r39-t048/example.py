"""Parameterized SQLite local query with failure and recovery (R39-T048).

Extends the Non-Relational Data lesson by creating an in-memory SQLite items
table and querying by category using parameters rather than string interpolation.
Handles quote-containing categories as literal data, exercises invalid inputs,
and demonstrates robust recovery.
"""

from __future__ import annotations
import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class ItemsDatabase:
    """In-memory SQLite database managing items and parameterized queries."""

    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute("CREATE TABLE items (name TEXT NOT NULL, category TEXT NOT NULL)")

    def seed(self, items: List[Tuple[str, str]]) -> None:
        with self.conn:
            self.conn.executemany("INSERT INTO items (name, category) VALUES (?, ?)", items)

    def query_by_category(self, category: Optional[str]) -> List[str]:
        """Query items by category using parameterized SQL.

        Enforces documented validation: category cannot be None, empty, or non-string.
        Raises ValueError on invalid input; treats quote-containing categories as literal values.
        """
        if category is None or not isinstance(category, str) or not category.strip():
            raise ValueError(f"Invalid category parameter: {repr(category)}. Must be a non-empty string.")

        cursor = self.conn.cursor()
        # Parameterized query ensures literal value matching and prevents SQL injection
        cursor.execute("SELECT name FROM items WHERE category = ? ORDER BY name ASC", (category,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def close(self) -> None:
        self.conn.close()


def run_demo() -> Dict[str, Any]:
    db = ItemsDatabase()
    try:
        # Stated contract rows: (tea,drink),(rice,food),(coffee,drink)
        seed_data = [("tea", "drink"), ("rice", "food"), ("coffee", "drink")]
        db.seed(seed_data)

        # 1. Normal query: drink -> returns coffee, tea in name order
        drink_items = db.query_by_category("drink")

        # 2. Quote-containing category: remains literal data
        quote_cat = "drink' OR '1'='1"
        quote_items = db.query_by_category(quote_cat)

        # 3. Documented invalid input exercising failure
        failure_caught = None
        try:
            db.query_by_category("")
        except ValueError as e:
            failure_caught = str(e)

        # 4. Immediate recovery on next valid input
        food_items = db.query_by_category("food")

        return {
            "drink_items": drink_items,
            "quote_query_items": quote_items,
            "failure_caught": failure_caught,
            "recovered_food_items": food_items,
        }
    finally:
        db.close()


def main() -> None:
    results = run_demo()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
