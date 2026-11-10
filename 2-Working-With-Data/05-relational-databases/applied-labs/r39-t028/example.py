"""
SQLite Parameterized Query Evaluation (R39-T028)

Extends lesson 05 (Relational Databases) by implementing safe parameterized queries
in an in-memory SQLite database:
- Avoids string interpolation vulnerability.
- Quotes in input parameters are treated strictly as literal data.
- Returns results in deterministic alphabetical name order.
- Compares three controlled dataset sizes for execution performance and correctness.
"""

import sqlite3
import time
from typing import Any, Dict, List, Tuple


def create_items_db(rows: List[Tuple[str, str]]) -> sqlite3.Connection:
    """Creates an in-memory SQLite database with an items table populated with rows."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE items (name TEXT NOT NULL, category TEXT NOT NULL)")
    cur.executemany("INSERT INTO items (name, category) VALUES (?, ?)", rows)
    conn.commit()
    return conn


def query_by_category_parameterized(conn: sqlite3.Connection, category: str) -> List[str]:
    """Queries item names for a given category using parameterized SQL with alphabetical ordering."""
    cur = conn.cursor()
    cur.execute("SELECT name FROM items WHERE category = ? ORDER BY name ASC", (category,))
    return [row[0] for row in cur.fetchall()]


def evaluate_configurations() -> List[Dict[str, Any]]:
    """
    Compares three controlled dataset size configurations:
    Config A: Small (3 rows - canonical fixture)
    Config B: Medium (10 rows)
    Config C: Scaled (25 rows)
    Returns benchmark and correctness metrics.
    """
    configs = {
        "Small (N=3)": [("tea", "drink"), ("rice", "food"), ("coffee", "drink")],
        "Medium (N=10)": [
            ("tea", "drink"), ("rice", "food"), ("coffee", "drink"),
            ("water", "drink"), ("bread", "food"), ("juice", "drink"),
            ("apple", "food"), ("milk", "drink"), ("soup", "food"), ("soda", "drink")
        ],
        "Scaled (N=25)": [
            (f"item_{i:02d}", "drink" if i % 2 == 0 else "food")
            for i in range(25)
        ]
    }

    results = []
    for label, data in configs.items():
        conn = create_items_db(data)
        start_time = time.perf_counter()
        # Query 100 times to obtain stable micro-benchmark
        for _ in range(100):
            res = query_by_category_parameterized(conn, "drink")
        elapsed_us = (time.perf_counter() - start_time) * 1e6 / 100

        results.append({
            "config": label,
            "total_rows": len(data),
            "drink_matches": len(res),
            "sample_results": res[:3],
            "avg_latency_us": round(elapsed_us, 2)
        })
        conn.close()

    return results


if __name__ == "__main__":
    canonical_rows = [("tea", "drink"), ("rice", "food"), ("coffee", "drink")]
    conn = create_items_db(canonical_rows)
    print("Drink items (sorted):", query_by_category_parameterized(conn, "drink"))
    print("Quote test:", query_by_category_parameterized(conn, "drink' OR '1'='1"))
    conn.close()
    print("Evaluation:", evaluate_configurations())
