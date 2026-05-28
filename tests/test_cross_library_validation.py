import pytest

from asbp.cross_library_validation import (
    assert_cross_library_validation_passes,
    assert_default_cross_library_validation_passes,
    build_cross_library_validation_issue_id,
    validate_cross_library_runtime,
    validate_default_cross_library_baseline,
)
from asbp.source_library_baseline_store import (
    load_default_source_library_baseline_runtime,
)


def _issue_codes(result):
    return {issue.issue_code for issue in result.issues}


def _first_mapping_by_kind(runtime, mapping_kind: str):
    for mapping in runtime.mapping_library.mappings:
        if mapping.mapping_kind == mapping_kind:
            return mapping
    raise AssertionError(f"Mapping kind not found: {mapping_kind}")


def test_default_cross_library_validation_passes():
    result = validate_default_cross_library_baseline()

    assert result.status == "passed"
    assert result.issues == []
    assert result.checked_families == [
        "baseline",
        "task_pools",
        "profiles",
        "calendars",
        "planning_basis",
        "mappings",
        "standards_bundles",
    ]


def test_default_cross_library_validation_assertion_passes():
    assert_default_cross_library_validation_passes()


def test_cross_library_validation_issue_id_is_deterministic():
    assert build_cross_library_validation_issue_id(
        "DANGLING_PROFILE_REF",
        ["MAP-TEST@v1", "PROF-MISSING@v1"],
    ) == "M27.9::DANGLING_PROFILE_REF::MAP-TEST@v1|PROF-MISSING@v1"


def test_validation_detects_missing_duration_ref_coverage():
    runtime = load_default_source_library_baseline_runtime()
    runtime.task_pool_library.task_pools[0].tasks[
        0
    ].duration_ref.duration_ref_id = "MISSING_DURATION_REF_DUR"

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "UNCOVERED_DURATION_REF" in _issue_codes(result)
    assert any(
        "MISSING_DURATION_REF_DUR" in issue.related_ids
        for issue in result.issues
    )


def test_validation_detects_dangling_profile_mapping_reference():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "preset_to_profile")
    mapping.target_refs[0].reference_id = "PROF-MISSING@v1"

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "DANGLING_PROFILE_REF" in _issue_codes(result)


def test_validation_detects_dangling_task_pool_mapping_reference():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "selector_to_task_pool")
    mapping.target_refs[0].reference_id = "TP-MISSING@v1"

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "DANGLING_TASK_POOL_REF" in _issue_codes(result)


def test_validation_detects_dangling_atomic_task_mapping_reference():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "task_to_document")
    mapping.source_refs[0].reference_id = "TP-PE-E2E-QUAL@v1::MISSING-TASK"

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "DANGLING_ATOMIC_TASK_REF" in _issue_codes(result)


def test_validation_detects_dangling_standards_bundle_mapping_reference():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "standard_to_template")
    mapping.source_refs[0].reference_id = "SB-MISSING@v1"

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "DANGLING_STANDARDS_BUNDLE_REF" in _issue_codes(result)


def test_validation_accepts_resolved_standards_bundle_mapping_reference():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "standard_to_template")

    assert mapping.source_refs[0].reference_type == "standard_bundle"
    assert mapping.source_refs[0].reference_status == "resolved_source"

    result = validate_cross_library_runtime(runtime)

    assert result.status == "passed"


def test_validation_detects_future_reference_without_resolution_checkpoint():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "task_to_document")
    mapping.target_refs[0].resolution_checkpoint = None

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "FUTURE_REF_WITHOUT_RESOLUTION" in _issue_codes(result)


def test_validation_detects_resolved_future_document_reference():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "task_to_document")
    mapping.target_refs[0].reference_status = "resolved_source"
    mapping.target_refs[0].resolution_checkpoint = None

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "RESOLVED_FUTURE_REF" in _issue_codes(result)


def test_validation_detects_resolved_future_template_reference():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "standard_to_template")
    mapping.target_refs[0].reference_status = "resolved_source"
    mapping.target_refs[0].resolution_checkpoint = None

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "RESOLVED_FUTURE_REF" in _issue_codes(result)


def test_validation_detects_empty_calendar_library():
    runtime = load_default_source_library_baseline_runtime()
    runtime.calendar_library.calendars = []

    result = validate_cross_library_runtime(runtime)

    assert result.status == "failed"
    assert "EMPTY_LIBRARY" in _issue_codes(result)


def test_validation_assertion_raises_clear_error_on_failure():
    runtime = load_default_source_library_baseline_runtime()
    mapping = _first_mapping_by_kind(runtime, "preset_to_profile")
    mapping.target_refs[0].reference_id = "PROF-MISSING@v1"

    with pytest.raises(ValueError) as exc_info:
        assert_cross_library_validation_passes(runtime)

    assert "Cross-library validation failed" in str(exc_info.value)
    assert "DANGLING_PROFILE_REF" in str(exc_info.value)
