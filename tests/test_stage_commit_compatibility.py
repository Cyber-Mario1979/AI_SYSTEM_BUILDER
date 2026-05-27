import pytest

from asbp.stage_commit_compatibility import (
    build_committed_collection_candidate,
    build_default_stage_commit_compatibility_path,
    build_planning_input_candidate,
    build_staged_collection_candidate,
    build_staged_task_candidates_from_task_pool,
    resolve_task_pool_id_for_selector_context,
)
from asbp.source_library_baseline_store import (
    load_default_source_library_baseline_runtime,
)


def test_default_stage_commit_compatibility_path_builds_planning_input_candidate():
    result = build_default_stage_commit_compatibility_path(
        "SEL-PF-PROCESS-EQUIPMENT-INT-E2E-QUALIFICATION",
        "WP-001",
    )

    assert result.status == "compatible"
    assert result.source_selection.task_pool_id == "TP-PE-E2E-QUAL@v1"
    assert len(result.staged_tasks) == 7
    assert result.staged_collection.collection_state == "staged"
    assert result.committed_collection.collection_state == "committed"
    assert result.planning_input.planning_input_state == "ready_for_planning_input"
    assert result.planning_input.task_ids == [
        candidate.task.task_id for candidate in result.staged_tasks
    ]
    assert result.planning_input.duration_ref_ids[0] == "PE_E2E_SCOPE_DUR"


def test_staged_task_candidates_preserve_source_identity_and_dependencies():
    runtime = load_default_source_library_baseline_runtime()
    task_pool = runtime.task_pool_library.task_pools[0]

    candidates = build_staged_task_candidates_from_task_pool(
        task_pool,
        "WP-001",
    )

    first = candidates[0]
    second = candidates[1]

    assert first.task.task_id == "TASK-001"
    assert first.task.status == "planned"
    assert first.task.instantiation_mode == "preset_resolved"
    assert first.task.source_definition_kind == "task_pool"
    assert first.task.source_definition_id == "TP-PE-E2E-QUAL@v1::PE-E2E-SCOPE"
    assert first.duration_ref_id == "PE_E2E_SCOPE_DUR"

    assert second.task.task_id == "TASK-002"
    assert second.task.dependencies == ["TASK-001"]


def test_selector_context_resolves_to_task_pool_through_mapping_source():
    runtime = load_default_source_library_baseline_runtime()

    assert resolve_task_pool_id_for_selector_context(
        runtime.mapping_library,
        "SEL-PF-CLEANROOM-INT-E2E-QUALIFICATION",
    ) == "TP-CLEANROOM-HVAC-QUAL@v1"


def test_unknown_selector_context_does_not_resolve_to_task_pool():
    runtime = load_default_source_library_baseline_runtime()

    with pytest.raises(ValueError) as exc_info:
        resolve_task_pool_id_for_selector_context(
            runtime.mapping_library,
            "SEL-UNKNOWN",
        )

    assert "Selector context does not resolve to a task pool" in str(
        exc_info.value
    )


def test_committed_collection_must_derive_from_staged_collection():
    source_collection = build_staged_collection_candidate(
        task_pool_id="TP-PE-E2E-QUAL@v1",
        task_ids=["TASK-001"],
        work_package_id="WP-001",
    )
    source_collection.collection_state = "source"

    with pytest.raises(ValueError) as exc_info:
        build_committed_collection_candidate(source_collection)

    assert "must derive from staged collection" in str(exc_info.value)


def test_planning_input_must_derive_from_committed_collection():
    runtime = load_default_source_library_baseline_runtime()
    task_pool = runtime.task_pool_library.task_pools[0]
    candidates = build_staged_task_candidates_from_task_pool(
        task_pool,
        "WP-001",
    )
    staged_collection = build_staged_collection_candidate(
        task_pool_id=task_pool.task_pool_id,
        task_ids=[candidate.task.task_id for candidate in candidates],
        work_package_id="WP-001",
    )

    with pytest.raises(ValueError) as exc_info:
        build_planning_input_candidate(
            committed_collection=staged_collection,
            instantiated_tasks=candidates,
            planning_basis_library=runtime.planning_basis_library,
            calendar_library=runtime.calendar_library,
            source_task_pool_id=task_pool.task_pool_id,
            calendar_id="CAL-CAIRO-FIVE-DAY-WORKWEEK@v1",
        )

    assert "Planning input must derive from committed instantiated tasks" in str(
        exc_info.value
    )


def test_planning_input_rejects_direct_source_without_instantiated_tasks():
    runtime = load_default_source_library_baseline_runtime()
    committed_collection = build_committed_collection_candidate(
        build_staged_collection_candidate(
            task_pool_id="TP-PE-E2E-QUAL@v1",
            task_ids=["TASK-001"],
            work_package_id="WP-001",
        )
    )

    with pytest.raises(ValueError) as exc_info:
        build_planning_input_candidate(
            committed_collection=committed_collection,
            instantiated_tasks=[],
            planning_basis_library=runtime.planning_basis_library,
            calendar_library=runtime.calendar_library,
            source_task_pool_id="TP-PE-E2E-QUAL@v1",
            calendar_id="CAL-CAIRO-FIVE-DAY-WORKWEEK@v1",
        )

    assert "Committed collection task_ids must match instantiated task ids" in str(
        exc_info.value
    )


def test_planning_input_rejects_missing_duration_ref():
    runtime = load_default_source_library_baseline_runtime()
    task_pool = runtime.task_pool_library.task_pools[0]
    candidates = build_staged_task_candidates_from_task_pool(
        task_pool,
        "WP-001",
    )
    candidates[0].duration_ref_id = "MISSING_DUR"
    committed_collection = build_committed_collection_candidate(
        build_staged_collection_candidate(
            task_pool_id=task_pool.task_pool_id,
            task_ids=[candidate.task.task_id for candidate in candidates],
            work_package_id="WP-001",
        )
    )

    with pytest.raises(ValueError) as exc_info:
        build_planning_input_candidate(
            committed_collection=committed_collection,
            instantiated_tasks=candidates,
            planning_basis_library=runtime.planning_basis_library,
            calendar_library=runtime.calendar_library,
            source_task_pool_id=task_pool.task_pool_id,
            calendar_id="CAL-CAIRO-FIVE-DAY-WORKWEEK@v1",
        )

    assert "Duration source definition not found: MISSING_DUR" in str(
        exc_info.value
    )


def test_planning_input_rejects_missing_calendar_ref():
    runtime = load_default_source_library_baseline_runtime()
    task_pool = runtime.task_pool_library.task_pools[0]
    candidates = build_staged_task_candidates_from_task_pool(
        task_pool,
        "WP-001",
    )
    committed_collection = build_committed_collection_candidate(
        build_staged_collection_candidate(
            task_pool_id=task_pool.task_pool_id,
            task_ids=[candidate.task.task_id for candidate in candidates],
            work_package_id="WP-001",
        )
    )

    with pytest.raises(ValueError) as exc_info:
        build_planning_input_candidate(
            committed_collection=committed_collection,
            instantiated_tasks=candidates,
            planning_basis_library=runtime.planning_basis_library,
            calendar_library=runtime.calendar_library,
            source_task_pool_id=task_pool.task_pool_id,
            calendar_id="CAL-MISSING@v1",
        )

    assert "Calendar source definition not found: CAL-MISSING@v1" in str(
        exc_info.value
    )
