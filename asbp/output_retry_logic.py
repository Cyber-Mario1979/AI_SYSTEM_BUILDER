from asbp.output_acceptance_logic import (
    validate_work_package_output_before_acceptance,
)
from asbp.retry_decision_helpers import build_retry_decision
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
    retry_decision = build_retry_decision(
        validation_state=validation_state,
        attempt_number=attempt_number,
        max_attempts=max_attempts,
        accepted_action="use_validated_output",
        retry_action="request_regenerated_output_from_same_mapping_contract",
        fail_closed_action="return_rejected_output_without_acceptance",
    )

    return {
        "wp_id": acceptance_payload["wp_id"],
        "output_retry_metadata": {
            "output_retry_id": OUTPUT_RETRY_ID,
            "output_acceptance_id": acceptance_metadata["output_acceptance_id"],
            "output_mapping_id": acceptance_metadata["output_mapping_id"],
            "output_contract_id": acceptance_metadata["output_contract_id"],
            "validation_state": validation_state,
            "decision_state": retry_decision["decision_state"],
            "regeneration_action": retry_decision["action"],
            "current_response_mode": acceptance_metadata["current_response_mode"],
            "selected_plan_id": acceptance_metadata["selected_plan_id"],
        },
        "retry_policy": {
            "attempt_number": attempt_number,
            "max_attempts": max_attempts,
            "retries_remaining": retry_decision["retries_remaining"],
        },
        "decision_rationale": list(retry_decision["decision_rationale"]),
        "validation_errors": list(acceptance_payload["errors"]),
        "validated_output": acceptance_payload["validated_output"],
    }