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

HANDOFF_CONTRACT_ID = "work_package_llm_handoff_v1"
GENERATION_SURFACE_ID = "work_package_controlled_generation_surface_v1"

OUTPUT_FIELD_TYPES: dict[str, str] = {
    "response_mode": "string",
    "operator_message": "string",
    "recommended_next_actions": "list[string]",
    "grounded_input_fields_used": "list[string]",
}


def build_runtime_boundary_state(*, eligible_for_prompt_contract: bool) -> str:
    return (
        "eligible_for_prompt_contract"
        if eligible_for_prompt_contract
        else "deterministic_blocked"
    )


def build_prompt_contract_state_and_mode(
    *,
    prompt_contract_ready: bool,
) -> tuple[str, str]:
    if prompt_contract_ready:
        return "ready", "execution_ready_summary"
    return "blocked", "blocked_explainer"


def build_handoff_state(*, generation_allowed: bool) -> str:
    return "ready_for_generation" if generation_allowed else "blocked"


def build_generation_state(*, generation_allowed: bool) -> str:
    return "ready" if generation_allowed else "blocked"


def build_prose_generation_instructions(*, prompt_contract_mode: str) -> dict:
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
        "required_output_fields": list(EXPECTED_OUTPUT_FIELDS),
        "grounded_input_fields": list(REQUIRED_INPUT_FIELDS),
        "prohibited_freeform_drift": list(PROHIBITED_FREEFORM_DRIFT),
    }


def build_candidate_response_template(*, response_mode: str) -> dict:
    return {
        "response_mode": response_mode,
        "operator_message": "",
        "recommended_next_actions": [],
        "grounded_input_fields_used": [],
    }


def build_output_contract() -> dict:
    return {
        "required_output_fields": list(EXPECTED_OUTPUT_FIELDS),
        "field_types": dict(OUTPUT_FIELD_TYPES),
    }