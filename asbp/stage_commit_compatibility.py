from __future__ import annotations

from asbp.calendar_source_store import get_calendar_by_id
from asbp.mapping_source_store import list_mappings_by_kind
from asbp.planning_basis_source_store import get_duration_source_by_ref_id
from asbp.source_library_baseline_store import (
    load_default_source_library_baseline_runtime,
)
from asbp.stage_commit_compatibility_model import (
    InstantiatedTaskCompatibilityModel,
    PlanningInputCompatibilityModel,
    SourceSelectionCompatibilityModel,
    StageCommitCompatibilityResultModel,
)
from asbp.state_model import TaskCollectionModel, TaskModel
from asbp.task_pool_source_store import (
    build_task_source_definition_id,
    get_task_pool_by_id,
)


def build_default_stage_commit_compatibility_path(
    selector_context_id: str,
    work_package_id: str,
    *,
    collection_id: str = "TC-001",
    calendar_id: str = "CAL-CAIRO-FIVE-DAY-WORKWEEK@v1",
) -> StageCommitCompatibilityResultModel:
    runtime = load_default_source_library_baseline_runtime()

    task_pool_id = resolve_task_pool_id_for_selector_context(
        runtime.mapping_library,
        selector_context_id,
    )
    task_pool = get_task_pool_by_id(runtime.task_pool_library, task_pool_id)

    source_selection = SourceSelectionCompatibilityModel(
        selector_context_id=selector_context_id,
        task_pool_id=task_pool.task_pool_id,
    )
    staged_tasks = build_staged_task_candidates_from_task_pool(
        task_pool,
        work_package_id,
    )
    staged_collection = build_staged_collection_candidate(
        task_pool_id=task_pool.task_pool_id,
        task_ids=[candidate.task.task_id for candidate in staged_tasks],
        work_package_id=work_package_id,
        collection_id=collection_id,
    )
    committed_collection = build_committed_collection_candidate(staged_collection)
    planning_input = build_planning_input_candidate(
        committed_collection=committed_collection,
        instantiated_tasks=staged_tasks,
        planning_basis_library=runtime.planning_basis_library,
        calendar_library=runtime.calendar_library,
        source_task_pool_id=task_pool.task_pool_id,
        calendar_id=calendar_id,
    )

    return StageCommitCompatibilityResultModel(
        source_selection=source_selection,
        staged_tasks=staged_tasks,
        staged_collection=staged_collection,
        committed_collection=committed_collection,
        planning_input=planning_input,
    )


def resolve_task_pool_id_for_selector_context(
    mapping_library,
    selector_context_id: str,
) -> str:
    matching_task_pool_ids: list[str] = []

    for mapping in list_mappings_by_kind(
        mapping_library,
        "selector_to_task_pool",
    ):
        source_matches = [
            reference
            for reference in mapping.source_refs
            if reference.reference_type == "selector_context"
            and reference.reference_status == "resolved_source"
            and reference.reference_id == selector_context_id
        ]
        if not source_matches:
            continue

        task_pool_targets = [
            reference.reference_id
            for reference in mapping.target_refs
            if reference.reference_type == "task_pool"
            and reference.reference_status == "resolved_source"
        ]

        if len(task_pool_targets) != 1:
            raise ValueError(
                "Selector mapping must resolve exactly one task pool: "
                f"{mapping.mapping_id}"
            )

        matching_task_pool_ids.append(task_pool_targets[0])

    if not matching_task_pool_ids:
        raise ValueError(
            "Selector context does not resolve to a task pool: "
            f"{selector_context_id}"
        )

    unique_task_pool_ids = set(matching_task_pool_ids)
    if len(unique_task_pool_ids) != 1:
        raise ValueError(
            "Selector context resolves ambiguously to multiple task pools: "
            f"{selector_context_id}"
        )

    return matching_task_pool_ids[0]


def build_staged_task_candidates_from_task_pool(
    task_pool,
    work_package_id: str,
) -> list[InstantiatedTaskCompatibilityModel]:
    atomic_task_to_task_id = {
        atomic_task.atomic_task_id: f"TASK-{index:03d}"
        for index, atomic_task in enumerate(task_pool.tasks, start=1)
    }

    staged_task_candidates: list[InstantiatedTaskCompatibilityModel] = []

    for index, atomic_task in enumerate(task_pool.tasks, start=1):
        dependency_task_ids: list[str] = []
        for dependency in atomic_task.dependencies:
            if dependency.atomic_task_id not in atomic_task_to_task_id:
                raise ValueError(
                    "Task-pool dependency cannot be instantiated because "
                    "the source dependency is missing: "
                    f"{task_pool.task_pool_id}::{atomic_task.atomic_task_id} -> "
                    f"{dependency.atomic_task_id}"
                )
            dependency_task_ids.append(
                atomic_task_to_task_id[dependency.atomic_task_id]
            )

        source_definition_id = build_task_source_definition_id(
            task_pool.task_pool_id,
            atomic_task.atomic_task_id,
        )
        task = TaskModel(
            task_id=atomic_task_to_task_id[atomic_task.atomic_task_id],
            order=index,
            title=atomic_task.title,
            description=atomic_task.purpose,
            owner=atomic_task.owner_role,
            duration=None,
            start_date=None,
            end_date=None,
            task_key=atomic_task.atomic_task_id.lower(),
            work_package_id=work_package_id,
            instantiation_mode="preset_resolved",
            source_definition_kind="task_pool",
            source_definition_id=source_definition_id,
            status="planned",
            dependencies=dependency_task_ids,
        )

        staged_task_candidates.append(
            InstantiatedTaskCompatibilityModel(
                task=task,
                atomic_task_id=atomic_task.atomic_task_id,
                duration_ref_id=atomic_task.duration_ref.duration_ref_id,
            )
        )

    return staged_task_candidates


def build_staged_collection_candidate(
    *,
    task_pool_id: str,
    task_ids: list[str],
    work_package_id: str,
    collection_id: str = "TC-001",
) -> TaskCollectionModel:
    if not task_ids:
        raise ValueError("Staged collection candidate requires task_ids")

    return TaskCollectionModel(
        collection_id=collection_id,
        title=f"Staged task-pool selection: {task_pool_id}",
        collection_state="staged",
        work_package_id=work_package_id,
        task_ids=task_ids,
    )


def build_committed_collection_candidate(
    staged_collection: TaskCollectionModel,
) -> TaskCollectionModel:
    if staged_collection.collection_state != "staged":
        raise ValueError(
            "Committed collection candidate must derive from staged collection"
        )

    return TaskCollectionModel(
        collection_id=staged_collection.collection_id,
        title=staged_collection.title.replace("Staged", "Committed", 1),
        collection_state="committed",
        work_package_id=staged_collection.work_package_id,
        task_ids=list(staged_collection.task_ids),
    )


def build_planning_input_candidate(
    *,
    committed_collection: TaskCollectionModel,
    instantiated_tasks: list[InstantiatedTaskCompatibilityModel],
    planning_basis_library,
    calendar_library,
    source_task_pool_id: str,
    calendar_id: str,
) -> PlanningInputCompatibilityModel:
    if committed_collection.collection_state != "committed":
        raise ValueError(
            "Planning input must derive from committed instantiated tasks"
        )

    committed_task_ids = list(committed_collection.task_ids)
    instantiated_task_ids = [
        instantiated_task.task.task_id
        for instantiated_task in instantiated_tasks
    ]
    if committed_task_ids != instantiated_task_ids:
        raise ValueError(
            "Committed collection task_ids must match instantiated task ids"
        )

    for instantiated_task in instantiated_tasks:
        if instantiated_task.task.instantiation_mode != "preset_resolved":
            raise ValueError(
                "Planning input requires preset-resolved instantiated tasks"
            )
        if instantiated_task.task.source_definition_kind != "task_pool":
            raise ValueError(
                "Planning input requires task_pool source_definition_kind"
            )
        if instantiated_task.task.source_definition_id is None:
            raise ValueError(
                "Planning input requires task source_definition_id"
            )
        get_duration_source_by_ref_id(
            planning_basis_library,
            instantiated_task.duration_ref_id,
        )

    get_calendar_by_id(calendar_library, calendar_id)

    return PlanningInputCompatibilityModel(
        work_package_id=committed_collection.work_package_id,
        committed_collection_id=committed_collection.collection_id,
        source_task_pool_id=source_task_pool_id,
        task_ids=committed_task_ids,
        duration_ref_ids=[
            instantiated_task.duration_ref_id
            for instantiated_task in instantiated_tasks
        ],
        planning_basis_library_id=planning_basis_library.library_id,
        calendar_id=calendar_id,
    )
