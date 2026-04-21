# tests/test_output_contract_logic.py

from datetime import datetime, timezone

from asbp.output_contract_logic import build_work_package_output_contract
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


def test_output_contract_returns_none_for_missing_work_package():
    payload = build_work_package_output_contract(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
    )

    assert payload is None


def test_output_contract_reports_blocked_single_work_package_operator_contract():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_contract(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["output_contract_metadata"] == {
        "output_contract_id": "work_package_operator_response_contract_v1",
        "output_target_id": "work_package_operator_response_target_v1",
        "output_target_family": "single_work_package_operator_response",
        "contract_scope": "single_work_package",
        "target_audience": "operator",
        "delivery_format": "chat_text",
        "contract_state": "blocked",
        "current_response_mode": "blocked_explainer",
        "selected_plan_id": None,
    }
    assert payload["required_output_fields"] == [
        "response_mode",
        "operator_message",
        "recommended_next_actions",
        "grounded_input_fields_used",
    ]
    assert payload["field_types"] == {
        "response_mode": "string",
        "operator_message": "string",
        "recommended_next_actions": "list[string]",
        "grounded_input_fields_used": "list[string]",
    }
    assert payload["allowed_response_modes"] == [
        "blocked_explainer",
        "execution_ready_summary",
    ]
    assert payload["prohibited_contract_drift"] == [
        "omit required output fields",
        "add output fields outside the declared contract",
        "invent facts outside the validated deterministic inputs",
        "change or reinterpret blocking conditions",
        "change selected plan, task scope, or collection scope",
        "propose state mutation as if it already occurred",
    ]
    assert payload["acceptance_shape"] == {
        "top_level_container": "object",
        "extra_fields_allowed": False,
        "field_rules": {
            "response_mode": {
                "type": "string",
                "allowed_values": [
                    "blocked_explainer",
                    "execution_ready_summary",
                ],
                "must_equal_current_response_mode": True,
            },
            "operator_message": {
                "type": "string",
                "allow_empty": False,
            },
            "recommended_next_actions": {
                "type": "list[string]",
                "allow_empty": True,
            },
            "grounded_input_fields_used": {
                "type": "list[string]",
                "allow_empty": False,
            },
        },
    }


def test_output_contract_reports_available_single_work_package_operator_contract():
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

    payload = build_work_package_output_contract(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert payload is not None
    assert payload["output_contract_metadata"] == {
        "output_contract_id": "work_package_operator_response_contract_v1",
        "output_target_id": "work_package_operator_response_target_v1",
        "output_target_family": "single_work_package_operator_response",
        "contract_scope": "single_work_package",
        "target_audience": "operator",
        "delivery_format": "chat_text",
        "contract_state": "available",
        "current_response_mode": "execution_ready_summary",
        "selected_plan_id": "PLAN-001",
    }
    assert payload["required_output_fields"] == [
        "response_mode",
        "operator_message",
        "recommended_next_actions",
        "grounded_input_fields_used",
    ]
    assert payload["allowed_response_modes"] == [
        "blocked_explainer",
        "execution_ready_summary",
    ]
    assert payload["acceptance_shape"]["top_level_container"] == "object"
    assert payload["acceptance_shape"]["extra_fields_allowed"] is False
    assert payload["acceptance_shape"]["field_rules"]["response_mode"] == {
        "type": "string",
        "allowed_values": [
            "blocked_explainer",
            "execution_ready_summary",
        ],
        "must_equal_current_response_mode": True,
    }