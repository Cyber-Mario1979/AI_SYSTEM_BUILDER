# tests/test_output_failure_logic.py

from datetime import datetime, timezone

from asbp.output_failure_logic import build_work_package_output_failure_payload
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


def test_output_failure_returns_none_for_missing_work_package():
    payload = build_work_package_output_failure_payload(
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


def test_output_failure_accepts_consistent_output():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_failure_payload(
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
    assert payload["output_failure_metadata"] == {
        "output_failure_id": "work_package_output_failure_v1",
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "failure_state": "accepted",
        "failure_action": "use_consistent_output",
        "failure_reason_category": None,
        "current_response_mode": "blocked_explainer",
        "resolved_family_id": "single_work_package_operator_response",
        "selected_plan_id": None,
    }
    assert payload["failure_feedback"] is None
    assert payload["accepted_output_family"] == {
        "output_family_id": "single_work_package_operator_response",
        "family_role": "default_detailed_response",
        "delivery_format": "chat_text",
        "supported_response_mode": "blocked_explainer",
        "summary_style": "standard_detailed",
        "requires_same_output_contract": True,
    }
    assert payload["accepted_output_payload"] == {
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


def test_output_failure_requests_retry_for_retryable_generation_rejection():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_failure_payload(
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
    assert payload["output_failure_metadata"] == {
        "output_failure_id": "work_package_output_failure_v1",
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "failure_state": "retry_needed",
        "failure_action": "request_regenerated_output_from_same_mapping_contract",
        "failure_reason_category": "retryable_generation_rejection",
        "current_response_mode": "blocked_explainer",
        "resolved_family_id": None,
        "selected_plan_id": None,
    }
    assert payload["failure_feedback"] == {
        "operator_message": (
            "Output generation was rejected before acceptance. "
            "Regenerate a new candidate output using the same deterministic "
            "mapping and output contract."
        ),
        "recommended_next_actions": [
            "Regenerate the candidate output from the same deterministic mapping and output contract.",
            "Keep the current response mode and grounded input boundaries unchanged.",
            "Retry budget remaining after this rejection: 1.",
        ],
    }
    assert payload["accepted_output_family"] is None
    assert payload["accepted_output_payload"] is None
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_but_retry_budget_remaining"
    ]


def test_output_failure_fails_closed_when_retry_budget_is_exhausted():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_failure_payload(
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

    assert payload is not None
    assert payload["output_failure_metadata"] == {
        "output_failure_id": "work_package_output_failure_v1",
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "failure_state": "fail_closed",
        "failure_action": "return_deterministic_failure_without_output_acceptance",
        "failure_reason_category": "retry_budget_exhausted",
        "current_response_mode": "blocked_explainer",
        "resolved_family_id": None,
        "selected_plan_id": None,
    }
    assert payload["failure_feedback"] == {
        "operator_message": (
            "Output generation failed closed. "
            "No output family or payload may be accepted from this attempt."
        ),
        "recommended_next_actions": [
            "Do not accept the rejected candidate output.",
            "Review the deterministic rejection details before starting a new attempt.",
            "Start a clean new attempt only after fixing the recorded validation errors.",
        ],
    }
    assert payload["accepted_output_family"] is None
    assert payload["accepted_output_payload"] is None
    assert payload["retry_policy"] == {
        "attempt_number": 2,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "validation_rejected_and_retry_budget_exhausted"
    ]


def test_output_failure_fails_closed_for_unavailable_requested_family():
    work_packages = [
        WorkPackageModel(
            wp_id="WP-001",
            title="Tablet press qualification",
            status="open",
        )
    ]

    payload = build_work_package_output_failure_payload(
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
    assert payload["output_failure_metadata"] == {
        "output_failure_id": "work_package_output_failure_v1",
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "failure_state": "fail_closed",
        "failure_action": "return_deterministic_failure_without_output_acceptance",
        "failure_reason_category": "non_retryable_output_family_rejection",
        "current_response_mode": "blocked_explainer",
        "resolved_family_id": "single_work_package_operator_next_actions_only",
        "selected_plan_id": None,
    }
    assert payload["failure_feedback"] == {
        "operator_message": (
            "Output generation failed closed. "
            "No output family or payload may be accepted from this attempt."
        ),
        "recommended_next_actions": [
            "Do not accept the rejected candidate output.",
            "Review the deterministic rejection details before starting a new attempt.",
            "Correct the requested output family selection before retrying.",
        ],
    }
    assert payload["accepted_output_family"] is None
    assert payload["accepted_output_payload"] is None
    assert payload["retry_policy"] == {
        "attempt_number": 1,
        "max_attempts": 2,
        "retries_remaining": 1,
    }
    assert payload["decision_rationale"] == ["validated_output_accepted"]


def test_output_failure_fails_closed_for_invalid_retry_control_state():
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

    payload = build_work_package_output_failure_payload(
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
        attempt_number=3,
        max_attempts=2,
    )

    assert payload is not None
    assert payload["output_failure_metadata"] == {
        "output_failure_id": "work_package_output_failure_v1",
        "output_consistency_id": "work_package_output_consistency_v1",
        "output_family_surface_id": "work_package_output_family_surface_v1",
        "output_contract_id": "work_package_operator_response_contract_v1",
        "failure_state": "fail_closed",
        "failure_action": "return_deterministic_failure_without_output_acceptance",
        "failure_reason_category": "non_retryable_retry_control_rejection",
        "current_response_mode": "execution_ready_summary",
        "resolved_family_id": None,
        "selected_plan_id": "PLAN-001",
    }
    assert payload["failure_feedback"] == {
        "operator_message": (
            "Output generation failed closed. "
            "No output family or payload may be accepted from this attempt."
        ),
        "recommended_next_actions": [
            "Do not accept the rejected candidate output.",
            "Review the deterministic rejection details before starting a new attempt.",
            "Correct the retry control inputs before retrying.",
        ],
    }
    assert payload["accepted_output_family"] is None
    assert payload["accepted_output_payload"] is None
    assert payload["retry_policy"] == {
        "attempt_number": 3,
        "max_attempts": 2,
        "retries_remaining": 0,
    }
    assert payload["decision_rationale"] == [
        "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
    ]