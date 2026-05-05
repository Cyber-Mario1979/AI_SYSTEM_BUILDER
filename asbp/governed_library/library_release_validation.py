"Library validation, freeze, and release discipline for M15.6."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

GOVERNED_LIBRARY_RELEASE_CHECKPOINT_ID = "M15.6"
GOVERNED_LIBRARY_RELEASE_CONTRACT_VERSION = (
    "library-validation-freeze-release-v1"
)

RUNTIME_AUTHORITY_STATUS_NOT_AUTHORITY = "not_runtime_authority"
DEPLOYMENT_COMPILED_STATUS_NOT_COMPILED = "not_compiled"

RELEASE_STATUS_DRAFT = "draft_not_runtime_authority"
RELEASE_STATUS_VALIDATION_CANDIDATE = "validation_candidate"
RELEASE_STATUS_FREEZE_CANDIDATE = "freeze_candidate"
RELEASE_STATUS_FROZEN_RELEASED = "frozen_released"
RELEASE_STATUS_REJECTED = "rejected"

SUPPORTED_LIBRARY_RELEASE_STATUSES = (
    RELEASE_STATUS_DRAFT,
    RELEASE_STATUS_VALIDATION_CANDIDATE,
    RELEASE_STATUS_FREEZE_CANDIDATE,
    RELEASE_STATUS_FROZEN_RELEASED,
    RELEASE_STATUS_REJECTED,
)

_LIBRARY_RELEASE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "release_manifest_id",
    "release_manifest_version",
    "release_manifest_ref",
    "release_status",
    "runtime_authority_status",
    "deployment_compiled_status",
)

_LIBRARY_RELEASE_REQUIRED_LIST_FIELDS = (
    "selector_refs",
    "task_pool_refs",
    "profile_refs",
    "standards_bundle_refs",
    "calendar_refs",
    "planning_basis_refs",
    "mapping_metadata_refs",
    "link_records",
    "task_profile_key_mappings",
    "document_obligation_mappings",
)

_PROHIBITED_RELEASE_FIELDS = (
    "runtime_authority_override",
    "compiled_lookup_as_source_truth",
    "source_truth_override",
    "execution_truth_override",
    "direct_filesystem_lookup",
    "raw_filesystem_path",
    "filesystem_glob",
    "ai_owned_source_truth",
    "ui_owned_source_truth",
    "cli_owned_source_truth",
)


def build_library_release_policy_baseline() -> dict[str, Any]:
    """Return the M15.6 validation/freeze/release policy baseline."""
    return {
        "checkpoint": GOVERNED_LIBRARY_RELEASE_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_RELEASE_CONTRACT_VERSION,
        "supported_release_statuses": list(SUPPORTED_LIBRARY_RELEASE_STATUSES),
        "runtime_authority_status": RUNTIME_AUTHORITY_STATUS_NOT_AUTHORITY,
        "deployment_compiled_status": DEPLOYMENT_COMPILED_STATUS_NOT_COMPILED,
        "structural_validity_rules": [
            "all required manifest fields must be present",
            "all library references must be version-pinned",
            "all link records must resolve to declared reference lists",
            "document obligation mappings must be non-empty per task pool",
        ],
        "taxonomy_identity_rules": [
            "CS is reserved as the context-selector prefix",
            "CSV is the computerized-systems domain acronym",
            "legacy CS-CS, TP-CS, PROF-CS, and PB-CS future-canonical refs are rejected",
            "latest/current/wildcard versions are rejected",
        ],
        "cross_library_linkage_rules": [
            "selector refs must link to declared task-pool refs",
            "selector refs must link to declared profile refs",
            "selector refs must link to declared calendar refs",
            "selector refs must link to declared standards-bundle refs",
            "selector refs must link to declared planning-basis refs",
            "task/profile key mappings must link to declared task pools and profiles",
        ],
        "compiled_lookup_consistency_rules": [
            "compiled refs must link back to included authored source refs",
            "compiled lookup must not become source authority",
            "compiled lookup is not generated in M15.6",
        ],
        "not_owned_by_m15_6": [
            "runtime migration",
            "deployment compiled lookup generation",
            "cli changes",
            "orchestration service hardening",
            "ai runtime behavior",
            "milestone validation checkpoint closure",
            "milestone uat",
        ],
    }


def build_library_release_manifest(
    *,
    release_manifest_id: str,
    release_manifest_version: str,
    release_status: str,
    selector_refs: list[str],
    task_pool_refs: list[str],
    profile_refs: list[str],
    standards_bundle_refs: list[str],
    calendar_refs: list[str],
    planning_basis_refs: list[str],
    mapping_metadata_refs: list[str],
    link_records: list[dict[str, object]],
    task_profile_key_mappings: list[dict[str, object]],
    document_obligation_mappings: list[dict[str, object]],
    compiled_lookup_refs: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build and validate an M15.6 library release manifest."""
    manifest_id = _normalize_manifest_id(release_manifest_id)
    manifest_version = _parse_ref_component_version(release_manifest_version)
    manifest = {
        "checkpoint": GOVERNED_LIBRARY_RELEASE_CHECKPOINT_ID,
        "contract_version": GOVERNED_LIBRARY_RELEASE_CONTRACT_VERSION,
        "release_manifest_id": manifest_id,
        "release_manifest_version": manifest_version,
        "release_manifest_ref": f"{manifest_id}@{manifest_version}",
        "release_status": _normalize_supported_release_status(release_status),
        "runtime_authority_status": RUNTIME_AUTHORITY_STATUS_NOT_AUTHORITY,
        "deployment_compiled_status": DEPLOYMENT_COMPILED_STATUS_NOT_COMPILED,
        "selector_refs": list(selector_refs),
        "task_pool_refs": list(task_pool_refs),
        "profile_refs": list(profile_refs),
        "standards_bundle_refs": list(standards_bundle_refs),
        "calendar_refs": list(calendar_refs),
        "planning_basis_refs": list(planning_basis_refs),
        "mapping_metadata_refs": list(mapping_metadata_refs),
        "link_records": list(link_records),
        "task_profile_key_mappings": list(task_profile_key_mappings),
        "document_obligation_mappings": list(document_obligation_mappings),
        "compiled_lookup_refs": list(compiled_lookup_refs or []),
    }
    validate_library_release_manifest(manifest)
    return manifest


def validate_library_release_manifest(manifest: dict[str, object]) -> None:
    """Validate one M15.6 library validation/freeze/release manifest."""
    _validate_prohibited_fields(manifest, _PROHIBITED_RELEASE_FIELDS)
    _validate_required_string_fields(
        manifest,
        _LIBRARY_RELEASE_REQUIRED_STRING_FIELDS,
        error_prefix="Library release manifest",
    )
    _validate_expected_exact_value(
        manifest,
        field_name="checkpoint",
        expected_value=GOVERNED_LIBRARY_RELEASE_CHECKPOINT_ID,
        error_prefix="Library release manifest",
    )
    _validate_expected_exact_value(
        manifest,
        field_name="contract_version",
        expected_value=GOVERNED_LIBRARY_RELEASE_CONTRACT_VERSION,
        error_prefix="Library release manifest",
    )
    _validate_expected_exact_value(
        manifest,
        field_name="runtime_authority_status",
        expected_value=RUNTIME_AUTHORITY_STATUS_NOT_AUTHORITY,
        error_prefix="Library release manifest",
    )
    _validate_expected_exact_value(
        manifest,
        field_name="deployment_compiled_status",
        expected_value=DEPLOYMENT_COMPILED_STATUS_NOT_COMPILED,
        error_prefix="Library release manifest",
    )

    manifest_id = _normalize_manifest_id(str(manifest["release_manifest_id"]))
    manifest_version = _parse_ref_component_version(
        str(manifest["release_manifest_version"])
    )
    expected_manifest_ref = f"{manifest_id}@{manifest_version}"
    if manifest["release_manifest_ref"] != expected_manifest_ref:
        raise ValueError(
            "Library release manifest declares invalid release_manifest_ref: "
            f"expected {expected_manifest_ref!r}, "
            f"got {manifest['release_manifest_ref']!r}."
        )

    _normalize_supported_release_status(str(manifest["release_status"]))

    for field_name in _LIBRARY_RELEASE_REQUIRED_LIST_FIELDS:
        if field_name not in manifest or not isinstance(manifest[field_name], list):
            raise ValueError(
                f"Library release manifest must declare list field {field_name}."
            )

    compiled_lookup_refs = manifest.get("compiled_lookup_refs", [])
    if not isinstance(compiled_lookup_refs, list):
        raise ValueError(
            "Library release manifest compiled_lookup_refs must be a list."
        )

    reference_sets = _validate_and_collect_reference_sets(manifest)
    _validate_link_records(manifest["link_records"], reference_sets)  # type: ignore[arg-type]
    _validate_task_profile_key_mappings(
        manifest["task_profile_key_mappings"],  # type: ignore[arg-type]
        reference_sets,
    )
    _validate_document_obligation_mappings(
        manifest["document_obligation_mappings"],  # type: ignore[arg-type]
        reference_sets,
    )
    _validate_compiled_lookup_refs(compiled_lookup_refs, reference_sets)


def validate_compiled_lookup_candidate(
    *,
    compiled_ref: str,
    source_ref: str,
    authored_source_refs: list[str],
    compiled_lookup_is_source_authority: bool,
) -> None:
    """Validate one compiled lookup reference candidate without generating it."""
    _parse_version_pinned_ref(
        compiled_ref,
        field_name="compiled_ref",
        reject_legacy_cs=False,
    )
    parsed_source = _parse_version_pinned_ref(
        source_ref,
        field_name="source_ref",
        reject_legacy_cs=False,
    )
    normalized_sources = {
        _parse_version_pinned_ref(
            ref,
            field_name="authored_source_ref",
            reject_legacy_cs=False,
        )["asset_ref"]
        for ref in authored_source_refs
    }
    if parsed_source["asset_ref"] not in normalized_sources:
        raise ValueError(
            "Compiled lookup candidate must link to an included authored source ref."
        )
    if compiled_lookup_is_source_authority is not False:
        raise ValueError("Compiled lookup candidate must not be source authority.")


def _validate_and_collect_reference_sets(
    manifest: dict[str, object],
) -> dict[str, set[str]]:
    reference_sets: dict[str, set[str]] = {}
    for field_name in (
        "selector_refs",
        "task_pool_refs",
        "profile_refs",
        "standards_bundle_refs",
        "calendar_refs",
        "planning_basis_refs",
        "mapping_metadata_refs",
    ):
        raw_refs = manifest[field_name]
        if not raw_refs:
            raise ValueError(
                f"Library release manifest must declare at least one {field_name}."
            )
        normalized_refs: list[str] = []
        for raw_ref in raw_refs:  # type: ignore[assignment]
            parsed = _parse_version_pinned_ref(
                raw_ref,
                field_name=field_name,
                reject_legacy_cs=True,
            )
            normalized_refs.append(parsed["asset_ref"])
        _reject_duplicates(normalized_refs, field_name=field_name)
        reference_sets[field_name] = set(normalized_refs)
    return reference_sets


def _validate_link_records(
    link_records: list[dict[str, object]],
    reference_sets: dict[str, set[str]],
) -> None:
    if not link_records:
        raise ValueError("Library release manifest must declare link_records.")
    seen_selectors: set[str] = set()
    for link in link_records:
        selector_ref = _require_ref_in_set(
            link,
            "selector_ref",
            reference_sets["selector_refs"],
        )
        if selector_ref in seen_selectors:
            raise ValueError(
                f"Duplicate selector link record for selector_ref {selector_ref!r}."
            )
        seen_selectors.add(selector_ref)
        _require_ref_in_set(link, "task_pool_ref", reference_sets["task_pool_refs"])
        _require_ref_in_set(link, "profile_ref", reference_sets["profile_refs"])
        _require_ref_in_set(link, "calendar_ref", reference_sets["calendar_refs"])
        _require_ref_in_set(
            link,
            "planning_basis_ref",
            reference_sets["planning_basis_refs"],
        )

        standards_refs = link.get("standards_bundle_refs")
        if not isinstance(standards_refs, list) or not standards_refs:
            raise ValueError(
                f"Link record {selector_ref!r} must declare standards_bundle_refs."
            )
        for standards_ref in standards_refs:
            parsed = _parse_version_pinned_ref(
                standards_ref,
                field_name="standards_bundle_refs",
                reject_legacy_cs=True,
            )
            if parsed["asset_ref"] not in reference_sets["standards_bundle_refs"]:
                raise ValueError(
                    "Link record references undeclared standards bundle "
                    f"{parsed['asset_ref']!r}."
                )


def _validate_task_profile_key_mappings(
    mappings: list[dict[str, object]],
    reference_sets: dict[str, set[str]],
) -> None:
    if not mappings:
        raise ValueError(
            "Library release manifest must declare task_profile_key_mappings."
        )
    seen: set[tuple[str, str, str]] = set()
    for mapping in mappings:
        task_pool_ref = _require_ref_in_set(
            mapping,
            "task_pool_ref",
            reference_sets["task_pool_refs"],
        )
        profile_ref = _require_ref_in_set(
            mapping,
            "profile_ref",
            reference_sets["profile_refs"],
        )
        profile_key = _require_non_empty_string(
            mapping.get("profile_key"),
            field_name="profile_key",
            error_prefix="Task/profile-key mapping",
        )
        key = (task_pool_ref, profile_ref, profile_key)
        if key in seen:
            raise ValueError(f"Duplicate task/profile-key mapping {key!r}.")
        seen.add(key)


def _validate_document_obligation_mappings(
    mappings: list[dict[str, object]],
    reference_sets: dict[str, set[str]],
) -> None:
    if not mappings:
        raise ValueError(
            "Library release manifest must declare document_obligation_mappings."
        )
    seen_task_pools: set[str] = set()
    for mapping in mappings:
        task_pool_ref = _require_ref_in_set(
            mapping,
            "task_pool_ref",
            reference_sets["task_pool_refs"],
        )
        if task_pool_ref in seen_task_pools:
            raise ValueError(
                "Duplicate document obligation mapping for task_pool_ref "
                f"{task_pool_ref!r}."
            )
        seen_task_pools.add(task_pool_ref)
        obligations = mapping.get("document_family_obligations")
        if not isinstance(obligations, list) or not obligations:
            raise ValueError(
                "Document obligation mapping must declare non-empty "
                "document_family_obligations."
            )
        for obligation in obligations:
            _require_non_empty_string(
                obligation,
                field_name="document_family_obligation",
                error_prefix="Document obligation mapping",
            )


def _validate_compiled_lookup_refs(
    compiled_lookup_refs: list[dict[str, object]],
    reference_sets: dict[str, set[str]],
) -> None:
    authored_source_refs: set[str] = set()
    for refs in reference_sets.values():
        authored_source_refs.update(refs)
    for candidate in compiled_lookup_refs:
        validate_compiled_lookup_candidate(
            compiled_ref=str(candidate.get("compiled_ref", "")),
            source_ref=str(candidate.get("source_ref", "")),
            authored_source_refs=sorted(authored_source_refs),
            compiled_lookup_is_source_authority=bool(
                candidate.get("compiled_lookup_is_source_authority")
            ),
        )


def _require_ref_in_set(
    payload: dict[str, object],
    field_name: str,
    allowed_refs: set[str],
) -> str:
    parsed = _parse_version_pinned_ref(
        payload.get(field_name),
        field_name=field_name,
        reject_legacy_cs=True,
    )
    normalized_ref = parsed["asset_ref"]
    if normalized_ref not in allowed_refs:
        raise ValueError(
            f"{field_name} references undeclared governed library ref "
            f"{normalized_ref!r}."
        )
    return normalized_ref


def _parse_version_pinned_ref(
    raw_ref: object,
    *,
    field_name: str,
    reject_legacy_cs: bool,
) -> dict[str, str]:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="Governed library release ref",
    )
    parsed = parse_version_pinned_asset_ref(ref)
    if reject_legacy_cs and _is_legacy_computerized_system_ref(parsed["asset_id"]):
        raise ValueError(
            "Legacy computerized-system CS refs are not allowed in future "
            f"canonical M15.6 release manifests: {parsed['asset_ref']!r}."
        )
    return parsed


def _is_legacy_computerized_system_ref(asset_id: str) -> bool:
    return asset_id.startswith(("CS-CS-", "TP-CS-", "PROF-CS-", "PB-CS-"))


def _normalize_manifest_id(release_manifest_id: str) -> str:
    return _parse_version_pinned_ref(
        f"{release_manifest_id}@v1",
        field_name="release_manifest_id",
        reject_legacy_cs=False,
    )["asset_id"]


def _parse_ref_component_version(version: str) -> str:
    return parse_version_pinned_asset_ref(f"MANIFEST@{version}")["asset_version"]


def _normalize_supported_release_status(value: str) -> str:
    normalized = _require_non_empty_string(
        value,
        field_name="release_status",
        error_prefix="Library release manifest",
    )
    if normalized not in SUPPORTED_LIBRARY_RELEASE_STATUSES:
        raise ValueError(
            "Library release manifest declares unsupported release_status. "
            "Expected one of: "
            f"{', '.join(SUPPORTED_LIBRARY_RELEASE_STATUSES)}."
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
                f"{field_name} is not allowed in M15.6 library release manifests."
            )
