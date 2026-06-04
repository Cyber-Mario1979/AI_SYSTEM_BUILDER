"""Read-only local workflow visibility logic for M32.5.

This module builds a bounded workflow visibility payload from validated state.
It does not mutate state, call AI/providers, or claim product readiness.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from asbp.core.collections import build_work_package_collection_ids
from asbp.core.work_packages import (
    build_work_package_task_ids,
    find_work_package_by_id,
)
from asbp.local_workflow_logic import (
    LOCAL_WORKFLOW_SURFACE,
    build_local_workflow_input_warnings,
)
from asbp.state_model import (
    PlanningModel,
    StateModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

LOCAL_WORKFLOW_VISIBILITY_CHECKPOINT = "M32.5 — Workflow visibility surfaces"

WORKFLOW_VISIBILITY_LIMITATIONS = [
    "CLI/local workflow surface is an adapter only.",
    "This status command is read-only and does not mutate state.",
    "No domain logic is implemented in the CLI surface.",
    "Document review/download behavior belongs to M32.6 unless separately scoped.",
    "Failure-handling completion belongs to M32.7 unless separately scoped.",
    "No AI, provider, Ollama, or live model call is performed.",
    "Generated or assembled output remains human-review-required.",
    "Retrieval, where later included, remains helper-only and non-authoritative.",
    "This is not release, deployment, SaaS, commercial, or customer-ready evidence.",
]


def _clean_selector_context(work_package: WorkPackageModel) -> dict[str, Any] | None:
    selector_context = work_package.selector_context
    if selector_context is None:
        return None

    payload = selector_context.model_dump()
    cleaned_payload = {
        key: value
        for key, value in payload.items()
        if value is not None and value != []
    }
    return cleaned_payload or None


def _build_work_package_tasks(
    tasks: list[TaskModel],
    *,
    task_ids: list[str],
) -> list[dict[str, Any]]:
    task_id_set = set(task_ids)
    selected_tasks = [task for task in tasks if task.task_id in task_id_set]
    selected_tasks = sorted(selected_tasks, key=lambda task: (task.order, task.task_id))

    return [
        {
            "task_id": task.task_id,
            "order": task.order,
            "title": task.title,
            "status": task.status,
            "duration": task.duration,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "dependencies": list(task.dependencies),
        }
        for task in selected_tasks
    ]


def _build_collection_visibility(
    task_collections: list[TaskCollectionModel],
    *,
    collection_ids: list[str],
) -> list[dict[str, Any]]:
    collection_id_set = set(collection_ids)
    selected_collections = [
        collection
        for collection in task_collections
        if collection.collection_id in collection_id_set
    ]
    selected_collections = sorted(
        selected_collections,
        key=lambda collection: collection.collection_id,
    )

    return [
        {
            "collection_id": collection.collection_id,
            "title": collection.title,
            "collection_state": collection.collection_state,
            "task_ids": list(collection.task_ids),
        }
        for collection in selected_collections
    ]


def _build_generated_schedule_bounds(plan: PlanningModel) -> dict[str, Any]:
    generated_rows = [
        generated_task_plan.model_dump(mode="json")
        for generated_task_plan in plan.generated_task_plans
    ]
    generated_rows = sorted(
        generated_rows,
        key=lambda row: (row["sequence_order"], row["task_id"]),
    )

    return {
        "generated_task_plan_count": len(generated_rows),
        "generated_schedule_start_at": (
            generated_rows[0]["planned_start_at"] if generated_rows else None
        ),
        "generated_schedule_finish_at": (
            generated_rows[-1]["planned_finish_at"] if generated_rows else None
        ),
    }


def _build_plan_visibility(
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> list[dict[str, Any]]:
    selected_plans = [plan for plan in plans if plan.work_package_id == wp_id]
    selected_plans = sorted(selected_plans, key=lambda plan: plan.plan_id)

    plan_payloads: list[dict[str, Any]] = []
    for plan in selected_plans:
        schedule_bounds = _build_generated_schedule_bounds(plan)
        plan_payloads.append(
            {
                "plan_id": plan.plan_id,
                "plan_state": plan.plan_state,
                "planning_basis": (
                    plan.planning_basis.model_dump()
                    if plan.planning_basis is not None
                    else None
                ),
                "planned_start_at": (
                    plan.planned_start_at.isoformat()
                    if plan.planned_start_at is not None
                    else None
                ),
                "planning_calendar": (
                    plan.planning_calendar.model_dump()
                    if plan.planning_calendar is not None
                    else None
                ),
                **schedule_bounds,
            }
        )

    return plan_payloads


def _build_status_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(Counter(row["status"] for row in rows))


def build_local_workflow_visibility_payload(
    state: StateModel,
    *,
    wp_id: str,
) -> dict[str, Any]:
    """Build a read-only workflow visibility payload for a work package."""

    work_package = find_work_package_by_id(state.work_packages, wp_id)
    if work_package is None:
        raise ValueError(f"Work Package not found: {wp_id}")

    task_ids = build_work_package_task_ids(state.tasks, wp_id=work_package.wp_id)
    collection_ids = build_work_package_collection_ids(
        state.task_collections,
        wp_id=work_package.wp_id,
    )
    task_rows = _build_work_package_tasks(state.tasks, task_ids=task_ids)
    collection_rows = _build_collection_visibility(
        state.task_collections,
        collection_ids=collection_ids,
    )
    plan_rows = _build_plan_visibility(state.plans, wp_id=work_package.wp_id)
    selector_context = _clean_selector_context(work_package)
    standards_bundles = (
        selector_context.get("standards_bundles", []) if selector_context else []
    )

    readiness_gaps: list[str] = []
    if selector_context is None:
        readiness_gaps.append("No preset/profile/source selector context is bound.")
    if not task_rows:
        readiness_gaps.append("No staged tasks are associated with this work package.")
    if not collection_rows:
        readiness_gaps.append("No source/task collection is bound to this work package.")
    if not plan_rows:
        readiness_gaps.append("No schedule plan is associated with this work package.")
    elif not any(row["generated_task_plan_count"] for row in plan_rows):
        readiness_gaps.append("No generated schedule is visible for this work package.")

    return {
        "checkpoint": LOCAL_WORKFLOW_VISIBILITY_CHECKPOINT,
        "surface": LOCAL_WORKFLOW_SURFACE,
        "adapter_boundary": "CLI adapter reads validated state and calls service/core boundaries only.",
        "workflow_state": {
            "project": state.project,
            "state_status": state.status,
            "selected_work_package": {
                "wp_id": work_package.wp_id,
                "title": work_package.title,
                "status": work_package.status,
                "selector_context": selector_context,
            },
        },
        "task_lifecycle": {
            "task_count": len(task_rows),
            "status_counts": _build_status_counts(task_rows),
            "tasks": task_rows,
        },
        "schedule_lifecycle": {
            "plan_count": len(plan_rows),
            "generated_schedule_present": any(
                row["generated_task_plan_count"] for row in plan_rows
            ),
            "plans": plan_rows,
        },
        "document_lifecycle": {
            "status": "not_implemented_in_current_surface",
            "limitation": "Document review/download behavior belongs to M32.6 unless separately scoped.",
        },
        "source_and_citation_state": {
            "collection_count": len(collection_rows),
            "collection_ids": collection_ids,
            "collections": collection_rows,
            "standards_bundles": standards_bundles,
            "citation_state": "Source collection and standards bundle identifiers are visible only; clause-level citation authority is not upgraded.",
            "authority_limit": "Existing repo state only; no retrieval or standards authority is upgraded.",
        },
        "ai_limitation_state": {
            "ai_call_performed": False,
            "provider_call_performed": False,
            "ollama_call_performed": False,
            "human_review_required": True,
            "limitation": "No AI, provider, Ollama, or live model call is performed.",
        },
        "input_warnings": build_local_workflow_input_warnings(work_package),
        "readiness_gaps": readiness_gaps,
        "limitations": list(WORKFLOW_VISIBILITY_LIMITATIONS),
        "next_safe_actions": [
            "Resolve readiness gaps before calling the workflow trial-ready.",
            "Use M32.6 for controlled output review/download behavior.",
            "Use M32.7 for local workflow error/failure-handling completion.",
        ],
    }
