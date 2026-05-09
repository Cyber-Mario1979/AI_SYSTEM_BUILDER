"AI-assisted workflow-expansion boundaries and refusal rules for M18.4."

from __future__ import annotations

from typing import Any

from asbp.ai_evaluation import QUALITY_GATE_PASS, validate_ai_quality_gate_result
from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

AI_WORKFLOW_EXPANSION_BOUNDARIES_CHECKPOINT_ID = "M18.4"
AI_WORKFLOW_EXPANSION_BOUNDARIES_CONTRACT_VERSION = "ai-workflow-expansion-boundaries-v1"
AI_WORKFLOW_EXPANSION_REQUEST_STATUS_VALIDATED = "ai_workflow_expansion_request_validated"
AI_WORKFLOW_EXPANSION_DECISION_STATUS_VALIDATED = "ai_workflow_expansion_decision_validated"

ADVISORY_WORKFLOW_EXPANSION_BOUNDARY_GATE_ROLE = "advisory_workflow_expansion_boundary_gate"

CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY = "controlled_review_assistance_request"
CONTROLLED_SUMMARIZATION_REPORTING_ASSISTANCE_REQUEST_FAMILY = (
    "controlled_summarization_reporting_assistance_request"
)
CONTROLLED_RECOMMENDATION_ASSISTANCE_REQUEST_FAMILY = "controlled_recommendation_assistance_request"
EVIDENCE_SOURCE_ROLE_DISCIPLINE_REQUEST_FAMILY = "evidence_source_role_discipline_request"
BOUNDARY_FINDING_METADATA_REQUEST_FAMILY = "boundary_finding_metadata_request"
HUMAN_REVIEW_HANDOFF_REQUEST_FAMILY = "human_review_handoff_request"
SUPPORTED_ALLOWED_WORKFLOW_EXPANSION_REQUEST_FAMILIES = (
    CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY,
    CONTROLLED_SUMMARIZATION_REPORTING_ASSISTANCE_REQUEST_FAMILY,
    CONTROLLED_RECOMMENDATION_ASSISTANCE_REQUEST_FAMILY,
    EVIDENCE_SOURCE_ROLE_DISCIPLINE_REQUEST_FAMILY,
    BOUNDARY_FINDING_METADATA_REQUEST_FAMILY,
    HUMAN_REVIEW_HANDOFF_REQUEST_FAMILY,
)

INSUFFICIENT_EVIDENCE_FALLBACK_REQUEST_FAMILY = "insufficient_evidence_fallback_request"
NON_AUTHORITATIVE_SOURCE_FALLBACK_REQUEST_FAMILY = "non_authoritative_source_fallback_request"
MISSING_CONTRACT_CONTEXT_FALLBACK_REQUEST_FAMILY = "missing_contract_context_fallback_request"
SUPPORTED_FALLBACK_ONLY_WORKFLOW_EXPANSION_REQUEST_FAMILIES = (
    INSUFFICIENT_EVIDENCE_FALLBACK_REQUEST_FAMILY,
    NON_AUTHORITATIVE_SOURCE_FALLBACK_REQUEST_FAMILY,
    MISSING_CONTRACT_CONTEXT_FALLBACK_REQUEST_FAMILY,
)

APPROVAL_OR_RELEASE_REQUEST_FAMILY = "approval_or_release_request"
WORKFLOW_STATE_MUTATION_REQUEST_FAMILY = "workflow_state_mutation_request"
ACTION_EXECUTION_REQUEST_FAMILY = "action_execution_request"
AUTONOMOUS_AGENTIC_BEHAVIOR_REQUEST_FAMILY = "autonomous_agentic_behavior_request"
DOCUMENT_GENERATION_REQUEST_FAMILY = "document_generation_request"
REPORT_GENERATION_REQUEST_FAMILY = "report_generation_request"
PRODUCT_READY_RENDERING_REQUEST_FAMILY = "product_ready_rendering_request"
PROMPT_TEMPLATE_REQUEST_FAMILY = "prompt_template_request"
DIRECT_LLM_CALL_REQUEST_FAMILY = "direct_llm_call_request"
VALIDATION_OR_UAT_TRUTH_REQUEST_FAMILY = "validation_or_uat_truth_request"
UI_API_CLOUD_PRODUCTIZATION_REQUEST_FAMILY = "ui_api_cloud_productization_request"
SUPPORTED_OUT_OF_SCOPE_WORKFLOW_EXPANSION_REQUEST_FAMILIES = (
    APPROVAL_OR_RELEASE_REQUEST_FAMILY,
    WORKFLOW_STATE_MUTATION_REQUEST_FAMILY,
    ACTION_EXECUTION_REQUEST_FAMILY,
    AUTONOMOUS_AGENTIC_BEHAVIOR_REQUEST_FAMILY,
    DOCUMENT_GENERATION_REQUEST_FAMILY,
    REPORT_GENERATION_REQUEST_FAMILY,
    PRODUCT_READY_RENDERING_REQUEST_FAMILY,
    PROMPT_TEMPLATE_REQUEST_FAMILY,
    DIRECT_LLM_CALL_REQUEST_FAMILY,
    VALIDATION_OR_UAT_TRUTH_REQUEST_FAMILY,
    UI_API_CLOUD_PRODUCTIZATION_REQUEST_FAMILY,
)

WORKFLOW_EXPANSION_ALLOWED = "workflow_expansion_allowed"
WORKFLOW_EXPANSION_REFUSED = "workflow_expansion_refused"
WORKFLOW_EXPANSION_FALLBACK_ONLY = "workflow_expansion_fallback_only"
SUPPORTED_WORKFLOW_EXPANSION_DECISIONS = (
    WORKFLOW_EXPANSION_ALLOWED,
    WORKFLOW_EXPANSION_REFUSED,
    WORKFLOW_EXPANSION_FALLBACK_ONLY,
)

APPROVAL_OR_RELEASE_REFUSAL = "approval_or_release_refusal"
WORKFLOW_STATE_MUTATION_REFUSAL = "workflow_state_mutation_refusal"
ACTION_EXECUTION_REFUSAL = "action_execution_refusal"
AUTONOMOUS_AGENTIC_BEHAVIOR_REFUSAL = "autonomous_agentic_behavior_refusal"
DOCUMENT_GENERATION_REFUSAL = "document_generation_refusal"
REPORT_GENERATION_REFUSAL = "report_generation_refusal"
PRODUCT_READY_RENDERING_REFUSAL = "product_ready_rendering_refusal"
PROMPT_TEMPLATE_OR_DIRECT_LLM_REFUSAL = "prompt_template_or_direct_llm_refusal"
VALIDATION_OR_UAT_TRUTH_REFUSAL = "validation_or_uat_truth_refusal"
UI_API_CLOUD_PRODUCTIZATION_REFUSAL = "ui_api_cloud_productization_refusal"
UNSUPPORTED_WORKFLOW_EXPANSION_FAMILY_REFUSAL = "unsupported_workflow_expansion_family_refusal"
SUPPORTED_WORKFLOW_EXPANSION_REFUSAL_REASONS = (
    APPROVAL_OR_RELEASE_REFUSAL,
    WORKFLOW_STATE_MUTATION_REFUSAL,
    ACTION_EXECUTION_REFUSAL,
    AUTONOMOUS_AGENTIC_BEHAVIOR_REFUSAL,
    DOCUMENT_GENERATION_REFUSAL,
    REPORT_GENERATION_REFUSAL,
    PRODUCT_READY_RENDERING_REFUSAL,
    PROMPT_TEMPLATE_OR_DIRECT_LLM_REFUSAL,
    VALIDATION_OR_UAT_TRUTH_REFUSAL,
    UI_API_CLOUD_PRODUCTIZATION_REFUSAL,
    UNSUPPORTED_WORKFLOW_EXPANSION_FAMILY_REFUSAL,
)

INSUFFICIENT_EVIDENCE_FALLBACK = "insufficient_evidence_fallback"
NON_AUTHORITATIVE_SOURCE_FALLBACK = "non_authoritative_source_fallback"
MISSING_CONTRACT_CONTEXT_FALLBACK = "missing_contract_context_fallback"
HUMAN_REVIEW_REQUIRED_FALLBACK = "human_review_required_fallback"
SUPPORTED_WORKFLOW_EXPANSION_FALLBACK_REASONS = (
    INSUFFICIENT_EVIDENCE_FALLBACK,
    NON_AUTHORITATIVE_SOURCE_FALLBACK,
    MISSING_CONTRACT_CONTEXT_FALLBACK,
    HUMAN_REVIEW_REQUIRED_FALLBACK,
)

_PROHIBITED_WORKFLOW_EXPANSION_FIELDS = (
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
    "generated_recommendation_text",
    "generated_summary_text",
    "document_factory_payload",
    "document_template_payload",
    "document_generation_payload",
    "report_generation_payload",
    "document_renderer_payload",
    "product_ready_document_payload",
    "product_ready_report_payload",
    "export_payload",
    "dashboard_payload",
    "state_mutation_payload",
    "action_execution_payload",
    "autonomous_agent_payload",
    "approval_payload",
    "workflow_release_payload",
    "repository_write_payload",
    "issue_creation_payload",
    "pull_request_creation_payload",
    "ui_api_payload",
    "cloud_deployment_payload",
    "saas_productization_payload",
    "execution_truth_override",
    "source_truth_override",
    "validation_truth_override",
    "standards_truth_override",
)

_REQUEST_BOOLEAN_FLAGS = (
    "approval_requested",
    "release_requested",
    "state_mutation_requested",
    "action_execution_requested",
    "autonomous_action_requested",
    "document_generation_requested",
    "report_generation_requested",
    "product_ready_rendering_requested",
    "prompt_template_requested",
    "direct_llm_call_requested",
    "validation_truth_requested",
    "uat_truth_requested",
    "ui_api_behavior_requested",
    "cloud_or_saas_behavior_requested",
)

_DECISION_REQUIRED_FALSE_FIELDS = (
    "ai_can_approve",
    "ai_can_release",
    "ai_can_mutate_workflow_state",
    "ai_can_execute_actions",
    "ai_can_run_autonomously",
    "ai_can_replace_human_decision",
    "ai_can_generate_document",
    "ai_can_generate_report",
    "ai_can_render_product_ready_output",
    "ai_can_create_prompt_template",
    "ai_can_call_llm_directly",
    "ai_can_claim_validation_or_uat_truth",
    "ai_can_create_ui_api_cloud_or_saas_behavior",
    "approval_payload_included",
    "workflow_release_payload_included",
    "state_mutation_payload_included",
    "action_execution_payload_included",
    "document_generation_payload_included",
    "report_generation_payload_included",
    "product_ready_rendering_payload_included",
    "prompt_template_payload_included",
    "direct_llm_call_payload_included",
    "validation_or_uat_truth_claimed",
)


def build_ai_workflow_expansion_boundaries_baseline() -> dict[str, Any]:
    """Return the M18.4 workflow-expansion boundary and refusal-rule baseline."""
    return {
        "checkpoint": AI_WORKFLOW_EXPANSION_BOUNDARIES_CHECKPOINT_ID,
        "contract_version": AI_WORKFLOW_EXPANSION_BOUNDARIES_CONTRACT_VERSION,
        "boundary_gate_role": ADVISORY_WORKFLOW_EXPANSION_BOUNDARY_GATE_ROLE,
        "supported_allowed_request_families": list(SUPPORTED_ALLOWED_WORKFLOW_EXPANSION_REQUEST_FAMILIES),
        "supported_fallback_only_request_families": list(
            SUPPORTED_FALLBACK_ONLY_WORKFLOW_EXPANSION_REQUEST_FAMILIES
        ),
        "supported_out_of_scope_request_families": list(
            SUPPORTED_OUT_OF_SCOPE_WORKFLOW_EXPANSION_REQUEST_FAMILIES
        ),
        "supported_workflow_expansion_decisions": list(SUPPORTED_WORKFLOW_EXPANSION_DECISIONS),
        "supported_refusal_reasons": list(SUPPORTED_WORKFLOW_EXPANSION_REFUSAL_REASONS),
        "supported_fallback_reasons": list(SUPPORTED_WORKFLOW_EXPANSION_FALLBACK_REASONS),
        "authority_policy": (
            "workflow_expansion_boundary_gate_may_route_to_bounded_advisory_assistance_only_"
            "and_cannot_approve_release_mutate_workflow_execute_actions_generate_documents_"
            "render_product_outputs_create_prompt_templates_or_claim_validation_truth"
        ),
        "fallback_policy": (
            "out_of_scope_or_insufficiently_grounded_requests_must_fail_closed_or_return_"
            "deterministic_refusal_or_fallback_metadata"
        ),
        "not_owned_by_m18_4": [
            "actual_llm_calls",
            "prompt_templates",
            "document_factory",
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
            "milestone_validation_checkpoint",
            "milestone_uat_checkpoint",
            "milestone_closeout",
        ],
    }


def build_workflow_expansion_boundary_request(
    *,
    workflow_expansion_request_id: str,
    source_quality_gate_result: dict[str, object],
    expansion_request_ref: str,
    expansion_request_family: str,
    workflow_expansion_evidence_refs: list[str] | None = None,
    source_refs_used_as_truth: list[str] | None = None,
    approval_requested: bool = False,
    release_requested: bool = False,
    state_mutation_requested: bool = False,
    action_execution_requested: bool = False,
    autonomous_action_requested: bool = False,
    document_generation_requested: bool = False,
    report_generation_requested: bool = False,
    product_ready_rendering_requested: bool = False,
    prompt_template_requested: bool = False,
    direct_llm_call_requested: bool = False,
    validation_truth_requested: bool = False,
    uat_truth_requested: bool = False,
    ui_api_behavior_requested: bool = False,
    cloud_or_saas_behavior_requested: bool = False,
) -> dict[str, object]:
    """Build and validate an M18.4 workflow-expansion boundary request."""
    validate_ai_quality_gate_result(source_quality_gate_result)
    request = {
        "checkpoint": AI_WORKFLOW_EXPANSION_BOUNDARIES_CHECKPOINT_ID,
        "contract_version": AI_WORKFLOW_EXPANSION_BOUNDARIES_CONTRACT_VERSION,
        "workflow_expansion_request_id": _require_non_empty_string(
            workflow_expansion_request_id,
            "workflow_expansion_request_id",
        ),
        "workflow_expansion_request_status": AI_WORKFLOW_EXPANSION_REQUEST_STATUS_VALIDATED,
        "expansion_request_ref": _parse_version_pinned_ref(expansion_request_ref, "expansion_request_ref"),
        "expansion_request_family": _require_non_empty_string(
            expansion_request_family,
            "expansion_request_family",
        ),
        "requested_boundary_gate_role": ADVISORY_WORKFLOW_EXPANSION_BOUNDARY_GATE_ROLE,
        "source_quality_gate_result_id": str(source_quality_gate_result["quality_gate_result_id"]),
        "source_quality_gate_result": dict(source_quality_gate_result),
        "workflow_expansion_evidence_refs": _normalize_ref_list(
            workflow_expansion_evidence_refs
            if workflow_expansion_evidence_refs is not None
            else _quality_gate_evidence_refs(source_quality_gate_result),
            "workflow_expansion_evidence_refs",
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
        "product_ready_rendering_requested": product_ready_rendering_requested,
        "prompt_template_requested": prompt_template_requested,
        "direct_llm_call_requested": direct_llm_call_requested,
        "validation_truth_requested": validation_truth_requested,
        "uat_truth_requested": uat_truth_requested,
        "ui_api_behavior_requested": ui_api_behavior_requested,
        "cloud_or_saas_behavior_requested": cloud_or_saas_behavior_requested,
        "document_factory_in_scope": False,
        "actual_document_generation_in_scope": False,
        "actual_report_generation_in_scope": False,
        "product_ready_rendering_in_scope": False,
        "workflow_mutation_authority_claimed": False,
        "action_execution_authority_claimed": False,
        "autonomous_action_authority_claimed": False,
        "approval_authority_claimed": False,
        "release_authority_claimed": False,
        "validation_truth_authority_claimed": False,
        "workflow_expansion_output_policy": "decision_metadata_only_no_action_or_generation_payload",
    }
    validate_workflow_expansion_boundary_request(request)
    return request


def validate_workflow_expansion_boundary_request(request: dict[str, object]) -> None:
    """Validate one M18.4 workflow-expansion boundary request."""
    _validate_prohibited_fields(request)
    _validate_required_string_fields(
        request,
        (
            "checkpoint",
            "contract_version",
            "workflow_expansion_request_id",
            "workflow_expansion_request_status",
            "expansion_request_ref",
            "expansion_request_family",
            "requested_boundary_gate_role",
            "source_quality_gate_result_id",
        ),
        "AI workflow-expansion boundary request",
    )
    _validate_exact(request, "checkpoint", AI_WORKFLOW_EXPANSION_BOUNDARIES_CHECKPOINT_ID)
    _validate_exact(request, "contract_version", AI_WORKFLOW_EXPANSION_BOUNDARIES_CONTRACT_VERSION)
    _validate_exact(
        request,
        "workflow_expansion_request_status",
        AI_WORKFLOW_EXPANSION_REQUEST_STATUS_VALIDATED,
    )
    _validate_exact(
        request,
        "requested_boundary_gate_role",
        ADVISORY_WORKFLOW_EXPANSION_BOUNDARY_GATE_ROLE,
    )
    source_quality_gate = request.get("source_quality_gate_result")
    if not isinstance(source_quality_gate, dict):
        raise ValueError("AI workflow-expansion boundary request must include source_quality_gate_result dict.")
    validate_ai_quality_gate_result(source_quality_gate)
    if source_quality_gate.get("quality_gate_result") != QUALITY_GATE_PASS:
        raise ValueError("AI workflow-expansion boundary request requires a passing source quality gate.")
    if request["source_quality_gate_result_id"] != source_quality_gate["quality_gate_result_id"]:
        raise ValueError(
            "AI workflow-expansion boundary request source_quality_gate_result_id must match payload."
        )
    _parse_version_pinned_ref(request["expansion_request_ref"], "expansion_request_ref")
    _validate_boolean_fields(request, _REQUEST_BOOLEAN_FLAGS, "AI workflow-expansion boundary request")
    _validate_required_false_fields(
        request,
        (
            "document_factory_in_scope",
            "actual_document_generation_in_scope",
            "actual_report_generation_in_scope",
            "product_ready_rendering_in_scope",
            "workflow_mutation_authority_claimed",
            "action_execution_authority_claimed",
            "autonomous_action_authority_claimed",
            "approval_authority_claimed",
            "release_authority_claimed",
            "validation_truth_authority_claimed",
        ),
        "AI workflow-expansion boundary request",
    )
    _validate_refs_subset(
        declared=_normalize_ref_list(
            request.get("workflow_expansion_evidence_refs"),
            "workflow_expansion_evidence_refs",
        ),
        allowed=_quality_gate_evidence_refs(source_quality_gate),
        field_name="workflow_expansion_evidence_refs",
    )
    _validate_refs_subset(
        declared=_normalize_ref_list(request.get("source_refs_used_as_truth"), "source_refs_used_as_truth"),
        allowed=_quality_gate_truth_refs(source_quality_gate),
        field_name="source_refs_used_as_truth",
    )
    classify_workflow_expansion_request(request)


def classify_workflow_expansion_request(request: dict[str, object]) -> str:
    """Return the deterministic M18.4 decision class for a workflow-expansion request."""
    _validate_prohibited_fields(request)
    family = _require_non_empty_string(request.get("expansion_request_family"), "expansion_request_family")
    if _deterministic_refusal_reasons(request):
        return WORKFLOW_EXPANSION_REFUSED
    if family in SUPPORTED_FALLBACK_ONLY_WORKFLOW_EXPANSION_REQUEST_FAMILIES:
        return WORKFLOW_EXPANSION_FALLBACK_ONLY
    if family in SUPPORTED_ALLOWED_WORKFLOW_EXPANSION_REQUEST_FAMILIES:
        return WORKFLOW_EXPANSION_ALLOWED
    return WORKFLOW_EXPANSION_REFUSED


def build_workflow_expansion_boundary_decision(
    *,
    workflow_expansion_decision_id: str,
    workflow_expansion_request: dict[str, object],
) -> dict[str, object]:
    """Build and validate a deterministic M18.4 workflow-expansion boundary decision."""
    validate_workflow_expansion_boundary_request(workflow_expansion_request)
    decision = classify_workflow_expansion_request(workflow_expansion_request)
    refusal_reasons = _deterministic_refusal_reasons(workflow_expansion_request)
    fallback_reasons = _deterministic_fallback_reasons(workflow_expansion_request)
    boundary_decision = {
        "checkpoint": AI_WORKFLOW_EXPANSION_BOUNDARIES_CHECKPOINT_ID,
        "contract_version": AI_WORKFLOW_EXPANSION_BOUNDARIES_CONTRACT_VERSION,
        "workflow_expansion_decision_id": _require_non_empty_string(
            workflow_expansion_decision_id,
            "workflow_expansion_decision_id",
        ),
        "workflow_expansion_decision_status": AI_WORKFLOW_EXPANSION_DECISION_STATUS_VALIDATED,
        "workflow_expansion_request_id": str(workflow_expansion_request["workflow_expansion_request_id"]),
        "expansion_request_ref": str(workflow_expansion_request["expansion_request_ref"]),
        "expansion_request_family": str(workflow_expansion_request["expansion_request_family"]),
        "workflow_expansion_decision": decision,
        "refusal_reasons": refusal_reasons,
        "fallback_reasons": fallback_reasons,
        "source_workflow_expansion_request": dict(workflow_expansion_request),
        "advisory_only": True,
        "human_review_required": True,
        "may_route_to_controlled_review_assistance": (
            decision == WORKFLOW_EXPANSION_ALLOWED
            and workflow_expansion_request["expansion_request_family"]
            == CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY
        ),
        "may_route_to_controlled_summarization_reporting_assistance": (
            decision == WORKFLOW_EXPANSION_ALLOWED
            and workflow_expansion_request["expansion_request_family"]
            == CONTROLLED_SUMMARIZATION_REPORTING_ASSISTANCE_REQUEST_FAMILY
        ),
        "may_route_to_controlled_recommendation_assistance": (
            decision == WORKFLOW_EXPANSION_ALLOWED
            and workflow_expansion_request["expansion_request_family"]
            == CONTROLLED_RECOMMENDATION_ASSISTANCE_REQUEST_FAMILY
        ),
        "may_emit_boundary_metadata": decision in (WORKFLOW_EXPANSION_ALLOWED, WORKFLOW_EXPANSION_FALLBACK_ONLY),
        "ai_can_approve": False,
        "ai_can_release": False,
        "ai_can_mutate_workflow_state": False,
        "ai_can_execute_actions": False,
        "ai_can_run_autonomously": False,
        "ai_can_replace_human_decision": False,
        "ai_can_generate_document": False,
        "ai_can_generate_report": False,
        "ai_can_render_product_ready_output": False,
        "ai_can_create_prompt_template": False,
        "ai_can_call_llm_directly": False,
        "ai_can_claim_validation_or_uat_truth": False,
        "ai_can_create_ui_api_cloud_or_saas_behavior": False,
        "approval_payload_included": False,
        "workflow_release_payload_included": False,
        "state_mutation_payload_included": False,
        "action_execution_payload_included": False,
        "document_generation_payload_included": False,
        "report_generation_payload_included": False,
        "product_ready_rendering_payload_included": False,
        "prompt_template_payload_included": False,
        "direct_llm_call_payload_included": False,
        "validation_or_uat_truth_claimed": False,
        "decision_output_policy": "decision_metadata_only_no_execution_generation_or_truth_payload",
    }
    validate_workflow_expansion_boundary_decision(boundary_decision)
    return boundary_decision


def validate_workflow_expansion_boundary_decision(decision: dict[str, object]) -> None:
    """Validate one deterministic M18.4 workflow-expansion boundary decision."""
    _validate_prohibited_fields(decision)
    _validate_required_string_fields(
        decision,
        (
            "checkpoint",
            "contract_version",
            "workflow_expansion_decision_id",
            "workflow_expansion_decision_status",
            "workflow_expansion_request_id",
            "expansion_request_ref",
            "expansion_request_family",
            "workflow_expansion_decision",
        ),
        "AI workflow-expansion boundary decision",
    )
    _validate_exact(decision, "checkpoint", AI_WORKFLOW_EXPANSION_BOUNDARIES_CHECKPOINT_ID)
    _validate_exact(decision, "contract_version", AI_WORKFLOW_EXPANSION_BOUNDARIES_CONTRACT_VERSION)
    _validate_exact(
        decision,
        "workflow_expansion_decision_status",
        AI_WORKFLOW_EXPANSION_DECISION_STATUS_VALIDATED,
    )
    if decision.get("advisory_only") is not True:
        raise ValueError("AI workflow-expansion boundary decision must be advisory_only.")
    if decision.get("human_review_required") is not True:
        raise ValueError("AI workflow-expansion boundary decision must require human review.")
    for field_name in _DECISION_REQUIRED_FALSE_FIELDS:
        if decision.get(field_name) is not False:
            raise ValueError(f"AI workflow-expansion boundary decision requires {field_name} to be False.")
    request = decision.get("source_workflow_expansion_request")
    if not isinstance(request, dict):
        raise ValueError(
            "AI workflow-expansion boundary decision must include source_workflow_expansion_request dict."
        )
    validate_workflow_expansion_boundary_request(request)
    for field_name in ("workflow_expansion_request_id", "expansion_request_ref", "expansion_request_family"):
        if decision[field_name] != request[field_name]:
            raise ValueError(f"AI workflow-expansion boundary decision {field_name} must match request.")

    expected_decision = classify_workflow_expansion_request(request)
    if decision["workflow_expansion_decision"] != expected_decision:
        raise ValueError("AI workflow-expansion boundary decision does not match deterministic classification.")
    _normalize_supported_value(
        decision["workflow_expansion_decision"],
        "workflow_expansion_decision",
        SUPPORTED_WORKFLOW_EXPANSION_DECISIONS,
    )

    refusal_reasons = _normalize_reason_list(decision.get("refusal_reasons"), "refusal_reasons")
    fallback_reasons = _normalize_reason_list(decision.get("fallback_reasons"), "fallback_reasons")
    expected_refusal_reasons = _deterministic_refusal_reasons(request)
    expected_fallback_reasons = _deterministic_fallback_reasons(request)
    if refusal_reasons != expected_refusal_reasons:
        raise ValueError("AI workflow-expansion boundary decision refusal_reasons must match request.")
    if fallback_reasons != expected_fallback_reasons:
        raise ValueError("AI workflow-expansion boundary decision fallback_reasons must match request.")
    if expected_decision == WORKFLOW_EXPANSION_REFUSED and not refusal_reasons:
        raise ValueError("AI workflow-expansion refused decision must include refusal reasons.")
    if expected_decision == WORKFLOW_EXPANSION_FALLBACK_ONLY and not fallback_reasons:
        raise ValueError("AI workflow-expansion fallback-only decision must include fallback reasons.")
    if expected_decision == WORKFLOW_EXPANSION_ALLOWED and (refusal_reasons or fallback_reasons):
        raise ValueError("AI workflow-expansion allowed decision must not include refusal or fallback reasons.")


def _deterministic_refusal_reasons(request: dict[str, object]) -> list[str]:
    reasons: list[str] = []
    family = str(request.get("expansion_request_family", "")).strip()
    if family == APPROVAL_OR_RELEASE_REQUEST_FAMILY:
        reasons.append(APPROVAL_OR_RELEASE_REFUSAL)
    if family == WORKFLOW_STATE_MUTATION_REQUEST_FAMILY:
        reasons.append(WORKFLOW_STATE_MUTATION_REFUSAL)
    if family == ACTION_EXECUTION_REQUEST_FAMILY:
        reasons.append(ACTION_EXECUTION_REFUSAL)
    if family == AUTONOMOUS_AGENTIC_BEHAVIOR_REQUEST_FAMILY:
        reasons.append(AUTONOMOUS_AGENTIC_BEHAVIOR_REFUSAL)
    if family == DOCUMENT_GENERATION_REQUEST_FAMILY:
        reasons.append(DOCUMENT_GENERATION_REFUSAL)
    if family == REPORT_GENERATION_REQUEST_FAMILY:
        reasons.append(REPORT_GENERATION_REFUSAL)
    if family == PRODUCT_READY_RENDERING_REQUEST_FAMILY:
        reasons.append(PRODUCT_READY_RENDERING_REFUSAL)
    if family in (PROMPT_TEMPLATE_REQUEST_FAMILY, DIRECT_LLM_CALL_REQUEST_FAMILY):
        reasons.append(PROMPT_TEMPLATE_OR_DIRECT_LLM_REFUSAL)
    if family == VALIDATION_OR_UAT_TRUTH_REQUEST_FAMILY:
        reasons.append(VALIDATION_OR_UAT_TRUTH_REFUSAL)
    if family == UI_API_CLOUD_PRODUCTIZATION_REQUEST_FAMILY:
        reasons.append(UI_API_CLOUD_PRODUCTIZATION_REFUSAL)

    if request.get("approval_requested") is True or request.get("release_requested") is True:
        reasons.append(APPROVAL_OR_RELEASE_REFUSAL)
    if request.get("state_mutation_requested") is True:
        reasons.append(WORKFLOW_STATE_MUTATION_REFUSAL)
    if request.get("action_execution_requested") is True:
        reasons.append(ACTION_EXECUTION_REFUSAL)
    if request.get("autonomous_action_requested") is True:
        reasons.append(AUTONOMOUS_AGENTIC_BEHAVIOR_REFUSAL)
    if request.get("document_generation_requested") is True:
        reasons.append(DOCUMENT_GENERATION_REFUSAL)
    if request.get("report_generation_requested") is True:
        reasons.append(REPORT_GENERATION_REFUSAL)
    if request.get("product_ready_rendering_requested") is True:
        reasons.append(PRODUCT_READY_RENDERING_REFUSAL)
    if request.get("prompt_template_requested") is True or request.get("direct_llm_call_requested") is True:
        reasons.append(PROMPT_TEMPLATE_OR_DIRECT_LLM_REFUSAL)
    if request.get("validation_truth_requested") is True or request.get("uat_truth_requested") is True:
        reasons.append(VALIDATION_OR_UAT_TRUTH_REFUSAL)
    if request.get("ui_api_behavior_requested") is True or request.get("cloud_or_saas_behavior_requested") is True:
        reasons.append(UI_API_CLOUD_PRODUCTIZATION_REFUSAL)

    known_families = (
        SUPPORTED_ALLOWED_WORKFLOW_EXPANSION_REQUEST_FAMILIES
        + SUPPORTED_FALLBACK_ONLY_WORKFLOW_EXPANSION_REQUEST_FAMILIES
        + SUPPORTED_OUT_OF_SCOPE_WORKFLOW_EXPANSION_REQUEST_FAMILIES
    )
    if family and family not in known_families:
        reasons.append(UNSUPPORTED_WORKFLOW_EXPANSION_FAMILY_REFUSAL)
    return sorted(_deduplicate(reasons))


def _deterministic_fallback_reasons(request: dict[str, object]) -> list[str]:
    family = str(request.get("expansion_request_family", "")).strip()
    reasons: list[str] = []
    if family == INSUFFICIENT_EVIDENCE_FALLBACK_REQUEST_FAMILY:
        reasons.append(INSUFFICIENT_EVIDENCE_FALLBACK)
    if family == NON_AUTHORITATIVE_SOURCE_FALLBACK_REQUEST_FAMILY:
        reasons.append(NON_AUTHORITATIVE_SOURCE_FALLBACK)
    if family == MISSING_CONTRACT_CONTEXT_FALLBACK_REQUEST_FAMILY:
        reasons.append(MISSING_CONTRACT_CONTEXT_FALLBACK)
    if family in SUPPORTED_FALLBACK_ONLY_WORKFLOW_EXPANSION_REQUEST_FAMILIES:
        reasons.append(HUMAN_REVIEW_REQUIRED_FALLBACK)
    return sorted(_deduplicate(reasons))


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
        raise ValueError("AI workflow-expansion boundary requires source_groundedness_check dict.")
    return groundedness


def _validate_refs_subset(*, declared: list[str], allowed: list[str], field_name: str) -> None:
    allowed_set = set(allowed)
    for ref in declared:
        if ref not in allowed_set:
            raise ValueError(
                "AI workflow-expansion boundary request "
                f"{field_name} includes ref outside the passed source quality gate: {ref}."
            )


def _parse_version_pinned_ref(raw_ref: object, field_name: str) -> str:
    ref = _require_non_empty_string(raw_ref, field_name)
    return parse_version_pinned_asset_ref(ref)["asset_ref"]


def _normalize_ref_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"AI workflow-expansion boundary requires non-empty list {field_name}.")
    refs = [_parse_version_pinned_ref(raw_ref, field_name) for raw_ref in value]
    return sorted(_deduplicate(refs))


def _normalize_reason_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"AI workflow-expansion boundary decision requires list {field_name}.")
    reasons = [_require_non_empty_string(raw_reason, field_name) for raw_reason in value]
    return sorted(_deduplicate(reasons))


def _normalize_supported_value(value: object, field_name: str, supported_values: tuple[str, ...]) -> str:
    normalized = _require_non_empty_string(value, field_name)
    if normalized not in supported_values:
        raise ValueError(
            f"AI workflow-expansion boundary declares unsupported {field_name}. "
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
        raise ValueError(f"AI workflow-expansion boundary must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(payload: dict[str, object], required_fields: tuple[str, ...], label: str) -> None:
    for field_name in required_fields:
        _require_non_empty_string(payload.get(field_name), field_name)


def _validate_boolean_fields(payload: dict[str, object], fields: tuple[str, ...], label: str) -> None:
    for field_name in fields:
        if not isinstance(payload.get(field_name), bool):
            raise ValueError(f"{label} requires boolean {field_name}.")


def _validate_required_false_fields(
    payload: dict[str, object],
    fields: tuple[str, ...],
    label: str,
) -> None:
    for field_name in fields:
        if payload.get(field_name) is not False:
            raise ValueError(f"{label} requires {field_name} to be False.")


def _validate_exact(payload: dict[str, object], field_name: str, expected_value: str) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            "AI workflow-expansion boundary declares invalid "
            f"{field_name}: expected {expected_value!r}, got {actual_value!r}."
        )


def _validate_prohibited_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_WORKFLOW_EXPANSION_FIELDS:
        if field_name in payload:
            raise ValueError(f"{field_name} is not allowed in M18.4 workflow-expansion boundary payloads.")
