"""End-to-end local workflow scenario logic for M32.8.

This module stages one bounded cleanroom HVAC CQV workflow scenario through
validated state models. It does not generate product-ready output, call AI,
approve/release artifacts, or place domain behavior in the CLI adapter.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from asbp.local_workflow_logic import LOCAL_WORKFLOW_SURFACE
from asbp.planning_logic import generate_plan_baseline
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    SelectorContextModel,
    StateModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)
from asbp.versioning import STATE_VERSION

LOCAL_WORKFLOW_SCENARIO_CHECKPOINT = "M32.8 — End-to-end local scenario implementation"

CLEANROOM_HVAC_SCENARIO_ID = "cleanroom-hvac-qualification-basic"
CLEANROOM_HVAC_WORK_PACKAGE_ID = "WP-032"
CLEANROOM_HVAC_COLLECTION_ID = "TC-032"
CLEANROOM_HVAC_PLAN_ID = "PLAN-032"
CLEANROOM_HVAC_TASK_IDS = [
    "TASK-M32-8-001",
    "TASK-M32-8-002",
    "TASK-M32-8-003",
]

SCENARIO_LIMITATIONS = [
    "CLI/local workflow surface is an adapter only.",
    "Scenario staging uses validated local state models and approved state-store persistence only.",
    "Scenario evidence proves local exerciseability only, not product readiness or UAT acceptance.",
    "Outputs remain review metadata/visibility only unless separately scoped.",
    "No output is silently accepted, approved, signed, released, or certified.",
    "No AI, provider, Ollama, or live model call is performed.",
    "This is not release, deployment, SaaS, commercial, or customer-ready evidence.",
]


def build_empty_local_workflow_scenario_state() -> StateModel:
    """Build an empty validated state suitable for scenario staging."""

    return StateModel(
        project="AI_SYSTEM_BUILDER",
        version=STATE_VERSION,
        status="in_flight",
    )


def _scenario_work_package() -> WorkPackageModel:
    return WorkPackageModel(
        wp_id=CLEANROOM_HVAC_WORK_PACKAGE_ID,
        title="M32.8 Cleanroom HVAC qualification-only local scenario",
        status="open",
        selector_context=SelectorContextModel(
            system_type="cleanroom-hvac",
            preset_id="cqv-cleanroom-hvac-basic",
            scope_intent="qualification-only",
            standards_bundles=["cqv-core", "cleanroom-hvac"],
        ),
    )


def _scenario_tasks() -> list[TaskModel]:
    return [
        TaskModel(
            task_id=CLEANROOM_HVAC_TASK_IDS[0],
            order=1,
            title="Prepare cleanroom HVAC qualification plan",
            description="Stage the qualification planning task for the local scenario.",
            owner="local-user",
            duration=2,
            work_package_id=CLEANROOM_HVAC_WORK_PACKAGE_ID,
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id=CLEANROOM_HVAC_TASK_IDS[1],
            order=2,
            title="Execute cleanroom HVAC field checks",
            description="Stage field execution checks for the local scenario.",
            owner="local-user",
            duration=1,
            work_package_id=CLEANROOM_HVAC_WORK_PACKAGE_ID,
            status="planned",
            dependencies=[CLEANROOM_HVAC_TASK_IDS[0]],
        ),
        TaskModel(
            task_id=CLEANROOM_HVAC_TASK_IDS[2],
            order=3,
            title="Review cleanroom HVAC qualification output",
            description="Stage human review before any output acceptance claim.",
            owner="local-user",
            duration=1,
            work_package_id=CLEANROOM_HVAC_WORK_PACKAGE_ID,
            status="planned",
            dependencies=[CLEANROOM_HVAC_TASK_IDS[1]],
        ),
    ]


def _scenario_collection() -> TaskCollectionModel:
    return TaskCollectionModel(
        collection_id=CLEANROOM_HVAC_COLLECTION_ID,
        title="M32.8 cleanroom HVAC local scenario source/task collection",
        collection_state="committed",
        work_package_id=CLEANROOM_HVAC_WORK_PACKAGE_ID,
        task_ids=list(CLEANROOM_HVAC_TASK_IDS),
    )


def _scenario_plan() -> PlanningModel:
    return PlanningModel(
        plan_id=CLEANROOM_HVAC_PLAN_ID,
        work_package_id=CLEANROOM_HVAC_WORK_PACKAGE_ID,
        plan_state="draft",
        planning_basis=PlanningBasisModel(
            duration_source="task_duration",
            basis_label="M32.8 cleanroom HVAC scenario task durations",
        ),
        planned_start_at=datetime.fromisoformat("2026-06-08T08:00:00+00:00"),
        planning_calendar=PlanningCalendarModel(
            working_days=["monday", "tuesday", "wednesday", "thursday", "friday"],
            workday_hours=8,
            workmonth_mode="calendar_month",
        ),
    )


def _remove_existing_scenario_rows(state: StateModel) -> None:
    scenario_task_ids = set(CLEANROOM_HVAC_TASK_IDS)

    state.work_packages = [
        work_package
        for work_package in state.work_packages
        if work_package.wp_id != CLEANROOM_HVAC_WORK_PACKAGE_ID
    ]
    state.tasks = [task for task in state.tasks if task.task_id not in scenario_task_ids]
    state.task_collections = [
        collection
        for collection in state.task_collections
        if collection.collection_id != CLEANROOM_HVAC_COLLECTION_ID
    ]
    state.plans = [plan for plan in state.plans if plan.plan_id != CLEANROOM_HVAC_PLAN_ID]


def _build_executable_local_use_steps() -> list[str]:
    wp_id = CLEANROOM_HVAC_WORK_PACKAGE_ID
    return [
        f"python -m asbp.adapters.local_workflow_cli configure --wp-id {wp_id} --system-type cleanroom-hvac --preset-id cqv-cleanroom-hvac-basic --scope-intent qualification-only --standards-bundle cleanroom-hvac",
        f"python -m asbp.adapters.local_workflow_cli plan --wp-id {wp_id}",
        f"python -m asbp.adapters.local_workflow_cli status --wp-id {wp_id}",
        f"python -m asbp.adapters.local_workflow_cli outputs --wp-id {wp_id}",
    ]


def _build_scenario_payload(state: StateModel) -> dict[str, Any]:
    scenario_plan = next(
        plan for plan in state.plans if plan.plan_id == CLEANROOM_HVAC_PLAN_ID
    )
    generated_task_plan_count = len(scenario_plan.generated_task_plans)

    return {
        "checkpoint": LOCAL_WORKFLOW_SCENARIO_CHECKPOINT,
        "surface": LOCAL_WORKFLOW_SURFACE,
        "adapter_boundary": "CLI adapter stages an approved scenario through validated local workflow boundaries only.",
        "scenario_id": CLEANROOM_HVAC_SCENARIO_ID,
        "scenario_status": "staged",
        "state_status": state.status,
        "selected_work_package": {
            "wp_id": CLEANROOM_HVAC_WORK_PACKAGE_ID,
            "title": "M32.8 Cleanroom HVAC qualification-only local scenario",
            "system_type": "cleanroom-hvac",
            "preset_id": "cqv-cleanroom-hvac-basic",
            "scope_intent": "qualification-only",
            "standards_bundles": ["cqv-core", "cleanroom-hvac"],
        },
        "scenario_assets": {
            "task_ids": list(CLEANROOM_HVAC_TASK_IDS),
            "task_count": len(CLEANROOM_HVAC_TASK_IDS),
            "collection_id": CLEANROOM_HVAC_COLLECTION_ID,
            "collection_state": "committed",
            "plan_id": CLEANROOM_HVAC_PLAN_ID,
            "generated_task_plan_count": generated_task_plan_count,
        },
        "executable_local_use_steps": _build_executable_local_use_steps(),
        "scenario_evidence": {
            "can_be_exercised_through_local_workflow": generated_task_plan_count
            == len(CLEANROOM_HVAC_TASK_IDS),
            "commands_to_exercise": ["configure", "plan", "status", "outputs"],
            "human_review_required": True,
            "approval_claimed": False,
            "release_claimed": False,
            "product_ready_claimed": False,
        },
        "limitations": list(SCENARIO_LIMITATIONS),
        "next_safe_actions": [
            "Run the listed local workflow commands to exercise the staged scenario.",
            "Record scenario command output as M32.8 evidence before tracker movement.",
            "Do not treat this scenario as UAT, release, deployment, SaaS, commercial, or customer-ready evidence.",
        ],
    }


def _revalidate_scenario_state(state: StateModel) -> StateModel:
    """Revalidate scenario state without dropping fields excluded from dumps.

    Some state fields are intentionally marked exclude=True for compact persisted
    JSON. Revalidating from model_dump would drop those runtime links before the
    approved state-store writer can persist them safely.
    """

    return StateModel(
        project=state.project,
        version=state.version,
        status=state.status,
        tasks=state.tasks,
        work_packages=state.work_packages,
        task_collections=state.task_collections,
        plans=state.plans,
    )


def stage_local_workflow_scenario(
    state: StateModel,
    *,
    scenario_id: str,
) -> dict[str, Any]:
    """Stage the approved M32.8 local CQV workflow scenario in validated state."""

    if scenario_id != CLEANROOM_HVAC_SCENARIO_ID:
        raise ValueError(f"Unsupported local workflow scenario: {scenario_id}")

    state.status = "in_flight"
    _remove_existing_scenario_rows(state)

    state.work_packages.append(_scenario_work_package())
    state.tasks.extend(_scenario_tasks())
    state.task_collections.append(_scenario_collection())
    state.plans.append(_scenario_plan())

    scenario_plan = generate_plan_baseline(
        state.plans,
        state.work_packages,
        state.tasks,
        state.task_collections,
        plan_id=CLEANROOM_HVAC_PLAN_ID,
    )
    if scenario_plan is None:
        raise ValueError(f"Scenario plan not found: {CLEANROOM_HVAC_PLAN_ID}")

    validated_state = _revalidate_scenario_state(state)
    state.status = validated_state.status
    state.work_packages = validated_state.work_packages
    state.tasks = validated_state.tasks
    state.task_collections = validated_state.task_collections
    state.plans = validated_state.plans

    return _build_scenario_payload(state)
