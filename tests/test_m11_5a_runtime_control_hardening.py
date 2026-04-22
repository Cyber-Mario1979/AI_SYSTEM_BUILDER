from datetime import datetime, timezone

from asbp.runtime.control import build_work_package_runtime_control_payload
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


def test_m11_5a_runtime_control_returns_none_for_missing_work_package() -> None:
    payload = build_work_package_runtime_control_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_m11_5a_runtime_control_reports_blocked_explainer_only_state() -> None:
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_runtime_control_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["wp_id"] == "WP-001"
    assert payload["runtime_control_metadata"] == {
        "runtime_control_id": "work_package_runtime_control_v1",
        "handoff_contract_id": "work_package_llm_handoff_v1",
        "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
        "runtime_control_state": "blocked_explainer_only",
        "control_action": "explain_blocked_state",
        "generation_allowed": False,
        "operator_response_allowed": True,
        "selected_plan_id": None,
        "allowed_response_modes": ["blocked_explainer"],
        "default_response_mode": "blocked_explainer",
    }
    assert payload["structured_facts"] == {
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
    }


def test_m11_5a_runtime_control_reports_execution_ready_summary_only_state() -> None:
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

    payload = build_work_package_runtime_control_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["wp_id"] == "WP-001"
    assert payload["runtime_control_metadata"] == {
        "runtime_control_id": "work_package_runtime_control_v1",
        "handoff_contract_id": "work_package_llm_handoff_v1",
        "source_prompt_contract_id": "work_package_runtime_prompt_contract_v1",
        "runtime_control_state": "execution_ready_summary_only",
        "control_action": "summarize_execution_ready_state",
        "generation_allowed": True,
        "operator_response_allowed": True,
        "selected_plan_id": "PLAN-001",
        "allowed_response_modes": ["execution_ready_summary"],
        "default_response_mode": "execution_ready_summary",
    }
    assert payload["structured_facts"] == {
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
    }