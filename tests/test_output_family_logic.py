# tests/test_output_family_logic.py

from datetime import datetime, timezone

from asbp.output_family_logic import build_work_package_output_family_payload
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


def test_output_family_returns_none_for_missing_work_package():
    payload = build_work_package_output_family_payload(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
        candidate_output={},
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is None


def test_output_family_reports_available_families_for_blocked_explainer_mode():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_family_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "blocked_explainer",
            "operator_message": (
                "Generation cannot proceed until selector context is completed."
            ),
            "recommended_next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "deterministic_facts.orchestration_stage",
                "deterministic_facts.blocking_conditions",
                "deterministic_facts.next_actions",
            ],
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_family_metadata"] == {
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_retry_id": "work_package_output_retry_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "family_state": "available",
        "decision_state": "accepted",
        "current_response_mode": "blocked_explainer",
        "selected_family_id": "single_work_package_operator_response",
        "selected_plan_id": None,
    }
    assert payload["available_output_families"] == [
        {
            "output_family_id": "single_work_package_operator_response",
            "family_role": "default_detailed_response",
            "delivery_format": "chat_text",
            "supported_response_mode": "blocked_explainer",
            "summary_style": "standard_detailed",
            "requires_same_output_contract": True,
        },
        {
            "output_family_id": "single_work_package_operator_response_brief",
            "family_role": "brief_operator_response",
            "delivery_format": "chat_text",
            "supported_response_mode": "blocked_explainer",
            "summary_style": "brief",
            "requires_same_output_contract": True,
        },
    ]
    assert payload["family_boundaries"] == {
        "multi_work_package_output": False,
        "document_artifact_output": False,
        "cross_family_contract_variation": False,
    }
    assert payload["family_ready_output"] == {
        "response_mode": "blocked_explainer",
        "operator_message": (
            "Generation cannot proceed until selector context is completed."
        ),
        "recommended_next_actions": [
            "Complete deterministic selector context before orchestration can proceed."
        ],
        "grounded_input_fields_used": [
            "wp_id",
            "deterministic_facts.orchestration_stage",
            "deterministic_facts.blocking_conditions",
            "deterministic_facts.next_actions",
        ],
    }


def test_output_family_reports_expanded_families_for_execution_ready_mode():
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

    payload = build_work_package_output_family_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": (
                "The work package is ready for generation using the selected committed plan."
            ),
            "recommended_next_actions": [
                "Execution-ready deterministic state reached."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "selected_plan_id",
                "deterministic_facts.orchestration_stage",
                "deterministic_facts.plan_ids",
            ],
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_family_metadata"] == {
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_retry_id": "work_package_output_retry_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "family_state": "available",
        "decision_state": "accepted",
        "current_response_mode": "execution_ready_summary",
        "selected_family_id": "single_work_package_operator_response",
        "selected_plan_id": "PLAN-001",
    }
    assert payload["available_output_families"] == [
        {
            "output_family_id": "single_work_package_operator_response",
            "family_role": "default_detailed_response",
            "delivery_format": "chat_text",
            "supported_response_mode": "execution_ready_summary",
            "summary_style": "standard_detailed",
            "requires_same_output_contract": True,
        },
        {
            "output_family_id": "single_work_package_operator_response_brief",
            "family_role": "brief_operator_response",
            "delivery_format": "chat_text",
            "supported_response_mode": "execution_ready_summary",
            "summary_style": "brief",
            "requires_same_output_contract": True,
        },
        {
            "output_family_id": "single_work_package_operator_next_actions_only",
            "family_role": "next_actions_focused_response",
            "delivery_format": "chat_text",
            "supported_response_mode": "execution_ready_summary",
            "summary_style": "next_actions_focused",
            "requires_same_output_contract": True,
        },
    ]
    assert payload["family_ready_output"] == {
        "response_mode": "execution_ready_summary",
        "operator_message": (
            "The work package is ready for generation using the selected committed plan."
        ),
        "recommended_next_actions": [
            "Execution-ready deterministic state reached."
        ],
        "grounded_input_fields_used": [
            "wp_id",
            "selected_plan_id",
            "deterministic_facts.orchestration_stage",
            "deterministic_facts.plan_ids",
        ],
    }


def test_output_family_stays_blocked_when_retry_decision_is_not_accepted():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_family_payload(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": "",
            "recommended_next_actions": "not-a-list",
            "grounded_input_fields_used": [
                "wp_id",
                "disallowed.field",
            ],
            "extra_field": "unexpected",
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_family_metadata"] == {
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_retry_id": "work_package_output_retry_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "family_state": "blocked",
        "decision_state": "retry_allowed",
        "current_response_mode": "blocked_explainer",
        "selected_family_id": None,
        "selected_plan_id": None,
    }
    assert payload["available_output_families"] == []
    assert payload["family_ready_output"] is None
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }