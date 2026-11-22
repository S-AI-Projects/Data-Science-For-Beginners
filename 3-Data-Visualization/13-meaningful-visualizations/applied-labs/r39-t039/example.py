"""Summarize integer values by label for a small meaningful-visualization example."""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


HEADERS = ["label", "value"]


def summarize_csv(path: Path) -> Dict[str, object]:
    """Group CSV values by label and return aligned groups and their grand total."""
    totals: Dict[str, int] = {}

    with path.open(encoding="utf-8", newline="") as input_file:
        reader = csv.DictReader(input_file)
        if reader.fieldnames != HEADERS:
            raise ValueError("CSV header must be exactly: label,value")

        for row in reader:
            row_number = reader.line_num
            if None in row or row.get("label") is None or row.get("value") is None:
                raise ValueError(f"row {row_number}: expected exactly two columns")

            label = row["label"].strip()
            if not label:
                raise ValueError(f"row {row_number}: label cannot be empty")

            try:
                value = int(row["value"])
            except ValueError as exc:
                raise ValueError(
                    f"row {row_number}: value must be a non-negative integer"
                ) from exc

            if value < 0:
                raise ValueError(f"row {row_number}: value must be a non-negative integer")

            totals[label] = totals.get(label, 0) + value

    groups: List[Dict[str, object]] = [
        {"label": label, "value": totals[label]} for label in sorted(totals)
    ]
    return {"groups": groups, "total": sum(totals.values())}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV file with label,value columns")
    args = parser.parse_args(argv)

    try:
        summary = summarize_csv(args.csv_file)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"{parser.prog}: error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
