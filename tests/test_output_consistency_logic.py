# tests/test_output_consistency_logic.py

from datetime import datetime, timezone

from asbp.output_consistency_logic import (
    validate_work_package_output_family_consistency,
)
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


def test_output_consistency_returns_none_for_missing_work_package():
    payload = validate_work_package_output_family_consistency(
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


def test_output_consistency_accepts_default_blocked_family_selection():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = validate_work_package_output_family_consistency(
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
    assert payload["output_consistency_metadata"] == {
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "consistency_state": "accepted",
        "current_response_mode": "blocked_explainer",
        "resolved_family_id": "single_work_package_operator_response",
        "selected_plan_id": None,
    }
    assert payload["consistency_errors"] == []
    assert payload["consistent_output_family"] == {
        "output_family_id": "single_work_package_operator_response",
        "family_role": "default_detailed_response",
        "delivery_format": "chat_text",
        "supported_response_mode": "blocked_explainer",
        "summary_style": "standard_detailed",
        "requires_same_output_contract": True,
    }
    assert payload["consistent_output_payload"] == {
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


def test_output_consistency_accepts_expanded_execution_ready_family_selection():
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

    payload = validate_work_package_output_family_consistency(
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
        requested_family_id="single_work_package_operator_next_actions_only",
    )

    assert payload is not None
    assert payload["output_consistency_metadata"] == {
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "consistency_state": "accepted",
        "current_response_mode": "execution_ready_summary",
        "resolved_family_id": "single_work_package_operator_next_actions_only",
        "selected_plan_id": "PLAN-001",
    }
    assert payload["consistency_errors"] == []
    assert payload["consistent_output_family"] == {
        "output_family_id": "single_work_package_operator_next_actions_only",
        "family_role": "next_actions_focused_response",
        "delivery_format": "chat_text",
        "supported_response_mode": "execution_ready_summary",
        "summary_style": "next_actions_focused",
        "requires_same_output_contract": True,
    }


def test_output_consistency_rejects_unavailable_requested_family():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = validate_work_package_output_family_consistency(
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
        requested_family_id="single_work_package_operator_next_actions_only",
    )

    assert payload is not None
    assert payload["output_consistency_metadata"] == {
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "consistency_state": "rejected",
        "current_response_mode": "blocked_explainer",
        "resolved_family_id": "single_work_package_operator_next_actions_only",
        "selected_plan_id": None,
    }
    assert payload["consistency_errors"] == [
        "Requested output family is not available: single_work_package_operator_next_actions_only"
    ]
    assert payload["consistent_output_family"] is None
    assert payload["consistent_output_payload"] is None


def test_output_consistency_rejects_when_family_surface_is_blocked():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = validate_work_package_output_family_consistency(
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
    assert payload["output_consistency_metadata"] == {
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "consistency_state": "rejected",
        "current_response_mode": "blocked_explainer",
        "resolved_family_id": None,
        "selected_plan_id": None,
    }
    assert payload["consistency_errors"] == [
        "output family state must be available, got 'blocked'",
        "No output family could be resolved.",
        "No family-ready output is available.",
    ]
    assert payload["consistent_output_family"] is None
    assert payload["consistent_output_payload"] is None