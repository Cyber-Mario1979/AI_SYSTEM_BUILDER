"Governed asset identity and version-pinned lookup for M14.2."

from __future__ import annotations

import re
from typing import Any

from .boundary import (
    CALENDAR_ASSET_FAMILY,
    MAPPING_METADATA_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
    PRESET_ASSET_FAMILY,
    PROFILE_ASSET_FAMILY,
    RESOLVER_REGISTRY_FAILURE_POLICY,
    RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    TASK_POOL_ASSET_FAMILY,
    TEMPLATE_ASSET_FAMILY,
)

RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID = "M14.2"
RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION = "governed-asset-identity-lookup-v1"

GOVERNED_ASSET_LOOKUP_ROLE = "version_pinned_governed_asset_identity_lookup_only"
GOVERNED_ASSET_SOURCE_AUTHORITY_ROLE = "identity_reference_only_not_asset_content_authority"
GOVERNED_ASSET_VERSION_PIN_POLICY = "lookup_requires_explicit_asset_version_and_rejects_latest_current_or_wildcards"
GOVERNED_ASSET_LOOKUP_FAILURE_POLICY = "lookup_fails_closed_on_unsupported_family_invalid_identity_missing_or_ambiguous_entry"
GOVERNED_ASSET_CONTENT_POLICY = "m14_2_resolves_identity_and_record_reference_only_not_asset_payload"

SUPPORTED_VERSION_PINNED_GOVERNED_ASSET_FAMILIES = (
    TEMPLATE_ASSET_FAMILY,
    PRESET_ASSET_FAMILY,
    TASK_POOL_ASSET_FAMILY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    PROFILE_ASSET_FAMILY,
    MAPPING_METADATA_ASSET_FAMILY,
)

DEFERRED_RESOLUTION_ASSET_FAMILIES = (
    CALENDAR_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
)

_ASSET_ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(?:[._-][A-Z0-9]+)*$")
_ASSET_VERSION_PATTERN = re.compile(r"^v[1-9][0-9]*(?:\.[0-9]+)*$")

_PROHIBITED_IDENTITY_FIELDS = (
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
)

_REQUIRED_IDENTITY_FIELDS = (
    "checkpoint",
    "contract_version",
    "asset_family",
    "asset_id",
    "asset_version",
    "asset_ref",
    "lookup_key",
    "lookup_role",
    "source_authority_role",
    "source_truth_policy",
    "version_pin_policy",
    "failure_policy",
    "content_policy",
)

_REQUIRED_LOOKUP_ENTRY_FIELDS = _REQUIRED_IDENTITY_FIELDS + (
    "asset_record_ref",
)


def build_governed_asset_identity_baseline() -> dict[str, Any]:
    """Return M14.2 identity and version-pinned lookup rules."""
    return {
        "checkpoint": RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION,
        "supported_version_pinned_asset_families": list(
            SUPPORTED_VERSION_PINNED_GOVERNED_ASSET_FAMILIES
        ),
        "deferred_resolution_asset_families": list(DEFERRED_RESOLUTION_ASSET_FAMILIES),
        "lookup_role": GOVERNED_ASSET_LOOKUP_ROLE,
        "source_authority_role": GOVERNED_ASSET_SOURCE_AUTHORITY_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "version_pin_policy": GOVERNED_ASSET_VERSION_PIN_POLICY,
        "failure_policy": GOVERNED_ASSET_LOOKUP_FAILURE_POLICY,
        "boundary_failure_policy": RESOLVER_REGISTRY_FAILURE_POLICY,
        "content_policy": GOVERNED_ASSET_CONTENT_POLICY,
        "canonical_ref_format": "<ASSET_ID>@<asset_version>",
        "canonical_lookup_key_format": "<asset_family>:<ASSET_ID>@<asset_version>",
        "implemented_lookup_families": [
            "templates",
            "presets",
            "task_pools",
            "standards_bundles",
            "profiles",
            "mapping_metadata",
        ],
        "not_yet_implemented": [
            "calendar_resolution_execution",
            "planning_basis_resolution_execution",
            "asset_payload_loading",
            "authored_source_vs_deployment_compiled_resolution",
            "support_retrieval_boundary",
        ],
    }


def build_version_pinned_asset_ref(
    *,
    asset_id: str,
    asset_version: str,
) -> str:
    """Build the canonical asset ref used by version-pinned lookup."""
    normalized_asset_id = _normalize_asset_id(asset_id)
    normalized_asset_version = _normalize_asset_version(asset_version)
    return f"{normalized_asset_id}@{normalized_asset_version}"


def parse_version_pinned_asset_ref(asset_ref: str) -> dict[str, str]:
    """Parse and validate a canonical version-pinned asset ref."""
    normalized_ref = _require_non_empty_string(
        asset_ref,
        field_name="asset_ref",
        error_prefix="Version-pinned asset ref",
    )
    if normalized_ref.count("@") != 1:
        raise ValueError(
            "Version-pinned asset ref must use exactly one '@' separator."
        )

    raw_asset_id, raw_asset_version = normalized_ref.split("@", 1)
    asset_id = _normalize_asset_id(raw_asset_id)
    asset_version = _normalize_asset_version(raw_asset_version)
    return {
        "asset_id": asset_id,
        "asset_version": asset_version,
        "asset_ref": f"{asset_id}@{asset_version}",
    }


def build_governed_asset_lookup_key(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
) -> str:
    """Build the canonical registry lookup key."""
    normalized_asset_family = _normalize_supported_asset_family(asset_family)
    asset_ref = build_version_pinned_asset_ref(
        asset_id=asset_id,
        asset_version=asset_version,
    )
    return f"{normalized_asset_family}:{asset_ref}"


def build_governed_asset_identity(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
) -> dict[str, str]:
    """Build a governed asset identity without loading asset payload content."""
    normalized_asset_family = _normalize_supported_asset_family(asset_family)
    parsed_ref = parse_version_pinned_asset_ref(
        build_version_pinned_asset_ref(
            asset_id=asset_id,
            asset_version=asset_version,
        )
    )
    identity = {
        "checkpoint": RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION,
        "asset_family": normalized_asset_family,
        "asset_id": parsed_ref["asset_id"],
        "asset_version": parsed_ref["asset_version"],
        "asset_ref": parsed_ref["asset_ref"],
        "lookup_key": f"{normalized_asset_family}:{parsed_ref['asset_ref']}",
        "lookup_role": GOVERNED_ASSET_LOOKUP_ROLE,
        "source_authority_role": GOVERNED_ASSET_SOURCE_AUTHORITY_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "version_pin_policy": GOVERNED_ASSET_VERSION_PIN_POLICY,
        "failure_policy": GOVERNED_ASSET_LOOKUP_FAILURE_POLICY,
        "content_policy": GOVERNED_ASSET_CONTENT_POLICY,
    }
    validate_governed_asset_identity(identity)
    return identity


def validate_governed_asset_identity(identity: dict[str, object]) -> None:
    """Validate a governed asset identity against M14.2 rules."""
    _validate_prohibited_fields(identity, _PROHIBITED_IDENTITY_FIELDS)
    _validate_required_string_fields(
        identity,
        _REQUIRED_IDENTITY_FIELDS,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="checkpoint",
        expected_value=RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="contract_version",
        expected_value=RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="lookup_role",
        expected_value=GOVERNED_ASSET_LOOKUP_ROLE,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="source_authority_role",
        expected_value=GOVERNED_ASSET_SOURCE_AUTHORITY_ROLE,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="source_truth_policy",
        expected_value=RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="version_pin_policy",
        expected_value=GOVERNED_ASSET_VERSION_PIN_POLICY,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="failure_policy",
        expected_value=GOVERNED_ASSET_LOOKUP_FAILURE_POLICY,
        error_prefix="Governed asset identity",
    )
    _validate_expected_exact_value(
        identity,
        field_name="content_policy",
        expected_value=GOVERNED_ASSET_CONTENT_POLICY,
        error_prefix="Governed asset identity",
    )

    normalized_asset_family = _normalize_supported_asset_family(
        str(identity["asset_family"])
    )
    normalized_asset_id = _normalize_asset_id(str(identity["asset_id"]))
    normalized_asset_version = _normalize_asset_version(str(identity["asset_version"]))
    expected_asset_ref = build_version_pinned_asset_ref(
        asset_id=normalized_asset_id,
        asset_version=normalized_asset_version,
    )
    expected_lookup_key = build_governed_asset_lookup_key(
        asset_family=normalized_asset_family,
        asset_id=normalized_asset_id,
        asset_version=normalized_asset_version,
    )

    if identity["asset_family"] != normalized_asset_family:
        raise ValueError(
            "Governed asset identity declares a non-canonical asset_family: "
            f"expected {normalized_asset_family!r}, got {identity['asset_family']!r}."
        )
    if identity["asset_id"] != normalized_asset_id:
        raise ValueError(
            "Governed asset identity declares a non-canonical asset_id: "
            f"expected {normalized_asset_id!r}, got {identity['asset_id']!r}."
        )
    if identity["asset_version"] != normalized_asset_version:
        raise ValueError(
            "Governed asset identity declares a non-canonical asset_version: "
            f"expected {normalized_asset_version!r}, got {identity['asset_version']!r}."
        )
    if identity["asset_ref"] != expected_asset_ref:
        raise ValueError(
            "Governed asset identity declares an invalid asset_ref: "
            f"expected {expected_asset_ref!r}, got {identity['asset_ref']!r}."
        )
    if identity["lookup_key"] != expected_lookup_key:
        raise ValueError(
            "Governed asset identity declares an invalid lookup_key: "
            f"expected {expected_lookup_key!r}, got {identity['lookup_key']!r}."
        )


def build_governed_asset_lookup_entry(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
    asset_record_ref: str,
) -> dict[str, str]:
    """Build one deterministic lookup entry for a governed asset identity."""
    identity = build_governed_asset_identity(
        asset_family=asset_family,
        asset_id=asset_id,
        asset_version=asset_version,
    )
    entry = {
        **identity,
        "asset_record_ref": _require_non_empty_string(
            asset_record_ref,
            field_name="asset_record_ref",
            error_prefix="Governed asset lookup entry",
        ),
    }
    validate_governed_asset_lookup_entry(entry)
    return entry


def validate_governed_asset_lookup_entry(entry: dict[str, object]) -> None:
    """Validate one governed lookup entry."""
    _validate_prohibited_fields(entry, _PROHIBITED_IDENTITY_FIELDS)
    _validate_required_string_fields(
        entry,
        _REQUIRED_LOOKUP_ENTRY_FIELDS,
        error_prefix="Governed asset lookup entry",
    )
    validate_governed_asset_identity(entry)


def build_governed_asset_registry(
    entries: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    """Build a lookup-keyed registry and reject duplicate identities."""
    registry: dict[str, dict[str, object]] = {}
    for entry in entries:
        validate_governed_asset_lookup_entry(entry)
        lookup_key = str(entry["lookup_key"])
        if lookup_key in registry:
            raise ValueError(
                "Duplicate governed asset lookup entry for lookup_key "
                f"{lookup_key!r}."
            )
        registry[lookup_key] = dict(entry)
    return registry


def resolve_version_pinned_governed_asset(
    *,
    registry: dict[str, dict[str, object]],
    asset_family: str,
    asset_id: str,
    asset_version: str,
    caller_context_ref: str,
) -> dict[str, object]:
    """Resolve a governed asset identity by exact version-pinned lookup key."""
    caller_context = _require_non_empty_string(
        caller_context_ref,
        field_name="caller_context_ref",
        error_prefix="Governed asset lookup request",
    )
    requested_identity = build_governed_asset_identity(
        asset_family=asset_family,
        asset_id=asset_id,
        asset_version=asset_version,
    )
    lookup_key = requested_identity["lookup_key"]
    entry = registry.get(lookup_key)
    if entry is None:
        raise ValueError(
            "Governed asset lookup failed closed because no exact version-pinned "
            f"entry exists for lookup_key {lookup_key!r}."
        )

    validate_governed_asset_lookup_entry(entry)
    return {
        "checkpoint": RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION,
        "lookup_result": "resolved",
        "caller_context_ref": caller_context,
        "requested_identity": requested_identity,
        "resolved_identity": {
            field_name: entry[field_name]
            for field_name in _REQUIRED_IDENTITY_FIELDS
        },
        "resolved_lookup_key": lookup_key,
        "asset_record_ref": entry["asset_record_ref"],
        "lookup_role": GOVERNED_ASSET_LOOKUP_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "version_pin_policy": GOVERNED_ASSET_VERSION_PIN_POLICY,
        "failure_policy": GOVERNED_ASSET_LOOKUP_FAILURE_POLICY,
        "content_policy": GOVERNED_ASSET_CONTENT_POLICY,
        "asset_payload_included": False,
    }


def _normalize_supported_asset_family(asset_family: str) -> str:
    normalized = _require_non_empty_string(
        asset_family,
        field_name="asset_family",
        error_prefix="Governed asset identity",
    ).lower()
    if normalized not in SUPPORTED_VERSION_PINNED_GOVERNED_ASSET_FAMILIES:
        if normalized in DEFERRED_RESOLUTION_ASSET_FAMILIES:
            raise ValueError(
                "Asset family is deferred to a later resolver checkpoint: "
                f"{normalized!r}."
            )
        raise ValueError(
            "Unsupported governed asset family for version-pinned lookup. "
            "Expected one of: "
            f"{', '.join(SUPPORTED_VERSION_PINNED_GOVERNED_ASSET_FAMILIES)}."
        )
    return normalized


def _normalize_asset_id(asset_id: str) -> str:
    normalized = _require_non_empty_string(
        asset_id,
        field_name="asset_id",
        error_prefix="Governed asset identity",
    ).upper()
    if "@" in normalized:
        raise ValueError("Governed asset identity asset_id must not contain '@'.")
    if not _ASSET_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Governed asset identity asset_id must be a canonical token using "
            "letters, numbers, underscore, dash, or dot."
        )
    return normalized


def _normalize_asset_version(asset_version: str) -> str:
    normalized = _require_non_empty_string(
        asset_version,
        field_name="asset_version",
        error_prefix="Governed asset identity",
    ).lower()
    if normalized in {"latest", "current", "*"}:
        raise ValueError(
            "Governed asset lookup requires an explicit pinned version; "
            "latest/current/wildcard versions are not allowed."
        )
    if not _ASSET_VERSION_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Governed asset identity asset_version must use canonical form "
            "'v<number>' or 'v<number>.<number>'."
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
                f"{field_name} is not allowed in governed asset identity lookup."
            )
