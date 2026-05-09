"AI standards-conformance and detail-level consistency checks for M17.3."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

from asbp.document_engine import (
    BOUNDED_INFERENCE_CLASSIFICATION,
    EVIDENCE_SUPPORTED_CLASSIFICATION,
    EXPLICIT_ASSUMPTION_CLASSIFICATION,
    PLACEHOLDER_ONLY_CLASSIFICATION,
    validate_guarded_authoring_output_payload,
)
from .quality_gates import (
    QUALITY_GATE_PASS,
    validate_ai_quality_gate_result,
)

AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID = "M17.3"
AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION = "ai-standards-detail-checks-v1"
AI_STANDARDS_CONFORMANCE_CHECK_STATUS_VALIDATED = (
    "ai_standards_conformance_check_validated"
)
AI_DETAIL_CONSISTENCY_CHECK_STATUS_VALIDATED = "ai_detail_consistency_check_validated"
AI_STANDARDS_DETAIL_CHECK_STATUS_VALIDATED = "ai_standards_detail_check_validated"

STANDARDS_CONFORMANCE_CHECK_PASS = "standards_conformance_check_pass"
STANDARDS_CONFORMANCE_CHECK_FAIL = "standards_conformance_check_fail"
SUPPORTED_STANDARDS_CONFORMANCE_CHECK_RESULTS = (
    STANDARDS_CONFORMANCE_CHECK_PASS,
    STANDARDS_CONFORMANCE_CHECK_FAIL,
)

DETAIL_CONSISTENCY_CHECK_PASS = "detail_consistency_check_pass"
DETAIL_CONSISTENCY_CHECK_FAIL = "detail_consistency_check_fail"
SUPPORTED_DETAIL_CONSISTENCY_CHECK_RESULTS = (
    DETAIL_CONSISTENCY_CHECK_PASS,
    DETAIL_CONSISTENCY_CHECK_FAIL,
)

STANDARDS_DETAIL_CHECK_PASS = "standards_detail_check_pass"
STANDARDS_DETAIL_CHECK_FAIL = "standards_detail_check_fail"
SUPPORTED_STANDARDS_DETAIL_CHECK_RESULTS = (
    STANDARDS_DETAIL_CHECK_PASS,
    STANDARDS_DETAIL_CHECK_FAIL,
)

GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE = "guarded_authoring_payload_invalid"
STANDARDS_REF_NOT_VERSION_PINNED_FAILURE = "standards_ref_not_version_pinned"
SECTION_STANDARD_REF_UNDECLARED_FAILURE = "section_standard_ref_undeclared"
PROHIBITED_LANGUAGE_PATTERN_FAILURE = "prohibited_language_pattern"
DOCUMENT_FAMILY_MISMATCH_FAILURE = "document_family_mismatch"
MISSING_GUARDRAIL_POLICY_FAILURE = "missing_guardrail_policy"
MISSING_SECTIONS_FAILURE = "missing_sections"
MISSING_REQUIRED_SECTION_FAILURE = "missing_required_section"
DISALLOWED_SECTION_FAILURE = "disallowed_section"
DUPLICATE_SECTION_ID_FAILURE = "duplicate_section_id"
EVIDENCE_SUPPORTED_SECTION_MISSING_EVIDENCE_REFS_FAILURE = (
    "evidence_supported_section_missing_evidence_refs"
)
BOUNDED_INFERENCE_SECTION_MISSING_INFERENCE_REFS_FAILURE = (
    "bounded_inference_section_missing_inference_refs"
)
BOUNDED_INFERENCE_SECTION_UNLABELED_ASSUMPTION_FAILURE = (
    "bounded_inference_section_unlabeled_assumption"
)
EXPLICIT_ASSUMPTION_SECTION_UNLABELED_ASSUMPTION_FAILURE = (
    "explicit_assumption_section_unlabeled_assumption"
)
PLACEHOLDER_SECTION_MISSING_EXPLICIT_PLACEHOLDER_FAILURE = (
    "placeholder_section_missing_explicit_placeholder"
)
SOURCE_QUALITY_GATE_NOT_PASS_FAILURE = "source_quality_gate_not_pass"

SUPPORTED_STANDARDS_CONFORMANCE_FAILURE_REASONS = (
    GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE,
    STANDARDS_REF_NOT_VERSION_PINNED_FAILURE,
    SECTION_STANDARD_REF_UNDECLARED_FAILURE,
    PROHIBITED_LANGUAGE_PATTERN_FAILURE,
    DOCUMENT_FAMILY_MISMATCH_FAILURE,
    MISSING_GUARDRAIL_POLICY_FAILURE,
)

SUPPORTED_DETAIL_CONSISTENCY_FAILURE_REASONS = (
    GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE,
    DOCUMENT_FAMILY_MISMATCH_FAILURE,
    MISSING_GUARDRAIL_POLICY_FAILURE,
    MISSING_SECTIONS_FAILURE,
    MISSING_REQUIRED_SECTION_FAILURE,
    DISALLOWED_SECTION_FAILURE,
    DUPLICATE_SECTION_ID_FAILURE,
    EVIDENCE_SUPPORTED_SECTION_MISSING_EVIDENCE_REFS_FAILURE,
    BOUNDED_INFERENCE_SECTION_MISSING_INFERENCE_REFS_FAILURE,
    BOUNDED_INFERENCE_SECTION_UNLABELED_ASSUMPTION_FAILURE,
    EXPLICIT_ASSUMPTION_SECTION_UNLABELED_ASSUMPTION_FAILURE,
    PLACEHOLDER_SECTION_MISSING_EXPLICIT_PLACEHOLDER_FAILURE,
)

SUPPORTED_STANDARDS_DETAIL_FAILURE_REASONS = (
    GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE,
    STANDARDS_REF_NOT_VERSION_PINNED_FAILURE,
    SECTION_STANDARD_REF_UNDECLARED_FAILURE,
    PROHIBITED_LANGUAGE_PATTERN_FAILURE,
    DOCUMENT_FAMILY_MISMATCH_FAILURE,
    MISSING_GUARDRAIL_POLICY_FAILURE,
    MISSING_SECTIONS_FAILURE,
    MISSING_REQUIRED_SECTION_FAILURE,
    DISALLOWED_SECTION_FAILURE,
    DUPLICATE_SECTION_ID_FAILURE,
    EVIDENCE_SUPPORTED_SECTION_MISSING_EVIDENCE_REFS_FAILURE,
    BOUNDED_INFERENCE_SECTION_MISSING_INFERENCE_REFS_FAILURE,
    BOUNDED_INFERENCE_SECTION_UNLABELED_ASSUMPTION_FAILURE,
    EXPLICIT_ASSUMPTION_SECTION_UNLABELED_ASSUMPTION_FAILURE,
    PLACEHOLDER_SECTION_MISSING_EXPLICIT_PLACEHOLDER_FAILURE,
    SOURCE_QUALITY_GATE_NOT_PASS_FAILURE,
)

_PROHIBITED_STANDARDS_DETAIL_FIELDS = (
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
    "retrieval_use_rule",
    "retrieval_use_decision",
    "recommendation_payload",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "source_truth_override",
    "execution_truth_override",
    "validation_truth_override",
)

_STANDARDS_CONFORMANCE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "standards_conformance_check_id",
    "standards_conformance_check_status",
    "document_family",
    "standards_conformance_check_result",
)

_DETAIL_CONSISTENCY_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "detail_consistency_check_id",
    "detail_consistency_check_status",
    "document_family",
    "detail_consistency_check_result",
)

_STANDARDS_DETAIL_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "standards_detail_check_result_id",
    "standards_detail_check_status",
    "document_family",
    "standards_detail_check_result",
    "standards_conformance_check_result",
    "detail_consistency_check_result",
)


def build_ai_standards_detail_checks_baseline() -> dict[str, Any]:
    """Return the M17.3 standards/detail consistency baseline."""
    return {
        "checkpoint": AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
        "contract_version": AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION,
        "supported_standards_conformance_check_results": list(
            SUPPORTED_STANDARDS_CONFORMANCE_CHECK_RESULTS
        ),
        "supported_detail_consistency_check_results": list(
            SUPPORTED_DETAIL_CONSISTENCY_CHECK_RESULTS
        ),
        "supported_standards_detail_check_results": list(
            SUPPORTED_STANDARDS_DETAIL_CHECK_RESULTS
        ),
        "supported_standards_conformance_failure_reasons": list(
            SUPPORTED_STANDARDS_CONFORMANCE_FAILURE_REASONS
        ),
        "supported_detail_consistency_failure_reasons": list(
            SUPPORTED_DETAIL_CONSISTENCY_FAILURE_REASONS
        ),
        "supported_standards_detail_failure_reasons": list(
            SUPPORTED_STANDARDS_DETAIL_FAILURE_REASONS
        ),
        "standards_conformance_policy": (
            "standards_checks_consume_guarded_authoring_payloads_and_verify_"
            "declared_version_pinned_standards_refs_section_ref_declarations_"
            "and_prohibited_language_patterns"
        ),
        "detail_consistency_policy": (
            "detail_checks_consume_guarded_authoring_payloads_and_verify_"
            "family_alignment_section_membership_required_sections_duplicate_"
            "sections_and_evidence_classification_detail_rules"
        ),
        "document_template_boundary_policy": (
            "m17_3_consumes_the_closed_m12_document_engine_boundary_and_must_not_"
            "reopen_document_template_product_implementation"
        ),
        "post_m17_template_reentry_policy": (
            "document_template_product_implementation_is_deferred_to_a_"
            "post_m17_pre_m18_decision_gate"
        ),
        "not_owned_by_m17_3": [
            "actual_llm_calls",
            "prompt_templates",
            "document_template_product_implementation",
            "actual_document_generation_from_expanded_library_content",
            "retrieval_use_governance",
            "recommendation_behavior",
            "ui_api_behavior",
            "workflow_state_mutation",
            "document_approval_or_release",
        ],
    }


def build_standards_conformance_check_result(
    *,
    standards_conformance_check_id: str,
    guarded_authoring_output_payload: dict[str, object],
) -> dict[str, object]:
    """Build and validate one deterministic M17.3 standards conformance check."""
    expected = _evaluate_standards_conformance(guarded_authoring_output_payload)
    result = {
        "checkpoint": AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
        "contract_version": AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION,
        "standards_conformance_check_id": _require_non_empty_string(
            standards_conformance_check_id,
            field_name="standards_conformance_check_id",
            error_prefix="AI standards conformance check",
        ),
        "standards_conformance_check_status": (
            AI_STANDARDS_CONFORMANCE_CHECK_STATUS_VALIDATED
        ),
        "document_family": _document_family_from_guarded_payload(
            guarded_authoring_output_payload
        ),
        "standards_conformance_check_result": expected[
            "standards_conformance_check_result"
        ],
        "standards_conformance_failure_reasons": expected[
            "standards_conformance_failure_reasons"
        ],
        "source_guarded_authoring_output_payload": dict(
            guarded_authoring_output_payload
        ),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_template_implementation_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "recommendation_behavior_in_scope": False,
        "standards_conformance_policy": (
            "standards_conformance_is_checked_from_structured_guarded_"
            "authoring_payload_metadata_not_free_raw_generated_text"
        ),
    }
    validate_standards_conformance_check_result(result)
    return result


def validate_standards_conformance_check_result(result: dict[str, object]) -> None:
    """Validate one deterministic M17.3 standards conformance check."""
    _validate_prohibited_fields(result, _PROHIBITED_STANDARDS_DETAIL_FIELDS)
    _validate_required_string_fields(
        result,
        _STANDARDS_CONFORMANCE_REQUIRED_STRING_FIELDS,
        error_prefix="AI standards conformance check",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
        error_prefix="AI standards conformance check",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION,
        error_prefix="AI standards conformance check",
    )
    _validate_expected_exact_value(
        result,
        field_name="standards_conformance_check_status",
        expected_value=AI_STANDARDS_CONFORMANCE_CHECK_STATUS_VALIDATED,
        error_prefix="AI standards conformance check",
    )
    _validate_required_false_fields(
        result,
        error_prefix="AI standards conformance check",
    )

    payload = _source_guarded_authoring_payload_from_check(
        result,
        error_prefix="AI standards conformance check",
    )
    expected = _evaluate_standards_conformance(payload)
    if result.get("document_family") != _document_family_from_guarded_payload(payload):
        raise ValueError(
            "AI standards conformance check document_family must match source payload."
        )
    if result.get("standards_conformance_check_result") != expected[
        "standards_conformance_check_result"
    ]:
        raise ValueError(
            "AI standards conformance check result does not match deterministic evaluation."
        )
    if result.get("standards_conformance_failure_reasons") != expected[
        "standards_conformance_failure_reasons"
    ]:
        raise ValueError(
            "AI standards conformance failure reasons do not match deterministic evaluation."
        )

    _normalize_supported_value(
        result["standards_conformance_check_result"],
        field_name="standards_conformance_check_result",
        supported_values=SUPPORTED_STANDARDS_CONFORMANCE_CHECK_RESULTS,
        error_prefix="AI standards conformance check",
    )
    _validate_failure_reasons(
        result.get("standards_conformance_failure_reasons"),
        supported_values=SUPPORTED_STANDARDS_CONFORMANCE_FAILURE_REASONS,
        error_prefix="AI standards conformance check",
    )


def build_detail_consistency_check_result(
    *,
    detail_consistency_check_id: str,
    guarded_authoring_output_payload: dict[str, object],
) -> dict[str, object]:
    """Build and validate one deterministic M17.3 detail consistency check."""
    expected = _evaluate_detail_consistency(guarded_authoring_output_payload)
    result = {
        "checkpoint": AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
        "contract_version": AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION,
        "detail_consistency_check_id": _require_non_empty_string(
            detail_consistency_check_id,
            field_name="detail_consistency_check_id",
            error_prefix="AI detail consistency check",
        ),
        "detail_consistency_check_status": AI_DETAIL_CONSISTENCY_CHECK_STATUS_VALIDATED,
        "document_family": _document_family_from_guarded_payload(
            guarded_authoring_output_payload
        ),
        "detail_consistency_check_result": expected[
            "detail_consistency_check_result"
        ],
        "detail_consistency_failure_reasons": expected[
            "detail_consistency_failure_reasons"
        ],
        "source_guarded_authoring_output_payload": dict(
            guarded_authoring_output_payload
        ),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_template_implementation_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "recommendation_behavior_in_scope": False,
        "detail_consistency_policy": (
            "detail_consistency_is_checked_from_structured_section_policy_"
            "metadata_not_free_raw_generated_text"
        ),
    }
    validate_detail_consistency_check_result(result)
    return result


def validate_detail_consistency_check_result(result: dict[str, object]) -> None:
    """Validate one deterministic M17.3 detail consistency check."""
    _validate_prohibited_fields(result, _PROHIBITED_STANDARDS_DETAIL_FIELDS)
    _validate_required_string_fields(
        result,
        _DETAIL_CONSISTENCY_REQUIRED_STRING_FIELDS,
        error_prefix="AI detail consistency check",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
        error_prefix="AI detail consistency check",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION,
        error_prefix="AI detail consistency check",
    )
    _validate_expected_exact_value(
        result,
        field_name="detail_consistency_check_status",
        expected_value=AI_DETAIL_CONSISTENCY_CHECK_STATUS_VALIDATED,
        error_prefix="AI detail consistency check",
    )
    _validate_required_false_fields(
        result,
        error_prefix="AI detail consistency check",
    )

    payload = _source_guarded_authoring_payload_from_check(
        result,
        error_prefix="AI detail consistency check",
    )
    expected = _evaluate_detail_consistency(payload)
    if result.get("document_family") != _document_family_from_guarded_payload(payload):
        raise ValueError(
            "AI detail consistency check document_family must match source payload."
        )
    if result.get("detail_consistency_check_result") != expected[
        "detail_consistency_check_result"
    ]:
        raise ValueError(
            "AI detail consistency check result does not match deterministic evaluation."
        )
    if result.get("detail_consistency_failure_reasons") != expected[
        "detail_consistency_failure_reasons"
    ]:
        raise ValueError(
            "AI detail consistency failure reasons do not match deterministic evaluation."
        )

    _normalize_supported_value(
        result["detail_consistency_check_result"],
        field_name="detail_consistency_check_result",
        supported_values=SUPPORTED_DETAIL_CONSISTENCY_CHECK_RESULTS,
        error_prefix="AI detail consistency check",
    )
    _validate_failure_reasons(
        result.get("detail_consistency_failure_reasons"),
        supported_values=SUPPORTED_DETAIL_CONSISTENCY_FAILURE_REASONS,
        error_prefix="AI detail consistency check",
    )


def build_ai_standards_detail_check_result(
    *,
    standards_detail_check_result_id: str,
    guarded_authoring_output_payload: dict[str, object],
    source_quality_gate_result: dict[str, object] | None = None,
) -> dict[str, object]:
    """Build and validate one deterministic M17.3 combined standards/detail result."""
    standards_check = build_standards_conformance_check_result(
        standards_conformance_check_id=(
            f"{standards_detail_check_result_id}-STANDARDS"
        ),
        guarded_authoring_output_payload=guarded_authoring_output_payload,
    )
    detail_check = build_detail_consistency_check_result(
        detail_consistency_check_id=f"{standards_detail_check_result_id}-DETAIL",
        guarded_authoring_output_payload=guarded_authoring_output_payload,
    )
    quality_gate_failure_reasons = _quality_gate_failure_reasons(
        source_quality_gate_result
    )
    combined_failure_reasons = _deduplicate(
        list(standards_check["standards_conformance_failure_reasons"])
        + list(detail_check["detail_consistency_failure_reasons"])
        + quality_gate_failure_reasons
    )
    combined_result = (
        STANDARDS_DETAIL_CHECK_PASS
        if not combined_failure_reasons
        else STANDARDS_DETAIL_CHECK_FAIL
    )
    result = {
        "checkpoint": AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
        "contract_version": AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION,
        "standards_detail_check_result_id": _require_non_empty_string(
            standards_detail_check_result_id,
            field_name="standards_detail_check_result_id",
            error_prefix="AI standards detail check",
        ),
        "standards_detail_check_status": AI_STANDARDS_DETAIL_CHECK_STATUS_VALIDATED,
        "document_family": _document_family_from_guarded_payload(
            guarded_authoring_output_payload
        ),
        "standards_detail_check_result": combined_result,
        "standards_conformance_check_result": str(
            standards_check["standards_conformance_check_result"]
        ),
        "detail_consistency_check_result": str(
            detail_check["detail_consistency_check_result"]
        ),
        "standards_detail_failure_reasons": combined_failure_reasons,
        "source_standards_conformance_check": standards_check,
        "source_detail_consistency_check": detail_check,
        "source_quality_gate_result_payload": (
            dict(source_quality_gate_result)
            if source_quality_gate_result is not None
            else None
        ),
        "source_guarded_authoring_output_payload": dict(
            guarded_authoring_output_payload
        ),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_template_implementation_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "recommendation_behavior_in_scope": False,
        "standards_detail_policy": (
            "standards_detail_check_pass_requires_standards_conformance_and_"
            "detail_consistency_checks_to_pass"
        ),
    }
    validate_ai_standards_detail_check_result(result)
    return result


def validate_ai_standards_detail_check_result(result: dict[str, object]) -> None:
    """Validate one deterministic M17.3 combined standards/detail result."""
    _validate_prohibited_fields(result, _PROHIBITED_STANDARDS_DETAIL_FIELDS)
    _validate_required_string_fields(
        result,
        _STANDARDS_DETAIL_REQUIRED_STRING_FIELDS,
        error_prefix="AI standards detail check",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
        error_prefix="AI standards detail check",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_STANDARDS_DETAIL_CHECKS_CONTRACT_VERSION,
        error_prefix="AI standards detail check",
    )
    _validate_expected_exact_value(
        result,
        field_name="standards_detail_check_status",
        expected_value=AI_STANDARDS_DETAIL_CHECK_STATUS_VALIDATED,
        error_prefix="AI standards detail check",
    )
    _validate_required_false_fields(
        result,
        error_prefix="AI standards detail check",
    )

    guarded_payload = _source_guarded_authoring_payload_from_check(
        result,
        error_prefix="AI standards detail check",
    )
    standards_check = result.get("source_standards_conformance_check")
    if not isinstance(standards_check, dict):
        raise ValueError(
            "AI standards detail check must include source_standards_conformance_check dict."
        )
    validate_standards_conformance_check_result(standards_check)

    detail_check = result.get("source_detail_consistency_check")
    if not isinstance(detail_check, dict):
        raise ValueError(
            "AI standards detail check must include source_detail_consistency_check dict."
        )
    validate_detail_consistency_check_result(detail_check)

    source_quality_gate_result = result.get("source_quality_gate_result_payload")
    if source_quality_gate_result is not None:
        if not isinstance(source_quality_gate_result, dict):
            raise ValueError(
                "AI standards detail check source_quality_gate_result_payload "
                "must be a dict or None."
            )
        validate_ai_quality_gate_result(source_quality_gate_result)

    expected_standards = _evaluate_standards_conformance(guarded_payload)
    expected_detail = _evaluate_detail_consistency(guarded_payload)
    expected_failure_reasons = _deduplicate(
        list(expected_standards["standards_conformance_failure_reasons"])
        + list(expected_detail["detail_consistency_failure_reasons"])
        + _quality_gate_failure_reasons(source_quality_gate_result)
    )
    expected_result = (
        STANDARDS_DETAIL_CHECK_PASS
        if not expected_failure_reasons
        else STANDARDS_DETAIL_CHECK_FAIL
    )
    expected_standards_result = expected_standards["standards_conformance_check_result"]
    expected_detail_result = expected_detail["detail_consistency_check_result"]

    expectations = {
        "document_family": _document_family_from_guarded_payload(guarded_payload),
        "standards_detail_check_result": expected_result,
        "standards_conformance_check_result": expected_standards_result,
        "detail_consistency_check_result": expected_detail_result,
        "standards_detail_failure_reasons": expected_failure_reasons,
    }
    for field_name, expected_value in expectations.items():
        if result.get(field_name) != expected_value:
            raise ValueError(
                f"AI standards detail check {field_name} does not match deterministic evaluation."
            )

    _normalize_supported_value(
        result["standards_detail_check_result"],
        field_name="standards_detail_check_result",
        supported_values=SUPPORTED_STANDARDS_DETAIL_CHECK_RESULTS,
        error_prefix="AI standards detail check",
    )
    _validate_failure_reasons(
        result.get("standards_detail_failure_reasons"),
        supported_values=SUPPORTED_STANDARDS_DETAIL_FAILURE_REASONS,
        error_prefix="AI standards detail check",
    )


def _evaluate_standards_conformance(
    guarded_payload: dict[str, object],
) -> dict[str, object]:
    failures: list[str] = []
    if _m12_guarded_payload_is_invalid(guarded_payload):
        failures.append(GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE)

    policy = _policy_from_guarded_payload(guarded_payload)
    if not policy:
        failures.append(MISSING_GUARDRAIL_POLICY_FAILURE)

    if _document_family_mismatches(guarded_payload):
        failures.append(DOCUMENT_FAMILY_MISMATCH_FAILURE)

    policy_standards_refs = _string_list(policy.get("standards_refs"))
    for standards_ref in policy_standards_refs:
        if not _is_version_pinned_ref(standards_ref):
            failures.append(STANDARDS_REF_NOT_VERSION_PINNED_FAILURE)

    prohibited_patterns = _string_list(policy.get("prohibited_language_patterns"))
    for section in _sections_from_guarded_payload(guarded_payload):
        section_standards_refs = _string_list(section.get("standards_refs"))
        for standards_ref in section_standards_refs:
            if not _is_version_pinned_ref(standards_ref):
                failures.append(STANDARDS_REF_NOT_VERSION_PINNED_FAILURE)
            if policy_standards_refs and standards_ref not in policy_standards_refs:
                failures.append(SECTION_STANDARD_REF_UNDECLARED_FAILURE)

        content = str(section.get("content", "")).lower()
        for pattern in prohibited_patterns:
            pattern_text = pattern.strip().lower()
            if pattern_text and pattern_text in content:
                failures.append(PROHIBITED_LANGUAGE_PATTERN_FAILURE)

    failures = _deduplicate(failures)
    return {
        "standards_conformance_check_result": (
            STANDARDS_CONFORMANCE_CHECK_PASS
            if not failures
            else STANDARDS_CONFORMANCE_CHECK_FAIL
        ),
        "standards_conformance_failure_reasons": failures,
    }


def _evaluate_detail_consistency(
    guarded_payload: dict[str, object],
) -> dict[str, object]:
    failures: list[str] = []
    if _m12_guarded_payload_is_invalid(guarded_payload):
        failures.append(GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE)

    policy = _policy_from_guarded_payload(guarded_payload)
    if not policy:
        failures.append(MISSING_GUARDRAIL_POLICY_FAILURE)

    if _document_family_mismatches(guarded_payload):
        failures.append(DOCUMENT_FAMILY_MISMATCH_FAILURE)

    sections = _sections_from_guarded_payload(guarded_payload)
    if not sections:
        failures.append(MISSING_SECTIONS_FAILURE)

    structure_rules = policy.get("document_family_structure_rules")
    if not isinstance(structure_rules, dict):
        structure_rules = {}
    allowed_sections = _string_list(structure_rules.get("allowed_sections"))
    required_sections = _string_list(structure_rules.get("required_sections"))

    seen_section_ids: set[str] = set()
    present_section_ids: set[str] = set()
    for section in sections:
        section_id = _string_or_empty(section.get("section_id"))
        if section_id:
            if section_id in seen_section_ids:
                failures.append(DUPLICATE_SECTION_ID_FAILURE)
            seen_section_ids.add(section_id)
            present_section_ids.add(section_id)
        if allowed_sections and section_id not in allowed_sections:
            failures.append(DISALLOWED_SECTION_FAILURE)

        evidence_classification = section.get("evidence_classification")
        evidence_refs = _string_list(section.get("evidence_refs"))
        inference_refs = _string_list(section.get("inference_refs"))
        assumptions = _string_list(section.get("assumptions"))
        placeholders = _string_list(section.get("placeholders"))

        if (
            evidence_classification == EVIDENCE_SUPPORTED_CLASSIFICATION
            and not evidence_refs
        ):
            failures.append(EVIDENCE_SUPPORTED_SECTION_MISSING_EVIDENCE_REFS_FAILURE)
        if evidence_classification == BOUNDED_INFERENCE_CLASSIFICATION:
            if not inference_refs:
                failures.append(
                    BOUNDED_INFERENCE_SECTION_MISSING_INFERENCE_REFS_FAILURE
                )
            if not _all_labeled_assumptions(assumptions):
                failures.append(BOUNDED_INFERENCE_SECTION_UNLABELED_ASSUMPTION_FAILURE)
        if evidence_classification == EXPLICIT_ASSUMPTION_CLASSIFICATION:
            if not _all_labeled_assumptions(assumptions):
                failures.append(EXPLICIT_ASSUMPTION_SECTION_UNLABELED_ASSUMPTION_FAILURE)
        if evidence_classification == PLACEHOLDER_ONLY_CLASSIFICATION:
            if not _all_explicit_placeholders(placeholders):
                failures.append(
                    PLACEHOLDER_SECTION_MISSING_EXPLICIT_PLACEHOLDER_FAILURE
                )

    for required_section in required_sections:
        if required_section not in present_section_ids:
            failures.append(MISSING_REQUIRED_SECTION_FAILURE)

    failures = _deduplicate(failures)
    return {
        "detail_consistency_check_result": (
            DETAIL_CONSISTENCY_CHECK_PASS
            if not failures
            else DETAIL_CONSISTENCY_CHECK_FAIL
        ),
        "detail_consistency_failure_reasons": failures,
    }


def _m12_guarded_payload_is_invalid(guarded_payload: dict[str, object]) -> bool:
    try:
        validate_guarded_authoring_output_payload(guarded_payload)
    except ValueError:
        return True
    return False


def _quality_gate_failure_reasons(
    source_quality_gate_result: dict[str, object] | None,
) -> list[str]:
    if source_quality_gate_result is None:
        return []
    validate_ai_quality_gate_result(source_quality_gate_result)
    if source_quality_gate_result.get("quality_gate_result") == QUALITY_GATE_PASS:
        return []
    return [SOURCE_QUALITY_GATE_NOT_PASS_FAILURE]


def _source_guarded_authoring_payload_from_check(
    check: dict[str, object],
    *,
    error_prefix: str,
) -> dict[str, object]:
    payload = check.get("source_guarded_authoring_output_payload")
    if not isinstance(payload, dict):
        raise ValueError(
            f"{error_prefix} must include source_guarded_authoring_output_payload dict."
        )
    return payload


def _document_family_from_guarded_payload(guarded_payload: dict[str, object]) -> str:
    return _require_non_empty_string(
        guarded_payload.get("document_family"),
        field_name="document_family",
        error_prefix="AI standards/detail source guarded authoring payload",
    )


def _policy_from_guarded_payload(
    guarded_payload: dict[str, object],
) -> dict[str, object]:
    policy = guarded_payload.get("document_family_guardrail_policy")
    if not isinstance(policy, dict):
        return {}
    return policy


def _authoring_snapshot_from_guarded_payload(
    guarded_payload: dict[str, object],
) -> dict[str, object]:
    snapshot = guarded_payload.get("authoring_request_snapshot")
    if not isinstance(snapshot, dict):
        return {}
    return snapshot


def _sections_from_guarded_payload(
    guarded_payload: dict[str, object],
) -> list[dict[str, object]]:
    raw_sections = guarded_payload.get("sections")
    if not isinstance(raw_sections, list):
        return []
    sections: list[dict[str, object]] = []
    for raw_section in raw_sections:
        if isinstance(raw_section, dict):
            sections.append(raw_section)
    return sections


def _document_family_mismatches(guarded_payload: dict[str, object]) -> bool:
    document_family = guarded_payload.get("document_family")
    policy = _policy_from_guarded_payload(guarded_payload)
    snapshot = _authoring_snapshot_from_guarded_payload(guarded_payload)
    if policy and policy.get("document_family") != document_family:
        return True
    if snapshot and snapshot.get("document_family") != document_family:
        return True
    return False


def _is_version_pinned_ref(value: object) -> bool:
    try:
        parse_version_pinned_asset_ref(
            _require_non_empty_string(
                value,
                field_name="standards_ref",
                error_prefix="AI standards/detail ref",
            )
        )
    except ValueError:
        return False
    return True


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    strings: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            strings.append(item.strip())
    return strings


def _string_or_empty(value: object) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return ""


def _all_labeled_assumptions(assumptions: list[str]) -> bool:
    if not assumptions:
        return False
    return all(assumption.startswith("Assumption:") for assumption in assumptions)


def _all_explicit_placeholders(placeholders: list[str]) -> bool:
    if not placeholders:
        return False
    return all(
        placeholder.startswith("(TBD)")
        or placeholder.startswith("TBD:")
        or placeholder.startswith("Placeholder:")
        for placeholder in placeholders
    )


def _validate_required_false_fields(
    result: dict[str, object],
    *,
    error_prefix: str,
) -> None:
    for field_name in (
        "actual_llm_call_required",
        "prompt_template_required",
        "state_mutation_allowed",
        "approval_or_release_allowed",
        "document_template_implementation_in_scope",
        "retrieval_use_governance_in_scope",
        "recommendation_behavior_in_scope",
    ):
        if result.get(field_name) is not False:
            raise ValueError(f"{error_prefix} requires {field_name} to be False.")


def _validate_failure_reasons(
    raw_reasons: object,
    *,
    supported_values: tuple[str, ...],
    error_prefix: str,
) -> None:
    if not isinstance(raw_reasons, list):
        raise ValueError(f"{error_prefix} failure reasons must be a list.")
    normalized = [
        _normalize_supported_value(
            reason,
            field_name="failure_reason",
            supported_values=supported_values,
            error_prefix=error_prefix,
        )
        for reason in raw_reasons
    ]
    if normalized != _deduplicate(normalized):
        raise ValueError(f"{error_prefix} failure reasons must not contain duplicates.")


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


def _deduplicate(values: list[str]) -> list[str]:
    deduplicated: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            deduplicated.append(value)
            seen.add(value)
    return deduplicated


def _deduplicate_tuple(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(_deduplicate(list(values)))


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
                f"{field_name} is not allowed in M17.3 AI standards/detail payloads."
            )
