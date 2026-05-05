"Governed library service hardening for M15.7."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

from .library_release_validation import (
    RELEASE_STATUS_FREEZE_CANDIDATE,
    RELEASE_STATUS_FROZEN_RELEASED,
    RELEASE_STATUS_VALIDATION_CANDIDATE,
    validate_library_release_manifest,
)

GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID = "M15.7"
GOVERNED_LIBRARY_SERVICE_HARDENING_CONTRACT_VERSION = (
    "governed-library-service-hardening-v1"
)

PREFLIGHT_VALIDATION_STATUS_VALIDATED = "m15_6_release_manifest_validated"

SERVICE_CALLER_BOUNDARY_CORE = "core_service_boundary"
SERVICE_CALLER_BOUNDARY_ORCHESTRATION = "orchestration_service_boundary"
SERVICE_CALLER_BOUNDARY_DOCUMENT_ENGINE = "document_engine_boundary"
SERVICE_CALLER_BOUNDARY_EXPORT_ENGINE = "export_engine_boundary"
SUPPORTED_SERVICE_CALLER_BOUNDARIES = (
    SERVICE_CALLER_BOUNDARY_CORE,
    SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
    SERVICE_CALLER_BOUNDARY_DOCUMENT_ENGINE,
    SERVICE_CALLER_BOUNDARY_EXPORT_ENGINE,
)

SERVICE_ENTRY_POINT_CORE = "core_service"
SERVICE_ENTRY_POINT_ORCHESTRATION = "orchestration_service"
SERVICE_ENTRY_POINT_DOCUMENT_ENGINE = "document_engine_service"
SERVICE_ENTRY_POINT_EXPORT_ENGINE = "export_engine_service"
SUPPORTED_SERVICE_ENTRY_POINTS = (
    SERVICE_ENTRY_POINT_CORE,
    SERVICE_ENTRY_POINT_ORCHESTRATION,
    SERVICE_ENTRY_POINT_DOCUMENT_ENGINE,
    SERVICE_ENTRY_POINT_EXPORT_ENGINE,
)

OPERATION_VALIDATE_LIBRARY_PREFLIGHT = "validate_library_preflight"
OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT = "resolve_governed_asset_context"
OPERATION_PREPARE_SERVICE_CONTEXT = "prepare_service_context"
OPERATION_PREPARE_DOCUMENT_INVOCATION_CONTEXT = "prepare_document_invocation_context"
OPERATION_PREPARE_EXPORT_INVOCATION_CONTEXT = "prepare_export_invocation_context"
SUPPORTED_SERVICE_OPERATIONS = (
    OPERATION_VALIDATE_LIBRARY_PREFLIGHT,
    OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT,
    OPERATION_PREPARE_SERVICE_CONTEXT,
    OPERATION_PREPARE_DOCUMENT_INVOCATION_CONTEXT,
    OPERATION_PREPARE_EXPORT_INVOCATION_CONTEXT,
)

ALLOWED_PREFLIGHT_RELEASE_STATUSES = (
    RELEASE_STATUS_VALIDATION_CANDIDATE,
    RELEASE_STATUS_FREEZE_CANDIDATE,
    RELEASE_STATUS_FROZEN_RELEASED,
)

_PROHIBITED_SERVICE_FIELDS = (
    "direct_filesystem_lookup",
    "raw_filesystem_path",
    "filesystem_glob",
    "cli_owned_lookup",
    "ui_owned_lookup",
    "ai_owned_source_truth",
    "support_retrieval_source_truth_override",
    "runtime_authority_override",
    "compiled_lookup_as_source_truth",
    "source_truth_override",
    "execution_truth_override",
)

_REQUIRED_SERVICE_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "service_request_id",
    "caller_boundary",
    "entry_point",
    "requested_operation",
    "release_manifest_ref",
    "release_status",
    "preflight_validation_status",
)

_REQUIRED_SERVICE_LIST_FIELDS = (
    "requested_asset_refs",
    "declared_release_refs",
)

_REQUIRED_SERVICE_FALSE_FIELDS = (
    "runtime_migration_requested",
    "deployment_compilation_requested",
    "support_retrieval_can_define_source_truth",
    "adapter_owns_lookup",
    "free_form_mutation_requested",
)


def build_library_service_hardening_baseline() -> dict[str, Any]:
    """Return the M15.7 governed library service hardening baseline."""
    return {
        "checkpoint": GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_SERVICE_HARDENING_CONTRACT_VERSION,
        "supported_caller_boundaries": list(SUPPORTED_SERVICE_CALLER_BOUNDARIES),
        "supported_entry_points": list(SUPPORTED_SERVICE_ENTRY_POINTS),
        "supported_operations": list(SUPPORTED_SERVICE_OPERATIONS),
        "allowed_preflight_release_statuses": list(ALLOWED_PREFLIGHT_RELEASE_STATUSES),
        "preflight_validation_status": PREFLIGHT_VALIDATION_STATUS_VALIDATED,
        "adapter_leakage_policy": "adapters_may_request_service_context_but_must_not_own_lookup_or_source_truth",
        "runtime_migration_policy": "runtime_migration_is_blocked_in_m15_7",
        "deployment_compilation_policy": "deployment_compiled_lookup_generation_is_blocked_in_m15_7",
        "support_retrieval_policy": "support_retrieval_must_not_define_source_truth",
        "document_export_policy": "document_and_export_context_may_be_prepared_only_after_governed_library_preflight_passes",
        "not_owned_by_m15_7": [
            "cli command implementation",
            "runtime migration",
            "deployment compiled lookup generation",
            "actual document generation",
            "actual export generation",
            "ai runtime behavior",
            "m15_8_validation_checkpoint_closure",
            "m15_9_uat",
            "m15_10_closeout",
        ],
    }


def build_governed_library_service_request(
    *,
    service_request_id: str,
    caller_boundary: str,
    entry_point: str,
    requested_operation: str,
    release_manifest: dict[str, object],
    requested_asset_refs: list[str],
) -> dict[str, object]:
    """Build and validate a governed-library service request."""
    validate_library_release_manifest(release_manifest)
    declared_refs = _collect_manifest_refs(release_manifest)
    request = {
        "checkpoint": GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_SERVICE_HARDENING_CONTRACT_VERSION,
        "service_request_id": _require_non_empty_string(
            service_request_id,
            field_name="service_request_id",
            error_prefix="Governed library service request",
        ),
        "caller_boundary": _normalize_supported_value(
            caller_boundary,
            field_name="caller_boundary",
            supported_values=SUPPORTED_SERVICE_CALLER_BOUNDARIES,
            error_prefix="Governed library service request",
        ),
        "entry_point": _normalize_supported_value(
            entry_point,
            field_name="entry_point",
            supported_values=SUPPORTED_SERVICE_ENTRY_POINTS,
            error_prefix="Governed library service request",
        ),
        "requested_operation": _normalize_supported_value(
            requested_operation,
            field_name="requested_operation",
            supported_values=SUPPORTED_SERVICE_OPERATIONS,
            error_prefix="Governed library service request",
        ),
        "release_manifest_ref": str(release_manifest["release_manifest_ref"]),
        "release_status": str(release_manifest["release_status"]),
        "preflight_validation_status": PREFLIGHT_VALIDATION_STATUS_VALIDATED,
        "requested_asset_refs": list(requested_asset_refs),
        "declared_release_refs": sorted(declared_refs),
        "runtime_migration_requested": False,
        "deployment_compilation_requested": False,
        "support_retrieval_can_define_source_truth": False,
        "adapter_owns_lookup": False,
        "free_form_mutation_requested": False,
        "source_role_policy": "governed_library_service_consumes_validated_release_refs_only",
        "mutation_policy": "no_canvas_state_or_runtime_mutation_is_performed_by_m15_7_preflight",
    }
    validate_governed_library_service_request(request)
    return request


def validate_governed_library_service_request(
    request: dict[str, object],
) -> None:
    """Validate an M15.7 governed-library service request."""
    _validate_prohibited_fields(request, _PROHIBITED_SERVICE_FIELDS)
    _validate_required_string_fields(
        request,
        _REQUIRED_SERVICE_STRING_FIELDS,
        error_prefix="Governed library service request",
    )
    _validate_expected_exact_value(
        request,
        field_name="checkpoint",
        expected_value=GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID,
        error_prefix="Governed library service request",
    )
    _validate_expected_exact_value(
        request,
        field_name="contract_version",
        expected_value=GOVERNED_LIBRARY_SERVICE_HARDENING_CONTRACT_VERSION,
        error_prefix="Governed library service request",
    )
    _validate_expected_exact_value(
        request,
        field_name="preflight_validation_status",
        expected_value=PREFLIGHT_VALIDATION_STATUS_VALIDATED,
        error_prefix="Governed library service request",
    )

    _normalize_supported_value(
        str(request["caller_boundary"]),
        field_name="caller_boundary",
        supported_values=SUPPORTED_SERVICE_CALLER_BOUNDARIES,
        error_prefix="Governed library service request",
    )
    _normalize_supported_value(
        str(request["entry_point"]),
        field_name="entry_point",
        supported_values=SUPPORTED_SERVICE_ENTRY_POINTS,
        error_prefix="Governed library service request",
    )
    _normalize_supported_value(
        str(request["requested_operation"]),
        field_name="requested_operation",
        supported_values=SUPPORTED_SERVICE_OPERATIONS,
        error_prefix="Governed library service request",
    )
    _normalize_supported_value(
        str(request["release_status"]),
        field_name="release_status",
        supported_values=ALLOWED_PREFLIGHT_RELEASE_STATUSES,
        error_prefix="Governed library service request",
    )

    for field_name in _REQUIRED_SERVICE_LIST_FIELDS:
        values = request.get(field_name)
        if not isinstance(values, list) or not values:
            raise ValueError(
                f"Governed library service request must declare non-empty {field_name}."
            )

    for field_name in _REQUIRED_SERVICE_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(
                f"Governed library service request requires {field_name} to be False."
            )

    declared_refs = {
        _parse_service_ref(ref, field_name="declared_release_refs")["asset_ref"]
        for ref in request["declared_release_refs"]  # type: ignore[index]
    }
    requested_refs = [
        _parse_service_ref(ref, field_name="requested_asset_refs")["asset_ref"]
        for ref in request["requested_asset_refs"]  # type: ignore[index]
    ]
    _reject_duplicates(requested_refs, field_name="requested_asset_refs")

    for requested_ref in requested_refs:
        if requested_ref not in declared_refs:
            raise ValueError(
                "Governed library service request references an asset not declared "
                f"in the validated release manifest: {requested_ref!r}."
            )


def validate_service_preflight_from_release_manifest(
    *,
    release_manifest: dict[str, object],
    requested_asset_refs: list[str],
    requested_operation: str,
) -> dict[str, object]:
    """Validate service preflight from a release manifest and requested refs."""
    request = build_governed_library_service_request(
        service_request_id="SERVICE-PREFLIGHT",
        caller_boundary=SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
        entry_point=SERVICE_ENTRY_POINT_ORCHESTRATION,
        requested_operation=requested_operation,
        release_manifest=release_manifest,
        requested_asset_refs=requested_asset_refs,
    )
    return {
        "checkpoint": GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_SERVICE_HARDENING_CONTRACT_VERSION,
        "preflight_result": "passed",
        "service_request": request,
        "requested_operation": request["requested_operation"],
        "requested_asset_refs": request["requested_asset_refs"],
        "release_manifest_ref": request["release_manifest_ref"],
    }


def _collect_manifest_refs(release_manifest: dict[str, object]) -> set[str]:
    declared_refs: set[str] = set()
    for field_name in (
        "selector_refs",
        "task_pool_refs",
        "profile_refs",
        "standards_bundle_refs",
        "calendar_refs",
        "planning_basis_refs",
        "mapping_metadata_refs",
    ):
        values = release_manifest.get(field_name)
        if not isinstance(values, list):
            raise ValueError(
                f"Validated release manifest must expose list field {field_name}."
            )
        for ref in values:
            declared_refs.add(_parse_service_ref(ref, field_name=field_name)["asset_ref"])
    return declared_refs


def _parse_service_ref(raw_ref: object, *, field_name: str) -> dict[str, str]:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="Governed library service request",
    )
    parsed = parse_version_pinned_asset_ref(ref)
    if parsed["asset_id"].startswith(("CS-CS-", "TP-CS-", "PROF-CS-", "PB-CS-")):
        raise ValueError(
            "Legacy computerized-system CS refs are not allowed in M15.7 "
            f"service requests: {parsed['asset_ref']!r}."
        )
    return parsed


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


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate ref in {field_name}: {value!r}.")
        seen.add(value)


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
                f"{field_name} is not allowed in M15.7 governed library service requests."
            )
