import pytest
from pydantic import ValidationError

from asbp.template_selection_model import (
    TemplateSelectionInputModel,
    TemplateSelectionResultModel,
)


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_generate_documents",
        "does_not_validate_document_input_schemas",
        "does_not_render_or_export_documents",
        "does_not_use_ai_to_choose_templates",
    ]


def _minimal_selection_payload() -> dict:
    return {
        "selection_id": "TPLSEL-QUALIFICATION-PLAN@v1",
        "status": "deterministic_template_selection_request",
        "document_family_id": "DOCF-PLAN-STRATEGY",
        "document_type": "Qualification Plan",
        "template_intent": "Qualification strategy planning",
        "selector_context_ref": "SEL-PF-PROCESS-EQUIPMENT-INT-E2E-QUALIFICATION",
        "profile_refs": ["PROF-PROCESS-EQUIPMENT-GMP-BASELINE@v1"],
        "standards_bundle_refs": ["SB-CQV-GMP@v1"],
        "task_document_mapping_refs": ["MAP-STD-CQV-GMP-TO-QP-TEMPLATE@v1"],
        "intake_route_ref": "ROUTE-DCF",
        "selection_controls": [
            "Template selection must use deterministic source records only."
        ],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def test_template_selection_input_accepts_controlled_minimum():
    request = TemplateSelectionInputModel(**_minimal_selection_payload())

    assert request.selection_id == "TPLSEL-QUALIFICATION-PLAN@v1"
    assert request.document_family_id == "DOCF-PLAN-STRATEGY"
    assert request.standards_bundle_refs == ["SB-CQV-GMP@v1"]


def test_template_selection_input_rejects_unsupported_intake_route():
    payload = _minimal_selection_payload()
    payload["intake_route_ref"] = "ROUTE-UNCONTROLLED"

    with pytest.raises(ValidationError) as exc_info:
        TemplateSelectionInputModel(**payload)

    assert "Input should be" in str(exc_info.value)


def test_template_selection_input_rejects_invalid_standard_bundle_ref():
    payload = _minimal_selection_payload()
    payload["standards_bundle_refs"] = ["STD-CQV-GMP"]

    with pytest.raises(ValidationError) as exc_info:
        TemplateSelectionInputModel(**payload)

    assert "standards_bundle_refs must use SB-...@v..." in str(exc_info.value)


def test_template_selection_input_requires_explicit_non_implementation_claims():
    payload = _minimal_selection_payload()
    payload["explicit_non_implementation_claims"] = ["does_not_generate_documents"]

    with pytest.raises(ValidationError) as exc_info:
        TemplateSelectionInputModel(**payload)

    assert "M29.3 template selection request is missing explicit" in str(exc_info.value)


def test_template_selection_result_requires_selected_template_for_selected_status():
    with pytest.raises(ValidationError) as exc_info:
        TemplateSelectionResultModel(
            selection_id="TPLSEL-QUALIFICATION-PLAN@v1",
            status="selected",
            candidate_template_ids=["TPL-FUTURE-QUALIFICATION-PLAN@v1"],
            decision_reason="Selected deterministically.",
            explicit_non_implementation_claims=_required_non_implementation_claims(),
        )

    assert "requires selected_template_id" in str(exc_info.value)


def test_template_selection_result_rejects_selected_template_for_no_match_status():
    with pytest.raises(ValidationError) as exc_info:
        TemplateSelectionResultModel(
            selection_id="TPLSEL-QUALIFICATION-PLAN@v1",
            status="no_match",
            selected_template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
            candidate_template_ids=[],
            decision_reason="No match.",
            explicit_non_implementation_claims=_required_non_implementation_claims(),
        )

    assert "cannot include selected_template_id" in str(exc_info.value)


def test_persisted_state_payload_is_not_template_selection_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValidationError):
        TemplateSelectionInputModel(**persisted_state_payload)
