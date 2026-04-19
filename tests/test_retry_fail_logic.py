from datetime import datetime, timezone

from asbp.retry_fail_logic import evaluate_work_package_candidate_response_attempt
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


def test_retry_fail_returns_none_for_missing_work_package():
    payload = evaluate_work_package_candidate_response_attempt(
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


def test_retry_fail_accepts_valid_candidate_output():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_candidate_response_attempt(
        work_packages,
        [],
        [],
        [],
        wp_id="WP-001",
        candidate_output={
            "response_mode": "blocked_explainer",
            "operator_message": "Selector context is still required.",
            "recommended_next_actions": [
                "Complete deterministic selector context before orchestration can proceed."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "deterministic_facts.orchestration_stage",
                "deterministic_facts.next_actions",
            ],
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload["validation_state"] == "accepted"
    assert payload["decision_state"] == "accepted"
    assert payload["fallback_action"] == "use_validated_output"
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == ["validated_output_accepted"]


def test_retry_fail_allows_retry_when_validation_rejects_and_budget_remains():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_candidate_response_attempt(
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
        },
        attempt_number=1,
        max_attempts=2,
    )

    assert payload["validation_state"] == "rejected"
    assert payload["decision_state"] == "retry_allowed"
    assert payload["fallback_action"] == "request_new_candidate_from_same_handoff_contract"
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_but_retry_budget_remaining"
    ]


def test_retry_fail_closes_when_validation_rejects_and_budget_is_exhausted():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = evaluate_work_package_candidate_response_attempt(
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
        },
        attempt_number=2,
        max_attempts=2,
    )

    assert payload["validation_state"] == "rejected"
    assert payload["decision_state"] == "fail_closed"
    assert payload["fallback_action"] == "return_deterministic_rejection_without_acceptance"
    assert payload["retry_policy"] == {
        "attempt_number": 2,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_and_retry_budget_exhausted"
    ]


def test_retry_fail_closes_on_invalid_retry_control_state():
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

    payload = evaluate_work_package_candidate_response_attempt(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output={
            "response_mode": "execution_ready_summary",
            "operator_message": "The work package is ready for generation.",
            "recommended_next_actions": [
                "Execution-ready deterministic state reached."
            ],
            "grounded_input_fields_used": [
                "wp_id",
                "selected_plan_id",
                "deterministic_facts.orchestration_stage",
            ],
        },
        attempt_number=3,
        max_attempts=2,
    )

    assert payload["validation_state"] == "accepted"
    assert payload["decision_state"] == "fail_closed"
    assert payload["fallback_action"] == "return_deterministic_rejection_without_acceptance"
    assert payload["retry_policy"] == {
        "attempt_number": 3,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
    ]
