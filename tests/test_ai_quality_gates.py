import pytest

from asbp.ai_evaluation import (
    ACCEPTANCE_DECISION_NOT_ACCEPT_FAILURE,
    AI_QUALITY_GATES_CHECKPOINT_ID,
    EVIDENCE_LINK_CHECK_FAIL,
    EVIDENCE_REF_NOT_IN_CONTEXT_FAILURE,
    EVIDENCE_REF_UNAVAILABLE_FAILURE,
    GROUNDEDNESS_CHECK_FAIL,
    GROUNDEDNESS_CHECK_PASS,
    MISSING_TRUTH_PLACEHOLDER_FAILURE,
    NON_AUTHORITATIVE_SOURCE_AS_TRUTH_FAILURE,
    QUALITY_GATE_FAIL,
    QUALITY_GATE_PASS,
    SOURCE_ROLE_CHECK_FAIL,
    SOURCE_ROLE_CHECK_PASS,
    UNLABELED_ASSUMPTION_FAILURE,
    UNSUPPORTED_EVIDENCE_CLAIM_FAILURE,
    build_ai_quality_gate_result,
    build_ai_quality_gates_baseline,
    build_groundedness_check_result,
    validate_ai_quality_gate_result,
)
from asbp.ai_runtime import (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_ENGINE_INPUT_ROLE,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
    REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
    STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    SUPPORTING_CONTEXT_PAYLOAD_CLASSIFICATION,
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    URS_DOCUMENT_FAMILY,
    VALIDATED_EVIDENCE_STATUS,
    UNAVAILABLE_EVIDENCE_STATUS,
    build_ai_candidate_output,
    build_ai_context_item,
    build_ai_context_package,
    build_ai_generation_mode_request,
    build_ai_output_acceptance_decision,
    build_ai_runtime_entry_request,
)


def _runtime_request(*, include_support_ref: bool = False) -> dict[str, object]:
    governed_source_refs = [
        "TEMPLATE-URS@v1",
        "DOCUMENT-LIFECYCLE-STATE@v1",
        "STANDARDS-GUARDRAIL-CONTEXT@v1",
    ]
    if include_support_ref:
        governed_source_refs.append("SUPPORT-CONTEXT@v1")
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-GATE-001",
        job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
        caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
        governed_source_refs=governed_source_refs,
        engine_contract_refs=[
            "DOCUMENT-REQUEST-CONTRACT@v1",
            "DOCUMENT-OUTPUT-CONTRACT@v1",
        ],
    )


def _context_package(
    *,
    include_support_context: bool = False,
    support_evidence_status: str = VALIDATED_EVIDENCE_STATUS,
) -> dict[str, object]:
    context_items = [
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
    ]
    if include_support_context:
        context_items.append(
            build_ai_context_item(
                context_item_id="CTX-SUPPORT",
                source_family=TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
                source_ref="SUPPORT-CONTEXT@v1",
                source_role=NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
                payload_classification=SUPPORTING_CONTEXT_PAYLOAD_CLASSIFICATION,
                evidence_status=support_evidence_status,
                is_authoritative=False,
                may_be_used_for_generation=True,
            )
        )

    return build_ai_context_package(
        context_package_id="CTXPKG-GATE-001",
        ai_runtime_entry_request=_runtime_request(
            include_support_ref=include_support_context
        ),
        context_items=context_items,
    )


def _generation_request(
    *,
    include_support_context: bool = False,
) -> dict[str, object]:
    return build_ai_generation_mode_request(
        generation_request_id="GEN-GATE-001",
        context_package=_context_package(
            include_support_context=include_support_context,
        ),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _acceptance_decision(
    *,
    content_contract_satisfied: bool = True,
    evidence_claims_supported: bool = True,
    assumptions_labeled_when_required: bool = True,
    placeholders_used_for_missing_truth: bool = True,
    include_support_context: bool = False,
    candidate_evidence_status: str = VALIDATED_EVIDENCE_STATUS,
) -> dict[str, object]:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-GATE-001",
        generation_mode_request=_generation_request(
            include_support_context=include_support_context,
        ),
        candidate_output_ref="CANDIDATE-URS-OUTPUT@v1",
        candidate_evidence_status=candidate_evidence_status,
        content_contract_satisfied=content_contract_satisfied,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=evidence_claims_supported,
        assumptions_labeled_when_required=assumptions_labeled_when_required,
        placeholders_used_for_missing_truth=placeholders_used_for_missing_truth,
    )
    return build_ai_output_acceptance_decision(
        acceptance_decision_id="ACC-GATE-001",
        candidate_output=candidate,
    )


def test_quality_gates_baseline_exposes_m17_2_scope_and_deferrals() -> None:
    baseline = build_ai_quality_gates_baseline()

    assert baseline["checkpoint"] == AI_QUALITY_GATES_CHECKPOINT_ID
    assert "document_template_product_implementation" in baseline["not_owned_by_m17_2"]
    assert "standards_conformance_checks" in baseline["not_owned_by_m17_2"]
    assert "retrieval_use_governance" in baseline["not_owned_by_m17_2"]
    assert "post_m17_pre_m18" in baseline["post_m17_template_reentry_policy"]


def test_valid_grounded_candidate_passes_quality_gate() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-PASS",
        source_acceptance_decision=_acceptance_decision(),
    )

    assert gate["quality_gate_result"] == QUALITY_GATE_PASS
    assert gate["groundedness_check_result"] == GROUNDEDNESS_CHECK_PASS
    assert gate["quality_gate_failure_reasons"] == []
    validate_ai_quality_gate_result(gate)


def test_unsupported_evidence_claim_fails_quality_gate() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-EVIDENCE-FAIL",
        source_acceptance_decision=_acceptance_decision(
            evidence_claims_supported=False,
        ),
    )

    assert gate["quality_gate_result"] == QUALITY_GATE_FAIL
    assert gate["groundedness_check_result"] == GROUNDEDNESS_CHECK_FAIL
    assert ACCEPTANCE_DECISION_NOT_ACCEPT_FAILURE in gate["quality_gate_failure_reasons"]
    assert UNSUPPORTED_EVIDENCE_CLAIM_FAILURE in gate["quality_gate_failure_reasons"]


def test_unlabeled_assumption_fails_quality_gate() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-ASSUMPTION-FAIL",
        source_acceptance_decision=_acceptance_decision(
            assumptions_labeled_when_required=False,
        ),
    )

    assert gate["quality_gate_result"] == QUALITY_GATE_FAIL
    assert UNLABELED_ASSUMPTION_FAILURE in gate["quality_gate_failure_reasons"]


def test_missing_truth_without_placeholder_fails_quality_gate() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-PLACEHOLDER-FAIL",
        source_acceptance_decision=_acceptance_decision(
            placeholders_used_for_missing_truth=False,
        ),
    )

    assert gate["quality_gate_result"] == QUALITY_GATE_FAIL
    assert MISSING_TRUTH_PLACEHOLDER_FAILURE in gate["quality_gate_failure_reasons"]


def test_unavailable_evidence_ref_fails_evidence_link_check() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-UNAVAILABLE-EVIDENCE",
        source_acceptance_decision=_acceptance_decision(
            candidate_evidence_status=UNAVAILABLE_EVIDENCE_STATUS,
        ),
    )

    assert gate["quality_gate_result"] == QUALITY_GATE_FAIL
    assert gate["evidence_link_check_result"] == EVIDENCE_LINK_CHECK_FAIL
    assert EVIDENCE_REF_UNAVAILABLE_FAILURE in gate["quality_gate_failure_reasons"]


def test_unversioned_evidence_ref_is_rejected() -> None:
    with pytest.raises(ValueError, match="exactly one '@'"):
        build_ai_quality_gate_result(
            quality_gate_result_id="QG-BAD-REF",
            source_acceptance_decision=_acceptance_decision(),
            evidence_refs_used=["TEMPLATE-URS"],
        )


def test_missing_evidence_ref_fails_evidence_link_check() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-MISSING-REF",
        source_acceptance_decision=_acceptance_decision(),
        evidence_refs_used=["MISSING-EVIDENCE@v1"],
    )

    assert gate["quality_gate_result"] == QUALITY_GATE_FAIL
    assert gate["evidence_link_check_result"] == EVIDENCE_LINK_CHECK_FAIL
    assert EVIDENCE_REF_NOT_IN_CONTEXT_FAILURE in gate["quality_gate_failure_reasons"]


def test_non_authoritative_support_context_cannot_be_used_as_truth() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-SOURCE-ROLE-FAIL",
        source_acceptance_decision=_acceptance_decision(
            include_support_context=True,
        ),
        evidence_refs_used=["TEMPLATE-URS@v1", "SUPPORT-CONTEXT@v1"],
        source_refs_used_as_truth=["SUPPORT-CONTEXT@v1"],
    )

    assert gate["quality_gate_result"] == QUALITY_GATE_FAIL
    assert gate["source_role_check_result"] == SOURCE_ROLE_CHECK_FAIL
    assert NON_AUTHORITATIVE_SOURCE_AS_TRUTH_FAILURE in gate[
        "quality_gate_failure_reasons"
    ]


def test_quality_gate_fails_if_any_subcheck_fails() -> None:
    groundedness = build_groundedness_check_result(
        groundedness_check_id="GROUND-MISSING-REF",
        source_acceptance_decision=_acceptance_decision(),
        evidence_refs_used=["MISSING-EVIDENCE@v1"],
    )

    assert groundedness["groundedness_check_result"] == GROUNDEDNESS_CHECK_FAIL
    assert groundedness["evidence_link_check_result"] == EVIDENCE_LINK_CHECK_FAIL


def test_quality_gate_does_not_mutate_state_or_authorize_release() -> None:
    gate = build_ai_quality_gate_result(
        quality_gate_result_id="QG-NO-MUTATION",
        source_acceptance_decision=_acceptance_decision(),
    )

    assert gate["actual_llm_call_required"] is False
    assert gate["prompt_template_required"] is False
    assert gate["state_mutation_allowed"] is False
    assert gate["approval_or_release_allowed"] is False
    assert gate["document_template_implementation_in_scope"] is False
    assert gate["standards_conformance_in_scope"] is False
    assert gate["detail_consistency_in_scope"] is False
    assert gate["retrieval_use_governance_in_scope"] is False
