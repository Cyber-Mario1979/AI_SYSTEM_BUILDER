"AI-assisted controlled summarization and reporting support for M18.2."

from __future__ import annotations

from typing import Any

from asbp.ai_evaluation import QUALITY_GATE_PASS, validate_ai_quality_gate_result
from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID = "M18.2"
AI_CONTROLLED_SUMMARIZATION_REPORTING_CONTRACT_VERSION = "ai-controlled-summarization-reporting-v1"
AI_SUMMARIZATION_REPORTING_REQUEST_STATUS_VALIDATED = "ai_summarization_reporting_request_validated"
AI_SUMMARIZATION_REPORTING_RESULT_STATUS_VALIDATED = "ai_summarization_reporting_result_validated"
AI_SUMMARIZATION_REPORTING_FINDING_STATUS_VALIDATED = "ai_summarization_reporting_finding_validated"

ADVISORY_SUMMARIZATION_REPORTING_ASSISTANCE_ROLE = "advisory_summarization_reporting_assistance"

DOCUMENT_ARTIFACT_SUMMARY_TARGET = "document_artifact_summary_target"
REPORTING_ARTIFACT_SUMMARY_TARGET = "reporting_artifact_summary_target"
WORKFLOW_STATE_SUMMARY_TARGET = "workflow_state_summary_target"
AI_OUTPUT_SUMMARY_TARGET = "ai_output_summary_target"
SUPPORTED_SUMMARIZATION_REPORTING_TARGET_FAMILIES = (
    DOCUMENT_ARTIFACT_SUMMARY_TARGET,
    REPORTING_ARTIFACT_SUMMARY_TARGET,
    WORKFLOW_STATE_SUMMARY_TARGET,
    AI_OUTPUT_SUMMARY_TARGET,
)

EVIDENCE_BOUND_SUMMARIZATION_MODE = "evidence_bound_summarization"
CONTRACT_ALIGNED_SUMMARIZATION_MODE = "contract_aligned_summarization"
GAP_AND_RISK_SUMMARIZATION_MODE = "gap_and_risk_summarization"
SUPPORTED_SUMMARIZATION_MODES = (
    EVIDENCE_BOUND_SUMMARIZATION_MODE,
    CONTRACT_ALIGNED_SUMMARIZATION_MODE,
    GAP_AND_RISK_SUMMARIZATION_MODE,
)

STATUS_SUMMARY_REPORTING_MODE = "status_summary_reporting"
DETAIL_DISCIPLINE_REPORTING_MODE = "detail_discipline_reporting"
EVIDENCE_TRACE_REPORTING_MODE = "evidence_trace_reporting"
SUPPORTED_REPORTING_ASSISTANCE_MODES = (
    STATUS_SUMMARY_REPORTING_MODE,
    DETAIL_DISCIPLINE_REPORTING_MODE,
    EVIDENCE_TRACE_REPORTING_MODE,
)

SUMMARIZATION_REPORTING_ASSISTANCE_READY = "summarization_reporting_assistance_ready"
SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED = "summarization_reporting_assistance_findings_identified"
SUPPORTED_SUMMARIZATION_REPORTING_ASSISTANCE_RESULTS = (
    SUMMARIZATION_REPORTING_ASSISTANCE_READY,
    SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED,
)

SUMMARY_CONTRACT_ALIGNMENT_FINDING = "summary_contract_alignment_finding"
SUMMARY_EVIDENCE_GAP_FINDING = "summary_evidence_gap_finding"
SUMMARY_ASSUMPTION_LABELING_FINDING = "summary_assumption_labeling_finding"
SUMMARY_SOURCE_ROLE_DISCIPLINE_FINDING = "summary_source_role_discipline_finding"
REPORTING_DETAIL_DISCIPLINE_FINDING = "reporting_detail_discipline_finding"
SUMMARY_REPORT_APPROVAL_AUTHORITY_BOUNDARY_FINDING = "summary_report_approval_authority_boundary_finding"
SUMMARY_REPORT_WORKFLOW_STATE_MUTATION_BOUNDARY_FINDING = "summary_report_workflow_state_mutation_boundary_finding"
SUMMARY_REPORT_DOCUMENT_GENERATION_BOUNDARY_FINDING = "summary_report_document_generation_boundary_finding"
SUMMARY_REPORT_REPORT_GENERATION_BOUNDARY_FINDING = "summary_report_report_generation_boundary_finding"
SUMMARY_REPORT_PRODUCT_RENDERING_BOUNDARY_FINDING = "summary_report_product_rendering_boundary_finding"
SUMMARY_REPORT_RECOMMENDATION_BOUNDARY_FINDING = "summary_report_recommendation_boundary_finding"
SUMMARY_REPORT_VALIDATION_TRUTH_BOUNDARY_FINDING = "summary_report_validation_truth_boundary_finding"
SUPPORTED_SUMMARIZATION_REPORTING_FINDING_CATEGORIES = (
    SUMMARY_CONTRACT_ALIGNMENT_FINDING,
    SUMMARY_EVIDENCE_GAP_FINDING,
    SUMMARY_ASSUMPTION_LABELING_FINDING,
    SUMMARY_SOURCE_ROLE_DISCIPLINE_FINDING,
    REPORTING_DETAIL_DISCIPLINE_FINDING,
    SUMMARY_REPORT_APPROVAL_AUTHORITY_BOUNDARY_FINDING,
    SUMMARY_REPORT_WORKFLOW_STATE_MUTATION_BOUNDARY_FINDING,
    SUMMARY_REPORT_DOCUMENT_GENERATION_BOUNDARY_FINDING,
    SUMMARY_REPORT_REPORT_GENERATION_BOUNDARY_FINDING,
    SUMMARY_REPORT_PRODUCT_RENDERING_BOUNDARY_FINDING,
    SUMMARY_REPORT_RECOMMENDATION_BOUNDARY_FINDING,
    SUMMARY_REPORT_VALIDATION_TRUTH_BOUNDARY_FINDING,
)

SUMMARIZATION_REPORTING_FINDING_INFO_SEVERITY = "info"
SUMMARIZATION_REPORTING_FINDING_WARNING_SEVERITY = "warning"
SUMMARIZATION_REPORTING_FINDING_BLOCKING_SEVERITY = "blocking"
SUPPORTED_SUMMARIZATION_REPORTING_FINDING_SEVERITIES = (
    SUMMARIZATION_REPORTING_FINDING_INFO_SEVERITY,
    SUMMARIZATION_REPORTING_FINDING_WARNING_SEVERITY,
    SUMMARIZATION_REPORTING_FINDING_BLOCKING_SEVERITY,
)

_PROHIBITED_SUMMARIZATION_REPORTING_FIELDS = (
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
    "generated_summary_text",
    "generated_report_text",
    "generated_document_text",
    "generated_output_text",
    "summary_narrative_text",
    "report_body_text",
    "report_markdown",
    "report_pdf_payload",
    "document_factory_payload",
    "document_template_payload",
    "document_generation_payload",
    "report_generation_payload",
    "document_renderer_payload",
    "product_ready_report_payload",
    "export_payload",
    "dashboard_payload",
    "library_architecture_payload",
    "recommendation_payload",
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
    "document_generation_requested",
    "report_generation_requested",
    "document_template_product_implementation_requested",
    "product_ready_rendering_requested",
    "recommendation_requested",
    "document_factory_in_scope",
    "actual_document_generation_in_scope",
    "actual_report_generation_in_scope",
    "product_ready_rendering_in_scope",
    "approval_authority_claimed",
    "release_authority_claimed",
    "workflow_mutation_authority_claimed",
    "recommendation_authority_claimed",
)

_RESULT_REQUIRED_FALSE_FIELDS = (
    "ai_can_approve",
    "ai_can_release",
    "ai_can_mutate_workflow_state",
    "ai_can_generate_document",
    "ai_can_generate_report",
    "ai_can_render_product_ready_report",
    "ai_can_recommend",
    "approval_payload_included",
    "workflow_release_payload_included",
    "state_mutation_payload_included",
    "document_generation_payload_included",
    "report_generation_payload_included",
    "product_ready_rendering_payload_included",
    "recommendation_payload_included",
    "validation_or_uat_truth_claimed",
)


def build_controlled_summarization_reporting_baseline() -> dict[str, Any]:
    """Return the M18.2 controlled summarization/reporting baseline."""
    return {
        "checkpoint": AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_SUMMARIZATION_REPORTING_CONTRACT_VERSION,
        "supported_summary_target_families": list(SUPPORTED_SUMMARIZATION_REPORTING_TARGET_FAMILIES),
        "supported_summarization_modes": list(SUPPORTED_SUMMARIZATION_MODES),
        "supported_reporting_assistance_modes": list(SUPPORTED_REPORTING_ASSISTANCE_MODES),
        "supported_finding_categories": list(SUPPORTED_SUMMARIZATION_REPORTING_FINDING_CATEGORIES),
        "supported_finding_severities": list(SUPPORTED_SUMMARIZATION_REPORTING_FINDING_SEVERITIES),
        "supported_assistance_results": list(SUPPORTED_SUMMARIZATION_REPORTING_ASSISTANCE_RESULTS),
        "assistance_role": ADVISORY_SUMMARIZATION_REPORTING_ASSISTANCE_ROLE,
        "authority_policy": (
            "summarization_reporting_assistance_is_advisory_only_and_cannot_approve_release_"
            "mutate_workflow_state_generate_documents_or_render_product_ready_reports"
        ),
        "source_discipline_policy": (
            "summarization_reporting_assistance_must_use_passed_m17_quality_gate_evidence_"
            "and_source_role_context"
        ),
        "detail_discipline_policy": (
            "summarization_reporting_assistance_must_preserve_document_report_family_rules_"
            "evidence_traceability_and_detail_level_discipline"
        ),
        "deferred_scope_policy": (
            "document_factory_document_generation_template_product_implementation_product_ready_"
            "report_rendering_recommendation_behavior_and_library_architecture_cleanup_remain_out_of_scope"
        ),
        "not_owned_by_m18_2": [
            "actual_llm_calls",
            "prompt_templates",
            "document_factory",
            "document_template_product_implementation",
            "actual_document_generation_from_expanded_governed_library_content",
            "actual_report_generation_from_expanded_governed_library_content",
            "product_ready_document_rendering",
            "product_ready_report_rendering",
            "controlled_recommendation_behavior",
            "workflow_state_mutation",
            "approval_or_release_authority",
            "validation_or_uat_truth_claims",
            "ui_api_behavior",
            "cloud_or_saas_productization",
        ],
    }


def build_controlled_summarization_reporting_request(
    *,
    summary_reporting_request_id: str,
    source_quality_gate_result: dict[str, object],
    summary_target_ref: str,
    summary_target_family: str,
    summarization_mode: str,
    reporting_assistance_mode: str,
    summary_evidence_refs: list[str] | None = None,
    source_refs_used_as_truth: list[str] | None = None,
    approval_requested: bool = False,
    release_requested: bool = False,
    state_mutation_requested: bool = False,
    document_generation_requested: bool = False,
    report_generation_requested: bool = False,
    document_template_product_implementation_requested: bool = False,
    product_ready_rendering_requested: bool = False,
    recommendation_requested: bool = False,
) -> dict[str, object]:
    """Build and validate a controlled M18.2 summarization/reporting request."""
    validate_ai_quality_gate_result(source_quality_gate_result)
    request = {
        "checkpoint": AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_SUMMARIZATION_REPORTING_CONTRACT_VERSION,
        "summary_reporting_request_id": _require_non_empty_string(
            summary_reporting_request_id,
            "summary_reporting_request_id",
        ),
        "summary_reporting_request_status": AI_SUMMARIZATION_REPORTING_REQUEST_STATUS_VALIDATED,
        "summary_target_ref": _parse_version_pinned_ref(summary_target_ref, "summary_target_ref"),
        "summary_target_family": _normalize_supported_value(
            summary_target_family,
            "summary_target_family",
            SUPPORTED_SUMMARIZATION_REPORTING_TARGET_FAMILIES,
        ),
        "summarization_mode": _normalize_supported_value(
            summarization_mode,
            "summarization_mode",
            SUPPORTED_SUMMARIZATION_MODES,
        ),
        "reporting_assistance_mode": _normalize_supported_value(
            reporting_assistance_mode,
            "reporting_assistance_mode",
            SUPPORTED_REPORTING_ASSISTANCE_MODES,
        ),
        "requested_assistance_role": ADVISORY_SUMMARIZATION_REPORTING_ASSISTANCE_ROLE,
        "source_quality_gate_result_id": str(source_quality_gate_result["quality_gate_result_id"]),
        "source_quality_gate_result": dict(source_quality_gate_result),
        "summary_evidence_refs": _normalize_ref_list(
            summary_evidence_refs
            if summary_evidence_refs is not None
            else _quality_gate_evidence_refs(source_quality_gate_result),
            "summary_evidence_refs",
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
        "document_generation_requested": document_generation_requested,
        "report_generation_requested": report_generation_requested,
        "document_template_product_implementation_requested": document_template_product_implementation_requested,
        "product_ready_rendering_requested": product_ready_rendering_requested,
        "recommendation_requested": recommendation_requested,
        "document_factory_in_scope": False,
        "actual_document_generation_in_scope": False,
        "actual_report_generation_in_scope": False,
        "product_ready_rendering_in_scope": False,
        "approval_authority_claimed": False,
        "release_authority_claimed": False,
        "workflow_mutation_authority_claimed": False,
        "recommendation_authority_claimed": False,
        "summary_output_policy": "structured_metadata_only_no_free_form_generated_summary_text",
        "reporting_output_policy": "assistance_metadata_only_no_product_ready_report_rendering",
    }
    validate_controlled_summarization_reporting_request(request)
    return request


def validate_controlled_summarization_reporting_request(request: dict[str, object]) -> None:
    """Validate one M18.2 controlled summarization/reporting request."""
    _validate_prohibited_fields(request)
    _validate_required_string_fields(
        request,
        (
            "checkpoint",
            "contract_version",
            "summary_reporting_request_id",
            "summary_reporting_request_status",
            "summary_target_ref",
            "summary_target_family",
            "summarization_mode",
            "reporting_assistance_mode",
            "requested_assistance_role",
            "source_quality_gate_result_id",
        ),
        "AI controlled summarization/reporting request",
    )
    _validate_exact(request, "checkpoint", AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID)
    _validate_exact(request, "contract_version", AI_CONTROLLED_SUMMARIZATION_REPORTING_CONTRACT_VERSION)
    _validate_exact(
        request,
        "summary_reporting_request_status",
        AI_SUMMARIZATION_REPORTING_REQUEST_STATUS_VALIDATED,
    )
    _validate_exact(request, "requested_assistance_role", ADVISORY_SUMMARIZATION_REPORTING_ASSISTANCE_ROLE)

    source_quality_gate = request.get("source_quality_gate_result")
    if not isinstance(source_quality_gate, dict):
        raise ValueError("AI controlled summarization/reporting request must include source_quality_gate_result dict.")
    validate_ai_quality_gate_result(source_quality_gate)
    if source_quality_gate.get("quality_gate_result") != QUALITY_GATE_PASS:
        raise ValueError("AI controlled summarization/reporting request requires a passing source quality gate.")
    if request["source_quality_gate_result_id"] != source_quality_gate["quality_gate_result_id"]:
        raise ValueError(
            "AI controlled summarization/reporting request source_quality_gate_result_id must match payload."
        )

    _parse_version_pinned_ref(request["summary_target_ref"], "summary_target_ref")
    _normalize_supported_value(
        request["summary_target_family"],
        "summary_target_family",
        SUPPORTED_SUMMARIZATION_REPORTING_TARGET_FAMILIES,
    )
    _normalize_supported_value(
        request["summarization_mode"],
        "summarization_mode",
        SUPPORTED_SUMMARIZATION_MODES,
    )
    _normalize_supported_value(
        request["reporting_assistance_mode"],
        "reporting_assistance_mode",
        SUPPORTED_REPORTING_ASSISTANCE_MODES,
    )
    for field_name in _REQUEST_REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(f"AI controlled summarization/reporting request requires {field_name} to be False.")

    _validate_refs_subset(
        declared=_normalize_ref_list(request.get("summary_evidence_refs"), "summary_evidence_refs"),
        allowed=_quality_gate_evidence_refs(source_quality_gate),
        field_name="summary_evidence_refs",
    )
    _validate_refs_subset(
        declared=_normalize_ref_list(request.get("source_refs_used_as_truth"), "source_refs_used_as_truth"),
        allowed=_quality_gate_truth_refs(source_quality_gate),
        field_name="source_refs_used_as_truth",
    )


def build_controlled_summarization_reporting_finding(
    *,
    finding_id: str,
    finding_category: str,
    evidence_ref: str,
    source_ref: str,
    finding_severity: str = SUMMARIZATION_REPORTING_FINDING_WARNING_SEVERITY,
) -> dict[str, object]:
    """Build and validate one controlled summarization/reporting finding metadata record."""
    finding = {
        "finding_id": _require_non_empty_string(finding_id, "finding_id"),
        "finding_status": AI_SUMMARIZATION_REPORTING_FINDING_STATUS_VALIDATED,
        "finding_category": _normalize_supported_value(
            finding_category,
            "finding_category",
            SUPPORTED_SUMMARIZATION_REPORTING_FINDING_CATEGORIES,
        ),
        "finding_severity": _normalize_supported_value(
            finding_severity,
            "finding_severity",
            SUPPORTED_SUMMARIZATION_REPORTING_FINDING_SEVERITIES,
        ),
        "evidence_ref": _parse_version_pinned_ref(evidence_ref, "evidence_ref"),
        "source_ref": _parse_version_pinned_ref(source_ref, "source_ref"),
        "finding_language_policy": "metadata_only_no_generated_summary_or_report_narrative",
    }
    validate_controlled_summarization_reporting_finding(finding)
    return finding


def validate_controlled_summarization_reporting_finding(finding: dict[str, object]) -> None:
    """Validate one controlled summarization/reporting finding metadata record."""
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
        "AI controlled summarization/reporting finding",
    )
    _validate_exact(
        finding,
        "finding_status",
        AI_SUMMARIZATION_REPORTING_FINDING_STATUS_VALIDATED,
    )
    _normalize_supported_value(
        finding["finding_category"],
        "finding_category",
        SUPPORTED_SUMMARIZATION_REPORTING_FINDING_CATEGORIES,
    )
    _normalize_supported_value(
        finding["finding_severity"],
        "finding_severity",
        SUPPORTED_SUMMARIZATION_REPORTING_FINDING_SEVERITIES,
    )
    _parse_version_pinned_ref(finding["evidence_ref"], "evidence_ref")
    _parse_version_pinned_ref(finding["source_ref"], "source_ref")


def build_controlled_summarization_reporting_result(
    *,
    summary_reporting_result_id: str,
    summary_reporting_request: dict[str, object],
    summary_reporting_findings: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build and validate a controlled M18.2 summarization/reporting result."""
    validate_controlled_summarization_reporting_request(summary_reporting_request)
    findings = [dict(finding) for finding in summary_reporting_findings or []]
    for finding in findings:
        validate_controlled_summarization_reporting_finding(finding)
    result = {
        "checkpoint": AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_SUMMARIZATION_REPORTING_CONTRACT_VERSION,
        "summary_reporting_result_id": _require_non_empty_string(
            summary_reporting_result_id,
            "summary_reporting_result_id",
        ),
        "summary_reporting_result_status": AI_SUMMARIZATION_REPORTING_RESULT_STATUS_VALIDATED,
        "summary_reporting_request_id": str(summary_reporting_request["summary_reporting_request_id"]),
        "summary_target_ref": str(summary_reporting_request["summary_target_ref"]),
        "summary_target_family": str(summary_reporting_request["summary_target_family"]),
        "summarization_mode": str(summary_reporting_request["summarization_mode"]),
        "reporting_assistance_mode": str(summary_reporting_request["reporting_assistance_mode"]),
        "summarization_reporting_assistance_result": (
            SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED
            if findings
            else SUMMARIZATION_REPORTING_ASSISTANCE_READY
        ),
        "summary_reporting_findings": findings,
        "source_summary_reporting_request": dict(summary_reporting_request),
        "advisory_only": True,
        "ai_can_approve": False,
        "ai_can_release": False,
        "ai_can_mutate_workflow_state": False,
        "ai_can_generate_document": False,
        "ai_can_generate_report": False,
        "ai_can_render_product_ready_report": False,
        "ai_can_recommend": False,
        "approval_payload_included": False,
        "workflow_release_payload_included": False,
        "state_mutation_payload_included": False,
        "document_generation_payload_included": False,
        "report_generation_payload_included": False,
        "product_ready_rendering_payload_included": False,
        "recommendation_payload_included": False,
        "validation_or_uat_truth_claimed": False,
        "summary_authority_policy": "advisory_metadata_only_requires_human_review_for_acceptance",
        "reporting_authority_policy": "reporting_assistance_metadata_only_no_product_ready_rendering",
        "deferred_scope_policy": (
            "document_factory_template_product_implementation_document_generation_report_generation_"
            "product_ready_rendering_recommendation_behavior_and_library_architecture_cleanup_remain_out_of_scope"
        ),
    }
    validate_controlled_summarization_reporting_result(result)
    return result


def validate_controlled_summarization_reporting_result(result: dict[str, object]) -> None:
    """Validate one M18.2 controlled summarization/reporting result."""
    _validate_prohibited_fields(result)
    _validate_required_string_fields(
        result,
        (
            "checkpoint",
            "contract_version",
            "summary_reporting_result_id",
            "summary_reporting_result_status",
            "summary_reporting_request_id",
            "summary_target_ref",
            "summary_target_family",
            "summarization_mode",
            "reporting_assistance_mode",
            "summarization_reporting_assistance_result",
        ),
        "AI controlled summarization/reporting result",
    )
    _validate_exact(result, "checkpoint", AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID)
    _validate_exact(result, "contract_version", AI_CONTROLLED_SUMMARIZATION_REPORTING_CONTRACT_VERSION)
    _validate_exact(
        result,
        "summary_reporting_result_status",
        AI_SUMMARIZATION_REPORTING_RESULT_STATUS_VALIDATED,
    )
    if result.get("advisory_only") is not True:
        raise ValueError("AI controlled summarization/reporting result must be advisory_only.")
    for field_name in _RESULT_REQUIRED_FALSE_FIELDS:
        if result.get(field_name) is not False:
            raise ValueError(f"AI controlled summarization/reporting result requires {field_name} to be False.")

    request = result.get("source_summary_reporting_request")
    if not isinstance(request, dict):
        raise ValueError(
            "AI controlled summarization/reporting result must include source_summary_reporting_request dict."
        )
    validate_controlled_summarization_reporting_request(request)
    for field_name in (
        "summary_reporting_request_id",
        "summary_target_ref",
        "summary_target_family",
        "summarization_mode",
        "reporting_assistance_mode",
    ):
        if result[field_name] != request[field_name]:
            raise ValueError(f"AI controlled summarization/reporting result {field_name} must match request.")

    findings = result.get("summary_reporting_findings")
    if not isinstance(findings, list):
        raise ValueError("AI controlled summarization/reporting result summary_reporting_findings must be a list.")
    seen_ids: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("AI controlled summarization/reporting result findings must contain dicts.")
        validate_controlled_summarization_reporting_finding(finding)
        finding_id = str(finding["finding_id"])
        if finding_id in seen_ids:
            raise ValueError("AI controlled summarization/reporting result finding_id values must be unique.")
        seen_ids.add(finding_id)
    _validate_finding_refs_within_request(findings, request)

    expected_result = (
        SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED
        if findings
        else SUMMARIZATION_REPORTING_ASSISTANCE_READY
    )
    if result["summarization_reporting_assistance_result"] != expected_result:
        raise ValueError(
            "AI controlled summarization/reporting result does not match deterministic finding evaluation."
        )
    _normalize_supported_value(
        result["summarization_reporting_assistance_result"],
        "summarization_reporting_assistance_result",
        SUPPORTED_SUMMARIZATION_REPORTING_ASSISTANCE_RESULTS,
    )


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
        raise ValueError("AI controlled summarization/reporting requires source_groundedness_check dict.")
    return groundedness


def _validate_refs_subset(*, declared: list[str], allowed: list[str], field_name: str) -> None:
    allowed_set = set(allowed)
    for ref in declared:
        if ref not in allowed_set:
            raise ValueError(
                "AI controlled summarization/reporting request "
                f"{field_name} includes ref outside the passed source quality gate: {ref}."
            )


def _validate_finding_refs_within_request(findings: list[dict[str, object]], request: dict[str, object]) -> None:
    evidence_refs = set(_normalize_ref_list(request.get("summary_evidence_refs"), "summary_evidence_refs"))
    source_refs = set(_normalize_ref_list(request.get("source_refs_used_as_truth"), "source_refs_used_as_truth"))
    for finding in findings:
        if _parse_version_pinned_ref(finding["evidence_ref"], "evidence_ref") not in evidence_refs:
            raise ValueError(
                "AI controlled summarization/reporting finding evidence_ref must be inside request evidence refs."
            )
        if _parse_version_pinned_ref(finding["source_ref"], "source_ref") not in source_refs:
            raise ValueError(
                "AI controlled summarization/reporting finding source_ref must be inside request source refs."
            )


def _parse_version_pinned_ref(raw_ref: object, field_name: str) -> str:
    ref = _require_non_empty_string(raw_ref, field_name)
    return parse_version_pinned_asset_ref(ref)["asset_ref"]


def _normalize_ref_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"AI controlled summarization/reporting requires non-empty list {field_name}.")
    refs = [_parse_version_pinned_ref(raw_ref, field_name) for raw_ref in value]
    return sorted(_deduplicate(refs))


def _normalize_supported_value(value: object, field_name: str, supported_values: tuple[str, ...]) -> str:
    normalized = _require_non_empty_string(value, field_name)
    if normalized not in supported_values:
        raise ValueError(
            f"AI controlled summarization/reporting declares unsupported {field_name}. "
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
        raise ValueError(f"AI controlled summarization/reporting must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(payload: dict[str, object], required_fields: tuple[str, ...], label: str) -> None:
    for field_name in required_fields:
        _require_non_empty_string(payload.get(field_name), field_name)


def _validate_exact(payload: dict[str, object], field_name: str, expected_value: str) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            "AI controlled summarization/reporting declares invalid "
            f"{field_name}: expected {expected_value!r}, got {actual_value!r}."
        )


def _validate_prohibited_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_SUMMARIZATION_REPORTING_FIELDS:
        if field_name in payload:
            raise ValueError(f"{field_name} is not allowed in M18.2 controlled summarization/reporting payloads.")
