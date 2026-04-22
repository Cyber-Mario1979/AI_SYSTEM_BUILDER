from asbp.runtime_handoff_logic import build_work_package_llm_handoff_payload
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

RUNTIME_CONTROL_ID = "work_package_runtime_control_v1"


def _build_runtime_control_metadata(
    handoff_metadata: dict,
) -> dict:
    prompt_contract_mode = handoff_metadata["prompt_contract_mode"]
    generation_allowed = handoff_metadata["generation_allowed"]

    if generation_allowed:
        if prompt_contract_mode != "execution_ready_summary":
            raise ValueError(
                "Runtime control expected execution_ready_summary when "
                "generation_allowed is True."
            )
        runtime_control_state = "execution_ready_summary_only"
        control_action = "summarize_execution_ready_state"
    else:
        if prompt_contract_mode != "blocked_explainer":
            raise ValueError(
                "Runtime control expected blocked_explainer when "
                "generation_allowed is False."
            )
        runtime_control_state = "blocked_explainer_only"
        control_action = "explain_blocked_state"

    return {
        "runtime_control_id": RUNTIME_CONTROL_ID,
        "handoff_contract_id": handoff_metadata["handoff_contract_id"],
        "source_prompt_contract_id": handoff_metadata["source_prompt_contract_id"],
        "runtime_control_state": runtime_control_state,
        "control_action": control_action,
        "generation_allowed": generation_allowed,
        "operator_response_allowed": True,
        "selected_plan_id": handoff_metadata["selected_plan_id"],
        "allowed_response_modes": [prompt_contract_mode],
        "default_response_mode": prompt_contract_mode,
    }


def build_work_package_runtime_control_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    handoff_payload = build_work_package_llm_handoff_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if handoff_payload is None:
        return None

    handoff_metadata = handoff_payload["handoff_metadata"]
    runtime_control_metadata = _build_runtime_control_metadata(handoff_metadata)

    return {
        "wp_id": handoff_payload["wp_id"],
        "handoff_metadata": dict(handoff_metadata),
        "runtime_control_metadata": runtime_control_metadata,
        "structured_facts": dict(handoff_payload["structured_facts"]),
        "prose_generation_instructions": dict(
            handoff_payload["prose_generation_instructions"]
        ),
    }