from datetime import datetime, timezone

from asbp.output_acceptance_logic import (
    validate_work_package_output_before_acceptance as legacy_validate_work_package_output_before_acceptance,
)
from asbp.output_contract_logic import (
    build_work_package_output_contract as legacy_build_work_package_output_contract,
)
from asbp.output_mapping_logic import (
    build_work_package_output_mapping_payload as legacy_build_work_package_output_mapping_payload,
)
from asbp.output_retry_logic import (
    evaluate_work_package_output_attempt as legacy_evaluate_work_package_output_attempt,
)
from asbp.output_target_logic import (
    build_work_package_output_target_payload as legacy_build_work_package_output_target_payload,
)
from asbp.output_validation_helpers import (
    build_disallowed_grounded_fields_errors,
    validate_list_of_strings_field,
    validate_non_empty_string_field,
)
from asbp.retry_decision_helpers import build_retry_decision
from asbp.runtime import (
    build_work_package_output_contract,
    build_work_package_output_mapping_payload,
    build_work_package_output_target_payload,
    evaluate_work_package_output_attempt,
    validate_work_package_output_before_acceptance,
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


def make_execution_ready_state() -> tuple[
    list[WorkPackageModel],
    list[TaskCollectionModel],
    list[TaskModel],
    list[PlanningModel],
]:
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
    return work_packages, task_collections, tasks, plans


def test_m11_5c_runtime_output_surface_wrappers_match_legacy_logic() -> None:
    work_packages, task_collections, tasks, plans = make_execution_ready_state()

    assert build_work_package_output_target_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    ) == legacy_build_work_package_output_target_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert build_work_package_output_contract(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    ) == legacy_build_work_package_output_contract(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    assert build_work_package_output_mapping_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    ) == legacy_build_work_package_output_mapping_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
    )

    candidate_output = {
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

    assert validate_work_package_output_before_acceptance(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output=candidate_output,
    ) == legacy_validate_work_package_output_before_acceptance(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output=candidate_output,
    )

    assert evaluate_work_package_output_attempt(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output=candidate_output,
        attempt_number=1,
        max_attempts=2,
    ) == legacy_evaluate_work_package_output_attempt(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id="WP-001",
        candidate_output=candidate_output,
        attempt_number=1,
        max_attempts=2,
    )


def test_m11_5c_shared_validation_helpers_preserve_existing_error_text() -> None:
    assert validate_non_empty_string_field(
        {"operator_message": "   "},
        "operator_message",
    ) == "operator_message must be a non-empty string."

    normalized_values, errors = validate_list_of_strings_field(
        {"recommended_next_actions": "not-a-list"},
        "recommended_next_actions",
    )
    assert normalized_values == []
    assert errors == ["recommended_next_actions must be a list of strings."]

    normalized_values, errors = validate_list_of_strings_field(
        {
            "grounded_input_fields_used": [
                "wp_id",
                "",
                "   ",
                5,
            ]
        },
        "grounded_input_fields_used",
    )
    assert normalized_values == ["wp_id"]
    assert errors == [
        "grounded_input_fields_used must contain only non-empty strings.",
        "grounded_input_fields_used must contain only non-empty strings.",
        "grounded_input_fields_used must contain only non-empty strings.",
    ]

    assert build_disallowed_grounded_fields_errors(
        ["wp_id", "disallowed.field"],
        allowed_grounded_fields={"wp_id"},
    ) == [
        "grounded_input_fields_used contains disallowed fields: disallowed.field"
    ]


def test_m11_5c_shared_retry_decision_helper_preserves_retry_semantics() -> None:
    assert build_retry_decision(
        validation_state="accepted",
        attempt_number=1,
        max_attempts=2,
        accepted_action="use_validated_output",
        retry_action="request_new_candidate",
        fail_closed_action="return_rejected_output_without_acceptance",
    ) == {
        "decision_state": "accepted",
        "action": "use_validated_output",
        "retries_remaining": 1,
        "decision_rationale": ["validated_output_accepted"],
    }

    assert build_retry_decision(
        validation_state="rejected",
        attempt_number=1,
        max_attempts=2,
        accepted_action="use_validated_output",
        retry_action="request_new_candidate",
        fail_closed_action="return_rejected_output_without_acceptance",
    ) == {
        "decision_state": "retry_allowed",
        "action": "request_new_candidate",
        "retries_remaining": 1,
        "decision_rationale": [
            "validation_rejected_but_retry_budget_remaining"
        ],
    }

    assert build_retry_decision(
        validation_state="accepted",
        attempt_number=3,
        max_attempts=2,
        accepted_action="use_validated_output",
        retry_action="request_new_candidate",
        fail_closed_action="return_rejected_output_without_acceptance",
    ) == {
        "decision_state": "fail_closed",
        "action": "return_rejected_output_without_acceptance",
        "retries_remaining": 0,
        "decision_rationale": [
            "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
        ],
    }