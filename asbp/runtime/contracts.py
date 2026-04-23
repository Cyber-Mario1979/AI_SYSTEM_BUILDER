"""Runtime contract helpers for the M11.1 production-structure baseline."""

from asbp.runtime_surface_helpers import (
    EXPECTED_OUTPUT_FIELDS,
    GENERATION_SURFACE_ID,
    HANDOFF_CONTRACT_ID,
    MODEL_MAY,
    MODEL_MAY_NOT,
    OUTPUT_FIELD_TYPES,
    PROMPT_CONTRACT_ID,
    PROHIBITED_FREEFORM_DRIFT,
    REQUIRED_INPUT_FIELDS,
    build_candidate_response_template,
    build_generation_state,
    build_handoff_state,
    build_output_contract,
    build_prompt_contract_state_and_mode,
    build_prose_generation_instructions,
    build_runtime_boundary_state,
)

__all__ = [
    "EXPECTED_OUTPUT_FIELDS",
    "GENERATION_SURFACE_ID",
    "HANDOFF_CONTRACT_ID",
    "MODEL_MAY",
    "MODEL_MAY_NOT",
    "OUTPUT_FIELD_TYPES",
    "PROMPT_CONTRACT_ID",
    "PROHIBITED_FREEFORM_DRIFT",
    "REQUIRED_INPUT_FIELDS",
    "build_candidate_response_template",
    "build_generation_state",
    "build_handoff_state",
    "build_output_contract",
    "build_prompt_contract_state_and_mode",
    "build_prose_generation_instructions",
    "build_runtime_boundary_state",
]