from datetime import datetime, timezone

from asbp.output_validation_logic import validate_work_package_candidate_response
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


def test_output_validation_returns_none_for_missing_work_package():
    payload = validate_work_package_candidate_response(
        [],
        [],
        [],
        [],
        wp_id="WP-404",
        candidate_output={},
    )

    assert payload is None


def test_output_validation_accepts_blocked_explainer_candidate():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = validate_work_package_candidate_response(
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
    )

    assert payload["validation_state"] == "accepted"
    assert payload["expected_response_mode"] == "blocked_explainer"
    assert payload["candidate_response_mode"] == "blocked_explainer"
    assert payload["errors"] == []


def test_output_validation_accepts_execution_ready_summary_candidate():
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

    payload = validate_work_package_candidate_response(
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
    )

    assert payload["validation_state"] == "accepted"
    assert payload["expected_response_mode"] == "execution_ready_summary"
    assert payload["candidate_response_mode"] == "execution_ready_summary"
    assert payload["errors"] == []


def test_output_validation_rejects_contract_breaking_candidate():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = validate_work_package_candidate_response(
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
    )

    assert payload["validation_state"] == "rejected"
    assert payload["validated_output"] is None
    assert payload["errors"] == [
        "Unexpected output fields: extra_field",
        "response_mode mismatch: expected blocked_explainer, got 'execution_ready_summary'",
        "operator_message must be a non-empty string.",
        "recommended_next_actions must be a list of strings.",
        "grounded_input_fields_used contains disallowed fields: disallowed.field",
    ]
