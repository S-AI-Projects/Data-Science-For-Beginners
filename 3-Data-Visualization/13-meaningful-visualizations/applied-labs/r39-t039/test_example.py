"""Tests for the local grouped-total example."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


LAB_DIR = Path(__file__).resolve().parent
EXAMPLE = LAB_DIR / "example.py"


def run_example(csv_text: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = Path(temp_dir) / "input.csv"
        csv_path.write_text(csv_text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(EXAMPLE), str(csv_path)],
            capture_output=True,
            text=True,
            check=False,
        )


class TestGroupedTotals(unittest.TestCase):
    def test_normal_fixture_groups_labels_and_reconciles_total(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXAMPLE), str(LAB_DIR / "fixture.csv")],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "groups": [
                    {"label": "Garden", "value": 10},
                    {"label": "Harbor", "value": 6},
                    {"label": "Hill", "value": 0},
                ],
                "total": 16,
            },
        )

    def test_boundary_header_only_csv_has_empty_groups_and_zero_total(self) -> None:
        result = run_example("label,value\n")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"groups": [], "total": 0})

    def test_boundary_zero_value_is_retained_and_labels_are_sorted(self) -> None:
        result = run_example("label,value\nZebra,0\nApple,0\n")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "groups": [
                    {"label": "Apple", "value": 0},
                    {"label": "Zebra", "value": 0},
                ],
                "total": 0,
            },
        )

    def test_failure_negative_value_exits_nonzero_with_diagnostic(self) -> None:
        result = run_example("label,value\nGarden,-1\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("row 2: value must be a non-negative integer", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_failure_misaligned_csv_row_exits_nonzero(self) -> None:
        result = run_example("label,value\nGarden,3,unexpected\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("row 2: expected exactly two columns", result.stderr)


if __name__ == "__main__":
    unittest.main()
