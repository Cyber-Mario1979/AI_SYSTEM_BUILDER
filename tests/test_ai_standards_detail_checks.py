import copy

from asbp.ai_evaluation import (
    AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID,
    BOUNDED_INFERENCE_SECTION_UNLABELED_ASSUMPTION_FAILURE,
    DETAIL_CONSISTENCY_CHECK_FAIL,
    DISALLOWED_SECTION_FAILURE,
    DOCUMENT_FAMILY_MISMATCH_FAILURE,
    DUPLICATE_SECTION_ID_FAILURE,
    EVIDENCE_SUPPORTED_SECTION_MISSING_EVIDENCE_REFS_FAILURE,
    GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE,
    MISSING_REQUIRED_SECTION_FAILURE,
    PLACEHOLDER_SECTION_MISSING_EXPLICIT_PLACEHOLDER_FAILURE,
    PROHIBITED_LANGUAGE_PATTERN_FAILURE,
    SECTION_STANDARD_REF_UNDECLARED_FAILURE,
    STANDARDS_CONFORMANCE_CHECK_FAIL,
    STANDARDS_DETAIL_CHECK_FAIL,
    STANDARDS_DETAIL_CHECK_PASS,
    build_ai_standards_detail_check_result,
    build_ai_standards_detail_checks_baseline,
    validate_ai_standards_detail_check_result,
)
from asbp.document_engine import (
    BOUNDED_INFERENCE_CLASSIFICATION,
    EVIDENCE_SUPPORTED_CLASSIFICATION,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    PLACEHOLDER_ONLY_CLASSIFICATION,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    build_ai_authoring_request_payload,
    build_document_family_guardrail_policy,
    build_document_request_payload,
    build_guarded_authoring_output_payload,
    build_guarded_document_section,
)


def _urs_template_identity() -> dict[str, object]:
    return {
        "template_family": "urs",
        "template_id": "URS_BASE_v1",
        "template_version": "1.0.0",
        "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
    }


def _complete_urs_document_request() -> dict[str, object]:
    return build_document_request_payload(
        document_job_id="DOCJOB-M17-3-001",
        document_family="urs",
        document_id="URS-M17-3-001",
        template_identity=_urs_template_identity(),
        execution_context_kind="work_package",
        execution_context_ref="WP-M17-3-001",
        input_data={
            "system_name": "Tablet Press",
            "system_type": "process-equipment",
            "intended_use": "Compress tablets",
            "user_requirements": ["safe operation", "controlled compression force"],
        },
    )


def _strong_authoring_request() -> dict[str, object]:
    return build_ai_authoring_request_payload(
        document_request_payload=_complete_urs_document_request(),
        authoring_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_refs=["CQV_CORE@v1"],
        guardrails=["do_not_replace_execution_truth"],
        document_family_rules={
            "document_family": "urs",
            "allowed_sections": ["purpose", "scope", "requirements"],
            "placeholder_policy": "missing_evidence_uses_explicit_placeholders",
        },
    )


def _partial_authoring_request() -> dict[str, object]:
    request = _complete_urs_document_request()
    request["input_data"]["intended_use"] = {
        "status": "missing",
        "field_name": "intended_use",
        "policy": "missing_required_data_marked_explicitly",
    }
    return build_ai_authoring_request_payload(
        document_request_payload=request,
        authoring_mode=PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
        standards_refs=["CQV_CORE@v1"],
        guardrails=["label_assumptions"],
        document_family_rules={
            "document_family": "urs",
            "allowed_sections": ["purpose", "scope", "requirements"],
            "placeholder_policy": "missing_evidence_uses_explicit_placeholders",
        },
        allow_bounded_invention=True,
        bounded_invention_scope=["complete_missing_intended_use_as_labeled_assumption"],
    )


def _urs_policy() -> dict[str, object]:
    return build_document_family_guardrail_policy(
        document_family="urs",
        standards_refs=["CQV_CORE@v1", "GMP_ANNEX_15@v1"],
        allowed_sections=["purpose", "scope", "requirements"],
        required_sections=["purpose"],
    )


def _purpose_section() -> dict[str, object]:
    return build_guarded_document_section(
        section_id="purpose",
        section_title="Purpose",
        content="Define the intended CQV use of the governed URS artifact.",
        evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        evidence_refs=["DCF-001:system_name", "DCF-001:intended_use"],
    )


def _scope_section() -> dict[str, object]:
    return build_guarded_document_section(
        section_id="scope",
        section_title="Scope",
        content="Define the CQV scope using a labeled assumption.",
        evidence_classification=BOUNDED_INFERENCE_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        inference_refs=["DOCJOB-M17-3-001:missing:intended_use"],
        assumptions=["Assumption: Intended use remains GMP production support."],
    )


def _placeholder_section() -> dict[str, object]:
    return build_guarded_document_section(
        section_id="requirements",
        section_title="Requirements",
        content="Requirement details remain pending user confirmation.",
        evidence_classification=PLACEHOLDER_ONLY_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        placeholders=["(TBD) Requirement owner pending."],
    )


def _valid_guarded_output() -> dict[str, object]:
    return build_guarded_authoring_output_payload(
        authoring_request_payload=_strong_authoring_request(),
        document_family_guardrail_policy=_urs_policy(),
        sections=[_purpose_section()],
    )


def test_standards_detail_baseline_exposes_m17_3_rules() -> None:
    baseline = build_ai_standards_detail_checks_baseline()

    assert baseline["checkpoint"] == AI_STANDARDS_DETAIL_CHECKS_CHECKPOINT_ID
    assert "document_template_product_implementation" in baseline["not_owned_by_m17_3"]
    assert "retrieval_use_governance" in baseline["not_owned_by_m17_3"]


def test_valid_guarded_authoring_payload_passes_standards_detail_checks() -> None:
    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="STD-DETAIL-PASS",
        guarded_authoring_output_payload=_valid_guarded_output(),
    )

    assert result["standards_detail_check_result"] == STANDARDS_DETAIL_CHECK_PASS
    assert result["standards_detail_failure_reasons"] == []
    validate_ai_standards_detail_check_result(result)


def test_undeclared_section_standard_ref_fails_standards_conformance() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    payload["sections"][0]["standards_refs"] = ["UNDECLARED_STANDARD@v1"]

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="STD-UNDECLARED",
        guarded_authoring_output_payload=payload,
    )

    assert result["standards_conformance_check_result"] == STANDARDS_CONFORMANCE_CHECK_FAIL
    assert SECTION_STANDARD_REF_UNDECLARED_FAILURE in result[
        "standards_detail_failure_reasons"
    ]


def test_prohibited_language_pattern_fails_standards_conformance() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    payload["sections"][0]["content"] = (
        "This URS is guaranteed compliant for all regulatory cases."
    )

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="STD-PROHIBITED-LANGUAGE",
        guarded_authoring_output_payload=payload,
    )

    assert PROHIBITED_LANGUAGE_PATTERN_FAILURE in result[
        "standards_detail_failure_reasons"
    ]


def test_missing_required_section_fails_detail_consistency() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    payload["document_family_guardrail_policy"]["document_family_structure_rules"][
        "required_sections"
    ] = ["purpose", "scope"]

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-MISSING-REQUIRED",
        guarded_authoring_output_payload=payload,
    )

    assert result["detail_consistency_check_result"] == DETAIL_CONSISTENCY_CHECK_FAIL
    assert MISSING_REQUIRED_SECTION_FAILURE in result["standards_detail_failure_reasons"]


def test_disallowed_section_fails_detail_consistency() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    disallowed = copy.deepcopy(_purpose_section())
    disallowed["section_id"] = "approval"
    disallowed["section_title"] = "Approval"
    payload["sections"].append(disallowed)

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-DISALLOWED",
        guarded_authoring_output_payload=payload,
    )

    assert DISALLOWED_SECTION_FAILURE in result["standards_detail_failure_reasons"]


def test_duplicate_section_id_fails_detail_consistency() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    payload["sections"].append(copy.deepcopy(payload["sections"][0]))

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-DUPLICATE",
        guarded_authoring_output_payload=payload,
    )

    assert DUPLICATE_SECTION_ID_FAILURE in result["standards_detail_failure_reasons"]


def test_evidence_supported_section_without_evidence_refs_fails_detail_consistency() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    payload["sections"][0]["evidence_refs"] = []

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-NO-EVIDENCE",
        guarded_authoring_output_payload=payload,
    )

    assert EVIDENCE_SUPPORTED_SECTION_MISSING_EVIDENCE_REFS_FAILURE in result[
        "standards_detail_failure_reasons"
    ]


def test_bounded_inference_without_labeled_assumption_fails_detail_consistency() -> None:
    payload = build_guarded_authoring_output_payload(
        authoring_request_payload=_partial_authoring_request(),
        document_family_guardrail_policy=_urs_policy(),
        sections=[_purpose_section(), _scope_section()],
    )
    payload["sections"][1]["assumptions"] = [
        "Intended use remains GMP production support."
    ]

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-UNLABELED-ASSUMPTION",
        guarded_authoring_output_payload=payload,
    )

    assert BOUNDED_INFERENCE_SECTION_UNLABELED_ASSUMPTION_FAILURE in result[
        "standards_detail_failure_reasons"
    ]


def test_placeholder_without_explicit_marker_fails_detail_consistency() -> None:
    payload = build_guarded_authoring_output_payload(
        authoring_request_payload=_partial_authoring_request(),
        document_family_guardrail_policy=_urs_policy(),
        sections=[_purpose_section(), _placeholder_section()],
    )
    payload["sections"][1]["placeholders"] = ["Requirement owner pending."]

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-BAD-PLACEHOLDER",
        guarded_authoring_output_payload=payload,
    )

    assert PLACEHOLDER_SECTION_MISSING_EXPLICIT_PLACEHOLDER_FAILURE in result[
        "standards_detail_failure_reasons"
    ]


def test_document_family_mismatch_fails_standards_and_detail_checks() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    payload["document_family_guardrail_policy"]["document_family"] = "report"

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-FAMILY-MISMATCH",
        guarded_authoring_output_payload=payload,
    )

    assert DOCUMENT_FAMILY_MISMATCH_FAILURE in result[
        "standards_detail_failure_reasons"
    ]


def test_invalid_guarded_payload_failure_is_preserved() -> None:
    payload = copy.deepcopy(_valid_guarded_output())
    payload["approved_document_state"] = "approved"

    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="DETAIL-INVALID-PAYLOAD",
        guarded_authoring_output_payload=payload,
    )

    assert result["standards_detail_check_result"] == STANDARDS_DETAIL_CHECK_FAIL
    assert GUARDED_AUTHORING_PAYLOAD_INVALID_FAILURE in result[
        "standards_detail_failure_reasons"
    ]


def test_standards_detail_result_does_not_call_llm_mutate_state_or_reopen_templates() -> None:
    result = build_ai_standards_detail_check_result(
        standards_detail_check_result_id="STD-DETAIL-NO-DRIFT",
        guarded_authoring_output_payload=_valid_guarded_output(),
    )

    assert result["actual_llm_call_required"] is False
    assert result["prompt_template_required"] is False
    assert result["state_mutation_allowed"] is False
    assert result["approval_or_release_allowed"] is False
    assert result["document_template_implementation_in_scope"] is False
    assert result["retrieval_use_governance_in_scope"] is False
    assert result["standards_detail_check_result"] == STANDARDS_DETAIL_CHECK_PASS
