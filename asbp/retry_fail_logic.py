from asbp.output_validation_logic import validate_work_package_candidate_response
from asbp.retry_decision_helpers import build_retry_decision
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

    validation_state = validation_payload["validation_state"]
    retry_decision = build_retry_decision(
        validation_state=validation_state,
        attempt_number=attempt_number,
        max_attempts=max_attempts,
        accepted_action="use_validated_output",
        retry_action="request_new_candidate_from_same_handoff_contract",
        fail_closed_action="return_deterministic_rejection_without_acceptance",
    )

    return {
        "wp_id": validation_payload["wp_id"],
        "handoff_contract_id": validation_payload["handoff_contract_id"],
        "validation_state": validation_state,
        "decision_state": retry_decision["decision_state"],
        "fallback_action": retry_decision["action"],
        "retry_policy": {
            "attempt_number": attempt_number,
            "max_attempts": max_attempts,
            "retries_remaining": retry_decision["retries_remaining"],
        },
        "decision_rationale": list(retry_decision["decision_rationale"]),
        "validation_errors": list(validation_payload["errors"]),
        "validated_output": validation_payload["validated_output"],
    }