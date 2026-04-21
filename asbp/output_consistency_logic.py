# asbp/output_consistency_logic.py

from asbp.output_family_logic import build_work_package_output_family_payload
from asbp.output_surface_helpers import (
    build_output_runtime_trace_payload,
    find_output_family_by_id,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_CONSISTENCY_ID = "work_package_output_consistency_v1"


def validate_work_package_output_family_consistency(
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
    family_payload = build_work_package_output_family_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
        candidate_output=candidate_output,
        attempt_number=attempt_number,
        max_attempts=max_attempts,
    )
    if family_payload is None:
        return None

    family_metadata = family_payload["output_family_metadata"]
    available_output_families = family_payload["available_output_families"]
    family_state = family_metadata["family_state"]
    current_response_mode = family_metadata["current_response_mode"]

    resolved_family_id = (
        requested_family_id
        if requested_family_id is not None
        else family_metadata["selected_family_id"]
    )

    errors: list[str] = []

    if family_state != "available":
        errors.append(
            f"output family state must be available, got {family_state!r}"
        )

    if resolved_family_id is None:
        errors.append("No output family could be resolved.")
        selected_family = None
    else:
        selected_family = find_output_family_by_id(
            available_output_families,
            resolved_family_id,
        )
        if selected_family is None:
            errors.append(
                f"Requested output family is not available: {resolved_family_id}"
            )

    family_ready_output = family_payload["family_ready_output"]
    if family_ready_output is None:
        errors.append("No family-ready output is available.")

    if selected_family is not None:
        supported_response_mode = selected_family["supported_response_mode"]
        if supported_response_mode != current_response_mode:
            errors.append(
                "Selected family response-mode mismatch: "
                f"expected {current_response_mode}, got {supported_response_mode}"
            )

    trace_payload = build_output_runtime_trace_payload(
        retry_policy=family_payload["retry_policy"],
        decision_rationale=family_payload["decision_rationale"],
        validation_errors=family_payload["validation_errors"],
    )

    return {
        "wp_id": family_payload["wp_id"],
        "output_consistency_metadata": {
            "output_consistency_id": OUTPUT_CONSISTENCY_ID,
            "output_family_surface_id": family_metadata["output_family_surface_id"],
            "output_contract_id": family_metadata["output_contract_id"],
            "consistency_state": "accepted" if not errors else "rejected",
            "current_response_mode": current_response_mode,
            "resolved_family_id": resolved_family_id,
            "selected_plan_id": family_metadata["selected_plan_id"],
        },
        "consistency_errors": errors,
        "consistent_output_family": selected_family if not errors else None,
        "consistent_output_payload": family_ready_output if not errors else None,
        **trace_payload,
    }