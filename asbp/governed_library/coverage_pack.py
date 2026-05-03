"Coverage-pack expansion framework for M15.2."

from __future__ import annotations

import re
from typing import Any

from asbp.resolver_registry.boundary import (
    CALENDAR_ASSET_FAMILY,
    MAPPING_METADATA_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
    PRESET_ASSET_FAMILY,
    PROFILE_ASSET_FAMILY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    SUPPORTED_RESOLVABLE_ASSET_FAMILIES,
    TASK_POOL_ASSET_FAMILY,
    TEMPLATE_ASSET_FAMILY,
)
from asbp.resolver_registry.identity import (
    build_version_pinned_asset_ref,
    parse_version_pinned_asset_ref,
)
from asbp.resolver_registry.source_compilation import (
    AUTHORED_SOURCE_TRUTH_ROLE,
    COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
    DEPLOYMENT_COMPILED_LOOKUP_ROLE,
)

GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID = "M15.2"
GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION = (
    "coverage-pack-expansion-framework-v1"
)

COVERAGE_PACK_ROLE = "bounded_governed_library_expansion_unit"
COVERAGE_PACK_EXPANSION_UNIT_POLICY = (
    "coverage_pack_is_the_coordinated_unit_for_governed_library_expansion"
)
COVERAGE_PACK_ARTIFACT_COORDINATION_POLICY = (
    "coverage_pack_coordinates_multiple_governed_artifact_families_without_"
    "expanding_content_inside_m15_2"
)
COVERAGE_PACK_SOURCE_TO_COMPILED_LINKAGE_POLICY = (
    "coverage_pack_preserves_authored_source_truth_and_links_deployment_compiled_"
    "refs_without_making_compiled_lookup_source_authority"
)
COVERAGE_PACK_CONTENT_POLICY = (
    "m15_2_defines_coverage_pack_identity_refs_and_coordination_rules_only_not_"
    "asset_payload_content_expansion_or_deployment_compile_pipeline"
)

AUTHORED_SOURCE_REF_ROLE = "authored_source_truth_ref"
DEPLOYMENT_COMPILED_REF_ROLE = "deployment_compiled_lookup_ref"

VALIDATION_STATUS_DRAFT = "draft_pending_validation"
VALIDATION_STATUS_VALIDATED = "validated"
VALIDATION_STATUS_REJECTED = "rejected"
SUPPORTED_COVERAGE_PACK_VALIDATION_STATUSES = (
    VALIDATION_STATUS_DRAFT,
    VALIDATION_STATUS_VALIDATED,
    VALIDATION_STATUS_REJECTED,
)

FREEZE_STATUS_UNFROZEN = "unfrozen"
FREEZE_STATUS_FREEZE_CANDIDATE = "freeze_candidate"
FREEZE_STATUS_FROZEN_RELEASED = "frozen_released"
SUPPORTED_COVERAGE_PACK_FREEZE_STATUSES = (
    FREEZE_STATUS_UNFROZEN,
    FREEZE_STATUS_FREEZE_CANDIDATE,
    FREEZE_STATUS_FROZEN_RELEASED,
)

SUPPORTED_COVERAGE_PACK_ASSET_FAMILIES = SUPPORTED_RESOLVABLE_ASSET_FAMILIES

_PACK_ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(?:[._-][A-Z0-9]+)*$")
_TAXONOMY_TOKEN_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[_-][a-z0-9]+)*$")

_PROHIBITED_COVERAGE_PACK_FIELDS = (
    "asset_payload",
    "unvalidated_asset_payload",
    "source_truth_override",
    "execution_truth_override",
    "compiled_as_source_truth",
    "compiled_source_authority",
    "compiled_authority_override",
    "runtime_mutates_authored_source",
    "compiled_runtime_writeback",
    "direct_filesystem_lookup",
    "raw_filesystem_path",
    "filesystem_glob",
    "selector_content_expansion",
    "task_pool_content_expansion",
    "calendar_content_expansion",
    "standards_content_expansion",
    "profile_content_expansion",
    "mapping_content_expansion",
    "deployment_compile_pipeline",
    "orchestration_service_hardening",
    "cli_command_surface",
)

_PROHIBITED_REFERENCE_FIELDS = (
    "asset_payload",
    "unvalidated_asset_payload",
    "source_truth_override",
    "execution_truth_override",
    "compiled_as_source_truth",
    "compiled_source_authority",
    "compiled_authority_override",
    "compiled_runtime_writeback",
    "direct_filesystem_lookup",
    "raw_filesystem_path",
    "filesystem_glob",
    "ai_owned_source_truth",
    "ui_owned_source_truth",
)

_COVERAGE_PACK_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "coverage_pack_id",
    "coverage_pack_version",
    "coverage_pack_ref",
    "coverage_family",
    "variant_scope_layer",
    "coverage_pack_role",
    "expansion_unit_policy",
    "artifact_family_coordination_policy",
    "source_to_compiled_linkage_policy",
    "validation_status",
    "freeze_status",
    "content_policy",
)

_COVERAGE_PACK_REQUIRED_LIST_FIELDS = (
    "authored_source_refs",
    "deployment_compiled_refs",
    "standards_bundle_refs",
    "calendar_refs",
    "planning_basis_refs",
    "mapping_metadata_refs",
)

_REFERENCE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "asset_family",
    "asset_id",
    "asset_version",
    "asset_ref",
    "record_ref",
    "reference_role",
    "source_authority_policy",
    "content_policy",
)

_REFERENCE_REQUIRED_BOOLEAN_FIELDS = (
    "asset_payload_included",
    "compiled_lookup_is_source_authority",
    "runtime_mutates_authored_source",
)


def build_coverage_pack_framework_baseline() -> dict[str, Any]:
    """Return the M15.2 coverage-pack expansion framework baseline."""
    return {
        "checkpoint": GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION,
        "coverage_pack_role": COVERAGE_PACK_ROLE,
        "expansion_unit_policy": COVERAGE_PACK_EXPANSION_UNIT_POLICY,
        "artifact_family_coordination_policy": (
            COVERAGE_PACK_ARTIFACT_COORDINATION_POLICY
        ),
        "source_to_compiled_linkage_policy": (
            COVERAGE_PACK_SOURCE_TO_COMPILED_LINKAGE_POLICY
        ),
        "content_policy": COVERAGE_PACK_CONTENT_POLICY,
        "supported_asset_families": list(SUPPORTED_COVERAGE_PACK_ASSET_FAMILIES),
        "supported_validation_statuses": list(
            SUPPORTED_COVERAGE_PACK_VALIDATION_STATUSES
        ),
        "supported_freeze_statuses": list(SUPPORTED_COVERAGE_PACK_FREEZE_STATUSES),
        "required_coverage_pack_fields": list(
            _COVERAGE_PACK_REQUIRED_STRING_FIELDS
            + _COVERAGE_PACK_REQUIRED_LIST_FIELDS
        ),
        "required_reference_fields": list(
            _REFERENCE_REQUIRED_STRING_FIELDS + _REFERENCE_REQUIRED_BOOLEAN_FIELDS
        ),
        "owned_by_m15_2": [
            "bounded_coverage_pack_model",
            "expansion_unit_expectations",
            "multi_artifact_family_coordination_rules",
            "authored_source_ref_rules",
            "deployment_compiled_ref_rules",
            "source_to_compiled_linkage_rules",
        ],
        "not_owned_by_m15_2": [
            "selector_content_expansion",
            "task_pool_content_expansion",
            "calendar_content_expansion",
            "standards_bundle_content_expansion",
            "profile_content_expansion",
            "mapping_content_expansion",
            "deployment_compile_pipeline",
            "orchestration_service_hardening",
            "cli_command_surface",
            "ai_runtime_behavior",
        ],
    }


def build_authored_source_ref(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
    source_record_ref: str,
) -> dict[str, object]:
    """Build a coverage-pack authored-source reference.

    The reference points to authored source truth only. It does not contain
    library payload content and does not perform resolver lookup.
    """
    identity = _build_reference_identity(
        asset_family=asset_family,
        asset_id=asset_id,
        asset_version=asset_version,
    )
    reference = {
        **identity,
        "record_ref": _require_non_empty_string(
            source_record_ref,
            field_name="source_record_ref",
            error_prefix="Authored source coverage-pack reference",
        ),
        "reference_role": AUTHORED_SOURCE_REF_ROLE,
        "source_authority_policy": AUTHORED_SOURCE_TRUTH_ROLE,
        "content_policy": COVERAGE_PACK_CONTENT_POLICY,
        "asset_payload_included": False,
        "compiled_lookup_is_source_authority": False,
        "runtime_mutates_authored_source": False,
    }
    validate_coverage_pack_reference(
        reference,
        expected_reference_role=AUTHORED_SOURCE_REF_ROLE,
    )
    return reference


def build_deployment_compiled_ref(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
    compiled_record_ref: str,
    compiled_surface_id: str,
    source_record_ref: str,
) -> dict[str, object]:
    """Build a coverage-pack deployment-compiled lookup reference.

    The reference may point to a compiled runtime lookup surface, but it cannot
    become source authority and must link back to an authored source ref.
    """
    identity = _build_reference_identity(
        asset_family=asset_family,
        asset_id=asset_id,
        asset_version=asset_version,
    )
    reference = {
        **identity,
        "record_ref": _require_non_empty_string(
            compiled_record_ref,
            field_name="compiled_record_ref",
            error_prefix="Deployment compiled coverage-pack reference",
        ),
        "compiled_surface_id": _require_non_empty_string(
            compiled_surface_id,
            field_name="compiled_surface_id",
            error_prefix="Deployment compiled coverage-pack reference",
        ),
        "source_record_ref": _require_non_empty_string(
            source_record_ref,
            field_name="source_record_ref",
            error_prefix="Deployment compiled coverage-pack reference",
        ),
        "reference_role": DEPLOYMENT_COMPILED_REF_ROLE,
        "source_authority_policy": COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
        "content_policy": COVERAGE_PACK_CONTENT_POLICY,
        "asset_payload_included": False,
        "compiled_lookup_is_source_authority": False,
        "runtime_mutates_authored_source": False,
    }
    validate_coverage_pack_reference(
        reference,
        expected_reference_role=DEPLOYMENT_COMPILED_REF_ROLE,
    )
    return reference


def build_coverage_pack(
    *,
    coverage_pack_id: str,
    coverage_pack_version: str,
    coverage_family: str,
    variant_scope_layer: str,
    authored_source_refs: list[dict[str, object]],
    deployment_compiled_refs: list[dict[str, object]] | None = None,
    standards_bundle_refs: list[dict[str, object]] | None = None,
    calendar_refs: list[dict[str, object]] | None = None,
    planning_basis_refs: list[dict[str, object]] | None = None,
    mapping_metadata_refs: list[dict[str, object]] | None = None,
    validation_status: str = VALIDATION_STATUS_DRAFT,
    freeze_status: str = FREEZE_STATUS_UNFROZEN,
) -> dict[str, object]:
    """Build one governed coverage-pack framework record."""
    normalized_pack_id = _normalize_coverage_pack_id(coverage_pack_id)
    normalized_pack_version = _normalize_coverage_pack_version(coverage_pack_version)
    coverage_pack = {
        "checkpoint": GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION,
        "coverage_pack_id": normalized_pack_id,
        "coverage_pack_version": normalized_pack_version,
        "coverage_pack_ref": f"{normalized_pack_id}@{normalized_pack_version}",
        "coverage_family": _normalize_taxonomy_token(
            coverage_family,
            field_name="coverage_family",
        ),
        "variant_scope_layer": _normalize_taxonomy_token(
            variant_scope_layer,
            field_name="variant_scope_layer",
        ),
        "coverage_pack_role": COVERAGE_PACK_ROLE,
        "expansion_unit_policy": COVERAGE_PACK_EXPANSION_UNIT_POLICY,
        "artifact_family_coordination_policy": (
            COVERAGE_PACK_ARTIFACT_COORDINATION_POLICY
        ),
        "source_to_compiled_linkage_policy": (
            COVERAGE_PACK_SOURCE_TO_COMPILED_LINKAGE_POLICY
        ),
        "authored_source_refs": list(authored_source_refs),
        "deployment_compiled_refs": list(deployment_compiled_refs or []),
        "standards_bundle_refs": list(standards_bundle_refs or []),
        "calendar_refs": list(calendar_refs or []),
        "planning_basis_refs": list(planning_basis_refs or []),
        "mapping_metadata_refs": list(mapping_metadata_refs or []),
        "validation_status": _normalize_supported_value(
            validation_status,
            field_name="validation_status",
            supported_values=SUPPORTED_COVERAGE_PACK_VALIDATION_STATUSES,
            error_prefix="Coverage pack",
        ),
        "freeze_status": _normalize_supported_value(
            freeze_status,
            field_name="freeze_status",
            supported_values=SUPPORTED_COVERAGE_PACK_FREEZE_STATUSES,
            error_prefix="Coverage pack",
        ),
        "content_policy": COVERAGE_PACK_CONTENT_POLICY,
    }
    validate_coverage_pack(coverage_pack)
    return coverage_pack


def validate_coverage_pack(pack: dict[str, object]) -> None:
    """Validate one governed coverage-pack framework record."""
    _validate_prohibited_fields(pack, _PROHIBITED_COVERAGE_PACK_FIELDS)
    _validate_required_string_fields(
        pack,
        _COVERAGE_PACK_REQUIRED_STRING_FIELDS,
        error_prefix="Coverage pack",
    )
    _validate_expected_exact_value(
        pack,
        field_name="checkpoint",
        expected_value=GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID,
        error_prefix="Coverage pack",
    )
    _validate_expected_exact_value(
        pack,
        field_name="contract_version",
        expected_value=GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION,
        error_prefix="Coverage pack",
    )
    _validate_expected_exact_value(
        pack,
        field_name="coverage_pack_role",
        expected_value=COVERAGE_PACK_ROLE,
        error_prefix="Coverage pack",
    )
    _validate_expected_exact_value(
        pack,
        field_name="expansion_unit_policy",
        expected_value=COVERAGE_PACK_EXPANSION_UNIT_POLICY,
        error_prefix="Coverage pack",
    )
    _validate_expected_exact_value(
        pack,
        field_name="artifact_family_coordination_policy",
        expected_value=COVERAGE_PACK_ARTIFACT_COORDINATION_POLICY,
        error_prefix="Coverage pack",
    )
    _validate_expected_exact_value(
        pack,
        field_name="source_to_compiled_linkage_policy",
        expected_value=COVERAGE_PACK_SOURCE_TO_COMPILED_LINKAGE_POLICY,
        error_prefix="Coverage pack",
    )
    _validate_expected_exact_value(
        pack,
        field_name="content_policy",
        expected_value=COVERAGE_PACK_CONTENT_POLICY,
        error_prefix="Coverage pack",
    )

    pack_id = _normalize_coverage_pack_id(str(pack["coverage_pack_id"]))
    pack_version = _normalize_coverage_pack_version(str(pack["coverage_pack_version"]))
    expected_ref = f"{pack_id}@{pack_version}"
    if pack["coverage_pack_id"] != pack_id:
        raise ValueError(
            "Coverage pack declares a non-canonical coverage_pack_id: "
            f"expected {pack_id!r}, got {pack['coverage_pack_id']!r}."
        )
    if pack["coverage_pack_version"] != pack_version:
        raise ValueError(
            "Coverage pack declares a non-canonical coverage_pack_version: "
            f"expected {pack_version!r}, got {pack['coverage_pack_version']!r}."
        )
    if pack["coverage_pack_ref"] != expected_ref:
        raise ValueError(
            "Coverage pack declares an invalid coverage_pack_ref: "
            f"expected {expected_ref!r}, got {pack['coverage_pack_ref']!r}."
        )

    _normalize_taxonomy_token(str(pack["coverage_family"]), field_name="coverage_family")
    _normalize_taxonomy_token(
        str(pack["variant_scope_layer"]),
        field_name="variant_scope_layer",
    )
    _normalize_supported_value(
        str(pack["validation_status"]),
        field_name="validation_status",
        supported_values=SUPPORTED_COVERAGE_PACK_VALIDATION_STATUSES,
        error_prefix="Coverage pack",
    )
    _normalize_supported_value(
        str(pack["freeze_status"]),
        field_name="freeze_status",
        supported_values=SUPPORTED_COVERAGE_PACK_FREEZE_STATUSES,
        error_prefix="Coverage pack",
    )

    for field_name in _COVERAGE_PACK_REQUIRED_LIST_FIELDS:
        if field_name not in pack or not isinstance(pack[field_name], list):
            raise ValueError(f"Coverage pack must declare list field {field_name}.")

    authored_source_refs = pack["authored_source_refs"]
    if not authored_source_refs:
        raise ValueError("Coverage pack must declare at least one authored_source_ref.")

    all_references = _collect_references(pack)
    _validate_reference_duplicates(all_references)
    for reference in all_references:
        validate_coverage_pack_reference(reference)

    for reference in pack["authored_source_refs"]:
        validate_coverage_pack_reference(
            reference,
            expected_reference_role=AUTHORED_SOURCE_REF_ROLE,
        )
    for reference in pack["deployment_compiled_refs"]:
        validate_coverage_pack_reference(
            reference,
            expected_reference_role=DEPLOYMENT_COMPILED_REF_ROLE,
        )
    _validate_reference_family_list(
        pack["standards_bundle_refs"],
        expected_asset_family=STANDARDS_BUNDLE_ASSET_FAMILY,
        list_name="standards_bundle_refs",
    )
    _validate_reference_family_list(
        pack["calendar_refs"],
        expected_asset_family=CALENDAR_ASSET_FAMILY,
        list_name="calendar_refs",
    )
    _validate_reference_family_list(
        pack["planning_basis_refs"],
        expected_asset_family=PLANNING_BASIS_ASSET_FAMILY,
        list_name="planning_basis_refs",
    )
    _validate_reference_family_list(
        pack["mapping_metadata_refs"],
        expected_asset_family=MAPPING_METADATA_ASSET_FAMILY,
        list_name="mapping_metadata_refs",
    )
    _validate_compiled_refs_link_to_authored_sources(all_references)


def validate_coverage_pack_reference(
    reference: dict[str, object],
    *,
    expected_reference_role: str | None = None,
    expected_asset_family: str | None = None,
) -> None:
    """Validate one coverage-pack asset reference."""
    _validate_prohibited_fields(reference, _PROHIBITED_REFERENCE_FIELDS)
    _validate_required_string_fields(
        reference,
        _REFERENCE_REQUIRED_STRING_FIELDS,
        error_prefix="Coverage-pack reference",
    )
    for field_name in _REFERENCE_REQUIRED_BOOLEAN_FIELDS:
        if field_name not in reference or not isinstance(reference[field_name], bool):
            raise ValueError(
                f"Coverage-pack reference must declare boolean {field_name}."
            )

    _validate_expected_exact_value(
        reference,
        field_name="checkpoint",
        expected_value=GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID,
        error_prefix="Coverage-pack reference",
    )
    _validate_expected_exact_value(
        reference,
        field_name="contract_version",
        expected_value=GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION,
        error_prefix="Coverage-pack reference",
    )
    _validate_expected_exact_value(
        reference,
        field_name="content_policy",
        expected_value=COVERAGE_PACK_CONTENT_POLICY,
        error_prefix="Coverage-pack reference",
    )

    normalized_family = _normalize_supported_asset_family(str(reference["asset_family"]))
    if expected_asset_family is not None and normalized_family != expected_asset_family:
        raise ValueError(
            f"{expected_asset_family} reference list contains unsupported asset_family "
            f"{normalized_family!r}."
        )
    parsed_ref = parse_version_pinned_asset_ref(str(reference["asset_ref"]))
    if reference["asset_family"] != normalized_family:
        raise ValueError(
            "Coverage-pack reference declares a non-canonical asset_family: "
            f"expected {normalized_family!r}, got {reference['asset_family']!r}."
        )
    if reference["asset_id"] != parsed_ref["asset_id"]:
        raise ValueError(
            "Coverage-pack reference declares a non-canonical asset_id: "
            f"expected {parsed_ref['asset_id']!r}, got {reference['asset_id']!r}."
        )
    if reference["asset_version"] != parsed_ref["asset_version"]:
        raise ValueError(
            "Coverage-pack reference declares a non-canonical asset_version: "
            f"expected {parsed_ref['asset_version']!r}, "
            f"got {reference['asset_version']!r}."
        )

    reference_role = str(reference["reference_role"])
    if expected_reference_role is not None and reference_role != expected_reference_role:
        raise ValueError(
            "Coverage-pack reference declares an invalid reference_role: "
            f"expected {expected_reference_role!r}, got {reference_role!r}."
        )

    if reference["asset_payload_included"] is not False:
        raise ValueError("Coverage-pack reference must not include asset payload.")
    if reference["compiled_lookup_is_source_authority"] is not False:
        raise ValueError(
            "Coverage-pack reference must not make compiled lookup source authority."
        )
    if reference["runtime_mutates_authored_source"] is not False:
        raise ValueError(
            "Coverage-pack reference must not allow runtime to mutate authored source."
        )

    if reference_role == AUTHORED_SOURCE_REF_ROLE:
        _validate_expected_exact_value(
            reference,
            field_name="source_authority_policy",
            expected_value=AUTHORED_SOURCE_TRUTH_ROLE,
            error_prefix="Coverage-pack authored-source reference",
        )
        if "compiled_surface_id" in reference or "source_record_ref" in reference:
            raise ValueError(
                "Authored-source coverage-pack reference must not declare compiled "
                "lookup fields."
            )
        return

    if reference_role == DEPLOYMENT_COMPILED_REF_ROLE:
        _validate_expected_exact_value(
            reference,
            field_name="source_authority_policy",
            expected_value=COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
            error_prefix="Coverage-pack deployment-compiled reference",
        )
        _require_non_empty_string(
            reference.get("compiled_surface_id"),
            field_name="compiled_surface_id",
            error_prefix="Coverage-pack deployment-compiled reference",
        )
        _require_non_empty_string(
            reference.get("source_record_ref"),
            field_name="source_record_ref",
            error_prefix="Coverage-pack deployment-compiled reference",
        )
        return

    raise ValueError(
        "Coverage-pack reference declares unsupported reference_role. Expected one "
        f"of: {AUTHORED_SOURCE_REF_ROLE}, {DEPLOYMENT_COMPILED_REF_ROLE}."
    )


def _build_reference_identity(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
) -> dict[str, str]:
    normalized_family = _normalize_supported_asset_family(asset_family)
    parsed_ref = parse_version_pinned_asset_ref(
        build_version_pinned_asset_ref(
            asset_id=asset_id,
            asset_version=asset_version,
        )
    )
    return {
        "checkpoint": GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION,
        "asset_family": normalized_family,
        "asset_id": parsed_ref["asset_id"],
        "asset_version": parsed_ref["asset_version"],
        "asset_ref": parsed_ref["asset_ref"],
    }


def _normalize_supported_asset_family(asset_family: str) -> str:
    normalized = _require_non_empty_string(
        asset_family,
        field_name="asset_family",
        error_prefix="Coverage-pack reference",
    ).lower()
    if normalized not in SUPPORTED_COVERAGE_PACK_ASSET_FAMILIES:
        raise ValueError(
            "Unsupported coverage-pack asset family. Expected one of: "
            f"{', '.join(SUPPORTED_COVERAGE_PACK_ASSET_FAMILIES)}."
        )
    return normalized


def _normalize_coverage_pack_id(coverage_pack_id: str) -> str:
    normalized = _require_non_empty_string(
        coverage_pack_id,
        field_name="coverage_pack_id",
        error_prefix="Coverage pack",
    ).upper()
    if "@" in normalized:
        raise ValueError("Coverage pack coverage_pack_id must not contain '@'.")
    if not _PACK_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Coverage pack coverage_pack_id must be a canonical token using "
            "letters, numbers, underscore, dash, or dot."
        )
    return normalized


def _normalize_coverage_pack_version(coverage_pack_version: str) -> str:
    parsed_ref = parse_version_pinned_asset_ref(f"PACK@{coverage_pack_version}")
    return parsed_ref["asset_version"]


def _normalize_taxonomy_token(value: str, *, field_name: str) -> str:
    normalized = _require_non_empty_string(
        value,
        field_name=field_name,
        error_prefix="Coverage pack",
    ).lower()
    if not _TAXONOMY_TOKEN_PATTERN.fullmatch(normalized):
        raise ValueError(
            f"Coverage pack {field_name} must be a lowercase taxonomy token using "
            "letters, numbers, underscore, or dash."
        )
    return normalized


def _normalize_supported_value(
    value: str,
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
            f"{error_prefix} declares unsupported {field_name}. Expected one of: "
            f"{', '.join(supported_values)}."
        )
    return normalized


def _collect_references(pack: dict[str, object]) -> list[dict[str, object]]:
    references: list[dict[str, object]] = []
    for field_name in _COVERAGE_PACK_REQUIRED_LIST_FIELDS:
        references.extend(pack[field_name])  # type: ignore[arg-type]
    return references


def _validate_reference_duplicates(references: list[dict[str, object]]) -> None:
    seen: set[tuple[str, str, str, str]] = set()
    for reference in references:
        key = (
            str(reference.get("reference_role")),
            str(reference.get("asset_family")),
            str(reference.get("asset_ref")),
            str(reference.get("record_ref")),
        )
        if key in seen:
            raise ValueError(
                "Duplicate coverage-pack reference for role/family/ref/record "
                f"{key!r}."
            )
        seen.add(key)


def _validate_reference_family_list(
    references: list[dict[str, object]],
    *,
    expected_asset_family: str,
    list_name: str,
) -> None:
    for reference in references:
        try:
            validate_coverage_pack_reference(
                reference,
                expected_asset_family=expected_asset_family,
            )
        except ValueError as exc:
            raise ValueError(f"{list_name} contains invalid reference: {exc}") from exc


def _validate_compiled_refs_link_to_authored_sources(
    references: list[dict[str, object]],
) -> None:
    authored_record_refs = {
        str(reference["record_ref"])
        for reference in references
        if reference.get("reference_role") == AUTHORED_SOURCE_REF_ROLE
    }
    for reference in references:
        if reference.get("reference_role") != DEPLOYMENT_COMPILED_REF_ROLE:
            continue
        source_record_ref = str(reference.get("source_record_ref"))
        if source_record_ref not in authored_record_refs:
            raise ValueError(
                "Coverage-pack deployment-compiled reference must link to an "
                f"included authored source_record_ref: {source_record_ref!r}."
            )


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
            raise ValueError(f"{field_name} is not allowed in coverage-pack framework.")
