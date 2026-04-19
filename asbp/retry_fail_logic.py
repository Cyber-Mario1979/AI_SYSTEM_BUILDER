from asbp.output_validation_logic import validate_work_package_candidate_response
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def evaluate_work_package_candidate_response_attempt(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
    candidate_output: dict,
    attempt_number: int,
    max_attempts: int,
) -> dict | None:
    validation_payload = validate_work_package_candidate_response(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
        candidate_output=candidate_output,
    )
    if validation_payload is None:
        return None

    decision_rationale: list[str] = []
    validation_state = validation_payload["validation_state"]

    if max_attempts < 1:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("invalid_retry_control_state:max_attempts_must_be_positive")
    elif attempt_number < 1:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("invalid_retry_control_state:attempt_number_must_be_positive")
    elif attempt_number > max_attempts:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("invalid_retry_control_state:attempt_number_exceeds_max_attempts")
    elif validation_state == "accepted":
        decision_state = "accepted"
        fallback_action = "use_validated_output"
        retries_remaining = max_attempts - attempt_number
        decision_rationale.append("validated_output_accepted")
    elif attempt_number < max_attempts:
        decision_state = "retry_allowed"
        fallback_action = "request_new_candidate_from_same_handoff_contract"
        retries_remaining = max_attempts - attempt_number
        decision_rationale.append("validation_rejected_but_retry_budget_remaining")
    else:
        decision_state = "fail_closed"
        fallback_action = "return_deterministic_rejection_without_acceptance"
        retries_remaining = 0
        decision_rationale.append("validation_rejected_and_retry_budget_exhausted")

    return {
        "wp_id": validation_payload["wp_id"],
        "handoff_contract_id": validation_payload["handoff_contract_id"],
        "validation_state": validation_state,
        "decision_state": decision_state,
        "fallback_action": fallback_action,
        "retry_policy": {
            "attempt_number": attempt_number,
            "max_attempts": max_attempts,
            "retries_remaining": retries_remaining,
        },
        "decision_rationale": decision_rationale,
        "validation_errors": list(validation_payload["errors"]),
        "validated_output": validation_payload["validated_output"],
    }
