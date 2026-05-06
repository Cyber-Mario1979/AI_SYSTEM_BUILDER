import pytest

from asbp.ai_runtime import (
    AI_GENERATION_MODES_CHECKPOINT_ID,
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    BOUNDED_REPORT_SUMMARY_MODE,
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    DASHBOARD_SUMMARY_REPORTING_FAMILY,
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    EVIDENCE_BOUND_REPORT_NARRATIVE_MODE,
    EXPORT_ENGINE_CALLER_BOUNDARY,
    EXPORT_REPORTING_REQUIREMENT_SOURCE_FAMILY,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_ENGINE_INPUT_ROLE,
    GOVERNED_REPORTING_JOB_FAMILY,
    PARTIAL_EVIDENCE_STATUS,
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    PROTOCOL_DOCUMENT_FAMILY,
    REPORT_DOCUMENT_FAMILY,
    REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
    STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    STRUCTURED_INPUT_PAYLOAD_CLASSIFICATION,
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    URS_DOCUMENT_FAMILY,
    VALIDATED_EVIDENCE_STATUS,
    build_ai_context_item,
    build_ai_context_package,
    build_ai_generation_mode_request,
    build_ai_generation_modes_baseline,
    build_ai_runtime_entry_request,
    validate_ai_generation_mode_request,
)


def _document_runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-DOC-GEN-001",
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


def _document_context_items(
    *, standards_status: str = VALIDATED_EVIDENCE_STATUS,
    dcf_status: str = VALIDATED_EVIDENCE_STATUS,
) -> list[dict[str, object]]:
    return [
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
            evidence_status=standards_status,
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
    ]


def _document_context_package(
    *, dcf_status: str = VALIDATED_EVIDENCE_STATUS,
) -> dict[str, object]:
    return build_ai_context_package(
        context_package_id="CTXPKG-DOC-GEN-001",
        ai_runtime_entry_request=_document_runtime_request(),
        context_items=_document_context_items(dcf_status=dcf_status),
    )


def _reporting_context_package() -> dict[str, object]:
    runtime_request = build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-REPORT-GEN-001",
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
    return build_ai_context_package(
        context_package_id="CTXPKG-REPORT-GEN-001",
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


def test_generation_modes_baseline_exposes_m16_3_rules() -> None:
    baseline = build_ai_generation_modes_baseline()

    assert baseline["checkpoint"] == AI_GENERATION_MODES_CHECKPOINT_ID
    assert URS_DOCUMENT_FAMILY in baseline["supported_document_output_families"]
    assert BOUNDED_REPORT_SUMMARY_MODE in baseline["supported_generation_modes"]
    assert "actual_llm_calls" in baseline["not_owned_by_m16_3"]
    assert baseline["bounded_invention_policy"] == (
        "bounded_invention_is_mode_specific_labeled_and_never_source_truth"
    )


def test_build_generation_mode_request_accepts_strong_urs_document_mode() -> None:
    request = build_ai_generation_mode_request(
        generation_request_id="GEN-DOC-001",
        context_package=_document_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )

    assert request["checkpoint"] == AI_GENERATION_MODES_CHECKPOINT_ID
    assert request["bounded_invention_allowed"] is False
    assert request["requested_output_role"] == "candidate_language_output"
    validate_ai_generation_mode_request(request)


def test_build_generation_mode_request_accepts_partial_protocol_mode_with_partial_input() -> None:
    request = build_ai_generation_mode_request(
        generation_request_id="GEN-DOC-PARTIAL-001",
        context_package=_document_context_package(dcf_status=PARTIAL_EVIDENCE_STATUS),
        output_family=PROTOCOL_DOCUMENT_FAMILY,
        generation_mode=PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )

    assert request["bounded_invention_allowed"] is True
    assert request["assumption_labeling_required"] is True
    validate_ai_generation_mode_request(request)


def test_build_generation_mode_request_accepts_reporting_summary_mode() -> None:
    request = build_ai_generation_mode_request(
        generation_request_id="GEN-REPORT-001",
        context_package=_reporting_context_package(),
        output_family=DASHBOARD_SUMMARY_REPORTING_FAMILY,
        generation_mode=BOUNDED_REPORT_SUMMARY_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )

    assert request["job_family"] == GOVERNED_REPORTING_JOB_FAMILY
    assert request["requested_output_role"] == "bounded_summary_output"
    validate_ai_generation_mode_request(request)


def test_generation_mode_request_rejects_reporting_mode_for_document_family() -> None:
    with pytest.raises(ValueError, match="generation_mode is not allowed"):
        build_ai_generation_mode_request(
            generation_request_id="GEN-BAD-MODE",
            context_package=_document_context_package(),
            output_family=URS_DOCUMENT_FAMILY,
            generation_mode=EVIDENCE_BOUND_REPORT_NARRATIVE_MODE,
            standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
        )


def test_generation_mode_request_rejects_output_family_misaligned_with_job_family() -> None:
    with pytest.raises(ValueError, match="output_family is not aligned"):
        build_ai_generation_mode_request(
            generation_request_id="GEN-BAD-FAMILY",
            context_package=_reporting_context_package(),
            output_family=REPORT_DOCUMENT_FAMILY,
            generation_mode=BOUNDED_REPORT_SUMMARY_MODE,
            standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
        )


def test_generation_mode_request_rejects_missing_standards_guardrail_ref() -> None:
    with pytest.raises(ValueError, match="standards_guardrail_ref must match"):
        build_ai_generation_mode_request(
            generation_request_id="GEN-MISSING-STANDARDS",
            context_package=_document_context_package(),
            output_family=URS_DOCUMENT_FAMILY,
            generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
            standards_guardrail_ref="STANDARDS-MISSING@v1",
        )


def test_generation_mode_request_rejects_partial_evidence_for_strong_mode() -> None:
    with pytest.raises(ValueError, match="all generation-eligible context evidence"):
        build_ai_generation_mode_request(
            generation_request_id="GEN-PARTIAL-STRONG",
            context_package=_document_context_package(dcf_status=PARTIAL_EVIDENCE_STATUS),
            output_family=URS_DOCUMENT_FAMILY,
            generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
            standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
        )


def test_generation_mode_request_rejects_raw_prompt_and_generated_text_fields() -> None:
    request = build_ai_generation_mode_request(
        generation_request_id="GEN-PROHIBITED",
        context_package=_document_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )

    request["raw_prompt"] = "draft this freely"
    with pytest.raises(ValueError, match="raw_prompt"):
        validate_ai_generation_mode_request(request)

    del request["raw_prompt"]
    request["generated_document_text"] = "generated output is not M16.3 scope"
    with pytest.raises(ValueError, match="generated_document_text"):
        validate_ai_generation_mode_request(request)


def test_generation_mode_request_rejects_output_acceptance_and_retry_scope() -> None:
    request = build_ai_generation_mode_request(
        generation_request_id="GEN-RETRY-SCOPE",
        context_package=_document_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )
    request["retry_or_fallback_in_scope"] = True

    with pytest.raises(ValueError, match="retry_or_fallback_in_scope"):
        validate_ai_generation_mode_request(request)
