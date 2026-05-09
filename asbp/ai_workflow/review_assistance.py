"AI-assisted controlled review support for M18.1."

from __future__ import annotations

from typing import Any

from asbp.ai_evaluation import QUALITY_GATE_PASS, validate_ai_quality_gate_result
from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID = "M18.1"
AI_CONTROLLED_REVIEW_ASSISTANCE_CONTRACT_VERSION = "ai-controlled-review-assistance-v1"
AI_REVIEW_ASSISTANCE_REQUEST_STATUS_VALIDATED = "ai_review_assistance_request_validated"
AI_REVIEW_ASSISTANCE_RESULT_STATUS_VALIDATED = "ai_review_assistance_result_validated"
AI_REVIEW_FINDING_STATUS_VALIDATED = "ai_review_finding_validated"

ADVISORY_REVIEW_ASSISTANCE_ROLE = "advisory_review_assistance"

DOCUMENT_ARTIFACT_REVIEW_TARGET = "document_artifact_review_target"
REPORTING_ARTIFACT_REVIEW_TARGET = "reporting_artifact_review_target"
WORKFLOW_STATE_REVIEW_TARGET = "workflow_state_review_target"
AI_OUTPUT_REVIEW_TARGET = "ai_output_review_target"
SUPPORTED_REVIEW_TARGET_FAMILIES = (
    DOCUMENT_ARTIFACT_REVIEW_TARGET,
    REPORTING_ARTIFACT_REVIEW_TARGET,
    WORKFLOW_STATE_REVIEW_TARGET,
    AI_OUTPUT_REVIEW_TARGET,
)

EVIDENCE_BOUND_REVIEW_MODE = "evidence_bound_review"
CONTRACT_ALIGNMENT_REVIEW_MODE = "contract_alignment_review"
GAP_AND_RISK_REVIEW_MODE = "gap_and_risk_review"
SUPPORTED_REVIEW_MODES = (
    EVIDENCE_BOUND_REVIEW_MODE,
    CONTRACT_ALIGNMENT_REVIEW_MODE,
    GAP_AND_RISK_REVIEW_MODE,
)

REVIEW_ASSISTANCE_NO_FINDINGS = "review_assistance_no_findings"
REVIEW_ASSISTANCE_FINDINGS_IDENTIFIED = "review_assistance_findings_identified"
SUPPORTED_REVIEW_ASSISTANCE_RESULTS = (
    REVIEW_ASSISTANCE_NO_FINDINGS,
    REVIEW_ASSISTANCE_FINDINGS_IDENTIFIED,
)

CONTRACT_ALIGNMENT_FINDING = "contract_alignment_finding"
EVIDENCE_GAP_FINDING = "evidence_gap_finding"
ASSUMPTION_LABELING_FINDING = "assumption_labeling_finding"
SOURCE_ROLE_DISCIPLINE_FINDING = "source_role_discipline_finding"
APPROVAL_AUTHORITY_BOUNDARY_FINDING = "approval_authority_boundary_finding"
WORKFLOW_STATE_MUTATION_BOUNDARY_FINDING = "workflow_state_mutation_boundary_finding"
DOCUMENT_GENERATION_BOUNDARY_FINDING = "document_generation_boundary_finding"
DOCUMENT_TEMPLATE_PRODUCT_BOUNDARY_FINDING = "document_template_product_boundary_finding"
LIBRARY_ARCHITECTURE_DEFERRED_SCOPE_FINDING = "library_architecture_deferred_scope_finding"
SUPPORTED_REVIEW_FINDING_CATEGORIES = (
    CONTRACT_ALIGNMENT_FINDING,
    EVIDENCE_GAP_FINDING,
    ASSUMPTION_LABELING_FINDING,
    SOURCE_ROLE_DISCIPLINE_FINDING,
    APPROVAL_AUTHORITY_BOUNDARY_FINDING,
    WORKFLOW_STATE_MUTATION_BOUNDARY_FINDING,
    DOCUMENT_GENERATION_BOUNDARY_FINDING,
    DOCUMENT_TEMPLATE_PRODUCT_BOUNDARY_FINDING,
    LIBRARY_ARCHITECTURE_DEFERRED_SCOPE_FINDING,
)

REVIEW_FINDING_INFO_SEVERITY = "info"
REVIEW_FINDING_WARNING_SEVERITY = "warning"
REVIEW_FINDING_BLOCKING_SEVERITY = "blocking"
SUPPORTED_REVIEW_FINDING_SEVERITIES = (
    REVIEW_FINDING_INFO_SEVERITY,
    REVIEW_FINDING_WARNING_SEVERITY,
    REVIEW_FINDING_BLOCKING_SEVERITY,
)

_PROHIBITED_REVIEW_FIELDS = (
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
    "document_factory_payload",
    "document_template_payload",
    "document_generation_payload",
    "document_renderer_payload",
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
    "document_template_product_implementation_requested",
    "library_architecture_change_requested",
    "document_factory_in_scope",
    "actual_document_generation_in_scope",
    "approval_authority_claimed",
    "release_authority_claimed",
    "workflow_mutation_authority_claimed",
)

_RESULT_REQUIRED_FALSE_FIELDS = (
    "ai_can_approve",
    "ai_can_release",
    "ai_can_mutate_workflow_state",
    "approval_payload_included",
    "workflow_release_payload_included",
    "state_mutation_payload_included",
    "document_generation_in_scope",
    "document_template_product_implementation_in_scope",
    "library_architecture_change_in_scope",
    "document_factory_output_created",
    "validation_or_uat_truth_claimed",
)


def build_controlled_review_assistance_baseline() -> dict[str, Any]:
    """Return the M18.1 controlled review-assistance baseline."""
    return {
        "checkpoint": AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_REVIEW_ASSISTANCE_CONTRACT_VERSION,
        "supported_review_target_families": list(SUPPORTED_REVIEW_TARGET_FAMILIES),
        "supported_review_modes": list(SUPPORTED_REVIEW_MODES),
        "supported_review_finding_categories": list(SUPPORTED_REVIEW_FINDING_CATEGORIES),
        "supported_review_finding_severities": list(SUPPORTED_REVIEW_FINDING_SEVERITIES),
        "supported_review_assistance_results": list(SUPPORTED_REVIEW_ASSISTANCE_RESULTS),
        "review_role": ADVISORY_REVIEW_ASSISTANCE_ROLE,
        "authority_policy": (
            "review_assistance_is_advisory_only_and_cannot_approve_release_or_"
            "mutate_workflow_state"
        ),
        "source_discipline_policy": (
            "review_assistance_must_use_passed_m17_quality_gate_evidence_and_"
            "source_role_context"
        ),
        "deferred_scope_policy": (
            "document_factory_document_generation_template_product_implementation_"
            "and_library_architecture_cleanup_remain_deferred_beyond_m18"
        ),
        "not_owned_by_m18_1": [
            "actual_llm_calls",
            "prompt_templates",
            "document_factory",
            "document_template_product_implementation",
            "actual_document_generation_from_expanded_library_content",
            "product_ready_document_rendering",
            "library_architecture_cleanup",
            "controlled_summarization_assistance",
            "controlled_recommendation_behavior",
            "workflow_state_mutation",
            "approval_or_release_authority",
            "ui_api_behavior",
            "cloud_or_saas_productization",
        ],
    }


def build_controlled_review_request(
    *,
    review_request_id: str,
    source_quality_gate_result: dict[str, object],
    review_target_ref: str,
    review_target_family: str,
    review_mode: str,
    review_evidence_refs: list[str] | None = None,
    source_refs_used_as_truth: list[str] | None = None,
    approval_requested: bool = False,
    release_requested: bool = False,
    state_mutation_requested: bool = False,
    document_generation_requested: bool = False,
    document_template_product_implementation_requested: bool = False,
    library_architecture_change_requested: bool = False,
) -> dict[str, object]:
    """Build and validate a controlled M18.1 review-assistance request."""
    validate_ai_quality_gate_result(source_quality_gate_result)
    request = {
        "checkpoint": AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_REVIEW_ASSISTANCE_CONTRACT_VERSION,
        "review_request_id": _require_non_empty_string(review_request_id, "review_request_id"),
        "review_request_status": AI_REVIEW_ASSISTANCE_REQUEST_STATUS_VALIDATED,
        "review_target_ref": _parse_version_pinned_ref(review_target_ref, "review_target_ref"),
        "review_target_family": _normalize_supported_value(
            review_target_family,
            "review_target_family",
            SUPPORTED_REVIEW_TARGET_FAMILIES,
        ),
        "review_mode": _normalize_supported_value(review_mode, "review_mode", SUPPORTED_REVIEW_MODES),
        "requested_review_role": ADVISORY_REVIEW_ASSISTANCE_ROLE,
        "source_quality_gate_result_id": str(source_quality_gate_result["quality_gate_result_id"]),
        "source_quality_gate_result": dict(source_quality_gate_result),
        "review_evidence_refs": _normalize_ref_list(
            review_evidence_refs
            if review_evidence_refs is not None
            else _quality_gate_evidence_refs(source_quality_gate_result),
            "review_evidence_refs",
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
        "document_template_product_implementation_requested": document_template_product_implementation_requested,
        "library_architecture_change_requested": library_architecture_change_requested,
        "document_factory_in_scope": False,
        "actual_document_generation_in_scope": False,
        "approval_authority_claimed": False,
        "release_authority_claimed": False,
        "workflow_mutation_authority_claimed": False,
        "review_output_policy": "advisory_metadata_only_no_generated_document_text",
    }
    validate_controlled_review_request(request)
    return request


def validate_controlled_review_request(request: dict[str, object]) -> None:
    """Validate one M18.1 controlled review-assistance request."""
    _validate_prohibited_fields(request)
    _validate_required_string_fields(
        request,
        (
            "checkpoint",
            "contract_version",
            "review_request_id",
            "review_request_status",
            "review_target_ref",
            "review_target_family",
            "review_mode",
            "requested_review_role",
            "source_quality_gate_result_id",
        ),
        "AI controlled review request",
    )
    _validate_exact(request, "checkpoint", AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID)
    _validate_exact(request, "contract_version", AI_CONTROLLED_REVIEW_ASSISTANCE_CONTRACT_VERSION)
    _validate_exact(request, "review_request_status", AI_REVIEW_ASSISTANCE_REQUEST_STATUS_VALIDATED)
    _validate_exact(request, "requested_review_role", ADVISORY_REVIEW_ASSISTANCE_ROLE)

    source_quality_gate = request.get("source_quality_gate_result")
    if not isinstance(source_quality_gate, dict):
        raise ValueError("AI controlled review request must include source_quality_gate_result dict.")
    validate_ai_quality_gate_result(source_quality_gate)
    if source_quality_gate.get("quality_gate_result") != QUALITY_GATE_PASS:
        raise ValueError("AI controlled review request requires a passing source quality gate.")
    if request["source_quality_gate_result_id"] != source_quality_gate["quality_gate_result_id"]:
        raise ValueError("AI controlled review request source_quality_gate_result_id must match payload.")

    _parse_version_pinned_ref(request["review_target_ref"], "review_target_ref")
    _normalize_supported_value(request["review_target_family"], "review_target_family", SUPPORTED_REVIEW_TARGET_FAMILIES)
    _normalize_supported_value(request["review_mode"], "review_mode", SUPPORTED_REVIEW_MODES)
    for field_name in _REQUEST_REQUIRED_FALSE_FIELDS:
        if request.get(field_name) is not False:
            raise ValueError(f"AI controlled review request requires {field_name} to be False.")

    _validate_refs_subset(
        declared=_normalize_ref_list(request.get("review_evidence_refs"), "review_evidence_refs"),
        allowed=_quality_gate_evidence_refs(source_quality_gate),
        field_name="review_evidence_refs",
    )
    _validate_refs_subset(
        declared=_normalize_ref_list(request.get("source_refs_used_as_truth"), "source_refs_used_as_truth"),
        allowed=_quality_gate_truth_refs(source_quality_gate),
        field_name="source_refs_used_as_truth",
    )


def build_controlled_review_finding(
    *,
    finding_id: str,
    finding_category: str,
    evidence_ref: str,
    source_ref: str,
    finding_severity: str = REVIEW_FINDING_WARNING_SEVERITY,
) -> dict[str, object]:
    """Build and validate one controlled review finding metadata record."""
    finding = {
        "finding_id": _require_non_empty_string(finding_id, "finding_id"),
        "finding_status": AI_REVIEW_FINDING_STATUS_VALIDATED,
        "finding_category": _normalize_supported_value(
            finding_category,
            "finding_category",
            SUPPORTED_REVIEW_FINDING_CATEGORIES,
        ),
        "finding_severity": _normalize_supported_value(
            finding_severity,
            "finding_severity",
            SUPPORTED_REVIEW_FINDING_SEVERITIES,
        ),
        "evidence_ref": _parse_version_pinned_ref(evidence_ref, "evidence_ref"),
        "source_ref": _parse_version_pinned_ref(source_ref, "source_ref"),
        "finding_language_policy": "metadata_only_no_generated_review_narrative",
    }
    validate_controlled_review_finding(finding)
    return finding


def validate_controlled_review_finding(finding: dict[str, object]) -> None:
    """Validate one controlled review finding metadata record."""
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
        "AI controlled review finding",
    )
    _validate_exact(finding, "finding_status", AI_REVIEW_FINDING_STATUS_VALIDATED)
    _normalize_supported_value(finding["finding_category"], "finding_category", SUPPORTED_REVIEW_FINDING_CATEGORIES)
    _normalize_supported_value(finding["finding_severity"], "finding_severity", SUPPORTED_REVIEW_FINDING_SEVERITIES)
    _parse_version_pinned_ref(finding["evidence_ref"], "evidence_ref")
    _parse_version_pinned_ref(finding["source_ref"], "source_ref")


def build_controlled_review_assistance_result(
    *,
    review_result_id: str,
    review_request: dict[str, object],
    review_findings: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build and validate a controlled M18.1 review-assistance result."""
    validate_controlled_review_request(review_request)
    findings = [dict(finding) for finding in review_findings or []]
    for finding in findings:
        validate_controlled_review_finding(finding)
    result = {
        "checkpoint": AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID,
        "contract_version": AI_CONTROLLED_REVIEW_ASSISTANCE_CONTRACT_VERSION,
        "review_result_id": _require_non_empty_string(review_result_id, "review_result_id"),
        "review_result_status": AI_REVIEW_ASSISTANCE_RESULT_STATUS_VALIDATED,
        "review_request_id": str(review_request["review_request_id"]),
        "review_target_ref": str(review_request["review_target_ref"]),
        "review_target_family": str(review_request["review_target_family"]),
        "review_mode": str(review_request["review_mode"]),
        "review_assistance_result": REVIEW_ASSISTANCE_FINDINGS_IDENTIFIED if findings else REVIEW_ASSISTANCE_NO_FINDINGS,
        "review_findings": findings,
        "source_review_request": dict(review_request),
        "advisory_only": True,
        "ai_can_approve": False,
        "ai_can_release": False,
        "ai_can_mutate_workflow_state": False,
        "approval_payload_included": False,
        "workflow_release_payload_included": False,
        "state_mutation_payload_included": False,
        "document_generation_in_scope": False,
        "document_template_product_implementation_in_scope": False,
        "library_architecture_change_in_scope": False,
        "document_factory_output_created": False,
        "validation_or_uat_truth_claimed": False,
        "review_authority_policy": "advisory_only_requires_human_review_for_acceptance",
        "deferred_scope_policy": (
            "document_factory_template_product_implementation_and_library_"
            "architecture_cleanup_remain_out_of_scope_for_m18_1"
        ),
    }
    validate_controlled_review_assistance_result(result)
    return result


def validate_controlled_review_assistance_result(result: dict[str, object]) -> None:
    """Validate one M18.1 controlled review-assistance result."""
    _validate_prohibited_fields(result)
    _validate_required_string_fields(
        result,
        (
            "checkpoint",
            "contract_version",
            "review_result_id",
            "review_result_status",
            "review_request_id",
            "review_target_ref",
            "review_target_family",
            "review_mode",
            "review_assistance_result",
        ),
        "AI controlled review result",
    )
    _validate_exact(result, "checkpoint", AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID)
    _validate_exact(result, "contract_version", AI_CONTROLLED_REVIEW_ASSISTANCE_CONTRACT_VERSION)
    _validate_exact(result, "review_result_status", AI_REVIEW_ASSISTANCE_RESULT_STATUS_VALIDATED)
    if result.get("advisory_only") is not True:
        raise ValueError("AI controlled review result must be advisory_only.")
    for field_name in _RESULT_REQUIRED_FALSE_FIELDS:
        if result.get(field_name) is not False:
            raise ValueError(f"AI controlled review result requires {field_name} to be False.")

    request = result.get("source_review_request")
    if not isinstance(request, dict):
        raise ValueError("AI controlled review result must include source_review_request dict.")
    validate_controlled_review_request(request)
    for field_name in ("review_request_id", "review_target_ref", "review_target_family", "review_mode"):
        if result[field_name] != request[field_name]:
            raise ValueError(f"AI controlled review result {field_name} must match request.")

    findings = result.get("review_findings")
    if not isinstance(findings, list):
        raise ValueError("AI controlled review result review_findings must be a list.")
    seen_ids: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("AI controlled review result review_findings must contain dicts.")
        validate_controlled_review_finding(finding)
        finding_id = str(finding["finding_id"])
        if finding_id in seen_ids:
            raise ValueError("AI controlled review result finding_id values must be unique.")
        seen_ids.add(finding_id)
    _validate_finding_refs_within_request(findings, request)

    expected_result = REVIEW_ASSISTANCE_FINDINGS_IDENTIFIED if findings else REVIEW_ASSISTANCE_NO_FINDINGS
    if result["review_assistance_result"] != expected_result:
        raise ValueError("AI controlled review result does not match deterministic finding evaluation.")
    _normalize_supported_value(result["review_assistance_result"], "review_assistance_result", SUPPORTED_REVIEW_ASSISTANCE_RESULTS)


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
        raise ValueError("AI controlled review requires source_groundedness_check dict.")
    return groundedness


def _validate_refs_subset(*, declared: list[str], allowed: list[str], field_name: str) -> None:
    allowed_set = set(allowed)
    for ref in declared:
        if ref not in allowed_set:
            raise ValueError(
                f"AI controlled review request {field_name} includes ref outside the passed source quality gate: {ref}."
            )


def _validate_finding_refs_within_request(findings: list[dict[str, object]], request: dict[str, object]) -> None:
    evidence_refs = set(_normalize_ref_list(request.get("review_evidence_refs"), "review_evidence_refs"))
    source_refs = set(_normalize_ref_list(request.get("source_refs_used_as_truth"), "source_refs_used_as_truth"))
    for finding in findings:
        if _parse_version_pinned_ref(finding["evidence_ref"], "evidence_ref") not in evidence_refs:
            raise ValueError("AI controlled review finding evidence_ref must be inside request evidence refs.")
        if _parse_version_pinned_ref(finding["source_ref"], "source_ref") not in source_refs:
            raise ValueError("AI controlled review finding source_ref must be inside request source refs.")


def _parse_version_pinned_ref(raw_ref: object, field_name: str) -> str:
    ref = _require_non_empty_string(raw_ref, field_name)
    return parse_version_pinned_asset_ref(ref)["asset_ref"]


def _normalize_ref_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"AI controlled review requires non-empty list {field_name}.")
    refs = [_parse_version_pinned_ref(raw_ref, field_name) for raw_ref in value]
    return sorted(_deduplicate(refs))


def _normalize_supported_value(value: object, field_name: str, supported_values: tuple[str, ...]) -> str:
    normalized = _require_non_empty_string(value, field_name)
    if normalized not in supported_values:
        raise ValueError(
            f"AI controlled review declares unsupported {field_name}. "
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
        raise ValueError(f"AI controlled review must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(payload: dict[str, object], required_fields: tuple[str, ...], label: str) -> None:
    for field_name in required_fields:
        _require_non_empty_string(payload.get(field_name), field_name)


def _validate_exact(payload: dict[str, object], field_name: str, expected_value: str) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"AI controlled review declares invalid {field_name}: expected {expected_value!r}, got {actual_value!r}."
        )


def _validate_prohibited_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_REVIEW_FIELDS:
        if field_name in payload:
            raise ValueError(f"{field_name} is not allowed in M18.1 controlled review payloads.")
