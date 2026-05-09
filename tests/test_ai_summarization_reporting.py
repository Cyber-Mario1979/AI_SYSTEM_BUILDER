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
    AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID,
    DETAIL_DISCIPLINE_REPORTING_MODE,
    DOCUMENT_ARTIFACT_SUMMARY_TARGET,
    EVIDENCE_BOUND_SUMMARIZATION_MODE,
    EVIDENCE_TRACE_REPORTING_MODE,
    REPORTING_ARTIFACT_SUMMARY_TARGET,
    REPORTING_DETAIL_DISCIPLINE_FINDING,
    STATUS_SUMMARY_REPORTING_MODE,
    SUMMARY_REPORT_DOCUMENT_GENERATION_BOUNDARY_FINDING,
    SUMMARY_REPORT_PRODUCT_RENDERING_BOUNDARY_FINDING,
    SUMMARY_REPORT_REPORT_GENERATION_BOUNDARY_FINDING,
    SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED,
    SUMMARIZATION_REPORTING_ASSISTANCE_READY,
    SUMMARIZATION_REPORTING_FINDING_BLOCKING_SEVERITY,
    build_controlled_summarization_reporting_baseline,
    build_controlled_summarization_reporting_finding,
    build_controlled_summarization_reporting_request,
    build_controlled_summarization_reporting_result,
    validate_controlled_summarization_reporting_request,
    validate_controlled_summarization_reporting_result,
)


def _runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-SUMMARY-001",
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
        context_package_id="CTXPKG-SUMMARY-001",
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
        generation_request_id="GEN-SUMMARY-001",
        context_package=_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _quality_gate(*, content_contract_satisfied: bool = True) -> dict[str, object]:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-SUMMARY-001",
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
        acceptance_decision_id="ACC-SUMMARY-001",
        candidate_output=candidate,
    )
    return build_ai_quality_gate_result(
        quality_gate_result_id="QG-SUMMARY-001",
        source_acceptance_decision=decision,
    )


def _summary_request() -> dict[str, object]:
    return build_controlled_summarization_reporting_request(
        summary_reporting_request_id="SUMREQ-001",
        source_quality_gate_result=_quality_gate(),
        summary_target_ref="SUMMARY-TARGET-URS@v1",
        summary_target_family=DOCUMENT_ARTIFACT_SUMMARY_TARGET,
        summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
        reporting_assistance_mode=STATUS_SUMMARY_REPORTING_MODE,
    )


def test_summarization_reporting_baseline_exposes_m18_2_scope_and_deferrals() -> None:
    baseline = build_controlled_summarization_reporting_baseline()

    assert baseline["checkpoint"] == AI_CONTROLLED_SUMMARIZATION_REPORTING_CHECKPOINT_ID
    assert "actual_llm_calls" in baseline["not_owned_by_m18_2"]
    assert "prompt_templates" in baseline["not_owned_by_m18_2"]
    assert "actual_document_generation_from_expanded_governed_library_content" in baseline["not_owned_by_m18_2"]
    assert "product_ready_report_rendering" in baseline["not_owned_by_m18_2"]
    assert "controlled_recommendation_behavior" in baseline["not_owned_by_m18_2"]


def test_valid_summary_reporting_request_and_result_are_advisory_only() -> None:
    result = build_controlled_summarization_reporting_result(
        summary_reporting_result_id="SUMRES-001",
        summary_reporting_request=_summary_request(),
    )

    assert result["summarization_reporting_assistance_result"] == SUMMARIZATION_REPORTING_ASSISTANCE_READY
    assert result["advisory_only"] is True
    assert result["ai_can_approve"] is False
    assert result["ai_can_release"] is False
    assert result["ai_can_mutate_workflow_state"] is False
    assert result["ai_can_generate_document"] is False
    assert result["ai_can_generate_report"] is False
    assert result["ai_can_render_product_ready_report"] is False
    assert result["ai_can_recommend"] is False
    validate_controlled_summarization_reporting_result(result)


def test_summarization_reporting_request_requires_passing_source_quality_gate() -> None:
    with pytest.raises(ValueError, match="passing source quality gate"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-FAILED-GATE",
            source_quality_gate_result=_quality_gate(content_contract_satisfied=False),
            summary_target_ref="SUMMARY-TARGET-URS@v1",
            summary_target_family=DOCUMENT_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=STATUS_SUMMARY_REPORTING_MODE,
        )


def test_summarization_reporting_request_rejects_approval_release_and_state_mutation() -> None:
    with pytest.raises(ValueError, match="approval_requested to be False"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-APPROVAL",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-URS@v1",
            summary_target_family=DOCUMENT_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=STATUS_SUMMARY_REPORTING_MODE,
            approval_requested=True,
        )

    with pytest.raises(ValueError, match="state_mutation_requested to be False"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-MUTATION",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-URS@v1",
            summary_target_family=DOCUMENT_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=STATUS_SUMMARY_REPORTING_MODE,
            state_mutation_requested=True,
        )


def test_summarization_reporting_request_rejects_document_and_report_generation_scope() -> None:
    with pytest.raises(ValueError, match="document_generation_requested to be False"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-DOCGEN",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-URS@v1",
            summary_target_family=DOCUMENT_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=STATUS_SUMMARY_REPORTING_MODE,
            document_generation_requested=True,
        )

    with pytest.raises(ValueError, match="report_generation_requested to be False"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-REPORTGEN",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-REPORT@v1",
            summary_target_family=REPORTING_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=EVIDENCE_TRACE_REPORTING_MODE,
            report_generation_requested=True,
        )


def test_summarization_reporting_request_rejects_product_rendering_and_recommendations() -> None:
    with pytest.raises(ValueError, match="product_ready_rendering_requested to be False"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-RENDER",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-REPORT@v1",
            summary_target_family=REPORTING_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=DETAIL_DISCIPLINE_REPORTING_MODE,
            product_ready_rendering_requested=True,
        )

    with pytest.raises(ValueError, match="recommendation_requested to be False"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-RECOMMEND",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-REPORT@v1",
            summary_target_family=REPORTING_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=DETAIL_DISCIPLINE_REPORTING_MODE,
            recommendation_requested=True,
        )


def test_summarization_reporting_request_rejects_template_product_implementation_scope() -> None:
    with pytest.raises(
        ValueError,
        match="document_template_product_implementation_requested to be False",
    ):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-TEMPLATE-PRODUCT",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-URS@v1",
            summary_target_family=DOCUMENT_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=STATUS_SUMMARY_REPORTING_MODE,
            document_template_product_implementation_requested=True,
        )


def test_summarization_reporting_request_rejects_evidence_ref_outside_source_quality_gate() -> None:
    with pytest.raises(ValueError, match="outside the passed source quality gate"):
        build_controlled_summarization_reporting_request(
            summary_reporting_request_id="SUMREQ-BAD-EVIDENCE",
            source_quality_gate_result=_quality_gate(),
            summary_target_ref="SUMMARY-TARGET-URS@v1",
            summary_target_family=DOCUMENT_ARTIFACT_SUMMARY_TARGET,
            summarization_mode=EVIDENCE_BOUND_SUMMARIZATION_MODE,
            reporting_assistance_mode=STATUS_SUMMARY_REPORTING_MODE,
            summary_evidence_refs=["MISSING-EVIDENCE@v1"],
        )


def test_controlled_reporting_findings_are_metadata_only_and_identify_findings() -> None:
    finding = build_controlled_summarization_reporting_finding(
        finding_id="SUMFIND-001",
        finding_category=SUMMARY_REPORT_REPORT_GENERATION_BOUNDARY_FINDING,
        finding_severity=SUMMARIZATION_REPORTING_FINDING_BLOCKING_SEVERITY,
        evidence_ref="TEMPLATE-URS@v1",
        source_ref="TEMPLATE-URS@v1",
    )
    result = build_controlled_summarization_reporting_result(
        summary_reporting_result_id="SUMRES-FINDINGS",
        summary_reporting_request=_summary_request(),
        summary_reporting_findings=[finding],
    )

    assert result["summarization_reporting_assistance_result"] == SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED
    assert result["summary_reporting_findings"][0]["finding_category"] == SUMMARY_REPORT_REPORT_GENERATION_BOUNDARY_FINDING
    validate_controlled_summarization_reporting_result(result)


def test_summarization_reporting_result_rejects_finding_ref_outside_request_scope() -> None:
    finding = build_controlled_summarization_reporting_finding(
        finding_id="SUMFIND-BAD-REF",
        finding_category=SUMMARY_REPORT_DOCUMENT_GENERATION_BOUNDARY_FINDING,
        evidence_ref="MISSING-EVIDENCE@v1",
        source_ref="TEMPLATE-URS@v1",
    )

    with pytest.raises(ValueError, match="evidence_ref must be inside request evidence refs"):
        build_controlled_summarization_reporting_result(
            summary_reporting_result_id="SUMRES-BAD-REF",
            summary_reporting_request=_summary_request(),
            summary_reporting_findings=[finding],
        )


def test_summarization_reporting_payloads_reject_generated_text_and_product_rendering_payloads() -> None:
    request = _summary_request()
    request["generated_summary_text"] = "This must not be accepted."

    with pytest.raises(ValueError, match="generated_summary_text is not allowed"):
        validate_controlled_summarization_reporting_request(request)

    result = build_controlled_summarization_reporting_result(
        summary_reporting_result_id="SUMRES-RENDER-PAYLOAD",
        summary_reporting_request=_summary_request(),
    )
    result["product_ready_report_payload"] = {"format": "pdf"}

    with pytest.raises(ValueError, match="product_ready_report_payload is not allowed"):
        validate_controlled_summarization_reporting_result(result)


def test_detail_discipline_issue_can_be_flagged_without_generating_report_content() -> None:
    finding = build_controlled_summarization_reporting_finding(
        finding_id="SUMFIND-DETAIL",
        finding_category=REPORTING_DETAIL_DISCIPLINE_FINDING,
        evidence_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
        source_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )
    result = build_controlled_summarization_reporting_result(
        summary_reporting_result_id="SUMRES-DETAIL",
        summary_reporting_request=_summary_request(),
        summary_reporting_findings=[finding],
    )

    assert result["summarization_reporting_assistance_result"] == SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED
    assert result["ai_can_generate_report"] is False
    assert result["ai_can_render_product_ready_report"] is False
    assert result["summary_reporting_findings"][0]["finding_category"] == REPORTING_DETAIL_DISCIPLINE_FINDING


def test_product_rendering_pressure_can_be_flagged_only_as_boundary_finding() -> None:
    finding = build_controlled_summarization_reporting_finding(
        finding_id="SUMFIND-RENDER",
        finding_category=SUMMARY_REPORT_PRODUCT_RENDERING_BOUNDARY_FINDING,
        evidence_ref="TEMPLATE-URS@v1",
        source_ref="TEMPLATE-URS@v1",
    )
    result = build_controlled_summarization_reporting_result(
        summary_reporting_result_id="SUMRES-RENDER",
        summary_reporting_request=_summary_request(),
        summary_reporting_findings=[finding],
    )

    assert result["summarization_reporting_assistance_result"] == SUMMARIZATION_REPORTING_ASSISTANCE_FINDINGS_IDENTIFIED
    assert result["ai_can_render_product_ready_report"] is False
    assert result["summary_reporting_findings"][0]["finding_category"] == SUMMARY_REPORT_PRODUCT_RENDERING_BOUNDARY_FINDING
