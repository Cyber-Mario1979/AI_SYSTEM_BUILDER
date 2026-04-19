from datetime import datetime, timezone

from asbp.binding_context_logic import (
    build_work_package_binding_context_blockers,
    validate_work_package_binding_context_for_planning,
)
from asbp.orchestration_logic import build_work_package_orchestration_payload
from asbp.state_model import (
    PlanningBasisModel,
    PlanningCalendarModel,
    PlanningModel,
    SelectorContextModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def make_bound_context_work_package_model(
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


def test_build_work_package_binding_context_blockers_returns_missing_selector_context_blocker():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    blockers = build_work_package_binding_context_blockers(
        work_packages,
        work_package_id="WP-001",
    )

    assert blockers == ["selector_context_missing"]


def test_validate_work_package_binding_context_for_planning_preserves_scope_intent_error_message():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
            selector_context=SelectorContextModel(
                preset_id="oral-solid-dose-standard",
                standards_bundles=["cqv-core", "automation"],
            ),
        )
    ]

    try:
        validate_work_package_binding_context_for_planning(
            work_packages,
            work_package_id="WP-001",
            plan_id="PLAN-001",
        )
    except ValueError as exc:
        assert (
            "Planning-bound Work Package must declare "
            "selector_context.scope_intent: PLAN-001 -> WP-001"
        ) == str(exc)
    else:
        raise AssertionError("Expected ValueError was not raised")


def test_build_work_package_orchestration_payload_preserves_execution_ready_contract():
    work_packages = [make_bound_context_work_package_model()]
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

    payload = build_work_package_orchestration_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload == {
        "wp_id": "WP-001",
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
        "selected_plan_id": "PLAN-001",
    }
