"""Runtime package for the M11.1 production-structure baseline."""

from .boundary import build_work_package_runtime_boundary_payload
from .contracts import (
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
from .generation import build_work_package_generation_request_payload
from .handoff import build_work_package_llm_handoff_payload
from .output_acceptance import validate_work_package_output_before_acceptance
from .output_contract import build_work_package_output_contract
from .output_mapping import build_work_package_output_mapping_payload
from .output_retry import evaluate_work_package_output_attempt
from .output_target import build_work_package_output_target_payload
from .output_validation import (
    load_candidate_response_json,
    validate_work_package_candidate_response,
)
from .prompt_contract import build_work_package_prompt_contract_payload
from .retry_fail import evaluate_work_package_candidate_response_attempt

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
    "build_work_package_generation_request_payload",
    "build_work_package_llm_handoff_payload",
    "build_work_package_output_contract",
    "build_work_package_output_mapping_payload",
    "build_work_package_output_target_payload",
    "build_work_package_prompt_contract_payload",
    "build_work_package_runtime_boundary_payload",
    "evaluate_work_package_candidate_response_attempt",
    "evaluate_work_package_output_attempt",
    "load_candidate_response_json",
    "validate_work_package_candidate_response",
    "validate_work_package_output_before_acceptance",
]