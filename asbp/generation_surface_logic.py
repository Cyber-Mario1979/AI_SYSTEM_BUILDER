from asbp.runtime_control_logic import build_work_package_runtime_control_payload
from asbp.runtime_surface_helpers import (
    GENERATION_SURFACE_ID,
    build_candidate_response_template,
    build_generation_state,
    build_output_contract,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def build_work_package_generation_request_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    runtime_control_payload = build_work_package_runtime_control_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if runtime_control_payload is None:
        return None

    handoff_metadata = runtime_control_payload["handoff_metadata"]
    runtime_control_metadata = runtime_control_payload["runtime_control_metadata"]
    structured_facts = runtime_control_payload["structured_facts"]
    instructions = runtime_control_payload["prose_generation_instructions"]
    generation_allowed = runtime_control_metadata["generation_allowed"]

    return {
        "wp_id": runtime_control_payload["wp_id"],
        "generation_surface_metadata": {
            "generation_surface_id": GENERATION_SURFACE_ID,
            "runtime_control_id": runtime_control_metadata["runtime_control_id"],
            "handoff_contract_id": runtime_control_metadata["handoff_contract_id"],
            "source_prompt_contract_id": runtime_control_metadata[
                "source_prompt_contract_id"
            ],
            "generation_state": build_generation_state(
                generation_allowed=generation_allowed
            ),
            "generation_allowed": generation_allowed,
            "operator_response_allowed": runtime_control_metadata[
                "operator_response_allowed"
            ],
            "runtime_control_state": runtime_control_metadata["runtime_control_state"],
            "control_action": runtime_control_metadata["control_action"],
            "allowed_response_modes": list(
                runtime_control_metadata["allowed_response_modes"]
            ),
            "generation_mode": runtime_control_metadata["default_response_mode"],
            "generation_scope": "single_work_package_operator_response",
            "selected_plan_id": runtime_control_metadata["selected_plan_id"],
        },
        "deterministic_input": {
            "handoff_metadata": dict(handoff_metadata),
            "runtime_control_metadata": dict(runtime_control_metadata),
            "structured_facts": dict(structured_facts),
        },
        "generation_instructions": {
            "writing_goal": instructions["writing_goal"],
            "grounded_input_fields": list(
                instructions["grounded_input_fields"]
            ),
            "prohibited_freeform_drift": list(
                instructions["prohibited_freeform_drift"]
            ),
        },
        "output_contract": build_output_contract(),
        "candidate_response_template": build_candidate_response_template(
            response_mode=runtime_control_metadata["default_response_mode"]
        ),
    }