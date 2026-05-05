"AI runtime entry boundary for governed document/reporting jobs."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

AI_RUNTIME_BOUNDARY_CHECKPOINT_ID = "M16.1"
AI_RUNTIME_BOUNDARY_CONTRACT_VERSION = "ai-runtime-boundary-v1"

GOVERNED_DOCUMENT_JOB_FAMILY = "governed_document_job"
GOVERNED_REPORTING_JOB_FAMILY = "governed_reporting_job"
SUPPORTED_AI_RUNTIME_JOB_FAMILIES = (
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_REPORTING_JOB_FAMILY,
)

DOCUMENT_ENGINE_CALLER_BOUNDARY = "document_engine_boundary"
EXPORT_ENGINE_CALLER_BOUNDARY = "export_engine_boundary"
ORCHESTRATION_SERVICE_CALLER_BOUNDARY = "orchestration_service_boundary"
SUPPORTED_AI_RUNTIME_CALLER_BOUNDARIES = (
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    EXPORT_ENGINE_CALLER_BOUNDARY,
    ORCHESTRATION_SERVICE_CALLER_BOUNDARY,
)

CONTROLLED_LANGUAGE_DRAFTING_PROFILE = "controlled_language_drafting"
BOUNDED_SUMMARIZATION_PROFILE = "bounded_summarization"
CANDIDATE_WORDING_GENERATION_PROFILE = "candidate_wording_generation"
SUPPORTED_MODEL_PERMISSION_PROFILES = (
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    BOUNDED_SUMMARIZATION_PROFILE,
    CANDIDATE_WORDING_GENERATION_PROFILE,
)

CANDIDATE_LANGUAGE_OUTPUT_ROLE = "candidate_language_output"
BOUNDED_SUMMARY_OUTPUT_ROLE = "bounded_summary_output"
SUPPORTED_AI_RUNTIME_OUTPUT_ROLES = (
    CANDIDATE_LANGUAGE_OUTPUT_ROLE,
    BOUNDED_SUMMARY_OUTPUT_ROLE,
)

AI_RUNTIME_BOUNDARY_STATUS_VALIDATED = "ai_runtime_boundary_validated"

_PROHIBITED_AI_RUNTIME_FIELDS = (
    "direct_llm_call",
    "llm_provider",
    "model_name",
    "api_key",
    "raw_prompt",
    "unvalidated_prompt",
    "free_form_user_prompt",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "execution_truth_override",
    "source_truth_override",
    "standards_truth_override",
    "validation_truth_override",
)

_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "ai_runtime_request_id",
    "job_family",
    "caller_boundary",
    "model_permission_profile",
    "requested_output_role",
    "runtime_boundary_status",
)

_REQUIRED_LIST_FIELDS = (
    "governed_source_refs",
    "engine_contract_refs",
)

_REQUIRED_FALSE_FIELDS = (
    "missing_engine_truth",
    "missing_contract_truth",
    "direct_user_prompt_as_source_truth",
    "ai_owns_source_truth",
    "ai_owns_execution_truth",
    "ai_can_mutate_state",
    "ai_can_approve_or_release",
    "ai_can_bypass_governed_retrieval",
    "ai_can_invent_standards",
    "ai_can_invent_evidence",
    "free_form_generation_requested",
    "unrestricted_generation_requested",
)

_DOCUMENT_CONTRACT_PREFIXES = (
    "DOCUMENT",
    "DOC",
    "TEMPLATE",
    "DCF",
    "GUARDRAIL",
)
_REPORTING_CONTRACT_PREFIXES = (
    "EXPORT",
    "REPORT",
    "REPORTING",
    "DASHBOARD",
    "GANTT",
    "SPREADSHEET",
)


def build_ai_runtime_boundary_baseline() -> dict[str, Any]:
    """Return M16.1 AI runtime boundary rules."""
    return {
        "checkpoint": AI_RUNTIME_BOUNDARY_CHECKPOINT_ID,
        "contract_version": AI_RUNTIME_BOUNDARY_CONTRACT_VERSION,
        "supported_job_families": list(SUPPORTED_AI_RUNTIME_JOB_FAMILIES),
        "supported_caller_boundaries": list(SUPPORTED_AI_RUNTIME_CALLER_BOUNDARIES),
        "supported_model_permission_profiles": list(
            SUPPORTED_MODEL_PERMISSION_PROFILES
        ),
        "supported_output_roles": list(SUPPORTED_AI_RUNTIME_OUTPUT_ROLES),
        "runtime_boundary_status": AI_RUNTIME_BOUNDARY_STATUS_VALIDATED,
        "allowed_ai_actions": [
            "draft_controlled_language",
            "summarize_governed_inputs",
            "prepare_candidate_wording",
            "produce_bounded_document_or_reporting_text",
            "return_candidate_output_for_downstream_acceptance",
        ],
        "prohibited_ai_actions": [
            "own_source_truth",
            "own_execution_truth",
            "approve_documents",
            "release_tasks",
            "mutate_workflow_state",
            "replace_template_document_or_export_contracts",
            "replace_standards_guardrails",
            "replace_validation_or_uat_evidence",
            "bypass_governed_retrieval",
            "invent_standards_or_evidence",
        ],
        "not_owned_by_m16_1": [
            "actual_llm_calls",
            "prompt_templates",
            "context_packaging",
            "controlled_generation_modes",
            "output_acceptance_retry_or_fallback",
            "ai_evaluation",
            "retrieval_use_governance",
            "recommendation_behavior",
            "ui_api_behavior",
            "runtime_document_generation",
            "runtime_export_generation",
        ],
    }


def build_ai_runtime_entry_request(
    *,
    ai_runtime_request_id: str,
    job_family: str,
    caller_boundary: str,
    model_permission_profile: str,
    governed_source_refs: list[str],
    engine_contract_refs: list[str],
    requested_output_role: str = CANDIDATE_LANGUAGE_OUTPUT_ROLE,
) -> dict[str, object]:
    """Build and validate an AI runtime entry request."""
    request = {
        "checkpoint": AI_RUNTIME_BOUNDARY_CHECKPOINT_ID,
        "contract_version": AI_RUNTIME_BOUNDARY_CONTRACT_VERSION,
        "ai_runtime_request_id": _require_non_empty_string(
            ai_runtime_request_id,
            field_name="ai_runtime_request_id",
            error_prefix="AI runtime entry request",
        ),
        "job_family": _normalize_supported_value(
            job_family,
            field_name="job_family",
            supported_values=SUPPORTED_AI_RUNTIME_JOB_FAMILIES,
            error_prefix="AI runtime entry request",
        ),
        "caller_boundary": _normalize_supported_value(
            caller_boundary,
            field_name="caller_boundary",
            supported_values=SUPPORTED_AI_RUNTIME_CALLER_BOUNDARIES,
            error_prefix="AI runtime entry request",
        ),
        "model_permission_profile": _normalize_supported_value(
            model_permission_profile,
            field_name="model_permission_profile",
            supported_values=SUPPORTED_MODEL_PERMISSION_PROFILES,
            error_prefix="AI runtime entry request",
        ),
        "requested_output_role": _normalize_supported_value(
            requested_output_role,
            field_name="requested_output_role",
            supported_values=SUPPORTED_AI_RUNTIME_OUTPUT_ROLES,
            error_prefix="AI runtime entry request",
        ),
        "runtime_boundary_status": AI_RUNTIME_BOUNDARY_STATUS_VALIDATED,
        "governed_source_refs": list(governed_source_refs),
        "engine_contract_refs": list(engine_contract_refs),
        "missing_engine_truth": False,
        "missing_contract_truth": False,
        "direct_user_prompt_as_source_truth": False,
        "ai_owns_source_truth": False,
        "ai_owns_execution_truth": False,
        "ai_can_mutate_state": False,
        "ai_can_approve_or_release": False,
        "ai_can_bypass_governed_retrieval": False,
        "ai_can_invent_standards": False,
        "ai_can_invent_evidence": False,
        "free_form_generation_requested": False,
        "unrestricted_generation_requested": False,
        "source_role_policy": "ai_runtime_consumes_governed_engine_truth_only",
        "output_role_policy": "ai_runtime_returns_candidate_output_for_downstream_acceptance_only",
    }
    validate_ai_runtime_entry_request(request)
    return request


def validate_ai_runtime_entry_request(request: dict[str, object]) -> None:
    """Validate an M16.1 AI runtime entry request."""
    _validate_prohibited_fields(request, _PROHIBITED_AI_RUNTIME_FIELDS)
    _validate_required_string_fields(
        request,
        _REQUIRED_STRING_FIELDS,
        error_prefix="AI runtime entry request",
    )
    _validate_expected_exact_value(
        request,
        field_name="checkpoint",
        expected_value=AI_RUNTIME_BOUNDARY_CHECKPOINT_ID,
        error_prefix="AI runtime entry request",
    )
    _validate_expected_exact_value(
        request,
        field_name="contract_version",
        expected_value=AI_RUNTIME_BOUNDARY_CONTRACT_VERSION,
        error_prefix="AI runtime entry request",
    )
    _validate_expected_exact_value(
        request,
        field_name="runtime_boundary_status",
        expected_value=AI_RUNTIME_BOUNDARY_STATUS_VALIDATED,
        error_prefix="AI runtime entry request",
    )

    job_family = _normalize_supported_value(
        request["job_family"],
        field_name="job_family",
        supported_values=SUPPORTED_AI_RUNTIME_JOB_FAMILIES,
        error_prefix="AI runtime entry request",
    )
    _normalize_supported_value(
        request["caller_boundary"],
        field_name="caller_boundary",
        supported_values=SUPPORTED_AI_RUNTIME_CALLER_BOUNDARIES,
        error_prefix="AI runtime entry request",
    )
    _normalize_supported_value(
        request["model_permission_profile"],
        field_name="model_permission_profile",
        supported_values=SUPPORTED_MODEL_PERMISSION_PROFILES,
        error_prefix="AI runtime entry request",
    )
    _normalize_supported_value(
        request["requested_output_role"],
        field_name="requested_output_role",
        supported_values=SUPPORTED_AI_RUNTIME_OUTPUT_ROLES,
        error_prefix="AI runtime entry request",
    )

    for field_name in _REQUIRED_LIST_FIELDS:
        values = request.get(field_name)
        if not isinstance(values, list) or not values:
            raise ValueError(
                f"AI runtime entry request must declare non-empty {field_name}."
            )

    for field_name in _REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(
                f"AI runtime entry request requires {field_name} to be False."
            )

    governed_source_refs = _parse_ref_list(
        request["governed_source_refs"],  # type: ignore[index]
        field_name="governed_source_refs",
    )
    _reject_duplicates(governed_source_refs, field_name="governed_source_refs")

    engine_contract_refs = _parse_ref_list(
        request["engine_contract_refs"],  # type: ignore[index]
        field_name="engine_contract_refs",
    )
    _reject_duplicates(engine_contract_refs, field_name="engine_contract_refs")
    _validate_contract_refs_for_job_family(
        job_family=job_family,
        engine_contract_refs=engine_contract_refs,
    )


def validate_ai_runtime_blocked_state(request: dict[str, object]) -> None:
    """Validate that request does not enter any M16.1 blocked state."""
    _validate_prohibited_fields(request, _PROHIBITED_AI_RUNTIME_FIELDS)
    for field_name in _REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(f"AI runtime blocked state detected: {field_name}.")


def _validate_contract_refs_for_job_family(
    *,
    job_family: str,
    engine_contract_refs: list[str],
) -> None:
    prefixes = (
        _DOCUMENT_CONTRACT_PREFIXES
        if job_family == GOVERNED_DOCUMENT_JOB_FAMILY
        else _REPORTING_CONTRACT_PREFIXES
    )
    for ref in engine_contract_refs:
        asset_id = parse_version_pinned_asset_ref(ref)["asset_id"]
        if asset_id.startswith(prefixes):
            return
    raise ValueError(
        "AI runtime entry request must include an engine contract ref aligned "
        f"with job_family {job_family!r}."
    )


def _parse_ref_list(raw_refs: list[object], *, field_name: str) -> list[str]:
    normalized_refs: list[str] = []
    for raw_ref in raw_refs:
        ref = _require_non_empty_string(
            raw_ref,
            field_name=field_name,
            error_prefix="AI runtime entry request",
        )
        normalized_refs.append(parse_version_pinned_asset_ref(ref)["asset_ref"])
    return normalized_refs


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


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate ref in {field_name}: {value!r}.")
        seen.add(value)


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
                f"{field_name} is not allowed in M16.1 AI runtime boundary requests."
            )
