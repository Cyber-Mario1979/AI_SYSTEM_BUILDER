from copy import deepcopy
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from asbp.planning_basis_source_model import PlanningBasisLibraryModel
from asbp.planning_basis_source_store import (
    assert_task_pool_duration_refs_covered,
    build_duration_source_definition_id,
    find_missing_task_pool_duration_refs,
    get_duration_source_by_ref_id,
    list_duration_ref_ids,
    load_default_planning_basis_library,
    load_planning_basis_library_from_payload,
)
from asbp.task_pool_source_store import load_default_task_pool_library


EXPECTED_DURATION_REFS = [
    "PE_E2E_SCOPE_DUR",
    "PE_E2E_READINESS_DUR",
    "PE_E2E_RISK_DUR",
    "PE_E2E_IQ_DUR",
    "PE_E2E_OQ_DUR",
    "PE_E2E_PQ_DUR",
    "PE_E2E_CLOSEOUT_DUR",
    "QCLAB_SCOPE_DUR",
    "QCLAB_CAL_STATUS_DUR",
    "QCLAB_URS_RISK_DUR",
    "QCLAB_IQOQ_DUR",
    "QCLAB_CSV_LINK_DUR",
    "QCLAB_CLOSEOUT_DUR",
    "CRHVAC_SCOPE_DUR",
    "CRHVAC_DESIGN_READINESS_DUR",
    "CRHVAC_INSTALL_CHECK_DUR",
    "CRHVAC_OPERATIONAL_TESTS_DUR",
    "CRHVAC_ENV_PERFORMANCE_DUR",
    "CRHVAC_CLOSEOUT_DUR",
    "UT_SCOPE_DUR",
    "UT_DESIGN_READINESS_DUR",
    "UT_IQ_DUR",
    "UT_OQ_DUR",
    "UT_PQ_SAMPLING_DUR",
    "UT_CLOSEOUT_DUR",
    "CSV_SCOPE_DUR",
    "CSV_URS_RISK_DUR",
    "CSV_SPEC_TRACE_DUR",
    "CSV_TESTING_DUR",
    "CSV_ACCESS_DI_DUR",
    "CSV_CLOSEOUT_DUR",
    "MF_CONTEXT_CAPTURE_DUR",
    "MF_ROUTE_ASSESSMENT_DUR",
    "MF_MANUAL_CONFIRM_DUR",
    "MF_TEMPORARY_PLAN_DUR",
    "MF_REVIEW_DECISION_DUR"
]


def _minimal_duration_source_payload() -> dict:
    return {
        "duration_ref_id": "TEST_SCOPE_DUR",
        "version": "v1",
        "status": "starter_runtime_source",
        "display_name": "Test scope duration",
        "estimate_type": "starter_estimate",
        "estimation_source_status": "starter_baseline",
        "duration_unit": "working_day",
        "duration_range": {
            "min_days": 0.5,
            "typical_days": 1.0,
            "max_days": 2.0,
        },
        "scope_rules": [
            {
                "rule_id": "standard_scope_baseline",
                "scope_complexity": "standard",
                "condition": "Standard test scope.",
                "adjustment_guidance": "Human reviewer may amend.",
                "user_amendable": True,
            }
        ],
        "calendar_dependency_status": "calendar_aware_no_capacity_calculation",
        "linked_task_sources": [
            {
                "task_pool_id": "TP-TEST-POOL@v1",
                "atomic_task_id": "TEST-SCOPE",
            }
        ],
        "user_amendable": True,
        "assumption_controls": [
            "Human confirmation is required before planning."
        ],
    }


def _minimal_library_payload(duration_source: dict | None = None) -> dict:
    return {
        "library_id": "TEST_PLANNING_BASIS_LIBRARY@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "duration_sources": [
            duration_source or _minimal_duration_source_payload()
        ],
    }


def _task_pool_library_with_duration_refs(duration_refs: list[str]):
    tasks = [
        SimpleNamespace(
            duration_ref=SimpleNamespace(duration_ref_id=duration_ref)
        )
        for duration_ref in duration_refs
    ]
    task_pool = SimpleNamespace(task_pools=[SimpleNamespace(tasks=tasks)])
    return task_pool


def test_default_starter_planning_basis_library_loads_duration_sources():
    library = load_default_planning_basis_library()

    assert library.library_id == "M27_PLANNING_BASIS_STARTER_LIBRARY@v1"
    assert list_duration_ref_ids(library) == EXPECTED_DURATION_REFS

    source = get_duration_source_by_ref_id(library, "PE_E2E_SCOPE_DUR")
    assert source.duration_range.typical_days == 1.0
    assert source.calendar_dependency_status == (
        "calendar_aware_no_capacity_calculation"
    )


def test_default_planning_basis_covers_default_task_pool_duration_refs():
    planning_basis_library = load_default_planning_basis_library()
    task_pool_library = load_default_task_pool_library()

    assert find_missing_task_pool_duration_refs(
        planning_basis_library,
        task_pool_library,
    ) == []

    assert_task_pool_duration_refs_covered(
        planning_basis_library,
        task_pool_library,
    )


def test_duration_source_definition_id_uses_duration_ref_identity():
    assert build_duration_source_definition_id(
        "PE_E2E_SCOPE_DUR",
    ) == "M27.6::PE_E2E_SCOPE_DUR"


def test_planning_basis_library_rejects_duplicate_duration_refs():
    duration_source = _minimal_duration_source_payload()
    payload = _minimal_library_payload(duration_source)
    payload["duration_sources"].append(deepcopy(duration_source))

    with pytest.raises(ValidationError) as exc_info:
        PlanningBasisLibraryModel(**payload)

    assert "Duplicate duration_ref_id is not allowed: TEST_SCOPE_DUR" in str(
        exc_info.value
    )


def test_duration_source_rejects_invalid_duration_ref_pattern():
    duration_source = _minimal_duration_source_payload()
    duration_source["duration_ref_id"] = "TEST_SCOPE"

    with pytest.raises(ValidationError) as exc_info:
        load_planning_basis_library_from_payload(
            _minimal_library_payload(duration_source)
        )

    assert "duration_ref_id" in str(exc_info.value)


def test_duration_source_rejects_invalid_duration_range_order():
    duration_source = _minimal_duration_source_payload()
    duration_source["duration_range"] = {
        "min_days": 2.0,
        "typical_days": 1.0,
        "max_days": 3.0,
    }

    with pytest.raises(ValidationError) as exc_info:
        load_planning_basis_library_from_payload(
            _minimal_library_payload(duration_source)
        )

    assert "Duration range must satisfy" in str(exc_info.value)


def test_duration_source_rejects_missing_scope_rules():
    duration_source = _minimal_duration_source_payload()
    duration_source["scope_rules"] = []

    with pytest.raises(ValidationError) as exc_info:
        load_planning_basis_library_from_payload(
            _minimal_library_payload(duration_source)
        )

    assert "scope_rules" in str(exc_info.value)


def test_duration_source_rejects_duplicate_linked_task_source():
    duration_source = _minimal_duration_source_payload()
    duration_source["linked_task_sources"].append(
        deepcopy(duration_source["linked_task_sources"][0])
    )

    with pytest.raises(ValidationError) as exc_info:
        load_planning_basis_library_from_payload(
            _minimal_library_payload(duration_source)
        )

    assert "Duplicate linked task source is not allowed" in str(exc_info.value)


def test_duration_source_rejects_blank_assumption_control():
    duration_source = _minimal_duration_source_payload()
    duration_source["assumption_controls"] = [" "]

    with pytest.raises(ValidationError) as exc_info:
        load_planning_basis_library_from_payload(
            _minimal_library_payload(duration_source)
        )

    assert "Blank planning-basis value is not allowed" in str(exc_info.value)


def test_future_mapping_expected_rejects_non_zero_typical_estimate():
    duration_source = _minimal_duration_source_payload()
    duration_source["estimate_type"] = "future_mapping_expected"

    with pytest.raises(ValidationError) as exc_info:
        load_planning_basis_library_from_payload(
            _minimal_library_payload(duration_source)
        )

    assert (
        "future_mapping_expected duration source cannot include a non-zero "
        "typical estimate"
    ) in str(exc_info.value)


def test_duration_ref_coverage_reports_missing_task_pool_refs():
    planning_basis_library = load_planning_basis_library_from_payload(
        _minimal_library_payload()
    )
    task_pool_library = _task_pool_library_with_duration_refs(
        ["TEST_SCOPE_DUR", "MISSING_DUR"]
    )

    assert find_missing_task_pool_duration_refs(
        planning_basis_library,
        task_pool_library,
    ) == ["MISSING_DUR"]

    with pytest.raises(ValueError) as exc_info:
        assert_task_pool_duration_refs_covered(
            planning_basis_library,
            task_pool_library,
        )

    assert "MISSING_DUR" in str(exc_info.value)


def test_missing_duration_source_lookup_raises_clear_error():
    library = load_planning_basis_library_from_payload(
        _minimal_library_payload()
    )

    with pytest.raises(ValueError) as exc_info:
        get_duration_source_by_ref_id(library, "MISSING_DUR")

    assert "Duration source definition not found: MISSING_DUR" in str(
        exc_info.value
    )


def test_persisted_state_payload_is_not_planning_basis_source_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_planning_basis_library_from_payload(persisted_state_payload)

    assert (
        "planning-basis library payload must include duration_sources"
    ) in str(exc_info.value)
