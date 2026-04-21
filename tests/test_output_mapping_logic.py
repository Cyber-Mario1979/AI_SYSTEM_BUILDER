# tests/test_output_mapping_logic.py

from datetime import datetime, timezone

from asbp.output_mapping_logic import build_work_package_output_mapping_payload
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


def test_output_mapping_returns_none_for_missing_work_package():
    payload = build_work_package_output_mapping_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_output_mapping_reports_blocked_mapping_payload():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_mapping_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["wp_id"] == "WP-001"
    assert payload["output_mapping_metadata"] == {
        "output_mapping_id": "work_package_output_mapping_v1",
        "output_target_id": "work_package_operator_response_target_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "generation_surface_id": "work_package_controlled_generation_surface_v1",
        "mapping_scope": "single_work_package",
        "mapping_state": "blocked",
        "current_response_mode": "blocked_explainer",
        "selected_plan_id": None,
    }
    assert payload["source_authority"] == {
        "deterministic_input_source": "generation_surface_payload",
        "contract_source": "output_contract_payload",
        "source_of_truth_rule": (
            "Only validated deterministic input and the bounded output "
            "contract may shape the mapped output payload."
        ),
    }
    assert payload["deterministic_input"]["structured_facts"] == {
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
    assert payload["mapped_output_contract"]["required_output_fields"] == [
        "response_mode",
        "operator_message",
        "recommended_next_actions",
        "grounded_input_fields_used",
    ]
    assert payload["mapped_output_payload"] == {
        "response_mode": "blocked_explainer",
        "candidate_response_template": {
            "response_mode": "blocked_explainer",
            "operator_message": "",
            "recommended_next_actions": [],
            "grounded_input_fields_used": [],
        },
    }


def test_output_mapping_reports_available_mapping_payload():
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

    payload = build_work_package_output_mapping_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["wp_id"] == "WP-001"
    assert payload["output_mapping_metadata"] == {
        "output_mapping_id": "work_package_output_mapping_v1",
        "output_target_id": "work_package_operator_response_target_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "generation_surface_id": "work_package_controlled_generation_surface_v1",
        "mapping_scope": "single_work_package",
        "mapping_state": "available",
        "current_response_mode": "execution_ready_summary",
        "selected_plan_id": "PLAN-001",
    }
    assert payload["deterministic_input"]["structured_facts"] == {
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
    assert payload["mapped_output_payload"] == {
        "response_mode": "execution_ready_summary",
        "candidate_response_template": {
            "response_mode": "execution_ready_summary",
            "operator_message": "",
            "recommended_next_actions": [],
            "grounded_input_fields_used": [],
        },
    }