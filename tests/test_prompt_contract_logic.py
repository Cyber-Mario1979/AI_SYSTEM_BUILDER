from datetime import datetime, timezone

from asbp.prompt_contract_logic import build_work_package_prompt_contract_payload
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


def test_prompt_contract_returns_none_for_missing_work_package():
    payload = build_work_package_prompt_contract_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_prompt_contract_reports_blocked_contract_mode_when_runtime_boundary_is_blocked():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_prompt_contract_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload["wp_id"] == "WP-001"
    assert payload["prompt_contract_id"] == "work_package_runtime_prompt_contract_v1"
    assert payload["prompt_contract_state"] == "blocked"
    assert payload["prompt_contract_mode"] == "blocked_explainer"
    assert payload["eligible_for_prompt_contract"] is False
    assert payload["required_input_fields"] == [
        "wp_id",
        "runtime_boundary_state",
        "eligible_for_prompt_contract",
        "selected_plan_id",
        "deterministic_facts.work_package_status",
        "deterministic_facts.orchestration_stage",
        "deterministic_facts.blocking_conditions",
        "deterministic_facts.next_actions",
        "deterministic_facts.selector_context_ready",
        "deterministic_facts.work_package_task_ids",
        "deterministic_facts.bound_committed_collection_ids",
        "deterministic_facts.bound_committed_task_ids",
        "deterministic_facts.plan_ids",
    ]
    assert payload["expected_output_fields"] == [
        "response_mode",
        "operator_message",
        "recommended_next_actions",
        "grounded_input_fields_used",
    ]
    assert payload["runtime_boundary"]["runtime_boundary_state"] == "deterministic_blocked"
    assert payload["runtime_boundary"]["deterministic_facts"]["orchestration_stage"] == "binding_context_required"


def test_prompt_contract_reports_ready_contract_mode_when_runtime_boundary_is_execution_ready():
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

    payload = build_work_package_prompt_contract_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload["wp_id"] == "WP-001"
    assert payload["prompt_contract_state"] == "ready"
    assert payload["prompt_contract_mode"] == "execution_ready_summary"
    assert payload["eligible_for_prompt_contract"] is True
    assert payload["runtime_boundary"]["runtime_boundary_state"] == "eligible_for_prompt_contract"
    assert payload["runtime_boundary"]["selected_plan_id"] == "PLAN-001"
