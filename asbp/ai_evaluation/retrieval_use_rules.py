"AI retrieval-use rules and source-role discipline for M17.4."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.retrieval_boundary import (
    GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
    GOVERNED_RETRIEVAL_ROLE,
    SUPPORT_RETRIEVAL_MODE,
    SUPPORT_RETRIEVAL_ROLE,
    validate_retrieval_boundary_request,
)

AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID = "M17.4"
AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION = "ai-retrieval-use-rules-v1"
AI_RETRIEVAL_USE_CHECK_STATUS_VALIDATED = "ai_retrieval_use_check_validated"
AI_SOURCE_ROLE_DISCIPLINE_CHECK_STATUS_VALIDATED = (
    "ai_source_role_discipline_check_validated"
)
AI_RETRIEVAL_USE_RULE_STATUS_VALIDATED = "ai_retrieval_use_rule_validated"

RETRIEVAL_USE_CHECK_PASS = "retrieval_use_check_pass"
RETRIEVAL_USE_CHECK_FAIL = "retrieval_use_check_fail"
SUPPORTED_RETRIEVAL_USE_CHECK_RESULTS = (
    RETRIEVAL_USE_CHECK_PASS,
    RETRIEVAL_USE_CHECK_FAIL,
)

SOURCE_ROLE_DISCIPLINE_CHECK_PASS = "source_role_discipline_check_pass"
SOURCE_ROLE_DISCIPLINE_CHECK_FAIL = "source_role_discipline_check_fail"
SUPPORTED_SOURCE_ROLE_DISCIPLINE_CHECK_RESULTS = (
    SOURCE_ROLE_DISCIPLINE_CHECK_PASS,
    SOURCE_ROLE_DISCIPLINE_CHECK_FAIL,
)

RETRIEVAL_USE_RULE_PASS = "retrieval_use_rule_pass"
RETRIEVAL_USE_RULE_FAIL = "retrieval_use_rule_fail"
SUPPORTED_RETRIEVAL_USE_RULE_RESULTS = (
    RETRIEVAL_USE_RULE_PASS,
    RETRIEVAL_USE_RULE_FAIL,
)

UNSUPPORTED_RETRIEVAL_MODE_FAILURE = "unsupported_retrieval_mode"
GOVERNED_RETRIEVAL_VALIDATION_FAILURE = "governed_retrieval_validation_failure"
SUPPORT_RETRIEVAL_VALIDATION_FAILURE = "support_retrieval_validation_failure"
SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE = "support_retrieval_as_source_truth"
SUPPORT_RETRIEVAL_EXECUTION_TRUTH_FAILURE = "support_retrieval_as_execution_truth"
SUPPORT_RETRIEVAL_COMPILED_AUTHORITY_FAILURE = (
    "support_retrieval_as_compiled_lookup_authority"
)
SUPPORT_RETRIEVAL_GOVERNED_EVIDENCE_FAILURE = (
    "support_retrieval_as_governed_evidence"
)
MIXED_GOVERNED_SUPPORT_AUTHORITY_FAILURE = "mixed_governed_support_authority"
RESOLVER_BYPASS_FAILURE = "resolver_bypass"
SOURCE_TRUTH_OVERRIDE_FAILURE = "source_truth_override"
EXECUTION_TRUTH_OVERRIDE_FAILURE = "execution_truth_override"
ASSET_PAYLOAD_INCLUDED_FAILURE = "asset_payload_included"
STATE_MUTATION_REQUEST_FAILURE = "retrieval_payload_requests_state_mutation"
APPROVAL_OR_RELEASE_REQUEST_FAILURE = "retrieval_payload_requests_approval_or_release"
DOCUMENT_GENERATION_REQUEST_FAILURE = "retrieval_payload_requests_document_generation"
DOCUMENT_TEMPLATE_IMPLEMENTATION_REQUEST_FAILURE = (
    "retrieval_payload_requests_document_template_implementation"
)

SUPPORTED_RETRIEVAL_USE_FAILURE_REASONS = (
    UNSUPPORTED_RETRIEVAL_MODE_FAILURE,
    GOVERNED_RETRIEVAL_VALIDATION_FAILURE,
    SUPPORT_RETRIEVAL_VALIDATION_FAILURE,
    RESOLVER_BYPASS_FAILURE,
    SOURCE_TRUTH_OVERRIDE_FAILURE,
    EXECUTION_TRUTH_OVERRIDE_FAILURE,
    ASSET_PAYLOAD_INCLUDED_FAILURE,
    STATE_MUTATION_REQUEST_FAILURE,
    APPROVAL_OR_RELEASE_REQUEST_FAILURE,
    DOCUMENT_GENERATION_REQUEST_FAILURE,
    DOCUMENT_TEMPLATE_IMPLEMENTATION_REQUEST_FAILURE,
)

SUPPORTED_SOURCE_ROLE_DISCIPLINE_FAILURE_REASONS = (
    SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE,
    SUPPORT_RETRIEVAL_EXECUTION_TRUTH_FAILURE,
    SUPPORT_RETRIEVAL_COMPILED_AUTHORITY_FAILURE,
    SUPPORT_RETRIEVAL_GOVERNED_EVIDENCE_FAILURE,
    MIXED_GOVERNED_SUPPORT_AUTHORITY_FAILURE,
)

SUPPORTED_RETRIEVAL_USE_RULE_FAILURE_REASONS = (
    *SUPPORTED_RETRIEVAL_USE_FAILURE_REASONS,
    *SUPPORTED_SOURCE_ROLE_DISCIPLINE_FAILURE_REASONS,
)

_USAGE_FLAG_FIELDS = (
    "support_retrieval_used_as_source_truth",
    "support_retrieval_used_as_execution_truth",
    "support_retrieval_used_as_compiled_lookup_authority",
    "support_retrieval_used_as_governed_evidence",
    "mixed_governed_support_authority",
    "requests_state_mutation",
    "approval_requested",
    "release_requested",
    "document_generation_requested",
    "document_template_implementation_requested",
)

_RETRIEVAL_USE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "retrieval_use_check_id",
    "retrieval_use_check_status",
    "retrieval_use_check_result",
)

_SOURCE_ROLE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "source_role_discipline_check_id",
    "source_role_discipline_check_status",
    "source_role_discipline_check_result",
)

_RETRIEVAL_RULE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "retrieval_use_rule_result_id",
    "retrieval_use_rule_status",
    "retrieval_use_rule_result",
    "retrieval_use_check_result",
    "source_role_discipline_check_result",
)

_PROHIBITED_RETRIEVAL_RULE_FIELDS = (
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
    "generated_output_payload",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "document_generation_payload",
    "document_template_implementation_payload",
    "source_truth_override_payload",
    "execution_truth_override_payload",
    "validation_truth_override",
)


def build_ai_retrieval_use_rules_baseline() -> dict[str, Any]:
    """Return the M17.4 retrieval-use and source-role baseline."""
    return {
        "checkpoint": AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
        "contract_version": AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION,
        "supported_retrieval_use_check_results": list(
            SUPPORTED_RETRIEVAL_USE_CHECK_RESULTS
        ),
        "supported_source_role_discipline_check_results": list(
            SUPPORTED_SOURCE_ROLE_DISCIPLINE_CHECK_RESULTS
        ),
        "supported_retrieval_use_rule_results": list(
            SUPPORTED_RETRIEVAL_USE_RULE_RESULTS
        ),
        "supported_retrieval_use_failure_reasons": list(
            SUPPORTED_RETRIEVAL_USE_FAILURE_REASONS
        ),
        "supported_source_role_discipline_failure_reasons": list(
            SUPPORTED_SOURCE_ROLE_DISCIPLINE_FAILURE_REASONS
        ),
        "retrieval_use_policy": (
            "ai_may_consume_governed_retrieval_only_with_governed_role_"
            "discipline_and_support_retrieval_only_as_non_authoritative_context"
        ),
        "source_role_policy": (
            "support_retrieval_must_not_be_promoted_to_source_truth_execution_"
            "truth_compiled_lookup_authority_or_governed_evidence"
        ),
        "m14_5_boundary_policy": (
            "m17_4_consumes_the_closed_m14_5_governed_retrieval_support_"
            "retrieval_boundary"
        ),
        "post_m17_template_reentry_policy": (
            "document_template_product_implementation_remains_deferred_to_a_"
            "post_m17_pre_m18_decision_gate"
        ),
        "not_owned_by_m17_4": [
            "real_vector_search",
            "embedding_generation",
            "external_web_search",
            "asset_payload_loading",
            "document_generation",
            "document_template_product_implementation",
            "standards_conformance_checks",
            "detail_level_consistency_checks",
            "recommendation_behavior",
            "ui_api_behavior",
            "workflow_state_mutation",
            "document_approval_or_release",
        ],
    }


def build_retrieval_use_check_result(
    *,
    retrieval_use_check_id: str,
    retrieval_requests: list[dict[str, object]],
    support_retrieval_used_as_source_truth: bool = False,
    support_retrieval_used_as_execution_truth: bool = False,
    support_retrieval_used_as_compiled_lookup_authority: bool = False,
    support_retrieval_used_as_governed_evidence: bool = False,
    mixed_governed_support_authority: bool = False,
    requests_state_mutation: bool = False,
    approval_requested: bool = False,
    release_requested: bool = False,
    document_generation_requested: bool = False,
    document_template_implementation_requested: bool = False,
) -> dict[str, object]:
    """Build and validate an M17.4 retrieval-use check result."""
    requests = _normalize_retrieval_requests(retrieval_requests)
    usage_flags = _build_usage_flags(
        support_retrieval_used_as_source_truth=support_retrieval_used_as_source_truth,
        support_retrieval_used_as_execution_truth=support_retrieval_used_as_execution_truth,
        support_retrieval_used_as_compiled_lookup_authority=(
            support_retrieval_used_as_compiled_lookup_authority
        ),
        support_retrieval_used_as_governed_evidence=(
            support_retrieval_used_as_governed_evidence
        ),
        mixed_governed_support_authority=mixed_governed_support_authority,
        requests_state_mutation=requests_state_mutation,
        approval_requested=approval_requested,
        release_requested=release_requested,
        document_generation_requested=document_generation_requested,
        document_template_implementation_requested=(
            document_template_implementation_requested
        ),
    )
    expected = _evaluate_retrieval_use(
        retrieval_requests=requests,
        usage_flags=usage_flags,
    )
    result = {
        "checkpoint": AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
        "contract_version": AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION,
        "retrieval_use_check_id": _require_non_empty_string(
            retrieval_use_check_id,
            field_name="retrieval_use_check_id",
            error_prefix="AI retrieval-use check",
        ),
        "retrieval_use_check_status": AI_RETRIEVAL_USE_CHECK_STATUS_VALIDATED,
        "retrieval_use_check_result": expected["retrieval_use_check_result"],
        "retrieval_use_failure_reasons": expected["retrieval_use_failure_reasons"],
        "source_role_discipline_check_result": expected[
            "source_role_discipline_check_result"
        ],
        "source_role_discipline_failure_reasons": expected[
            "source_role_discipline_failure_reasons"
        ],
        "retrieval_requests": requests,
        "usage_flags": usage_flags,
        "request_count": expected["request_count"],
        "governed_retrieval_request_count": expected[
            "governed_retrieval_request_count"
        ],
        "support_retrieval_request_count": expected["support_retrieval_request_count"],
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_generation_in_scope": False,
        "document_template_implementation_in_scope": False,
        "standards_conformance_in_scope": False,
        "detail_consistency_in_scope": False,
        "recommendation_behavior_in_scope": False,
        "retrieval_use_policy": (
            "retrieval_use_is_context_consumption_only_not_source_truth_"
            "execution_truth_or_payload_generation"
        ),
    }
    validate_retrieval_use_check_result(result)
    return result


def validate_retrieval_use_check_result(result: dict[str, object]) -> None:
    """Validate an M17.4 retrieval-use check result."""
    _validate_prohibited_fields(result, _PROHIBITED_RETRIEVAL_RULE_FIELDS)
    _validate_required_string_fields(
        result,
        _RETRIEVAL_USE_REQUIRED_STRING_FIELDS,
        error_prefix="AI retrieval-use check",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
        error_prefix="AI retrieval-use check",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION,
        error_prefix="AI retrieval-use check",
    )
    _validate_expected_exact_value(
        result,
        field_name="retrieval_use_check_status",
        expected_value=AI_RETRIEVAL_USE_CHECK_STATUS_VALIDATED,
        error_prefix="AI retrieval-use check",
    )
    _validate_boundary_false_flags(result, error_prefix="AI retrieval-use check")

    requests = _normalize_retrieval_requests(result.get("retrieval_requests"))
    usage_flags = _normalize_usage_flags(result.get("usage_flags"))
    expected = _evaluate_retrieval_use(
        retrieval_requests=requests,
        usage_flags=usage_flags,
    )

    for field_name in (
        "retrieval_use_check_result",
        "retrieval_use_failure_reasons",
        "source_role_discipline_check_result",
        "source_role_discipline_failure_reasons",
        "request_count",
        "governed_retrieval_request_count",
        "support_retrieval_request_count",
    ):
        if result.get(field_name) != expected[field_name]:
            raise ValueError(
                f"AI retrieval-use check {field_name} does not match deterministic evaluation."
            )

    _normalize_supported_value(
        result["retrieval_use_check_result"],
        field_name="retrieval_use_check_result",
        supported_values=SUPPORTED_RETRIEVAL_USE_CHECK_RESULTS,
        error_prefix="AI retrieval-use check",
    )
    _validate_failure_reasons(
        result.get("retrieval_use_failure_reasons"),
        supported_values=SUPPORTED_RETRIEVAL_USE_FAILURE_REASONS,
        error_prefix="AI retrieval-use check",
    )
    _validate_failure_reasons(
        result.get("source_role_discipline_failure_reasons"),
        supported_values=SUPPORTED_SOURCE_ROLE_DISCIPLINE_FAILURE_REASONS,
        error_prefix="AI retrieval-use check",
    )


def build_source_role_discipline_check_result(
    *,
    source_role_discipline_check_id: str,
    retrieval_requests: list[dict[str, object]],
    support_retrieval_used_as_source_truth: bool = False,
    support_retrieval_used_as_execution_truth: bool = False,
    support_retrieval_used_as_compiled_lookup_authority: bool = False,
    support_retrieval_used_as_governed_evidence: bool = False,
    mixed_governed_support_authority: bool = False,
) -> dict[str, object]:
    """Build and validate an M17.4 source-role discipline check result."""
    requests = _normalize_retrieval_requests(retrieval_requests)
    usage_flags = _build_usage_flags(
        support_retrieval_used_as_source_truth=support_retrieval_used_as_source_truth,
        support_retrieval_used_as_execution_truth=support_retrieval_used_as_execution_truth,
        support_retrieval_used_as_compiled_lookup_authority=(
            support_retrieval_used_as_compiled_lookup_authority
        ),
        support_retrieval_used_as_governed_evidence=(
            support_retrieval_used_as_governed_evidence
        ),
        mixed_governed_support_authority=mixed_governed_support_authority,
        requests_state_mutation=False,
        approval_requested=False,
        release_requested=False,
        document_generation_requested=False,
        document_template_implementation_requested=False,
    )
    expected = _evaluate_retrieval_use(
        retrieval_requests=requests,
        usage_flags=usage_flags,
    )
    result = {
        "checkpoint": AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
        "contract_version": AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION,
        "source_role_discipline_check_id": _require_non_empty_string(
            source_role_discipline_check_id,
            field_name="source_role_discipline_check_id",
            error_prefix="AI source-role discipline check",
        ),
        "source_role_discipline_check_status": (
            AI_SOURCE_ROLE_DISCIPLINE_CHECK_STATUS_VALIDATED
        ),
        "source_role_discipline_check_result": expected[
            "source_role_discipline_check_result"
        ],
        "source_role_discipline_failure_reasons": expected[
            "source_role_discipline_failure_reasons"
        ],
        "retrieval_requests": requests,
        "usage_flags": usage_flags,
        "governed_retrieval_request_count": expected[
            "governed_retrieval_request_count"
        ],
        "support_retrieval_request_count": expected["support_retrieval_request_count"],
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_generation_in_scope": False,
        "document_template_implementation_in_scope": False,
    }
    validate_source_role_discipline_check_result(result)
    return result


def validate_source_role_discipline_check_result(result: dict[str, object]) -> None:
    """Validate an M17.4 source-role discipline check result."""
    _validate_prohibited_fields(result, _PROHIBITED_RETRIEVAL_RULE_FIELDS)
    _validate_required_string_fields(
        result,
        _SOURCE_ROLE_REQUIRED_STRING_FIELDS,
        error_prefix="AI source-role discipline check",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
        error_prefix="AI source-role discipline check",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION,
        error_prefix="AI source-role discipline check",
    )
    _validate_expected_exact_value(
        result,
        field_name="source_role_discipline_check_status",
        expected_value=AI_SOURCE_ROLE_DISCIPLINE_CHECK_STATUS_VALIDATED,
        error_prefix="AI source-role discipline check",
    )
    _validate_boundary_false_flags(
        result,
        error_prefix="AI source-role discipline check",
    )

    requests = _normalize_retrieval_requests(result.get("retrieval_requests"))
    usage_flags = _normalize_usage_flags(result.get("usage_flags"))
    expected = _evaluate_retrieval_use(
        retrieval_requests=requests,
        usage_flags=usage_flags,
    )
    for field_name in (
        "source_role_discipline_check_result",
        "source_role_discipline_failure_reasons",
        "governed_retrieval_request_count",
        "support_retrieval_request_count",
    ):
        if result.get(field_name) != expected[field_name]:
            raise ValueError(
                "AI source-role discipline check "
                f"{field_name} does not match deterministic evaluation."
            )

    _normalize_supported_value(
        result["source_role_discipline_check_result"],
        field_name="source_role_discipline_check_result",
        supported_values=SUPPORTED_SOURCE_ROLE_DISCIPLINE_CHECK_RESULTS,
        error_prefix="AI source-role discipline check",
    )
    _validate_failure_reasons(
        result.get("source_role_discipline_failure_reasons"),
        supported_values=SUPPORTED_SOURCE_ROLE_DISCIPLINE_FAILURE_REASONS,
        error_prefix="AI source-role discipline check",
    )


def build_ai_retrieval_use_rule_result(
    *,
    retrieval_use_rule_result_id: str,
    retrieval_requests: list[dict[str, object]],
    support_retrieval_used_as_source_truth: bool = False,
    support_retrieval_used_as_execution_truth: bool = False,
    support_retrieval_used_as_compiled_lookup_authority: bool = False,
    support_retrieval_used_as_governed_evidence: bool = False,
    mixed_governed_support_authority: bool = False,
    requests_state_mutation: bool = False,
    approval_requested: bool = False,
    release_requested: bool = False,
    document_generation_requested: bool = False,
    document_template_implementation_requested: bool = False,
) -> dict[str, object]:
    """Build and validate one combined M17.4 retrieval-use rule result."""
    retrieval_use_check = build_retrieval_use_check_result(
        retrieval_use_check_id=f"{retrieval_use_rule_result_id}-RETRIEVAL-USE",
        retrieval_requests=retrieval_requests,
        support_retrieval_used_as_source_truth=support_retrieval_used_as_source_truth,
        support_retrieval_used_as_execution_truth=(
            support_retrieval_used_as_execution_truth
        ),
        support_retrieval_used_as_compiled_lookup_authority=(
            support_retrieval_used_as_compiled_lookup_authority
        ),
        support_retrieval_used_as_governed_evidence=(
            support_retrieval_used_as_governed_evidence
        ),
        mixed_governed_support_authority=mixed_governed_support_authority,
        requests_state_mutation=requests_state_mutation,
        approval_requested=approval_requested,
        release_requested=release_requested,
        document_generation_requested=document_generation_requested,
        document_template_implementation_requested=(
            document_template_implementation_requested
        ),
    )
    source_role_check = build_source_role_discipline_check_result(
        source_role_discipline_check_id=(
            f"{retrieval_use_rule_result_id}-SOURCE-ROLE"
        ),
        retrieval_requests=retrieval_requests,
        support_retrieval_used_as_source_truth=support_retrieval_used_as_source_truth,
        support_retrieval_used_as_execution_truth=(
            support_retrieval_used_as_execution_truth
        ),
        support_retrieval_used_as_compiled_lookup_authority=(
            support_retrieval_used_as_compiled_lookup_authority
        ),
        support_retrieval_used_as_governed_evidence=(
            support_retrieval_used_as_governed_evidence
        ),
        mixed_governed_support_authority=mixed_governed_support_authority,
    )
    retrieval_use_rule_result = (
        RETRIEVAL_USE_RULE_PASS
        if (
            retrieval_use_check["retrieval_use_check_result"]
            == RETRIEVAL_USE_CHECK_PASS
            and source_role_check["source_role_discipline_check_result"]
            == SOURCE_ROLE_DISCIPLINE_CHECK_PASS
        )
        else RETRIEVAL_USE_RULE_FAIL
    )
    failure_reasons = _deduplicate(
        list(retrieval_use_check["retrieval_use_failure_reasons"])
        + list(source_role_check["source_role_discipline_failure_reasons"])
    )
    result = {
        "checkpoint": AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
        "contract_version": AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION,
        "retrieval_use_rule_result_id": _require_non_empty_string(
            retrieval_use_rule_result_id,
            field_name="retrieval_use_rule_result_id",
            error_prefix="AI retrieval-use rule",
        ),
        "retrieval_use_rule_status": AI_RETRIEVAL_USE_RULE_STATUS_VALIDATED,
        "retrieval_use_rule_result": retrieval_use_rule_result,
        "retrieval_use_check_result": str(
            retrieval_use_check["retrieval_use_check_result"]
        ),
        "source_role_discipline_check_result": str(
            source_role_check["source_role_discipline_check_result"]
        ),
        "retrieval_use_rule_failure_reasons": failure_reasons,
        "source_retrieval_use_check": retrieval_use_check,
        "source_role_discipline_check": source_role_check,
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "document_generation_in_scope": False,
        "document_template_implementation_in_scope": False,
        "standards_conformance_in_scope": False,
        "detail_consistency_in_scope": False,
        "recommendation_behavior_in_scope": False,
        "retrieval_use_policy": (
            "ai_retrieval_use_rules_preserve_source_role_discipline_and_"
            "do_not_create_source_execution_or_release_truth"
        ),
    }
    validate_ai_retrieval_use_rule_result(result)
    return result


def validate_ai_retrieval_use_rule_result(result: dict[str, object]) -> None:
    """Validate one combined M17.4 retrieval-use rule result."""
    _validate_prohibited_fields(result, _PROHIBITED_RETRIEVAL_RULE_FIELDS)
    _validate_required_string_fields(
        result,
        _RETRIEVAL_RULE_REQUIRED_STRING_FIELDS,
        error_prefix="AI retrieval-use rule",
    )
    _validate_expected_exact_value(
        result,
        field_name="checkpoint",
        expected_value=AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
        error_prefix="AI retrieval-use rule",
    )
    _validate_expected_exact_value(
        result,
        field_name="contract_version",
        expected_value=AI_RETRIEVAL_USE_RULES_CONTRACT_VERSION,
        error_prefix="AI retrieval-use rule",
    )
    _validate_expected_exact_value(
        result,
        field_name="retrieval_use_rule_status",
        expected_value=AI_RETRIEVAL_USE_RULE_STATUS_VALIDATED,
        error_prefix="AI retrieval-use rule",
    )
    _validate_boundary_false_flags(result, error_prefix="AI retrieval-use rule")

    retrieval_use_check = result.get("source_retrieval_use_check")
    if not isinstance(retrieval_use_check, dict):
        raise ValueError("AI retrieval-use rule must include source_retrieval_use_check.")
    validate_retrieval_use_check_result(retrieval_use_check)

    source_role_check = result.get("source_role_discipline_check")
    if not isinstance(source_role_check, dict):
        raise ValueError(
            "AI retrieval-use rule must include source_role_discipline_check."
        )
    validate_source_role_discipline_check_result(source_role_check)

    if (
        result["retrieval_use_check_result"]
        != retrieval_use_check["retrieval_use_check_result"]
    ):
        raise ValueError(
            "AI retrieval-use rule retrieval_use_check_result must match source check."
        )
    if (
        result["source_role_discipline_check_result"]
        != source_role_check["source_role_discipline_check_result"]
    ):
        raise ValueError(
            "AI retrieval-use rule source_role_discipline_check_result must match source check."
        )

    expected_rule_result = (
        RETRIEVAL_USE_RULE_PASS
        if (
            retrieval_use_check["retrieval_use_check_result"]
            == RETRIEVAL_USE_CHECK_PASS
            and source_role_check["source_role_discipline_check_result"]
            == SOURCE_ROLE_DISCIPLINE_CHECK_PASS
        )
        else RETRIEVAL_USE_RULE_FAIL
    )
    if result["retrieval_use_rule_result"] != expected_rule_result:
        raise ValueError(
            "AI retrieval-use rule result does not match deterministic evaluation."
        )

    expected_failure_reasons = _deduplicate(
        list(retrieval_use_check["retrieval_use_failure_reasons"])
        + list(source_role_check["source_role_discipline_failure_reasons"])
    )
    if result.get("retrieval_use_rule_failure_reasons") != expected_failure_reasons:
        raise ValueError(
            "AI retrieval-use rule failure reasons must match source checks."
        )

    _normalize_supported_value(
        result["retrieval_use_rule_result"],
        field_name="retrieval_use_rule_result",
        supported_values=SUPPORTED_RETRIEVAL_USE_RULE_RESULTS,
        error_prefix="AI retrieval-use rule",
    )
    _validate_failure_reasons(
        result.get("retrieval_use_rule_failure_reasons"),
        supported_values=SUPPORTED_RETRIEVAL_USE_RULE_FAILURE_REASONS,
        error_prefix="AI retrieval-use rule",
    )


def _evaluate_retrieval_use(
    *,
    retrieval_requests: list[dict[str, object]],
    usage_flags: dict[str, bool],
) -> dict[str, object]:
    retrieval_failures: list[str] = []
    source_role_failures: list[str] = []
    governed_count = 0
    support_count = 0

    for request in retrieval_requests:
        mode = request.get("retrieval_mode")
        if mode == GOVERNED_DETERMINISTIC_RETRIEVAL_MODE:
            governed_count += 1
            try:
                validate_retrieval_boundary_request(request)
            except ValueError:
                retrieval_failures.append(GOVERNED_RETRIEVAL_VALIDATION_FAILURE)
            if request.get("retrieval_role") != GOVERNED_RETRIEVAL_ROLE:
                retrieval_failures.append(GOVERNED_RETRIEVAL_VALIDATION_FAILURE)
        elif mode == SUPPORT_RETRIEVAL_MODE:
            support_count += 1
            try:
                validate_retrieval_boundary_request(request)
            except ValueError:
                retrieval_failures.append(SUPPORT_RETRIEVAL_VALIDATION_FAILURE)
            if request.get("retrieval_role") != SUPPORT_RETRIEVAL_ROLE:
                source_role_failures.append(
                    SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE
                )
        else:
            retrieval_failures.append(UNSUPPORTED_RETRIEVAL_MODE_FAILURE)

        retrieval_failures.extend(_request_retrieval_failures(request))
        source_role_failures.extend(_request_source_role_failures(request))

    if usage_flags["support_retrieval_used_as_source_truth"]:
        source_role_failures.append(SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE)
    if usage_flags["support_retrieval_used_as_execution_truth"]:
        source_role_failures.append(SUPPORT_RETRIEVAL_EXECUTION_TRUTH_FAILURE)
    if usage_flags["support_retrieval_used_as_compiled_lookup_authority"]:
        source_role_failures.append(SUPPORT_RETRIEVAL_COMPILED_AUTHORITY_FAILURE)
    if usage_flags["support_retrieval_used_as_governed_evidence"]:
        source_role_failures.append(SUPPORT_RETRIEVAL_GOVERNED_EVIDENCE_FAILURE)
    if usage_flags["mixed_governed_support_authority"] and governed_count and support_count:
        source_role_failures.append(MIXED_GOVERNED_SUPPORT_AUTHORITY_FAILURE)

    if usage_flags["requests_state_mutation"]:
        retrieval_failures.append(STATE_MUTATION_REQUEST_FAILURE)
    if usage_flags["approval_requested"] or usage_flags["release_requested"]:
        retrieval_failures.append(APPROVAL_OR_RELEASE_REQUEST_FAILURE)
    if usage_flags["document_generation_requested"]:
        retrieval_failures.append(DOCUMENT_GENERATION_REQUEST_FAILURE)
    if usage_flags["document_template_implementation_requested"]:
        retrieval_failures.append(DOCUMENT_TEMPLATE_IMPLEMENTATION_REQUEST_FAILURE)

    retrieval_failures = _deduplicate(retrieval_failures)
    source_role_failures = _deduplicate(source_role_failures)

    return {
        "retrieval_use_check_result": (
            RETRIEVAL_USE_CHECK_PASS
            if not retrieval_failures and not source_role_failures
            else RETRIEVAL_USE_CHECK_FAIL
        ),
        "source_role_discipline_check_result": (
            SOURCE_ROLE_DISCIPLINE_CHECK_PASS
            if not source_role_failures
            else SOURCE_ROLE_DISCIPLINE_CHECK_FAIL
        ),
        "retrieval_use_failure_reasons": retrieval_failures,
        "source_role_discipline_failure_reasons": source_role_failures,
        "request_count": len(retrieval_requests),
        "governed_retrieval_request_count": governed_count,
        "support_retrieval_request_count": support_count,
    }


def _request_retrieval_failures(request: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if "resolver_bypass" in request and request.get("resolver_bypass") is not False:
        failures.append(RESOLVER_BYPASS_FAILURE)
    if "source_truth_override" in request:
        failures.append(SOURCE_TRUTH_OVERRIDE_FAILURE)
    if "execution_truth_override" in request:
        failures.append(EXECUTION_TRUTH_OVERRIDE_FAILURE)
    if (
        request.get("asset_payload_included") is not False
        or "asset_payload" in request
        or "unvalidated_asset_payload" in request
    ):
        failures.append(ASSET_PAYLOAD_INCLUDED_FAILURE)
    if request.get("requests_state_mutation") is True:
        failures.append(STATE_MUTATION_REQUEST_FAILURE)
    if request.get("approval_requested") is True or request.get("release_requested") is True:
        failures.append(APPROVAL_OR_RELEASE_REQUEST_FAILURE)
    if request.get("document_generation_requested") is True:
        failures.append(DOCUMENT_GENERATION_REQUEST_FAILURE)
    if request.get("document_template_implementation_requested") is True:
        failures.append(DOCUMENT_TEMPLATE_IMPLEMENTATION_REQUEST_FAILURE)
    return failures


def _request_source_role_failures(request: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if request.get("support_retrieval_as_source_truth") is True:
        failures.append(SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE)
    if request.get("support_retrieval_as_execution_truth") is True:
        failures.append(SUPPORT_RETRIEVAL_EXECUTION_TRUTH_FAILURE)
    if request.get("compiled_lookup_authority") is True and request.get("retrieval_mode") == SUPPORT_RETRIEVAL_MODE:
        failures.append(SUPPORT_RETRIEVAL_COMPILED_AUTHORITY_FAILURE)
    if request.get("support_retrieval_as_governed_evidence") is True:
        failures.append(SUPPORT_RETRIEVAL_GOVERNED_EVIDENCE_FAILURE)
    if request.get("support_retrieval_as_source_truth") is True:
        failures.append(SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE)
    return failures


def _normalize_retrieval_requests(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list) or not value:
        raise ValueError("AI retrieval-use rules require non-empty retrieval_requests.")
    requests: list[dict[str, object]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("AI retrieval-use rules retrieval_requests must contain dicts.")
        requests.append(dict(item))
    return requests


def _build_usage_flags(
    *,
    support_retrieval_used_as_source_truth: bool,
    support_retrieval_used_as_execution_truth: bool,
    support_retrieval_used_as_compiled_lookup_authority: bool,
    support_retrieval_used_as_governed_evidence: bool,
    mixed_governed_support_authority: bool,
    requests_state_mutation: bool,
    approval_requested: bool,
    release_requested: bool,
    document_generation_requested: bool,
    document_template_implementation_requested: bool,
) -> dict[str, bool]:
    return _normalize_usage_flags(
        {
            "support_retrieval_used_as_source_truth": support_retrieval_used_as_source_truth,
            "support_retrieval_used_as_execution_truth": support_retrieval_used_as_execution_truth,
            "support_retrieval_used_as_compiled_lookup_authority": support_retrieval_used_as_compiled_lookup_authority,
            "support_retrieval_used_as_governed_evidence": support_retrieval_used_as_governed_evidence,
            "mixed_governed_support_authority": mixed_governed_support_authority,
            "requests_state_mutation": requests_state_mutation,
            "approval_requested": approval_requested,
            "release_requested": release_requested,
            "document_generation_requested": document_generation_requested,
            "document_template_implementation_requested": document_template_implementation_requested,
        }
    )


def _normalize_usage_flags(value: object) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("AI retrieval-use rules require usage_flags dict.")
    flags: dict[str, bool] = {}
    for field_name in _USAGE_FLAG_FIELDS:
        raw_value = value.get(field_name)
        if not isinstance(raw_value, bool):
            raise ValueError(
                f"AI retrieval-use rules usage_flags must declare boolean {field_name}."
            )
        flags[field_name] = raw_value
    return flags


def _validate_boundary_false_flags(
    payload: dict[str, object],
    *,
    error_prefix: str,
) -> None:
    for field_name in (
        "actual_llm_call_required",
        "prompt_template_required",
        "state_mutation_allowed",
        "approval_or_release_allowed",
        "document_generation_in_scope",
        "document_template_implementation_in_scope",
    ):
        if payload.get(field_name) is not False:
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


def _deduplicate(values: list[str]) -> list[str]:
    deduplicated: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            deduplicated.append(value)
            seen.add(value)
    return deduplicated


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
                f"{field_name} is not allowed in M17.4 AI retrieval-use payloads."
            )
