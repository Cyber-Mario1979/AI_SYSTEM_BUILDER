# asbp/output_mapping_logic.py

from asbp.generation_surface_logic import (
    build_work_package_generation_request_payload,
)
from asbp.output_contract_logic import build_work_package_output_contract
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

OUTPUT_MAPPING_ID = "work_package_output_mapping_v1"


def build_work_package_output_mapping_payload(
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

    output_contract_payload = build_work_package_output_contract(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if output_contract_payload is None:
        return None

    output_contract_metadata = output_contract_payload["output_contract_metadata"]
    generation_surface_metadata = generation_request_payload[
        "generation_surface_metadata"
    ]
    current_response_mode = output_contract_metadata["current_response_mode"]

    return {
        "wp_id": generation_request_payload["wp_id"],
        "output_mapping_metadata": {
            "output_mapping_id": OUTPUT_MAPPING_ID,
            "output_target_id": output_contract_metadata["output_target_id"],
            "output_contract_id": output_contract_metadata["output_contract_id"],
            "generation_surface_id": generation_surface_metadata[
                "generation_surface_id"
            ],
            "mapping_scope": output_contract_metadata["contract_scope"],
            "mapping_state": output_contract_metadata["contract_state"],
            "current_response_mode": current_response_mode,
            "selected_plan_id": output_contract_metadata["selected_plan_id"],
        },
        "source_authority": {
            "deterministic_input_source": "generation_surface_payload",
            "contract_source": "output_contract_payload",
            "source_of_truth_rule": (
                "Only validated deterministic input and the bounded output "
                "contract may shape the mapped output payload."
            ),
        },
        "deterministic_input": {
            "handoff_metadata": dict(
                generation_request_payload["deterministic_input"][
                    "handoff_metadata"
                ]
            ),
            "structured_facts": dict(
                generation_request_payload["deterministic_input"][
                    "structured_facts"
                ]
            ),
        },
        "generation_instructions": {
            "writing_goal": generation_request_payload["generation_instructions"][
                "writing_goal"
            ],
            "grounded_input_fields": list(
                generation_request_payload["generation_instructions"][
                    "grounded_input_fields"
                ]
            ),
            "prohibited_freeform_drift": list(
                generation_request_payload["generation_instructions"][
                    "prohibited_freeform_drift"
                ]
            ),
        },
        "mapped_output_contract": {
            "required_output_fields": list(
                output_contract_payload["required_output_fields"]
            ),
            "field_types": dict(output_contract_payload["field_types"]),
            "allowed_response_modes": list(
                output_contract_payload["allowed_response_modes"]
            ),
            "acceptance_shape": dict(
                output_contract_payload["acceptance_shape"]
            ),
        },
        "mapped_output_payload": {
            "response_mode": current_response_mode,
            "candidate_response_template": dict(
                generation_request_payload["candidate_response_template"]
            ),
        },
    }