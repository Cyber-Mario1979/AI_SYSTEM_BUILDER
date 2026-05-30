import pytest

from asbp.controlled_drafting import build_controlled_draft_packet_for_template
from asbp.document_lifecycle import (
    create_document_lifecycle_record_from_artifact,
    supersede_document_lifecycle_record,
)
from asbp.document_lifecycle_model import DocumentLifecycleRecordModel
from asbp.output_validation import (
    assert_output_validation_passes,
    validate_output_artifact,
)
from asbp.renderer_output import render_output_artifact
from asbp.renderer_output_model import RendererOutputArtifactModel
from asbp.standards_backed_output import build_standards_backed_output_controls_for_draft


def _draft_packet():
    return build_controlled_draft_packet_for_template(
        draft_id="DRAFT-QUALIFICATION-PLAN-OUTPUT-VALIDATION@v1",
        drafting_mode_id="DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        input_values={
            "project_title": "Project Alpha",
            "cqv_scope": "Qualification plan for controlled system",
        },
        intake_route_ref="ROUTE-SKIP-DCF",
    )


def _artifact_and_lifecycle(output_format: str = "markdown"):
    draft_packet = _draft_packet()
    standards_packet = build_standards_backed_output_controls_for_draft(
        control_packet_id="STDOUT-QUALIFICATION-PLAN-OUTPUT-VALIDATION@v1",
        draft_packet=draft_packet,
        standards_bundle_refs=["SB-CQV-GMP@v1"],
    )
    artifact = render_output_artifact(
        artifact_id=f"ART-QUALIFICATION-PLAN-{output_format.upper().replace('_', '-')}@v1",
        output_format=output_format,  # type: ignore[arg-type]
        draft_packet=draft_packet,
        standards_packet=standards_packet,
    )
    lifecycle_record = create_document_lifecycle_record_from_artifact(
        lifecycle_record_id=f"LIFECYCLE-QUALIFICATION-PLAN-{output_format.upper().replace('_', '-')}@v1",
        artifact=artifact,
    )
    return artifact, lifecycle_record


def test_valid_markdown_artifact_passes_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")

    result = validate_output_artifact(
        validation_id="OUTVAL-QUALIFICATION-PLAN-MARKDOWN@v1",
        artifact=artifact,
        lifecycle_record=lifecycle_record,
    )

    assert result.status == "passed"
    assert result.issues == []
    assert result.output_format == "markdown"
    assert_output_validation_passes(result)


def test_valid_csv_summary_artifact_passes_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("csv_summary")

    result = validate_output_artifact(
        validation_id="OUTVAL-QUALIFICATION-PLAN-CSV-SUMMARY@v1",
        artifact=artifact,
        lifecycle_record=lifecycle_record,
    )

    assert result.status == "passed"
    assert result.issues == []
    assert result.output_format == "csv_summary"


def test_empty_rendered_content_fails_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")
    payload = artifact.model_dump()
    payload["rendered_content"] = " "
    malformed_artifact = RendererOutputArtifactModel(**payload)

    result = validate_output_artifact(
        validation_id="OUTVAL-EMPTY-CONTENT@v1",
        artifact=malformed_artifact,
        lifecycle_record=lifecycle_record,
    )

    assert result.status == "failed"
    assert "EMPTY_RENDERED_CONTENT" in _issue_codes(result)


def test_metadata_mismatch_fails_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")
    payload = lifecycle_record.model_dump()
    payload["source_artifact_id"] = "ART-MISMATCH@v1"
    mismatched_record = DocumentLifecycleRecordModel(**payload)

    result = validate_output_artifact(
        validation_id="OUTVAL-METADATA-MISMATCH@v1",
        artifact=artifact,
        lifecycle_record=mismatched_record,
    )

    assert result.status == "failed"
    assert "METADATA_ALIGNMENT_MISMATCH" in _issue_codes(result)


def test_missing_placeholder_visibility_fails_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")
    payload = artifact.model_dump()
    payload["rendered_content"] = "Controlled output without visible controls."
    malformed_artifact = RendererOutputArtifactModel(**payload)

    result = validate_output_artifact(
        validation_id="OUTVAL-PLACEHOLDER-MISSING@v1",
        artifact=malformed_artifact,
        lifecycle_record=lifecycle_record,
    )

    assert result.status == "failed"
    assert "MISSING_PLACEHOLDER_VISIBILITY" in _issue_codes(result)


def test_missing_limitation_visibility_fails_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")
    payload = artifact.model_dump()
    payload["rendered_content"] = "Controlled output with placeholder only."
    malformed_artifact = RendererOutputArtifactModel(**payload)

    result = validate_output_artifact(
        validation_id="OUTVAL-LIMITATION-MISSING@v1",
        artifact=malformed_artifact,
        lifecycle_record=lifecycle_record,
    )

    assert result.status == "failed"
    assert "MISSING_LIMITATION_VISIBILITY" in _issue_codes(result)


def test_missing_standards_warning_visibility_fails_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")
    payload = artifact.model_dump()
    payload["rendered_content"] = "Controlled output with placeholder and limitation only."
    malformed_artifact = RendererOutputArtifactModel(**payload)

    result = validate_output_artifact(
        validation_id="OUTVAL-STANDARDS-WARNING-MISSING@v1",
        artifact=malformed_artifact,
        lifecycle_record=lifecycle_record,
    )

    assert result.status == "failed"
    assert "MISSING_STANDARDS_WARNING_VISIBILITY" in _issue_codes(result)


def test_superseded_lifecycle_state_fails_output_validation():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")
    superseded_record = supersede_document_lifecycle_record(
        lifecycle_record,
        superseded_by_record_id="LIFECYCLE-REPLACEMENT-RECORD@v1",
    )

    result = validate_output_artifact(
        validation_id="OUTVAL-SUPERSEDED-LIFECYCLE@v1",
        artifact=artifact,
        lifecycle_record=superseded_record,
    )

    assert result.status == "failed"
    assert "INELIGIBLE_LIFECYCLE_STATE" in _issue_codes(result)


def test_output_validation_does_not_create_uat_acceptance_or_release():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")

    result = validate_output_artifact(
        validation_id="OUTVAL-NON-UAT-BOUNDARY@v1",
        artifact=artifact,
        lifecycle_record=lifecycle_record,
    )

    assert result.status == "passed"
    assert "does_not_create_uat_acceptance" in result.explicit_non_implementation_claims
    assert "does_not_approve_sign_or_release_documents" in (
        result.explicit_non_implementation_claims
    )
    assert "does_not_generate_trial_document_sets" in result.explicit_non_implementation_claims


def test_assert_output_validation_passes_raises_clear_error_on_failure():
    artifact, lifecycle_record = _artifact_and_lifecycle("markdown")
    payload = artifact.model_dump()
    payload["rendered_content"] = " "
    malformed_artifact = RendererOutputArtifactModel(**payload)
    result = validate_output_artifact(
        validation_id="OUTVAL-ASSERTION-FAILURE@v1",
        artifact=malformed_artifact,
        lifecycle_record=lifecycle_record,
    )

    with pytest.raises(ValueError) as exc_info:
        assert_output_validation_passes(result)

    assert "Output validation failed" in str(exc_info.value)
    assert "EMPTY_RENDERED_CONTENT" in str(exc_info.value)


def _issue_codes(result):
    return {issue.issue_code for issue in result.issues}
