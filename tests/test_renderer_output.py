import pytest

from asbp.controlled_drafting import build_controlled_draft_packet_for_template
from asbp.renderer_output import render_output_artifact
from asbp.standards_backed_output import build_standards_backed_output_controls_for_draft
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


def _draft_packet_with_placeholders():
    return build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QUALIFICATION-PLAN-PLACEHOLDERS@v1",
        drafting_mode_id="DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values={
            "project_title": "Project Alpha",
            "cqv_scope": "Qualification plan for controlled system",
            "system_or_area": "Manufacturing suite",
        },
        intake_route_ref="ROUTE-SKIP-DCF",
    )


def _standards_packet(draft_packet=None):
    draft_packet = draft_packet or _draft_packet()
    return build_standards_backed_output_controls_for_draft(
        control_packet_id="STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        draft_packet=draft_packet,
        standards_bundle_refs=["SB-CQV-GMP@v1"],
    )


def test_markdown_renderer_preserves_metadata_and_visible_controls():
    draft_packet = _draft_packet_with_placeholders()
    artifact = render_output_artifact(
        artifact_id="ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        output_format="markdown",
        draft_packet=draft_packet,
        standards_packet=_standards_packet(draft_packet),
    )

    assert artifact.output_format == "markdown"
    assert artifact.media_type == "text/markdown"
    assert artifact.artifact_filename.endswith(".md")
    assert artifact.metadata.placeholder_present is True
    assert artifact.metadata.limitation_present is True
    assert artifact.metadata.standards_warning_present is True
    assert artifact.metadata.non_product_ready is True
    assert "NON-PRODUCT-READY CONTROLLED RENDER" in artifact.rendered_content
    assert "Project Alpha" in artifact.rendered_content
    assert "Standards Warning" in artifact.rendered_content
    assert "Visible Limitations" in artifact.rendered_content
    assert "Visible Placeholders" in artifact.rendered_content


def test_csv_summary_renderer_preserves_artifact_metadata():
    artifact = render_output_artifact(
        artifact_id="ART-QUALIFICATION-PLAN-CSV-SUMMARY@v1",
        output_format="csv_summary",
        draft_packet=_draft_packet(),
        standards_packet=_standards_packet(),
    )

    assert artifact.output_format == "csv_summary"
    assert artifact.media_type == "text/csv"
    assert artifact.artifact_filename.endswith(".csv")
    assert "artifact_id" in artifact.rendered_content
    assert "ART-QUALIFICATION-PLAN-CSV-SUMMARY@v1" in artifact.rendered_content
    assert "non_product_ready,True" in artifact.rendered_content


def test_renderer_rejects_unsupported_docx_until_implemented():
    with pytest.raises(ValueError) as exc_info:
        render_output_artifact(
            artifact_id="ART-QUALIFICATION-PLAN-DOCX@v1",
            output_format="docx",
            draft_packet=_draft_packet(),
            standards_packet=_standards_packet(),
        )

    assert "Unsupported renderer output format" in str(exc_info.value)


def test_renderer_rejects_mismatched_standards_packet():
    standards_packet_payload = _standards_packet().model_dump()
    standards_packet_payload["draft_id"] = "DRAFT-OTHER-CONTROLLED-PACKET@v1"
    mismatched_packet = StandardsBackedOutputControlPacketModel(
        **standards_packet_payload
    )

    with pytest.raises(ValueError) as exc_info:
        render_output_artifact(
            artifact_id="ART-QUALIFICATION-PLAN-MARKDOWN@v1",
            output_format="markdown",
            draft_packet=_draft_packet(),
            standards_packet=mismatched_packet,
        )

    assert "draft_id does not match" in str(exc_info.value)


def test_renderer_does_not_claim_lifecycle_or_approval_state():
    artifact = render_output_artifact(
        artifact_id="ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        output_format="markdown",
        draft_packet=_draft_packet(),
        standards_packet=_standards_packet(),
    )

    assert artifact.metadata.lifecycle_state_mutated is False
    assert artifact.metadata.approval_claimed is False
    assert "does_not_mutate_lifecycle_or_review_state" in (
        artifact.explicit_non_implementation_claims
    )
