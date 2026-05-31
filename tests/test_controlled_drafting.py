import pytest

from asbp.controlled_drafting import (
    build_controlled_draft_packet_for_selection,
    build_controlled_draft_packet_for_template,
)
from asbp.template_selection import select_template_for_request
from asbp.template_selection_model import (
    REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS,
    TemplateSelectionInputModel,
)


def _selection_request() -> TemplateSelectionInputModel:
    return TemplateSelectionInputModel(
        selection_id="TPLSEL-QP-TEST@v1",
        document_family_id="DOCF-PLAN-STRATEGY",
        document_type="Qualification Plan",
        standards_bundle_refs=["SB-CQV-GMP@v1"],
        intake_route_ref="ROUTE-DCF",
        selection_controls=["Select qualification plan template deterministically."],
        explicit_non_implementation_claims=sorted(
            REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def _complete_qp_inputs() -> dict:
    return {
        "project_title": "Cleanroom HVAC Qualification",
        "cqv_scope": "End-to-end HVAC qualification for cleanroom baseline.",
        "system_or_area": "Cleanroom HVAC",
        "qualification_strategy": "IQ/OQ with controlled prerequisites and reports.",
        "standards_context": ["EU GMP Annex 15", "EU GMP Chapter 4"],
    }


def test_strong_input_fill_succeeds_with_required_fields():
    packet = build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QP-STRONG@v1",
        drafting_mode_id="DRAFTMODE-STRONG-INPUT-FILL@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values=_complete_qp_inputs(),
        intake_route_ref="ROUTE-DCF",
    )

    assert packet.drafting_mode == "strong_input_fill"
    assert packet.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert packet.schema_id == "SCHEMA-QUALIFICATION-PLAN@v1"
    assert packet.missing_required_field_ids == []
    assert packet.placeholders == []


def test_strong_input_fill_fails_with_missing_required_fields():
    inputs = _complete_qp_inputs()
    inputs.pop("qualification_strategy")

    with pytest.raises(ValueError) as exc_info:
        build_controlled_draft_packet_for_template(
            draft_id="DRAFT-QP-STRONG-MISSING@v1",
            drafting_mode_id="DRAFTMODE-STRONG-INPUT-FILL@v1",
            template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
            input_values=inputs,
            intake_route_ref="ROUTE-DCF",
        )

    assert "Strong input fill requires all required fields" in str(exc_info.value)
    assert "qualification_strategy" in str(exc_info.value)


def test_partial_bounded_completion_preserves_missing_limitations():
    inputs = {
        "project_title": "Cleanroom HVAC Qualification",
        "cqv_scope": "HVAC qualification scope.",
    }

    packet = build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QP-PARTIAL@v1",
        drafting_mode_id="DRAFTMODE-PARTIAL-BOUNDED-COMPLETION@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values=inputs,
        intake_route_ref="ROUTE-DCF",
    )

    assert packet.drafting_mode == "partial_bounded_completion"
    assert "system_or_area" in packet.missing_required_field_ids
    assert "qualification_strategy" in packet.missing_required_field_ids
    assert packet.placeholders
    assert any("Missing required field" in note for note in packet.limitation_statements)


def test_minimal_scaffold_produces_placeholders_only():
    packet = build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QP-SCAFFOLD@v1",
        drafting_mode_id="DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values={},
        intake_route_ref="ROUTE-SKIP-DCF",
    )

    assert packet.drafting_mode == "minimal_scaffold_with_placeholders"
    assert packet.placeholders
    assert all("placeholder" in section.draft_text.casefold() for section in packet.section_drafts)


def test_rationale_bound_section_drafting_includes_rationale_refs():
    packet = build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QP-RATIONALE@v1",
        drafting_mode_id="DRAFTMODE-RATIONALE-BOUND-SECTION-DRAFTING@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values=_complete_qp_inputs(),
        intake_route_ref="ROUTE-DCF",
    )

    assert packet.drafting_mode == "rationale_bound_section_drafting"
    assert any(section.rationale_refs for section in packet.section_drafts)


def test_selection_result_can_feed_controlled_drafting():
    selection = select_template_for_request(_selection_request())

    packet = build_controlled_draft_packet_for_selection(
        draft_id="DRAFT-QP-SELECTION@v1",
        drafting_mode_id="DRAFTMODE-STRONG-INPUT-FILL@v1",
        selection_result=selection,
        input_values=_complete_qp_inputs(),
        intake_route_ref="ROUTE-DCF",
    )

    assert packet.template_id == selection.selected_template_id
    assert packet.schema_id == "SCHEMA-QUALIFICATION-PLAN@v1"


def test_unrecognized_drafting_mode_is_rejected():
    with pytest.raises(ValueError) as exc_info:
        build_controlled_draft_packet_for_template(
            draft_id="DRAFT-QP-MISSING-MODE@v1",
            drafting_mode_id="DRAFTMODE-MISSING@v1",
            template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
            input_values=_complete_qp_inputs(),
            intake_route_ref="ROUTE-DCF",
        )

    assert "Controlled drafting mode source record not found" in str(exc_info.value)


def test_drafting_does_not_render_or_generate_product_ready_document():
    packet = build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QP-NONPRODUCT@v1",
        drafting_mode_id="DRAFTMODE-PARTIAL-BOUNDED-COMPLETION@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values={"project_title": "Only title"},
        intake_route_ref="ROUTE-DCF",
    )

    assert "does_not_create_product_ready_documents" in packet.explicit_non_implementation_claims
    assert "does_not_render_or_export_documents" in packet.explicit_non_implementation_claims
    assert not hasattr(packet, "rendered_file_path")
