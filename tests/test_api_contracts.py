from __future__ import annotations

import pytest

from asbp.api import (
    ApiError,
    ApiRequest,
    ApiResponse,
    ApiResult,
    ApiStatus,
    build_error_response,
    build_success_response,
)


def test_api_request_contract_shape_is_deterministic() -> None:
    request = ApiRequest(
        operation=" show_task ",
        payload={"task_id": "T001"},
        metadata={"request_id": "REQ-1"},
    )

    assert request.to_dict() == {
        "operation": "show_task",
        "payload": {"task_id": "T001"},
        "metadata": {"request_id": "REQ-1"},
    }


def test_api_request_rejects_empty_operation() -> None:
    with pytest.raises(ValueError, match="operation must be a non-empty string"):
        ApiRequest(operation=" ")


def test_api_request_rejects_non_mapping_payload() -> None:
    with pytest.raises(TypeError, match="metadata and payload values must be mappings"):
        ApiRequest(operation="show_task", payload=["not", "a", "mapping"])  # type: ignore[arg-type]


def test_success_response_shape_is_deterministic() -> None:
    response = build_success_response(
        payload={"task_id": "T001"},
        metadata={"request_id": "REQ-1"},
    )

    assert response.to_dict() == {
        "status": "success",
        "result": "accepted",
        "payload": {"task_id": "T001"},
        "error": None,
        "metadata": {"request_id": "REQ-1"},
    }


def test_error_response_shape_is_deterministic() -> None:
    response = build_error_response(
        code="INVALID_REQUEST",
        message="Request is invalid.",
        details={"field": "operation"},
        metadata={"request_id": "REQ-1"},
    )

    assert response.to_dict() == {
        "status": "error",
        "result": "rejected",
        "payload": {},
        "error": {
            "code": "INVALID_REQUEST",
            "message": "Request is invalid.",
            "details": {"field": "operation"},
        },
        "metadata": {"request_id": "REQ-1"},
    }


def test_error_contract_rejects_empty_code_or_message() -> None:
    with pytest.raises(ValueError, match="error code must be a non-empty string"):
        ApiError(code=" ", message="Request is invalid.")

    with pytest.raises(ValueError, match="error message must be a non-empty string"):
        ApiError(code="INVALID_REQUEST", message=" ")


def test_status_and_result_vocabularies_reject_unsupported_values() -> None:
    with pytest.raises(ValueError):
        ApiResponse(status="maybe", result=ApiResult.ACCEPTED)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        ApiResponse(status=ApiStatus.SUCCESS, result="maybe")  # type: ignore[arg-type]


def test_success_response_rejects_error_payload() -> None:
    with pytest.raises(ValueError, match="success responses must not include an error"):
        ApiResponse(
            status=ApiStatus.SUCCESS,
            result=ApiResult.ACCEPTED,
            error=ApiError(code="INVALID", message="Invalid."),
        )


def test_error_response_requires_error_payload() -> None:
    with pytest.raises(ValueError, match="error responses must include an error"):
        ApiResponse(status=ApiStatus.ERROR, result=ApiResult.REJECTED)


def test_contract_module_does_not_introduce_route_or_framework_behavior() -> None:
    import asbp.api.contracts as contracts

    names = set(dir(contracts))

    assert "FastAPI" not in names
    assert "Flask" not in names
    assert "APIRouter" not in names
    assert "route" not in names
    assert "endpoint" not in names
