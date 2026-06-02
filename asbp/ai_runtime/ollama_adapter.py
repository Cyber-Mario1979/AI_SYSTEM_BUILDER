"Bounded local Ollama adapter smoke contract for M31.10-A."

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

from asbp.ai_runtime.runtime_shakedown import (
    APPROVED_BOUNDED_RUNTIME_TARGET,
    LOCAL_RUNTIME_CANDIDATE_TARGET,
    RUNTIME_TARGET_STATUS_READY,
    SCENARIO_ADVISORY_QA,
)

M3110A_CHECKPOINT_ID = "M31.10-A"
M3110A_CONTRACT_VERSION = "bounded-ollama-adapter-smoke-v1"
M3110A_SMOKE_STATUS_READY = "bounded_ollama_adapter_smoke_ready"
M3110A_SMOKE_STATUS_CAPTURED = "bounded_ollama_adapter_smoke_evidence_captured"
M3110A_PROVIDER_KIND = "local_ollama_runtime"
M3110A_MODEL_NAME = "llama3.2:3b"
M3110A_DEFAULT_ENDPOINT = "http://localhost:11434/api/generate"
M3110A_ALLOWED_ASSISTANCE_MODE = "advisory_qa"

_REQUIRED_FALSE_FIELDS = (
    "api_key_required",
    "api_key_storage_allowed",
    "cloud_provider_call_allowed",
    "raw_provider_payload_storage_allowed",
    "raw_model_output_storage_allowed",
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

_REQUIRED_REQUEST_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "smoke_request_id",
    "provider_kind",
    "model_name",
    "endpoint_url",
    "runtime_target",
    "runtime_target_status",
    "scenario_id",
    "scenario_kind",
    "assistance_mode",
    "prompt_contract_ref",
    "context_packet_ref",
    "refusal_decision_ref",
    "output_review_ref",
    "evidence_ref",
)

_REQUIRED_EVIDENCE_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "smoke_run_id",
    "smoke_request_id",
    "provider_kind",
    "model_name",
    "endpoint_url",
    "scenario_id",
    "result_status",
    "response_summary",
    "limitation_summary",
    "output_review_state",
)

_PROHIBITED_FIELDS = (
    "api_key",
    "provider_api_key",
    "openai_api_key",
    "secret",
    "token",
    "access_token",
    "raw_prompt",
    "free_form_prompt",
    "messages",
    "system_prompt",
    "developer_prompt",
    "raw_provider_payload",
    "raw_provider_response",
    "raw_ollama_payload",
    "raw_ollama_response",
    "model_output",
    "generated_final_output",
    "state_mutation_payload",
    "approval_payload",
    "release_payload",
    "certification_payload",
    "customer_ready_output_payload",
    "commercial_launch_payload",
)

_FORBIDDEN_OUTPUT_TERMS = (
    "approved",
    "certified",
    "released",
    "release ready",
    "customer-ready",
    "customer ready",
    "compliant",
    "compliance is confirmed",
)


def build_bounded_ollama_smoke_baseline() -> dict[str, Any]:
    """Return the bounded M31.10-A Ollama smoke baseline."""
    return {
        "checkpoint": M3110A_CHECKPOINT_ID,
        "contract_version": M3110A_CONTRACT_VERSION,
        "provider_kind": M3110A_PROVIDER_KIND,
        "model_name": M3110A_MODEL_NAME,
        "default_endpoint_url": M3110A_DEFAULT_ENDPOINT,
        "allowed_endpoint_policy": "localhost_only_http_endpoint",
        "normal_pytest_requires_ollama": False,
        "api_key_required": False,
        "cloud_provider_call_allowed": False,
        "minimum_path": (
            "asbp_provider_boundary_to_local_ollama_runtime_to_predeclared_context_"
            "to_bounded_response_to_output_review_evidence"
        ),
        "next_checkpoint": "M31.11 — AI assistance UAT / owner acceptance",
    }


def build_bounded_ollama_smoke_request(
    *,
    smoke_request_id: str,
    endpoint_url: str = M3110A_DEFAULT_ENDPOINT,
    model_name: str = M3110A_MODEL_NAME,
    enable_local_runtime: bool = False,
    allow_prompt_execution: bool = False,
    scenario_id: str = "M3110A-S1-ADVISORY-DRAFT-SUPPORT",
    scenario_kind: str = SCENARIO_ADVISORY_QA,
    assistance_mode: str = M3110A_ALLOWED_ASSISTANCE_MODE,
    prompt_contract_ref: str = "PROMPT-CONTRACT-M3110A-S1@v1",
    context_packet_ref: str = "CTX-PACKET-M3110A-S1@v1",
    refusal_decision_ref: str = "REFUSAL-DECISION-M3110A-S1@v1",
    output_review_ref: str = "OUTPUT-REVIEW-M3110A-S1@v1",
    evidence_ref: str = "EVIDENCE-M3110A-S1@v1",
) -> dict[str, object]:
    """Build and validate an explicit opt-in local Ollama smoke request."""
    if enable_local_runtime and allow_prompt_execution:
        runtime_target = APPROVED_BOUNDED_RUNTIME_TARGET
        runtime_target_status = RUNTIME_TARGET_STATUS_READY
    else:
        runtime_target = LOCAL_RUNTIME_CANDIDATE_TARGET
        runtime_target_status = "runtime_blocked_until_explicit_opt_in"
    request = {
        "checkpoint": M3110A_CHECKPOINT_ID,
        "contract_version": M3110A_CONTRACT_VERSION,
        "smoke_request_id": _require_non_empty_string(
            smoke_request_id,
            field_name="smoke_request_id",
            error_prefix="Bounded Ollama smoke request",
        ),
        "provider_kind": M3110A_PROVIDER_KIND,
        "model_name": _require_expected_value(
            model_name,
            field_name="model_name",
            expected_value=M3110A_MODEL_NAME,
            error_prefix="Bounded Ollama smoke request",
        ),
        "endpoint_url": _normalize_localhost_endpoint(endpoint_url),
        "runtime_target": runtime_target,
        "runtime_target_status": runtime_target_status,
        "enable_local_runtime": bool(enable_local_runtime),
        "allow_prompt_execution": bool(allow_prompt_execution),
        "scenario_id": _require_non_empty_string(
            scenario_id,
            field_name="scenario_id",
            error_prefix="Bounded Ollama smoke request",
        ),
        "scenario_kind": _require_expected_value(
            scenario_kind,
            field_name="scenario_kind",
            expected_value=SCENARIO_ADVISORY_QA,
            error_prefix="Bounded Ollama smoke request",
        ),
        "assistance_mode": _require_expected_value(
            assistance_mode,
            field_name="assistance_mode",
            expected_value=M3110A_ALLOWED_ASSISTANCE_MODE,
            error_prefix="Bounded Ollama smoke request",
        ),
        "prompt_contract_ref": _require_non_empty_string(
            prompt_contract_ref,
            field_name="prompt_contract_ref",
            error_prefix="Bounded Ollama smoke request",
        ),
        "context_packet_ref": _require_non_empty_string(
            context_packet_ref,
            field_name="context_packet_ref",
            error_prefix="Bounded Ollama smoke request",
        ),
        "refusal_decision_ref": _require_non_empty_string(
            refusal_decision_ref,
            field_name="refusal_decision_ref",
            error_prefix="Bounded Ollama smoke request",
        ),
        "output_review_ref": _require_non_empty_string(
            output_review_ref,
            field_name="output_review_ref",
            error_prefix="Bounded Ollama smoke request",
        ),
        "evidence_ref": _require_non_empty_string(
            evidence_ref,
            field_name="evidence_ref",
            error_prefix="Bounded Ollama smoke request",
        ),
        "api_key_required": False,
        "api_key_storage_allowed": False,
        "cloud_provider_call_allowed": False,
        "raw_provider_payload_storage_allowed": False,
        "raw_model_output_storage_allowed": False,
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
    validate_bounded_ollama_smoke_request(request)
    return request


def validate_bounded_ollama_smoke_request(request: dict[str, object]) -> None:
    """Validate an M31.10-A local Ollama smoke request."""
    _validate_prohibited_fields(request)
    _validate_required_string_fields(
        request,
        _REQUIRED_REQUEST_STRING_FIELDS,
        error_prefix="Bounded Ollama smoke request",
    )
    _require_expected_value(
        request["checkpoint"],
        field_name="checkpoint",
        expected_value=M3110A_CHECKPOINT_ID,
        error_prefix="Bounded Ollama smoke request",
    )
    _require_expected_value(
        request["contract_version"],
        field_name="contract_version",
        expected_value=M3110A_CONTRACT_VERSION,
        error_prefix="Bounded Ollama smoke request",
    )
    _require_expected_value(
        request["provider_kind"],
        field_name="provider_kind",
        expected_value=M3110A_PROVIDER_KIND,
        error_prefix="Bounded Ollama smoke request",
    )
    _require_expected_value(
        request["model_name"],
        field_name="model_name",
        expected_value=M3110A_MODEL_NAME,
        error_prefix="Bounded Ollama smoke request",
    )
    _normalize_localhost_endpoint(request["endpoint_url"])
    _require_bool(
        request.get("enable_local_runtime"),
        field_name="enable_local_runtime",
        error_prefix="Bounded Ollama smoke request",
    )
    _require_bool(
        request.get("allow_prompt_execution"),
        field_name="allow_prompt_execution",
        error_prefix="Bounded Ollama smoke request",
    )
    for field_name in _REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(
                f"Bounded Ollama smoke request requires {field_name} to be False."
            )
    if request.get("enable_local_runtime") is not True:
        raise ValueError(
            "Bounded Ollama smoke request requires explicit local runtime opt-in."
        )
    if request.get("allow_prompt_execution") is not True:
        raise ValueError(
            "Bounded Ollama smoke request requires explicit prompt execution opt-in."
        )
    _require_expected_value(
        request["runtime_target"],
        field_name="runtime_target",
        expected_value=APPROVED_BOUNDED_RUNTIME_TARGET,
        error_prefix="Bounded Ollama smoke request",
    )
    _require_expected_value(
        request["runtime_target_status"],
        field_name="runtime_target_status",
        expected_value=RUNTIME_TARGET_STATUS_READY,
        error_prefix="Bounded Ollama smoke request",
    )


def build_ollama_generate_payload(request: dict[str, object]) -> dict[str, object]:
    """Build the bounded local Ollama generate payload without storing secrets."""
    validate_bounded_ollama_smoke_request(request)
    prompt = (
        "M31.10-A bounded app-coupled Ollama adapter smoke.\n\n"
        "Use only the bounded scenario and context references below.\n"
        "Output must be draft support only and must mention limitations.\n"
        "Do not claim approval, certification, release readiness, compliance, "
        "customer readiness, or final authority.\n\n"
        f"Scenario ID: {request['scenario_id']}\n"
        f"Prompt contract ref: {request['prompt_contract_ref']}\n"
        f"Context packet ref: {request['context_packet_ref']}\n"
        f"Refusal decision ref: {request['refusal_decision_ref']}\n"
        f"Output review ref: {request['output_review_ref']}\n\n"
        "Governed context summary:\n"
        "- Project type: HVAC qualification.\n"
        "- Current task: prepare Installation Qualification checklist draft support.\n"
        "- Source limitation: simplified demonstration evidence only.\n"
        "- Allowed use: advisory drafting support only.\n"
        "- Blocked use: approval, certification, release, compliance, or customer-ready claims.\n\n"
        "Question: Suggest three draft IQ checklist items based only on this bounded context."
    )
    return {
        "model": request["model_name"],
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m",
    }


def execute_bounded_ollama_smoke(
    request: dict[str, object],
    *,
    post_json: Callable[[str, dict[str, object]], dict[str, object]],
) -> dict[str, object]:
    """Execute an explicitly opted-in local Ollama smoke through an injected caller.

    The injected callable keeps normal tests independent from Ollama, networking,
    local models, GPUs, or a running service.
    """
    validate_bounded_ollama_smoke_request(request)
    payload = build_ollama_generate_payload(request)
    response = post_json(str(request["endpoint_url"]), payload)
    return build_bounded_ollama_smoke_evidence(
        smoke_run_id=f"{request['smoke_request_id']}-RUN",
        request=request,
        response=response,
    )


def build_bounded_ollama_smoke_evidence(
    *,
    smoke_run_id: str,
    request: dict[str, object],
    response: dict[str, object],
) -> dict[str, object]:
    """Build bounded evidence from a local Ollama smoke response."""
    validate_bounded_ollama_smoke_request(request)
    _validate_prohibited_fields(response)
    response_text = _require_non_empty_string(
        response.get("response"),
        field_name="response",
        error_prefix="Bounded Ollama smoke response",
    )
    forbidden_terms = _detect_forbidden_terms(response_text)
    evidence = {
        "checkpoint": M3110A_CHECKPOINT_ID,
        "contract_version": M3110A_CONTRACT_VERSION,
        "smoke_run_id": _require_non_empty_string(
            smoke_run_id,
            field_name="smoke_run_id",
            error_prefix="Bounded Ollama smoke evidence",
        ),
        "smoke_request_id": str(request["smoke_request_id"]),
        "provider_kind": M3110A_PROVIDER_KIND,
        "model_name": str(request["model_name"]),
        "endpoint_url": str(request["endpoint_url"]),
        "scenario_id": str(request["scenario_id"]),
        "result_status": (
            "fail_closed_for_forbidden_claims"
            if forbidden_terms
            else M3110A_SMOKE_STATUS_CAPTURED
        ),
        "response_summary": _summarize_response(response_text),
        "limitation_summary": (
            "response_contains_forbidden_terms: " + ", ".join(forbidden_terms)
            if forbidden_terms
            else "bounded_draft_support_response_captured_without_forbidden_claim_terms"
        ),
        "output_review_state": (
            "requires_correction_before_acceptance"
            if forbidden_terms
            else "human_review_required_before_use"
        ),
        "forbidden_terms_detected": forbidden_terms,
        "api_key_required": False,
        "api_key_storage_allowed": False,
        "cloud_provider_call_allowed": False,
        "raw_provider_payload_storage_allowed": False,
        "raw_model_output_storage_allowed": False,
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
    validate_bounded_ollama_smoke_evidence(evidence)
    return evidence


def validate_bounded_ollama_smoke_evidence(evidence: dict[str, object]) -> None:
    """Validate bounded evidence from an app-coupled Ollama smoke."""
    _validate_prohibited_fields(evidence)
    _validate_required_string_fields(
        evidence,
        _REQUIRED_EVIDENCE_STRING_FIELDS,
        error_prefix="Bounded Ollama smoke evidence",
    )
    _require_expected_value(
        evidence["checkpoint"],
        field_name="checkpoint",
        expected_value=M3110A_CHECKPOINT_ID,
        error_prefix="Bounded Ollama smoke evidence",
    )
    _require_expected_value(
        evidence["contract_version"],
        field_name="contract_version",
        expected_value=M3110A_CONTRACT_VERSION,
        error_prefix="Bounded Ollama smoke evidence",
    )
    _require_expected_value(
        evidence["provider_kind"],
        field_name="provider_kind",
        expected_value=M3110A_PROVIDER_KIND,
        error_prefix="Bounded Ollama smoke evidence",
    )
    _require_expected_value(
        evidence["model_name"],
        field_name="model_name",
        expected_value=M3110A_MODEL_NAME,
        error_prefix="Bounded Ollama smoke evidence",
    )
    _normalize_localhost_endpoint(evidence["endpoint_url"])
    for field_name in _REQUIRED_FALSE_FIELDS:
        if evidence.get(field_name) is not False:
            raise ValueError(
                f"Bounded Ollama smoke evidence requires {field_name} to be False."
            )
    forbidden_terms = evidence.get("forbidden_terms_detected")
    if not isinstance(forbidden_terms, list):
        raise ValueError("Bounded Ollama smoke evidence requires forbidden terms list.")
    result_status = _require_non_empty_string(
        evidence["result_status"],
        field_name="result_status",
        error_prefix="Bounded Ollama smoke evidence",
    )
    if forbidden_terms and result_status != "fail_closed_for_forbidden_claims":
        raise ValueError("Forbidden claims require fail-closed result status.")
    if not forbidden_terms and result_status != M3110A_SMOKE_STATUS_CAPTURED:
        raise ValueError("Clean smoke evidence requires captured result status.")


def _normalize_localhost_endpoint(value: object) -> str:
    endpoint = _require_non_empty_string(
        value,
        field_name="endpoint_url",
        error_prefix="Bounded Ollama smoke endpoint",
    )
    parsed = urlparse(endpoint)
    if parsed.scheme != "http":
        raise ValueError("Bounded Ollama smoke endpoint must use http localhost only.")
    if parsed.hostname not in {"localhost", "127.0.0.1"}:
        raise ValueError("Bounded Ollama smoke endpoint must target localhost only.")
    if parsed.port not in {11434, None}:
        raise ValueError("Bounded Ollama smoke endpoint must use the Ollama local port.")
    if parsed.path != "/api/generate":
        raise ValueError("Bounded Ollama smoke endpoint must target /api/generate.")
    return endpoint


def _detect_forbidden_terms(response_text: str) -> list[str]:
    lowered = response_text.lower()
    return [term for term in _FORBIDDEN_OUTPUT_TERMS if term in lowered]


def _summarize_response(response_text: str, *, max_length: int = 240) -> str:
    normalized = " ".join(response_text.split())
    if len(normalized) <= max_length:
        return normalized
    return normalized[: max_length - 3].rstrip() + "..."


def _require_expected_value(
    value: object,
    *,
    field_name: str,
    expected_value: str,
    error_prefix: str,
) -> str:
    normalized = _require_non_empty_string(
        value,
        field_name=field_name,
        error_prefix=error_prefix,
    )
    if normalized != expected_value:
        raise ValueError(
            f"{error_prefix} declares invalid {field_name}: "
            f"expected {expected_value!r}, got {normalized!r}."
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


def _validate_prohibited_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_FIELDS:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in M31.10-A Ollama smoke payloads."
            )
