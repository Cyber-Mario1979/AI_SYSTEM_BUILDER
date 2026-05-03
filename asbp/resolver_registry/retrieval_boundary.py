"Governed retrieval versus support-retrieval boundary for M14.5."

from __future__ import annotations

from typing import Any

from .boundary import RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY
from .source_compilation import (
    COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
    DEPLOYMENT_COMPILED_LOOKUP_ROLE,
    validate_deployment_compiled_lookup_record,
)

RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID = "M14.5"
RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION = "governed-retrieval-support-boundary-v1"

GOVERNED_DETERMINISTIC_RETRIEVAL_MODE = "governed_deterministic_retrieval"
SUPPORT_RETRIEVAL_MODE = "support_retrieval"
GOVERNED_RETRIEVAL_ROLE = "governed_version_pinned_retrieval_only"
SUPPORT_RETRIEVAL_ROLE = "non_authoritative_support_retrieval_only"
GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY = "governed_retrieval_preserves_existing_authored_source_and_compiled_lookup_roles"
SUPPORT_RETRIEVAL_SOURCE_AUTHORITY_POLICY = "support_retrieval_may_provide_context_but_must_not_define_source_or_execution_truth"
SUPPORT_RETRIEVAL_AI_COMPATIBILITY_POLICY = "support_retrieval_may_be_consumed_by_later_ai_workflows_only_as_non_authoritative_context"
RETRIEVAL_BOUNDARY_FAILURE_POLICY = "retrieval_boundary_fails_closed_on_unsupported_mode_authority_override_or_mixed_source_roles"
RETRIEVAL_BOUNDARY_CONTENT_POLICY = "m14_5_defines_retrieval_role_boundary_only_not_asset_payload_loading_search_execution_or_ai_runtime"

_GOVERNED_REQUIRED = (
    "checkpoint", "contract_version", "retrieval_mode", "caller_context_ref",
    "lookup_key", "asset_family", "asset_id", "asset_version", "asset_ref",
    "compiled_record_ref", "compiled_surface_id", "source_record_ref",
    "compiled_lookup_role", "retrieval_role", "source_truth_policy",
    "source_authority_policy", "support_retrieval_policy", "failure_policy",
    "content_policy",
)
_SUPPORT_REQUIRED = (
    "checkpoint", "contract_version", "retrieval_mode", "support_request_id",
    "query_text", "support_context_ref", "caller_context_ref", "retrieval_role",
    "source_truth_policy", "source_authority_policy", "ai_compatibility_policy",
    "failure_policy", "content_policy",
)
_GOVERNED_PROHIBITED = (
    "support_query_text", "support_search_scope", "support_search_results",
    "probabilistic_score", "vector_embedding", "source_truth_override",
    "execution_truth_override", "support_retrieval_as_source_truth",
    "asset_payload", "unvalidated_asset_payload", "ai_owned_source_truth",
    "ui_owned_source_truth", "external_web_search",
)
_SUPPORT_PROHIBITED = (
    "asset_family", "asset_id", "asset_version", "asset_ref", "lookup_key",
    "governed_lookup_key", "compiled_record_ref", "compiled_surface_id",
    "source_record_ref", "compiled_lookup_role", "compiled_authority",
    "compiled_source_authority", "source_truth_override", "execution_truth_override",
    "support_retrieval_as_source_truth", "support_retrieval_as_execution_truth",
    "asset_payload", "unvalidated_asset_payload", "ai_owned_source_truth",
    "ui_owned_source_truth", "resolver_bypass",
)


def build_retrieval_boundary_baseline() -> dict[str, Any]:
    return {
        "checkpoint": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION,
        "retrieval_modes": [GOVERNED_DETERMINISTIC_RETRIEVAL_MODE, SUPPORT_RETRIEVAL_MODE],
        "governed_retrieval_role": GOVERNED_RETRIEVAL_ROLE,
        "support_retrieval_role": SUPPORT_RETRIEVAL_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "governed_source_authority_policy": GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
        "support_source_authority_policy": SUPPORT_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
        "support_ai_compatibility_policy": SUPPORT_RETRIEVAL_AI_COMPATIBILITY_POLICY,
        "compiled_lookup_not_source_authority_policy": COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
        "failure_policy": RETRIEVAL_BOUNDARY_FAILURE_POLICY,
        "content_policy": RETRIEVAL_BOUNDARY_CONTENT_POLICY,
        "owned_by_m14_5": [
            "governed_deterministic_retrieval_role",
            "support_retrieval_role",
            "support_retrieval_non_authority_validation",
            "future_ai_retrieval_compatibility_boundary",
        ],
        "not_owned_by_m14_5": [
            "vector_search_execution", "embedding_generation", "external_web_search",
            "ai_runtime_retrieval_consumption", "asset_payload_loading",
            "document_generation", "ui_api_adapter_work",
        ],
    }


def build_governed_retrieval_request_from_compiled_lookup(*, deployment_compiled_record: dict[str, object], caller_context_ref: str) -> dict[str, object]:
    validate_deployment_compiled_lookup_record(deployment_compiled_record)
    request = {
        "checkpoint": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION,
        "retrieval_mode": GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
        "caller_context_ref": _require_non_empty_string(caller_context_ref, "caller_context_ref", "Governed retrieval request"),
        "lookup_key": deployment_compiled_record["lookup_key"],
        "asset_family": deployment_compiled_record["asset_family"],
        "asset_id": deployment_compiled_record["asset_id"],
        "asset_version": deployment_compiled_record["asset_version"],
        "asset_ref": deployment_compiled_record["asset_ref"],
        "compiled_record_ref": deployment_compiled_record["compiled_record_ref"],
        "compiled_surface_id": deployment_compiled_record["compiled_surface_id"],
        "source_record_ref": deployment_compiled_record["source_record_ref"],
        "compiled_lookup_role": DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        "retrieval_role": GOVERNED_RETRIEVAL_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "source_authority_policy": GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
        "support_retrieval_policy": "support_retrieval_not_used_for_governed_lookup_authority",
        "failure_policy": RETRIEVAL_BOUNDARY_FAILURE_POLICY,
        "content_policy": RETRIEVAL_BOUNDARY_CONTENT_POLICY,
        "asset_payload_included": False,
        "support_retrieval_used": False,
    }
    validate_governed_retrieval_request(request)
    return request


def build_support_retrieval_request(*, support_request_id: str, query_text: str, support_context_ref: str, caller_context_ref: str) -> dict[str, object]:
    request = {
        "checkpoint": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION,
        "retrieval_mode": SUPPORT_RETRIEVAL_MODE,
        "support_request_id": _require_non_empty_string(support_request_id, "support_request_id", "Support retrieval request"),
        "query_text": _require_non_empty_string(query_text, "query_text", "Support retrieval request"),
        "support_context_ref": _require_non_empty_string(support_context_ref, "support_context_ref", "Support retrieval request"),
        "caller_context_ref": _require_non_empty_string(caller_context_ref, "caller_context_ref", "Support retrieval request"),
        "retrieval_role": SUPPORT_RETRIEVAL_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "source_authority_policy": SUPPORT_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
        "ai_compatibility_policy": SUPPORT_RETRIEVAL_AI_COMPATIBILITY_POLICY,
        "failure_policy": RETRIEVAL_BOUNDARY_FAILURE_POLICY,
        "content_policy": RETRIEVAL_BOUNDARY_CONTENT_POLICY,
        "governed_lookup_authority": False,
        "execution_truth_authority": False,
        "compiled_lookup_authority": False,
        "asset_payload_included": False,
    }
    validate_support_retrieval_request(request)
    return request


def validate_retrieval_boundary_request(request: dict[str, object]) -> None:
    mode = request.get("retrieval_mode")
    if mode == GOVERNED_DETERMINISTIC_RETRIEVAL_MODE:
        validate_governed_retrieval_request(request)
        return
    if mode == SUPPORT_RETRIEVAL_MODE:
        validate_support_retrieval_request(request)
        return
    raise ValueError("Unsupported resolver registry retrieval mode. Expected one of: governed_deterministic_retrieval, support_retrieval.")


def validate_governed_retrieval_request(request: dict[str, object]) -> None:
    _validate_prohibited(request, _GOVERNED_PROHIBITED)
    _validate_required(request, _GOVERNED_REQUIRED, "Governed retrieval request")
    _exact(request, "checkpoint", RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID, "Governed retrieval request")
    _exact(request, "contract_version", RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION, "Governed retrieval request")
    _exact(request, "retrieval_mode", GOVERNED_DETERMINISTIC_RETRIEVAL_MODE, "Governed retrieval request")
    _exact(request, "compiled_lookup_role", DEPLOYMENT_COMPILED_LOOKUP_ROLE, "Governed retrieval request")
    _exact(request, "retrieval_role", GOVERNED_RETRIEVAL_ROLE, "Governed retrieval request")
    _exact(request, "source_truth_policy", RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY, "Governed retrieval request")
    _exact(request, "source_authority_policy", GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY, "Governed retrieval request")
    _exact(request, "failure_policy", RETRIEVAL_BOUNDARY_FAILURE_POLICY, "Governed retrieval request")
    _exact(request, "content_policy", RETRIEVAL_BOUNDARY_CONTENT_POLICY, "Governed retrieval request")
    if bool(request.get("asset_payload_included")) is not False:
        raise ValueError("Governed retrieval request must not include asset payload.")
    if bool(request.get("support_retrieval_used")) is not False:
        raise ValueError("Governed retrieval request must not use support retrieval.")


def validate_support_retrieval_request(request: dict[str, object]) -> None:
    _validate_prohibited(request, _SUPPORT_PROHIBITED)
    _validate_required(request, _SUPPORT_REQUIRED, "Support retrieval request")
    _exact(request, "checkpoint", RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID, "Support retrieval request")
    _exact(request, "contract_version", RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION, "Support retrieval request")
    _exact(request, "retrieval_mode", SUPPORT_RETRIEVAL_MODE, "Support retrieval request")
    _exact(request, "retrieval_role", SUPPORT_RETRIEVAL_ROLE, "Support retrieval request")
    _exact(request, "source_truth_policy", RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY, "Support retrieval request")
    _exact(request, "source_authority_policy", SUPPORT_RETRIEVAL_SOURCE_AUTHORITY_POLICY, "Support retrieval request")
    _exact(request, "ai_compatibility_policy", SUPPORT_RETRIEVAL_AI_COMPATIBILITY_POLICY, "Support retrieval request")
    _exact(request, "failure_policy", RETRIEVAL_BOUNDARY_FAILURE_POLICY, "Support retrieval request")
    _exact(request, "content_policy", RETRIEVAL_BOUNDARY_CONTENT_POLICY, "Support retrieval request")
    for field in ("governed_lookup_authority", "execution_truth_authority", "compiled_lookup_authority", "asset_payload_included"):
        if bool(request.get(field)) is not False:
            raise ValueError(f"Support retrieval request must keep {field} false.")


def _require_non_empty_string(value: object, field_name: str, error_prefix: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")
    return value.strip()


def _validate_required(payload: dict[str, object], required_fields: tuple[str, ...], error_prefix: str) -> None:
    for field in required_fields:
        _require_non_empty_string(payload.get(field), field, error_prefix)


def _exact(payload: dict[str, object], field_name: str, expected_value: str, error_prefix: str) -> None:
    actual = payload.get(field_name)
    if actual != expected_value:
        raise ValueError(f"{error_prefix} declares an invalid {field_name}: expected {expected_value!r}, got {actual!r}.")


def _validate_prohibited(payload: dict[str, object], prohibited_fields: tuple[str, ...]) -> None:
    for field in prohibited_fields:
        if field in payload:
            raise ValueError(f"{field} is not allowed in this retrieval boundary mode.")
