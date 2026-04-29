"Calendar and planning-basis resolution family for M14.3."

from __future__ import annotations

from typing import Any

from .boundary import (
    CALENDAR_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
    RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
)
from .identity import (
    build_version_pinned_asset_ref,
    parse_version_pinned_asset_ref,
)

RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID = "M14.3"
RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION = (
    "calendar-planning-basis-resolution-v1"
)

CALENDAR_RESOLUTION_ROLE = "governed_calendar_family_resolution_only"
PLANNING_BASIS_RESOLUTION_ROLE = "governed_planning_basis_data_resolution_only"
CALENDAR_PLANNING_CORE_INPUT_POLICY = (
    "resolved_calendar_and_planning_basis_records_are_deterministic_core_engine_inputs"
)
CALENDAR_PLANNING_NO_ARITHMETIC_POLICY = (
    "resolver_registry_resolves_inputs_but_does_not_perform_calendar_arithmetic_schedule_generation_duration_calculation_or_rendering"
)
CALENDAR_PLANNING_FAILURE_POLICY = (
    "calendar_planning_resolution_fails_closed_on_invalid_unversioned_missing_or_ambiguous_inputs"
)
CALENDAR_CONTENT_POLICY = (
    "calendar_resolution_returns_identity_and_planning_use_metadata_only_not_calendar_payload"
)
PLANNING_BASIS_CONTENT_POLICY = (
    "planning_basis_resolution_returns_identity_and_duration_dependency_source_metadata_only_not_calculated_plan"
)

SUPPORTED_CALENDAR_RESOLUTION_FAMILIES = (CALENDAR_ASSET_FAMILY,)
SUPPORTED_PLANNING_BASIS_RESOLUTION_FAMILIES = (PLANNING_BASIS_ASSET_FAMILY,)

_CALENDAR_REQUIRED_ENTRY_FIELDS = (
    "checkpoint",
    "contract_version",
    "asset_family",
    "asset_id",
    "asset_version",
    "asset_ref",
    "lookup_key",
    "resolution_role",
    "source_truth_policy",
    "core_engine_input_policy",
    "no_arithmetic_policy",
    "failure_policy",
    "content_policy",
    "calendar_record_ref",
    "calendar_family",
    "workday_model_ref",
    "timezone_policy_ref",
)

_PLANNING_BASIS_REQUIRED_ENTRY_FIELDS = (
    "checkpoint",
    "contract_version",
    "asset_family",
    "asset_id",
    "asset_version",
    "asset_ref",
    "lookup_key",
    "resolution_role",
    "source_truth_policy",
    "core_engine_input_policy",
    "no_arithmetic_policy",
    "failure_policy",
    "content_policy",
    "planning_basis_record_ref",
    "duration_source_ref",
    "dependency_source_ref",
    "calendar_requirement_ref",
)

_PROHIBITED_RESOLUTION_FIELDS = (
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
    "calendar_arithmetic",
    "workday_calculation",
    "calculated_schedule",
    "schedule_generated",
    "task_duration_calculation",
    "calculated_task_duration",
    "calculated_start_date",
    "calculated_finish_date",
    "rendered_gantt",
    "rendered_calendar",
    "regional_weekend_default",
)


def build_calendar_planning_resolution_baseline() -> dict[str, Any]:
    """Return the M14.3 resolver-family contract."""
    return {
        "checkpoint": RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION,
        "calendar_resolution_families": list(SUPPORTED_CALENDAR_RESOLUTION_FAMILIES),
        "planning_basis_resolution_families": list(
            SUPPORTED_PLANNING_BASIS_RESOLUTION_FAMILIES
        ),
        "calendar_resolution_role": CALENDAR_RESOLUTION_ROLE,
        "planning_basis_resolution_role": PLANNING_BASIS_RESOLUTION_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "core_engine_input_policy": CALENDAR_PLANNING_CORE_INPUT_POLICY,
        "no_arithmetic_policy": CALENDAR_PLANNING_NO_ARITHMETIC_POLICY,
        "failure_policy": CALENDAR_PLANNING_FAILURE_POLICY,
        "calendar_content_policy": CALENDAR_CONTENT_POLICY,
        "planning_basis_content_policy": PLANNING_BASIS_CONTENT_POLICY,
        "canonical_lookup_key_formats": [
            "calendar:<CALENDAR_ID>@<asset_version>",
            "planning_basis:<PLANNING_BASIS_ID>@<asset_version>",
        ],
        "owned_by_m14_3": [
            "calendar_family_resolution",
            "planning_basis_data_resolution",
            "calendar_family_addition_rules",
            "resolved_input_contract_for_core_engine_planning",
        ],
        "not_owned_by_m14_3": [
            "calendar_arithmetic",
            "schedule_generation",
            "task_duration_calculation",
            "regional_weekend_defaults",
            "gantt_rendering",
            "export_rendering",
            "ai_planning_behavior",
        ],
    }


def build_calendar_resolution_lookup_key(
    *,
    calendar_id: str,
    calendar_version: str,
) -> str:
    """Build the canonical lookup key for a calendar family record."""
    return _build_resolution_lookup_key(
        asset_family=CALENDAR_ASSET_FAMILY,
        asset_id=calendar_id,
        asset_version=calendar_version,
    )


def build_planning_basis_resolution_lookup_key(
    *,
    planning_basis_id: str,
    planning_basis_version: str,
) -> str:
    """Build the canonical lookup key for a planning-basis record."""
    return _build_resolution_lookup_key(
        asset_family=PLANNING_BASIS_ASSET_FAMILY,
        asset_id=planning_basis_id,
        asset_version=planning_basis_version,
    )


def build_calendar_resolution_entry(
    *,
    calendar_id: str,
    calendar_version: str,
    calendar_record_ref: str,
    calendar_family: str,
    workday_model_ref: str,
    timezone_policy_ref: str,
) -> dict[str, str]:
    """Build one governed calendar resolution entry.

    The entry exposes identity and planning-use metadata only. It does not
    calculate workdays, start dates, finish dates, or rendered schedules.
    """
    identity = _build_resolution_identity(
        asset_family=CALENDAR_ASSET_FAMILY,
        asset_id=calendar_id,
        asset_version=calendar_version,
        resolution_role=CALENDAR_RESOLUTION_ROLE,
        content_policy=CALENDAR_CONTENT_POLICY,
    )
    entry = {
        **identity,
        "calendar_record_ref": _require_non_empty_string(
            calendar_record_ref,
            field_name="calendar_record_ref",
            error_prefix="Calendar resolution entry",
        ),
        "calendar_family": _require_non_empty_string(
            calendar_family,
            field_name="calendar_family",
            error_prefix="Calendar resolution entry",
        ),
        "workday_model_ref": _require_non_empty_string(
            workday_model_ref,
            field_name="workday_model_ref",
            error_prefix="Calendar resolution entry",
        ),
        "timezone_policy_ref": _require_non_empty_string(
            timezone_policy_ref,
            field_name="timezone_policy_ref",
            error_prefix="Calendar resolution entry",
        ),
    }
    validate_calendar_resolution_entry(entry)
    return entry


def build_planning_basis_resolution_entry(
    *,
    planning_basis_id: str,
    planning_basis_version: str,
    planning_basis_record_ref: str,
    duration_source_ref: str,
    dependency_source_ref: str,
    calendar_requirement_ref: str,
) -> dict[str, str]:
    """Build one governed planning-basis resolution entry.

    The entry exposes data-source metadata only. It does not calculate task
    durations, sequence tasks, or generate a plan.
    """
    identity = _build_resolution_identity(
        asset_family=PLANNING_BASIS_ASSET_FAMILY,
        asset_id=planning_basis_id,
        asset_version=planning_basis_version,
        resolution_role=PLANNING_BASIS_RESOLUTION_ROLE,
        content_policy=PLANNING_BASIS_CONTENT_POLICY,
    )
    entry = {
        **identity,
        "planning_basis_record_ref": _require_non_empty_string(
            planning_basis_record_ref,
            field_name="planning_basis_record_ref",
            error_prefix="Planning-basis resolution entry",
        ),
        "duration_source_ref": _require_non_empty_string(
            duration_source_ref,
            field_name="duration_source_ref",
            error_prefix="Planning-basis resolution entry",
        ),
        "dependency_source_ref": _require_non_empty_string(
            dependency_source_ref,
            field_name="dependency_source_ref",
            error_prefix="Planning-basis resolution entry",
        ),
        "calendar_requirement_ref": _require_non_empty_string(
            calendar_requirement_ref,
            field_name="calendar_requirement_ref",
            error_prefix="Planning-basis resolution entry",
        ),
    }
    validate_planning_basis_resolution_entry(entry)
    return entry


def validate_calendar_resolution_entry(entry: dict[str, object]) -> None:
    """Validate one governed calendar resolution entry."""
    _validate_prohibited_fields(entry)
    _validate_required_string_fields(
        entry,
        _CALENDAR_REQUIRED_ENTRY_FIELDS,
        error_prefix="Calendar resolution entry",
    )
    _validate_common_resolution_identity(
        entry,
        expected_asset_family=CALENDAR_ASSET_FAMILY,
        expected_resolution_role=CALENDAR_RESOLUTION_ROLE,
        expected_content_policy=CALENDAR_CONTENT_POLICY,
        error_prefix="Calendar resolution entry",
    )


def validate_planning_basis_resolution_entry(entry: dict[str, object]) -> None:
    """Validate one governed planning-basis resolution entry."""
    _validate_prohibited_fields(entry)
    _validate_required_string_fields(
        entry,
        _PLANNING_BASIS_REQUIRED_ENTRY_FIELDS,
        error_prefix="Planning-basis resolution entry",
    )
    _validate_common_resolution_identity(
        entry,
        expected_asset_family=PLANNING_BASIS_ASSET_FAMILY,
        expected_resolution_role=PLANNING_BASIS_RESOLUTION_ROLE,
        expected_content_policy=PLANNING_BASIS_CONTENT_POLICY,
        error_prefix="Planning-basis resolution entry",
    )


def build_calendar_resolution_registry(
    entries: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    """Build a lookup-keyed calendar registry and reject duplicate entries."""
    registry: dict[str, dict[str, object]] = {}
    for entry in entries:
        validate_calendar_resolution_entry(entry)
        _add_entry_by_lookup_key(
            registry,
            entry,
            duplicate_error_prefix="Duplicate calendar resolution entry",
        )
    return registry


def build_planning_basis_resolution_registry(
    entries: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    """Build a lookup-keyed planning-basis registry and reject duplicates."""
    registry: dict[str, dict[str, object]] = {}
    for entry in entries:
        validate_planning_basis_resolution_entry(entry)
        _add_entry_by_lookup_key(
            registry,
            entry,
            duplicate_error_prefix="Duplicate planning-basis resolution entry",
        )
    return registry


def resolve_calendar_family(
    *,
    registry: dict[str, dict[str, object]],
    calendar_id: str,
    calendar_version: str,
    caller_context_ref: str,
) -> dict[str, object]:
    """Resolve a governed calendar family by exact version-pinned key."""
    caller_context = _require_non_empty_string(
        caller_context_ref,
        field_name="caller_context_ref",
        error_prefix="Calendar resolution request",
    )
    lookup_key = build_calendar_resolution_lookup_key(
        calendar_id=calendar_id,
        calendar_version=calendar_version,
    )
    entry = registry.get(lookup_key)
    if entry is None:
        raise ValueError(
            "Calendar resolution failed closed because no exact version-pinned "
            f"entry exists for lookup_key {lookup_key!r}."
        )

    validate_calendar_resolution_entry(entry)
    return {
        "checkpoint": RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION,
        "resolution_result": "resolved",
        "resolution_family": CALENDAR_ASSET_FAMILY,
        "caller_context_ref": caller_context,
        "resolved_lookup_key": lookup_key,
        "resolved_identity": _resolved_identity_from_entry(entry),
        "calendar_record_ref": entry["calendar_record_ref"],
        "calendar_family": entry["calendar_family"],
        "workday_model_ref": entry["workday_model_ref"],
        "timezone_policy_ref": entry["timezone_policy_ref"],
        "core_engine_input_policy": CALENDAR_PLANNING_CORE_INPUT_POLICY,
        "no_arithmetic_policy": CALENDAR_PLANNING_NO_ARITHMETIC_POLICY,
        "failure_policy": CALENDAR_PLANNING_FAILURE_POLICY,
        "content_policy": CALENDAR_CONTENT_POLICY,
        "asset_payload_included": False,
        "calendar_arithmetic_performed": False,
        "schedule_generated": False,
    }


def resolve_planning_basis(
    *,
    registry: dict[str, dict[str, object]],
    planning_basis_id: str,
    planning_basis_version: str,
    caller_context_ref: str,
) -> dict[str, object]:
    """Resolve governed planning-basis data by exact version-pinned key."""
    caller_context = _require_non_empty_string(
        caller_context_ref,
        field_name="caller_context_ref",
        error_prefix="Planning-basis resolution request",
    )
    lookup_key = build_planning_basis_resolution_lookup_key(
        planning_basis_id=planning_basis_id,
        planning_basis_version=planning_basis_version,
    )
    entry = registry.get(lookup_key)
    if entry is None:
        raise ValueError(
            "Planning-basis resolution failed closed because no exact "
            f"version-pinned entry exists for lookup_key {lookup_key!r}."
        )

    validate_planning_basis_resolution_entry(entry)
    return {
        "checkpoint": RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION,
        "resolution_result": "resolved",
        "resolution_family": PLANNING_BASIS_ASSET_FAMILY,
        "caller_context_ref": caller_context,
        "resolved_lookup_key": lookup_key,
        "resolved_identity": _resolved_identity_from_entry(entry),
        "planning_basis_record_ref": entry["planning_basis_record_ref"],
        "duration_source_ref": entry["duration_source_ref"],
        "dependency_source_ref": entry["dependency_source_ref"],
        "calendar_requirement_ref": entry["calendar_requirement_ref"],
        "core_engine_input_policy": CALENDAR_PLANNING_CORE_INPUT_POLICY,
        "no_arithmetic_policy": CALENDAR_PLANNING_NO_ARITHMETIC_POLICY,
        "failure_policy": CALENDAR_PLANNING_FAILURE_POLICY,
        "content_policy": PLANNING_BASIS_CONTENT_POLICY,
        "asset_payload_included": False,
        "duration_calculation_performed": False,
        "plan_calculated": False,
        "schedule_generated": False,
    }


def _build_resolution_lookup_key(
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


def _build_resolution_identity(
    *,
    asset_family: str,
    asset_id: str,
    asset_version: str,
    resolution_role: str,
    content_policy: str,
) -> dict[str, str]:
    parsed_ref = parse_version_pinned_asset_ref(
        build_version_pinned_asset_ref(
            asset_id=asset_id,
            asset_version=asset_version,
        )
    )
    return {
        "checkpoint": RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION,
        "asset_family": asset_family,
        "asset_id": parsed_ref["asset_id"],
        "asset_version": parsed_ref["asset_version"],
        "asset_ref": parsed_ref["asset_ref"],
        "lookup_key": f"{asset_family}:{parsed_ref['asset_ref']}",
        "resolution_role": resolution_role,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "core_engine_input_policy": CALENDAR_PLANNING_CORE_INPUT_POLICY,
        "no_arithmetic_policy": CALENDAR_PLANNING_NO_ARITHMETIC_POLICY,
        "failure_policy": CALENDAR_PLANNING_FAILURE_POLICY,
        "content_policy": content_policy,
    }


def _validate_common_resolution_identity(
    entry: dict[str, object],
    *,
    expected_asset_family: str,
    expected_resolution_role: str,
    expected_content_policy: str,
    error_prefix: str,
) -> None:
    _validate_expected_exact_value(
        entry,
        field_name="checkpoint",
        expected_value=RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="contract_version",
        expected_value=RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="asset_family",
        expected_value=expected_asset_family,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="resolution_role",
        expected_value=expected_resolution_role,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="source_truth_policy",
        expected_value=RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="core_engine_input_policy",
        expected_value=CALENDAR_PLANNING_CORE_INPUT_POLICY,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="no_arithmetic_policy",
        expected_value=CALENDAR_PLANNING_NO_ARITHMETIC_POLICY,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="failure_policy",
        expected_value=CALENDAR_PLANNING_FAILURE_POLICY,
        error_prefix=error_prefix,
    )
    _validate_expected_exact_value(
        entry,
        field_name="content_policy",
        expected_value=expected_content_policy,
        error_prefix=error_prefix,
    )

    parsed_ref = parse_version_pinned_asset_ref(str(entry["asset_ref"]))
    if entry["asset_id"] != parsed_ref["asset_id"]:
        raise ValueError(
            f"{error_prefix} declares a non-canonical asset_id: "
            f"expected {parsed_ref['asset_id']!r}, got {entry['asset_id']!r}."
        )
    if entry["asset_version"] != parsed_ref["asset_version"]:
        raise ValueError(
            f"{error_prefix} declares a non-canonical asset_version: "
            f"expected {parsed_ref['asset_version']!r}, got "
            f"{entry['asset_version']!r}."
        )

    expected_lookup_key = f"{expected_asset_family}:{parsed_ref['asset_ref']}"
    if entry["lookup_key"] != expected_lookup_key:
        raise ValueError(
            f"{error_prefix} declares an invalid lookup_key: "
            f"expected {expected_lookup_key!r}, got {entry['lookup_key']!r}."
        )


def _resolved_identity_from_entry(entry: dict[str, object]) -> dict[str, object]:
    return {
        "checkpoint": entry["checkpoint"],
        "contract_version": entry["contract_version"],
        "asset_family": entry["asset_family"],
        "asset_id": entry["asset_id"],
        "asset_version": entry["asset_version"],
        "asset_ref": entry["asset_ref"],
        "lookup_key": entry["lookup_key"],
        "source_truth_policy": entry["source_truth_policy"],
        "core_engine_input_policy": entry["core_engine_input_policy"],
        "no_arithmetic_policy": entry["no_arithmetic_policy"],
    }


def _add_entry_by_lookup_key(
    registry: dict[str, dict[str, object]],
    entry: dict[str, object],
    *,
    duplicate_error_prefix: str,
) -> None:
    lookup_key = str(entry["lookup_key"])
    if lookup_key in registry:
        raise ValueError(f"{duplicate_error_prefix} for lookup_key {lookup_key!r}.")
    registry[lookup_key] = dict(entry)


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
    for field_name in _PROHIBITED_RESOLUTION_FIELDS:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in calendar/planning-basis resolution."
            )
