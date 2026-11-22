"""Summarize quantities by category with aligned labels and aggregate totals.

Illustrates grouping, label/value alignment, and aggregate totals from
3-Data-Visualization/09-visualization-quantities/README.md.
"""

import argparse
import csv
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional


HEADERS = ["Category", "Quantity"]


def summarize_quantities(path: Path) -> Dict[str, Any]:
    """Group quantities by category and return aligned categories and aggregate total.
    
    Validates exact header: Category,Quantity
    Validates non-empty string Category, non-negative integer Quantity.
    Returns categories sorted alphabetically with preserved zero quantities and grand total.
    """
    totals: Dict[str, int] = {}

    with path.open(encoding="utf-8", newline="") as input_file:
        reader = csv.DictReader(input_file)
        if reader.fieldnames != HEADERS:
            raise ValueError(f"CSV header must be exactly: {','.join(HEADERS)}")

        for row in reader:
            row_number = reader.line_num
            if None in row or row.get("Category") is None or row.get("Quantity") is None:
                raise ValueError(f"row {row_number}: expected exactly two columns")

            category = row["Category"].strip()
            if not category:
                raise ValueError(f"row {row_number}: category cannot be empty")

            try:
                quantity = int(row["Quantity"])
            except ValueError as exc:
                raise ValueError(
                    f"row {row_number}: quantity must be a non-negative integer"
                ) from exc

            if quantity < 0:
                raise ValueError(f"row {row_number}: quantity must be a non-negative integer")

            totals[category] = totals.get(category, 0) + quantity

    groups: List[Dict[str, Any]] = [
        {"category": cat, "quantity": totals[cat]} for cat in sorted(totals)
    ]
    return {"groups": groups, "total": sum(totals.values())}


def answer_questions() -> Dict[str, Dict[str, Any]]:
    """Return the three applied questions, their rationale, and factual answers."""
    return {
        "q1_predict_output": {
            "question": "What is the grouped output and aggregate total for a dataset with categories Waterfowl (5), Birds of Prey (3), Waterfowl (2), and Songbirds (0)?",
            "factual_answer": {
                "groups": [
                    {"category": "Birds of Prey", "quantity": 3},
                    {"category": "Songbirds", "quantity": 0},
                    {"category": "Waterfowl", "quantity": 7},
                ],
                "total": 10,
            },
            "rationale": "Waterfowl occurrences are aggregated (5 + 2 = 7), Songbirds with 0 is retained with exact label/value alignment, Birds of Prey has 3, and categories are sorted alphabetically. Grand total is 3 + 0 + 7 = 10.",
        },
        "q2_diagnose_failure": {
            "question": "Why does a CSV row containing 'Ducks/Geese,-4' fail validation, and what diagnostic is emitted?",
            "factual_answer": {
                "error_type": "ValueError",
                "diagnostic_substring": "quantity must be a non-negative integer",
                "exit_code": 2,
            },
            "rationale": "Quantities represent physical counts or measurable non-negative extents; negative values violate the domain contract and are rejected with a descriptive ValueError.",
        },
        "q3_boundary_policy": {
            "question": "What is the boundary policy when input data has only the CSV header with zero data rows, or contains explicit zero quantities?",
            "factual_answer": {
                "header_only": {"groups": [], "total": 0},
                "zero_quantity_retention": True,
            },
            "rationale": "A header-only CSV is valid tabular data representing zero observed entities (empty groups list and total of 0). Categories explicitly recorded with a quantity of 0 are preserved in the grouped output to accurately show observed absence rather than omitting the category.",
        },
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV file with Category,Quantity columns")
    args = parser.parse_args(argv)

    try:
        summary = summarize_quantities(args.csv_file)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"{parser.prog}: error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
