"""Tests for 3-Data-Visualization/09-visualization-quantities/applied-labs/r39-t040.

Tests normal execution, boundary inputs, failure cases, and verifies the three
applied questions (predict output, diagnose failure, choose boundary policy).
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from example import answer_questions, summarize_quantities


LAB_DIR = Path(__file__).resolve().parent
EXAMPLE = LAB_DIR / "example.py"
FIXTURE = LAB_DIR / "fixture.csv"


def run_cli(csv_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(EXAMPLE), str(csv_path)],
        capture_output=True,
        text=True,
        check=False,
    )


def run_csv_text(csv_text: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_csv = Path(temp_dir) / "test.csv"
        temp_csv.write_text(csv_text, encoding="utf-8")
        return run_cli(temp_csv)


class TestQuantityAggregation(unittest.TestCase):
    # --- Normal Scenarios ---
    def test_normal_fixture_grouping_and_totals(self) -> None:
        result = run_cli(FIXTURE)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {
            "groups": [
                {"category": "Birds of Prey", "quantity": 3},
                {"category": "Songbirds", "quantity": 0},
                {"category": "Waterfowl", "quantity": 7},
            ],
            "total": 10,
        }
        self.assertEqual(json.loads(result.stdout), expected)

    def test_normal_single_row(self) -> None:
        result = run_csv_text("Category,Quantity\nGulls,15\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {"groups": [{"category": "Gulls", "quantity": 15}], "total": 15},
        )

    # --- Boundary Scenarios ---
    def test_boundary_header_only_csv(self) -> None:
        result = run_csv_text("Category,Quantity\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"groups": [], "total": 0})

    def test_boundary_zero_quantities_preserved_and_sorted(self) -> None:
        result = run_csv_text("Category,Quantity\nOwls,0\nFalcons,0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {
            "groups": [
                {"category": "Falcons", "quantity": 0},
                {"category": "Owls", "quantity": 0},
            ],
            "total": 0,
        }
        self.assertEqual(json.loads(result.stdout), expected)

    def test_boundary_large_integers(self) -> None:
        result = run_csv_text("Category,Quantity\nPigeons,1000000\nSparrows,2500000\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "groups": [
                    {"category": "Pigeons", "quantity": 1000000},
                    {"category": "Sparrows", "quantity": 2500000},
                ],
                "total": 3500000,
            },
        )

    # --- Failure Scenarios ---
    def test_failure_invalid_header(self) -> None:
        result = run_csv_text("label,value\nFalcons,1\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("CSV header must be exactly: Category,Quantity", result.stderr)

    def test_failure_empty_category(self) -> None:
        result = run_csv_text("Category,Quantity\n  ,5\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("row 2: category cannot be empty", result.stderr)

    def test_failure_negative_quantity(self) -> None:
        result = run_csv_text("Category,Quantity\nFalcons,-4\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("row 2: quantity must be a non-negative integer", result.stderr)

    def test_failure_non_integer_quantity(self) -> None:
        result = run_csv_text("Category,Quantity\nFalcons,three\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("row 2: quantity must be a non-negative integer", result.stderr)

    def test_failure_misaligned_row_columns(self) -> None:
        result = run_csv_text("Category,Quantity\nFalcons,3,extra\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("row 2: expected exactly two columns", result.stderr)

    # --- Applied Questions Executable Checks ---
    def test_applied_question_1_predict_output(self) -> None:
        """Executable check verifying Q1: predict output for multi-category fixture."""
        qa = answer_questions()["q1_predict_output"]
        summary = summarize_quantities(FIXTURE)
        self.assertEqual(summary, qa["factual_answer"])
        # Reconcile grand total with sum of group quantities
        self.assertEqual(summary["total"], sum(g["quantity"] for g in summary["groups"]))

    def test_applied_question_2_diagnose_failure(self) -> None:
        """Executable check verifying Q2: diagnose failure for negative quantity."""
        qa = answer_questions()["q2_diagnose_failure"]
        result = run_csv_text("Category,Quantity\nDucks/Geese,-4\n")
        self.assertEqual(result.returncode, qa["factual_answer"]["exit_code"])
        self.assertIn(qa["factual_answer"]["diagnostic_substring"], result.stderr)
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as f:
            f.write("Category,Quantity\nDucks/Geese,-4\n")
            f_path = Path(f.name)
        try:
            with self.assertRaises(ValueError) as ctx:
                summarize_quantities(f_path)
            self.assertIn(qa["factual_answer"]["diagnostic_substring"], str(ctx.exception))
        finally:
            f_path.unlink(missing_ok=True)

    def test_applied_question_3_boundary_policy(self) -> None:
        """Executable check verifying Q3: boundary policies for header-only and explicit 0."""
        qa = answer_questions()["q3_boundary_policy"]
        # Check header-only
        res_header = run_csv_text("Category,Quantity\n")
        self.assertEqual(json.loads(res_header.stdout), qa["factual_answer"]["header_only"])

        # Check explicit zero retention
        res_zeros = run_csv_text("Category,Quantity\nHerons,0\n")
        data = json.loads(res_zeros.stdout)
        self.assertEqual(len(data["groups"]), 1)
        self.assertEqual(data["groups"][0], {"category": "Herons", "quantity": 0})
        self.assertTrue(qa["factual_answer"]["zero_quantity_retention"])


if __name__ == "__main__":
    unittest.main()
