import pytest

from asbp.controlled_drafting import build_controlled_draft_packet_for_template
from asbp.document_lifecycle import (
    assert_generated_prose_cannot_mutate_lifecycle_truth,
    create_document_lifecycle_record_from_artifact,
    supersede_document_lifecycle_record,
    transition_document_lifecycle_record,
)
from asbp.renderer_output import render_output_artifact
from asbp.standards_backed_output import build_standards_backed_output_controls_for_draft


def _draft_packet():
    return build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QUALIFICATION-PLAN-CONTROLS@v1",
        drafting_mode_id="DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values={
            "project_title": "Project Alpha",
            "cqv_scope": "Qualification plan for controlled system",
            "system_or_area": "Manufacturing suite",
        },
        intake_route_ref="ROUTE-SKIP-DCF",
    )


def _artifact():
    draft_packet = _draft_packet()
    standards_packet = build_standards_backed_output_controls_for_draft(
        control_packet_id="STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        draft_packet=draft_packet,
        standards_bundle_refs=["SB-CQV-GMP@v1"],
    )
    return render_output_artifact(
        artifact_id="ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        output_format="markdown",
        draft_packet=draft_packet,
        standards_packet=standards_packet,
    )


def _lifecycle_record():
    return create_document_lifecycle_record_from_artifact(
        lifecycle_record_id="LIFECYCLE-QUALIFICATION-PLAN@v1",
        artifact=_artifact(),
    )


def test_lifecycle_record_is_created_from_renderer_metadata():
    record = _lifecycle_record()

    assert record.lifecycle_state == "draft"
    assert record.source_artifact_id == "ART-QUALIFICATION-PLAN-MARKDOWN@v1"
    assert record.source_draft_id == "DRAFT-QUALIFICATION-PLAN-CONTROLS@v1"
    assert record.placeholder_present is True
    assert record.limitation_present is True
    assert record.standards_warning_present is True
    assert any("placeholders" in item for item in record.carried_forward_limitations)


def test_draft_to_review_transition_succeeds():
    record = _lifecycle_record()

    transitioned = transition_document_lifecycle_record(record, "in_review")

    assert transitioned.lifecycle_state == "in_review"
    assert transitioned.transition_history[-1].from_state == "draft"
    assert transitioned.transition_history[-1].to_state == "in_review"


def test_review_to_approved_ready_requires_review_obligations_resolved():
    record = transition_document_lifecycle_record(_lifecycle_record(), "in_review")

    with pytest.raises(ValueError) as exc_info:
        transition_document_lifecycle_record(record, "approved_ready")

    assert "requires resolved review obligations" in str(exc_info.value)

    transitioned = transition_document_lifecycle_record(
        record,
        "approved_ready",
        resolved_review_obligation_ids={
            "OBL-TECHNICAL-REVIEW@v1",
            "OBL-QUALITY-REVIEW@v1",
        },
    )
    assert transitioned.lifecycle_state == "approved_ready"


def test_final_ready_requires_approval_and_task_closure_dependencies_resolved():
    record = transition_document_lifecycle_record(_lifecycle_record(), "in_review")
    approved_ready = transition_document_lifecycle_record(
        record,
        "approved_ready",
        resolved_review_obligation_ids={
            "OBL-TECHNICAL-REVIEW@v1",
            "OBL-QUALITY-REVIEW@v1",
        },
    )

    with pytest.raises(ValueError) as exc_info:
        transition_document_lifecycle_record(approved_ready, "final_ready")

    assert "requires resolved approval obligations" in str(exc_info.value)

    final_ready = transition_document_lifecycle_record(
        approved_ready,
        "final_ready",
        resolved_approval_obligation_ids={"OBL-APPROVAL-READINESS@v1"},
        resolved_task_closure_dependency_ids={"OBL-TASK-CLOSURE-DEPENDENCIES@v1"},
    )
    assert final_ready.lifecycle_state == "final_ready"


def test_invalid_transition_is_rejected():
    with pytest.raises(ValueError) as exc_info:
        transition_document_lifecycle_record(_lifecycle_record(), "final_ready")

    assert "transition is not allowed" in str(exc_info.value)


def test_supersede_lifecycle_record_requires_replacement_reference():
    record = _lifecycle_record()

    superseded = supersede_document_lifecycle_record(
        record,
        superseded_by_record_id="LIFECYCLE-QUALIFICATION-PLAN-REVISION@v1",
    )

    assert superseded.lifecycle_state == "superseded"
    assert superseded.superseded_by_record_id == "LIFECYCLE-QUALIFICATION-PLAN-REVISION@v1"


def test_generated_prose_cannot_mutate_lifecycle_truth():
    record = _lifecycle_record()

    with pytest.raises(ValueError) as exc_info:
        assert_generated_prose_cannot_mutate_lifecycle_truth(
            record,
            requested_state_from_generated_content="approved_ready",
        )

    assert "Generated prose cannot mutate" in str(exc_info.value)
