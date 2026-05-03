import pytest

from asbp.resolver_registry import (
    CALENDAR_ASSET_FAMILY,
    CALENDAR_CONTENT_POLICY,
    CALENDAR_PLANNING_CORE_INPUT_POLICY,
    CALENDAR_PLANNING_NO_ARITHMETIC_POLICY,
    CALENDAR_RESOLUTION_ROLE,
    PLANNING_BASIS_ASSET_FAMILY,
    PLANNING_BASIS_CONTENT_POLICY,
    PLANNING_BASIS_RESOLUTION_ROLE,
    RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID,
    RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION,
    build_calendar_planning_resolution_baseline,
    build_calendar_resolution_entry,
    build_calendar_resolution_lookup_key,
    build_calendar_resolution_registry,
    build_planning_basis_resolution_entry,
    build_planning_basis_resolution_lookup_key,
    build_planning_basis_resolution_registry,
    resolve_calendar_family,
    resolve_planning_basis,
    validate_calendar_resolution_entry,
    validate_planning_basis_resolution_entry,
)


def _calendar_entry() -> dict[str, str]:
    return build_calendar_resolution_entry(
        calendar_id="EG_CAIRO_5X8",
        calendar_version="v1",
        calendar_record_ref="compiled://calendars/EG_CAIRO_5X8@v1",
        calendar_family="five_by_eight_workweek",
        workday_model_ref="workday-model://5x8",
        timezone_policy_ref="timezone-policy://Africa/Cairo",
    )


def _planning_basis_entry() -> dict[str, str]:
    return build_planning_basis_resolution_entry(
        planning_basis_id="CQV_STANDARD_PLANNING",
        planning_basis_version="v1",
        planning_basis_record_ref="compiled://planning_basis/CQV_STANDARD_PLANNING@v1",
        duration_source_ref="duration-source://cqv-standard",
        dependency_source_ref="dependency-source://cqv-standard",
        calendar_requirement_ref="calendar-requirement://workday-calendar-required",
    )


def test_calendar_planning_resolution_baseline_exposes_m14_3_rules() -> None:
    baseline = build_calendar_planning_resolution_baseline()

    assert baseline["checkpoint"] == RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID
    assert (
        baseline["contract_version"]
        == RESOLVER_REGISTRY_CALENDAR_PLANNING_CONTRACT_VERSION
    )
    assert CALENDAR_ASSET_FAMILY in baseline["calendar_resolution_families"]
    assert (
        PLANNING_BASIS_ASSET_FAMILY
        in baseline["planning_basis_resolution_families"]
    )
    assert baseline["calendar_resolution_role"] == CALENDAR_RESOLUTION_ROLE
    assert (
        baseline["planning_basis_resolution_role"]
        == PLANNING_BASIS_RESOLUTION_ROLE
    )
    assert baseline["core_engine_input_policy"] == CALENDAR_PLANNING_CORE_INPUT_POLICY
    assert baseline["no_arithmetic_policy"] == CALENDAR_PLANNING_NO_ARITHMETIC_POLICY
    assert "calendar_arithmetic" in baseline["not_owned_by_m14_3"]
    assert "schedule_generation" in baseline["not_owned_by_m14_3"]


def test_build_calendar_resolution_entry_requires_version_pinned_identity() -> None:
    entry = _calendar_entry()

    assert entry["checkpoint"] == RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID
    assert entry["asset_family"] == CALENDAR_ASSET_FAMILY
    assert entry["asset_id"] == "EG_CAIRO_5X8"
    assert entry["asset_version"] == "v1"
    assert entry["asset_ref"] == "EG_CAIRO_5X8@v1"
    assert entry["lookup_key"] == "calendar:EG_CAIRO_5X8@v1"
    assert entry["resolution_role"] == CALENDAR_RESOLUTION_ROLE
    assert entry["content_policy"] == CALENDAR_CONTENT_POLICY
    validate_calendar_resolution_entry(entry)


def test_build_planning_basis_resolution_entry_requires_version_pinned_identity() -> None:
    entry = _planning_basis_entry()

    assert entry["checkpoint"] == RESOLVER_REGISTRY_CALENDAR_PLANNING_CHECKPOINT_ID
    assert entry["asset_family"] == PLANNING_BASIS_ASSET_FAMILY
    assert entry["asset_id"] == "CQV_STANDARD_PLANNING"
    assert entry["asset_version"] == "v1"
    assert entry["asset_ref"] == "CQV_STANDARD_PLANNING@v1"
    assert entry["lookup_key"] == "planning_basis:CQV_STANDARD_PLANNING@v1"
    assert entry["resolution_role"] == PLANNING_BASIS_RESOLUTION_ROLE
    assert entry["content_policy"] == PLANNING_BASIS_CONTENT_POLICY
    validate_planning_basis_resolution_entry(entry)


def test_build_calendar_resolution_lookup_key_is_canonical() -> None:
    lookup_key = build_calendar_resolution_lookup_key(
        calendar_id="eg_cairo_5x8",
        calendar_version="V1",
    )

    assert lookup_key == "calendar:EG_CAIRO_5X8@v1"


def test_build_planning_basis_resolution_lookup_key_is_canonical() -> None:
    lookup_key = build_planning_basis_resolution_lookup_key(
        planning_basis_id="cqv_standard_planning",
        planning_basis_version="V1",
    )

    assert lookup_key == "planning_basis:CQV_STANDARD_PLANNING@v1"


def test_calendar_resolution_rejects_latest_or_current_versions() -> None:
    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_calendar_resolution_entry(
            calendar_id="EG_CAIRO_5X8",
            calendar_version="latest",
            calendar_record_ref="compiled://calendars/EG_CAIRO_5X8@latest",
            calendar_family="five_by_eight_workweek",
            workday_model_ref="workday-model://5x8",
            timezone_policy_ref="timezone-policy://Africa/Cairo",
        )

    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_calendar_resolution_lookup_key(
            calendar_id="EG_CAIRO_5X8",
            calendar_version="current",
        )


def test_planning_basis_resolution_rejects_latest_or_current_versions() -> None:
    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_planning_basis_resolution_entry(
            planning_basis_id="CQV_STANDARD_PLANNING",
            planning_basis_version="current",
            planning_basis_record_ref="compiled://planning_basis/current",
            duration_source_ref="duration-source://cqv-standard",
            dependency_source_ref="dependency-source://cqv-standard",
            calendar_requirement_ref="calendar-requirement://workday-calendar-required",
        )

    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_planning_basis_resolution_lookup_key(
            planning_basis_id="CQV_STANDARD_PLANNING",
            planning_basis_version="latest",
        )


def test_calendar_resolution_rejects_arithmetic_and_payload_fields() -> None:
    entry = _calendar_entry()
    entry["calendar_arithmetic"] = True

    with pytest.raises(ValueError, match="calendar_arithmetic is not allowed"):
        validate_calendar_resolution_entry(entry)

    entry = _calendar_entry()
    entry["asset_payload"] = {"weekend_days": ["FR", "SA"]}

    with pytest.raises(ValueError, match="asset_payload is not allowed"):
        validate_calendar_resolution_entry(entry)


def test_planning_basis_resolution_rejects_calculation_and_payload_fields() -> None:
    entry = _planning_basis_entry()
    entry["task_duration_calculation"] = True

    with pytest.raises(ValueError, match="task_duration_calculation is not allowed"):
        validate_planning_basis_resolution_entry(entry)

    entry = _planning_basis_entry()
    entry["calculated_schedule"] = {"task": "T001"}

    with pytest.raises(ValueError, match="calculated_schedule is not allowed"):
        validate_planning_basis_resolution_entry(entry)


def test_build_calendar_resolution_registry_rejects_duplicate_lookup_keys() -> None:
    entry = _calendar_entry()

    with pytest.raises(ValueError, match="Duplicate calendar resolution entry"):
        build_calendar_resolution_registry([entry, dict(entry)])


def test_build_planning_basis_resolution_registry_rejects_duplicate_lookup_keys() -> None:
    entry = _planning_basis_entry()

    with pytest.raises(ValueError, match="Duplicate planning-basis resolution entry"):
        build_planning_basis_resolution_registry([entry, dict(entry)])


def test_resolve_calendar_family_returns_metadata_only() -> None:
    registry = build_calendar_resolution_registry([_calendar_entry()])

    result = resolve_calendar_family(
        registry=registry,
        calendar_id="EG_CAIRO_5X8",
        calendar_version="v1",
        caller_context_ref="planning_engine",
    )

    assert result["resolution_result"] == "resolved"
    assert result["resolution_family"] == CALENDAR_ASSET_FAMILY
    assert result["resolved_lookup_key"] == "calendar:EG_CAIRO_5X8@v1"
    assert result["calendar_record_ref"] == "compiled://calendars/EG_CAIRO_5X8@v1"
    assert result["asset_payload_included"] is False
    assert result["calendar_arithmetic_performed"] is False
    assert result["schedule_generated"] is False
    assert "calculated_start_date" not in result
    assert result["core_engine_input_policy"] == CALENDAR_PLANNING_CORE_INPUT_POLICY


def test_resolve_planning_basis_returns_metadata_only() -> None:
    registry = build_planning_basis_resolution_registry([_planning_basis_entry()])

    result = resolve_planning_basis(
        registry=registry,
        planning_basis_id="CQV_STANDARD_PLANNING",
        planning_basis_version="v1",
        caller_context_ref="planning_engine",
    )

    assert result["resolution_result"] == "resolved"
    assert result["resolution_family"] == PLANNING_BASIS_ASSET_FAMILY
    assert result["resolved_lookup_key"] == "planning_basis:CQV_STANDARD_PLANNING@v1"
    assert (
        result["planning_basis_record_ref"]
        == "compiled://planning_basis/CQV_STANDARD_PLANNING@v1"
    )
    assert result["asset_payload_included"] is False
    assert result["duration_calculation_performed"] is False
    assert result["plan_calculated"] is False
    assert result["schedule_generated"] is False
    assert "calculated_finish_date" not in result
    assert result["core_engine_input_policy"] == CALENDAR_PLANNING_CORE_INPUT_POLICY


def test_resolve_calendar_family_fails_closed_for_missing_exact_key() -> None:
    registry = build_calendar_resolution_registry([_calendar_entry()])

    with pytest.raises(ValueError, match="Calendar resolution failed closed"):
        resolve_calendar_family(
            registry=registry,
            calendar_id="EG_CAIRO_5X8",
            calendar_version="v2",
            caller_context_ref="planning_engine",
        )


def test_resolve_planning_basis_fails_closed_for_missing_exact_key() -> None:
    registry = build_planning_basis_resolution_registry([_planning_basis_entry()])

    with pytest.raises(ValueError, match="Planning-basis resolution failed closed"):
        resolve_planning_basis(
            registry=registry,
            planning_basis_id="CQV_STANDARD_PLANNING",
            planning_basis_version="v2",
            caller_context_ref="planning_engine",
        )
