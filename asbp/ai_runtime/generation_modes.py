"AI controlled generation modes for document/reporting families in M16.3."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

from .context_packaging import (
    AI_CONTEXT_PACKAGE_STATUS_VALIDATED,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
    UNAVAILABLE_EVIDENCE_STATUS,
    VALIDATED_EVIDENCE_STATUS,
    validate_ai_context_package,
)
from .runtime_boundary import (
    BOUNDED_SUMMARY_OUTPUT_ROLE,
    CANDIDATE_LANGUAGE_OUTPUT_ROLE,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_REPORTING_JOB_FAMILY,
    SUPPORTED_AI_RUNTIME_OUTPUT_ROLES,
)

AI_GENERATION_MODES_CHECKPOINT_ID = "M16.3"
AI_GENERATION_MODES_CONTRACT_VERSION = "ai-generation-modes-v1"
AI_GENERATION_MODE_STATUS_VALIDATED = "ai_generation_mode_validated"

URS_DOCUMENT_FAMILY = "urs_document"
DCF_DOCUMENT_FAMILY = "dcf_document"
PROTOCOL_DOCUMENT_FAMILY = "protocol_document"
REPORT_DOCUMENT_FAMILY = "report_document"
SUPPORTED_DOCUMENT_OUTPUT_FAMILIES = (
    URS_DOCUMENT_FAMILY,
    DCF_DOCUMENT_FAMILY,
    PROTOCOL_DOCUMENT_FAMILY,
    REPORT_DOCUMENT_FAMILY,
)

STATUS_SUMMARY_REPORTING_FAMILY = "status_summary_reporting"
DASHBOARD_SUMMARY_REPORTING_FAMILY = "dashboard_summary_reporting"
EXCEPTION_NARRATIVE_REPORTING_FAMILY = "exception_narrative_reporting"
SUPPORTED_REPORTING_OUTPUT_FAMILIES = (
    STATUS_SUMMARY_REPORTING_FAMILY,
    DASHBOARD_SUMMARY_REPORTING_FAMILY,
    EXCEPTION_NARRATIVE_REPORTING_FAMILY,
)
SUPPORTED_GENERATION_OUTPUT_FAMILIES = (
    *SUPPORTED_DOCUMENT_OUTPUT_FAMILIES,
    *SUPPORTED_REPORTING_OUTPUT_FAMILIES,
)

STRONG_STRUCTURED_INPUT_FILL_MODE = "strong_structured_input_fill"
PARTIAL_INPUT_BOUNDED_COMPLETION_MODE = "partial_input_bounded_completion"
MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE = "minimal_input_scaffold_generation"
EVIDENCE_BOUND_REPORT_NARRATIVE_MODE = "evidence_bound_report_narrative"
BOUNDED_REPORT_SUMMARY_MODE = "bounded_report_summary"
SUPPORTED_GENERATION_MODES = (
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE,
    EVIDENCE_BOUND_REPORT_NARRATIVE_MODE,
    BOUNDED_REPORT_SUMMARY_MODE,
)

_GENERATION_MODES_BY_OUTPUT_FAMILY = {
    URS_DOCUMENT_FAMILY: (
        STRONG_STRUCTURED_INPUT_FILL_MODE,
        PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
        MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE,
    ),
    DCF_DOCUMENT_FAMILY: (
        STRONG_STRUCTURED_INPUT_FILL_MODE,
        PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    ),
    PROTOCOL_DOCUMENT_FAMILY: (
        STRONG_STRUCTURED_INPUT_FILL_MODE,
        PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
        MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE,
    ),
    REPORT_DOCUMENT_FAMILY: (
        STRONG_STRUCTURED_INPUT_FILL_MODE,
        PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
        EVIDENCE_BOUND_REPORT_NARRATIVE_MODE,
        BOUNDED_REPORT_SUMMARY_MODE,
    ),
    STATUS_SUMMARY_REPORTING_FAMILY: (BOUNDED_REPORT_SUMMARY_MODE,),
    DASHBOARD_SUMMARY_REPORTING_FAMILY: (BOUNDED_REPORT_SUMMARY_MODE,),
    EXCEPTION_NARRATIVE_REPORTING_FAMILY: (EVIDENCE_BOUND_REPORT_NARRATIVE_MODE,),
}

_MODE_POLICIES: dict[str, dict[str, object]] = {
    STRONG_STRUCTURED_INPUT_FILL_MODE: {
        "bounded_invention_allowed": False,
        "assumption_labeling_required": False,
        "placeholder_policy_required": True,
        "all_generation_context_must_be_validated": True,
        "language_policy": "fill_from_validated_structured_and_contract_inputs_only",
    },
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE: {
        "bounded_invention_allowed": True,
        "assumption_labeling_required": True,
        "placeholder_policy_required": True,
        "all_generation_context_must_be_validated": False,
        "language_policy": "complete_only_with_labeled_assumptions_and_tbd_placeholders",
    },
    MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE: {
        "bounded_invention_allowed": True,
        "assumption_labeling_required": True,
        "placeholder_policy_required": True,
        "all_generation_context_must_be_validated": False,
        "language_policy": "produce_scaffold_only_without_unverified_evidence_claims",
    },
    EVIDENCE_BOUND_REPORT_NARRATIVE_MODE: {
        "bounded_invention_allowed": False,
        "assumption_labeling_required": False,
        "placeholder_policy_required": True,
        "all_generation_context_must_be_validated": True,
        "language_policy": "narrate_validated_evidence_without_new_claims",
    },
    BOUNDED_REPORT_SUMMARY_MODE: {
        "bounded_invention_allowed": False,
        "assumption_labeling_required": False,
        "placeholder_policy_required": True,
        "all_generation_context_must_be_validated": True,
        "language_policy": "summarize_validated_reporting_inputs_only",
    },
}

_PROHIBITED_GENERATION_FIELDS = (
    "raw_prompt",
    "free_form_prompt",
    "unvalidated_user_prompt",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "direct_llm_call",
    "llm_provider",
    "model_name",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "execution_truth_override",
    "source_truth_override",
    "standards_truth_override",
    "generated_document_text",
    "generated_report_text",
    "accepted_output_payload",
    "retry_payload",
    "fallback_output_payload",
)

_GENERATION_REQUEST_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "generation_request_id",
    "context_package_id",
    "runtime_request_id",
    "job_family",
    "output_family",
    "generation_mode",
    "generation_mode_status",
    "source_context_package_status",
    "standards_guardrail_ref",
    "requested_output_role",
)

_GENERATION_REQUEST_REQUIRED_FALSE_FIELDS = (
    "actual_llm_call_requested",
    "raw_prompt_allowed",
    "prompt_template_generated",
    "unrestricted_generation_allowed",
    "ai_can_define_source_truth",
    "ai_can_define_execution_truth",
    "ai_can_invent_standards",
    "ai_can_invent_evidence",
    "ai_can_mutate_state",
    "output_acceptance_in_scope",
    "retry_or_fallback_in_scope",
)

_GENERATION_REQUEST_REQUIRED_BOOL_FIELDS = (
    "bounded_invention_allowed",
    "assumption_labeling_required",
    "placeholder_policy_required",
    "standards_guardrail_required",
    "all_generation_context_must_be_validated",
)


def build_ai_generation_modes_baseline() -> dict[str, Any]:
    """Return the M16.3 controlled-generation-mode baseline."""
    return {
        "checkpoint": AI_GENERATION_MODES_CHECKPOINT_ID,
        "contract_version": AI_GENERATION_MODES_CONTRACT_VERSION,
        "supported_document_output_families": list(SUPPORTED_DOCUMENT_OUTPUT_FAMILIES),
        "supported_reporting_output_families": list(SUPPORTED_REPORTING_OUTPUT_FAMILIES),
        "supported_generation_modes": list(SUPPORTED_GENERATION_MODES),
        "generation_modes_by_output_family": {
            family: list(modes)
            for family, modes in _GENERATION_MODES_BY_OUTPUT_FAMILY.items()
        },
        "mode_policies": _copy_mode_policies(),
        "standards_awareness_policy": (
            "generation_modes_must_use_declared_standards_guardrail_context_only"
        ),
        "bounded_invention_policy": (
            "bounded_invention_is_mode_specific_labeled_and_never_source_truth"
        ),
        "output_truth_policy": (
            "generation_mode_requests_may_prepare_candidate_language_only"
        ),
        "not_owned_by_m16_3": [
            "actual_llm_calls",
            "prompt_templates",
            "document_or_report_text_generation",
            "output_acceptance",
            "retry_fallback_behavior",
            "ai_evaluation",
            "retrieval_use_governance",
            "recommendation_behavior",
            "ui_api_behavior",
        ],
    }


def build_ai_generation_mode_request(
    *,
    generation_request_id: str,
    context_package: dict[str, object],
    output_family: str,
    generation_mode: str,
    standards_guardrail_ref: str,
    requested_output_role: str | None = None,
) -> dict[str, object]:
    """Build and validate an M16.3 controlled generation-mode request."""
    validate_ai_context_package(context_package)
    normalized_output_family = _normalize_supported_value(
        output_family,
        field_name="output_family",
        supported_values=SUPPORTED_GENERATION_OUTPUT_FAMILIES,
        error_prefix="AI generation mode request",
    )
    normalized_generation_mode = _normalize_supported_value(
        generation_mode,
        field_name="generation_mode",
        supported_values=SUPPORTED_GENERATION_MODES,
        error_prefix="AI generation mode request",
    )
    default_output_role = _default_output_role_for_output_family(normalized_output_family)
    policy = _mode_policy(normalized_generation_mode)

    request = {
        "checkpoint": AI_GENERATION_MODES_CHECKPOINT_ID,
        "contract_version": AI_GENERATION_MODES_CONTRACT_VERSION,
        "generation_request_id": _require_non_empty_string(
            generation_request_id,
            field_name="generation_request_id",
            error_prefix="AI generation mode request",
        ),
        "context_package_id": str(context_package["context_package_id"]),
        "runtime_request_id": str(context_package["runtime_request_id"]),
        "job_family": str(context_package["job_family"]),
        "output_family": normalized_output_family,
        "generation_mode": normalized_generation_mode,
        "generation_mode_status": AI_GENERATION_MODE_STATUS_VALIDATED,
        "source_context_package_status": str(context_package["context_package_status"]),
        "standards_guardrail_ref": _parse_version_pinned_ref(
            standards_guardrail_ref,
            field_name="standards_guardrail_ref",
        ),
        "requested_output_role": _normalize_supported_value(
            requested_output_role or default_output_role,
            field_name="requested_output_role",
            supported_values=SUPPORTED_AI_RUNTIME_OUTPUT_ROLES,
            error_prefix="AI generation mode request",
        ),
        "source_context_package": dict(context_package),
        "bounded_invention_allowed": bool(policy["bounded_invention_allowed"]),
        "assumption_labeling_required": bool(policy["assumption_labeling_required"]),
        "placeholder_policy_required": bool(policy["placeholder_policy_required"]),
        "standards_guardrail_required": True,
        "all_generation_context_must_be_validated": bool(
            policy["all_generation_context_must_be_validated"]
        ),
        "actual_llm_call_requested": False,
        "raw_prompt_allowed": False,
        "prompt_template_generated": False,
        "unrestricted_generation_allowed": False,
        "ai_can_define_source_truth": False,
        "ai_can_define_execution_truth": False,
        "ai_can_invent_standards": False,
        "ai_can_invent_evidence": False,
        "ai_can_mutate_state": False,
        "output_acceptance_in_scope": False,
        "retry_or_fallback_in_scope": False,
        "language_policy": str(policy["language_policy"]),
        "source_truth_policy": "generation_modes_consume_context_only",
        "output_boundary_policy": "candidate_language_only_no_acceptance_or_retry",
    }
    validate_ai_generation_mode_request(request)
    return request


def validate_ai_generation_mode_request(request: dict[str, object]) -> None:
    """Validate an M16.3 controlled generation-mode request."""
    _validate_prohibited_fields(request, _PROHIBITED_GENERATION_FIELDS)
    _validate_required_string_fields(
        request,
        _GENERATION_REQUEST_REQUIRED_STRING_FIELDS,
        error_prefix="AI generation mode request",
    )
    _validate_expected_exact_value(
        request,
        field_name="checkpoint",
        expected_value=AI_GENERATION_MODES_CHECKPOINT_ID,
        error_prefix="AI generation mode request",
    )
    _validate_expected_exact_value(
        request,
        field_name="contract_version",
        expected_value=AI_GENERATION_MODES_CONTRACT_VERSION,
        error_prefix="AI generation mode request",
    )
    _validate_expected_exact_value(
        request,
        field_name="generation_mode_status",
        expected_value=AI_GENERATION_MODE_STATUS_VALIDATED,
        error_prefix="AI generation mode request",
    )
    _validate_expected_exact_value(
        request,
        field_name="source_context_package_status",
        expected_value=AI_CONTEXT_PACKAGE_STATUS_VALIDATED,
        error_prefix="AI generation mode request",
    )

    for field_name in _GENERATION_REQUEST_REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(
                f"AI generation mode request requires {field_name} to be False."
            )
    for field_name in _GENERATION_REQUEST_REQUIRED_BOOL_FIELDS:
        _require_bool(
            request.get(field_name),
            field_name=field_name,
            error_prefix="AI generation mode request",
        )

    context_package = request.get("source_context_package")
    if not isinstance(context_package, dict):
        raise ValueError(
            "AI generation mode request must include source_context_package dict."
        )
    validate_ai_context_package(context_package)

    if request["context_package_id"] != context_package["context_package_id"]:
        raise ValueError(
            "AI generation mode request context_package_id must match source_context_package."
        )
    if request["runtime_request_id"] != context_package["runtime_request_id"]:
        raise ValueError(
            "AI generation mode request runtime_request_id must match source_context_package."
        )

    job_family = _normalize_supported_value(
        request["job_family"],
        field_name="job_family",
        supported_values=(GOVERNED_DOCUMENT_JOB_FAMILY, GOVERNED_REPORTING_JOB_FAMILY),
        error_prefix="AI generation mode request",
    )
    if job_family != context_package["job_family"]:
        raise ValueError(
            "AI generation mode request job_family must match source_context_package."
        )

    output_family = _normalize_supported_value(
        request["output_family"],
        field_name="output_family",
        supported_values=SUPPORTED_GENERATION_OUTPUT_FAMILIES,
        error_prefix="AI generation mode request",
    )
    generation_mode = _normalize_supported_value(
        request["generation_mode"],
        field_name="generation_mode",
        supported_values=SUPPORTED_GENERATION_MODES,
        error_prefix="AI generation mode request",
    )
    requested_output_role = _normalize_supported_value(
        request["requested_output_role"],
        field_name="requested_output_role",
        supported_values=SUPPORTED_AI_RUNTIME_OUTPUT_ROLES,
        error_prefix="AI generation mode request",
    )

    _validate_output_family_for_job_family(
        output_family=output_family,
        job_family=job_family,
    )
    _validate_generation_mode_for_output_family(
        generation_mode=generation_mode,
        output_family=output_family,
    )
    _validate_output_role_for_output_family(
        requested_output_role=requested_output_role,
        output_family=output_family,
    )
    _validate_mode_policy_flags(
        request=request,
        generation_mode=generation_mode,
    )
    _validate_standards_guardrail_ref(
        context_package=context_package,
        standards_guardrail_ref=request["standards_guardrail_ref"],
    )
    _validate_evidence_policy_for_mode(
        context_package=context_package,
        generation_mode=generation_mode,
    )


def _copy_mode_policies() -> dict[str, dict[str, object]]:
    return {mode: dict(policy) for mode, policy in _MODE_POLICIES.items()}


def _mode_policy(generation_mode: str) -> dict[str, object]:
    try:
        return _MODE_POLICIES[generation_mode]
    except KeyError as exc:
        raise ValueError(
            f"AI generation mode request declares unsupported generation_mode: "
            f"{generation_mode!r}."
        ) from exc


def _default_output_role_for_output_family(output_family: str) -> str:
    if output_family in SUPPORTED_REPORTING_OUTPUT_FAMILIES:
        return BOUNDED_SUMMARY_OUTPUT_ROLE
    return CANDIDATE_LANGUAGE_OUTPUT_ROLE


def _validate_output_family_for_job_family(*, output_family: str, job_family: str) -> None:
    if job_family == GOVERNED_DOCUMENT_JOB_FAMILY:
        allowed_families = SUPPORTED_DOCUMENT_OUTPUT_FAMILIES
    elif job_family == GOVERNED_REPORTING_JOB_FAMILY:
        allowed_families = SUPPORTED_REPORTING_OUTPUT_FAMILIES
    else:
        raise ValueError(f"Unsupported AI generation job_family: {job_family!r}.")

    if output_family not in allowed_families:
        raise ValueError(
            "AI generation mode request output_family is not aligned with "
            f"job_family {job_family!r}."
        )


def _validate_generation_mode_for_output_family(
    *, generation_mode: str, output_family: str
) -> None:
    allowed_modes = _GENERATION_MODES_BY_OUTPUT_FAMILY[output_family]
    if generation_mode not in allowed_modes:
        raise ValueError(
            "AI generation mode request generation_mode is not allowed for "
            f"output_family {output_family!r}."
        )


def _validate_output_role_for_output_family(
    *, requested_output_role: str, output_family: str
) -> None:
    expected_role = _default_output_role_for_output_family(output_family)
    if requested_output_role != expected_role:
        raise ValueError(
            "AI generation mode request requested_output_role is not aligned "
            f"with output_family {output_family!r}. Expected {expected_role!r}."
        )


def _validate_mode_policy_flags(
    *, request: dict[str, object], generation_mode: str
) -> None:
    policy = _mode_policy(generation_mode)
    for field_name in (
        "bounded_invention_allowed",
        "assumption_labeling_required",
        "placeholder_policy_required",
        "all_generation_context_must_be_validated",
    ):
        if request.get(field_name) != policy[field_name]:
            raise ValueError(
                f"AI generation mode request {field_name} does not match "
                f"policy for {generation_mode!r}."
            )


def _validate_standards_guardrail_ref(
    *, context_package: dict[str, object], standards_guardrail_ref: object
) -> None:
    normalized_ref = _parse_version_pinned_ref(
        standards_guardrail_ref,
        field_name="standards_guardrail_ref",
    )
    for item in _context_items(context_package):
        if (
            item.get("source_family") == STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY
            and item.get("source_ref") == normalized_ref
            and item.get("may_be_used_for_generation") is True
            and item.get("evidence_status") != UNAVAILABLE_EVIDENCE_STATUS
        ):
            return
    raise ValueError(
        "AI generation mode request standards_guardrail_ref must match a "
        "generation-eligible standards guardrail context item."
    )


def _validate_evidence_policy_for_mode(
    *, context_package: dict[str, object], generation_mode: str
) -> None:
    policy = _mode_policy(generation_mode)
    generation_items = [
        item
        for item in _context_items(context_package)
        if item.get("may_be_used_for_generation") is True
    ]
    if not generation_items:
        raise ValueError(
            "AI generation mode request requires at least one generation-eligible "
            "context item."
        )

    if policy["all_generation_context_must_be_validated"] is True:
        for item in generation_items:
            if item.get("evidence_status") != VALIDATED_EVIDENCE_STATUS:
                raise ValueError(
                    "AI generation mode request requires all generation-eligible "
                    f"context evidence to be validated for mode {generation_mode!r}."
                )


def _context_items(context_package: dict[str, object]) -> list[dict[str, object]]:
    raw_items = context_package.get("context_items")
    if not isinstance(raw_items, list):
        raise ValueError("AI context package must expose list context_items.")
    items: list[dict[str, object]] = []
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            raise ValueError("AI context package context_items must contain dicts.")
        items.append(raw_item)
    return items


def _parse_version_pinned_ref(raw_ref: object, *, field_name: str) -> str:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="AI generation mode ref",
    )
    return parse_version_pinned_asset_ref(ref)["asset_ref"]


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
    payload: dict[str, object], prohibited_fields: tuple[str, ...]
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in M16.3 AI generation mode requests."
            )
