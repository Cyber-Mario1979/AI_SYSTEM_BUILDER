import pytest

from asbp.ai_runtime import (
    AI_CONTEXT_PACKAGING_CHECKPOINT_ID,
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    BOUNDED_SUMMARIZATION_PROFILE,
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    DCF_EXTRACTED_INPUT_SOURCE_FAMILY,
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    EXPORT_ENGINE_CALLER_BOUNDARY,
    EXPORT_REPORTING_REQUIREMENT_SOURCE_FAMILY,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_ENGINE_INPUT_ROLE,
    GOVERNED_REPORTING_JOB_FAMILY,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
    REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
    STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
    STRUCTURED_INPUT_PAYLOAD_CLASSIFICATION,
    SUPPORTING_CONTEXT_PAYLOAD_CLASSIFICATION,
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    VALIDATED_EVIDENCE_STATUS,
    build_ai_context_item,
    build_ai_context_package,
    build_ai_context_packaging_baseline,
    build_ai_runtime_entry_request,
    validate_ai_context_item,
    validate_ai_context_package,
)


def _document_runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-DOC-CTX-001",
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


def _document_context_items() -> list[dict[str, object]]:
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
            evidence_status=VALIDATED_EVIDENCE_STATUS,
            is_authoritative=True,
            may_be_used_for_generation=True,
        ),
    ]


def test_context_packaging_baseline_exposes_m16_2_rules() -> None:
    baseline = build_ai_context_packaging_baseline()

    assert baseline["checkpoint"] == AI_CONTEXT_PACKAGING_CHECKPOINT_ID
    assert TEMPLATE_RETRIEVAL_SOURCE_FAMILY in baseline["supported_context_source_families"]
    assert "prompt_templates" in baseline["not_owned_by_m16_2"]
    assert baseline["execution_truth_policy"] == (
        "ai_context_packages_must_never_define_execution_truth"
    )


def test_build_ai_context_item_accepts_governed_authoritative_item() -> None:
    item = build_ai_context_item(
        context_item_id="CTX-DCF",
        source_family=DCF_EXTRACTED_INPUT_SOURCE_FAMILY,
        source_ref="DCF-EXTRACTED-INPUT@v1",
        source_role=GOVERNED_ENGINE_INPUT_ROLE,
        payload_classification=STRUCTURED_INPUT_PAYLOAD_CLASSIFICATION,
        evidence_status=VALIDATED_EVIDENCE_STATUS,
        is_authoritative=True,
        may_be_used_for_generation=True,
    )

    assert item["source_ref"] == "DCF-EXTRACTED-INPUT@v1"
    validate_ai_context_item(item)


def test_build_ai_context_package_accepts_document_context_package() -> None:
    package = build_ai_context_package(
        context_package_id="CTXPKG-DOC-001",
        ai_runtime_entry_request=_document_runtime_request(),
        context_items=_document_context_items(),
    )

    assert package["checkpoint"] == AI_CONTEXT_PACKAGING_CHECKPOINT_ID
    assert package["context_package_status"] == "ai_context_package_validated"
    validate_ai_context_package(package)


def test_build_ai_context_package_accepts_reporting_context_package() -> None:
    runtime_request = build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-REPORT-CTX-001",
        job_family=GOVERNED_REPORTING_JOB_FAMILY,
        caller_boundary=EXPORT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile=BOUNDED_SUMMARIZATION_PROFILE,
        governed_source_refs=[
            "REPORTING-REQUIREMENT@v1",
            "STANDARDS-GUARDRAIL-CONTEXT@v1",
        ],
        engine_contract_refs=[
            "EXPORT-REQUEST-CONTRACT@v1",
            "REPORTING-SURFACE-CONTRACT@v1",
        ],
    )
    items = [
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
    ]

    package = build_ai_context_package(
        context_package_id="CTXPKG-REPORT-001",
        ai_runtime_entry_request=runtime_request,
        context_items=items,
    )

    assert package["job_family"] == GOVERNED_REPORTING_JOB_FAMILY
    validate_ai_context_package(package)


def test_context_item_rejects_unversioned_source_ref() -> None:
    with pytest.raises(ValueError, match="exactly one '@'"):
        build_ai_context_item(
            context_item_id="CTX-BAD-REF",
            source_family=TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
            source_ref="TEMPLATE-URS",
            source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
            payload_classification=REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
            evidence_status=VALIDATED_EVIDENCE_STATUS,
            is_authoritative=True,
            may_be_used_for_generation=True,
        )


def test_context_item_rejects_support_context_promoted_to_authority() -> None:
    with pytest.raises(ValueError, match="non-authoritative support context"):
        build_ai_context_item(
            context_item_id="CTX-SUPPORT",
            source_family=DCF_EXTRACTED_INPUT_SOURCE_FAMILY,
            source_ref="DCF-EXTRACTED-INPUT@v1",
            source_role=NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
            payload_classification=SUPPORTING_CONTEXT_PAYLOAD_CLASSIFICATION,
            evidence_status=VALIDATED_EVIDENCE_STATUS,
            is_authoritative=True,
            may_be_used_for_generation=True,
        )


def test_context_item_rejects_execution_truth_definition() -> None:
    with pytest.raises(ValueError, match="must not define execution truth"):
        build_ai_context_item(
            context_item_id="CTX-EXEC-TRUTH",
            source_family=DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
            source_ref="DOCUMENT-LIFECYCLE-STATE@v1",
            source_role=GOVERNED_ENGINE_INPUT_ROLE,
            payload_classification=STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
            evidence_status=VALIDATED_EVIDENCE_STATUS,
            is_authoritative=True,
            may_be_used_for_generation=True,
            may_define_execution_truth=True,
        )


def test_context_package_rejects_missing_required_context_family() -> None:
    with pytest.raises(ValueError, match="missing required context source families"):
        build_ai_context_package(
            context_package_id="CTXPKG-MISSING",
            ai_runtime_entry_request=_document_runtime_request(),
            context_items=_document_context_items()[:2],
        )


def test_context_package_rejects_item_not_declared_by_runtime_request() -> None:
    items = _document_context_items()
    items[0]["source_ref"] = "TEMPLATE-MISSING@v1"

    with pytest.raises(ValueError, match="not declared by the AI runtime entry request"):
        build_ai_context_package(
            context_package_id="CTXPKG-UNDECLARED",
            ai_runtime_entry_request=_document_runtime_request(),
            context_items=items,
        )


def test_context_package_rejects_prompt_template_or_raw_prompt_fields() -> None:
    package = build_ai_context_package(
        context_package_id="CTXPKG-PROMPT",
        ai_runtime_entry_request=_document_runtime_request(),
        context_items=_document_context_items(),
    )
    package["prompt_template"] = "summarize this"

    with pytest.raises(ValueError, match="prompt_template"):
        validate_ai_context_package(package)

    item = _document_context_items()[0]
    item["raw_prompt"] = "free text"

    with pytest.raises(ValueError, match="raw_prompt"):
        validate_ai_context_item(item)
