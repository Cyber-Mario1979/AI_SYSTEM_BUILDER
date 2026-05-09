"AI-assisted controlled recommendation behavior support for M18.3."

from __future__ import annotations

from typing import Any

from asbp.ai_evaluation import QUALITY_GATE_PASS, validate_ai_quality_gate_result
from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID = "M18.3"
AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CONTRACT_VERSION = "ai-controlled-recommendation-behavior-v1"
AI_RECOMMENDATION_REQUEST_STATUS_VALIDATED = "ai_recommendation_request_validated"
AI_RECOMMENDATION_RESULT_STATUS_VALIDATED = "ai_recommendation_result_validated"
AI_RECOMMENDATION_ITEM_STATUS_VALIDATED = "ai_recommendation_item_validated"
AI_RECOMMENDATION_BOUNDARY_FINDING_STATUS_VALIDATED = "ai_recommendation_boundary_finding_validated"

ADVISORY_RECOMMENDATION_ASSISTANCE_ROLE = "advisory_recommendation_assistance"

DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET = "document_artifact_recommendation_target"
REPORTING_ARTIFACT_RECOMMENDATION_TARGET = "reporting_artifact_recommendation_target"
WORKFLOW_STATE_RECOMMENDATION_TARGET = "workflow_state_recommendation_target"
AI_OUTPUT_RECOMMENDATION_TARGET = "ai_output_recommendation_target"
SUPPORTED_RECOMMENDATION_TARGET_FAMILIES = (
    DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
    REPORTING_ARTIFACT_RECOMMENDATION_TARGET,
    WORKFLOW_STATE_RECOMMENDATION_TARGET,
    AI_OUTPUT_RECOMMENDATION_TARGET,
)

EVIDENCE_BOUND_RECOMMENDATION_MODE = "evidence_bound_recommendation"
CONTRACT_ALIGNED_RECOMMENDATION_MODE = "contract_aligned_recommendation"
GAP_AND_RISK_RECOMMENDATION_MODE = "gap_and_risk_recommendation"
SUPPORTED_RECOMMENDATION_MODES = (
    EVIDENCE_BOUND_RECOMMENDATION_MODE,
    CONTRACT_ALIGNED_RECOMMENDATION_MODE,
    GAP_AND_RISK_RECOMMENDATION_MODE,
)

EVIDENCE_FOLLOWUP_RECOMMENDATION = "evidence_followup_recommendation"
CONTRACT_ALIGNMENT_RECOMMENDATION = "contract_alignment_recommendation"
GAP_CLOSURE_RECOMMENDATION = "gap_closure_recommendation"
RISK_MITIGATION_RECOMMENDATION = "risk_mitigation_recommendation"
HUMAN_REVIEW_ESCALATION_RECOMMENDATION = "human_review_escalation_recommendation"
SOURCE_ROLE_DISCIPLINE_RECOMMENDATION = "source_role_discipline_recommendation"
DETAIL_DISCIPLINE_RECOMMENDATION = "detail_discipline_recommendation"
WORKFLOW_READINESS_RECOMMENDATION = "workflow_readiness_recommendation"
SUPPORTED_RECOMMENDATION_CATEGORIES = (
    EVIDENCE_FOLLOWUP_RECOMMENDATION,
    CONTRACT_ALIGNMENT_RECOMMENDATION,
    GAP_CLOSURE_RECOMMENDATION,
    RISK_MITIGATION_RECOMMENDATION,
    HUMAN_REVIEW_ESCALATION_RECOMMENDATION,
    SOURCE_ROLE_DISCIPLINE_RECOMMENDATION,
    DETAIL_DISCIPLINE_RECOMMENDATION,
    WORKFLOW_READINESS_RECOMMENDATION,
)

RECOMMENDATION_PRIORITY_LOW = "low"
RECOMMENDATION_PRIORITY_MEDIUM = "medium"
RECOMMENDATION_PRIORITY_HIGH = "high"
SUPPORTED_RECOMMENDATION_PRIORITIES = (
    RECOMMENDATION_PRIORITY_LOW,
    RECOMMENDATION_PRIORITY_MEDIUM,
    RECOMMENDATION_PRIORITY_HIGH,
)

RECOMMENDATION_ASSISTANCE_READY = "recommendation_assistance_ready"
RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_IDENTIFIED = "recommendation_assistance_recommendations_identified"
RECOMMENDATION_ASSISTANCE_BOUNDARY_FINDINGS_IDENTIFIED = "recommendation_assistance_boundary_findings_identified"
RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_AND_BOUNDARY_FINDINGS_IDENTIFIED = (
    "recommendation_assistance_recommendations_and_boundary_findings_identified"
)
SUPPORTED_RECOMMENDATION_ASSISTANCE_RESULTS = (
    RECOMMENDATION_ASSISTANCE_READY,
    RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_IDENTIFIED,
    RECOMMENDATION_ASSISTANCE_BOUNDARY_FINDINGS_IDENTIFIED,
    RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_AND_BOUNDARY_FINDINGS_IDENTIFIED,
)

RECOMMENDATION_APPROVAL_AUTHORITY_BOUNDARY_FINDING = "recommendation_approval_authority_boundary_finding"
RECOMMENDATION_RELEASE_AUTHORITY_BOUNDARY_FINDING = "recommendation_release_authority_boundary_finding"
RECOMMENDATION_WORKFLOW_STATE_MUTATION_BOUNDARY_FINDING = (
    "recommendation_workflow_state_mutation_boundary_finding"
)
RECOMMENDATION_ACTION_EXECUTION_BOUNDARY_FINDING = "recommendation_action_execution_boundary_finding"
RECOMMENDATION_DOCUMENT_GENERATION_BOUNDARY_FINDING = "recommendation_document_generation_boundary_finding"
RECOMMENDATION_REPORT_GENERATION_BOUNDARY_FINDING = "recommendation_report_generation_boundary_finding"
RECOMMENDATION_PRODUCT_RENDERING_BOUNDARY_FINDING = "recommendation_product_rendering_boundary_finding"
RECOMMENDATION_VALIDATION_TRUTH_BOUNDARY_FINDING = "recommendation_validation_truth_boundary_finding"
RECOMMENDATION_AUTONOMOUS_AGENTIC_BEHAVIOR_BOUNDARY_FINDING = (
    "recommendation_autonomous_agentic_behavior_boundary_finding"
)
RECOMMENDATION_UNGROUNDED_ACTION_BOUNDARY_FINDING = "recommendation_ungrounded_action_boundary_finding"
SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_CATEGORIES = (
    RECOMMENDATION_APPROVAL_AUTHORITY_BOUNDARY_FINDING,
    RECOMMENDATION_RELEASE_AUTHORITY_BOUNDARY_FINDING,
    RECOMMENDATION_WORKFLOW_STATE_MUTATION_BOUNDARY_FINDING,
    RECOMMENDATION_ACTION_EXECUTION_BOUNDARY_FINDING,
    RECOMMENDATION_DOCUMENT_GENERATION_BOUNDARY_FINDING,
    RECOMMENDATION_REPORT_GENERATION_BOUNDARY_FINDING,
    RECOMMENDATION_PRODUCT_RENDERING_BOUNDARY_FINDING,
    RECOMMENDATION_VALIDATION_TRUTH_BOUNDARY_FINDING,
    RECOMMENDATION_AUTONOMOUS_AGENTIC_BEHAVIOR_BOUNDARY_FINDING,
    RECOMMENDATION_UNGROUNDED_ACTION_BOUNDARY_FINDING,
)

RECOMMENDATION_BOUNDARY_FINDING_INFO_SEVERITY = "info"
RECOMMENDATION_BOUNDARY_FINDING_WARNING_SEVERITY = "warning"
RECOMMENDATION_BOUNDARY_FINDING_BLOCKING_SEVERITY = "blocking"
SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_SEVERITIES = (
    RECOMMENDATION_BOUNDARY_FINDING_INFO_SEVERITY,
    RECOMMENDATION_BOUNDARY_FINDING_WARNING_SEVERITY,
    RECOMMENDATION_BOUNDARY_FINDING_BLOCKING_SEVERITY,
)

_PROHIBITED_RECOMMENDATION_FIELDS = (
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
    "generated_recommendation_text",
    "recommendation_narrative_text",
    "free_form_recommendation_text",
    "generated_document_text",
    "generated_report_text",
    "generated_output_text",
    "document_factory_payload",
    "document_template_payload",
    "document_generation_payload",
    "report_generation_payload",
    "document_renderer_payload",
    "product_ready_document_payload",
    "product_ready_report_payload",
    "export_payload",
    "dashboard_payload",
    "recommendation_payload",
    "action_execution_payload",
    "autonomous_agent_payload",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "execution_truth_override",
    "source_truth_override",
    "validation_truth_override",
    "standards_truth_override",
)

_REQUEST_REQUIRED_FALSE_FIELDS = (
    "approval_requested",
    "release_requested",
    "state_mutation_requested",
    "action_execution_requested",
    "autonomous_action_requested",
    "document_generation_requested",
    "report_generation_requested",
    "document_template_product_implementation_requested",
    "product_ready_rendering_requested",
    "validation_truth_requested",
    "uat_truth_requested",
    "human_decision_replacement_requested",
    "document_factory_in_scope",
    "actual_document_generation_in_scope",
    "actual_report_generation_in_scope",
    "product_ready_rendering_in_scope",
    "approval_authority_claimed",
    "release_authority_claimed",
    "workflow_mutation_authority_claimed",
    "action_execution_authority_claimed",
    "autonomous_action_authority_claimed",
    "validation_truth_authority_claimed",
)

_RESULT_REQUIRED_FALSE_FIELDS = (
    "ai_can_approve",
    "ai_can_release",
    "ai_can_mutate_workflow_state",
    "ai_can_execute_actions",
    "ai_can_replace_human_decision",
    "ai_can_generate_document",
    "ai_can_generate_report",
    "ai_can_render_product_ready_document",
    "ai_can_render_product_ready_report",
    "ai_can_claim_validation_truth",
    "approval_payload_included",
    "workflow_release_payload_included",
    "state_mutation_payload_included",
    "action_execution_payload_included",
    "document_generation_payload_included",
    "report_generation_payload_included",
    "product_ready_rendering_payload_included",
    "validation_or_uat_truth_claimed",
)


def build_controlled_recommendation_behavior_baseline() -> dict[str, Any]:
    """Return the M18.3 controlled recommendation-behavior baseline."""
    return {
        "checkpoint": AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CONTRACT_VERSION,
        "supported_recommendation_target_families": list(SUPPORTED_RECOMMENDATION_TARGET_FAMILIES),
        "supported_recommendation_modes": list(SUPPORTED_RECOMMENDATION_MODES),
        "supported_recommendation_categories": list(SUPPORTED_RECOMMENDATION_CATEGORIES),
        "supported_recommendation_priorities": list(SUPPORTED_RECOMMENDATION_PRIORITIES),
        "supported_boundary_finding_categories": list(SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_CATEGORIES),
        "supported_boundary_finding_severities": list(SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_SEVERITIES),
        "supported_assistance_results": list(SUPPORTED_RECOMMENDATION_ASSISTANCE_RESULTS),
        "assistance_role": ADVISORY_RECOMMENDATION_ASSISTANCE_ROLE,
        "authority_policy": (
            "recommendation_assistance_is_advisory_metadata_only_and_cannot_approve_release_"
            "mutate_workflow_state_execute_actions_replace_human_decisions_or_claim_validation_truth"
        ),
        "source_discipline_policy": (
            "recommendation_assistance_must_use_passed_m17_quality_gate_evidence_"
            "and_source_role_context"
        ),
        "controlled_recommendation_policy": (
            "recommendations_may_only_identify_bounded_evidence_contract_gap_risk_human_review_"
            "source_role_detail_discipline_or_readiness_suggestions"
        ),
        "deferred_scope_policy": (
            "document_factory_document_generation_report_generation_product_rendering_action_execution_"
            "autonomous_agentic_behavior_and_validation_truth_remain_out_of_scope"
        ),
        "not_owned_by_m18_3": [
            "actual_llm_calls",
            "prompt_templates",
            "document_factory",
            "document_template_product_implementation",
            "actual_document_generation_from_expanded_governed_library_content",
            "actual_report_generation_from_expanded_governed_library_content",
            "product_ready_document_rendering",
            "product_ready_report_rendering",
            "workflow_state_mutation",
            "action_execution",
            "autonomous_agentic_behavior",
            "approval_or_release_authority",
            "validation_or_uat_truth_claims",
            "ui_api_behavior",
            "cloud_or_saas_productization",
        ],
    }


def build_controlled_recommendation_request(
    *,
    recommendation_request_id: str,
    source_quality_gate_result: dict[str, object],
    recommendation_target_ref: str,
    recommendation_target_family: str,
    recommendation_mode: str,
    recommendation_evidence_refs: list[str] | None = None,
    source_refs_used_as_truth: list[str] | None = None,
    approval_requested: bool = False,
    release_requested: bool = False,
    state_mutation_requested: bool = False,
    action_execution_requested: bool = False,
    autonomous_action_requested: bool = False,
    document_generation_requested: bool = False,
    report_generation_requested: bool = False,
    document_template_product_implementation_requested: bool = False,
    product_ready_rendering_requested: bool = False,
    validation_truth_requested: bool = False,
    uat_truth_requested: bool = False,
    human_decision_replacement_requested: bool = False,
) -> dict[str, object]:
    """Build and validate a controlled M18.3 recommendation request."""
    validate_ai_quality_gate_result(source_quality_gate_result)
    request = {
        "checkpoint": AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CONTRACT_VERSION,
        "recommendation_request_id": _require_non_empty_string(
            recommendation_request_id,
            "recommendation_request_id",
        ),
        "recommendation_request_status": AI_RECOMMENDATION_REQUEST_STATUS_VALIDATED,
        "recommendation_target_ref": _parse_version_pinned_ref(
            recommendation_target_ref,
            "recommendation_target_ref",
        ),
        "recommendation_target_family": _normalize_supported_value(
            recommendation_target_family,
            "recommendation_target_family",
            SUPPORTED_RECOMMENDATION_TARGET_FAMILIES,
        ),
        "recommendation_mode": _normalize_supported_value(
            recommendation_mode,
            "recommendation_mode",
            SUPPORTED_RECOMMENDATION_MODES,
        ),
        "requested_assistance_role": ADVISORY_RECOMMENDATION_ASSISTANCE_ROLE,
        "source_quality_gate_result_id": str(source_quality_gate_result["quality_gate_result_id"]),
        "source_quality_gate_result": dict(source_quality_gate_result),
        "recommendation_evidence_refs": _normalize_ref_list(
            recommendation_evidence_refs
            if recommendation_evidence_refs is not None
            else _quality_gate_evidence_refs(source_quality_gate_result),
            "recommendation_evidence_refs",
        ),
        "source_refs_used_as_truth": _normalize_ref_list(
            source_refs_used_as_truth
            if source_refs_used_as_truth is not None
            else _quality_gate_truth_refs(source_quality_gate_result),
            "source_refs_used_as_truth",
        ),
        "approval_requested": approval_requested,
        "release_requested": release_requested,
        "state_mutation_requested": state_mutation_requested,
        "action_execution_requested": action_execution_requested,
        "autonomous_action_requested": autonomous_action_requested,
        "document_generation_requested": document_generation_requested,
        "report_generation_requested": report_generation_requested,
        "document_template_product_implementation_requested": document_template_product_implementation_requested,
        "product_ready_rendering_requested": product_ready_rendering_requested,
        "validation_truth_requested": validation_truth_requested,
        "uat_truth_requested": uat_truth_requested,
        "human_decision_replacement_requested": human_decision_replacement_requested,
        "document_factory_in_scope": False,
        "actual_document_generation_in_scope": False,
        "actual_report_generation_in_scope": False,
        "product_ready_rendering_in_scope": False,
        "approval_authority_claimed": False,
        "release_authority_claimed": False,
        "workflow_mutation_authority_claimed": False,
        "action_execution_authority_claimed": False,
        "autonomous_action_authority_claimed": False,
        "validation_truth_authority_claimed": False,
        "recommendation_output_policy": "structured_metadata_only_no_free_form_recommendation_text",
    }
    validate_controlled_recommendation_request(request)
    return request


def validate_controlled_recommendation_request(request: dict[str, object]) -> None:
    """Validate one M18.3 controlled recommendation request."""
    _validate_prohibited_fields(request)
    _validate_required_string_fields(
        request,
        (
            "checkpoint",
            "contract_version",
            "recommendation_request_id",
            "recommendation_request_status",
            "recommendation_target_ref",
            "recommendation_target_family",
            "recommendation_mode",
            "requested_assistance_role",
            "source_quality_gate_result_id",
        ),
        "AI controlled recommendation request",
    )
    _validate_exact(request, "checkpoint", AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID)
    _validate_exact(request, "contract_version", AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CONTRACT_VERSION)
    _validate_exact(request, "recommendation_request_status", AI_RECOMMENDATION_REQUEST_STATUS_VALIDATED)
    _validate_exact(request, "requested_assistance_role", ADVISORY_RECOMMENDATION_ASSISTANCE_ROLE)

    source_quality_gate = request.get("source_quality_gate_result")
    if not isinstance(source_quality_gate, dict):
        raise ValueError("AI controlled recommendation request must include source_quality_gate_result dict.")
    validate_ai_quality_gate_result(source_quality_gate)
    if source_quality_gate.get("quality_gate_result") != QUALITY_GATE_PASS:
        raise ValueError("AI controlled recommendation request requires a passing source quality gate.")
    if request["source_quality_gate_result_id"] != source_quality_gate["quality_gate_result_id"]:
        raise ValueError("AI controlled recommendation request source_quality_gate_result_id must match payload.")

    _parse_version_pinned_ref(request["recommendation_target_ref"], "recommendation_target_ref")
    _normalize_supported_value(
        request["recommendation_target_family"],
        "recommendation_target_family",
        SUPPORTED_RECOMMENDATION_TARGET_FAMILIES,
    )
    _normalize_supported_value(
        request["recommendation_mode"],
        "recommendation_mode",
        SUPPORTED_RECOMMENDATION_MODES,
    )
    for field_name in _REQUEST_REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(f"AI controlled recommendation request requires {field_name} to be False.")

    _validate_refs_subset(
        declared=_normalize_ref_list(request.get("recommendation_evidence_refs"), "recommendation_evidence_refs"),
        allowed=_quality_gate_evidence_refs(source_quality_gate),
        field_name="recommendation_evidence_refs",
    )
    _validate_refs_subset(
        declared=_normalize_ref_list(request.get("source_refs_used_as_truth"), "source_refs_used_as_truth"),
        allowed=_quality_gate_truth_refs(source_quality_gate),
        field_name="source_refs_used_as_truth",
    )


def build_controlled_recommendation_item(
    *,
    recommendation_id: str,
    recommendation_category: str,
    evidence_ref: str,
    source_ref: str,
    recommendation_priority: str = RECOMMENDATION_PRIORITY_MEDIUM,
) -> dict[str, object]:
    """Build and validate one controlled recommendation metadata item."""
    recommendation = {
        "recommendation_id": _require_non_empty_string(recommendation_id, "recommendation_id"),
        "recommendation_status": AI_RECOMMENDATION_ITEM_STATUS_VALIDATED,
        "recommendation_category": _normalize_supported_value(
            recommendation_category,
            "recommendation_category",
            SUPPORTED_RECOMMENDATION_CATEGORIES,
        ),
        "recommendation_priority": _normalize_supported_value(
            recommendation_priority,
            "recommendation_priority",
            SUPPORTED_RECOMMENDATION_PRIORITIES,
        ),
        "evidence_ref": _parse_version_pinned_ref(evidence_ref, "evidence_ref"),
        "source_ref": _parse_version_pinned_ref(source_ref, "source_ref"),
        "requires_human_decision": True,
        "recommendation_language_policy": "metadata_only_no_free_form_recommendation_text",
        "action_policy": "recommendation_does_not_execute_or_mutate_workflow_state",
    }
    validate_controlled_recommendation_item(recommendation)
    return recommendation


def validate_controlled_recommendation_item(recommendation: dict[str, object]) -> None:
    """Validate one controlled recommendation metadata item."""
    _validate_prohibited_fields(recommendation)
    _validate_required_string_fields(
        recommendation,
        (
            "recommendation_id",
            "recommendation_status",
            "recommendation_category",
            "recommendation_priority",
            "evidence_ref",
            "source_ref",
        ),
        "AI controlled recommendation item",
    )
    _validate_exact(recommendation, "recommendation_status", AI_RECOMMENDATION_ITEM_STATUS_VALIDATED)
    _normalize_supported_value(
        recommendation["recommendation_category"],
        "recommendation_category",
        SUPPORTED_RECOMMENDATION_CATEGORIES,
    )
    _normalize_supported_value(
        recommendation["recommendation_priority"],
        "recommendation_priority",
        SUPPORTED_RECOMMENDATION_PRIORITIES,
    )
    _parse_version_pinned_ref(recommendation["evidence_ref"], "evidence_ref")
    _parse_version_pinned_ref(recommendation["source_ref"], "source_ref")
    if recommendation.get("requires_human_decision") is not True:
        raise ValueError("AI controlled recommendation item must require human decision.")


def build_controlled_recommendation_boundary_finding(
    *,
    finding_id: str,
    finding_category: str,
    evidence_ref: str,
    source_ref: str,
    finding_severity: str = RECOMMENDATION_BOUNDARY_FINDING_WARNING_SEVERITY,
) -> dict[str, object]:
    """Build and validate one controlled recommendation boundary-finding record."""
    finding = {
        "finding_id": _require_non_empty_string(finding_id, "finding_id"),
        "finding_status": AI_RECOMMENDATION_BOUNDARY_FINDING_STATUS_VALIDATED,
        "finding_category": _normalize_supported_value(
            finding_category,
            "finding_category",
            SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_CATEGORIES,
        ),
        "finding_severity": _normalize_supported_value(
            finding_severity,
            "finding_severity",
            SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_SEVERITIES,
        ),
        "evidence_ref": _parse_version_pinned_ref(evidence_ref, "evidence_ref"),
        "source_ref": _parse_version_pinned_ref(source_ref, "source_ref"),
        "finding_language_policy": "metadata_only_no_free_form_recommendation_narrative",
    }
    validate_controlled_recommendation_boundary_finding(finding)
    return finding


def validate_controlled_recommendation_boundary_finding(finding: dict[str, object]) -> None:
    """Validate one controlled recommendation boundary-finding record."""
    _validate_prohibited_fields(finding)
    _validate_required_string_fields(
        finding,
        (
            "finding_id",
            "finding_status",
            "finding_category",
            "finding_severity",
            "evidence_ref",
            "source_ref",
        ),
        "AI controlled recommendation boundary finding",
    )
    _validate_exact(finding, "finding_status", AI_RECOMMENDATION_BOUNDARY_FINDING_STATUS_VALIDATED)
    _normalize_supported_value(
        finding["finding_category"],
        "finding_category",
        SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_CATEGORIES,
    )
    _normalize_supported_value(
        finding["finding_severity"],
        "finding_severity",
        SUPPORTED_RECOMMENDATION_BOUNDARY_FINDING_SEVERITIES,
    )
    _parse_version_pinned_ref(finding["evidence_ref"], "evidence_ref")
    _parse_version_pinned_ref(finding["source_ref"], "source_ref")


def build_controlled_recommendation_result(
    *,
    recommendation_result_id: str,
    recommendation_request: dict[str, object],
    recommendation_items: list[dict[str, object]] | None = None,
    recommendation_boundary_findings: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build and validate a controlled M18.3 recommendation result."""
    validate_controlled_recommendation_request(recommendation_request)
    items = [dict(item) for item in recommendation_items or []]
    findings = [dict(finding) for finding in recommendation_boundary_findings or []]
    for item in items:
        validate_controlled_recommendation_item(item)
    for finding in findings:
        validate_controlled_recommendation_boundary_finding(finding)
    result = {
        "checkpoint": AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CONTRACT_VERSION,
        "recommendation_result_id": _require_non_empty_string(
            recommendation_result_id,
            "recommendation_result_id",
        ),
        "recommendation_result_status": AI_RECOMMENDATION_RESULT_STATUS_VALIDATED,
        "recommendation_request_id": str(recommendation_request["recommendation_request_id"]),
        "recommendation_target_ref": str(recommendation_request["recommendation_target_ref"]),
        "recommendation_target_family": str(recommendation_request["recommendation_target_family"]),
        "recommendation_mode": str(recommendation_request["recommendation_mode"]),
        "recommendation_assistance_result": _deterministic_recommendation_assistance_result(items, findings),
        "recommendation_items": items,
        "recommendation_boundary_findings": findings,
        "source_recommendation_request": dict(recommendation_request),
        "advisory_only": True,
        "controlled_recommendation_behavior_in_scope": True,
        "ai_can_issue_controlled_recommendation_metadata": True,
        "ai_can_approve": False,
        "ai_can_release": False,
        "ai_can_mutate_workflow_state": False,
        "ai_can_execute_actions": False,
        "ai_can_replace_human_decision": False,
        "ai_can_generate_document": False,
        "ai_can_generate_report": False,
        "ai_can_render_product_ready_document": False,
        "ai_can_render_product_ready_report": False,
        "ai_can_claim_validation_truth": False,
        "approval_payload_included": False,
        "workflow_release_payload_included": False,
        "state_mutation_payload_included": False,
        "action_execution_payload_included": False,
        "document_generation_payload_included": False,
        "report_generation_payload_included": False,
        "product_ready_rendering_payload_included": False,
        "validation_or_uat_truth_claimed": False,
        "recommendation_authority_policy": "advisory_metadata_only_requires_human_decision_for_acceptance",
        "deferred_scope_policy": (
            "document_factory_template_product_implementation_document_generation_report_generation_"
            "product_ready_rendering_action_execution_autonomous_agentic_behavior_and_validation_truth_remain_out_of_scope"
        ),
    }
    validate_controlled_recommendation_result(result)
    return result


def validate_controlled_recommendation_result(result: dict[str, object]) -> None:
    """Validate one M18.3 controlled recommendation result."""
    _validate_prohibited_fields(result)
    _validate_required_string_fields(
        result,
        (
            "checkpoint",
            "contract_version",
            "recommendation_result_id",
            "recommendation_result_status",
            "recommendation_request_id",
            "recommendation_target_ref",
            "recommendation_target_family",
            "recommendation_mode",
            "recommendation_assistance_result",
        ),
        "AI controlled recommendation result",
    )
    _validate_exact(result, "checkpoint", AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID)
    _validate_exact(result, "contract_version", AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CONTRACT_VERSION)
    _validate_exact(result, "recommendation_result_status", AI_RECOMMENDATION_RESULT_STATUS_VALIDATED)
    if result.get("advisory_only") is not True:
        raise ValueError("AI controlled recommendation result must be advisory_only.")
    if result.get("controlled_recommendation_behavior_in_scope") is not True:
        raise ValueError("AI controlled recommendation result must keep controlled recommendation behavior in scope.")
    if result.get("ai_can_issue_controlled_recommendation_metadata") is not True:
        raise ValueError("AI controlled recommendation result must permit controlled recommendation metadata only.")
    for field_name in _RESULT_REQUIRED_FALSE_FIELDS:
        if result.get(field_name) is not False:
            raise ValueError(f"AI controlled recommendation result requires {field_name} to be False.")

    request = result.get("source_recommendation_request")
    if not isinstance(request, dict):
        raise ValueError("AI controlled recommendation result must include source_recommendation_request dict.")
    validate_controlled_recommendation_request(request)
    for field_name in (
        "recommendation_request_id",
        "recommendation_target_ref",
        "recommendation_target_family",
        "recommendation_mode",
    ):
        if result[field_name] != request[field_name]:
            raise ValueError(f"AI controlled recommendation result {field_name} must match request.")

    items = result.get("recommendation_items")
    if not isinstance(items, list):
        raise ValueError("AI controlled recommendation result recommendation_items must be a list.")
    seen_item_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("AI controlled recommendation result recommendation_items must contain dicts.")
        validate_controlled_recommendation_item(item)
        item_id = str(item["recommendation_id"])
        if item_id in seen_item_ids:
            raise ValueError("AI controlled recommendation result recommendation_id values must be unique.")
        seen_item_ids.add(item_id)

    findings = result.get("recommendation_boundary_findings")
    if not isinstance(findings, list):
        raise ValueError("AI controlled recommendation result recommendation_boundary_findings must be a list.")
    seen_finding_ids: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("AI controlled recommendation result recommendation_boundary_findings must contain dicts.")
        validate_controlled_recommendation_boundary_finding(finding)
        finding_id = str(finding["finding_id"])
        if finding_id in seen_finding_ids:
            raise ValueError("AI controlled recommendation result finding_id values must be unique.")
        seen_finding_ids.add(finding_id)

    _validate_item_and_finding_refs_within_request(items, findings, request)
    expected_result = _deterministic_recommendation_assistance_result(items, findings)
    if result["recommendation_assistance_result"] != expected_result:
        raise ValueError("AI controlled recommendation result does not match deterministic recommendation evaluation.")
    _normalize_supported_value(
        result["recommendation_assistance_result"],
        "recommendation_assistance_result",
        SUPPORTED_RECOMMENDATION_ASSISTANCE_RESULTS,
    )


def _deterministic_recommendation_assistance_result(
    recommendation_items: list[dict[str, object]],
    recommendation_boundary_findings: list[dict[str, object]],
) -> str:
    has_items = bool(recommendation_items)
    has_findings = bool(recommendation_boundary_findings)
    if has_items and has_findings:
        return RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_AND_BOUNDARY_FINDINGS_IDENTIFIED
    if has_items:
        return RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_IDENTIFIED
    if has_findings:
        return RECOMMENDATION_ASSISTANCE_BOUNDARY_FINDINGS_IDENTIFIED
    return RECOMMENDATION_ASSISTANCE_READY


def _quality_gate_evidence_refs(source_quality_gate_result: dict[str, object]) -> list[str]:
    groundedness = _groundedness_payload(source_quality_gate_result)
    return _normalize_ref_list(groundedness.get("evidence_refs_used"), "evidence_refs_used")


def _quality_gate_truth_refs(source_quality_gate_result: dict[str, object]) -> list[str]:
    groundedness = _groundedness_payload(source_quality_gate_result)
    return _normalize_ref_list(groundedness.get("source_refs_used_as_truth"), "source_refs_used_as_truth")


def _groundedness_payload(source_quality_gate_result: dict[str, object]) -> dict[str, object]:
    validate_ai_quality_gate_result(source_quality_gate_result)
    groundedness = source_quality_gate_result.get("source_groundedness_check")
    if not isinstance(groundedness, dict):
        raise ValueError("AI controlled recommendation requires source_groundedness_check dict.")
    return groundedness


def _validate_refs_subset(*, declared: list[str], allowed: list[str], field_name: str) -> None:
    allowed_set = set(allowed)
    for ref in declared:
        if ref not in allowed_set:
            raise ValueError(
                "AI controlled recommendation request "
                f"{field_name} includes ref outside the passed source quality gate: {ref}."
            )


def _validate_item_and_finding_refs_within_request(
    recommendation_items: list[dict[str, object]],
    recommendation_boundary_findings: list[dict[str, object]],
    request: dict[str, object],
) -> None:
    evidence_refs = set(
        _normalize_ref_list(request.get("recommendation_evidence_refs"), "recommendation_evidence_refs")
    )
    source_refs = set(_normalize_ref_list(request.get("source_refs_used_as_truth"), "source_refs_used_as_truth"))
    for item in recommendation_items:
        if _parse_version_pinned_ref(item["evidence_ref"], "evidence_ref") not in evidence_refs:
            raise ValueError("AI controlled recommendation item evidence_ref must be inside request evidence refs.")
        if _parse_version_pinned_ref(item["source_ref"], "source_ref") not in source_refs:
            raise ValueError("AI controlled recommendation item source_ref must be inside request source refs.")
    for finding in recommendation_boundary_findings:
        if _parse_version_pinned_ref(finding["evidence_ref"], "evidence_ref") not in evidence_refs:
            raise ValueError("AI controlled recommendation boundary finding evidence_ref must be inside request evidence refs.")
        if _parse_version_pinned_ref(finding["source_ref"], "source_ref") not in source_refs:
            raise ValueError("AI controlled recommendation boundary finding source_ref must be inside request source refs.")


def _parse_version_pinned_ref(raw_ref: object, field_name: str) -> str:
    ref = _require_non_empty_string(raw_ref, field_name)
    return parse_version_pinned_asset_ref(ref)["asset_ref"]


def _normalize_ref_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"AI controlled recommendation requires non-empty list {field_name}.")
    refs = [_parse_version_pinned_ref(raw_ref, field_name) for raw_ref in value]
    return sorted(_deduplicate(refs))


def _normalize_supported_value(value: object, field_name: str, supported_values: tuple[str, ...]) -> str:
    normalized = _require_non_empty_string(value, field_name)
    if normalized not in supported_values:
        raise ValueError(
            f"AI controlled recommendation declares unsupported {field_name}. "
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


def _require_non_empty_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"AI controlled recommendation must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(payload: dict[str, object], required_fields: tuple[str, ...], label: str) -> None:
    for field_name in required_fields:
        _require_non_empty_string(payload.get(field_name), field_name)


def _validate_exact(payload: dict[str, object], field_name: str, expected_value: str) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            "AI controlled recommendation declares invalid "
            f"{field_name}: expected {expected_value!r}, got {actual_value!r}."
        )


def _validate_prohibited_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_RECOMMENDATION_FIELDS:
        if field_name in payload:
            raise ValueError(f"{field_name} is not allowed in M18.3 controlled recommendation payloads.")
