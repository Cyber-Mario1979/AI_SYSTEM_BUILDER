# asbp/output_failure_logic.py

from asbp.output_consistency_logic import (
    validate_work_package_output_family_consistency,
)
from asbp.output_surface_helpers import (
    INVALID_RETRY_CONTROL_PREFIX,
    REQUESTED_OUTPUT_FAMILY_UNAVAILABLE_PREFIX,
    build_output_runtime_trace_payload,
    list_contains_prefixed_value,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_FAILURE_ID = "work_package_output_failure_v1"


def _resolve_failure_reason_category(
    *,
    consistency_state: str,
    consistency_errors: list[str],
    decision_rationale: list[str],
) -> str | None:
    if consistency_state == "accepted":
        return None

    if "validation_rejected_but_retry_budget_remaining" in decision_rationale:
        return "retryable_generation_rejection"

    if list_contains_prefixed_value(
        consistency_errors,
        REQUESTED_OUTPUT_FAMILY_UNAVAILABLE_PREFIX,
    ):
        return "non_retryable_output_family_rejection"

    if list_contains_prefixed_value(
        decision_rationale,
        INVALID_RETRY_CONTROL_PREFIX,
    ):
        return "non_retryable_retry_control_rejection"

    if "validation_rejected_and_retry_budget_exhausted" in decision_rationale:
        return "retry_budget_exhausted"

    return "non_retryable_consistency_rejection"


def _build_retry_needed_feedback(*, retries_remaining: int) -> dict:
    return {
        "operator_message": (
            "Output generation was rejected before acceptance. "
            "Regenerate a new candidate output using the same deterministic "
            "mapping and output contract."
        ),
        "recommended_next_actions": [
            "Regenerate the candidate output from the same deterministic mapping and output contract.",
            "Keep the current response mode and grounded input boundaries unchanged.",
            f"Retry budget remaining after this rejection: {retries_remaining}.",
        ],
    }


def _build_fail_closed_feedback(
    *,
    consistency_errors: list[str],
    decision_rationale: list[str],
) -> dict:
    recommended_next_actions = [
        "Do not accept the rejected candidate output.",
        "Review the deterministic rejection details before starting a new attempt.",
    ]

    if list_contains_prefixed_value(
        consistency_errors,
        REQUESTED_OUTPUT_FAMILY_UNAVAILABLE_PREFIX,
    ):
        recommended_next_actions.append(
            "Correct the requested output family selection before retrying."
        )
    elif "validation_rejected_and_retry_budget_exhausted" in decision_rationale:
        recommended_next_actions.append(
            "Start a clean new attempt only after fixing the recorded validation errors."
        )
    elif list_contains_prefixed_value(
        decision_rationale,
        INVALID_RETRY_CONTROL_PREFIX,
    ):
        recommended_next_actions.append(
            "Correct the retry control inputs before retrying."
        )

    return {
        "operator_message": (
            "Output generation failed closed. "
            "No output family or payload may be accepted from this attempt."
        ),
        "recommended_next_actions": recommended_next_actions,
    }


def build_work_package_output_failure_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
    candidate_output: object,
    attempt_number: int,
    max_attempts: int,
    requested_family_id: str | None = None,
) -> dict | None:
    consistency_payload = validate_work_package_output_family_consistency(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
        candidate_output=candidate_output,
        attempt_number=attempt_number,
        max_attempts=max_attempts,
        requested_family_id=requested_family_id,
    )
    if consistency_payload is None:
        return None

    consistency_metadata = consistency_payload["output_consistency_metadata"]
    consistency_state = consistency_metadata["consistency_state"]
    retry_policy = dict(consistency_payload["retry_policy"])
    decision_rationale = list(consistency_payload["decision_rationale"])
    consistency_errors = list(consistency_payload["consistency_errors"])
    validation_errors = list(consistency_payload["validation_errors"])

    failure_reason_category = _resolve_failure_reason_category(
        consistency_state=consistency_state,
        consistency_errors=consistency_errors,
        decision_rationale=decision_rationale,
    )

    if consistency_state == "accepted":
        failure_state = "accepted"
        failure_action = "use_consistent_output"
        failure_feedback = None
    elif "validation_rejected_but_retry_budget_remaining" in decision_rationale:
        failure_state = "retry_needed"
        failure_action = "request_regenerated_output_from_same_mapping_contract"
        failure_feedback = _build_retry_needed_feedback(
            retries_remaining=retry_policy["retries_remaining"]
        )
    else:
        failure_state = "fail_closed"
        failure_action = "return_deterministic_failure_without_output_acceptance"
        failure_feedback = _build_fail_closed_feedback(
            consistency_errors=consistency_errors,
            decision_rationale=decision_rationale,
        )

    trace_payload = build_output_runtime_trace_payload(
        retry_policy=retry_policy,
        decision_rationale=decision_rationale,
        validation_errors=validation_errors,
        consistency_errors=consistency_errors,
    )

    return {
        "wp_id": consistency_payload["wp_id"],
        "output_failure_metadata": {
            "output_failure_id": OUTPUT_FAILURE_ID,
            "output_consistency_id": consistency_metadata["output_consistency_id"],
            "output_family_surface_id": consistency_metadata[
                "output_family_surface_id"
            ],
            "output_contract_id": consistency_metadata["output_contract_id"],
            "failure_state": failure_state,
            "failure_action": failure_action,
            "failure_reason_category": failure_reason_category,
            "current_response_mode": consistency_metadata["current_response_mode"],
            "resolved_family_id": consistency_metadata["resolved_family_id"],
            "selected_plan_id": consistency_metadata["selected_plan_id"],
        },
        "failure_feedback": failure_feedback,
        "accepted_output_family": (
            consistency_payload["consistent_output_family"]
            if failure_state == "accepted"
            else None
        ),
        "accepted_output_payload": (
            consistency_payload["consistent_output_payload"]
            if failure_state == "accepted"
            else None
        ),
        **trace_payload,
    }