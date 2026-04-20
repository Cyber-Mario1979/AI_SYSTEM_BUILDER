from asbp.prompt_contract_logic import build_work_package_prompt_contract_payload
from asbp.runtime_surface_helpers import (
    HANDOFF_CONTRACT_ID,
    build_handoff_state,
    build_prose_generation_instructions,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


def build_work_package_llm_handoff_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    prompt_contract_payload = build_work_package_prompt_contract_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if prompt_contract_payload is None:
        return None

    runtime_boundary = prompt_contract_payload["runtime_boundary"]
    prompt_contract_mode = prompt_contract_payload["prompt_contract_mode"]
    generation_allowed = prompt_contract_payload["eligible_for_prompt_contract"]

    return {
        "wp_id": prompt_contract_payload["wp_id"],
        "handoff_metadata": {
            "handoff_contract_id": HANDOFF_CONTRACT_ID,
            "source_prompt_contract_id": prompt_contract_payload["prompt_contract_id"],
            "handoff_state": build_handoff_state(
                generation_allowed=generation_allowed
            ),
            "generation_allowed": generation_allowed,
            "selected_plan_id": runtime_boundary["selected_plan_id"],
            "prompt_contract_state": prompt_contract_payload["prompt_contract_state"],
            "prompt_contract_mode": prompt_contract_mode,
        },
        "structured_facts": dict(runtime_boundary["deterministic_facts"]),
        "prose_generation_instructions": build_prose_generation_instructions(
            prompt_contract_mode=prompt_contract_mode
        ),
    }