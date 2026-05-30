import pytest

from asbp.controlled_drafting import build_controlled_draft_packet_for_template
from asbp.standards_backed_output import (
    assert_no_product_ready_standards_output_claim,
    build_standards_backed_output_controls_for_draft,
)
from asbp.standards_backed_output_model import StandardsBackedOutputControlPacketModel


def _draft_packet():
    return build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QUALIFICATION-PLAN-CONTROLS@v1",
        drafting_mode_id="DRAFTMODE-PARTIAL-BOUNDED-COMPLETION@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values={
            "project_title": "Project Alpha",
            "cqv_scope": "Qualification plan for controlled system",
            "system_or_area": "Manufacturing suite",
        },
        intake_route_ref="ROUTE-SKIP-DCF",
    )


def test_build_standards_backed_output_controls_for_draft_qp_path():
    packet = build_standards_backed_output_controls_for_draft(
        control_packet_id="STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        draft_packet=_draft_packet(),
        standards_bundle_refs=["SB-CQV-GMP@v1"],
    )

    assert packet.status == "standards_backed_output_control_packet"
    assert packet.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert packet.standards_bundle_refs == ["SB-CQV-GMP@v1"]
    assert packet.output_warning_visibility == "visible"
    assert "does_not_implement_standards_retrieval_or_embedding" in (
        packet.explicit_non_implementation_claims
    )


def test_build_standards_backed_output_controls_downgrades_unverified_clause_depth():
    packet = build_standards_backed_output_controls_for_draft(
        control_packet_id="STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        draft_packet=_draft_packet(),
        standards_bundle_refs=["SB-CQV-GMP@v1"],
        requested_citation_depth="clause",
    )

    assert all(
        source.rendered_citation_depth == "document"
        for source in packet.source_controls
        if source.verification_status != "verified"
    )
    assert packet.output_warning_visibility == "visible"
    assert any("Requested citation depth" in item for item in packet.output_limitation_summary)


def test_unknown_standard_bundle_is_rejected():
    with pytest.raises(ValueError) as exc_info:
        build_standards_backed_output_controls_for_draft(
            control_packet_id="STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
            draft_packet=_draft_packet(),
            standards_bundle_refs=["SB-MISSING@v1"],
        )

    assert "Standards bundle binding not found" in str(exc_info.value)


def test_product_ready_output_claim_is_rejected_by_guard():
    packet = build_standards_backed_output_controls_for_draft(
        control_packet_id="STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        draft_packet=_draft_packet(),
        standards_bundle_refs=["SB-CQV-GMP@v1"],
    )
    payload = packet.model_dump()
    payload["reviewer_attention_points"].append("This is product ready.")
    unsafe_packet = StandardsBackedOutputControlPacketModel(**payload)

    with pytest.raises(ValueError) as exc_info:
        assert_no_product_ready_standards_output_claim(unsafe_packet)

    assert "must not claim product-ready" in str(exc_info.value)
