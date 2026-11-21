"""Local mock scoring service and request client simulating Azure ML Low-Code AutoML endpoint.

Illustrates the scoring service workflow described in 5-Data-Science-In-Cloud/18-Low-Code/README.md.
"""

from dataclasses import dataclass
import json
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union


# Expected feature schema based on the Heart Failure dataset (12 features)
EXPECTED_FEATURES: Tuple[str, ...] = (
    "age",
    "anaemia",
    "creatinine_phosphokinase",
    "diabetes",
    "ejection_fraction",
    "high_blood_pressure",
    "platelets",
    "serum_creatinine",
    "serum_sodium",
    "sex",
    "smoking",
    "time",
)

BOOLEAN_FEATURES = frozenset({
    "anaemia",
    "diabetes",
    "high_blood_pressure",
    "sex",
    "smoking",
})

NUMERICAL_FEATURES = frozenset({
    "age",
    "creatinine_phosphokinase",
    "ejection_fraction",
    "platelets",
    "serum_creatinine",
    "serum_sodium",
    "time",
})


@dataclass(frozen=True)
class EndpointResponse:
    status_code: int
    raw_body: bytes
    json_data: Optional[Dict[str, Any]]
    error: Optional[str] = None


class ScoringServiceError(Exception):
    """Raised when the scoring service encounters an error."""
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _parse_bool(val: Any, field_name: str) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        if val in (0, 0.0):
            return False
        if val in (1, 1.0):
            return True
        raise ValueError(f"Field '{field_name}' numeric value must be 0 or 1, got {val}")
    if isinstance(val, str):
        v = val.strip().lower()
        if v in ("true", "1", "yes"):
            return True
        if v in ("false", "0", "no"):
            return False
        raise ValueError(f"Field '{field_name}' string value must be boolean-compatible, got '{val}'")
    raise TypeError(f"Field '{field_name}' must be boolean or string representation, got {type(val).__name__}")


def _parse_float(val: Any, field_name: str) -> float:
    if isinstance(val, bool):
        raise TypeError(f"Field '{field_name}' expected numerical value, got boolean {val}")
    try:
        f = float(val)
        if f < 0:
            raise ValueError(f"Field '{field_name}' must be non-negative, got {f}")
        return f
    except (ValueError, TypeError) as exc:
        if isinstance(exc, ValueError) and "must be non-negative" in str(exc):
            raise
        raise ValueError(f"Field '{field_name}' must be a valid number, got {val!r}") from exc


def validate_and_parse_record(record: Mapping[str, Any]) -> Dict[str, Union[float, bool]]:
    """Validate a single patient record against the 12 expected features."""
    if not isinstance(record, Mapping):
        raise TypeError(f"Record must be a key-value mapping, got {type(record).__name__}")

    missing_fields = [f for f in EXPECTED_FEATURES if f not in record]
    if missing_fields:
        raise ValueError(f"Missing required feature(s): {', '.join(missing_fields)}")

    cleaned: Dict[str, Union[float, bool]] = {}

    for f in EXPECTED_FEATURES:
        val = record[f]
        if val is None or (isinstance(val, str) and val.strip() == ""):
            raise ValueError(f"Field '{f}' cannot be null or empty")

        if f in BOOLEAN_FEATURES:
            cleaned[f] = _parse_bool(val, f)
        else:
            cleaned[f] = _parse_float(val, f)

    return cleaned


def mock_predict(parsed_record: Dict[str, Union[float, bool]]) -> bool:
    """Deterministic local mock inference rule.

    Replicates the lesson's observed predictions without external ML models:
    - Default sample (all 0 / false) -> True
    - Clinical sample (age 60, platelets 260k, time 130, etc.) -> False
    """
    # If time follow-up is 0 and ejection fraction is 0, high risk / baseline default
    time_val = float(parsed_record["time"])
    ef_val = float(parsed_record["ejection_fraction"])
    serum_creat = float(parsed_record["serum_creatinine"])

    if time_val < 30 and (ef_val < 20 or serum_creat > 2.0):
        return True
    if time_val == 0.0 and ef_val == 0.0:
        return True

    return False


class MockAzureMLEndpoint:
    """Simulates an Azure Container Instance REST scoring endpoint."""

    def __init__(self, api_key: str = "mock-azure-key-12345") -> None:
        self.api_key = api_key

    def handle_request(self, payload_bytes: bytes, auth_header: Optional[str] = None) -> EndpointResponse:
        """Process incoming raw request bytes and return HTTP-like response."""
        # 1. Authentication check
        expected_auth = f"Bearer {self.api_key}"
        if auth_header != expected_auth and auth_header != self.api_key:
            err_body = json.dumps({"error": "Unauthorized: Invalid or missing API key"}).encode("utf-8")
            return EndpointResponse(status_code=401, raw_body=err_body, json_data=None, error="Unauthorized")

        # 2. JSON decoding check
        try:
            payload_str = payload_bytes.decode("utf-8")
            req_data = json.loads(payload_str)
        except Exception as exc:
            err_body = json.dumps({"error": f"Invalid JSON payload: {str(exc)}"}).encode("utf-8")
            return EndpointResponse(status_code=400, raw_body=err_body, json_data=None, error=f"Invalid JSON: {exc}")

        # 3. Payload contract check
        if not isinstance(req_data, dict) or "data" not in req_data:
            err_body = json.dumps({"error": "Payload must contain top-level 'data' key"}).encode("utf-8")
            return EndpointResponse(status_code=400, raw_body=err_body, json_data=None, error="Missing 'data' key")

        data_list = req_data["data"]
        if not isinstance(data_list, list) or len(data_list) == 0:
            err_body = json.dumps({"error": "'data' must be a non-empty list of records"}).encode("utf-8")
            return EndpointResponse(status_code=400, raw_body=err_body, json_data=None, error="Empty or invalid 'data'")

        # 4. Feature validation & scoring
        results: List[bool] = []
        for idx, item in enumerate(data_list):
            try:
                parsed = validate_and_parse_record(item)
                pred = mock_predict(parsed)
                results.append(pred)
            except (ValueError, TypeError) as exc:
                err_body = json.dumps({"error": f"Validation error at record {idx}: {str(exc)}"}).encode("utf-8")
                return EndpointResponse(
                    status_code=422,
                    raw_body=err_body,
                    json_data=None,
                    error=f"Record {idx} validation error: {exc}",
                )

        # 5. Return success in Azure ML format: b'"{\\"result\\": [true, false]}"'
        # In urllib / requests, the Azure ML endpoint returns a JSON string enclosed in quotes with escaped characters
        inner_json = json.dumps({"result": results})
        raw_output = f'"{inner_json.replace(chr(34), chr(92) + chr(34))}"'.encode("utf-8")
        return EndpointResponse(
            status_code=200,
            raw_body=raw_output,
            json_data={"result": results},
            error=None,
        )


def run_client_consumption(
    endpoint: MockAzureMLEndpoint,
    data_payload: Dict[str, Any],
    api_key: str,
) -> EndpointResponse:
    """Local simulation of the endpoint consumption script from README section 3.2."""
    body_bytes = json.dumps(data_payload).encode("utf-8")
    auth_header = f"Bearer {api_key}"
    return endpoint.handle_request(body_bytes, auth_header=auth_header)


# Canonical fixtures matching lesson 3.2
FIXTURE_DEFAULT_SAMPLE = {
    "age": "0",
    "anaemia": "false",
    "creatinine_phosphokinase": "0",
    "diabetes": "false",
    "ejection_fraction": "0",
    "high_blood_pressure": "false",
    "platelets": "0",
    "serum_creatinine": "0",
    "serum_sodium": "0",
    "sex": "false",
    "smoking": "false",
    "time": "0",
}

FIXTURE_CLINICAL_SAMPLE = {
    "age": "60",
    "anaemia": "false",
    "creatinine_phosphokinase": "500",
    "diabetes": "false",
    "ejection_fraction": "38",
    "high_blood_pressure": "false",
    "platelets": "260000",
    "serum_creatinine": "1.40",
    "serum_sodium": "137",
    "sex": "false",
    "smoking": "false",
    "time": "130",
}


def main() -> None:
    """Run normal scoring, documented invalid failure, and subsequent recovery."""
    api_key = "mock-azure-key-12345"
    endpoint = MockAzureMLEndpoint(api_key=api_key)

    print("--- 1. Single sample execution (lesson default: all 0 / false) ---")
    single_payload = {"data": [FIXTURE_DEFAULT_SAMPLE]}
    resp1 = run_client_consumption(endpoint, single_payload, api_key)
    print(f"Status Code: {resp1.status_code}")
    print(f"Response Body: {resp1.raw_body}")
    print(f"Parsed Result: {resp1.json_data}")

    print("\n--- 2. Dual sample execution (lesson batch: default + clinical) ---")
    dual_payload = {"data": [FIXTURE_DEFAULT_SAMPLE, FIXTURE_CLINICAL_SAMPLE]}
    resp2 = run_client_consumption(endpoint, dual_payload, api_key)
    print(f"Status Code: {resp2.status_code}")
    print(f"Response Body: {resp2.raw_body}")
    print(f"Parsed Result: {resp2.json_data}")

    print("\n--- 3. Invalid / Missing-Data Case ---")
    invalid_sample = dict(FIXTURE_DEFAULT_SAMPLE)
    del invalid_sample["serum_creatinine"]  # Missing required clinical feature
    invalid_payload = {"data": [invalid_sample]}
    resp_err = run_client_consumption(endpoint, invalid_payload, api_key)
    print(f"Status Code: {resp_err.status_code}")
    print(f"Response Body: {resp_err.raw_body.decode('utf-8')}")
    print(f"Error Diagnostic: {resp_err.error}")

    print("\n--- 4. Recovery Demonstration on Valid Input ---")
    # Recover by supplying the missing field on the next request
    recovered_sample = dict(invalid_sample)
    recovered_sample["serum_creatinine"] = "1.10"
    recovered_payload = {"data": [recovered_sample]}
    resp_recovered = run_client_consumption(endpoint, recovered_payload, api_key)
    print(f"Status Code: {resp_recovered.status_code}")
    print(f"Response Body: {resp_recovered.raw_body}")
    print(f"Parsed Result: {resp_recovered.json_data}")
    print("Recovery verified: service resumed healthy predictions.")


if __name__ == "__main__":
    main()
