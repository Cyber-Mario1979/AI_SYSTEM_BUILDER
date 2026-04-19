from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def _find_work_package_by_id(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
) -> WorkPackageModel | None:
    for work_package in work_packages:
        if work_package.wp_id == wp_id:
            return work_package
    return None


def _build_bound_committed_collections(
    task_collections: list[TaskCollectionModel],
    *,
    wp_id: str,
) -> list[TaskCollectionModel]:
    return [
        task_collection
        for task_collection in task_collections
        if task_collection.collection_state == "committed"
        and task_collection.work_package_id == wp_id
    ]


def _build_committed_task_ids(
    task_collections: list[TaskCollectionModel],
) -> list[str]:
    committed_task_ids: set[str] = set()
    for task_collection in task_collections:
        committed_task_ids.update(task_collection.task_ids)
    return sorted(committed_task_ids)


def _build_work_package_task_ids(
    tasks: list[TaskModel],
    *,
    wp_id: str,
) -> list[str]:
    return sorted(
        task.task_id
        for task in tasks
        if task.work_package_id == wp_id
    )


def _build_work_package_plans(
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> list[PlanningModel]:
    return [
        plan
        for plan in plans
        if plan.work_package_id == wp_id
    ]


def _build_binding_context_blockers(
    work_package: WorkPackageModel,
) -> list[str]:
    selector_context = work_package.selector_context
    if selector_context is None:
        return ["selector_context_missing"]

    blockers: list[str] = []
    if selector_context.scope_intent is None:
        blockers.append("scope_intent_missing")
    if not selector_context.standards_bundles:
        blockers.append("standards_bundles_missing")
    return blockers


def build_work_package_orchestration_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    work_package = _find_work_package_by_id(work_packages, wp_id=wp_id)
    if work_package is None:
        return None

    binding_context_blockers = _build_binding_context_blockers(work_package)
    bound_committed_collections = _build_bound_committed_collections(
        task_collections,
        wp_id=wp_id,
    )
    bound_committed_collection_ids = [
        task_collection.collection_id
        for task_collection in bound_committed_collections
    ]
    bound_committed_task_ids = _build_committed_task_ids(
        bound_committed_collections,
    )
    work_package_task_ids = _build_work_package_task_ids(tasks, wp_id=wp_id)
    work_package_plans = _build_work_package_plans(plans, wp_id=wp_id)
    plan_ids = [plan.plan_id for plan in work_package_plans]

    payload = {
        "wp_id": work_package.wp_id,
        "work_package_status": work_package.status,
        "orchestration_stage": "",
        "blocking_conditions": [],
        "next_actions": [],
        "selector_context_ready": not binding_context_blockers,
        "work_package_task_ids": work_package_task_ids,
        "bound_committed_collection_ids": bound_committed_collection_ids,
        "bound_committed_task_ids": bound_committed_task_ids,
        "plan_ids": plan_ids,
        "selected_plan_id": None,
    }

    if binding_context_blockers:
        payload["orchestration_stage"] = "binding_context_required"
        payload["blocking_conditions"] = binding_context_blockers
        payload["next_actions"] = [
            "Complete deterministic selector context before orchestration can proceed."
        ]
        return payload

    if not bound_committed_collection_ids:
        payload["orchestration_stage"] = "selection_required"
        payload["blocking_conditions"] = ["bound_committed_collection_missing"]
        payload["next_actions"] = [
            "Bind at least one committed collection to the Work Package."
        ]
        return payload

    if not bound_committed_task_ids:
        payload["orchestration_stage"] = "selection_required"
        payload["blocking_conditions"] = ["committed_task_scope_empty"]
        payload["next_actions"] = [
            "Add committed task membership before planning orchestration can proceed."
        ]
        return payload

    committed_plans = [
        plan
        for plan in work_package_plans
        if plan.plan_state == "committed"
    ]
    draft_plans = [
        plan
        for plan in work_package_plans
        if plan.plan_state == "draft"
    ]

    if len(committed_plans) > 1:
        payload["orchestration_stage"] = "blocked"
        payload["blocking_conditions"] = ["multiple_committed_plans"]
        payload["next_actions"] = [
            "Reduce the Work Package to one committed plan before orchestration can continue."
        ]
        return payload

    if not committed_plans and len(draft_plans) > 1:
        payload["orchestration_stage"] = "blocked"
        payload["blocking_conditions"] = ["multiple_draft_plans"]
        payload["next_actions"] = [
            "Reduce the Work Package to one draft plan before orchestration can continue."
        ]
        return payload

    if committed_plans:
        selected_plan = committed_plans[0]
        payload["selected_plan_id"] = selected_plan.plan_id
        payload["orchestration_stage"] = "execution_ready"
        payload["next_actions"] = [
            "Execution-ready deterministic state reached."
        ]
        return payload

    if not draft_plans:
        payload["orchestration_stage"] = "planning_setup_required"
        payload["blocking_conditions"] = ["draft_plan_missing"]
        payload["next_actions"] = [
            "Create one draft plan for the Work Package."
        ]
        return payload

    selected_plan = draft_plans[0]
    payload["selected_plan_id"] = selected_plan.plan_id

    planning_setup_blockers: list[str] = []
    if selected_plan.planning_basis is None:
        planning_setup_blockers.append("planning_basis_missing")
    if selected_plan.planned_start_at is None:
        planning_setup_blockers.append("planned_start_at_missing")
    if selected_plan.planning_calendar is None:
        planning_setup_blockers.append("planning_calendar_missing")

    if planning_setup_blockers:
        payload["orchestration_stage"] = "planning_setup_required"
        payload["blocking_conditions"] = planning_setup_blockers
        payload["next_actions"] = [
            "Complete planning basis, planned start, and planning calendar on the selected draft plan."
        ]
        return payload

    if not selected_plan.generated_task_plans:
        payload["orchestration_stage"] = "plan_generation_required"
        payload["next_actions"] = [
            "Generate baseline task plan from committed task scope."
        ]
        return payload

    payload["orchestration_stage"] = "plan_commit_required"
    payload["next_actions"] = [
        "Commit the generated draft plan."
    ]
    return payload
