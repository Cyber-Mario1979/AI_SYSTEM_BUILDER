# asbp/output_family_logic.py

from asbp.output_retry_logic import evaluate_work_package_output_attempt
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_FAMILY_SURFACE_ID = "work_package_output_family_surface_v1"


def _build_available_output_families(
    *,
    current_response_mode: str,
) -> list[dict]:
    families = [
        {
            "output_family_id": "single_work_package_operator_response",
            "family_role": "default_detailed_response",
            "delivery_format": "chat_text",
            "supported_response_mode": current_response_mode,
            "summary_style": "standard_detailed",
            "requires_same_output_contract": True,
        },
        {
            "output_family_id": "single_work_package_operator_response_brief",
            "family_role": "brief_operator_response",
            "delivery_format": "chat_text",
            "supported_response_mode": current_response_mode,
            "summary_style": "brief",
            "requires_same_output_contract": True,
        },
    ]

    if current_response_mode == "execution_ready_summary":
        families.append(
            {
                "output_family_id": "single_work_package_operator_next_actions_only",
                "family_role": "next_actions_focused_response",
                "delivery_format": "chat_text",
                "supported_response_mode": current_response_mode,
                "summary_style": "next_actions_focused",
                "requires_same_output_contract": True,
            }
        )

    return families


def build_work_package_output_family_payload(
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
    retry_payload = evaluate_work_package_output_attempt(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
        candidate_output=candidate_output,
        attempt_number=attempt_number,
        max_attempts=max_attempts,
    )
    if retry_payload is None:
        return None

    retry_metadata = retry_payload["output_retry_metadata"]
    decision_state = retry_metadata["decision_state"]
    current_response_mode = retry_metadata["current_response_mode"]

    if decision_state == "accepted":
        available_output_families = _build_available_output_families(
            current_response_mode=current_response_mode
        )
        selected_family_id = available_output_families[0]["output_family_id"]
        family_state = "available"
    else:
        available_output_families = []
        selected_family_id = None
        family_state = "blocked"

    return {
        "wp_id": retry_payload["wp_id"],
        "output_family_metadata": {
            "output_family_surface_id": OUTPUT_FAMILY_SURFACE_ID,
            "output_retry_id": retry_metadata["output_retry_id"],
            "output_contract_id": retry_metadata["output_contract_id"],
            "family_state": family_state,
            "decision_state": decision_state,
            "current_response_mode": current_response_mode,
            "selected_family_id": selected_family_id,
            "selected_plan_id": retry_metadata["selected_plan_id"],
        },
        "available_output_families": available_output_families,
        "family_boundaries": {
            "multi_work_package_output": False,
            "document_artifact_output": False,
            "cross_family_contract_variation": False,
        },
        "family_ready_output": (
            retry_payload["validated_output"]
            if decision_state == "accepted"
            else None
        ),
        "retry_policy": dict(retry_payload["retry_policy"]),
        "decision_rationale": list(retry_payload["decision_rationale"]),
        "validation_errors": list(retry_payload["validation_errors"]),
    }