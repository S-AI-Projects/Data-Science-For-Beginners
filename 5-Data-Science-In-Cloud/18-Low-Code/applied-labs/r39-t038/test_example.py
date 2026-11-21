"""Unit tests for applied lab r39-t038.

Tests normal execution, boundary inputs, failure cases (auth, validation, missing fields),
and subsequent recovery on valid input.
"""

import json
import subprocess
import sys
import unittest

from example import (
    BOOLEAN_FEATURES,
    EXPECTED_FEATURES,
    FIXTURE_CLINICAL_SAMPLE,
    FIXTURE_DEFAULT_SAMPLE,
    MockAzureMLEndpoint,
    NUMERICAL_FEATURES,
    mock_predict,
    run_client_consumption,
    validate_and_parse_record,
)


class TestMockAzureMLEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.api_key = "test-secret-key-999"
        self.endpoint = MockAzureMLEndpoint(api_key=self.api_key)

    # --- Normal Scenarios ---
    def test_normal_single_sample_scoring(self) -> None:
        payload = {"data": [FIXTURE_DEFAULT_SAMPLE]}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.error)
        self.assertEqual(resp.json_data, {"result": [True]})
        # Verify raw body matches Azure ML serialized format
        self.assertEqual(resp.raw_body, b'"{\\"result\\": [true]}"')

    def test_normal_dual_sample_scoring(self) -> None:
        payload = {"data": [FIXTURE_DEFAULT_SAMPLE, FIXTURE_CLINICAL_SAMPLE]}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.error)
        self.assertEqual(resp.json_data, {"result": [True, False]})
        self.assertEqual(resp.raw_body, b'"{\\"result\\": [true, false]}"')

    # --- Boundary Scenarios ---
    def test_boundary_boolean_formats(self) -> None:
        # Test varied boolean representations: "1", "0", True, False, "true", "false", "yes", "no"
        sample_bools = dict(FIXTURE_DEFAULT_SAMPLE)
        sample_bools["anaemia"] = 1
        sample_bools["diabetes"] = "yes"
        sample_bools["high_blood_pressure"] = "no"
        sample_bools["sex"] = True
        sample_bools["smoking"] = "0"

        parsed = validate_and_parse_record(sample_bools)
        self.assertIs(parsed["anaemia"], True)
        self.assertIs(parsed["diabetes"], True)
        self.assertIs(parsed["high_blood_pressure"], False)
        self.assertIs(parsed["sex"], True)
        self.assertIs(parsed["smoking"], False)

    def test_boundary_zero_and_large_numbers(self) -> None:
        # Test extreme boundary numbers
        sample_num = dict(FIXTURE_DEFAULT_SAMPLE)
        sample_num["age"] = "0"
        sample_num["platelets"] = 1000000.0
        sample_num["serum_creatinine"] = "0.0"
        parsed = validate_and_parse_record(sample_num)
        self.assertEqual(parsed["age"], 0.0)
        self.assertEqual(parsed["platelets"], 1000000.0)
        self.assertEqual(parsed["serum_creatinine"], 0.0)

    def test_boundary_batch_single_and_multiple(self) -> None:
        # 10 records in a batch
        batch = [dict(FIXTURE_DEFAULT_SAMPLE) for _ in range(10)]
        payload = {"data": batch}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json_data["result"]), 10)

    # --- Failure Scenarios & Diagnostics ---
    def test_failure_unauthorized_missing_or_bad_api_key(self) -> None:
        payload = {"data": [FIXTURE_DEFAULT_SAMPLE]}
        # Bad API key
        resp_bad = run_client_consumption(self.endpoint, payload, "wrong-key")
        self.assertEqual(resp_bad.status_code, 401)
        self.assertIn("Unauthorized", resp_bad.error)

        # Direct missing auth
        raw_body = json.dumps(payload).encode("utf-8")
        resp_none = self.endpoint.handle_request(raw_body, auth_header=None)
        self.assertEqual(resp_none.status_code, 401)

    def test_failure_invalid_json_bytes(self) -> None:
        invalid_bytes = b"not a json string"
        resp = self.endpoint.handle_request(invalid_bytes, auth_header=f"Bearer {self.api_key}")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid JSON", resp.error)

    def test_failure_missing_top_level_data_key(self) -> None:
        payload = {"wrong_key": [FIXTURE_DEFAULT_SAMPLE]}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Missing 'data' key", resp.error)

    def test_failure_empty_data_list(self) -> None:
        payload = {"data": []}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Empty or invalid 'data'", resp.error)

    def test_failure_missing_feature_column(self) -> None:
        bad_sample = dict(FIXTURE_DEFAULT_SAMPLE)
        del bad_sample["platelets"]
        payload = {"data": [bad_sample]}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 422)
        self.assertIn("Missing required feature(s): platelets", resp.error)

    def test_failure_null_or_empty_field_value(self) -> None:
        bad_sample = dict(FIXTURE_DEFAULT_SAMPLE)
        bad_sample["ejection_fraction"] = ""
        payload = {"data": [bad_sample]}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 422)
        self.assertIn("cannot be null or empty", resp.error)

    def test_failure_invalid_numeric_value(self) -> None:
        bad_sample = dict(FIXTURE_DEFAULT_SAMPLE)
        bad_sample["age"] = "not_a_number"
        payload = {"data": [bad_sample]}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 422)
        self.assertIn("must be a valid number", resp.error)

    def test_failure_negative_numeric_value(self) -> None:
        bad_sample = dict(FIXTURE_DEFAULT_SAMPLE)
        bad_sample["serum_sodium"] = -10
        payload = {"data": [bad_sample]}
        resp = run_client_consumption(self.endpoint, payload, self.api_key)
        self.assertEqual(resp.status_code, 422)
        self.assertIn("must be non-negative", resp.error)

    # --- Documented Failure and Recovery Demonstration ---
    def test_invalid_missing_data_and_subsequent_recovery(self) -> None:
        """Explicitly exercises missing-data error and demonstrates immediate recovery on valid input."""
        # 1. Invalid input: missing required clinical feature
        invalid_sample = dict(FIXTURE_DEFAULT_SAMPLE)
        del invalid_sample["serum_creatinine"]
        err_resp = run_client_consumption(self.endpoint, {"data": [invalid_sample]}, self.api_key)
        self.assertEqual(err_resp.status_code, 422)
        self.assertIn("Missing required feature(s): serum_creatinine", err_resp.error)

        # 2. Recovery on next valid input
        recovered_sample = dict(invalid_sample)
        recovered_sample["serum_creatinine"] = "1.10"
        ok_resp = run_client_consumption(self.endpoint, {"data": [recovered_sample]}, self.api_key)
        self.assertEqual(ok_resp.status_code, 200)
        self.assertIsNone(ok_resp.error)
        self.assertEqual(ok_resp.json_data, {"result": [True]})

    # --- Regression test of CLI output ---
    def test_cli_execution_and_stdout(self) -> None:
        proc = subprocess.run(
            [sys.executable, "5-Data-Science-In-Cloud/18-Low-Code/applied-labs/r39-t038/example.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("--- 1. Single sample execution", proc.stdout)
        self.assertIn('Response Body: b\'"{\\\\"result\\\\": [true]}"\'', proc.stdout)
        self.assertIn('Response Body: b\'"{\\\\"result\\\\": [true, false]}"\'', proc.stdout)
        self.assertIn("Status Code: 422", proc.stdout)
        self.assertIn("Missing required feature(s): serum_creatinine", proc.stdout)
        self.assertIn("Recovery verified: service resumed healthy predictions.", proc.stdout)


if __name__ == "__main__":
    unittest.main()
