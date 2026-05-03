"Authored-source versus deployment-compiled separation for M14.4."

from __future__ import annotations

from typing import Any

from .boundary import (
    CALENDAR_ASSET_FAMILY,
    MAPPING_METADATA_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
    PRESET_ASSET_FAMILY,
    PROFILE_ASSET_FAMILY,
    RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    TASK_POOL_ASSET_FAMILY,
    TEMPLATE_ASSET_FAMILY,
)
from .identity import (
    build_version_pinned_asset_ref,
    parse_version_pinned_asset_ref,
)

RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID = "M14.4"
RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION = (
    "authored-source-deployment-compiled-separation-v1"
)

AUTHORED_SOURCE_TRUTH_ROLE = "editable_authoritative_source_truth"
DEPLOYMENT_COMPILED_LOOKUP_ROLE = "deployment_compiled_runtime_lookup_surface_only"
COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY = (
    "compiled_lookup_may_reference_authored_source_but_must_not_become_source_authority"
)
AUTHORED_SOURCE_EDITABILITY_POLICY = (
    "authored_source_records_remain_editable_source_truth_until_intentionally_frozen_or_released"
)
DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY = (
    "deployment_compiled_lookup_records_are_runtime_read_surfaces_and_must_not_mutate_authored_source"
)
SOURCE_COMPILATION_FAILURE_POLICY = (
    "source_compilation_boundary_fails_closed_on_unversioned_mismatched_ambiguous_or_authority_overriding_records"
)
SOURCE_COMPILATION_CONTENT_POLICY = (
    "m14_4_tracks_identity_source_and_compiled_lookup_references_only_not_asset_payload"
)

SUPPORTED_COMPILED_LOOKUP_FAMILIES = (
    TEMPLATE_ASSET_FAMILY,
    PRESET_ASSET_FAMILY,
    TASK_POOL_ASSET_FAMILY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    PROFILE_ASSET_FAMILY,
    MAPPING_METADATA_ASSET_FAMILY,
    CALENDAR_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
)

_AUTHORED_SOURCE_REQUIRED_FIELDS = (
    "checkpoint",
    "contract_version",
    "asset_family",
    "asset_id",
    "asset_version",
    "asset_ref",
    "source_record_ref",
    "source_role",
    "source_truth_policy",
    "source_editability_policy",
    "failure_policy",
    "content_policy",
)

_DEPLOYMENT_COMPILED_REQUIRED_FIELDS = (
    "checkpoint",
    "contract_version",
    "asset_family",
    "asset_id",
    "asset_version",
    "asset_ref",
    "lookup_key",
    "compiled_record_ref",
    "compiled_surface_id",
    "source_record_ref",
    "source_role",
    "compiled_lookup_role",
    "source_truth_policy",
    "compiled_not_source_authority_policy",
    "compiled_immutability_policy",
    "failure_policy",
    "content_policy",
)

_COMPILATION_LINK_REQUIRED_FIELDS = (
    "checkpoint",
    "contract_version",
    "asset_family",
    "asset_id",
    "asset_version",
    "asset_ref",
    "source_record_ref",
    "compiled_record_ref",
    "compiled_surface_id",
    "source_role",
    "compiled_lookup_role",
    "source_truth_policy",
    "compiled_not_source_authority_policy",
    "compiled_immutability_policy",
    "failure_policy",
    "content_policy",
)

_PROHIBITED_SOURCE_COMPILATION_FIELDS = (
    "latest",
    "current",
    "wildcard_asset_version",
    "version_range",
    "unversioned_asset_ref",
    "direct_filesystem_lookup",
    "raw_filesystem_path",
    "filesystem_glob",
    "asset_payload",
    "unvalidated_asset_payload",
    "source_truth_override",
    "execution_truth_override",
    "resolver_bypass",
    "compiled_source_truth",
    "compiled_as_source_truth",
    "compiled_authority_override",
    "compiled_source_authority",
    "runtime_mutates_authored_source",
    "authored_source_mutated_by_runtime",
    "compiled_runtime_writeback",
    "ui_owned_source_truth",
    "ai_owned_source_truth",
)


def build_source_compilation_separation_baseline() -> dict[str, Any]:
    """Return the M14.4 authored-source / compiled-lookup separation rules."""
    return {
        "checkpoint": RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION,
        "supported_compiled_lookup_families": list(SUPPORTED_COMPILED_LOOKUP_FAMILIES),
        "authored_source_role": AUTHORED_SOURCE_TRUTH_ROLE,
        "deployment_compiled_lookup_role": DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "compiled_not_source_authority_policy": (
            COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
        ),
        "source_editability_policy": AUTHORED_SOURCE_EDITABILITY_POLICY,
        "compiled_immutability_policy": DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY,
        "failure_policy": SOURCE_COMPILATION_FAILURE_POLICY,
        "content_policy": SOURCE_COMPILATION_CONTENT_POLICY,
        "owned_by_m14_4": [
            "authored_source_truth_role",
            "deployment_compiled_lookup_role",
            "source_to_compiled_identity_link",
            "compiled_lookup_family_allowlist",
            "compiled_lookup_not_source_authority_validation",
        ],
        "not_owned_by_m14_4": [
            "asset_payload_loading",
            "asset_content_editing",
            "library_expansion_content_authoring",
            "deployment_packaging_pipeline",
            "support_retrieval_boundary",
            "ai_retrieval_consumption",
        ],
    }


def build_authored_source_record(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
    source_record_ref: str,
) -> dict[str, str]:
    """Build an authored-source truth record."""
    normalized_family = _normalize_supported_family(asset_family)
    parsed_ref = parse_version_pinned_asset_ref(
        build_version_pinned_asset_ref(
            asset_id=asset_id,
            asset_version=asset_version,
        )
    )
    record = {
        "checkpoint": RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION,
        "asset_family": normalized_family,
        "asset_id": parsed_ref["asset_id"],
        "asset_version": parsed_ref["asset_version"],
        "asset_ref": parsed_ref["asset_ref"],
        "source_record_ref": _require_non_empty_string(
            source_record_ref,
            field_name="source_record_ref",
            error_prefix="Authored source record",
        ),
        "source_role": AUTHORED_SOURCE_TRUTH_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "source_editability_policy": AUTHORED_SOURCE_EDITABILITY_POLICY,
        "failure_policy": SOURCE_COMPILATION_FAILURE_POLICY,
        "content_policy": SOURCE_COMPILATION_CONTENT_POLICY,
    }
    validate_authored_source_record(record)
    return record


def build_deployment_compiled_lookup_record(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
    compiled_record_ref: str,
    compiled_surface_id: str,
    source_record_ref: str,
) -> dict[str, str]:
    """Build a deployment-compiled runtime lookup record."""
    normalized_family = _normalize_supported_family(asset_family)
    parsed_ref = parse_version_pinned_asset_ref(
        build_version_pinned_asset_ref(
            asset_id=asset_id,
            asset_version=asset_version,
        )
    )
    lookup_key = _build_source_compilation_lookup_key(
        asset_family=normalized_family,
        asset_id=parsed_ref["asset_id"],
        asset_version=parsed_ref["asset_version"],
    )
    record = {
        "checkpoint": RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION,
        "asset_family": normalized_family,
        "asset_id": parsed_ref["asset_id"],
        "asset_version": parsed_ref["asset_version"],
        "asset_ref": parsed_ref["asset_ref"],
        "lookup_key": lookup_key,
        "compiled_record_ref": _require_non_empty_string(
            compiled_record_ref,
            field_name="compiled_record_ref",
            error_prefix="Deployment compiled lookup record",
        ),
        "compiled_surface_id": _require_non_empty_string(
            compiled_surface_id,
            field_name="compiled_surface_id",
            error_prefix="Deployment compiled lookup record",
        ),
        "source_record_ref": _require_non_empty_string(
            source_record_ref,
            field_name="source_record_ref",
            error_prefix="Deployment compiled lookup record",
        ),
        "source_role": AUTHORED_SOURCE_TRUTH_ROLE,
        "compiled_lookup_role": DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "compiled_not_source_authority_policy": (
            COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
        ),
        "compiled_immutability_policy": DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY,
        "failure_policy": SOURCE_COMPILATION_FAILURE_POLICY,
        "content_policy": SOURCE_COMPILATION_CONTENT_POLICY,
    }
    validate_deployment_compiled_lookup_record(record)
    return record


def build_source_to_compiled_link(
    *,
    authored_source_record: dict[str, object],
    deployment_compiled_record: dict[str, object],
) -> dict[str, object]:
    """Build and validate the identity-preserving source-to-compiled link."""
    validate_authored_source_record(authored_source_record)
    validate_deployment_compiled_lookup_record(deployment_compiled_record)

    for field_name in ("asset_family", "asset_id", "asset_version", "asset_ref"):
        if authored_source_record[field_name] != deployment_compiled_record[field_name]:
            raise ValueError(
                "Source-to-compiled link requires matching version-pinned "
                f"{field_name}."
            )

    if (
        authored_source_record["source_record_ref"]
        != deployment_compiled_record["source_record_ref"]
    ):
        raise ValueError(
            "Source-to-compiled link requires the compiled record to reference "
            "the same authored source_record_ref."
        )

    link = {
        "checkpoint": RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION,
        "asset_family": authored_source_record["asset_family"],
        "asset_id": authored_source_record["asset_id"],
        "asset_version": authored_source_record["asset_version"],
        "asset_ref": authored_source_record["asset_ref"],
        "source_record_ref": authored_source_record["source_record_ref"],
        "compiled_record_ref": deployment_compiled_record["compiled_record_ref"],
        "compiled_surface_id": deployment_compiled_record["compiled_surface_id"],
        "source_role": AUTHORED_SOURCE_TRUTH_ROLE,
        "compiled_lookup_role": DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "compiled_not_source_authority_policy": (
            COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
        ),
        "compiled_immutability_policy": DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY,
        "failure_policy": SOURCE_COMPILATION_FAILURE_POLICY,
        "content_policy": SOURCE_COMPILATION_CONTENT_POLICY,
    }
    validate_source_to_compiled_link(link)
    return link


def validate_authored_source_record(record: dict[str, object]) -> None:
    """Validate an authored-source truth record."""
    _validate_prohibited_fields(record)
    _validate_required_string_fields(
        record,
        _AUTHORED_SOURCE_REQUIRED_FIELDS,
        error_prefix="Authored source record",
    )
    _validate_common_source_identity(
        record,
        expected_error_prefix="Authored source record",
    )
    _validate_expected_exact_value(
        record,
        field_name="source_role",
        expected_value=AUTHORED_SOURCE_TRUTH_ROLE,
        error_prefix="Authored source record",
    )
    _validate_expected_exact_value(
        record,
        field_name="source_editability_policy",
        expected_value=AUTHORED_SOURCE_EDITABILITY_POLICY,
        error_prefix="Authored source record",
    )


def validate_deployment_compiled_lookup_record(record: dict[str, object]) -> None:
    """Validate a deployment-compiled runtime lookup record."""
    _validate_prohibited_fields(record)
    _validate_required_string_fields(
        record,
        _DEPLOYMENT_COMPILED_REQUIRED_FIELDS,
        error_prefix="Deployment compiled lookup record",
    )
    _validate_common_source_identity(
        record,
        expected_error_prefix="Deployment compiled lookup record",
    )
    expected_lookup_key = _build_source_compilation_lookup_key(
        asset_family=str(record["asset_family"]),
        asset_id=str(record["asset_id"]),
        asset_version=str(record["asset_version"]),
    )
    if record["lookup_key"] != expected_lookup_key:
        raise ValueError(
            "Deployment compiled lookup record declares an invalid lookup_key: "
            f"expected {expected_lookup_key!r}, got {record['lookup_key']!r}."
        )

    _validate_expected_exact_value(
        record,
        field_name="source_role",
        expected_value=AUTHORED_SOURCE_TRUTH_ROLE,
        error_prefix="Deployment compiled lookup record",
    )
    _validate_expected_exact_value(
        record,
        field_name="compiled_lookup_role",
        expected_value=DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        error_prefix="Deployment compiled lookup record",
    )
    _validate_expected_exact_value(
        record,
        field_name="compiled_not_source_authority_policy",
        expected_value=COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
        error_prefix="Deployment compiled lookup record",
    )
    _validate_expected_exact_value(
        record,
        field_name="compiled_immutability_policy",
        expected_value=DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY,
        error_prefix="Deployment compiled lookup record",
    )


def validate_source_to_compiled_link(link: dict[str, object]) -> None:
    """Validate the source-to-compiled linkage record."""
    _validate_prohibited_fields(link)
    _validate_required_string_fields(
        link,
        _COMPILATION_LINK_REQUIRED_FIELDS,
        error_prefix="Source-to-compiled link",
    )
    _validate_common_source_identity(
        link,
        expected_error_prefix="Source-to-compiled link",
    )
    _validate_expected_exact_value(
        link,
        field_name="source_role",
        expected_value=AUTHORED_SOURCE_TRUTH_ROLE,
        error_prefix="Source-to-compiled link",
    )
    _validate_expected_exact_value(
        link,
        field_name="compiled_lookup_role",
        expected_value=DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        error_prefix="Source-to-compiled link",
    )
    _validate_expected_exact_value(
        link,
        field_name="compiled_not_source_authority_policy",
        expected_value=COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
        error_prefix="Source-to-compiled link",
    )
    _validate_expected_exact_value(
        link,
        field_name="compiled_immutability_policy",
        expected_value=DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY,
        error_prefix="Source-to-compiled link",
    )


def build_deployment_compiled_lookup_registry(
    entries: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    """Build a compiled lookup registry and reject duplicate lookup keys."""
    registry: dict[str, dict[str, object]] = {}
    for entry in entries:
        validate_deployment_compiled_lookup_record(entry)
        lookup_key = str(entry["lookup_key"])
        if lookup_key in registry:
            raise ValueError(
                "Duplicate deployment compiled lookup record for lookup_key "
                f"{lookup_key!r}."
            )
        registry[lookup_key] = dict(entry)
    return registry


def resolve_deployment_compiled_lookup(
    *,
    registry: dict[str, dict[str, object]],
    asset_family: str,
    asset_id: str,
    asset_version: str,
    caller_context_ref: str,
) -> dict[str, object]:
    """Resolve a deployment-compiled lookup record by exact governed key."""
    caller_context = _require_non_empty_string(
        caller_context_ref,
        field_name="caller_context_ref",
        error_prefix="Deployment compiled lookup request",
    )
    normalized_family = _normalize_supported_family(asset_family)
    parsed_ref = parse_version_pinned_asset_ref(
        build_version_pinned_asset_ref(
            asset_id=asset_id,
            asset_version=asset_version,
        )
    )
    lookup_key = _build_source_compilation_lookup_key(
        asset_family=normalized_family,
        asset_id=parsed_ref["asset_id"],
        asset_version=parsed_ref["asset_version"],
    )
    entry = registry.get(lookup_key)
    if entry is None:
        raise ValueError(
            "Deployment compiled lookup failed closed because no exact "
            f"version-pinned entry exists for lookup_key {lookup_key!r}."
        )

    validate_deployment_compiled_lookup_record(entry)
    return {
        "checkpoint": RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION,
        "lookup_result": "resolved",
        "caller_context_ref": caller_context,
        "resolved_lookup_key": lookup_key,
        "resolved_identity": {
            "asset_family": entry["asset_family"],
            "asset_id": entry["asset_id"],
            "asset_version": entry["asset_version"],
            "asset_ref": entry["asset_ref"],
        },
        "compiled_record_ref": entry["compiled_record_ref"],
        "compiled_surface_id": entry["compiled_surface_id"],
        "source_record_ref": entry["source_record_ref"],
        "source_role": AUTHORED_SOURCE_TRUTH_ROLE,
        "compiled_lookup_role": DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        "compiled_not_source_authority_policy": (
            COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
        ),
        "compiled_immutability_policy": DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY,
        "failure_policy": SOURCE_COMPILATION_FAILURE_POLICY,
        "content_policy": SOURCE_COMPILATION_CONTENT_POLICY,
        "asset_payload_included": False,
        "compiled_lookup_is_source_authority": False,
        "runtime_mutates_authored_source": False,
    }


def _build_source_compilation_lookup_key(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
) -> str:
    parsed_ref = parse_version_pinned_asset_ref(
        build_version_pinned_asset_ref(
            asset_id=asset_id,
            asset_version=asset_version,
        )
    )
    return f"{asset_family}:{parsed_ref['asset_ref']}"


def _validate_common_source_identity(
    record: dict[str, object],
    *,
    expected_error_prefix: str,
) -> None:
    _validate_expected_exact_value(
        record,
        field_name="checkpoint",
        expected_value=RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID,
        error_prefix=expected_error_prefix,
    )
    _validate_expected_exact_value(
        record,
        field_name="contract_version",
        expected_value=RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION,
        error_prefix=expected_error_prefix,
    )
    _validate_expected_exact_value(
        record,
        field_name="source_truth_policy",
        expected_value=RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        error_prefix=expected_error_prefix,
    )
    _validate_expected_exact_value(
        record,
        field_name="failure_policy",
        expected_value=SOURCE_COMPILATION_FAILURE_POLICY,
        error_prefix=expected_error_prefix,
    )
    _validate_expected_exact_value(
        record,
        field_name="content_policy",
        expected_value=SOURCE_COMPILATION_CONTENT_POLICY,
        error_prefix=expected_error_prefix,
    )

    normalized_family = _normalize_supported_family(str(record["asset_family"]))
    parsed_ref = parse_version_pinned_asset_ref(str(record["asset_ref"]))
    if record["asset_family"] != normalized_family:
        raise ValueError(
            f"{expected_error_prefix} declares a non-canonical asset_family: "
            f"expected {normalized_family!r}, got {record['asset_family']!r}."
        )
    if record["asset_id"] != parsed_ref["asset_id"]:
        raise ValueError(
            f"{expected_error_prefix} declares a non-canonical asset_id: "
            f"expected {parsed_ref['asset_id']!r}, got {record['asset_id']!r}."
        )
    if record["asset_version"] != parsed_ref["asset_version"]:
        raise ValueError(
            f"{expected_error_prefix} declares a non-canonical asset_version: "
            f"expected {parsed_ref['asset_version']!r}, got "
            f"{record['asset_version']!r}."
        )


def _normalize_supported_family(asset_family: str) -> str:
    normalized = _require_non_empty_string(
        asset_family,
        field_name="asset_family",
        error_prefix="Source compilation record",
    ).lower()
    if normalized not in SUPPORTED_COMPILED_LOOKUP_FAMILIES:
        raise ValueError(
            "Unsupported source compilation asset family. Expected one of: "
            f"{', '.join(SUPPORTED_COMPILED_LOOKUP_FAMILIES)}."
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


def _validate_prohibited_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_SOURCE_COMPILATION_FIELDS:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in source compilation separation."
            )
