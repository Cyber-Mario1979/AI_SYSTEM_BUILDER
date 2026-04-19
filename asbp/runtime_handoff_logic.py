from asbp.prompt_contract_logic import build_work_package_prompt_contract_payload
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

HANDOFF_CONTRACT_ID = "work_package_llm_handoff_v1"


def _build_prose_generation_instructions(
    *,
    prompt_contract_mode: str,
    expected_output_fields: list[str],
    required_input_fields: list[str],
    prohibited_freeform_drift: list[str],
) -> dict:
    if prompt_contract_mode == "execution_ready_summary":
        writing_goal = (
            "Summarize execution-ready deterministic state for the operator "
            "using only the structured facts in this handoff payload."
        )
    else:
        writing_goal = (
            "Explain why generation cannot proceed yet using only the "
            "structured facts, blockers, and next actions in this handoff payload."
        )

    return {
        "response_mode": prompt_contract_mode,
        "writing_goal": writing_goal,
        "required_output_fields": list(expected_output_fields),
        "grounded_input_fields": list(required_input_fields),
        "prohibited_freeform_drift": list(prohibited_freeform_drift),
    }


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
            "handoff_state": (
                "ready_for_generation"
                if generation_allowed
                else "blocked"
            ),
            "generation_allowed": generation_allowed,
            "selected_plan_id": runtime_boundary["selected_plan_id"],
            "prompt_contract_state": prompt_contract_payload["prompt_contract_state"],
            "prompt_contract_mode": prompt_contract_mode,
        },
        "structured_facts": dict(runtime_boundary["deterministic_facts"]),
        "prose_generation_instructions": _build_prose_generation_instructions(
            prompt_contract_mode=prompt_contract_mode,
            expected_output_fields=prompt_contract_payload["expected_output_fields"],
            required_input_fields=prompt_contract_payload["required_input_fields"],
            prohibited_freeform_drift=prompt_contract_payload[
                "prohibited_freeform_drift"
            ],
        ),
    }
