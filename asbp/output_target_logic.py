# asbp/output_target_logic.py

from asbp.generation_surface_logic import (
    build_work_package_generation_request_payload,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_TARGET_ID = "work_package_operator_response_target_v1"
OUTPUT_TARGET_FAMILY = "single_work_package_operator_response"
ALLOWED_RESPONSE_MODES: list[str] = [
    "blocked_explainer",
    "execution_ready_summary",
]


def build_work_package_output_target_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    generation_request_payload = build_work_package_generation_request_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if generation_request_payload is None:
        return None

    generation_surface_metadata = generation_request_payload[
        "generation_surface_metadata"
    ]
    generation_allowed = generation_surface_metadata["generation_allowed"]

    return {
        "wp_id": generation_request_payload["wp_id"],
        "output_target_metadata": {
            "output_target_id": OUTPUT_TARGET_ID,
            "output_target_family": OUTPUT_TARGET_FAMILY,
            "target_scope": "single_work_package",
            "target_audience": "operator",
            "delivery_format": "chat_text",
            "target_state": "available" if generation_allowed else "blocked",
            "generation_surface_id": generation_surface_metadata[
                "generation_surface_id"
            ],
            "selected_plan_id": generation_surface_metadata["selected_plan_id"],
            "generation_allowed": generation_allowed,
        },
        "allowed_response_modes": list(ALLOWED_RESPONSE_MODES),
        "current_response_mode": generation_surface_metadata["generation_mode"],
        "target_boundaries": {
            "multi_work_package_output": False,
            "document_artifact_output": False,
            "file_export_output": False,
        },
    }