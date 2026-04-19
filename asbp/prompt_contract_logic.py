from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

PROMPT_CONTRACT_ID = "work_package_runtime_prompt_contract_v1"

REQUIRED_INPUT_FIELDS: list[str] = [
    "wp_id",
    "runtime_boundary_state",
    "eligible_for_prompt_contract",
    "selected_plan_id",
    "deterministic_facts.work_package_status",
    "deterministic_facts.orchestration_stage",
    "deterministic_facts.blocking_conditions",
    "deterministic_facts.next_actions",
    "deterministic_facts.selector_context_ready",
    "deterministic_facts.work_package_task_ids",
    "deterministic_facts.bound_committed_collection_ids",
    "deterministic_facts.bound_committed_task_ids",
    "deterministic_facts.plan_ids",
]

EXPECTED_OUTPUT_FIELDS: list[str] = [
    "response_mode",
    "operator_message",
    "recommended_next_actions",
    "grounded_input_fields_used",
]

PROHIBITED_FREEFORM_DRIFT: list[str] = [
    "omit required output fields",
    "add output fields outside the declared contract",
    "invent facts outside the validated deterministic inputs",
    "change or reinterpret blocking conditions",
    "change selected plan, task scope, or collection scope",
    "propose state mutation as if it already occurred",
]


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

    return {
        "wp_id": runtime_boundary_payload["wp_id"],
        "prompt_contract_id": PROMPT_CONTRACT_ID,
        "prompt_contract_state": (
            "ready"
            if prompt_contract_ready
            else "blocked"
        ),
        "prompt_contract_mode": (
            "execution_ready_summary"
            if prompt_contract_ready
            else "blocked_explainer"
        ),
        "eligible_for_prompt_contract": prompt_contract_ready,
        "required_input_fields": list(REQUIRED_INPUT_FIELDS),
        "expected_output_fields": list(EXPECTED_OUTPUT_FIELDS),
        "prohibited_freeform_drift": list(PROHIBITED_FREEFORM_DRIFT),
        "runtime_boundary": runtime_boundary_payload,
    }
