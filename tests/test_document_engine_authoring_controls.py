import pytest

from asbp.document_engine import (
    AI_AUTHORING_LAYER_ROLE,
    AUTHORING_CONTROL_CHECKPOINT_ID,
    AUTHORING_CONTROL_CONTRACT_VERSION,
    BOUNDED_INVENTION_POLICY,
    GENERATED_OUTPUT_TRUTH_BOUNDARY,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE,
    PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    UNRESTRICTED_FREE_DRAFTING_POLICY,
    build_ai_authoring_control_baseline,
    build_ai_authoring_request_payload,
    build_authoring_mode_policy,
    validate_ai_authoring_request_payload,
)


def _urs_template_identity() -> dict[str, object]:
    return {
        "template_family": "urs",
        "template_id": "URS_BASE_v1",
        "template_version": "1.0.0",
        "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
    }


def _complete_urs_document_request() -> dict[str, object]:
    from asbp.document_engine import build_document_request_payload

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
            "user_requirements": [
                "safe operation",
                "controlled compression force",
            ],
        },
    )


def _partial_urs_document_request() -> dict[str, object]:
    request = _complete_urs_document_request()
    request["input_data"]["intended_use"] = {
        "status": "missing",
        "field_name": "intended_use",
        "policy": "missing_required_data_marked_explicitly",
    }
    return request


def _document_family_rules() -> dict[str, object]:
    return {
        "document_family": "urs",
        "allowed_sections": [
            "purpose",
            "scope",
            "requirements",
            "assumptions",
        ],
        "placeholder_policy": "missing_evidence_uses_explicit_placeholders",
    }


def test_build_ai_authoring_control_baseline_exposes_m12_4_rules() -> None:
    baseline = build_ai_authoring_control_baseline()

    assert baseline["checkpoint"] == AUTHORING_CONTROL_CHECKPOINT_ID
    assert baseline["contract_version"] == AUTHORING_CONTROL_CONTRACT_VERSION
    assert baseline["authoring_layer_role"] == AI_AUTHORING_LAYER_ROLE
    assert STRONG_STRUCTURED_INPUT_FILL_MODE in baseline["supported_authoring_modes"]
    assert PARTIAL_INPUT_BOUNDED_COMPLETION_MODE in baseline[
        "supported_authoring_modes"
    ]
    assert MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE in baseline[
        "supported_authoring_modes"
    ]
    assert baseline["bounded_invention_policy"] == BOUNDED_INVENTION_POLICY
    assert baseline["unrestricted_free_drafting_policy"] == (
        UNRESTRICTED_FREE_DRAFTING_POLICY
    )


def test_build_authoring_mode_policy_distinguishes_strong_input_from_bounded_modes() -> None:
    strong_policy = build_authoring_mode_policy(STRONG_STRUCTURED_INPUT_FILL_MODE)
    partial_policy = build_authoring_mode_policy(
        PARTIAL_INPUT_BOUNDED_COMPLETION_MODE
    )

    assert strong_policy["requires_complete_structured_input"] is True
    assert strong_policy["bounded_invention_required"] is False
    assert partial_policy["requires_complete_structured_input"] is False
    assert partial_policy["bounded_invention_required"] is True


def test_build_ai_authoring_request_payload_accepts_strong_structured_input_fill() -> None:
    payload = build_ai_authoring_request_payload(
        document_request_payload=_complete_urs_document_request(),
        authoring_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_refs=["CQV_CORE@v1"],
        guardrails=["do_not_replace_execution_truth"],
        document_family_rules=_document_family_rules(),
    )

    assert payload["checkpoint"] == AUTHORING_CONTROL_CHECKPOINT_ID
    assert payload["authoring_mode"] == STRONG_STRUCTURED_INPUT_FILL_MODE
    assert payload["bounded_invention"]["allowed"] is False
    assert payload["input_completeness"]["has_missing_input"] is False
    assert payload["truth_separation"]["generated_output_boundary"] == (
        GENERATED_OUTPUT_TRUTH_BOUNDARY
    )


def test_strong_structured_input_fill_rejects_missing_input_markers() -> None:
    with pytest.raises(ValueError, match="requires complete structured input"):
        build_ai_authoring_request_payload(
            document_request_payload=_partial_urs_document_request(),
            authoring_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
            standards_refs=["CQV_CORE@v1"],
            guardrails=["do_not_replace_execution_truth"],
            document_family_rules=_document_family_rules(),
        )


def test_partial_input_bounded_completion_requires_bounded_controls() -> None:
    with pytest.raises(ValueError, match="requires bounded invention controls"):
        build_ai_authoring_request_payload(
            document_request_payload=_partial_urs_document_request(),
            authoring_mode=PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
            standards_refs=["CQV_CORE@v1"],
            guardrails=["do_not_replace_execution_truth"],
            document_family_rules=_document_family_rules(),
        )


def test_partial_input_bounded_completion_accepts_bounded_scope() -> None:
    payload = build_ai_authoring_request_payload(
        document_request_payload=_partial_urs_document_request(),
        authoring_mode=PARTIAL_INPUT_BOUNDED_COMPLETION_MODE,
        standards_refs=["CQV_CORE@v1"],
        guardrails=[
            "label_assumptions",
            "do_not_replace_execution_truth",
        ],
        document_family_rules=_document_family_rules(),
        allow_bounded_invention=True,
        bounded_invention_scope=[
            "complete_missing_intended_use_as_labeled_assumption",
        ],
    )

    assert payload["bounded_invention"]["allowed"] is True
    assert payload["input_completeness"]["missing_input_fields"] == [
        "intended_use"
    ]


def test_minimal_scaffold_generation_requires_bounded_scope() -> None:
    payload = build_ai_authoring_request_payload(
        document_request_payload=_partial_urs_document_request(),
        authoring_mode=MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE,
        standards_refs=["CQV_CORE@v1"],
        guardrails=["placeholders_for_missing_evidence"],
        document_family_rules=_document_family_rules(),
        allow_bounded_invention=True,
        bounded_invention_scope=["generate_allowed_sections_as_scaffold_only"],
    )

    assert payload["authoring_mode"] == MINIMAL_INPUT_SCAFFOLD_GENERATION_MODE
    assert payload["bounded_invention"]["scope"] == [
        "generate_allowed_sections_as_scaffold_only"
    ]


def test_ai_authoring_payload_rejects_unrestricted_free_prompt_field() -> None:
    payload = build_ai_authoring_request_payload(
        document_request_payload=_complete_urs_document_request(),
        authoring_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_refs=["CQV_CORE@v1"],
        guardrails=["do_not_replace_execution_truth"],
        document_family_rules=_document_family_rules(),
    )
    payload["freeform_prompt"] = "Write anything you want."

    with pytest.raises(ValueError, match="freeform_prompt is not allowed"):
        validate_ai_authoring_request_payload(payload)


def test_ai_authoring_payload_rejects_document_family_rule_mismatch() -> None:
    rules = _document_family_rules()
    rules["document_family"] = "report"

    with pytest.raises(ValueError, match="document_family_rules.document_family"):
        build_ai_authoring_request_payload(
            document_request_payload=_complete_urs_document_request(),
            authoring_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
            standards_refs=["CQV_CORE@v1"],
            guardrails=["do_not_replace_execution_truth"],
            document_family_rules=rules,
        )
