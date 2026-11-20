# R39-T048: Parameterized Local SQLite Query (Failure & Recovery)

## Overview
This local applied lab extends [Working with Data: Non-Relational Data](../../README.md) by demonstrating secure parameterized SQL querying, handling quote-containing literal values, and implementing graceful error recovery.

## Contract & Fixture
- **Database:** In-memory SQLite table `items (name TEXT, category TEXT)`
- **Seed Data:** `[("tea", "drink"), ("rice", "food"), ("coffee", "drink")]`
- **Category Query `drink`:** Returns `["coffee", "tea"]` (alphabetical name order).
- **Quote-Containing Literal:** `drink' OR '1'='1` is treated as literal data, returning `[]` without SQL injection.

## Failure & Recovery
- **Failure:** Passing `None` or empty string `""` triggers a documented `ValueError`.
- **Recovery:** Database connection remains fully healthy, and subsequent valid query for `food` immediately succeeds, returning `["rice"]`.

## Invocation & Output
```bash
python3 2-Working-With-Data/06-non-relational/applied-labs/r39-t048/example.py
```
Output:
```json
{
  "drink_items": ["coffee", "tea"],
  "quote_query_items": [],
  "failure_caught": "Invalid category parameter: ''. Must be a non-empty string.",
  "recovered_food_items": ["rice"]
}
```

Run tests:
```bash
python3 -m unittest discover -s 2-Working-With-Data/06-non-relational/applied-labs/r39-t048 -p "test_*.py"
```
