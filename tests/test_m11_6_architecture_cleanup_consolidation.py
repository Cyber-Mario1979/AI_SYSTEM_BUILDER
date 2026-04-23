import asbp.runtime as runtime_pkg
import asbp.runtime.boundary as runtime_boundary_module
import asbp.runtime.contracts as runtime_contracts_module
import asbp.runtime.control as runtime_control_module
import asbp.runtime.generation as runtime_generation_module
import asbp.runtime.handoff as runtime_handoff_module
import asbp.runtime.output_acceptance as runtime_output_acceptance_module
import asbp.runtime.output_contract as runtime_output_contract_module
import asbp.runtime.output_mapping as runtime_output_mapping_module
import asbp.runtime.output_retry as runtime_output_retry_module
import asbp.runtime.output_target as runtime_output_target_module
import asbp.runtime.output_validation as runtime_output_validation_module
import asbp.runtime.prompt_contract as runtime_prompt_contract_module
import asbp.runtime.retry_fail as runtime_retry_fail_module
from asbp.generation_surface_logic import build_work_package_generation_request_payload
from asbp.output_acceptance_logic import validate_work_package_output_before_acceptance
from asbp.output_contract_logic import build_work_package_output_contract
from asbp.output_mapping_logic import build_work_package_output_mapping_payload
from asbp.output_retry_logic import evaluate_work_package_output_attempt
from asbp.output_target_logic import build_work_package_output_target_payload
from asbp.output_validation_logic import (
    load_candidate_response_json,
    validate_work_package_candidate_response,
)
from asbp.prompt_contract_logic import build_work_package_prompt_contract_payload
from asbp.retry_fail_logic import evaluate_work_package_candidate_response_attempt
from asbp.runtime_boundary_logic import build_work_package_runtime_boundary_payload
from asbp.runtime_control_logic import build_work_package_runtime_control_payload
from asbp.runtime_handoff_logic import build_work_package_llm_handoff_payload
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


def test_m11_6_runtime_wrapper_modules_export_explicit_callable_surfaces() -> None:
    assert runtime_boundary_module.__all__ == ["build_work_package_runtime_boundary_payload"]
    assert runtime_control_module.__all__ == ["build_work_package_runtime_control_payload"]
    assert runtime_generation_module.__all__ == ["build_work_package_generation_request_payload"]
    assert runtime_handoff_module.__all__ == ["build_work_package_llm_handoff_payload"]
    assert runtime_prompt_contract_module.__all__ == ["build_work_package_prompt_contract_payload"]
    assert runtime_output_validation_module.__all__ == [
        "load_candidate_response_json",
        "validate_work_package_candidate_response",
    ]
    assert runtime_retry_fail_module.__all__ == [
        "evaluate_work_package_candidate_response_attempt"
    ]
    assert runtime_output_target_module.__all__ == [
        "build_work_package_output_target_payload"
    ]
    assert runtime_output_contract_module.__all__ == [
        "build_work_package_output_contract"
    ]
    assert runtime_output_mapping_module.__all__ == [
        "build_work_package_output_mapping_payload"
    ]
    assert runtime_output_acceptance_module.__all__ == [
        "validate_work_package_output_before_acceptance"
    ]
    assert runtime_output_retry_module.__all__ == [
        "evaluate_work_package_output_attempt"
    ]

    assert (
        runtime_boundary_module.build_work_package_runtime_boundary_payload
        is build_work_package_runtime_boundary_payload
    )
    assert (
        runtime_control_module.build_work_package_runtime_control_payload
        is build_work_package_runtime_control_payload
    )
    assert (
        runtime_generation_module.build_work_package_generation_request_payload
        is build_work_package_generation_request_payload
    )
    assert (
        runtime_handoff_module.build_work_package_llm_handoff_payload
        is build_work_package_llm_handoff_payload
    )
    assert (
        runtime_prompt_contract_module.build_work_package_prompt_contract_payload
        is build_work_package_prompt_contract_payload
    )
    assert (
        runtime_output_validation_module.load_candidate_response_json
        is load_candidate_response_json
    )
    assert (
        runtime_output_validation_module.validate_work_package_candidate_response
        is validate_work_package_candidate_response
    )
    assert (
        runtime_retry_fail_module.evaluate_work_package_candidate_response_attempt
        is evaluate_work_package_candidate_response_attempt
    )
    assert (
        runtime_output_target_module.build_work_package_output_target_payload
        is build_work_package_output_target_payload
    )
    assert (
        runtime_output_contract_module.build_work_package_output_contract
        is build_work_package_output_contract
    )
    assert (
        runtime_output_mapping_module.build_work_package_output_mapping_payload
        is build_work_package_output_mapping_payload
    )
    assert (
        runtime_output_acceptance_module.validate_work_package_output_before_acceptance
        is validate_work_package_output_before_acceptance
    )
    assert (
        runtime_output_retry_module.evaluate_work_package_output_attempt
        is evaluate_work_package_output_attempt
    )


def test_m11_6_runtime_contract_wrapper_exports_are_explicit_and_stable() -> None:
    assert runtime_contracts_module.__all__ == [
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

    assert runtime_contracts_module.EXPECTED_OUTPUT_FIELDS is EXPECTED_OUTPUT_FIELDS
    assert runtime_contracts_module.GENERATION_SURFACE_ID is GENERATION_SURFACE_ID
    assert runtime_contracts_module.HANDOFF_CONTRACT_ID is HANDOFF_CONTRACT_ID
    assert runtime_contracts_module.MODEL_MAY is MODEL_MAY
    assert runtime_contracts_module.MODEL_MAY_NOT is MODEL_MAY_NOT
    assert runtime_contracts_module.OUTPUT_FIELD_TYPES is OUTPUT_FIELD_TYPES
    assert runtime_contracts_module.PROMPT_CONTRACT_ID is PROMPT_CONTRACT_ID
    assert (
        runtime_contracts_module.PROHIBITED_FREEFORM_DRIFT
        is PROHIBITED_FREEFORM_DRIFT
    )
    assert runtime_contracts_module.REQUIRED_INPUT_FIELDS is REQUIRED_INPUT_FIELDS
    assert (
        runtime_contracts_module.build_candidate_response_template
        is build_candidate_response_template
    )
    assert runtime_contracts_module.build_generation_state is build_generation_state
    assert runtime_contracts_module.build_handoff_state is build_handoff_state
    assert runtime_contracts_module.build_output_contract is build_output_contract
    assert (
        runtime_contracts_module.build_prompt_contract_state_and_mode
        is build_prompt_contract_state_and_mode
    )
    assert (
        runtime_contracts_module.build_prose_generation_instructions
        is build_prose_generation_instructions
    )
    assert (
        runtime_contracts_module.build_runtime_boundary_state
        is build_runtime_boundary_state
    )


def test_m11_6_runtime_package_exports_remain_aligned_with_root_logic() -> None:
    assert (
        runtime_pkg.build_work_package_runtime_boundary_payload
        is build_work_package_runtime_boundary_payload
    )
    assert (
        runtime_pkg.build_work_package_generation_request_payload
        is build_work_package_generation_request_payload
    )
    assert (
        runtime_pkg.build_work_package_llm_handoff_payload
        is build_work_package_llm_handoff_payload
    )
    assert (
        runtime_pkg.build_work_package_prompt_contract_payload
        is build_work_package_prompt_contract_payload
    )
    assert (
        runtime_pkg.build_work_package_output_target_payload
        is build_work_package_output_target_payload
    )
    assert (
        runtime_pkg.build_work_package_output_contract
        is build_work_package_output_contract
    )
    assert (
        runtime_pkg.build_work_package_output_mapping_payload
        is build_work_package_output_mapping_payload
    )
    assert (
        runtime_pkg.validate_work_package_output_before_acceptance
        is validate_work_package_output_before_acceptance
    )
    assert (
        runtime_pkg.evaluate_work_package_output_attempt
        is evaluate_work_package_output_attempt
    )
    assert (
        runtime_pkg.validate_work_package_candidate_response
        is validate_work_package_candidate_response
    )
    assert (
        runtime_pkg.evaluate_work_package_candidate_response_attempt
        is evaluate_work_package_candidate_response_attempt
    )