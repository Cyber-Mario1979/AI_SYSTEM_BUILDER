"AI quality gates and groundedness checks for M17.2."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

from asbp.ai_runtime.context_packaging import (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_ENGINE_INPUT_ROLE,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
    UNAVAILABLE_EVIDENCE_STATUS,
    validate_ai_context_package,
)
from asbp.ai_runtime.output_acceptance import (
    ACCEPT_CANDIDATE_OUTPUT_DECISION,
    validate_ai_candidate_output,
    validate_ai_output_acceptance_decision,
)

AI_QUALITY_GATES_CHECKPOINT_ID = "M17.2"
AI_QUALITY_GATES_CONTRACT_VERSION = "ai-quality-gates-v1"
AI_GROUNDEDNESS_CHECK_STATUS_VALIDATED = "ai_groundedness_check_validated"
AI_QUALITY_GATE_STATUS_VALIDATED = "ai_quality_gate_validated"

GROUNDEDNESS_CHECK_PASS = "groundedness_check_pass"
GROUNDEDNESS_CHECK_FAIL = "groundedness_check_fail"
SUPPORTED_GROUNDEDNESS_CHECK_RESULTS = (
    GROUNDEDNESS_CHECK_PASS,
    GROUNDEDNESS_CHECK_FAIL,
)

EVIDENCE_LINK_CHECK_PASS = "evidence_link_check_pass"
EVIDENCE_LINK_CHECK_FAIL = "evidence_link_check_fail"
SUPPORTED_EVIDENCE_LINK_CHECK_RESULTS = (
    EVIDENCE_LINK_CHECK_PASS,
    EVIDENCE_LINK_CHECK_FAIL,
)

SOURCE_ROLE_CHECK_PASS = "source_role_check_pass"
SOURCE_ROLE_CHECK_FAIL = "source_role_check_fail"
SUPPORTED_SOURCE_ROLE_CHECK_RESULTS = (
    SOURCE_ROLE_CHECK_PASS,
    SOURCE_ROLE_CHECK_FAIL,
)

QUALITY_GATE_PASS = "quality_gate_pass"
QUALITY_GATE_FAIL = "quality_gate_fail"
SUPPORTED_QUALITY_GATE_RESULTS = (
    QUALITY_GATE_PASS,
    QUALITY_GATE_FAIL,
)

SUPPORTED_AUTHORITATIVE_SOURCE_ROLES = (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    GOVERNED_ENGINE_INPUT_ROLE,
    GOVERNED_CONTRACT_ROLE,
)

ACCEPTANCE_DECISION_NOT_ACCEPT_FAILURE = "source_acceptance_decision_not_accept"
UNSUPPORTED_EVIDENCE_CLAIM_FAILURE = "unsupported_evidence_claim"
UNLABELED_ASSUMPTION_FAILURE = "unlabeled_assumption"
MISSING_TRUTH_PLACEHOLDER_FAILURE = "missing_truth_placeholder_not_used"
UNBOUNDED_INVENTION_FAILURE = "unbounded_invention"
UNVERIFIED_STANDARDS_CLAIM_FAILURE = "unverified_standards_claim"
UNVERIFIED_EVIDENCE_CLAIM_FAILURE = "unverified_evidence_claim"
EXECUTION_TRUTH_CLAIM_FAILURE = "execution_truth_claim"
STATE_MUTATION_REQUEST_FAILURE = "state_mutation_request"
APPROVAL_OR_RELEASE_REQUEST_FAILURE = "approval_or_release_request"
EVIDENCE_REF_NOT_IN_CONTEXT_FAILURE = "evidence_ref_not_in_context"
EVIDENCE_REF_NOT_GENERATION_ELIGIBLE_FAILURE = "evidence_ref_not_generation_eligible"
EVIDENCE_REF_UNAVAILABLE_FAILURE = "evidence_ref_unavailable"
SOURCE_REF_NOT_IN_CONTEXT_FAILURE = "source_ref_not_in_context"
NON_AUTHORITATIVE_SOURCE_AS_TRUTH_FAILURE = "non_authoritative_source_used_as_truth"
SOURCE_CAN_DEFINE_EXECUTION_TRUTH_FAILURE = "source_can_define_execution_truth"

SUPPORTED_GROUNDEDNESS_FAILURE_REASONS = (
    ACCEPTANCE_DECISION_NOT_ACCEPT_FAILURE,
    UNSUPPORTED_EVIDENCE_CLAIM_FAILURE,
    UNLABELED_ASSUMPTION_FAILURE,
    MISSING_TRUTH_PLACEHOLDER_FAILURE,
    UNBOUNDED_INVENTION_FAILURE,
    UNVERIFIED_STANDARDS_CLAIM_FAILURE,
    UNVERIFIED_EVIDENCE_CLAIM_FAILURE,
    EXECUTION_TRUTH_CLAIM_FAILURE,
    STATE_MUTATION_REQUEST_FAILURE,
    APPROVAL_OR_RELEASE_REQUEST_FAILURE,
    EVIDENCE_REF_NOT_IN_CONTEXT_FAILURE,
    EVIDENCE_REF_NOT_GENERATION_ELIGIBLE_FAILURE,
    EVIDENCE_REF_UNAVAILABLE_FAILURE,
    SOURCE_REF_NOT_IN_CONTEXT_FAILURE,
    NON_AUTHORITATIVE_SOURCE_AS_TRUTH_FAILURE,
    SOURCE_CAN_DEFINE_EXECUTION_TRUTH_FAILURE,
)

_PROHIBITED_QUALITY_GATE_FIELDS = (
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
    "standards_conformance_score",
    "standards_conformance_check",
    "detail_consistency_score",
    "detail_consistency_check",
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

_GROUNDEDNESS_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "groundedness_check_id",
    "groundedness_check_status",
    "source_acceptance_decision_id",
    "source_output_candidate_id",
    "output_family",
    "generation_mode",
    "groundedness_check_result",
    "evidence_link_check_result",
    "source_role_check_result",
)

_QUALITY_GATE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "quality_gate_result_id",
    "quality_gate_status",
    "source_acceptance_decision_id",
    "source_output_candidate_id",
    "output_family",
    "generation_mode",
    "quality_gate_result",
    "groundedness_check_result",
    "evidence_link_check_result",
    "source_role_check_result",
)


def build_ai_quality_gates_baseline() -> dict[str, Any]:
    """Return the M17.2 quality-gates and groundedness baseline."""
    return {
        "checkpoint": AI_QUALITY_GATES_CHECKPOINT_ID,
        "contract_version": AI_QUALITY_GATES_CONTRACT_VERSION,
        "supported_groundedness_check_results": list(
            SUPPORTED_GROUNDEDNESS_CHECK_RESULTS
        ),
        "supported_evidence_link_check_results": list(
            SUPPORTED_EVIDENCE_LINK_CHECK_RESULTS
        ),
        "supported_source_role_check_results": list(
            SUPPORTED_SOURCE_ROLE_CHECK_RESULTS
        ),
        "supported_quality_gate_results": list(SUPPORTED_QUALITY_GATE_RESULTS),
        "supported_failure_reasons": list(SUPPORTED_GROUNDEDNESS_FAILURE_REASONS),
        "quality_gate_policy": (
            "quality_gate_pass_requires_groundedness_evidence_link_and_"
            "source_role_checks_to_pass"
        ),
        "groundedness_policy": (
            "attractive_language_output_is_not_acceptable_without_supported_"
            "evidence_labeled_assumptions_placeholders_and_source_role_discipline"
        ),
        "document_template_boundary_policy": (
            "m17_2_consumes_the_closed_m12_document_engine_boundary_and_must_not_"
            "reopen_document_template_product_implementation"
        ),
        "post_m17_template_reentry_policy": (
            "document_template_product_implementation_is_deferred_to_a_"
            "post_m17_pre_m18_decision_gate"
        ),
        "not_owned_by_m17_2": [
            "actual_llm_calls",
            "prompt_templates",
            "document_template_product_implementation",
            "actual_document_generation_from_expanded_library_content",
            "standards_conformance_checks",
            "detail_level_consistency_checks",
            "retrieval_use_governance",
            "recommendation_behavior",
            "ui_api_behavior",
            "workflow_state_mutation",
            "document_approval_or_release",
        ],
    }


def build_groundedness_check_result(
    *,
    groundedness_check_id: str,
    source_acceptance_decision: dict[str, object],
    evidence_refs_used: list[str] | None = None,
    source_refs_used_as_truth: list[str] | None = None,
) -> dict[str, object]:
    """Build and validate one deterministic M17.2 groundedness check result."""
    validate_ai_output_acceptance_decision(source_acceptance_decision)
    candidate = _candidate_from_acceptance_decision(source_acceptance_decision)

    evidence_refs = _normalize_ref_list(
        evidence_refs_used
        if evidence_refs_used is not None
        else _generation_eligible_context_refs(candidate),
        field_name="evidence_refs_used",
    )
    truth_refs = _normalize_ref_list(
        source_refs_used_as_truth
        if source_refs_used_as_truth is not None
        else _authoritative_generation_context_refs(candidate),
        field_name="source_refs_used_as_truth",
    )
    expected = _evaluate_groundedness(
        source_acceptance_decision=source_acceptance_decision,
        evidence_refs_used=evidence_refs,
        source_refs_used_as_truth=truth_refs,
    )

    result = {
        "checkpoint": AI_QUALITY_GATES_CHECKPOINT_ID,
        "contract_version": AI_QUALITY_GATES_CONTRACT_VERSION,
        "groundedness_check_id": _require_non_empty_string(
            groundedness_check_id,
            field_name="groundedness_check_id",
            error_prefix="AI groundedness check",
        ),
        "groundedness_check_status": AI_GROUNDEDNESS_CHECK_STATUS_VALIDATED,
        "source_acceptance_decision_id": str(
            source_acceptance_decision["acceptance_decision_id"]
        ),
        "source_output_candidate_id": str(
            source_acceptance_decision["output_candidate_id"]
        ),
        "output_family": str(source_acceptance_decision["output_family"]),
        "generation_mode": str(source_acceptance_decision["generation_mode"]),
        "evidence_refs_used": evidence_refs,
        "source_refs_used_as_truth": truth_refs,
        "groundedness_check_result": expected["groundedness_check_result"],
        "evidence_link_check_result": expected["evidence_link_check_result"],
        "source_role_check_result": expected["source_role_check_result"],
        "failure_reasons": expected["failure_reasons"],
        "source_acceptance_decision_payload": dict(source_acceptance_decision),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_template_implementation_in_scope": False,
        "standards_conformance_in_scope": False,
        "detail_consistency_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "measurement_policy": (
            "m17_2_groundedness_checks_metadata_and_source_role_discipline_only"
        ),
    }
    validate_groundedness_check_result(result)
    return result


def validate_groundedness_check_result(result: dict[str, object]) -> None:
    """Validate one deterministic M17.2 groundedness check result."""
    _validate_prohibited_fields(result, _PROHIBITED_QUALITY_GATE_FIELDS)
    _validate_required_string_fields(
        result,
        _GROUNDEDNESS_REQUIRED_STRING_FIELDS,
        error_prefix="AI groundedness check",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_QUALITY_GATES_CHECKPOINT_ID,
        error_prefix="AI groundedness check",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_QUALITY_GATES_CONTRACT_VERSION,
        error_prefix="AI groundedness check",
    )
    _validate_expected_exact_value(
        result,
        field_name="groundedness_check_status",
        expected_value=AI_GROUNDEDNESS_CHECK_STATUS_VALIDATED,
        error_prefix="AI groundedness check",
    )

    for field_name in (
        "actual_llm_call_required",
        "prompt_template_required",
        "state_mutation_allowed",
        "approval_or_release_allowed",
        "document_template_implementation_in_scope",
        "standards_conformance_in_scope",
        "detail_consistency_in_scope",
        "retrieval_use_governance_in_scope",
    ):
        if result.get(field_name) is not False:
            raise ValueError(f"AI groundedness check requires {field_name} to be False.")

    decision = result.get("source_acceptance_decision_payload")
    if not isinstance(decision, dict):
        raise ValueError(
            "AI groundedness check must include source_acceptance_decision_payload dict."
        )
    validate_ai_output_acceptance_decision(decision)

    if result["source_acceptance_decision_id"] != decision["acceptance_decision_id"]:
        raise ValueError(
            "AI groundedness check source_acceptance_decision_id must match payload."
        )
    if result["source_output_candidate_id"] != decision["output_candidate_id"]:
        raise ValueError(
            "AI groundedness check source_output_candidate_id must match payload."
        )
    if result["output_family"] != decision["output_family"]:
        raise ValueError("AI groundedness check output_family must match payload.")
    if result["generation_mode"] != decision["generation_mode"]:
        raise ValueError("AI groundedness check generation_mode must match payload.")

    evidence_refs = _normalize_ref_list(
        result.get("evidence_refs_used"),
        field_name="evidence_refs_used",
    )
    truth_refs = _normalize_ref_list(
        result.get("source_refs_used_as_truth"),
        field_name="source_refs_used_as_truth",
    )
    expected = _evaluate_groundedness(
        source_acceptance_decision=decision,
        evidence_refs_used=evidence_refs,
        source_refs_used_as_truth=truth_refs,
    )
    for field_name in (
        "groundedness_check_result",
        "evidence_link_check_result",
        "source_role_check_result",
        "failure_reasons",
    ):
        if result.get(field_name) != expected[field_name]:
            raise ValueError(
                f"AI groundedness check {field_name} does not match deterministic evaluation."
            )

    _normalize_supported_value(
        result["groundedness_check_result"],
        field_name="groundedness_check_result",
        supported_values=SUPPORTED_GROUNDEDNESS_CHECK_RESULTS,
        error_prefix="AI groundedness check",
    )
    _normalize_supported_value(
        result["evidence_link_check_result"],
        field_name="evidence_link_check_result",
        supported_values=SUPPORTED_EVIDENCE_LINK_CHECK_RESULTS,
        error_prefix="AI groundedness check",
    )
    _normalize_supported_value(
        result["source_role_check_result"],
        field_name="source_role_check_result",
        supported_values=SUPPORTED_SOURCE_ROLE_CHECK_RESULTS,
        error_prefix="AI groundedness check",
    )
    _validate_failure_reasons(result.get("failure_reasons"))


def build_ai_quality_gate_result(
    *,
    quality_gate_result_id: str,
    source_acceptance_decision: dict[str, object],
    evidence_refs_used: list[str] | None = None,
    source_refs_used_as_truth: list[str] | None = None,
) -> dict[str, object]:
    """Build and validate one deterministic M17.2 quality-gate result."""
    groundedness_check = build_groundedness_check_result(
        groundedness_check_id=f"{quality_gate_result_id}-GROUNDEDNESS",
        source_acceptance_decision=source_acceptance_decision,
        evidence_refs_used=evidence_refs_used,
        source_refs_used_as_truth=source_refs_used_as_truth,
    )
    groundedness_failure_reasons = _failure_reasons_from_groundedness_check(
        groundedness_check
    )
    quality_gate_result = (
        QUALITY_GATE_PASS
        if (
            groundedness_check["groundedness_check_result"]
            == GROUNDEDNESS_CHECK_PASS
            and groundedness_check["evidence_link_check_result"]
            == EVIDENCE_LINK_CHECK_PASS
            and groundedness_check["source_role_check_result"]
            == SOURCE_ROLE_CHECK_PASS
        )
        else QUALITY_GATE_FAIL
    )

    result = {
        "checkpoint": AI_QUALITY_GATES_CHECKPOINT_ID,
        "contract_version": AI_QUALITY_GATES_CONTRACT_VERSION,
        "quality_gate_result_id": _require_non_empty_string(
            quality_gate_result_id,
            field_name="quality_gate_result_id",
            error_prefix="AI quality gate",
        ),
        "quality_gate_status": AI_QUALITY_GATE_STATUS_VALIDATED,
        "source_acceptance_decision_id": str(
            source_acceptance_decision["acceptance_decision_id"]
        ),
        "source_output_candidate_id": str(
            source_acceptance_decision["output_candidate_id"]
        ),
        "output_family": str(source_acceptance_decision["output_family"]),
        "generation_mode": str(source_acceptance_decision["generation_mode"]),
        "quality_gate_result": quality_gate_result,
        "groundedness_check_result": str(
            groundedness_check["groundedness_check_result"]
        ),
        "evidence_link_check_result": str(
            groundedness_check["evidence_link_check_result"]
        ),
        "source_role_check_result": str(groundedness_check["source_role_check_result"]),
        "quality_gate_failure_reasons": groundedness_failure_reasons,
        "source_groundedness_check": groundedness_check,
        "source_acceptance_decision_payload": dict(source_acceptance_decision),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_template_implementation_in_scope": False,
        "standards_conformance_in_scope": False,
        "detail_consistency_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "quality_gate_policy": (
            "quality_gate_pass_requires_groundedness_evidence_link_and_"
            "source_role_checks_to_pass"
        ),
    }
    validate_ai_quality_gate_result(result)
    return result


def validate_ai_quality_gate_result(result: dict[str, object]) -> None:
    """Validate one deterministic M17.2 quality-gate result."""
    _validate_prohibited_fields(result, _PROHIBITED_QUALITY_GATE_FIELDS)
    _validate_required_string_fields(
        result,
        _QUALITY_GATE_REQUIRED_STRING_FIELDS,
        error_prefix="AI quality gate",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_QUALITY_GATES_CHECKPOINT_ID,
        error_prefix="AI quality gate",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_QUALITY_GATES_CONTRACT_VERSION,
        error_prefix="AI quality gate",
    )
    _validate_expected_exact_value(
        result,
        field_name="quality_gate_status",
        expected_value=AI_QUALITY_GATE_STATUS_VALIDATED,
        error_prefix="AI quality gate",
    )

    for field_name in (
        "actual_llm_call_required",
        "prompt_template_required",
        "state_mutation_allowed",
        "approval_or_release_allowed",
        "document_template_implementation_in_scope",
        "standards_conformance_in_scope",
        "detail_consistency_in_scope",
        "retrieval_use_governance_in_scope",
    ):
        if result.get(field_name) is not False:
            raise ValueError(f"AI quality gate requires {field_name} to be False.")

    decision = result.get("source_acceptance_decision_payload")
    if not isinstance(decision, dict):
        raise ValueError(
            "AI quality gate must include source_acceptance_decision_payload dict."
        )
    validate_ai_output_acceptance_decision(decision)

    groundedness_check = result.get("source_groundedness_check")
    if not isinstance(groundedness_check, dict):
        raise ValueError("AI quality gate must include source_groundedness_check dict.")
    validate_groundedness_check_result(groundedness_check)

    for result_field, decision_field in (
        ("source_acceptance_decision_id", "acceptance_decision_id"),
        ("source_output_candidate_id", "output_candidate_id"),
        ("output_family", "output_family"),
        ("generation_mode", "generation_mode"),
    ):
        if result[result_field] != decision[decision_field]:
            raise ValueError(f"AI quality gate {result_field} must match payload.")

    for result_field in (
        "groundedness_check_result",
        "evidence_link_check_result",
        "source_role_check_result",
    ):
        if result[result_field] != groundedness_check[result_field]:
            raise ValueError(
                f"AI quality gate {result_field} must match source_groundedness_check."
            )

    expected_result = (
        QUALITY_GATE_PASS
        if (
            groundedness_check["groundedness_check_result"]
            == GROUNDEDNESS_CHECK_PASS
            and groundedness_check["evidence_link_check_result"]
            == EVIDENCE_LINK_CHECK_PASS
            and groundedness_check["source_role_check_result"]
            == SOURCE_ROLE_CHECK_PASS
        )
        else QUALITY_GATE_FAIL
    )
    if result["quality_gate_result"] != expected_result:
        raise ValueError(
            "AI quality gate quality_gate_result does not match deterministic evaluation."
        )

    groundedness_failure_reasons = _failure_reasons_from_groundedness_check(
        groundedness_check
    )
    if result.get("quality_gate_failure_reasons") != groundedness_failure_reasons:
        raise ValueError(
            "AI quality gate quality_gate_failure_reasons must match groundedness failure reasons."
        )

    _normalize_supported_value(
        result["quality_gate_result"],
        field_name="quality_gate_result",
        supported_values=SUPPORTED_QUALITY_GATE_RESULTS,
        error_prefix="AI quality gate",
    )
    _validate_failure_reasons(result.get("quality_gate_failure_reasons"))


def _failure_reasons_from_groundedness_check(
    groundedness_check: dict[str, object]
) -> list[str]:
    raw_reasons = groundedness_check.get("failure_reasons")
    if not isinstance(raw_reasons, list):
        raise ValueError(
            "AI quality gate source_groundedness_check must expose list failure_reasons."
        )
    reasons = [
        _normalize_supported_value(
            reason,
            field_name="failure_reason",
            supported_values=SUPPORTED_GROUNDEDNESS_FAILURE_REASONS,
            error_prefix="AI quality gate",
        )
        for reason in raw_reasons
    ]
    return _deduplicate(reasons)


def _evaluate_groundedness(
    *,
    source_acceptance_decision: dict[str, object],
    evidence_refs_used: list[str],
    source_refs_used_as_truth: list[str],
) -> dict[str, object]:
    candidate = _candidate_from_acceptance_decision(source_acceptance_decision)
    failures: list[str] = []

    if (
        source_acceptance_decision.get("acceptance_decision")
        != ACCEPT_CANDIDATE_OUTPUT_DECISION
    ):
        failures.append(ACCEPTANCE_DECISION_NOT_ACCEPT_FAILURE)
    if candidate.get("candidate_evidence_status") == UNAVAILABLE_EVIDENCE_STATUS:
        failures.append(EVIDENCE_REF_UNAVAILABLE_FAILURE)
    if candidate.get("evidence_claims_supported") is not True:
        failures.append(UNSUPPORTED_EVIDENCE_CLAIM_FAILURE)
    if candidate.get("assumptions_labeled_when_required") is not True:
        failures.append(UNLABELED_ASSUMPTION_FAILURE)
    if candidate.get("placeholders_used_for_missing_truth") is not True:
        failures.append(MISSING_TRUTH_PLACEHOLDER_FAILURE)
    if candidate.get("contains_unbounded_invention") is not False:
        failures.append(UNBOUNDED_INVENTION_FAILURE)
    if candidate.get("contains_unverified_standards_claims") is not False:
        failures.append(UNVERIFIED_STANDARDS_CLAIM_FAILURE)
    if candidate.get("contains_unverified_evidence_claims") is not False:
        failures.append(UNVERIFIED_EVIDENCE_CLAIM_FAILURE)
    if candidate.get("contains_execution_truth_claims") is not False:
        failures.append(EXECUTION_TRUTH_CLAIM_FAILURE)
    if candidate.get("requests_state_mutation") is not False:
        failures.append(STATE_MUTATION_REQUEST_FAILURE)
    if (
        candidate.get("approval_requested") is not False
        or candidate.get("release_requested") is not False
    ):
        failures.append(APPROVAL_OR_RELEASE_REQUEST_FAILURE)

    evidence_failures = _evaluate_evidence_links(
        candidate=candidate,
        evidence_refs_used=evidence_refs_used,
    )
    source_role_failures = _evaluate_source_roles(
        candidate=candidate,
        source_refs_used_as_truth=source_refs_used_as_truth,
    )
    failures.extend(evidence_failures)
    failures.extend(source_role_failures)
    failures = _deduplicate(failures)

    return {
        "groundedness_check_result": (
            GROUNDEDNESS_CHECK_PASS if not failures else GROUNDEDNESS_CHECK_FAIL
        ),
        "evidence_link_check_result": (
            EVIDENCE_LINK_CHECK_PASS
            if not evidence_failures
            else EVIDENCE_LINK_CHECK_FAIL
        ),
        "source_role_check_result": (
            SOURCE_ROLE_CHECK_PASS
            if not source_role_failures
            else SOURCE_ROLE_CHECK_FAIL
        ),
        "failure_reasons": failures,
    }


def _evaluate_evidence_links(
    *,
    candidate: dict[str, object],
    evidence_refs_used: list[str],
) -> list[str]:
    failures: list[str] = []
    if candidate.get("candidate_evidence_status") == UNAVAILABLE_EVIDENCE_STATUS:
        failures.append(EVIDENCE_REF_UNAVAILABLE_FAILURE)

    items_by_ref = _context_items_by_ref(candidate)
    for ref in evidence_refs_used:
        item = items_by_ref.get(ref)
        if item is None:
            failures.append(EVIDENCE_REF_NOT_IN_CONTEXT_FAILURE)
            continue
        if item.get("may_be_used_for_generation") is not True:
            failures.append(EVIDENCE_REF_NOT_GENERATION_ELIGIBLE_FAILURE)
        if item.get("evidence_status") == UNAVAILABLE_EVIDENCE_STATUS:
            failures.append(EVIDENCE_REF_UNAVAILABLE_FAILURE)
    return _deduplicate(failures)


def _evaluate_source_roles(
    *,
    candidate: dict[str, object],
    source_refs_used_as_truth: list[str],
) -> list[str]:
    items_by_ref = _context_items_by_ref(candidate)
    failures: list[str] = []
    for ref in source_refs_used_as_truth:
        item = items_by_ref.get(ref)
        if item is None:
            failures.append(SOURCE_REF_NOT_IN_CONTEXT_FAILURE)
            continue
        if (
            item.get("source_role") == NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE
            or item.get("is_authoritative") is not True
            or item.get("source_role") not in SUPPORTED_AUTHORITATIVE_SOURCE_ROLES
        ):
            failures.append(NON_AUTHORITATIVE_SOURCE_AS_TRUTH_FAILURE)
        if item.get("may_define_execution_truth") is not False:
            failures.append(SOURCE_CAN_DEFINE_EXECUTION_TRUTH_FAILURE)
    return _deduplicate(failures)


def _candidate_from_acceptance_decision(
    source_acceptance_decision: dict[str, object]
) -> dict[str, object]:
    validate_ai_output_acceptance_decision(source_acceptance_decision)
    candidate = source_acceptance_decision.get("candidate_output")
    if not isinstance(candidate, dict):
        raise ValueError("AI quality gates require source candidate_output dict.")
    validate_ai_candidate_output(candidate)
    return candidate


def _context_package_from_candidate(candidate: dict[str, object]) -> dict[str, object]:
    request = candidate.get("source_generation_mode_request")
    if not isinstance(request, dict):
        raise ValueError("AI quality gates require source_generation_mode_request dict.")
    context_package = request.get("source_context_package")
    if not isinstance(context_package, dict):
        raise ValueError("AI quality gates require source_context_package dict.")
    validate_ai_context_package(context_package)
    return context_package


def _context_items_by_ref(candidate: dict[str, object]) -> dict[str, dict[str, object]]:
    context_package = _context_package_from_candidate(candidate)
    raw_items = context_package.get("context_items")
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("AI quality gates require non-empty context_items.")

    items_by_ref: dict[str, dict[str, object]] = {}
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            raise ValueError("AI quality gate context_items must contain dicts.")
        ref = _parse_version_pinned_ref(raw_item.get("source_ref"), field_name="source_ref")
        items_by_ref[ref] = raw_item
    return items_by_ref


def _generation_eligible_context_refs(candidate: dict[str, object]) -> list[str]:
    refs: list[str] = []
    for ref, item in _context_items_by_ref(candidate).items():
        if item.get("may_be_used_for_generation") is True:
            refs.append(ref)
    if not refs:
        raise ValueError("AI quality gates require generation-eligible evidence refs.")
    return sorted(refs)


def _authoritative_generation_context_refs(candidate: dict[str, object]) -> list[str]:
    refs: list[str] = []
    for ref, item in _context_items_by_ref(candidate).items():
        if (
            item.get("may_be_used_for_generation") is True
            and item.get("is_authoritative") is True
            and item.get("source_role") in SUPPORTED_AUTHORITATIVE_SOURCE_ROLES
        ):
            refs.append(ref)
    if not refs:
        raise ValueError("AI quality gates require authoritative source refs.")
    return sorted(refs)


def _normalize_ref_list(value: object, *, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"AI quality gates require non-empty list {field_name}.")
    refs = [
        _parse_version_pinned_ref(raw_ref, field_name=field_name)
        for raw_ref in value
    ]
    return sorted(_deduplicate(refs))


def _parse_version_pinned_ref(raw_ref: object, *, field_name: str) -> str:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="AI quality gates ref",
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


def _validate_failure_reasons(raw_reasons: object) -> None:
    if not isinstance(raw_reasons, list):
        raise ValueError("AI quality gates failure_reasons must be a list.")
    normalized = [
        _normalize_supported_value(
            reason,
            field_name="failure_reason",
            supported_values=SUPPORTED_GROUNDEDNESS_FAILURE_REASONS,
            error_prefix="AI quality gates",
        )
        for reason in raw_reasons
    ]
    if normalized != _deduplicate(normalized):
        raise ValueError("AI quality gates failure_reasons must not contain duplicates.")


def _deduplicate(values: list[str]) -> list[str]:
    deduplicated: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            deduplicated.append(value)
            seen.add(value)
    return deduplicated


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
                f"{field_name} is not allowed in M17.2 AI quality-gate payloads."
            )