from asbp.output_target_logic import build_work_package_output_target_payload
from asbp.runtime_surface_helpers import (
    EXPECTED_OUTPUT_FIELDS,
    OUTPUT_FIELD_TYPES,
    PROHIBITED_FREEFORM_DRIFT,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_CONTRACT_ID = "work_package_operator_response_contract_v1"


def build_work_package_output_contract(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    output_target_payload = build_work_package_output_target_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if output_target_payload is None:
        return None

    output_target_metadata = output_target_payload["output_target_metadata"]
    current_response_mode = output_target_payload["current_response_mode"]
    allowed_response_modes = list(output_target_payload["allowed_response_modes"])

    return {
        "output_contract_metadata": {
            "output_contract_id": OUTPUT_CONTRACT_ID,
            "output_target_id": output_target_metadata["output_target_id"],
            "output_target_family": output_target_metadata["output_target_family"],
            "contract_scope": output_target_metadata["target_scope"],
            "target_audience": output_target_metadata["target_audience"],
            "delivery_format": output_target_metadata["delivery_format"],
            "contract_state": output_target_metadata["target_state"],
            "current_response_mode": current_response_mode,
            "selected_plan_id": output_target_metadata["selected_plan_id"],
        },
        "required_output_fields": list(EXPECTED_OUTPUT_FIELDS),
        "field_types": dict(OUTPUT_FIELD_TYPES),
        "allowed_response_modes": allowed_response_modes,
        "prohibited_contract_drift": list(PROHIBITED_FREEFORM_DRIFT),
        "acceptance_shape": {
            "top_level_container": "object",
            "extra_fields_allowed": False,
            "field_rules": {
                "response_mode": {
                    "type": "string",
                    "allowed_values": allowed_response_modes,
                    "must_equal_current_response_mode": True,
                },
                "operator_message": {
                    "type": "string",
                    "allow_empty": False,
                },
                "recommended_next_actions": {
                    "type": "list[string]",
                    "allow_empty": True,
                },
                "grounded_input_fields_used": {
                    "type": "list[string]",
                    "allow_empty": False,
                },
            },
        },
    }