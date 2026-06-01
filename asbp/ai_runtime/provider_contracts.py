"Provider adapter boundary contracts for M31.3 governed AI assistance."

from __future__ import annotations

from typing import Any

AI_PROVIDER_ADAPTER_BOUNDARY_CHECKPOINT_ID = "M31.3"
AI_PROVIDER_ADAPTER_BOUNDARY_CONTRACT_VERSION = "ai-provider-adapter-boundary-v1"
AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED = "provider_adapter_boundary_validated"

AI_RUNTIME_BOUNDARY_CALLER = "ai_runtime_boundary"
ORCHESTRATION_SERVICE_CALLER_BOUNDARY = "orchestration_service_boundary"
SUPPORTED_PROVIDER_ADAPTER_CALLER_BOUNDARIES = (
    AI_RUNTIME_BOUNDARY_CALLER,
    ORCHESTRATION_SERVICE_CALLER_BOUNDARY,
)

DISABLED_PROVIDER_KIND = "disabled"
LOCAL_OFFLINE_PROVIDER_KIND = "local_offline_runtime"
EXTERNAL_API_PROVIDER_KIND = "external_api_provider"
SUPPORTED_PROVIDER_KINDS = (
    DISABLED_PROVIDER_KIND,
    LOCAL_OFFLINE_PROVIDER_KIND,
    EXTERNAL_API_PROVIDER_KIND,
)
IMPLEMENTATION_BLOCKED_PROVIDER_KINDS = (
    LOCAL_OFFLINE_PROVIDER_KIND,
    EXTERNAL_API_PROVIDER_KIND,
)

PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS = "execution_blocked_until_later_checkpoint"
DISABLED_BOUNDARY_ONLY_IMPLEMENTATION_STATUS = "disabled_boundary_only"
STRATEGY_CANDIDATE_ONLY_IMPLEMENTATION_STATUS = "strategy_candidate_only"

_PROHIBITED_PROVIDER_FIELDS = (
    "api_key",
    "provider_api_key",
    "secret",
    "token",
    "access_token",
    "raw_prompt",
    "prompt",
    "messages",
    "model_name",
    "provider_sdk_client",
    "provider_response",
    "raw_provider_response",
    "raw_provider_payload",
    "local_model_path",
    "inference_result",
    "completion",
    "embedding_request",
    "vector_store_request",
)

_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "adapter_request_id",
    "caller_boundary",
    "provider_kind",
    "provider_execution_status",
    "provider_implementation_status",
    "boundary_status",
)

_REQUIRED_FALSE_FIELDS = (
    "direct_model_call_enabled",
    "prompt_execution_enabled",
    "provider_credentials_present",
    "raw_provider_payload_allowed",
    "raw_provider_response_leakage_allowed",
    "model_state_mutation_allowed",
    "core_ui_direct_call_allowed",
    "autonomous_execution_allowed",
    "retrieval_as_source_truth_allowed",
    "ai_approval_authority_allowed",
)

_REQUIRED_TRUE_DEPENDENCY_FIELDS = (
    "context_packet_contract_required",
    "refusal_limitation_rules_required",
    "output_acceptance_rules_required",
    "evaluation_validation_required",
)


def build_ai_provider_adapter_boundary_baseline() -> dict[str, Any]:
    """Return M31.3 provider/adapter boundary rules."""
    return {
        "checkpoint": AI_PROVIDER_ADAPTER_BOUNDARY_CHECKPOINT_ID,
        "contract_version": AI_PROVIDER_ADAPTER_BOUNDARY_CONTRACT_VERSION,
        "boundary_status": AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
        "supported_caller_boundaries": list(
            SUPPORTED_PROVIDER_ADAPTER_CALLER_BOUNDARIES
        ),
        "supported_provider_kinds": list(SUPPORTED_PROVIDER_KINDS),
        "implementation_blocked_provider_kinds": list(
            IMPLEMENTATION_BLOCKED_PROVIDER_KINDS
        ),
        "allowed_m31_3_build_scope": [
            "provider_neutral_boundary_contracts",
            "disabled_adapter_boundary",
            "adapter_registry_shape",
            "boundary_validation_tests",
        ],
        "blocked_m31_3_runtime_scope": [
            "real_provider_calls",
            "local_model_inference",
            "prompt_execution",
            "api_key_handling",
            "provider_sdk_integration",
            "embedding_or_vector_store_execution",
            "app_coupled_heavy_use_testing",
        ],
        "boundary_rules": [
            "no_direct_model_calls_from_core_or_ui",
            "no_raw_provider_payload_leakage",
            "no_model_owned_state_mutation",
            "no_ai_approval_authority",
            "context_packets_required_before_model_input",
            "refusal_and_limitation_rules_required_before_execution",
            "output_acceptance_required_before_ai_output_acceptance",
            "evaluation_required_before_behavior_readiness_claims",
        ],
    }


def build_ai_provider_adapter_boundary_request(
    *,
    adapter_request_id: str,
    provider_kind: str = DISABLED_PROVIDER_KIND,
    caller_boundary: str = AI_RUNTIME_BOUNDARY_CALLER,
) -> dict[str, object]:
    """Build and validate an M31.3 provider adapter boundary request."""
    normalized_provider_kind = _normalize_supported_value(
        provider_kind,
        field_name="provider_kind",
        supported_values=SUPPORTED_PROVIDER_KINDS,
        error_prefix="AI provider adapter boundary request",
    )
    request = {
        "checkpoint": AI_PROVIDER_ADAPTER_BOUNDARY_CHECKPOINT_ID,
        "contract_version": AI_PROVIDER_ADAPTER_BOUNDARY_CONTRACT_VERSION,
        "adapter_request_id": _require_non_empty_string(
            adapter_request_id,
            field_name="adapter_request_id",
            error_prefix="AI provider adapter boundary request",
        ),
        "caller_boundary": _normalize_supported_value(
            caller_boundary,
            field_name="caller_boundary",
            supported_values=SUPPORTED_PROVIDER_ADAPTER_CALLER_BOUNDARIES,
            error_prefix="AI provider adapter boundary request",
        ),
        "provider_kind": normalized_provider_kind,
        "provider_execution_status": PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
        "provider_implementation_status": _implementation_status_for_provider_kind(
            normalized_provider_kind
        ),
        "boundary_status": AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
        "direct_model_call_enabled": False,
        "prompt_execution_enabled": False,
        "provider_credentials_present": False,
        "raw_provider_payload_allowed": False,
        "raw_provider_response_leakage_allowed": False,
        "model_state_mutation_allowed": False,
        "core_ui_direct_call_allowed": False,
        "autonomous_execution_allowed": False,
        "retrieval_as_source_truth_allowed": False,
        "ai_approval_authority_allowed": False,
        "context_packet_contract_required": True,
        "refusal_limitation_rules_required": True,
        "output_acceptance_rules_required": True,
        "evaluation_validation_required": True,
        "provider_boundary_policy": "provider_behavior_must_attach_only_behind_adapter_boundary",
        "state_mutation_policy": "model_output_cannot_mutate_state",
        "payload_policy": "raw_provider_payloads_must_not_cross_core_boundary",
    }
    validate_ai_provider_adapter_boundary_request(request)
    return request


def validate_ai_provider_adapter_boundary_request(request: dict[str, object]) -> None:
    """Validate that a provider adapter request remains inside M31.3 boundaries."""
    _validate_prohibited_fields(request, _PROHIBITED_PROVIDER_FIELDS)
    _validate_required_string_fields(
        request,
        _REQUIRED_STRING_FIELDS,
        error_prefix="AI provider adapter boundary request",
    )
    _validate_expected_exact_value(
        request,
        field_name="checkpoint",
        expected_value=AI_PROVIDER_ADAPTER_BOUNDARY_CHECKPOINT_ID,
        error_prefix="AI provider adapter boundary request",
    )
    _validate_expected_exact_value(
        request,
        field_name="contract_version",
        expected_value=AI_PROVIDER_ADAPTER_BOUNDARY_CONTRACT_VERSION,
        error_prefix="AI provider adapter boundary request",
    )
    _validate_expected_exact_value(
        request,
        field_name="provider_execution_status",
        expected_value=PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
        error_prefix="AI provider adapter boundary request",
    )
    _validate_expected_exact_value(
        request,
        field_name="boundary_status",
        expected_value=AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
        error_prefix="AI provider adapter boundary request",
    )

    provider_kind = _normalize_supported_value(
        request["provider_kind"],
        field_name="provider_kind",
        supported_values=SUPPORTED_PROVIDER_KINDS,
        error_prefix="AI provider adapter boundary request",
    )
    _normalize_supported_value(
        request["caller_boundary"],
        field_name="caller_boundary",
        supported_values=SUPPORTED_PROVIDER_ADAPTER_CALLER_BOUNDARIES,
        error_prefix="AI provider adapter boundary request",
    )
    _validate_expected_exact_value(
        request,
        field_name="provider_implementation_status",
        expected_value=_implementation_status_for_provider_kind(provider_kind),
        error_prefix="AI provider adapter boundary request",
    )

    for field_name in _REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(
                "AI provider adapter boundary request requires "
                f"{field_name} to be False."
            )

    for field_name in _REQUIRED_TRUE_DEPENDENCY_FIELDS:
        if request.get(field_name) is not True:
            raise ValueError(
                "AI provider adapter boundary request requires "
                f"{field_name} to be True."
            )


def validate_ai_provider_adapter_blocked_state(request: dict[str, object]) -> None:
    """Validate that no real provider/model execution state is present."""
    validate_ai_provider_adapter_boundary_request(request)


def _implementation_status_for_provider_kind(provider_kind: str) -> str:
    if provider_kind == DISABLED_PROVIDER_KIND:
        return DISABLED_BOUNDARY_ONLY_IMPLEMENTATION_STATUS
    return STRATEGY_CANDIDATE_ONLY_IMPLEMENTATION_STATUS


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
                f"{field_name} is not allowed in M31.3 provider adapter boundary requests."
            )
