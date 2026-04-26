import pytest

from asbp.document_engine import (
    ASSUMPTION_LABELING_POLICY,
    BOUNDED_INFERENCE_CLASSIFICATION,
    CONTROLLED_GMP_CQV_LANGUAGE_PROFILE,
    DETAIL_LEVEL_CONSISTENCY_POLICY,
    EVIDENCE_INFERENCE_SEPARATION_POLICY,
    EVIDENCE_SUPPORTED_CLASSIFICATION,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    PLACEHOLDER_ONLY_CLASSIFICATION,
    PLACEHOLDER_POLICY,
    STANDARDS_GUARDRAIL_CHECKPOINT_ID,
    STANDARDS_GUARDRAIL_CONTRACT_VERSION,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    build_ai_authoring_request_payload,
    build_document_family_guardrail_policy,
    build_document_request_payload,
    build_guarded_authoring_output_payload,
    build_guarded_document_section,
    build_standards_language_evidence_guardrail_baseline,
    validate_guarded_authoring_output_payload,
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
        document_job_id="DOCJOB-001",
        document_family="urs",
        document_id="URS-001",
        template_identity=_urs_template_identity(),
        execution_context_kind="work_package",
        execution_context_ref="WP-001",
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


def test_standards_language_evidence_baseline_exposes_m12_5_rules() -> None:
    baseline = build_standards_language_evidence_guardrail_baseline()

    assert baseline["checkpoint"] == STANDARDS_GUARDRAIL_CHECKPOINT_ID
    assert baseline["contract_version"] == STANDARDS_GUARDRAIL_CONTRACT_VERSION
    assert baseline["language_profile"] == CONTROLLED_GMP_CQV_LANGUAGE_PROFILE
    assert baseline["assumption_labeling_policy"] == ASSUMPTION_LABELING_POLICY
    assert baseline["placeholder_policy"] == PLACEHOLDER_POLICY
    assert baseline["evidence_inference_separation_policy"] == EVIDENCE_INFERENCE_SEPARATION_POLICY
    assert baseline["detail_level_consistency_policy"] == DETAIL_LEVEL_CONSISTENCY_POLICY


def test_document_family_guardrail_policy_defines_structure_standards_and_language_rules() -> None:
    policy = _urs_policy()

    assert policy["checkpoint"] == STANDARDS_GUARDRAIL_CHECKPOINT_ID
    assert policy["document_family"] == "urs"
    assert policy["standards_refs"] == ["CQV_CORE@v1", "GMP_ANNEX_15@v1"]
    assert policy["document_family_structure_rules"]["allowed_sections"] == [
        "purpose",
        "scope",
        "requirements",
    ]
    assert "purpose" in policy["section_level_authoring_constraints"]


def test_guarded_authoring_output_accepts_evidence_supported_section() -> None:
    section = build_guarded_document_section(
        section_id="purpose",
        section_title="Purpose",
        content="Define the intended CQV use of the governed URS artifact.",
        evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        evidence_refs=["DCF-001:system_name", "DCF-001:intended_use"],
    )

    payload = build_guarded_authoring_output_payload(
        authoring_request_payload=_strong_authoring_request(),
        document_family_guardrail_policy=_urs_policy(),
        sections=[section],
    )

    assert payload["checkpoint"] == STANDARDS_GUARDRAIL_CHECKPOINT_ID
    assert payload["sections"][0]["evidence_classification"] == EVIDENCE_SUPPORTED_CLASSIFICATION


def test_evidence_supported_section_requires_evidence_refs() -> None:
    with pytest.raises(ValueError, match="evidence_refs must be a non-empty"):
        build_guarded_document_section(
            section_id="purpose",
            section_title="Purpose",
            content="Define the intended CQV use of the governed URS artifact.",
            evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
            standards_refs=["CQV_CORE@v1"],
        )


def test_bounded_inference_section_requires_labeled_assumptions() -> None:
    with pytest.raises(ValueError, match="Assumptions must be explicitly labeled"):
        build_guarded_document_section(
            section_id="scope",
            section_title="Scope",
            content="The scope is inferred from partial user input.",
            evidence_classification=BOUNDED_INFERENCE_CLASSIFICATION,
            standards_refs=["CQV_CORE@v1"],
            inference_refs=["DOCJOB-001:missing:intended_use"],
            assumptions=["The equipment is used in routine GMP production."],
        )


def test_guarded_output_accepts_bounded_inference_with_labeled_assumption() -> None:
    section = build_guarded_document_section(
        section_id="purpose",
        section_title="Purpose",
        content="Define the intended CQV use with a labeled assumption.",
        evidence_classification=BOUNDED_INFERENCE_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        inference_refs=["DOCJOB-001:missing:intended_use"],
        assumptions=["Assumption: Intended use remains GMP production support."],
    )

    payload = build_guarded_authoring_output_payload(
        authoring_request_payload=_partial_authoring_request(),
        document_family_guardrail_policy=_urs_policy(),
        sections=[section],
    )

    assert payload["sections"][0]["assumptions"] == [
        "Assumption: Intended use remains GMP production support."
    ]


def test_placeholder_section_requires_explicit_placeholder_marker() -> None:
    with pytest.raises(ValueError, match="Placeholders must be explicitly labeled"):
        build_guarded_document_section(
            section_id="requirements",
            section_title="Requirements",
            content="Requirement details are pending.",
            evidence_classification=PLACEHOLDER_ONLY_CLASSIFICATION,
            standards_refs=["CQV_CORE@v1"],
            placeholders=["Requirement owner pending"],
        )


def test_guarded_output_rejects_section_outside_document_family_policy() -> None:
    section = build_guarded_document_section(
        section_id="approval",
        section_title="Approval",
        content="Approval state is outside generated language truth.",
        evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        evidence_refs=["DOCJOB-001:output-boundary"],
    )

    with pytest.raises(ValueError, match="not allowed by the document-family"):
        build_guarded_authoring_output_payload(
            authoring_request_payload=_strong_authoring_request(),
            document_family_guardrail_policy=_urs_policy(),
            sections=[section],
        )


def test_guarded_output_rejects_prohibited_language_patterns() -> None:
    section = build_guarded_document_section(
        section_id="purpose",
        section_title="Purpose",
        content="This URS is guaranteed compliant for all regulatory cases.",
        evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        evidence_refs=["DCF-001:system_name"],
    )

    with pytest.raises(ValueError, match="prohibited language pattern"):
        build_guarded_authoring_output_payload(
            authoring_request_payload=_strong_authoring_request(),
            document_family_guardrail_policy=_urs_policy(),
            sections=[section],
        )


def test_guarded_output_rejects_undeclared_section_standard_ref() -> None:
    section = build_guarded_document_section(
        section_id="purpose",
        section_title="Purpose",
        content="Define the intended CQV use of the governed URS artifact.",
        evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
        standards_refs=["UNDECLARED_STANDARD@v1"],
        evidence_refs=["DCF-001:system_name"],
    )

    with pytest.raises(ValueError, match="must be declared"):
        build_guarded_authoring_output_payload(
            authoring_request_payload=_strong_authoring_request(),
            document_family_guardrail_policy=_urs_policy(),
            sections=[section],
        )


def test_guarded_output_rejects_document_family_mismatch() -> None:
    section = build_guarded_document_section(
        section_id="purpose",
        section_title="Purpose",
        content="Define the intended CQV use of the governed URS artifact.",
        evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        evidence_refs=["DCF-001:system_name"],
    )
    policy = build_document_family_guardrail_policy(
        document_family="report",
        standards_refs=["CQV_CORE@v1"],
        allowed_sections=["purpose"],
        required_sections=["purpose"],
    )

    with pytest.raises(ValueError, match="document_family must match"):
        build_guarded_authoring_output_payload(
            authoring_request_payload=_strong_authoring_request(),
            document_family_guardrail_policy=policy,
            sections=[section],
        )


def test_validate_guarded_authoring_output_rejects_approval_state_field() -> None:
    section = build_guarded_document_section(
        section_id="purpose",
        section_title="Purpose",
        content="Define the intended CQV use of the governed URS artifact.",
        evidence_classification=EVIDENCE_SUPPORTED_CLASSIFICATION,
        standards_refs=["CQV_CORE@v1"],
        evidence_refs=["DCF-001:system_name"],
    )
    payload = build_guarded_authoring_output_payload(
        authoring_request_payload=_strong_authoring_request(),
        document_family_guardrail_policy=_urs_policy(),
        sections=[section],
    )
    payload["approved_document_state"] = "approved"

    with pytest.raises(ValueError, match="approved_document_state is not allowed"):
        validate_guarded_authoring_output_payload(payload)
