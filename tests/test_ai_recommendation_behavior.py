import pytest

from asbp.ai_evaluation import build_ai_quality_gate_result
from asbp.ai_runtime import (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_ENGINE_INPUT_ROLE,
    REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
    STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    URS_DOCUMENT_FAMILY,
    VALIDATED_EVIDENCE_STATUS,
    build_ai_candidate_output,
    build_ai_context_item,
    build_ai_context_package,
    build_ai_generation_mode_request,
    build_ai_output_acceptance_decision,
    build_ai_runtime_entry_request,
)
from asbp.ai_workflow import (
    AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID,
    CONTRACT_ALIGNED_RECOMMENDATION_MODE,
    DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
    EVIDENCE_BOUND_RECOMMENDATION_MODE,
    EVIDENCE_FOLLOWUP_RECOMMENDATION,
    GAP_AND_RISK_RECOMMENDATION_MODE,
    HUMAN_REVIEW_ESCALATION_RECOMMENDATION,
    RECOMMENDATION_ACTION_EXECUTION_BOUNDARY_FINDING,
    RECOMMENDATION_APPROVAL_AUTHORITY_BOUNDARY_FINDING,
    RECOMMENDATION_ASSISTANCE_BOUNDARY_FINDINGS_IDENTIFIED,
    RECOMMENDATION_ASSISTANCE_READY,
    RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_AND_BOUNDARY_FINDINGS_IDENTIFIED,
    RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_IDENTIFIED,
    RECOMMENDATION_AUTONOMOUS_AGENTIC_BEHAVIOR_BOUNDARY_FINDING,
    RECOMMENDATION_BOUNDARY_FINDING_BLOCKING_SEVERITY,
    RECOMMENDATION_PRIORITY_HIGH,
    REPORTING_ARTIFACT_RECOMMENDATION_TARGET,
    WORKFLOW_READINESS_RECOMMENDATION,
    build_controlled_recommendation_behavior_baseline,
    build_controlled_recommendation_boundary_finding,
    build_controlled_recommendation_item,
    build_controlled_recommendation_request,
    build_controlled_recommendation_result,
    validate_controlled_recommendation_request,
    validate_controlled_recommendation_result,
)


def _runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-RECOMMEND-001",
        job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
        caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
        governed_source_refs=[
            "TEMPLATE-URS@v1",
            "DOCUMENT-LIFECYCLE-STATE@v1",
            "STANDARDS-GUARDRAIL-CONTEXT@v1",
        ],
        engine_contract_refs=[
            "DOCUMENT-REQUEST-CONTRACT@v1",
            "DOCUMENT-OUTPUT-CONTRACT@v1",
        ],
    )


def _context_package() -> dict[str, object]:
    return build_ai_context_package(
        context_package_id="CTXPKG-RECOMMEND-001",
        ai_runtime_entry_request=_runtime_request(),
        context_items=[
            build_ai_context_item(
                context_item_id="CTX-TEMPLATE",
                source_family=TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
                source_ref="TEMPLATE-URS@v1",
                source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
                payload_classification=REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
                evidence_status=VALIDATED_EVIDENCE_STATUS,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
            build_ai_context_item(
                context_item_id="CTX-LIFECYCLE",
                source_family=DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
                source_ref="DOCUMENT-LIFECYCLE-STATE@v1",
                source_role=GOVERNED_ENGINE_INPUT_ROLE,
                payload_classification=STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
                evidence_status=VALIDATED_EVIDENCE_STATUS,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
            build_ai_context_item(
                context_item_id="CTX-STANDARDS",
                source_family=STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
                source_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
                source_role=GOVERNED_CONTRACT_ROLE,
                payload_classification=REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
                evidence_status=VALIDATED_EVIDENCE_STATUS,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
        ],
    )


def _generation_request() -> dict[str, object]:
    return build_ai_generation_mode_request(
        generation_request_id="GEN-RECOMMEND-001",
        context_package=_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _quality_gate(*, content_contract_satisfied: bool = True) -> dict[str, object]:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-RECOMMEND-001",
        generation_mode_request=_generation_request(),
        candidate_output_ref="CANDIDATE-URS-OUTPUT@v1",
        candidate_evidence_status=VALIDATED_EVIDENCE_STATUS,
        content_contract_satisfied=content_contract_satisfied,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=True,
        assumptions_labeled_when_required=True,
        placeholders_used_for_missing_truth=True,
    )
    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="ACC-RECOMMEND-001",
        candidate_output=candidate,
    )
    return build_ai_quality_gate_result(
        quality_gate_result_id="QG-RECOMMEND-001",
        source_acceptance_decision=decision,
    )


def _recommendation_request() -> dict[str, object]:
    return build_controlled_recommendation_request(
        recommendation_request_id="REC-REQ-001",
        source_quality_gate_result=_quality_gate(),
        recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
        recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
        recommendation_mode=EVIDENCE_BOUND_RECOMMENDATION_MODE,
    )


def test_recommendation_baseline_exposes_m18_3_scope_and_deferrals() -> None:
    baseline = build_controlled_recommendation_behavior_baseline()

    assert baseline["checkpoint"] == AI_CONTROLLED_RECOMMENDATION_BEHAVIOR_CHECKPOINT_ID
    assert "action_execution" in baseline["not_owned_by_m18_3"]
    assert "autonomous_agentic_behavior" in baseline["not_owned_by_m18_3"]
    assert "approval_or_release_authority" in baseline["not_owned_by_m18_3"]
    assert "actual_document_generation_from_expanded_governed_library_content" in baseline["not_owned_by_m18_3"]
    assert "product_ready_report_rendering" in baseline["not_owned_by_m18_3"]


def test_valid_recommendation_result_without_items_is_advisory_ready() -> None:
    result = build_controlled_recommendation_result(
        recommendation_result_id="REC-RES-READY",
        recommendation_request=_recommendation_request(),
    )

    assert result["recommendation_assistance_result"] == RECOMMENDATION_ASSISTANCE_READY
    assert result["advisory_only"] is True
    assert result["controlled_recommendation_behavior_in_scope"] is True
    assert result["ai_can_issue_controlled_recommendation_metadata"] is True
    assert result["ai_can_approve"] is False
    assert result["ai_can_release"] is False
    assert result["ai_can_mutate_workflow_state"] is False
    assert result["ai_can_execute_actions"] is False
    assert result["ai_can_generate_document"] is False
    assert result["ai_can_generate_report"] is False
    assert result["ai_can_render_product_ready_report"] is False
    assert result["ai_can_claim_validation_truth"] is False
    validate_controlled_recommendation_result(result)


def test_recommendation_request_requires_passing_source_quality_gate() -> None:
    with pytest.raises(ValueError, match="passing source quality gate"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-FAILED-GATE",
            source_quality_gate_result=_quality_gate(content_contract_satisfied=False),
            recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
            recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=EVIDENCE_BOUND_RECOMMENDATION_MODE,
        )


def test_recommendation_request_rejects_approval_release_mutation_and_execution_pressure() -> None:
    with pytest.raises(ValueError, match="approval_requested to be False"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-APPROVAL",
            source_quality_gate_result=_quality_gate(),
            recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
            recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=CONTRACT_ALIGNED_RECOMMENDATION_MODE,
            approval_requested=True,
        )

    with pytest.raises(ValueError, match="state_mutation_requested to be False"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-MUTATION",
            source_quality_gate_result=_quality_gate(),
            recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
            recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=CONTRACT_ALIGNED_RECOMMENDATION_MODE,
            state_mutation_requested=True,
        )

    with pytest.raises(ValueError, match="action_execution_requested to be False"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-ACTION",
            source_quality_gate_result=_quality_gate(),
            recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
            recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=CONTRACT_ALIGNED_RECOMMENDATION_MODE,
            action_execution_requested=True,
        )


def test_recommendation_request_rejects_document_report_rendering_and_truth_claims() -> None:
    with pytest.raises(ValueError, match="document_generation_requested to be False"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-DOCGEN",
            source_quality_gate_result=_quality_gate(),
            recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
            recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=GAP_AND_RISK_RECOMMENDATION_MODE,
            document_generation_requested=True,
        )

    with pytest.raises(ValueError, match="report_generation_requested to be False"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-REPORTGEN",
            source_quality_gate_result=_quality_gate(),
            recommendation_target_ref="RECOMMENDATION-TARGET-REPORT@v1",
            recommendation_target_family=REPORTING_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=GAP_AND_RISK_RECOMMENDATION_MODE,
            report_generation_requested=True,
        )

    with pytest.raises(ValueError, match="validation_truth_requested to be False"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-TRUTH",
            source_quality_gate_result=_quality_gate(),
            recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
            recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=GAP_AND_RISK_RECOMMENDATION_MODE,
            validation_truth_requested=True,
        )


def test_recommendation_request_rejects_evidence_ref_outside_source_quality_gate() -> None:
    with pytest.raises(ValueError, match="outside the passed source quality gate"):
        build_controlled_recommendation_request(
            recommendation_request_id="REC-REQ-BAD-EVIDENCE",
            source_quality_gate_result=_quality_gate(),
            recommendation_target_ref="RECOMMENDATION-TARGET-URS@v1",
            recommendation_target_family=DOCUMENT_ARTIFACT_RECOMMENDATION_TARGET,
            recommendation_mode=EVIDENCE_BOUND_RECOMMENDATION_MODE,
            recommendation_evidence_refs=["MISSING-EVIDENCE@v1"],
        )


def test_controlled_recommendation_items_are_metadata_only_and_identified() -> None:
    item = build_controlled_recommendation_item(
        recommendation_id="REC-ITEM-001",
        recommendation_category=EVIDENCE_FOLLOWUP_RECOMMENDATION,
        recommendation_priority=RECOMMENDATION_PRIORITY_HIGH,
        evidence_ref="TEMPLATE-URS@v1",
        source_ref="TEMPLATE-URS@v1",
    )
    result = build_controlled_recommendation_result(
        recommendation_result_id="REC-RES-ITEMS",
        recommendation_request=_recommendation_request(),
        recommendation_items=[item],
    )

    assert result["recommendation_assistance_result"] == RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_IDENTIFIED
    assert result["recommendation_items"][0]["requires_human_decision"] is True
    assert result["ai_can_execute_actions"] is False
    validate_controlled_recommendation_result(result)


def test_prohibited_recommendation_classes_are_not_supported_as_recommendation_items() -> None:
    with pytest.raises(ValueError, match="unsupported recommendation_category"):
        build_controlled_recommendation_item(
            recommendation_id="REC-ITEM-PROHIBITED",
            recommendation_category="approval_or_release_recommendation",
            evidence_ref="TEMPLATE-URS@v1",
            source_ref="TEMPLATE-URS@v1",
        )


def test_prohibited_recommendation_pressure_can_be_flagged_as_boundary_finding_only() -> None:
    finding = build_controlled_recommendation_boundary_finding(
        finding_id="REC-FIND-APPROVAL",
        finding_category=RECOMMENDATION_APPROVAL_AUTHORITY_BOUNDARY_FINDING,
        finding_severity=RECOMMENDATION_BOUNDARY_FINDING_BLOCKING_SEVERITY,
        evidence_ref="TEMPLATE-URS@v1",
        source_ref="TEMPLATE-URS@v1",
    )
    result = build_controlled_recommendation_result(
        recommendation_result_id="REC-RES-FINDING",
        recommendation_request=_recommendation_request(),
        recommendation_boundary_findings=[finding],
    )

    assert result["recommendation_assistance_result"] == RECOMMENDATION_ASSISTANCE_BOUNDARY_FINDINGS_IDENTIFIED
    assert result["recommendation_boundary_findings"][0]["finding_category"] == RECOMMENDATION_APPROVAL_AUTHORITY_BOUNDARY_FINDING
    assert result["ai_can_approve"] is False
    validate_controlled_recommendation_result(result)


def test_recommendation_result_supports_items_and_boundary_findings_together() -> None:
    item = build_controlled_recommendation_item(
        recommendation_id="REC-ITEM-HUMAN-REVIEW",
        recommendation_category=HUMAN_REVIEW_ESCALATION_RECOMMENDATION,
        evidence_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
        source_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )
    finding = build_controlled_recommendation_boundary_finding(
        finding_id="REC-FIND-AUTONOMOUS",
        finding_category=RECOMMENDATION_AUTONOMOUS_AGENTIC_BEHAVIOR_BOUNDARY_FINDING,
        evidence_ref="TEMPLATE-URS@v1",
        source_ref="TEMPLATE-URS@v1",
    )
    result = build_controlled_recommendation_result(
        recommendation_result_id="REC-RES-BOTH",
        recommendation_request=_recommendation_request(),
        recommendation_items=[item],
        recommendation_boundary_findings=[finding],
    )

    assert (
        result["recommendation_assistance_result"]
        == RECOMMENDATION_ASSISTANCE_RECOMMENDATIONS_AND_BOUNDARY_FINDINGS_IDENTIFIED
    )
    assert result["ai_can_replace_human_decision"] is False
    validate_controlled_recommendation_result(result)


def test_recommendation_result_rejects_item_ref_outside_request_scope() -> None:
    item = build_controlled_recommendation_item(
        recommendation_id="REC-ITEM-BAD-REF",
        recommendation_category=WORKFLOW_READINESS_RECOMMENDATION,
        evidence_ref="MISSING-EVIDENCE@v1",
        source_ref="TEMPLATE-URS@v1",
    )

    with pytest.raises(ValueError, match="evidence_ref must be inside request evidence refs"):
        build_controlled_recommendation_result(
            recommendation_result_id="REC-RES-BAD-REF",
            recommendation_request=_recommendation_request(),
            recommendation_items=[item],
        )


def test_recommendation_payloads_reject_generated_text_and_action_payloads() -> None:
    request = _recommendation_request()
    request["generated_recommendation_text"] = "This must not be accepted."

    with pytest.raises(ValueError, match="generated_recommendation_text is not allowed"):
        validate_controlled_recommendation_request(request)

    result = build_controlled_recommendation_result(
        recommendation_result_id="REC-RES-ACTION-PAYLOAD",
        recommendation_request=_recommendation_request(),
    )
    result["action_execution_payload"] = {"execute": "now"}

    with pytest.raises(ValueError, match="action_execution_payload is not allowed"):
        validate_controlled_recommendation_result(result)


def test_action_execution_pressure_can_be_flagged_without_action_execution_payload() -> None:
    finding = build_controlled_recommendation_boundary_finding(
        finding_id="REC-FIND-ACTION",
        finding_category=RECOMMENDATION_ACTION_EXECUTION_BOUNDARY_FINDING,
        evidence_ref="DOCUMENT-LIFECYCLE-STATE@v1",
        source_ref="DOCUMENT-LIFECYCLE-STATE@v1",
    )
    result = build_controlled_recommendation_result(
        recommendation_result_id="REC-RES-ACTION-FINDING",
        recommendation_request=_recommendation_request(),
        recommendation_boundary_findings=[finding],
    )

    assert result["recommendation_assistance_result"] == RECOMMENDATION_ASSISTANCE_BOUNDARY_FINDINGS_IDENTIFIED
    assert result["ai_can_execute_actions"] is False
    assert result["action_execution_payload_included"] is False
