"Evaluation and regression harness for M31.7 governed AI assistance."

from __future__ import annotations

from typing import Any

from asbp.ai_runtime.context_packets import validate_ai_context_packet
from asbp.ai_runtime.output_acceptance import (
    AI_OUTPUT_REVIEW_ACCEPTANCE_STATUS_VALIDATED,
    validate_ai_output_review_decision,
)
from asbp.ai_runtime.provider_contracts import (
    AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
    DISABLED_PROVIDER_KIND,
    PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
    validate_ai_provider_adapter_boundary_request,
)
from asbp.ai_runtime.refusal_rules import (
    AI_REFUSAL_RULES_STATUS_VALIDATED,
    validate_ai_refusal_limitation_decision,
)

AI_EVALUATION_HARNESS_CHECKPOINT_ID = "M31.7"
AI_EVALUATION_HARNESS_CONTRACT_VERSION = "ai-evaluation-regression-harness-v1"
AI_EVALUATION_HARNESS_STATUS_VALIDATED = "ai_evaluation_regression_harness_validated"
AI_PROVIDER_SMOKE_STATUS_BLOCKED = "ai_provider_smoke_blocked"
AI_PROVIDER_SMOKE_STATUS_SKIPPED = "ai_provider_smoke_skipped"
AI_PROVIDER_SMOKE_STATUS_READY = "ai_provider_smoke_ready"

REGRESSION_CASE_CONTEXT_PACKET = "context_packet_regression"
REGRESSION_CASE_REFUSAL_LIMITATION = "refusal_limitation_regression"
REGRESSION_CASE_OUTPUT_ACCEPTANCE = "output_acceptance_review_regression"
REGRESSION_CASE_PROVIDER_BOUNDARY = "provider_boundary_regression"
REGRESSION_CASE_PROVIDER_SMOKE = "provider_smoke_gate_regression"
SUPPORTED_REGRESSION_CASE_KINDS = (
    REGRESSION_CASE_CONTEXT_PACKET,
    REGRESSION_CASE_REFUSAL_LIMITATION,
    REGRESSION_CASE_OUTPUT_ACCEPTANCE,
    REGRESSION_CASE_PROVIDER_BOUNDARY,
    REGRESSION_CASE_PROVIDER_SMOKE,
)

REGRESSION_PASS_STATUS = "pass"
REGRESSION_FAIL_CLOSED_STATUS = "fail_closed"
REGRESSION_SKIPPED_STATUS = "skipped"
SUPPORTED_REGRESSION_STATUSES = (
    REGRESSION_PASS_STATUS,
    REGRESSION_FAIL_CLOSED_STATUS,
    REGRESSION_SKIPPED_STATUS,
)

LOCAL_PROVIDER_SMOKE_KIND = "local_provider_smoke"
DISABLED_PROVIDER_SMOKE_KIND = "disabled_provider_smoke"
SUPPORTED_PROVIDER_SMOKE_KINDS = (
    LOCAL_PROVIDER_SMOKE_KIND,
    DISABLED_PROVIDER_SMOKE_KIND,
)

_REQUIRED_REGRESSION_CASE_STRING_FIELDS = (
    "case_id",
    "case_kind",
    "description",
    "expected_status",
    "evidence_ref",
)

_REQUIRED_EVALUATION_RESULT_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "evaluation_result_id",
    "evaluation_status",
)

_REQUIRED_SMOKE_REQUEST_STRING_FIELDS = (
    "smoke_request_id",
    "smoke_kind",
    "provider_boundary_status",
    "provider_execution_status",
    "provider_kind",
)

_REQUIRED_FALSE_FIELDS = (
    "app_coupled_heavy_use_enabled",
    "ui_api_behavior_enabled",
    "productization_claim_allowed",
    "customer_ready_output_claim_allowed",
    "ai_approval_authority_allowed",
    "model_owned_state_mutation_allowed",
    "retrieval_as_source_truth_allowed",
)

_PROHIBITED_HARNESS_FIELDS = (
    "raw_prompt",
    "free_form_prompt",
    "untracked_fact",
    "untracked_facts",
    "raw_retrieval_dump",
    "raw_retrieval_chunks",
    "messages",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "api_key",
    "provider_sdk_client",
    "raw_provider_payload",
    "raw_provider_response",
    "model_output",
    "generated_final_output",
    "state_mutation_payload",
    "approval_payload",
    "release_payload",
    "certification_payload",
)


def build_ai_evaluation_harness_baseline() -> dict[str, Any]:
    """Return the M31.7 evaluation/regression baseline."""
    return {
        "checkpoint": AI_EVALUATION_HARNESS_CHECKPOINT_ID,
        "contract_version": AI_EVALUATION_HARNESS_CONTRACT_VERSION,
        "evaluation_harness_status": AI_EVALUATION_HARNESS_STATUS_VALIDATED,
        "supported_regression_case_kinds": list(SUPPORTED_REGRESSION_CASE_KINDS),
        "supported_regression_statuses": list(SUPPORTED_REGRESSION_STATUSES),
        "provider_smoke_default_status": AI_PROVIDER_SMOKE_STATUS_BLOCKED,
        "provider_smoke_policy": (
            "first_provider_or_local_runtime_smoke_must_be_explicitly_enabled_"
            "bounded_evidence_recorded_and_disabled_by_default"
        ),
        "m31_8_boundary": "app_coupled_heavy_use_shakedown_is_deferred_to_m31_8",
        "blocked_scope": [
            "app_coupled_heavy_use_testing_before_m31_8",
            "ui_api_behavior",
            "productization",
            "customer_ready_output",
            "ai_approval_authority",
            "model_owned_state_mutation",
            "retrieval_backed_source_truth",
        ],
    }


def build_ai_regression_case(
    *,
    case_id: str,
    case_kind: str,
    description: str,
    expected_status: str,
    evidence_ref: str,
) -> dict[str, object]:
    """Build and validate a deterministic M31.7 regression case."""
    case = {
        "case_id": _require_non_empty_string(
            case_id,
            field_name="case_id",
            error_prefix="AI regression case",
        ),
        "case_kind": _normalize_supported_value(
            case_kind,
            field_name="case_kind",
            supported_values=SUPPORTED_REGRESSION_CASE_KINDS,
            error_prefix="AI regression case",
        ),
        "description": _require_non_empty_string(
            description,
            field_name="description",
            error_prefix="AI regression case",
        ),
        "expected_status": _normalize_supported_value(
            expected_status,
            field_name="expected_status",
            supported_values=SUPPORTED_REGRESSION_STATUSES,
            error_prefix="AI regression case",
        ),
        "evidence_ref": _require_non_empty_string(
            evidence_ref,
            field_name="evidence_ref",
            error_prefix="AI regression case",
        ),
    }
    validate_ai_regression_case(case)
    return case


def validate_ai_regression_case(case: dict[str, object]) -> None:
    """Validate one M31.7 regression case."""
    _validate_prohibited_fields(case, _PROHIBITED_HARNESS_FIELDS)
    _validate_required_string_fields(
        case,
        _REQUIRED_REGRESSION_CASE_STRING_FIELDS,
        error_prefix="AI regression case",
    )
    _normalize_supported_value(
        case["case_kind"],
        field_name="case_kind",
        supported_values=SUPPORTED_REGRESSION_CASE_KINDS,
        error_prefix="AI regression case",
    )
    _normalize_supported_value(
        case["expected_status"],
        field_name="expected_status",
        supported_values=SUPPORTED_REGRESSION_STATUSES,
        error_prefix="AI regression case",
    )


def build_ai_provider_smoke_request(
    *,
    smoke_request_id: str,
    provider_boundary_request: dict[str, object],
    smoke_kind: str = DISABLED_PROVIDER_SMOKE_KIND,
    enable_provider_smoke: bool = False,
    allow_prompt_execution: bool = False,
) -> dict[str, object]:
    """Build a disabled-by-default provider/local runtime smoke request."""
    validate_ai_provider_adapter_boundary_request(provider_boundary_request)
    smoke_kind = _normalize_supported_value(
        smoke_kind,
        field_name="smoke_kind",
        supported_values=SUPPORTED_PROVIDER_SMOKE_KINDS,
        error_prefix="AI provider smoke request",
    )
    smoke_status = AI_PROVIDER_SMOKE_STATUS_BLOCKED
    if enable_provider_smoke and allow_prompt_execution:
        smoke_status = AI_PROVIDER_SMOKE_STATUS_READY
    elif enable_provider_smoke:
        smoke_status = AI_PROVIDER_SMOKE_STATUS_SKIPPED
    request = {
        "smoke_request_id": _require_non_empty_string(
            smoke_request_id,
            field_name="smoke_request_id",
            error_prefix="AI provider smoke request",
        ),
        "smoke_kind": smoke_kind,
        "smoke_status": smoke_status,
        "provider_boundary_status": str(provider_boundary_request["boundary_status"]),
        "provider_execution_status": str(
            provider_boundary_request["provider_execution_status"]
        ),
        "provider_kind": str(provider_boundary_request["provider_kind"]),
        "enable_provider_smoke": bool(enable_provider_smoke),
        "allow_prompt_execution": bool(allow_prompt_execution),
        "app_coupled_heavy_use_enabled": False,
        "ui_api_behavior_enabled": False,
        "productization_claim_allowed": False,
        "customer_ready_output_claim_allowed": False,
        "ai_approval_authority_allowed": False,
        "model_owned_state_mutation_allowed": False,
        "retrieval_as_source_truth_allowed": False,
        "smoke_policy": "disabled_by_default_explicit_opt_in_required_no_m31_8_heavy_use",
    }
    validate_ai_provider_smoke_request(request)
    return request


def validate_ai_provider_smoke_request(request: dict[str, object]) -> None:
    """Validate a disabled-by-default M31.7 provider/local smoke request."""
    _validate_prohibited_fields(request, _PROHIBITED_HARNESS_FIELDS)
    _validate_required_string_fields(
        request,
        _REQUIRED_SMOKE_REQUEST_STRING_FIELDS,
        error_prefix="AI provider smoke request",
    )
    _validate_expected_exact_value(
        request,
        field_name="provider_boundary_status",
        expected_value=AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
        error_prefix="AI provider smoke request",
    )
    _normalize_supported_value(
        request["provider_kind"],
        field_name="provider_kind",
        supported_values=(DISABLED_PROVIDER_KIND,),
        error_prefix="AI provider smoke request",
    )
    _normalize_supported_value(
        request["smoke_kind"],
        field_name="smoke_kind",
        supported_values=SUPPORTED_PROVIDER_SMOKE_KINDS,
        error_prefix="AI provider smoke request",
    )
    smoke_status = _normalize_supported_value(
        request.get("smoke_status"),
        field_name="smoke_status",
        supported_values=(
            AI_PROVIDER_SMOKE_STATUS_BLOCKED,
            AI_PROVIDER_SMOKE_STATUS_SKIPPED,
            AI_PROVIDER_SMOKE_STATUS_READY,
        ),
        error_prefix="AI provider smoke request",
    )
    if request.get("provider_execution_status") != PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS:
        raise ValueError("M31.7 smoke request must keep provider adapter execution blocked.")
    enable_provider_smoke = _require_bool(
        request.get("enable_provider_smoke"),
        field_name="enable_provider_smoke",
        error_prefix="AI provider smoke request",
    )
    allow_prompt_execution = _require_bool(
        request.get("allow_prompt_execution"),
        field_name="allow_prompt_execution",
        error_prefix="AI provider smoke request",
    )
    for field_name in _REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(f"AI provider smoke request requires {field_name} to be False.")
    if not enable_provider_smoke and smoke_status != AI_PROVIDER_SMOKE_STATUS_BLOCKED:
        raise ValueError("Provider smoke must be blocked unless explicitly enabled.")
    if enable_provider_smoke and not allow_prompt_execution:
        if smoke_status != AI_PROVIDER_SMOKE_STATUS_SKIPPED:
            raise ValueError("Provider smoke must skip unless prompt execution is explicitly allowed.")
    if enable_provider_smoke and allow_prompt_execution:
        if smoke_status != AI_PROVIDER_SMOKE_STATUS_READY:
            raise ValueError("Provider smoke ready status requires explicit smoke and prompt opt-in.")


def build_ai_evaluation_regression_result(
    *,
    evaluation_result_id: str,
    context_packet: dict[str, object],
    refusal_decision: dict[str, object],
    output_review_decision: dict[str, object],
    provider_boundary_request: dict[str, object],
    regression_cases: list[dict[str, object]],
    provider_smoke_request: dict[str, object] | None = None,
) -> dict[str, object]:
    """Build and validate an M31.7 evaluation/regression result."""
    validate_ai_context_packet(context_packet)
    validate_ai_refusal_limitation_decision(refusal_decision)
    validate_ai_output_review_decision(output_review_decision)
    validate_ai_provider_adapter_boundary_request(provider_boundary_request)
    if provider_smoke_request is not None:
        validate_ai_provider_smoke_request(provider_smoke_request)
    result = {
        "checkpoint": AI_EVALUATION_HARNESS_CHECKPOINT_ID,
        "contract_version": AI_EVALUATION_HARNESS_CONTRACT_VERSION,
        "evaluation_result_id": _require_non_empty_string(
            evaluation_result_id,
            field_name="evaluation_result_id",
            error_prefix="AI evaluation regression result",
        ),
        "evaluation_status": AI_EVALUATION_HARNESS_STATUS_VALIDATED,
        "context_packet_id": str(context_packet["context_packet_id"]),
        "refusal_decision_id": str(refusal_decision["refusal_decision_id"]),
        "refusal_limitation_status": str(refusal_decision["refusal_limitation_status"]),
        "output_review_decision_id": str(output_review_decision["review_decision_id"]),
        "output_acceptance_status": str(output_review_decision["output_acceptance_status"]),
        "provider_boundary_status": str(provider_boundary_request["boundary_status"]),
        "provider_execution_status": str(
            provider_boundary_request["provider_execution_status"]
        ),
        "provider_smoke_status": (
            str(provider_smoke_request["smoke_status"])
            if provider_smoke_request is not None
            else AI_PROVIDER_SMOKE_STATUS_BLOCKED
        ),
        "regression_cases": list(regression_cases),
        "provider_smoke_request": (
            dict(provider_smoke_request) if provider_smoke_request is not None else None
        ),
        "app_coupled_heavy_use_enabled": False,
        "ui_api_behavior_enabled": False,
        "productization_claim_allowed": False,
        "customer_ready_output_claim_allowed": False,
        "ai_approval_authority_allowed": False,
        "model_owned_state_mutation_allowed": False,
        "retrieval_as_source_truth_allowed": False,
        "fail_closed_policy": "failed_or_missing_regression_evidence_must_fail_closed",
        "m31_8_boundary": "heavy_use_shakedown_deferred_to_m31_8",
    }
    validate_ai_evaluation_regression_result(result)
    return result


def validate_ai_evaluation_regression_result(result: dict[str, object]) -> None:
    """Validate one M31.7 evaluation/regression result."""
    _validate_prohibited_fields(result, _PROHIBITED_HARNESS_FIELDS)
    _validate_required_string_fields(
        result,
        _REQUIRED_EVALUATION_RESULT_STRING_FIELDS,
        error_prefix="AI evaluation regression result",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_EVALUATION_HARNESS_CHECKPOINT_ID,
        error_prefix="AI evaluation regression result",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_EVALUATION_HARNESS_CONTRACT_VERSION,
        error_prefix="AI evaluation regression result",
    )
    _validate_expected_exact_value(
        result,
        field_name="evaluation_status",
        expected_value=AI_EVALUATION_HARNESS_STATUS_VALIDATED,
        error_prefix="AI evaluation regression result",
    )
    _validate_expected_exact_value(
        result,
        field_name="refusal_limitation_status",
        expected_value=AI_REFUSAL_RULES_STATUS_VALIDATED,
        error_prefix="AI evaluation regression result",
    )
    _validate_expected_exact_value(
        result,
        field_name="output_acceptance_status",
        expected_value=AI_OUTPUT_REVIEW_ACCEPTANCE_STATUS_VALIDATED,
        error_prefix="AI evaluation regression result",
    )
    _validate_expected_exact_value(
        result,
        field_name="provider_boundary_status",
        expected_value=AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
        error_prefix="AI evaluation regression result",
    )
    _validate_expected_exact_value(
        result,
        field_name="provider_execution_status",
        expected_value=PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
        error_prefix="AI evaluation regression result",
    )
    for field_name in _REQUIRED_FALSE_FIELDS:
        if result.get(field_name) is not False:
            raise ValueError(
                "AI evaluation regression result requires "
                f"{field_name} to be False."
            )
    cases = result.get("regression_cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("AI evaluation regression result must declare regression_cases.")
    case_ids: list[str] = []
    case_kinds: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("AI evaluation regression result cases must be dicts.")
        validate_ai_regression_case(case)
        case_ids.append(str(case["case_id"]))
        case_kinds.add(str(case["case_kind"]))
    _reject_duplicates(case_ids, field_name="case_id")
    required_case_kinds = {
        REGRESSION_CASE_CONTEXT_PACKET,
        REGRESSION_CASE_REFUSAL_LIMITATION,
        REGRESSION_CASE_OUTPUT_ACCEPTANCE,
        REGRESSION_CASE_PROVIDER_BOUNDARY,
        REGRESSION_CASE_PROVIDER_SMOKE,
    }
    missing = sorted(required_case_kinds - case_kinds)
    if missing:
        raise ValueError(
            "AI evaluation regression result is missing required case kinds: "
            + ", ".join(missing)
        )
    smoke_request = result.get("provider_smoke_request")
    if smoke_request is not None:
        if not isinstance(smoke_request, dict):
            raise ValueError("provider_smoke_request must be a dict when present.")
        validate_ai_provider_smoke_request(smoke_request)
        if result.get("provider_smoke_status") != smoke_request["smoke_status"]:
            raise ValueError("provider_smoke_status must match provider_smoke_request.")
    else:
        _validate_expected_exact_value(
            result,
            field_name="provider_smoke_status",
            expected_value=AI_PROVIDER_SMOKE_STATUS_BLOCKED,
            error_prefix="AI evaluation regression result",
        )


def _normalize_supported_value(
    value: object,
    *,
    field_name: str,
    supported_values: tuple[str, ...],
    error_prefix: str,
) -> str:
    normalized = _require_non_empty_string(
        value,
        field_name=field_name,
        error_prefix=error_prefix,
    )
    if normalized not in supported_values:
        raise ValueError(
            f"{error_prefix} declares unsupported {field_name}. "
            f"Expected one of: {', '.join(supported_values)}."
        )
    return normalized


def _require_bool(value: object, *, field_name: str, error_prefix: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{error_prefix} must declare boolean {field_name}.")
    return value


def _require_non_empty_string(
    value: object,
    *,
    field_name: str,
    error_prefix: str,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        _require_non_empty_string(
            payload.get(field_name),
            field_name=field_name,
            error_prefix=error_prefix,
        )


def _validate_expected_exact_value(
    payload: dict[str, object],
    *,
    field_name: str,
    expected_value: str,
    error_prefix: str,
) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: "
            f"expected {expected_value!r}, got {actual_value!r}."
        )


def _validate_prohibited_fields(
    payload: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in M31.7 evaluation/regression harness payloads."
            )


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate value in {field_name}: {value!r}.")
        seen.add(value)
