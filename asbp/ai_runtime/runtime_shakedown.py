"Bounded local/provider runtime shakedown protocol for M31.8."

from __future__ import annotations

from typing import Any

from asbp.ai_runtime.evaluation_harness import (
    AI_EVALUATION_HARNESS_STATUS_VALIDATED,
    AI_PROVIDER_SMOKE_STATUS_BLOCKED,
    AI_PROVIDER_SMOKE_STATUS_READY,
    AI_PROVIDER_SMOKE_STATUS_SKIPPED,
    validate_ai_evaluation_regression_result,
    validate_ai_provider_smoke_request,
)

AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID = "M31.8"
AI_RUNTIME_SHAKEDOWN_CONTRACT_VERSION = "ai-runtime-shakedown-protocol-v1"
AI_RUNTIME_SHAKEDOWN_STATUS_VALIDATED = "ai_runtime_shakedown_protocol_validated"

DISABLED_RUNTIME_TARGET = "disabled_runtime"
LOCAL_RUNTIME_CANDIDATE_TARGET = "local_runtime_candidate"
PROVIDER_RUNTIME_CANDIDATE_TARGET = "provider_runtime_candidate"
APPROVED_BOUNDED_RUNTIME_TARGET = "approved_bounded_runtime"
SUPPORTED_RUNTIME_TARGETS = (
    DISABLED_RUNTIME_TARGET,
    LOCAL_RUNTIME_CANDIDATE_TARGET,
    PROVIDER_RUNTIME_CANDIDATE_TARGET,
    APPROVED_BOUNDED_RUNTIME_TARGET,
)

RUNTIME_TARGET_STATUS_DISABLED = "runtime_disabled"
RUNTIME_TARGET_STATUS_SKIPPED = "runtime_skipped_prompt_execution_blocked"
RUNTIME_TARGET_STATUS_READY = "runtime_ready_for_bounded_shakedown"
SUPPORTED_RUNTIME_TARGET_STATUSES = (
    RUNTIME_TARGET_STATUS_DISABLED,
    RUNTIME_TARGET_STATUS_SKIPPED,
    RUNTIME_TARGET_STATUS_READY,
)

SCENARIO_ADVISORY_QA = "advisory_qa_governed_context"
SCENARIO_RETRIEVAL_LIMITED = "retrieval_supported_limited_answer"
SCENARIO_MISSING_SOURCE_REFUSAL = "missing_source_refusal"
SCENARIO_DRAFT_OUTPUT_SUPPORT = "draft_output_support"
SCENARIO_HUMAN_REVIEW_REQUIRED = "human_review_required_output"
SUPPORTED_SHAKEDOWN_SCENARIO_KINDS = (
    SCENARIO_ADVISORY_QA,
    SCENARIO_RETRIEVAL_LIMITED,
    SCENARIO_MISSING_SOURCE_REFUSAL,
    SCENARIO_DRAFT_OUTPUT_SUPPORT,
    SCENARIO_HUMAN_REVIEW_REQUIRED,
)

STOP_NONE_EXPECTED = "no_stop_expected"
STOP_UNDECLARED_SCENARIO = "undeclared_scenario"
STOP_MISSING_PROMPT_CONTRACT = "missing_prompt_contract"
STOP_MISSING_CONTEXT_PACKET = "missing_context_packet"
STOP_MISSING_REFUSAL_DECISION = "missing_refusal_decision"
STOP_MISSING_OUTPUT_REVIEW = "missing_output_review"
STOP_RUNTIME_NOT_EXPLICITLY_ENABLED = "runtime_not_explicitly_enabled"
STOP_RAW_RETRIEVAL_TRUTH_ATTEMPT = "raw_retrieval_truth_attempt"
STOP_AUTHORITY_CLAIM_ATTEMPT = "approval_release_certification_claim_attempt"
STOP_STATE_MUTATION_ATTEMPT = "state_mutation_attempt"
STOP_RUNTIME_ERROR = "runtime_error"
SUPPORTED_STOP_CONDITIONS = (
    STOP_NONE_EXPECTED,
    STOP_UNDECLARED_SCENARIO,
    STOP_MISSING_PROMPT_CONTRACT,
    STOP_MISSING_CONTEXT_PACKET,
    STOP_MISSING_REFUSAL_DECISION,
    STOP_MISSING_OUTPUT_REVIEW,
    STOP_RUNTIME_NOT_EXPLICITLY_ENABLED,
    STOP_RAW_RETRIEVAL_TRUTH_ATTEMPT,
    STOP_AUTHORITY_CLAIM_ATTEMPT,
    STOP_STATE_MUTATION_ATTEMPT,
    STOP_RUNTIME_ERROR,
)

SHAKEDOWN_RESULT_NOT_RUN = "not_run"
SHAKEDOWN_RESULT_READY = "ready_for_bounded_shakedown"
SHAKEDOWN_RESULT_FAIL_CLOSED = "fail_closed"
SHAKEDOWN_RESULT_EVIDENCE_CAPTURED = "evidence_captured"
SUPPORTED_SHAKEDOWN_RESULT_STATUSES = (
    SHAKEDOWN_RESULT_NOT_RUN,
    SHAKEDOWN_RESULT_READY,
    SHAKEDOWN_RESULT_FAIL_CLOSED,
    SHAKEDOWN_RESULT_EVIDENCE_CAPTURED,
)

_REQUIRED_RUNTIME_TARGET_STRING_FIELDS = (
    "runtime_target_id",
    "runtime_target",
    "runtime_target_status",
)

_REQUIRED_SCENARIO_STRING_FIELDS = (
    "scenario_id",
    "scenario_kind",
    "assistance_mode",
    "runtime_target",
    "prompt_contract_ref",
    "context_packet_ref",
    "expected_refusal_decision",
    "expected_output_state",
    "expected_stop_condition",
)

_REQUIRED_PROTOCOL_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "protocol_id",
    "runtime_shakedown_status",
    "evaluation_result_id",
    "evaluation_status",
    "runtime_target_id",
    "runtime_target",
    "runtime_target_status",
)

_REQUIRED_EVIDENCE_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "shakedown_run_id",
    "protocol_id",
    "scenario_id",
    "runtime_target",
    "runtime_target_status",
    "result_status",
    "stop_condition",
    "evaluation_result_id",
)

_REQUIRED_FALSE_FIELDS = (
    "api_key_required",
    "api_key_storage_allowed",
    "raw_provider_call_allowed",
    "unbounded_prompt_execution_allowed",
    "autonomous_agentic_execution_allowed",
    "model_owned_state_mutation_allowed",
    "ai_approval_authority_allowed",
    "ai_release_certification_authority_allowed",
    "retrieval_as_source_truth_allowed",
    "ui_api_behavior_enabled",
    "productization_claim_allowed",
    "customer_ready_output_claim_allowed",
    "commercialization_launch_planning_allowed",
)

_PROHIBITED_SHAKEDOWN_FIELDS = (
    "api_key",
    "provider_api_key",
    "openai_api_key",
    "raw_prompt",
    "free_form_prompt",
    "untracked_fact",
    "untracked_facts",
    "raw_retrieval_dump",
    "raw_retrieval_chunks",
    "messages",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "provider_sdk_client",
    "raw_provider_payload",
    "raw_provider_response",
    "model_output",
    "generated_final_output",
    "state_mutation_payload",
    "approval_payload",
    "release_payload",
    "certification_payload",
    "customer_ready_output_payload",
    "commercial_launch_payload",
)


def build_ai_runtime_shakedown_baseline() -> dict[str, Any]:
    """Return the M31.8 runtime shakedown protocol baseline."""
    return {
        "checkpoint": AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID,
        "contract_version": AI_RUNTIME_SHAKEDOWN_CONTRACT_VERSION,
        "runtime_shakedown_status": AI_RUNTIME_SHAKEDOWN_STATUS_VALIDATED,
        "supported_runtime_targets": list(SUPPORTED_RUNTIME_TARGETS),
        "supported_scenario_kinds": list(SUPPORTED_SHAKEDOWN_SCENARIO_KINDS),
        "supported_stop_conditions": list(SUPPORTED_STOP_CONDITIONS),
        "default_runtime_target": DISABLED_RUNTIME_TARGET,
        "api_key_required_by_default": False,
        "api_key_policy": "no_api_key_required_or_stored_for_m31_8_protocol_scaffold",
        "execution_policy": (
            "bounded_runtime_shakedown_requires_predeclared_scenario_prompt_contract_"
            "context_packet_refusal_output_review_and_evaluation_evidence"
        ),
        "next_checkpoint": "M31.9 — Real internal human AI-use shakedown / owner observation",
    }


def build_ai_runtime_target_descriptor(
    *,
    runtime_target_id: str,
    runtime_target: str = DISABLED_RUNTIME_TARGET,
    enable_runtime: bool = False,
    allow_prompt_execution: bool = False,
) -> dict[str, object]:
    """Build and validate a bounded M31.8 runtime target descriptor."""
    runtime_target = _normalize_supported_value(
        runtime_target,
        field_name="runtime_target",
        supported_values=SUPPORTED_RUNTIME_TARGETS,
        error_prefix="AI runtime target descriptor",
    )
    runtime_target_status = RUNTIME_TARGET_STATUS_DISABLED
    if enable_runtime and allow_prompt_execution:
        runtime_target_status = RUNTIME_TARGET_STATUS_READY
    elif enable_runtime:
        runtime_target_status = RUNTIME_TARGET_STATUS_SKIPPED
    descriptor = {
        "runtime_target_id": _require_non_empty_string(
            runtime_target_id,
            field_name="runtime_target_id",
            error_prefix="AI runtime target descriptor",
        ),
        "runtime_target": runtime_target,
        "runtime_target_status": runtime_target_status,
        "enable_runtime": bool(enable_runtime),
        "allow_prompt_execution": bool(allow_prompt_execution),
        "api_key_required": False,
        "api_key_storage_allowed": False,
        "raw_provider_call_allowed": False,
        "unbounded_prompt_execution_allowed": False,
        "autonomous_agentic_execution_allowed": False,
        "model_owned_state_mutation_allowed": False,
        "ai_approval_authority_allowed": False,
        "ai_release_certification_authority_allowed": False,
        "retrieval_as_source_truth_allowed": False,
        "ui_api_behavior_enabled": False,
        "productization_claim_allowed": False,
        "customer_ready_output_claim_allowed": False,
        "commercialization_launch_planning_allowed": False,
    }
    validate_ai_runtime_target_descriptor(descriptor)
    return descriptor


def validate_ai_runtime_target_descriptor(descriptor: dict[str, object]) -> None:
    """Validate a bounded M31.8 runtime target descriptor."""
    _validate_prohibited_fields(descriptor, _PROHIBITED_SHAKEDOWN_FIELDS)
    _validate_required_string_fields(
        descriptor,
        _REQUIRED_RUNTIME_TARGET_STRING_FIELDS,
        error_prefix="AI runtime target descriptor",
    )
    runtime_target = _normalize_supported_value(
        descriptor["runtime_target"],
        field_name="runtime_target",
        supported_values=SUPPORTED_RUNTIME_TARGETS,
        error_prefix="AI runtime target descriptor",
    )
    runtime_target_status = _normalize_supported_value(
        descriptor["runtime_target_status"],
        field_name="runtime_target_status",
        supported_values=SUPPORTED_RUNTIME_TARGET_STATUSES,
        error_prefix="AI runtime target descriptor",
    )
    enable_runtime = _require_bool(
        descriptor.get("enable_runtime"),
        field_name="enable_runtime",
        error_prefix="AI runtime target descriptor",
    )
    allow_prompt_execution = _require_bool(
        descriptor.get("allow_prompt_execution"),
        field_name="allow_prompt_execution",
        error_prefix="AI runtime target descriptor",
    )
    for field_name in _REQUIRED_FALSE_FIELDS:
        if descriptor.get(field_name) is not False:
            raise ValueError(
                "AI runtime target descriptor requires " f"{field_name} to be False."
            )
    if not enable_runtime:
        if runtime_target != DISABLED_RUNTIME_TARGET:
            raise ValueError("Disabled runtime requires disabled_runtime target.")
        if runtime_target_status != RUNTIME_TARGET_STATUS_DISABLED:
            raise ValueError("Disabled runtime requires runtime_disabled status.")
    if enable_runtime and not allow_prompt_execution:
        if runtime_target_status != RUNTIME_TARGET_STATUS_SKIPPED:
            raise ValueError(
                "Runtime target must skip when prompt execution is not explicitly allowed."
            )
    if enable_runtime and allow_prompt_execution:
        if runtime_target != APPROVED_BOUNDED_RUNTIME_TARGET:
            raise ValueError(
                "Prompt execution opt-in requires approved_bounded_runtime target."
            )
        if runtime_target_status != RUNTIME_TARGET_STATUS_READY:
            raise ValueError(
                "Approved bounded runtime target requires ready shakedown status."
            )


def build_ai_runtime_shakedown_scenario(
    *,
    scenario_id: str,
    scenario_kind: str,
    assistance_mode: str,
    runtime_target: str,
    prompt_contract_ref: str,
    context_packet_ref: str,
    expected_refusal_decision: str,
    expected_output_state: str,
    expected_stop_condition: str = STOP_NONE_EXPECTED,
    evidence_capture_required: bool = True,
    human_observation_deferred_to_m31_9: bool = True,
) -> dict[str, object]:
    """Build and validate a predeclared M31.8 shakedown scenario."""
    scenario = {
        "scenario_id": _require_non_empty_string(
            scenario_id,
            field_name="scenario_id",
            error_prefix="AI runtime shakedown scenario",
        ),
        "scenario_kind": _normalize_supported_value(
            scenario_kind,
            field_name="scenario_kind",
            supported_values=SUPPORTED_SHAKEDOWN_SCENARIO_KINDS,
            error_prefix="AI runtime shakedown scenario",
        ),
        "assistance_mode": _require_non_empty_string(
            assistance_mode,
            field_name="assistance_mode",
            error_prefix="AI runtime shakedown scenario",
        ),
        "runtime_target": _normalize_supported_value(
            runtime_target,
            field_name="runtime_target",
            supported_values=SUPPORTED_RUNTIME_TARGETS,
            error_prefix="AI runtime shakedown scenario",
        ),
        "prompt_contract_ref": _require_non_empty_string(
            prompt_contract_ref,
            field_name="prompt_contract_ref",
            error_prefix="AI runtime shakedown scenario",
        ),
        "context_packet_ref": _require_non_empty_string(
            context_packet_ref,
            field_name="context_packet_ref",
            error_prefix="AI runtime shakedown scenario",
        ),
        "expected_refusal_decision": _require_non_empty_string(
            expected_refusal_decision,
            field_name="expected_refusal_decision",
            error_prefix="AI runtime shakedown scenario",
        ),
        "expected_output_state": _require_non_empty_string(
            expected_output_state,
            field_name="expected_output_state",
            error_prefix="AI runtime shakedown scenario",
        ),
        "expected_stop_condition": _normalize_supported_value(
            expected_stop_condition,
            field_name="expected_stop_condition",
            supported_values=SUPPORTED_STOP_CONDITIONS,
            error_prefix="AI runtime shakedown scenario",
        ),
        "evidence_capture_required": bool(evidence_capture_required),
        "human_observation_deferred_to_m31_9": bool(human_observation_deferred_to_m31_9),
    }
    validate_ai_runtime_shakedown_scenario(scenario)
    return scenario


def validate_ai_runtime_shakedown_scenario(scenario: dict[str, object]) -> None:
    """Validate a predeclared M31.8 shakedown scenario."""
    _validate_prohibited_fields(scenario, _PROHIBITED_SHAKEDOWN_FIELDS)
    _validate_required_string_fields(
        scenario,
        _REQUIRED_SCENARIO_STRING_FIELDS,
        error_prefix="AI runtime shakedown scenario",
    )
    _normalize_supported_value(
        scenario["scenario_kind"],
        field_name="scenario_kind",
        supported_values=SUPPORTED_SHAKEDOWN_SCENARIO_KINDS,
        error_prefix="AI runtime shakedown scenario",
    )
    _normalize_supported_value(
        scenario["runtime_target"],
        field_name="runtime_target",
        supported_values=SUPPORTED_RUNTIME_TARGETS,
        error_prefix="AI runtime shakedown scenario",
    )
    _normalize_supported_value(
        scenario["expected_stop_condition"],
        field_name="expected_stop_condition",
        supported_values=SUPPORTED_STOP_CONDITIONS,
        error_prefix="AI runtime shakedown scenario",
    )
    _require_bool(
        scenario.get("evidence_capture_required"),
        field_name="evidence_capture_required",
        error_prefix="AI runtime shakedown scenario",
    )
    _require_bool(
        scenario.get("human_observation_deferred_to_m31_9"),
        field_name="human_observation_deferred_to_m31_9",
        error_prefix="AI runtime shakedown scenario",
    )
    if scenario.get("evidence_capture_required") is not True:
        raise ValueError("M31.8 scenarios must require evidence capture.")
    if scenario.get("human_observation_deferred_to_m31_9") is not True:
        raise ValueError("M31.8 scenarios must defer human observation completion to M31.9.")


def build_ai_runtime_shakedown_protocol(
    *,
    protocol_id: str,
    evaluation_result: dict[str, object],
    runtime_target_descriptor: dict[str, object],
    scenarios: list[dict[str, object]],
    provider_smoke_request: dict[str, object] | None = None,
) -> dict[str, object]:
    """Build and validate an M31.8 bounded runtime shakedown protocol."""
    validate_ai_evaluation_regression_result(evaluation_result)
    validate_ai_runtime_target_descriptor(runtime_target_descriptor)
    if provider_smoke_request is not None:
        validate_ai_provider_smoke_request(provider_smoke_request)
    protocol = {
        "checkpoint": AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID,
        "contract_version": AI_RUNTIME_SHAKEDOWN_CONTRACT_VERSION,
        "protocol_id": _require_non_empty_string(
            protocol_id,
            field_name="protocol_id",
            error_prefix="AI runtime shakedown protocol",
        ),
        "runtime_shakedown_status": AI_RUNTIME_SHAKEDOWN_STATUS_VALIDATED,
        "evaluation_result_id": str(evaluation_result["evaluation_result_id"]),
        "evaluation_status": str(evaluation_result["evaluation_status"]),
        "provider_smoke_status": str(evaluation_result["provider_smoke_status"]),
        "runtime_target_id": str(runtime_target_descriptor["runtime_target_id"]),
        "runtime_target": str(runtime_target_descriptor["runtime_target"]),
        "runtime_target_status": str(runtime_target_descriptor["runtime_target_status"]),
        "scenarios": list(scenarios),
        "provider_smoke_request": (
            dict(provider_smoke_request) if provider_smoke_request is not None else None
        ),
        "api_key_required": False,
        "api_key_storage_allowed": False,
        "raw_provider_call_allowed": False,
        "unbounded_prompt_execution_allowed": False,
        "autonomous_agentic_execution_allowed": False,
        "model_owned_state_mutation_allowed": False,
        "ai_approval_authority_allowed": False,
        "ai_release_certification_authority_allowed": False,
        "retrieval_as_source_truth_allowed": False,
        "ui_api_behavior_enabled": False,
        "productization_claim_allowed": False,
        "customer_ready_output_claim_allowed": False,
        "commercialization_launch_planning_allowed": False,
        "stop_policy": "missing_or_unapproved_runtime_context_output_or_evidence_fails_closed",
        "next_checkpoint": "M31.9 — Real internal human AI-use shakedown / owner observation",
    }
    validate_ai_runtime_shakedown_protocol(protocol)
    return protocol


def validate_ai_runtime_shakedown_protocol(protocol: dict[str, object]) -> None:
    """Validate an M31.8 bounded runtime shakedown protocol."""
    _validate_prohibited_fields(protocol, _PROHIBITED_SHAKEDOWN_FIELDS)
    _validate_required_string_fields(
        protocol,
        _REQUIRED_PROTOCOL_STRING_FIELDS,
        error_prefix="AI runtime shakedown protocol",
    )
    _validate_expected_exact_value(
        protocol,
        field_name="checkpoint",
        expected_value=AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID,
        error_prefix="AI runtime shakedown protocol",
    )
    _validate_expected_exact_value(
        protocol,
        field_name="contract_version",
        expected_value=AI_RUNTIME_SHAKEDOWN_CONTRACT_VERSION,
        error_prefix="AI runtime shakedown protocol",
    )
    _validate_expected_exact_value(
        protocol,
        field_name="runtime_shakedown_status",
        expected_value=AI_RUNTIME_SHAKEDOWN_STATUS_VALIDATED,
        error_prefix="AI runtime shakedown protocol",
    )
    _validate_expected_exact_value(
        protocol,
        field_name="evaluation_status",
        expected_value=AI_EVALUATION_HARNESS_STATUS_VALIDATED,
        error_prefix="AI runtime shakedown protocol",
    )
    _normalize_supported_value(
        protocol["runtime_target"],
        field_name="runtime_target",
        supported_values=SUPPORTED_RUNTIME_TARGETS,
        error_prefix="AI runtime shakedown protocol",
    )
    _normalize_supported_value(
        protocol["runtime_target_status"],
        field_name="runtime_target_status",
        supported_values=SUPPORTED_RUNTIME_TARGET_STATUSES,
        error_prefix="AI runtime shakedown protocol",
    )
    _normalize_supported_value(
        protocol.get("provider_smoke_status"),
        field_name="provider_smoke_status",
        supported_values=(
            AI_PROVIDER_SMOKE_STATUS_BLOCKED,
            AI_PROVIDER_SMOKE_STATUS_SKIPPED,
            AI_PROVIDER_SMOKE_STATUS_READY,
        ),
        error_prefix="AI runtime shakedown protocol",
    )
    for field_name in _REQUIRED_FALSE_FIELDS:
        if protocol.get(field_name) is not False:
            raise ValueError(
                "AI runtime shakedown protocol requires " f"{field_name} to be False."
            )
    scenarios = protocol.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("AI runtime shakedown protocol must declare scenarios.")
    scenario_ids: list[str] = []
    scenario_kinds: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            raise ValueError("AI runtime shakedown protocol scenarios must be dicts.")
        validate_ai_runtime_shakedown_scenario(scenario)
        scenario_ids.append(str(scenario["scenario_id"]))
        scenario_kinds.add(str(scenario["scenario_kind"]))
    _reject_duplicates(scenario_ids, field_name="scenario_id")
    required_scenarios = set(SUPPORTED_SHAKEDOWN_SCENARIO_KINDS)
    missing = sorted(required_scenarios - scenario_kinds)
    if missing:
        raise ValueError(
            "AI runtime shakedown protocol is missing required scenario kinds: "
            + ", ".join(missing)
        )
    provider_smoke_request = protocol.get("provider_smoke_request")
    if provider_smoke_request is not None:
        if not isinstance(provider_smoke_request, dict):
            raise ValueError("provider_smoke_request must be a dict when present.")
        validate_ai_provider_smoke_request(provider_smoke_request)


def build_ai_runtime_shakedown_evidence(
    *,
    shakedown_run_id: str,
    protocol: dict[str, object],
    scenario_id: str,
    result_status: str,
    stop_condition: str,
    failure_reason: str = "none",
) -> dict[str, object]:
    """Build and validate one bounded M31.8 shakedown evidence record."""
    validate_ai_runtime_shakedown_protocol(protocol)
    selected_scenario = _select_scenario(protocol, scenario_id=scenario_id)
    result_status = _normalize_supported_value(
        result_status,
        field_name="result_status",
        supported_values=SUPPORTED_SHAKEDOWN_RESULT_STATUSES,
        error_prefix="AI runtime shakedown evidence",
    )
    stop_condition = _normalize_supported_value(
        stop_condition,
        field_name="stop_condition",
        supported_values=SUPPORTED_STOP_CONDITIONS,
        error_prefix="AI runtime shakedown evidence",
    )
    evidence = {
        "checkpoint": AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID,
        "contract_version": AI_RUNTIME_SHAKEDOWN_CONTRACT_VERSION,
        "shakedown_run_id": _require_non_empty_string(
            shakedown_run_id,
            field_name="shakedown_run_id",
            error_prefix="AI runtime shakedown evidence",
        ),
        "protocol_id": str(protocol["protocol_id"]),
        "scenario_id": str(selected_scenario["scenario_id"]),
        "scenario_kind": str(selected_scenario["scenario_kind"]),
        "runtime_target": str(protocol["runtime_target"]),
        "runtime_target_status": str(protocol["runtime_target_status"]),
        "result_status": result_status,
        "stop_condition": stop_condition,
        "failure_reason": _require_non_empty_string(
            failure_reason,
            field_name="failure_reason",
            error_prefix="AI runtime shakedown evidence",
        ),
        "evaluation_result_id": str(protocol["evaluation_result_id"]),
        "prompt_contract_ref": str(selected_scenario["prompt_contract_ref"]),
        "context_packet_ref": str(selected_scenario["context_packet_ref"]),
        "human_observation_completed": False,
        "api_key_required": False,
        "api_key_storage_allowed": False,
        "raw_provider_call_allowed": False,
        "unbounded_prompt_execution_allowed": False,
        "autonomous_agentic_execution_allowed": False,
        "model_owned_state_mutation_allowed": False,
        "ai_approval_authority_allowed": False,
        "ai_release_certification_authority_allowed": False,
        "retrieval_as_source_truth_allowed": False,
        "ui_api_behavior_enabled": False,
        "productization_claim_allowed": False,
        "customer_ready_output_claim_allowed": False,
        "commercialization_launch_planning_allowed": False,
    }
    validate_ai_runtime_shakedown_evidence(evidence)
    return evidence


def validate_ai_runtime_shakedown_evidence(evidence: dict[str, object]) -> None:
    """Validate one bounded M31.8 shakedown evidence record."""
    _validate_prohibited_fields(evidence, _PROHIBITED_SHAKEDOWN_FIELDS)
    _validate_required_string_fields(
        evidence,
        _REQUIRED_EVIDENCE_STRING_FIELDS,
        error_prefix="AI runtime shakedown evidence",
    )
    _validate_expected_exact_value(
        evidence,
        field_name="checkpoint",
        expected_value=AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID,
        error_prefix="AI runtime shakedown evidence",
    )
    _validate_expected_exact_value(
        evidence,
        field_name="contract_version",
        expected_value=AI_RUNTIME_SHAKEDOWN_CONTRACT_VERSION,
        error_prefix="AI runtime shakedown evidence",
    )
    _normalize_supported_value(
        evidence["runtime_target"],
        field_name="runtime_target",
        supported_values=SUPPORTED_RUNTIME_TARGETS,
        error_prefix="AI runtime shakedown evidence",
    )
    _normalize_supported_value(
        evidence["runtime_target_status"],
        field_name="runtime_target_status",
        supported_values=SUPPORTED_RUNTIME_TARGET_STATUSES,
        error_prefix="AI runtime shakedown evidence",
    )
    result_status = _normalize_supported_value(
        evidence["result_status"],
        field_name="result_status",
        supported_values=SUPPORTED_SHAKEDOWN_RESULT_STATUSES,
        error_prefix="AI runtime shakedown evidence",
    )
    stop_condition = _normalize_supported_value(
        evidence["stop_condition"],
        field_name="stop_condition",
        supported_values=SUPPORTED_STOP_CONDITIONS,
        error_prefix="AI runtime shakedown evidence",
    )
    for field_name in _REQUIRED_FALSE_FIELDS:
        if evidence.get(field_name) is not False:
            raise ValueError(
                "AI runtime shakedown evidence requires " f"{field_name} to be False."
            )
    if evidence.get("human_observation_completed") is not False:
        raise ValueError("M31.8 evidence must not claim completed M31.9 human observation.")
    if result_status == SHAKEDOWN_RESULT_FAIL_CLOSED and stop_condition == STOP_NONE_EXPECTED:
        raise ValueError("Fail-closed evidence requires a concrete stop condition.")
    if result_status in (SHAKEDOWN_RESULT_READY, SHAKEDOWN_RESULT_EVIDENCE_CAPTURED):
        if stop_condition != STOP_NONE_EXPECTED:
            raise ValueError("Ready/captured shakedown evidence requires no stop condition.")


def _select_scenario(
    protocol: dict[str, object],
    *,
    scenario_id: str,
) -> dict[str, object]:
    requested = _require_non_empty_string(
        scenario_id,
        field_name="scenario_id",
        error_prefix="AI runtime shakedown evidence",
    )
    scenarios = protocol.get("scenarios")
    if not isinstance(scenarios, list):
        raise ValueError("AI runtime shakedown protocol must declare scenarios.")
    for scenario in scenarios:
        if isinstance(scenario, dict) and scenario.get("scenario_id") == requested:
            return scenario
    raise ValueError(f"Undeclared M31.8 shakedown scenario: {requested!r}.")


def _normalize_supported_value(
    value: object,
    *,
    field_name: str,
    supported_values: tuple[str, ...],
    error_prefix: str,
) -> str:
    normalized = _require_non_empty_string(
        value,
        field_name=field_name,
        error_prefix=error_prefix,
    )
    if normalized not in supported_values:
        raise ValueError(
            f"{error_prefix} declares unsupported {field_name}. "
            f"Expected one of: {', '.join(supported_values)}."
        )
    return normalized


def _require_bool(value: object, *, field_name: str, error_prefix: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{error_prefix} must declare boolean {field_name}.")
    return value


def _require_non_empty_string(
    value: object,
    *,
    field_name: str,
    error_prefix: str,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        _require_non_empty_string(
            payload.get(field_name),
            field_name=field_name,
            error_prefix=error_prefix,
        )


def _validate_expected_exact_value(
    payload: dict[str, object],
    *,
    field_name: str,
    expected_value: str,
    error_prefix: str,
) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: "
            f"expected {expected_value!r}, got {actual_value!r}."
        )


def _validate_prohibited_fields(
    payload: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in M31.8 runtime shakedown payloads."
            )


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate value in {field_name}: {value!r}.")
        seen.add(value)
