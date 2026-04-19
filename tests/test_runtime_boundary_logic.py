from datetime import datetime, timezone

from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    SelectorContextModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def make_bound_context_work_package(
    wp_id: str = "WP-001",
    title: str = "Tablet press qualification",
) -> WorkPackageModel:
    return WorkPackageModel(
        wp_id=wp_id,
        title=title,
        status="open",
        selector_context=SelectorContextModel(
            preset_id="oral-solid-dose-standard",
            scope_intent="qualification-only",
            standards_bundles=["cqv-core", "automation"],
        ),
    )


def test_runtime_boundary_returns_none_for_missing_work_package():
    payload = build_work_package_runtime_boundary_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_runtime_boundary_reports_deterministic_blocked_when_orchestration_is_not_execution_ready():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_runtime_boundary_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload == {
        "wp_id": "WP-001",
        "runtime_boundary_state": "deterministic_blocked",
        "eligible_for_prompt_contract": False,
        "selected_plan_id": None,
        "deterministic_facts": {
            "work_package_status": "open",
            "orchestration_stage": "binding_context_required",
            "blocking_conditions": ["selector_context_missing"],
            "next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "selector_context_ready": False,
            "work_package_task_ids": [],
            "bound_committed_collection_ids": [],
            "bound_committed_task_ids": [],
            "plan_ids": [],
        },
        "model_may": [
            "consume only validated deterministic facts exposed through this boundary payload",
            "transform those facts into bounded language outputs only after a future prompt contract is defined",
            "return only fields explicitly requested by a future runtime contract",
        ],
        "model_may_not": [
            "mutate persisted state",
            "invent facts, statuses, dates, dependencies, or identifiers",
            "change selected work package, selected plan, task scope, or collection scope",
            "resolve blocked deterministic state by inference",
            "bypass deterministic validation or acceptance rules",
        ],
    }


def test_runtime_boundary_reports_prompt_contract_eligibility_when_execution_ready():
    work_packages = [make_bound_context_work_package()]
    task_collections = [
        TaskCollectionModel(
            collection_id="TC-001",
            title="Committed Selection",
            collection_state="committed",
            work_package_id="WP-001",
            task_ids=["TASK-001"],
        )
    ]
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            duration=1,
            work_package_id="WP-001",
            status="planned",
        )
    ]
    plans = [
        PlanningModel(
            plan_id="PLAN-001",
            work_package_id="WP-001",
            plan_state="committed",
            planning_basis=PlanningBasisModel(
                duration_source="task_duration",
            ),
            planned_start_at=datetime(2026, 4, 13, 8, 30, tzinfo=timezone.utc),
            planning_calendar=PlanningCalendarModel(
                working_days=["monday", "wednesday", "friday"],
                workday_hours=8,
                workmonth_mode="calendar_month",
            ),
        )
    ]

    payload = build_work_package_runtime_boundary_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload == {
        "wp_id": "WP-001",
        "runtime_boundary_state": "eligible_for_prompt_contract",
        "eligible_for_prompt_contract": True,
        "selected_plan_id": "PLAN-001",
        "deterministic_facts": {
            "work_package_status": "open",
            "orchestration_stage": "execution_ready",
            "blocking_conditions": [],
            "next_actions": [
                "Execution-ready deterministic state reached."
            ],
            "selector_context_ready": True,
            "work_package_task_ids": ["TASK-001"],
            "bound_committed_collection_ids": ["TC-001"],
            "bound_committed_task_ids": ["TASK-001"],
            "plan_ids": ["PLAN-001"],
        },
        "model_may": [
            "consume only validated deterministic facts exposed through this boundary payload",
            "transform those facts into bounded language outputs only after a future prompt contract is defined",
            "return only fields explicitly requested by a future runtime contract",
        ],
        "model_may_not": [
            "mutate persisted state",
            "invent facts, statuses, dates, dependencies, or identifiers",
            "change selected work package, selected plan, task scope, or collection scope",
            "resolve blocked deterministic state by inference",
            "bypass deterministic validation or acceptance rules",
        ],
    }
