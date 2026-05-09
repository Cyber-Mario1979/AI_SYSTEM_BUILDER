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
    ACTION_EXECUTION_REQUEST_FAMILY,
    APPROVAL_OR_RELEASE_REFUSAL,
    APPROVAL_OR_RELEASE_REQUEST_FAMILY,
    AUTONOMOUS_AGENTIC_BEHAVIOR_REFUSAL,
    CONTROLLED_RECOMMENDATION_ASSISTANCE_REQUEST_FAMILY,
    CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY,
    CONTROLLED_SUMMARIZATION_REPORTING_ASSISTANCE_REQUEST_FAMILY,
    DIRECT_LLM_CALL_REQUEST_FAMILY,
    DOCUMENT_GENERATION_REFUSAL,
    DOCUMENT_GENERATION_REQUEST_FAMILY,
    HUMAN_REVIEW_REQUIRED_FALLBACK,
    INSUFFICIENT_EVIDENCE_FALLBACK,
    INSUFFICIENT_EVIDENCE_FALLBACK_REQUEST_FAMILY,
    PROMPT_TEMPLATE_OR_DIRECT_LLM_REFUSAL,
    UI_API_CLOUD_PRODUCTIZATION_REFUSAL,
    UI_API_CLOUD_PRODUCTIZATION_REQUEST_FAMILY,
    UNSUPPORTED_WORKFLOW_EXPANSION_FAMILY_REFUSAL,
    WORKFLOW_EXPANSION_ALLOWED,
    WORKFLOW_EXPANSION_FALLBACK_ONLY,
    WORKFLOW_EXPANSION_REFUSED,
    build_ai_workflow_expansion_boundaries_baseline,
    build_workflow_expansion_boundary_decision,
    build_workflow_expansion_boundary_request,
    classify_workflow_expansion_request,
    validate_workflow_expansion_boundary_decision,
    validate_workflow_expansion_boundary_request,
)


def _runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-WFX-001",
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
        context_package_id="CTXPKG-WFX-001",
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
        generation_request_id="GEN-WFX-001",
        context_package=_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _quality_gate(*, content_contract_satisfied: bool = True) -> dict[str, object]:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-WFX-001",
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
        acceptance_decision_id="ACC-WFX-001",
        candidate_output=candidate,
    )
    return build_ai_quality_gate_result(
        quality_gate_result_id="QG-WFX-001",
        source_acceptance_decision=decision,
    )


def _boundary_request(
    *,
    family: str = CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY,
    **kwargs: object,
) -> dict[str, object]:
    return build_workflow_expansion_boundary_request(
        workflow_expansion_request_id="WFXREQ-001",
        source_quality_gate_result=_quality_gate(),
        expansion_request_ref="WFX-REQUEST@v1",
        expansion_request_family=family,
        **kwargs,
    )


def test_workflow_expansion_baseline_exposes_m18_4_scope_and_deferrals() -> None:
    baseline = build_ai_workflow_expansion_boundaries_baseline()

    assert baseline["checkpoint"] == "M18.4"
    assert CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY in baseline["supported_allowed_request_families"]
    assert CONTROLLED_SUMMARIZATION_REPORTING_ASSISTANCE_REQUEST_FAMILY in baseline["supported_allowed_request_families"]
    assert CONTROLLED_RECOMMENDATION_ASSISTANCE_REQUEST_FAMILY in baseline["supported_allowed_request_families"]
    assert DOCUMENT_GENERATION_REQUEST_FAMILY in baseline["supported_out_of_scope_request_families"]
    assert "autonomous_agentic_behavior" in baseline["not_owned_by_m18_4"]
    assert "milestone_uat_checkpoint" in baseline["not_owned_by_m18_4"]


@pytest.mark.parametrize(
    "family",
    [
        CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY,
        CONTROLLED_SUMMARIZATION_REPORTING_ASSISTANCE_REQUEST_FAMILY,
        CONTROLLED_RECOMMENDATION_ASSISTANCE_REQUEST_FAMILY,
    ],
)
def test_allowed_m18_assistance_families_are_classified_as_allowed(family: str) -> None:
    request = _boundary_request(family=family)
    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id=f"WFXDEC-{family}",
        workflow_expansion_request=request,
    )

    assert classify_workflow_expansion_request(request) == WORKFLOW_EXPANSION_ALLOWED
    assert decision["workflow_expansion_decision"] == WORKFLOW_EXPANSION_ALLOWED
    assert decision["refusal_reasons"] == []
    assert decision["fallback_reasons"] == []
    assert decision["advisory_only"] is True
    assert decision["human_review_required"] is True
    assert decision["ai_can_approve"] is False
    assert decision["ai_can_mutate_workflow_state"] is False
    assert decision["ai_can_generate_document"] is False
    assert decision["ai_can_call_llm_directly"] is False
    validate_workflow_expansion_boundary_decision(decision)


def test_out_of_scope_request_family_is_refused_with_deterministic_reason() -> None:
    request = _boundary_request(family=APPROVAL_OR_RELEASE_REQUEST_FAMILY)
    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-REFUSED",
        workflow_expansion_request=request,
    )

    assert decision["workflow_expansion_decision"] == WORKFLOW_EXPANSION_REFUSED
    assert decision["refusal_reasons"] == [APPROVAL_OR_RELEASE_REFUSAL]
    assert decision["fallback_reasons"] == []
    assert decision["ai_can_release"] is False


def test_out_of_scope_flags_refuse_even_allowed_request_family() -> None:
    request = _boundary_request(
        family=CONTROLLED_RECOMMENDATION_ASSISTANCE_REQUEST_FAMILY,
        document_generation_requested=True,
        direct_llm_call_requested=True,
    )
    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-FLAGS",
        workflow_expansion_request=request,
    )

    assert decision["workflow_expansion_decision"] == WORKFLOW_EXPANSION_REFUSED
    assert DOCUMENT_GENERATION_REFUSAL in decision["refusal_reasons"]
    assert PROMPT_TEMPLATE_OR_DIRECT_LLM_REFUSAL in decision["refusal_reasons"]
    assert decision["document_generation_payload_included"] is False
    assert decision["direct_llm_call_payload_included"] is False


def test_fallback_only_request_family_returns_fallback_metadata() -> None:
    request = _boundary_request(family=INSUFFICIENT_EVIDENCE_FALLBACK_REQUEST_FAMILY)
    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-FALLBACK",
        workflow_expansion_request=request,
    )

    assert decision["workflow_expansion_decision"] == WORKFLOW_EXPANSION_FALLBACK_ONLY
    assert decision["refusal_reasons"] == []
    assert decision["fallback_reasons"] == [
        HUMAN_REVIEW_REQUIRED_FALLBACK,
        INSUFFICIENT_EVIDENCE_FALLBACK,
    ]
    assert decision["may_emit_boundary_metadata"] is True


def test_unsupported_request_family_is_refused_deterministically() -> None:
    request = _boundary_request(family="unsupported_expansion_family")
    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-UNSUPPORTED",
        workflow_expansion_request=request,
    )

    assert decision["workflow_expansion_decision"] == WORKFLOW_EXPANSION_REFUSED
    assert decision["refusal_reasons"] == [UNSUPPORTED_WORKFLOW_EXPANSION_FAMILY_REFUSAL]


def test_request_requires_passing_quality_gate() -> None:
    with pytest.raises(ValueError, match="requires a passing source quality gate"):
        build_workflow_expansion_boundary_request(
            workflow_expansion_request_id="WFXREQ-FAILED-QG",
            source_quality_gate_result=_quality_gate(content_contract_satisfied=False),
            expansion_request_ref="WFX-REQUEST@v1",
            expansion_request_family=CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY,
        )


def test_request_rejects_evidence_ref_outside_source_quality_gate() -> None:
    with pytest.raises(ValueError, match="outside the passed source quality gate"):
        build_workflow_expansion_boundary_request(
            workflow_expansion_request_id="WFXREQ-BAD-EVIDENCE",
            source_quality_gate_result=_quality_gate(),
            expansion_request_ref="WFX-REQUEST@v1",
            expansion_request_family=CONTROLLED_REVIEW_ASSISTANCE_REQUEST_FAMILY,
            workflow_expansion_evidence_refs=["MISSING-EVIDENCE@v1"],
        )


def test_payloads_reject_direct_execution_generation_and_productization_fields() -> None:
    request = _boundary_request()
    request["state_mutation_payload"] = {"status": "approved"}

    with pytest.raises(ValueError, match="state_mutation_payload is not allowed"):
        validate_workflow_expansion_boundary_request(request)

    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-PROHIBITED",
        workflow_expansion_request=_boundary_request(),
    )
    decision["ui_api_payload"] = {"route": "/api"}

    with pytest.raises(ValueError, match="ui_api_payload is not allowed"):
        validate_workflow_expansion_boundary_decision(decision)


def test_decision_rejects_tampered_decision_or_reasons() -> None:
    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-TAMPER",
        workflow_expansion_request=_boundary_request(family=DOCUMENT_GENERATION_REQUEST_FAMILY),
    )

    decision["workflow_expansion_decision"] = WORKFLOW_EXPANSION_ALLOWED
    with pytest.raises(ValueError, match="does not match deterministic classification"):
        validate_workflow_expansion_boundary_decision(decision)

    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-TAMPER-REASON",
        workflow_expansion_request=_boundary_request(family=UI_API_CLOUD_PRODUCTIZATION_REQUEST_FAMILY),
    )
    decision["refusal_reasons"] = [AUTONOMOUS_AGENTIC_BEHAVIOR_REFUSAL]
    with pytest.raises(ValueError, match="refusal_reasons must match request"):
        validate_workflow_expansion_boundary_decision(decision)


def test_multiple_out_of_scope_flags_are_deduplicated_and_sorted() -> None:
    request = _boundary_request(
        family=ACTION_EXECUTION_REQUEST_FAMILY,
        action_execution_requested=True,
        autonomous_action_requested=True,
        cloud_or_saas_behavior_requested=True,
    )
    decision = build_workflow_expansion_boundary_decision(
        workflow_expansion_decision_id="WFXDEC-MULTI-REFUSAL",
        workflow_expansion_request=request,
    )

    assert decision["workflow_expansion_decision"] == WORKFLOW_EXPANSION_REFUSED
    assert AUTONOMOUS_AGENTIC_BEHAVIOR_REFUSAL in decision["refusal_reasons"]
    assert UI_API_CLOUD_PRODUCTIZATION_REFUSAL in decision["refusal_reasons"]
    assert len(decision["refusal_reasons"]) == len(set(decision["refusal_reasons"]))
