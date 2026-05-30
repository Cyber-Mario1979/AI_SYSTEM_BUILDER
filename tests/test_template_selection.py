import pytest

from asbp.document_template_store import load_default_document_template_library
from asbp.template_selection import load_template_for_request, select_template_for_request
from asbp.template_selection_model import TemplateSelectionInputModel


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_generate_documents",
        "does_not_validate_document_input_schemas",
        "does_not_render_or_export_documents",
        "does_not_use_ai_to_choose_templates",
    ]


def _qp_request(**overrides) -> TemplateSelectionInputModel:
    payload = {
        "selection_id": "TPLSEL-QUALIFICATION-PLAN@v1",
        "status": "deterministic_template_selection_request",
        "document_family_id": "DOCF-PLAN-STRATEGY",
        "document_type": "Qualification Plan",
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
    payload.update(overrides)
    return TemplateSelectionInputModel(**payload)


def _csv_request(**overrides) -> TemplateSelectionInputModel:
    payload = {
        "selection_id": "TPLSEL-CSV-VALIDATION-PLAN@v1",
        "status": "deterministic_template_selection_request",
        "document_family_id": "DOCF-PLAN-STRATEGY",
        "document_type": "CSV Validation Plan",
        "selector_context_ref": "SEL-PF-COMPUTERIZED-SYSTEMS-INT-CSV",
        "profile_refs": ["PROF-COMPUTERIZED-SYSTEM-BASELINE@v1"],
        "standards_bundle_refs": ["SB-CSV-GXP@v1"],
        "task_document_mapping_refs": ["MAP-STD-CSV-GXP-TO-CSV-TEMPLATE@v1"],
        "intake_route_ref": "ROUTE-DCF",
        "selection_controls": [
            "Template selection must use deterministic source records only."
        ],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }
    payload.update(overrides)
    return TemplateSelectionInputModel(**payload)


def test_selects_qualification_plan_template_deterministically():
    result = select_template_for_request(_qp_request())

    assert result.status == "selected"
    assert result.selected_template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert result.source_mapping_ids == ["MAP-STD-CQV-GMP-TO-QP-TEMPLATE@v1"]


def test_loads_selected_qualification_plan_template_record():
    template = load_template_for_request(_qp_request())

    assert template.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert template.document_type == "Qualification Plan"
    assert "SB-CQV-GMP@v1" in template.standards_bundle_refs


def test_selects_csv_validation_plan_template_deterministically():
    result = select_template_for_request(_csv_request())

    assert result.status == "selected"
    assert result.selected_template_id == "TPL-FUTURE-CSV-VALIDATION-PLAN@v1"
    assert result.source_mapping_ids == ["MAP-STD-CSV-GXP-TO-CSV-TEMPLATE@v1"]


def test_selection_returns_no_match_for_unknown_document_type():
    result = select_template_for_request(
        _qp_request(
            selection_id="TPLSEL-OQ-PROTOCOL@v1",
            document_type="OQ Protocol",
        )
    )

    assert result.status == "no_match"
    assert result.selected_template_id is None
    assert any(
        rejection.reason_code == "document_type_mismatch"
        for rejection in result.rejected_candidates
    )


def test_selection_returns_no_match_for_unsupported_standards_bundle():
    result = select_template_for_request(
        _qp_request(
            standards_bundle_refs=["SB-UNSUPPORTED@v1"],
            task_document_mapping_refs=[],
        )
    )

    assert result.status == "no_match"
    assert result.selected_template_id is None
    assert any(
        rejection.reason_code == "standards_bundle_mismatch"
        for rejection in result.rejected_candidates
    )


def test_selection_returns_no_match_for_unsupported_template_intake_route():
    library = load_default_document_template_library()
    library.template_records[0].intake_route_refs = ["ROUTE-DCF"]

    result = select_template_for_request(
        _qp_request(intake_route_ref="ROUTE-SKIP-DCF"),
        template_library=library,
    )

    assert result.status == "no_match"
    assert any(
        rejection.reason_code == "intake_route_mismatch"
        for rejection in result.rejected_candidates
    )


def test_selection_rejects_inactive_template_record():
    library = load_default_document_template_library()
    library.template_records[0].lifecycle_status = "retired"

    result = select_template_for_request(_qp_request(), template_library=library)

    assert result.status == "no_match"
    assert any(
        rejection.reason_code == "inactive_lifecycle_status"
        for rejection in result.rejected_candidates
    )


def test_selection_returns_ambiguous_when_multiple_records_match_without_standard_filter():
    library = load_default_document_template_library()
    alternate = library.template_records[0].model_copy(deep=True)
    alternate.template_id = "TPL-ALT-QUALIFICATION-PLAN@v1"
    alternate.source_location = (
        "data/source/document_templates/starter_document_templates.json::"
        "TPL-ALT-QUALIFICATION-PLAN@v1"
    )
    library.template_records.append(alternate)

    result = select_template_for_request(
        _qp_request(standards_bundle_refs=[], task_document_mapping_refs=[]),
        template_library=library,
    )

    assert result.status == "ambiguous"
    assert sorted(result.candidate_template_ids) == [
        "TPL-ALT-QUALIFICATION-PLAN@v1",
        "TPL-FUTURE-QUALIFICATION-PLAN@v1",
    ]


def test_load_template_raises_when_selection_is_not_unique():
    with pytest.raises(ValueError) as exc_info:
        load_template_for_request(
            _qp_request(
                selection_id="TPLSEL-MISSING-TEMPLATE@v1",
                document_type="Missing Template",
            )
        )

    assert "did not resolve to exactly one template" in str(exc_info.value)
