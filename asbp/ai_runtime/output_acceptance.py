"AI output acceptance, bounded retry, and fallback behavior for M16.4."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

from .context_packaging import (
    PARTIAL_EVIDENCE_STATUS,
    UNAVAILABLE_EVIDENCE_STATUS,
    VALIDATED_EVIDENCE_STATUS,
)
from .generation_modes import (
    AI_GENERATION_MODE_STATUS_VALIDATED,
    SUPPORTED_DOCUMENT_OUTPUT_FAMILIES,
    SUPPORTED_GENERATION_MODES,
    SUPPORTED_REPORTING_OUTPUT_FAMILIES,
    validate_ai_generation_mode_request,
)

AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID = "M16.4"
AI_OUTPUT_ACCEPTANCE_CONTRACT_VERSION = "ai-output-acceptance-v1"
AI_CANDIDATE_OUTPUT_STATUS_VALIDATED = "ai_candidate_output_validated"
AI_OUTPUT_ACCEPTANCE_STATUS_VALIDATED = "ai_output_acceptance_validated"

CANDIDATE_DOCUMENT_LANGUAGE_OUTPUT_CLASSIFICATION = "candidate_document_language"
CANDIDATE_REPORTING_LANGUAGE_OUTPUT_CLASSIFICATION = "candidate_reporting_language"
SUPPORTED_CANDIDATE_OUTPUT_CLASSIFICATIONS = (
    CANDIDATE_DOCUMENT_LANGUAGE_OUTPUT_CLASSIFICATION,
    CANDIDATE_REPORTING_LANGUAGE_OUTPUT_CLASSIFICATION,
)

ACCEPT_CANDIDATE_OUTPUT_DECISION = "accept_candidate_output"
RETRY_CANDIDATE_OUTPUT_DECISION = "retry_candidate_output"
FALLBACK_OR_REFUSE_OUTPUT_DECISION = "fallback_or_refuse_output"
SUPPORTED_OUTPUT_ACCEPTANCE_DECISIONS = (
    ACCEPT_CANDIDATE_OUTPUT_DECISION,
    RETRY_CANDIDATE_OUTPUT_DECISION,
    FALLBACK_OR_REFUSE_OUTPUT_DECISION,
)

CONTRACT_RULE_FAILURE_RETRY_REASON = "contract_rule_failure"
STANDARDS_GUARDRAIL_FAILURE_RETRY_REASON = "standards_guardrail_failure"
EVIDENCE_SUPPORT_FAILURE_RETRY_REASON = "evidence_support_failure"
ASSUMPTION_LABELING_FAILURE_RETRY_REASON = "assumption_labeling_failure"
PLACEHOLDER_POLICY_FAILURE_RETRY_REASON = "placeholder_policy_failure"
PROHIBITED_OUTPUT_CLAIM_FAILURE_RETRY_REASON = "prohibited_output_claim_failure"
SUPPORTED_BOUNDED_RETRY_REASONS = (
    CONTRACT_RULE_FAILURE_RETRY_REASON,
    STANDARDS_GUARDRAIL_FAILURE_RETRY_REASON,
    EVIDENCE_SUPPORT_FAILURE_RETRY_REASON,
    ASSUMPTION_LABELING_FAILURE_RETRY_REASON,
    PLACEHOLDER_POLICY_FAILURE_RETRY_REASON,
    PROHIBITED_OUTPUT_CLAIM_FAILURE_RETRY_REASON,
)

INSUFFICIENT_EVIDENCE_FALLBACK_REASON = "insufficient_evidence"
BROKEN_CONTRACT_FALLBACK_REASON = "broken_contract"
RETRY_LIMIT_REACHED_FALLBACK_REASON = "retry_limit_reached"
FAIL_CLOSED_REQUIRED_FALLBACK_REASON = "fail_closed_required"
SUPPORTED_FALLBACK_REASONS = (
    INSUFFICIENT_EVIDENCE_FALLBACK_REASON,
    BROKEN_CONTRACT_FALLBACK_REASON,
    RETRY_LIMIT_REACHED_FALLBACK_REASON,
    FAIL_CLOSED_REQUIRED_FALLBACK_REASON,
)

DEFAULT_MAX_RETRY_ATTEMPTS = 2

_PROHIBITED_ACCEPTANCE_FIELDS = (
    "raw_prompt",
    "free_form_prompt",
    "unvalidated_user_prompt",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "direct_llm_call",
    "llm_provider",
    "model_name",
    "api_key",
    "generated_document_text",
    "generated_report_text",
    "generated_output_text",
    "replacement_prompt",
    "retry_prompt",
    "fallback_prompt",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "execution_truth_override",
    "source_truth_override",
    "standards_truth_override",
    "validation_truth_override",
)

_CANDIDATE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "output_candidate_id",
    "generation_request_id",
    "context_package_id",
    "runtime_request_id",
    "job_family",
    "output_family",
    "generation_mode",
    "candidate_output_ref",
    "candidate_output_role",
    "candidate_output_classification",
    "candidate_output_status",
    "source_generation_mode_status",
    "candidate_evidence_status",
)

_CANDIDATE_REQUIRED_TRUE_FIELDS = (
    "content_contract_satisfied",
    "family_constraints_satisfied",
    "standards_guardrails_satisfied",
    "evidence_claims_supported",
    "assumptions_labeled_when_required",
    "placeholders_used_for_missing_truth",
)

_CANDIDATE_REQUIRED_FALSE_FIELDS = (
    "contains_unbounded_invention",
    "contains_unverified_standards_claims",
    "contains_unverified_evidence_claims",
    "contains_execution_truth_claims",
    "requests_state_mutation",
    "approval_requested",
    "release_requested",
    "accepted_as_final_output",
    "validation_or_uat_truth_claimed",
)

_DECISION_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "acceptance_decision_id",
    "output_candidate_id",
    "generation_request_id",
    "context_package_id",
    "runtime_request_id",
    "job_family",
    "output_family",
    "generation_mode",
    "acceptance_status",
    "acceptance_decision",
)

_DECISION_REQUIRED_FALSE_FIELDS = (
    "ai_can_mutate_state",
    "ai_can_approve_or_release",
    "approval_payload_included",
    "workflow_release_payload_included",
    "validation_or_uat_truth_claimed",
)


def build_ai_output_acceptance_baseline() -> dict[str, Any]:
    """Return the M16.4 output-acceptance baseline."""
    return {
        "checkpoint": AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID,
        "contract_version": AI_OUTPUT_ACCEPTANCE_CONTRACT_VERSION,
        "candidate_output_classifications": list(
            SUPPORTED_CANDIDATE_OUTPUT_CLASSIFICATIONS
        ),
        "supported_output_acceptance_decisions": list(
            SUPPORTED_OUTPUT_ACCEPTANCE_DECISIONS
        ),
        "supported_bounded_retry_reasons": list(SUPPORTED_BOUNDED_RETRY_REASONS),
        "supported_fallback_reasons": list(SUPPORTED_FALLBACK_REASONS),
        "default_max_retry_attempts": DEFAULT_MAX_RETRY_ATTEMPTS,
        "acceptance_policy": (
            "candidate_output_must_satisfy_contract_family_standards_evidence_"
            "assumption_and_placeholder_rules"
        ),
        "bounded_retry_policy": (
            "retry_is_limited_and_must_not_relax_generation_mode_or_contract_rules"
        ),
        "fallback_policy": (
            "fallback_or_refusal_is_required_when_evidence_is_insufficient_"
            "contracts_are_broken_or_retry_limits_are_reached"
        ),
        "fail_closed_policy": "unsafe_or_unsupported_output_must_not_be_accepted",
        "not_owned_by_m16_4": [
            "actual_llm_calls",
            "prompt_templates",
            "document_or_report_text_generation",
            "ai_evaluation",
            "retrieval_use_governance",
            "recommendation_behavior",
            "ui_api_behavior",
            "workflow_state_mutation",
            "document_approval_or_release",
        ],
    }


def build_ai_candidate_output(
    *,
    output_candidate_id: str,
    generation_mode_request: dict[str, object],
    candidate_output_ref: str,
    candidate_evidence_status: str,
    content_contract_satisfied: bool,
    family_constraints_satisfied: bool,
    standards_guardrails_satisfied: bool,
    evidence_claims_supported: bool,
    assumptions_labeled_when_required: bool,
    placeholders_used_for_missing_truth: bool,
    contains_unbounded_invention: bool = False,
    contains_unverified_standards_claims: bool = False,
    contains_unverified_evidence_claims: bool = False,
    contains_execution_truth_claims: bool = False,
    requests_state_mutation: bool = False,
    approval_requested: bool = False,
    release_requested: bool = False,
) -> dict[str, object]:
    """Build and validate candidate-output metadata."""
    validate_ai_generation_mode_request(generation_mode_request)
    output_family = str(generation_mode_request["output_family"])
    candidate = {
        "checkpoint": AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID,
        "contract_version": AI_OUTPUT_ACCEPTANCE_CONTRACT_VERSION,
        "output_candidate_id": _require_non_empty_string(
            output_candidate_id,
            field_name="output_candidate_id",
            error_prefix="AI candidate output",
        ),
        "generation_request_id": str(generation_mode_request["generation_request_id"]),
        "context_package_id": str(generation_mode_request["context_package_id"]),
        "runtime_request_id": str(generation_mode_request["runtime_request_id"]),
        "job_family": str(generation_mode_request["job_family"]),
        "output_family": output_family,
        "generation_mode": str(generation_mode_request["generation_mode"]),
        "candidate_output_ref": _parse_version_pinned_ref(
            candidate_output_ref,
            field_name="candidate_output_ref",
        ),
        "candidate_output_role": str(generation_mode_request["requested_output_role"]),
        "candidate_output_classification": _classification_for_output_family(
            output_family
        ),
        "candidate_output_status": AI_CANDIDATE_OUTPUT_STATUS_VALIDATED,
        "source_generation_mode_status": str(
            generation_mode_request["generation_mode_status"]
        ),
        "candidate_evidence_status": _normalize_supported_value(
            candidate_evidence_status,
            field_name="candidate_evidence_status",
            supported_values=(
                VALIDATED_EVIDENCE_STATUS,
                PARTIAL_EVIDENCE_STATUS,
                UNAVAILABLE_EVIDENCE_STATUS,
            ),
            error_prefix="AI candidate output",
        ),
        "source_generation_mode_request": dict(generation_mode_request),
        "content_contract_satisfied": content_contract_satisfied,
        "family_constraints_satisfied": family_constraints_satisfied,
        "standards_guardrails_satisfied": standards_guardrails_satisfied,
        "evidence_claims_supported": evidence_claims_supported,
        "assumptions_labeled_when_required": assumptions_labeled_when_required,
        "placeholders_used_for_missing_truth": placeholders_used_for_missing_truth,
        "contains_unbounded_invention": contains_unbounded_invention,
        "contains_unverified_standards_claims": contains_unverified_standards_claims,
        "contains_unverified_evidence_claims": contains_unverified_evidence_claims,
        "contains_execution_truth_claims": contains_execution_truth_claims,
        "requests_state_mutation": requests_state_mutation,
        "approval_requested": approval_requested,
        "release_requested": release_requested,
        "accepted_as_final_output": False,
        "validation_or_uat_truth_claimed": False,
        "output_acceptance_policy": "candidate_metadata_only_no_generated_text_payload",
    }
    validate_ai_candidate_output(candidate)
    return candidate


def validate_ai_candidate_output(candidate: dict[str, object]) -> None:
    """Validate one M16.4 candidate-output metadata payload."""
    _validate_prohibited_fields(candidate, _PROHIBITED_ACCEPTANCE_FIELDS)
    _validate_required_string_fields(
        candidate,
        _CANDIDATE_REQUIRED_STRING_FIELDS,
        error_prefix="AI candidate output",
    )
    _validate_expected_exact_value(
        candidate,
        field_name="checkpoint",
        expected_value=AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID,
        error_prefix="AI candidate output",
    )
    _validate_expected_exact_value(
        candidate,
        field_name="contract_version",
        expected_value=AI_OUTPUT_ACCEPTANCE_CONTRACT_VERSION,
        error_prefix="AI candidate output",
    )
    _validate_expected_exact_value(
        candidate,
        field_name="candidate_output_status",
        expected_value=AI_CANDIDATE_OUTPUT_STATUS_VALIDATED,
        error_prefix="AI candidate output",
    )
    _validate_expected_exact_value(
        candidate,
        field_name="source_generation_mode_status",
        expected_value=AI_GENERATION_MODE_STATUS_VALIDATED,
        error_prefix="AI candidate output",
    )

    request = candidate.get("source_generation_mode_request")
    if not isinstance(request, dict):
        raise ValueError("AI candidate output must include source_generation_mode_request dict.")
    validate_ai_generation_mode_request(request)

    for field_name in (*_CANDIDATE_REQUIRED_TRUE_FIELDS, *_CANDIDATE_REQUIRED_FALSE_FIELDS):
        _require_bool(candidate.get(field_name), field_name=field_name, error_prefix="AI candidate output")

    for field_name in _CANDIDATE_REQUIRED_FALSE_FIELDS:
        if candidate.get(field_name) is not False:
            raise ValueError(f"AI candidate output requires {field_name} to be False.")

    for field_name in (
        "generation_request_id",
        "context_package_id",
        "runtime_request_id",
        "job_family",
        "output_family",
        "generation_mode",
    ):
        if candidate[field_name] != request[field_name]:
            raise ValueError(f"AI candidate output {field_name} must match source_generation_mode_request.")

    if candidate["candidate_output_role"] != request["requested_output_role"]:
        raise ValueError(
            "AI candidate output candidate_output_role must match source_generation_mode_request."
        )

    output_family = _normalize_supported_value(
        candidate["output_family"],
        field_name="output_family",
        supported_values=(*SUPPORTED_DOCUMENT_OUTPUT_FAMILIES, *SUPPORTED_REPORTING_OUTPUT_FAMILIES),
        error_prefix="AI candidate output",
    )
    if candidate["candidate_output_classification"] != _classification_for_output_family(output_family):
        raise ValueError("AI candidate output classification is not aligned with output_family.")

    _normalize_supported_value(
        candidate["generation_mode"],
        field_name="generation_mode",
        supported_values=SUPPORTED_GENERATION_MODES,
        error_prefix="AI candidate output",
    )
    _normalize_supported_value(
        candidate["candidate_evidence_status"],
        field_name="candidate_evidence_status",
        supported_values=(VALIDATED_EVIDENCE_STATUS, PARTIAL_EVIDENCE_STATUS, UNAVAILABLE_EVIDENCE_STATUS),
        error_prefix="AI candidate output",
    )
    _parse_version_pinned_ref(candidate["candidate_output_ref"], field_name="candidate_output_ref")


def build_ai_output_acceptance_decision(
    *,
    acceptance_decision_id: str,
    candidate_output: dict[str, object],
    retry_attempt_number: int = 0,
    max_retry_attempts: int = DEFAULT_MAX_RETRY_ATTEMPTS,
) -> dict[str, object]:
    """Build and validate a deterministic M16.4 acceptance decision."""
    validate_ai_candidate_output(candidate_output)
    retry_attempt_number = _require_non_negative_int(
        retry_attempt_number,
        field_name="retry_attempt_number",
        error_prefix="AI output acceptance decision",
    )
    max_retry_attempts = _require_non_negative_int(
        max_retry_attempts,
        field_name="max_retry_attempts",
        error_prefix="AI output acceptance decision",
    )
    decision = _derive_decision(
        candidate_output=candidate_output,
        retry_attempt_number=retry_attempt_number,
        max_retry_attempts=max_retry_attempts,
    )
    primary_reason = _primary_failure_reason(candidate_output)
    payload = {
        "checkpoint": AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID,
        "contract_version": AI_OUTPUT_ACCEPTANCE_CONTRACT_VERSION,
        "acceptance_decision_id": _require_non_empty_string(
            acceptance_decision_id,
            field_name="acceptance_decision_id",
            error_prefix="AI output acceptance decision",
        ),
        "output_candidate_id": str(candidate_output["output_candidate_id"]),
        "generation_request_id": str(candidate_output["generation_request_id"]),
        "context_package_id": str(candidate_output["context_package_id"]),
        "runtime_request_id": str(candidate_output["runtime_request_id"]),
        "job_family": str(candidate_output["job_family"]),
        "output_family": str(candidate_output["output_family"]),
        "generation_mode": str(candidate_output["generation_mode"]),
        "acceptance_status": AI_OUTPUT_ACCEPTANCE_STATUS_VALIDATED,
        "acceptance_decision": decision,
        "source_candidate_output_status": str(candidate_output["candidate_output_status"]),
        "candidate_evidence_status": str(candidate_output["candidate_evidence_status"]),
        "retry_attempt_number": retry_attempt_number,
        "max_retry_attempts": max_retry_attempts,
        "bounded_retry_reason": primary_reason if decision == RETRY_CANDIDATE_OUTPUT_DECISION else None,
        "fallback_reason": _fallback_reason(
            decision=decision,
            primary_reason=primary_reason,
            candidate_output=candidate_output,
            retry_attempt_number=retry_attempt_number,
            max_retry_attempts=max_retry_attempts,
        ),
        "retry_allowed": decision == RETRY_CANDIDATE_OUTPUT_DECISION,
        "fallback_or_refusal_required": decision == FALLBACK_OR_REFUSE_OUTPUT_DECISION,
        "accepted_for_downstream_review": decision == ACCEPT_CANDIDATE_OUTPUT_DECISION,
        "candidate_output": dict(candidate_output),
        "ai_can_mutate_state": False,
        "ai_can_approve_or_release": False,
        "approval_payload_included": False,
        "workflow_release_payload_included": False,
        "validation_or_uat_truth_claimed": False,
        "bounded_retry_policy": "retry_must_keep_same_generation_mode_and_contract_rules",
        "fallback_policy": "fallback_or_refusal_must_not_create_source_execution_or_approval_truth",
    }
    validate_ai_output_acceptance_decision(payload)
    return payload


def validate_ai_output_acceptance_decision(decision: dict[str, object]) -> None:
    """Validate one M16.4 output acceptance/retry/fallback decision."""
    _validate_prohibited_fields(decision, _PROHIBITED_ACCEPTANCE_FIELDS)
    _validate_required_string_fields(
        decision,
        _DECISION_REQUIRED_STRING_FIELDS,
        error_prefix="AI output acceptance decision",
    )
    _validate_expected_exact_value(
        decision,
        field_name="checkpoint",
        expected_value=AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID,
        error_prefix="AI output acceptance decision",
    )
    _validate_expected_exact_value(
        decision,
        field_name="contract_version",
        expected_value=AI_OUTPUT_ACCEPTANCE_CONTRACT_VERSION,
        error_prefix="AI output acceptance decision",
    )
    _validate_expected_exact_value(
        decision,
        field_name="acceptance_status",
        expected_value=AI_OUTPUT_ACCEPTANCE_STATUS_VALIDATED,
        error_prefix="AI output acceptance decision",
    )
    for field_name in _DECISION_REQUIRED_FALSE_FIELDS:
        if decision.get(field_name) is not False:
            raise ValueError(f"AI output acceptance decision requires {field_name} to be False.")

    candidate = decision.get("candidate_output")
    if not isinstance(candidate, dict):
        raise ValueError("AI output acceptance decision must include candidate_output dict.")
    validate_ai_candidate_output(candidate)

    for field_name in (
        "output_candidate_id",
        "generation_request_id",
        "context_package_id",
        "runtime_request_id",
        "job_family",
        "output_family",
        "generation_mode",
    ):
        if decision[field_name] != candidate[field_name]:
            raise ValueError(f"AI output acceptance decision {field_name} must match candidate_output.")

    retry_attempt_number = _require_non_negative_int(
        decision.get("retry_attempt_number"),
        field_name="retry_attempt_number",
        error_prefix="AI output acceptance decision",
    )
    max_retry_attempts = _require_non_negative_int(
        decision.get("max_retry_attempts"),
        field_name="max_retry_attempts",
        error_prefix="AI output acceptance decision",
    )
    acceptance_decision = _normalize_supported_value(
        decision["acceptance_decision"],
        field_name="acceptance_decision",
        supported_values=SUPPORTED_OUTPUT_ACCEPTANCE_DECISIONS,
        error_prefix="AI output acceptance decision",
    )
    expected_decision = _derive_decision(
        candidate_output=candidate,
        retry_attempt_number=retry_attempt_number,
        max_retry_attempts=max_retry_attempts,
    )
    if acceptance_decision != expected_decision:
        raise ValueError("AI output acceptance decision does not match deterministic acceptance evaluation.")

    _validate_decision_flags(
        decision=decision,
        candidate_output=candidate,
        acceptance_decision=acceptance_decision,
        retry_attempt_number=retry_attempt_number,
        max_retry_attempts=max_retry_attempts,
    )


def _classification_for_output_family(output_family: str) -> str:
    if output_family in SUPPORTED_DOCUMENT_OUTPUT_FAMILIES:
        return CANDIDATE_DOCUMENT_LANGUAGE_OUTPUT_CLASSIFICATION
    if output_family in SUPPORTED_REPORTING_OUTPUT_FAMILIES:
        return CANDIDATE_REPORTING_LANGUAGE_OUTPUT_CLASSIFICATION
    raise ValueError(f"Unsupported AI candidate output_family: {output_family!r}.")


def _candidate_meets_acceptance(candidate_output: dict[str, object]) -> bool:
    if candidate_output.get("candidate_evidence_status") == UNAVAILABLE_EVIDENCE_STATUS:
        return False
    for field_name in _CANDIDATE_REQUIRED_TRUE_FIELDS:
        if candidate_output.get(field_name) is not True:
            return False
    for field_name in _CANDIDATE_REQUIRED_FALSE_FIELDS:
        if candidate_output.get(field_name) is not False:
            return False
    return True


def _primary_failure_reason(candidate_output: dict[str, object]) -> str | None:
    if candidate_output.get("candidate_evidence_status") == UNAVAILABLE_EVIDENCE_STATUS:
        return EVIDENCE_SUPPORT_FAILURE_RETRY_REASON
    if candidate_output.get("content_contract_satisfied") is not True:
        return CONTRACT_RULE_FAILURE_RETRY_REASON
    if candidate_output.get("family_constraints_satisfied") is not True:
        return CONTRACT_RULE_FAILURE_RETRY_REASON
    if candidate_output.get("standards_guardrails_satisfied") is not True:
        return STANDARDS_GUARDRAIL_FAILURE_RETRY_REASON
    if candidate_output.get("evidence_claims_supported") is not True:
        return EVIDENCE_SUPPORT_FAILURE_RETRY_REASON
    if candidate_output.get("assumptions_labeled_when_required") is not True:
        return ASSUMPTION_LABELING_FAILURE_RETRY_REASON
    if candidate_output.get("placeholders_used_for_missing_truth") is not True:
        return PLACEHOLDER_POLICY_FAILURE_RETRY_REASON
    for field_name in (
        "contains_unbounded_invention",
        "contains_unverified_standards_claims",
        "contains_unverified_evidence_claims",
        "contains_execution_truth_claims",
        "requests_state_mutation",
        "approval_requested",
        "release_requested",
    ):
        if candidate_output.get(field_name) is not False:
            return PROHIBITED_OUTPUT_CLAIM_FAILURE_RETRY_REASON
    return None


def _derive_decision(
    *,
    candidate_output: dict[str, object],
    retry_attempt_number: int,
    max_retry_attempts: int,
) -> str:
    if _candidate_meets_acceptance(candidate_output):
        return ACCEPT_CANDIDATE_OUTPUT_DECISION
    if candidate_output.get("candidate_evidence_status") == UNAVAILABLE_EVIDENCE_STATUS:
        return FALLBACK_OR_REFUSE_OUTPUT_DECISION
    if retry_attempt_number >= max_retry_attempts:
        return FALLBACK_OR_REFUSE_OUTPUT_DECISION
    return RETRY_CANDIDATE_OUTPUT_DECISION


def _fallback_reason(
    *,
    decision: str,
    primary_reason: str | None,
    candidate_output: dict[str, object],
    retry_attempt_number: int,
    max_retry_attempts: int,
) -> str | None:
    if decision != FALLBACK_OR_REFUSE_OUTPUT_DECISION:
        return None
    if candidate_output.get("candidate_evidence_status") == UNAVAILABLE_EVIDENCE_STATUS:
        return INSUFFICIENT_EVIDENCE_FALLBACK_REASON
    if primary_reason == PROHIBITED_OUTPUT_CLAIM_FAILURE_RETRY_REASON:
        return FAIL_CLOSED_REQUIRED_FALLBACK_REASON
    if retry_attempt_number >= max_retry_attempts:
        return RETRY_LIMIT_REACHED_FALLBACK_REASON
    return BROKEN_CONTRACT_FALLBACK_REASON


def _validate_decision_flags(
    *,
    decision: dict[str, object],
    candidate_output: dict[str, object],
    acceptance_decision: str,
    retry_attempt_number: int,
    max_retry_attempts: int,
) -> None:
    retry_allowed = _require_bool(
        decision.get("retry_allowed"),
        field_name="retry_allowed",
        error_prefix="AI output acceptance decision",
    )
    fallback_required = _require_bool(
        decision.get("fallback_or_refusal_required"),
        field_name="fallback_or_refusal_required",
        error_prefix="AI output acceptance decision",
    )
    accepted_for_downstream_review = _require_bool(
        decision.get("accepted_for_downstream_review"),
        field_name="accepted_for_downstream_review",
        error_prefix="AI output acceptance decision",
    )
    if acceptance_decision == ACCEPT_CANDIDATE_OUTPUT_DECISION:
        if not _candidate_meets_acceptance(candidate_output):
            raise ValueError("AI output acceptance decision cannot accept failed candidate output.")
        if retry_allowed or fallback_required or not accepted_for_downstream_review:
            raise ValueError("AI output acceptance decision accept state has invalid flags.")
        if decision.get("bounded_retry_reason") is not None or decision.get("fallback_reason") is not None:
            raise ValueError("AI output acceptance decision accept state cannot include retry or fallback reason.")
    if acceptance_decision == RETRY_CANDIDATE_OUTPUT_DECISION:
        if _candidate_meets_acceptance(candidate_output):
            raise ValueError("AI output acceptance decision cannot retry accepted candidate output.")
        if retry_attempt_number >= max_retry_attempts:
            raise ValueError("AI output acceptance decision cannot retry after retry limit.")
        if not retry_allowed or fallback_required or accepted_for_downstream_review:
            raise ValueError("AI output acceptance decision retry state has invalid flags.")
        _normalize_supported_value(
            decision.get("bounded_retry_reason"),
            field_name="bounded_retry_reason",
            supported_values=SUPPORTED_BOUNDED_RETRY_REASONS,
            error_prefix="AI output acceptance decision",
        )
        if decision.get("fallback_reason") is not None:
            raise ValueError("AI output acceptance decision retry state cannot include fallback reason.")
    if acceptance_decision == FALLBACK_OR_REFUSE_OUTPUT_DECISION:
        if _candidate_meets_acceptance(candidate_output):
            raise ValueError("AI output acceptance decision cannot fallback accepted candidate output.")
        if retry_allowed or not fallback_required or accepted_for_downstream_review:
            raise ValueError("AI output acceptance decision fallback state has invalid flags.")
        if decision.get("bounded_retry_reason") is not None:
            raise ValueError("AI output acceptance decision fallback state cannot include retry reason.")
        _normalize_supported_value(
            decision.get("fallback_reason"),
            field_name="fallback_reason",
            supported_values=SUPPORTED_FALLBACK_REASONS,
            error_prefix="AI output acceptance decision",
        )


def _parse_version_pinned_ref(raw_ref: object, *, field_name: str) -> str:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="AI output acceptance ref",
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


def _require_non_negative_int(value: object, *, field_name: str, error_prefix: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{error_prefix} must declare non-negative int {field_name}.")
    return value


def _require_non_empty_string(value: object, *, field_name: str, error_prefix: str) -> str:
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
        _require_non_empty_string(payload.get(field_name), field_name=field_name, error_prefix=error_prefix)


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


def _validate_prohibited_fields(payload: dict[str, object], prohibited_fields: tuple[str, ...]) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(f"{field_name} is not allowed in M16.4 AI output acceptance payloads.")
