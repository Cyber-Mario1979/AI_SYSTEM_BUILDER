from asbp.orchestration_logic import build_work_package_orchestration_payload
from asbp.runtime_surface_helpers import (
    MODEL_MAY,
    MODEL_MAY_NOT,
    build_runtime_boundary_state,
)
from asbp.state_model import (
    PlanningModel,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)


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
        "runtime_boundary_state": build_runtime_boundary_state(
            eligible_for_prompt_contract=eligible_for_prompt_contract
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