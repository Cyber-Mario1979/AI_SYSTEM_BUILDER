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
    AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID,
    CONTRACT_ALIGNMENT_REVIEW_MODE,
    DOCUMENT_ARTIFACT_REVIEW_TARGET,
    DOCUMENT_GENERATION_BOUNDARY_FINDING,
    DOCUMENT_TEMPLATE_PRODUCT_BOUNDARY_FINDING,
    EVIDENCE_BOUND_REVIEW_MODE,
    LIBRARY_ARCHITECTURE_DEFERRED_SCOPE_FINDING,
    REVIEW_ASSISTANCE_FINDINGS_IDENTIFIED,
    REVIEW_ASSISTANCE_NO_FINDINGS,
    REVIEW_FINDING_BLOCKING_SEVERITY,
    build_controlled_review_assistance_baseline,
    build_controlled_review_assistance_result,
    build_controlled_review_finding,
    build_controlled_review_request,
    validate_controlled_review_assistance_result,
    validate_controlled_review_request,
)


def _runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-REVIEW-001",
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
        context_package_id="CTXPKG-REVIEW-001",
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
        generation_request_id="GEN-REVIEW-001",
        context_package=_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _quality_gate(*, content_contract_satisfied: bool = True) -> dict[str, object]:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-REVIEW-001",
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
        acceptance_decision_id="ACC-REVIEW-001",
        candidate_output=candidate,
    )
    return build_ai_quality_gate_result(
        quality_gate_result_id="QG-REVIEW-001",
        source_acceptance_decision=decision,
    )


def _review_request() -> dict[str, object]:
    return build_controlled_review_request(
        review_request_id="REVREQ-001",
        source_quality_gate_result=_quality_gate(),
        review_target_ref="REVIEW-TARGET-URS@v1",
        review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
        review_mode=EVIDENCE_BOUND_REVIEW_MODE,
    )


def test_review_assistance_baseline_exposes_m18_1_scope_and_deferrals() -> None:
    baseline = build_controlled_review_assistance_baseline()

    assert baseline["checkpoint"] == AI_CONTROLLED_REVIEW_ASSISTANCE_CHECKPOINT_ID
    assert "document_factory" in baseline["not_owned_by_m18_1"]
    assert "document_template_product_implementation" in baseline["not_owned_by_m18_1"]
    assert "library_architecture_cleanup" in baseline["not_owned_by_m18_1"]
    assert "approval_or_release_authority" in baseline["not_owned_by_m18_1"]


def test_valid_review_request_and_no_finding_result_are_advisory_only() -> None:
    result = build_controlled_review_assistance_result(
        review_result_id="REVRES-001",
        review_request=_review_request(),
    )

    assert result["review_assistance_result"] == REVIEW_ASSISTANCE_NO_FINDINGS
    assert result["advisory_only"] is True
    assert result["ai_can_approve"] is False
    assert result["ai_can_release"] is False
    assert result["ai_can_mutate_workflow_state"] is False
    assert result["document_generation_in_scope"] is False
    assert result["document_template_product_implementation_in_scope"] is False
    assert result["library_architecture_change_in_scope"] is False
    validate_controlled_review_assistance_result(result)


def test_review_request_requires_passing_source_quality_gate() -> None:
    with pytest.raises(ValueError, match="passing source quality gate"):
        build_controlled_review_request(
            review_request_id="REVREQ-FAILED-GATE",
            source_quality_gate_result=_quality_gate(content_contract_satisfied=False),
            review_target_ref="REVIEW-TARGET-URS@v1",
            review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
            review_mode=CONTRACT_ALIGNMENT_REVIEW_MODE,
        )


def test_review_request_rejects_approval_release_and_state_mutation() -> None:
    with pytest.raises(ValueError, match="approval_requested to be False"):
        build_controlled_review_request(
            review_request_id="REVREQ-APPROVAL",
            source_quality_gate_result=_quality_gate(),
            review_target_ref="REVIEW-TARGET-URS@v1",
            review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
            review_mode=EVIDENCE_BOUND_REVIEW_MODE,
            approval_requested=True,
        )

    with pytest.raises(ValueError, match="state_mutation_requested to be False"):
        build_controlled_review_request(
            review_request_id="REVREQ-MUTATION",
            source_quality_gate_result=_quality_gate(),
            review_target_ref="REVIEW-TARGET-URS@v1",
            review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
            review_mode=EVIDENCE_BOUND_REVIEW_MODE,
            state_mutation_requested=True,
        )


def test_review_request_rejects_document_generation_and_template_product_scope() -> None:
    with pytest.raises(ValueError, match="document_generation_requested to be False"):
        build_controlled_review_request(
            review_request_id="REVREQ-DOCGEN",
            source_quality_gate_result=_quality_gate(),
            review_target_ref="REVIEW-TARGET-URS@v1",
            review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
            review_mode=EVIDENCE_BOUND_REVIEW_MODE,
            document_generation_requested=True,
        )

    with pytest.raises(
        ValueError,
        match="document_template_product_implementation_requested to be False",
    ):
        build_controlled_review_request(
            review_request_id="REVREQ-TEMPLATE-PRODUCT",
            source_quality_gate_result=_quality_gate(),
            review_target_ref="REVIEW-TARGET-URS@v1",
            review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
            review_mode=EVIDENCE_BOUND_REVIEW_MODE,
            document_template_product_implementation_requested=True,
        )


def test_review_request_rejects_library_architecture_change_scope() -> None:
    with pytest.raises(ValueError, match="library_architecture_change_requested to be False"):
        build_controlled_review_request(
            review_request_id="REVREQ-LIB-ARCH",
            source_quality_gate_result=_quality_gate(),
            review_target_ref="REVIEW-TARGET-URS@v1",
            review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
            review_mode=EVIDENCE_BOUND_REVIEW_MODE,
            library_architecture_change_requested=True,
        )


def test_review_request_rejects_evidence_ref_outside_source_quality_gate() -> None:
    with pytest.raises(ValueError, match="outside the passed source quality gate"):
        build_controlled_review_request(
            review_request_id="REVREQ-BAD-EVIDENCE",
            source_quality_gate_result=_quality_gate(),
            review_target_ref="REVIEW-TARGET-URS@v1",
            review_target_family=DOCUMENT_ARTIFACT_REVIEW_TARGET,
            review_mode=EVIDENCE_BOUND_REVIEW_MODE,
            review_evidence_refs=["MISSING-EVIDENCE@v1"],
        )


def test_controlled_findings_are_metadata_only_and_identify_review_findings() -> None:
    finding = build_controlled_review_finding(
        finding_id="REVFIND-001",
        finding_category=DOCUMENT_TEMPLATE_PRODUCT_BOUNDARY_FINDING,
        finding_severity=REVIEW_FINDING_BLOCKING_SEVERITY,
        evidence_ref="TEMPLATE-URS@v1",
        source_ref="TEMPLATE-URS@v1",
    )
    result = build_controlled_review_assistance_result(
        review_result_id="REVRES-FINDINGS",
        review_request=_review_request(),
        review_findings=[finding],
    )

    assert result["review_assistance_result"] == REVIEW_ASSISTANCE_FINDINGS_IDENTIFIED
    assert result["review_findings"][0]["finding_category"] == DOCUMENT_TEMPLATE_PRODUCT_BOUNDARY_FINDING
    validate_controlled_review_assistance_result(result)


def test_review_result_rejects_finding_ref_outside_request_scope() -> None:
    finding = build_controlled_review_finding(
        finding_id="REVFIND-BAD-REF",
        finding_category=DOCUMENT_GENERATION_BOUNDARY_FINDING,
        evidence_ref="MISSING-EVIDENCE@v1",
        source_ref="TEMPLATE-URS@v1",
    )

    with pytest.raises(ValueError, match="evidence_ref must be inside request evidence refs"):
        build_controlled_review_assistance_result(
            review_result_id="REVRES-BAD-REF",
            review_request=_review_request(),
            review_findings=[finding],
        )


def test_review_payloads_reject_generated_text_and_product_payloads() -> None:
    request = _review_request()
    request["generated_document_text"] = "This must not be accepted."

    with pytest.raises(ValueError, match="generated_document_text is not allowed"):
        validate_controlled_review_request(request)


def test_library_architecture_issue_can_be_flagged_only_as_deferred_scope_finding() -> None:
    finding = build_controlled_review_finding(
        finding_id="REVFIND-LIB-DEFERRED",
        finding_category=LIBRARY_ARCHITECTURE_DEFERRED_SCOPE_FINDING,
        evidence_ref="TEMPLATE-URS@v1",
        source_ref="TEMPLATE-URS@v1",
    )
    result = build_controlled_review_assistance_result(
        review_result_id="REVRES-LIB-DEFERRED",
        review_request=_review_request(),
        review_findings=[finding],
    )

    assert result["review_assistance_result"] == REVIEW_ASSISTANCE_FINDINGS_IDENTIFIED
    assert result["library_architecture_change_in_scope"] is False
    assert result["review_findings"][0]["finding_category"] == LIBRARY_ARCHITECTURE_DEFERRED_SCOPE_FINDING
