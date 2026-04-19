from asbp.orchestration_logic import build_work_package_orchestration_payload
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)

MODEL_MAY: list[str] = [
    "consume only validated deterministic facts exposed through this boundary payload",
    "transform those facts into bounded language outputs only after a future prompt contract is defined",
    "return only fields explicitly requested by a future runtime contract",
]

MODEL_MAY_NOT: list[str] = [
    "mutate persisted state",
    "invent facts, statuses, dates, dependencies, or identifiers",
    "change selected work package, selected plan, task scope, or collection scope",
    "resolve blocked deterministic state by inference",
    "bypass deterministic validation or acceptance rules",
]


def build_work_package_runtime_boundary_payload(
    work_packages: list[WorkPackageModel],
    task_collections: list[TaskCollectionModel],
    tasks: list[TaskModel],
    plans: list[PlanningModel],
    *,
    wp_id: str,
) -> dict | None:
    orchestration_payload = build_work_package_orchestration_payload(
        work_packages,
        task_collections,
        tasks,
        plans,
        wp_id=wp_id,
    )
    if orchestration_payload is None:
        return None

    orchestration_stage = orchestration_payload["orchestration_stage"]
    eligible_for_prompt_contract = orchestration_stage == "execution_ready"

    return {
        "wp_id": orchestration_payload["wp_id"],
        "runtime_boundary_state": (
            "eligible_for_prompt_contract"
            if eligible_for_prompt_contract
            else "deterministic_blocked"
        ),
        "eligible_for_prompt_contract": eligible_for_prompt_contract,
        "selected_plan_id": orchestration_payload["selected_plan_id"],
        "deterministic_facts": {
            "work_package_status": orchestration_payload["work_package_status"],
            "orchestration_stage": orchestration_stage,
            "blocking_conditions": list(orchestration_payload["blocking_conditions"]),
            "next_actions": list(orchestration_payload["next_actions"]),
            "selector_context_ready": orchestration_payload["selector_context_ready"],
            "work_package_task_ids": list(orchestration_payload["work_package_task_ids"]),
            "bound_committed_collection_ids": list(
                orchestration_payload["bound_committed_collection_ids"]
            ),
            "bound_committed_task_ids": list(
                orchestration_payload["bound_committed_task_ids"]
            ),
            "plan_ids": list(orchestration_payload["plan_ids"]),
        },
        "model_may": list(MODEL_MAY),
        "model_may_not": list(MODEL_MAY_NOT),
    }
