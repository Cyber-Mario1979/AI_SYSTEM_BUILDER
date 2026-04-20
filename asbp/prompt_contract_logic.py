from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload
from asbp.runtime_surface_helpers import (
    EXPECTED_OUTPUT_FIELDS,
    PROMPT_CONTRACT_ID,
    PROHIBITED_FREEFORM_DRIFT,
    REQUIRED_INPUT_FIELDS,
    build_prompt_contract_state_and_mode,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def build_work_package_prompt_contract_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    runtime_boundary_payload = build_work_package_runtime_boundary_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if runtime_boundary_payload is None:
        return None

    prompt_contract_ready = runtime_boundary_payload["eligible_for_prompt_contract"]
    prompt_contract_state, prompt_contract_mode = (
        build_prompt_contract_state_and_mode(
            prompt_contract_ready=prompt_contract_ready
        )
    )

    return {
        "wp_id": runtime_boundary_payload["wp_id"],
        "prompt_contract_id": PROMPT_CONTRACT_ID,
        "prompt_contract_state": prompt_contract_state,
        "prompt_contract_mode": prompt_contract_mode,
        "eligible_for_prompt_contract": prompt_contract_ready,
        "required_input_fields": list(REQUIRED_INPUT_FIELDS),
        "expected_output_fields": list(EXPECTED_OUTPUT_FIELDS),
        "prohibited_freeform_drift": list(PROHIBITED_FREEFORM_DRIFT),
        "runtime_boundary": runtime_boundary_payload,
    }