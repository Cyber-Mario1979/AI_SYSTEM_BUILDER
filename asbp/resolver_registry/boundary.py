"Resolver / registry boundary foundation for M14.1."

from __future__ import annotations

from typing import Any

RESOLVER_REGISTRY_BOUNDARY_CHECKPOINT_ID = "M14.1"
RESOLVER_REGISTRY_BOUNDARY_CONTRACT_VERSION = "resolver-registry-boundary-v1"

CORE_RESOLVER_REGISTRY_BOUNDARY = "core_resolver_registry_boundary"
RUNTIME_RESOLVER_REGISTRY_BOUNDARY = "runtime_resolver_registry_boundary"
SUPPORTED_RESOLVER_REGISTRY_BOUNDARIES = (
    CORE_RESOLVER_REGISTRY_BOUNDARY,
    RUNTIME_RESOLVER_REGISTRY_BOUNDARY,
)

CORE_SERVICE_ENTRY_POINT = "core_service"
RUNTIME_SERVICE_ENTRY_POINT = "runtime_service"
CLI_ADAPTER_ENTRY_POINT = "cli_adapter"
SUPPORTED_ASSET_ACCESS_ENTRY_POINTS = (
    CORE_SERVICE_ENTRY_POINT,
    RUNTIME_SERVICE_ENTRY_POINT,
    CLI_ADAPTER_ENTRY_POINT,
)

CLI_ADAPTER_ONLY_POLICY = "cli_may_call_resolver_registry_but_may_not_own_lookup_or_source_truth"
RESOLVER_REGISTRY_ROLE = "governed_asset_access_boundary_only"
DETERMINISTIC_CORE_TRUTH_ROLE = "deterministic_state_or_core_truth_reference_only"
DOWNSTREAM_AI_PRODUCT_ROLE = "downstream_ai_product_surface_only"
RESOLVER_REGISTRY_LAYER_POSITION = "resolver_registry_sits_above_deterministic_core_truth_and_below_ai_product_surfaces"
RESOLVER_REGISTRY_FAILURE_POLICY = "resolver_registry_boundary_fails_closed_on_unsupported_or_bypassed_asset_access"
RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY = "resolver_registry_may_resolve_governed_asset_references_but_must_not_redefine_execution_truth"

TEMPLATE_ASSET_FAMILY = "template"
PRESET_ASSET_FAMILY = "preset"
TASK_POOL_ASSET_FAMILY = "task_pool"
STANDARDS_BUNDLE_ASSET_FAMILY = "standards_bundle"
PROFILE_ASSET_FAMILY = "profile"
CALENDAR_ASSET_FAMILY = "calendar"
PLANNING_BASIS_ASSET_FAMILY = "planning_basis"
MAPPING_METADATA_ASSET_FAMILY = "mapping_metadata"
SUPPORTED_RESOLVABLE_ASSET_FAMILIES = (
    TEMPLATE_ASSET_FAMILY,
    PRESET_ASSET_FAMILY,
    TASK_POOL_ASSET_FAMILY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    PROFILE_ASSET_FAMILY,
    CALENDAR_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
    MAPPING_METADATA_ASSET_FAMILY,
)

_PROHIBITED_ACCESS_FIELDS = (
    "direct_filesystem_lookup",
    "raw_filesystem_path",
    "filesystem_glob",
    "cli_owned_lookup",
    "ai_owned_source_truth",
    "ui_owned_lookup",
    "api_owned_lookup",
    "renderer_owned_lookup",
    "state_bypass",
    "persistence_bypass",
    "resolver_bypass",
    "execution_truth_override",
    "source_truth_override",
    "unvalidated_asset_payload",
)

_REQUIRED_ACCESS_REQUEST_FIELDS = (
    "checkpoint",
    "contract_version",
    "access_request_id",
    "access_boundary",
    "entry_point",
    "requested_asset_family",
    "requested_asset_ref",
    "caller_context_ref",
    "resolver_registry_role",
    "layer_position",
    "source_truth_policy",
    "failure_policy",
    "adapter_policy",
)


def build_resolver_registry_boundary_baseline() -> dict[str, Any]:
    return {
        "checkpoint": RESOLVER_REGISTRY_BOUNDARY_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_BOUNDARY_CONTRACT_VERSION,
        "supported_boundaries": list(SUPPORTED_RESOLVER_REGISTRY_BOUNDARIES),
        "supported_entry_points": list(SUPPORTED_ASSET_ACCESS_ENTRY_POINTS),
        "supported_resolvable_asset_families": list(SUPPORTED_RESOLVABLE_ASSET_FAMILIES),
        "resolver_registry_role": RESOLVER_REGISTRY_ROLE,
        "deterministic_core_truth_role": DETERMINISTIC_CORE_TRUTH_ROLE,
        "downstream_ai_product_role": DOWNSTREAM_AI_PRODUCT_ROLE,
        "layer_position": RESOLVER_REGISTRY_LAYER_POSITION,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "failure_policy": RESOLVER_REGISTRY_FAILURE_POLICY,
        "cli_adapter_policy": CLI_ADAPTER_ONLY_POLICY,
        "prohibited_access_fields": list(_PROHIBITED_ACCESS_FIELDS),
        "required_access_request_fields": list(_REQUIRED_ACCESS_REQUEST_FIELDS),
        "boundary_policy": "m14_1_defines_asset_access_entry_points_only_not_versioned_asset_lookup",
        "not_yet_implemented": [
            "version_pinned_asset_identity_lookup",
            "calendar_resolution_execution",
            "authored_source_vs_compiled_runtime_lookup",
            "support_retrieval_boundary",
            "ui_api_delivery",
            "ai_retrieval_consumption",
        ],
    }


def build_resolver_registry_access_request(
    *,
    access_request_id: str,
    access_boundary: str,
    entry_point: str,
    requested_asset_family: str,
    requested_asset_ref: str,
    caller_context_ref: str,
) -> dict[str, Any]:
    request = {
        "checkpoint": RESOLVER_REGISTRY_BOUNDARY_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_BOUNDARY_CONTRACT_VERSION,
        "access_request_id": access_request_id,
        "access_boundary": access_boundary,
        "entry_point": entry_point,
        "requested_asset_family": requested_asset_family,
        "requested_asset_ref": requested_asset_ref,
        "caller_context_ref": caller_context_ref,
        "resolver_registry_role": RESOLVER_REGISTRY_ROLE,
        "layer_position": RESOLVER_REGISTRY_LAYER_POSITION,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "failure_policy": RESOLVER_REGISTRY_FAILURE_POLICY,
        "adapter_policy": CLI_ADAPTER_ONLY_POLICY,
    }
    validate_resolver_registry_access_request(request)
    return request


def validate_resolver_registry_access_request(request: dict[str, object]) -> None:
    _validate_prohibited_fields(request, _PROHIBITED_ACCESS_FIELDS)
    for field_name in _REQUIRED_ACCESS_REQUEST_FIELDS:
        if field_name not in request:
            raise ValueError(f"Resolver registry access request must declare {field_name}.")

    _validate_required_string_fields(
        request,
        _REQUIRED_ACCESS_REQUEST_FIELDS,
        error_prefix="Resolver registry access request",
    )
    _validate_expected_exact_value(
        request,
        field_name="checkpoint",
        expected_value=RESOLVER_REGISTRY_BOUNDARY_CHECKPOINT_ID,
        error_prefix="Resolver registry access request",
    )
    _validate_expected_exact_value(
        request,
        field_name="contract_version",
        expected_value=RESOLVER_REGISTRY_BOUNDARY_CONTRACT_VERSION,
        error_prefix="Resolver registry access request",
    )
    _validate_expected_exact_value(
        request,
        field_name="resolver_registry_role",
        expected_value=RESOLVER_REGISTRY_ROLE,
        error_prefix="Resolver registry access request",
    )
    _validate_expected_exact_value(
        request,
        field_name="layer_position",
        expected_value=RESOLVER_REGISTRY_LAYER_POSITION,
        error_prefix="Resolver registry access request",
    )
    _validate_expected_exact_value(
        request,
        field_name="source_truth_policy",
        expected_value=RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        error_prefix="Resolver registry access request",
    )
    _validate_expected_exact_value(
        request,
        field_name="failure_policy",
        expected_value=RESOLVER_REGISTRY_FAILURE_POLICY,
        error_prefix="Resolver registry access request",
    )
    _validate_expected_exact_value(
        request,
        field_name="adapter_policy",
        expected_value=CLI_ADAPTER_ONLY_POLICY,
        error_prefix="Resolver registry access request",
    )

    _validate_supported_access_boundary(str(request["access_boundary"]))
    _validate_supported_entry_point(str(request["entry_point"]))
    _validate_supported_asset_family(str(request["requested_asset_family"]))


def _validate_supported_access_boundary(access_boundary: str) -> None:
    if access_boundary not in SUPPORTED_RESOLVER_REGISTRY_BOUNDARIES:
        raise ValueError(
            "Unsupported resolver registry access boundary. "
            f"Expected one of: {', '.join(SUPPORTED_RESOLVER_REGISTRY_BOUNDARIES)}."
        )


def _validate_supported_entry_point(entry_point: str) -> None:
    if entry_point not in SUPPORTED_ASSET_ACCESS_ENTRY_POINTS:
        raise ValueError(
            "Unsupported resolver registry entry point. "
            f"Expected one of: {', '.join(SUPPORTED_ASSET_ACCESS_ENTRY_POINTS)}."
        )


def _validate_supported_asset_family(asset_family: str) -> None:
    if asset_family not in SUPPORTED_RESOLVABLE_ASSET_FAMILIES:
        raise ValueError(
            "Unsupported resolver registry asset family. "
            f"Expected one of: {', '.join(SUPPORTED_RESOLVABLE_ASSET_FAMILIES)}."
        )


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        value = payload.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")


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
                f"{field_name} is not allowed in resolver registry boundary requests."
            )
