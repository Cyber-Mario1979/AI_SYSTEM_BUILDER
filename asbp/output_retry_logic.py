# asbp/output_retry_logic.py

from asbp.output_acceptance_logic import (
    validate_work_package_output_before_acceptance,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_RETRY_ID = "work_package_output_retry_v1"


def evaluate_work_package_output_attempt(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
    candidate_output: object,
    attempt_number: int,
    max_attempts: int,
) -> dict | None:
    acceptance_payload = validate_work_package_output_before_acceptance(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
        candidate_output=candidate_output,
    )
    if acceptance_payload is None:
        return None

    acceptance_metadata = acceptance_payload["output_acceptance_metadata"]
    validation_state = acceptance_metadata["validation_state"]
    decision_rationale: list[str] = []

    if max_attempts < 1:
        decision_state = "fail_closed"
        regeneration_action = "return_rejected_output_without_acceptance"
        retries_remaining = 0
        decision_rationale.append(
            "invalid_retry_control_state:max_attempts_must_be_positive"
        )
    elif attempt_number < 1:
        decision_state = "fail_closed"
        regeneration_action = "return_rejected_output_without_acceptance"
        retries_remaining = 0
        decision_rationale.append(
            "invalid_retry_control_state:attempt_number_must_be_positive"
        )
    elif attempt_number > max_attempts:
        decision_state = "fail_closed"
        regeneration_action = "return_rejected_output_without_acceptance"
        retries_remaining = 0
        decision_rationale.append(
            "invalid_retry_control_state:attempt_number_exceeds_max_attempts"
        )
    elif validation_state == "accepted":
        decision_state = "accepted"
        regeneration_action = "use_validated_output"
        retries_remaining = max_attempts - attempt_number
        decision_rationale.append("validated_output_accepted")
    elif attempt_number < max_attempts:
        decision_state = "retry_allowed"
        regeneration_action = "request_regenerated_output_from_same_mapping_contract"
        retries_remaining = max_attempts - attempt_number
        decision_rationale.append(
            "validation_rejected_but_retry_budget_remaining"
        )
    else:
        decision_state = "fail_closed"
        regeneration_action = "return_rejected_output_without_acceptance"
        retries_remaining = 0
        decision_rationale.append(
            "validation_rejected_and_retry_budget_exhausted"
        )

    return {
        "wp_id": acceptance_payload["wp_id"],
        "output_retry_metadata": {
            "output_retry_id": OUTPUT_RETRY_ID,
            "output_acceptance_id": acceptance_metadata["output_acceptance_id"],
            "output_mapping_id": acceptance_metadata["output_mapping_id"],
            "output_contract_id": acceptance_metadata["output_contract_id"],
            "validation_state": validation_state,
            "decision_state": decision_state,
            "regeneration_action": regeneration_action,
            "current_response_mode": acceptance_metadata["current_response_mode"],
            "selected_plan_id": acceptance_metadata["selected_plan_id"],
        },
        "retry_policy": {
            "attempt_number": attempt_number,
            "max_attempts": max_attempts,
            "retries_remaining": retries_remaining,
        },
        "decision_rationale": decision_rationale,
        "validation_errors": list(acceptance_payload["errors"]),
        "validated_output": acceptance_payload["validated_output"],
    }