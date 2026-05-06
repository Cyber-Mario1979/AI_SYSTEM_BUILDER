import pytest

from asbp.ai_runtime import (
    ACCEPT_CANDIDATE_OUTPUT_DECISION,
    AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID,
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    BOUNDED_REPORT_SUMMARY_MODE,
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    EXPORT_ENGINE_CALLER_BOUNDARY,
    EXPORT_REPORTING_REQUIREMENT_SOURCE_FAMILY,
    FALLBACK_OR_REFUSE_OUTPUT_DECISION,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_ENGINE_INPUT_ROLE,
    GOVERNED_REPORTING_JOB_FAMILY,
    INSUFFICIENT_EVIDENCE_FALLBACK_REASON,
    PARTIAL_EVIDENCE_STATUS,
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    RETRY_CANDIDATE_OUTPUT_DECISION,
    RETRY_LIMIT_REACHED_FALLBACK_REASON,
    REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
    STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    STRUCTURED_INPUT_PAYLOAD_CLASSIFICATION,
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    UNAVAILABLE_EVIDENCE_STATUS,
    URS_DOCUMENT_FAMILY,
    VALIDATED_EVIDENCE_STATUS,
    build_ai_candidate_output,
    build_ai_context_item,
    build_ai_context_package,
    build_ai_generation_mode_request,
    build_ai_output_acceptance_baseline,
    build_ai_output_acceptance_decision,
    build_ai_runtime_entry_request,
    validate_ai_candidate_output,
    validate_ai_output_acceptance_decision,
)


def _document_runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-DOC-ACCEPT-001",
        job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
        caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
        governed_source_refs=[
            "TEMPLATE-URS@v1",
            "DOCUMENT-LIFECYCLE-STATE@v1",
            "STANDARDS-GUARDRAIL-CONTEXT@v1",
            "DCF-EXTRACTED-INPUT@v1",
        ],
        engine_contract_refs=[
            "DOCUMENT-REQUEST-CONTRACT@v1",
            "DOCUMENT-OUTPUT-CONTRACT@v1",
        ],
    )


def _document_context_package(
    *, dcf_status: str = VALIDATED_EVIDENCE_STATUS
) -> dict[str, object]:
    return build_ai_context_package(
        context_package_id="CTXPKG-DOC-ACCEPT-001",
        ai_runtime_entry_request=_document_runtime_request(),
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
            build_ai_context_item(
                context_item_id="CTX-DCF",
                source_family="dcf_extracted_input",
                source_ref="DCF-EXTRACTED-INPUT@v1",
                source_role=GOVERNED_ENGINE_INPUT_ROLE,
                payload_classification=STRUCTURED_INPUT_PAYLOAD_CLASSIFICATION,
                evidence_status=dcf_status,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
        ],
    )


def _document_generation_request(
    *, dcf_status: str = VALIDATED_EVIDENCE_STATUS
) -> dict[str, object]:
    mode = (
        PARTIAL_INPUT_BOUNDED_COMPLETION_MODE
        if dcf_status == PARTIAL_EVIDENCE_STATUS
        else STRONG_STRUCTURED_INPUT_FILL_MODE
    )
    return build_ai_generation_mode_request(
        generation_request_id="GEN-DOC-ACCEPT-001",
        context_package=_document_context_package(dcf_status=dcf_status),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=mode,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _reporting_generation_request() -> dict[str, object]:
    runtime_request = build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-REPORT-ACCEPT-001",
        job_family=GOVERNED_REPORTING_JOB_FAMILY,
        caller_boundary=EXPORT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile="bounded_summarization",
        governed_source_refs=[
            "REPORTING-REQUIREMENT@v1",
            "STANDARDS-GUARDRAIL-CONTEXT@v1",
        ],
        engine_contract_refs=[
            "EXPORT-REQUEST-CONTRACT@v1",
            "REPORTING-SURFACE-CONTRACT@v1",
        ],
    )
    context_package = build_ai_context_package(
        context_package_id="CTXPKG-REPORT-ACCEPT-001",
        ai_runtime_entry_request=runtime_request,
        context_items=[
            build_ai_context_item(
                context_item_id="CTX-REPORTING-REQ",
                source_family=EXPORT_REPORTING_REQUIREMENT_SOURCE_FAMILY,
                source_ref="REPORTING-REQUIREMENT@v1",
                source_role=GOVERNED_CONTRACT_ROLE,
                payload_classification=REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
                evidence_status=VALIDATED_EVIDENCE_STATUS,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
            build_ai_context_item(
                context_item_id="CTX-REPORTING-STANDARDS",
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
    return build_ai_generation_mode_request(
        generation_request_id="GEN-REPORT-ACCEPT-001",
        context_package=context_package,
        output_family="dashboard_summary_reporting",
        generation_mode=BOUNDED_REPORT_SUMMARY_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _passing_candidate(
    *, candidate_evidence_status: str = VALIDATED_EVIDENCE_STATUS
) -> dict[str, object]:
    return build_ai_candidate_output(
        output_candidate_id="CAND-DOC-001",
        generation_mode_request=_document_generation_request(
            dcf_status=(
                PARTIAL_EVIDENCE_STATUS
                if candidate_evidence_status == PARTIAL_EVIDENCE_STATUS
                else VALIDATED_EVIDENCE_STATUS
            )
        ),
        candidate_output_ref="AI-CANDIDATE-DOC@v1",
        candidate_evidence_status=candidate_evidence_status,
        content_contract_satisfied=True,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=True,
        assumptions_labeled_when_required=True,
        placeholders_used_for_missing_truth=True,
    )


def test_output_acceptance_baseline_exposes_m16_4_rules() -> None:
    baseline = build_ai_output_acceptance_baseline()

    assert baseline["checkpoint"] == AI_OUTPUT_ACCEPTANCE_CHECKPOINT_ID
    assert ACCEPT_CANDIDATE_OUTPUT_DECISION in baseline[
        "supported_output_acceptance_decisions"
    ]
    assert "workflow_state_mutation" in baseline["not_owned_by_m16_4"]
    assert baseline["bounded_retry_policy"] == (
        "retry_is_limited_and_must_not_relax_generation_mode_or_contract_rules"
    )


def test_candidate_output_accepts_valid_document_candidate_metadata() -> None:
    candidate = _passing_candidate()

    assert candidate["candidate_output_ref"] == "AI-CANDIDATE-DOC@v1"
    assert candidate["accepted_as_final_output"] is False
    validate_ai_candidate_output(candidate)


def test_output_acceptance_decision_accepts_passing_candidate() -> None:
    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="ACCEPT-DOC-001",
        candidate_output=_passing_candidate(),
    )

    assert decision["acceptance_decision"] == ACCEPT_CANDIDATE_OUTPUT_DECISION
    assert decision["accepted_for_downstream_review"] is True
    assert decision["retry_allowed"] is False
    assert decision["fallback_or_refusal_required"] is False
    validate_ai_output_acceptance_decision(decision)


def test_partial_input_candidate_can_be_accepted_when_controls_are_satisfied() -> None:
    candidate = _passing_candidate(candidate_evidence_status=PARTIAL_EVIDENCE_STATUS)

    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="ACCEPT-PARTIAL-001",
        candidate_output=candidate,
    )

    assert decision["acceptance_decision"] == ACCEPT_CANDIDATE_OUTPUT_DECISION
    validate_ai_output_acceptance_decision(decision)


def test_reporting_candidate_uses_reporting_classification_and_can_be_accepted() -> None:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-REPORT-001",
        generation_mode_request=_reporting_generation_request(),
        candidate_output_ref="AI-CANDIDATE-REPORT@v1",
        candidate_evidence_status=VALIDATED_EVIDENCE_STATUS,
        content_contract_satisfied=True,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=True,
        assumptions_labeled_when_required=True,
        placeholders_used_for_missing_truth=True,
    )

    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="ACCEPT-REPORT-001",
        candidate_output=candidate,
    )

    assert candidate["candidate_output_classification"] == "candidate_reporting_language"
    assert decision["acceptance_decision"] == ACCEPT_CANDIDATE_OUTPUT_DECISION


def test_output_acceptance_decision_retries_failed_candidate_before_limit() -> None:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-RETRY-001",
        generation_mode_request=_document_generation_request(),
        candidate_output_ref="AI-CANDIDATE-RETRY@v1",
        candidate_evidence_status=VALIDATED_EVIDENCE_STATUS,
        content_contract_satisfied=False,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=True,
        assumptions_labeled_when_required=True,
        placeholders_used_for_missing_truth=True,
    )

    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="RETRY-DOC-001",
        candidate_output=candidate,
        retry_attempt_number=0,
        max_retry_attempts=2,
    )

    assert decision["acceptance_decision"] == RETRY_CANDIDATE_OUTPUT_DECISION
    assert decision["retry_allowed"] is True
    assert decision["fallback_or_refusal_required"] is False


def test_output_acceptance_decision_fallbacks_at_retry_limit() -> None:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-FALLBACK-LIMIT",
        generation_mode_request=_document_generation_request(),
        candidate_output_ref="AI-CANDIDATE-FALLBACK@v1",
        candidate_evidence_status=VALIDATED_EVIDENCE_STATUS,
        content_contract_satisfied=False,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=True,
        assumptions_labeled_when_required=True,
        placeholders_used_for_missing_truth=True,
    )

    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="FALLBACK-DOC-001",
        candidate_output=candidate,
        retry_attempt_number=2,
        max_retry_attempts=2,
    )

    assert decision["acceptance_decision"] == FALLBACK_OR_REFUSE_OUTPUT_DECISION
    assert decision["fallback_reason"] == RETRY_LIMIT_REACHED_FALLBACK_REASON


def test_output_acceptance_decision_fallbacks_when_evidence_is_unavailable() -> None:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-INSUFFICIENT-EVIDENCE",
        generation_mode_request=_document_generation_request(),
        candidate_output_ref="AI-CANDIDATE-INSUFFICIENT@v1",
        candidate_evidence_status=UNAVAILABLE_EVIDENCE_STATUS,
        content_contract_satisfied=True,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=False,
        assumptions_labeled_when_required=True,
        placeholders_used_for_missing_truth=True,
    )

    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="FALLBACK-EVIDENCE-001",
        candidate_output=candidate,
    )

    assert decision["acceptance_decision"] == FALLBACK_OR_REFUSE_OUTPUT_DECISION
    assert decision["fallback_reason"] == INSUFFICIENT_EVIDENCE_FALLBACK_REASON


def test_candidate_output_rejects_unversioned_candidate_ref() -> None:
    with pytest.raises(ValueError, match="exactly one '@'"):
        build_ai_candidate_output(
            output_candidate_id="CAND-BAD-REF",
            generation_mode_request=_document_generation_request(),
            candidate_output_ref="AI-CANDIDATE-DOC",
            candidate_evidence_status=VALIDATED_EVIDENCE_STATUS,
            content_contract_satisfied=True,
            family_constraints_satisfied=True,
            standards_guardrails_satisfied=True,
            evidence_claims_supported=True,
            assumptions_labeled_when_required=True,
            placeholders_used_for_missing_truth=True,
        )


def test_candidate_output_rejects_generated_text_and_prompt_fields() -> None:
    candidate = _passing_candidate()
    candidate["generated_document_text"] = "M16.4 does not carry generated text."

    with pytest.raises(ValueError, match="generated_document_text"):
        validate_ai_candidate_output(candidate)

    candidate = _passing_candidate()
    candidate["prompt_template"] = "retry with this prompt"

    with pytest.raises(ValueError, match="prompt_template"):
        validate_ai_candidate_output(candidate)


def test_acceptance_decision_rejects_state_mutation_or_approval_claims() -> None:
    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="ACCEPT-NO-MUTATION",
        candidate_output=_passing_candidate(),
    )
    decision["ai_can_approve_or_release"] = True

    with pytest.raises(ValueError, match="ai_can_approve_or_release"):
        validate_ai_output_acceptance_decision(decision)

    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="ACCEPT-NO-MUTATION-2",
        candidate_output=_passing_candidate(),
    )
    decision["state_mutation_payload"] = {"status": "approved"}

    with pytest.raises(ValueError, match="state_mutation_payload"):
        validate_ai_output_acceptance_decision(decision)


def test_acceptance_decision_rejects_manual_decision_that_conflicts_with_rules() -> None:
    decision = build_ai_output_acceptance_decision(
        acceptance_decision_id="ACCEPT-CORRUPTED",
        candidate_output=_passing_candidate(),
    )
    decision["acceptance_decision"] = RETRY_CANDIDATE_OUTPUT_DECISION

    with pytest.raises(ValueError, match="does not match deterministic acceptance"):
        validate_ai_output_acceptance_decision(decision)
