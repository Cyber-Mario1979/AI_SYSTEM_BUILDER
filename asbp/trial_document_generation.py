from __future__ import annotations

from asbp.controlled_drafting import build_controlled_draft_packet_for_template
from asbp.document_lifecycle import create_document_lifecycle_record_from_artifact
from asbp.output_validation import assert_output_validation_passes, validate_output_artifact
from asbp.renderer_output import render_output_artifact
from asbp.standards_backed_output import build_standards_backed_output_controls_for_draft
from asbp.trial_document_generation_model import (
    REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS,
    TrialDocumentOutputFormat,
    TrialDocumentScenarioLibraryModel,
    TrialDocumentSetModel,
    TrialGeneratedArtifactRefModel,
)
from asbp.trial_document_generation_store import (
    get_trial_document_scenario_by_id,
    load_default_trial_document_scenario_library,
)


def generate_trial_document_set(
    *,
    trial_set_id: str,
    scenario_id: str,
    output_formats: list[TrialDocumentOutputFormat] | None = None,
    scenario_library: TrialDocumentScenarioLibraryModel | None = None,
) -> TrialDocumentSetModel:
    scenario_library = scenario_library or load_default_trial_document_scenario_library()
    scenario = get_trial_document_scenario_by_id(scenario_library, scenario_id)
    requested_output_formats = output_formats or list(scenario.output_formats)

    unsupported_formats = sorted(set(requested_output_formats) - set(scenario.output_formats))
    if unsupported_formats:
        raise ValueError(
            "Trial document scenario does not support requested output format(s): "
            f"{', '.join(unsupported_formats)}"
        )

    generated_artifacts = [
        _generate_trial_sample_for_format(
            scenario=scenario,
            output_format=output_format,
        )
        for output_format in requested_output_formats
    ]

    first_sample = generated_artifacts[0]
    return TrialDocumentSetModel(
        trial_set_id=trial_set_id,
        version=_version_from_id(trial_set_id),
        scenario_id=scenario.scenario_id,
        template_id=scenario.template_id,
        schema_id=_schema_id_from_sample(first_sample),
        generated_artifacts=generated_artifacts,
        trial_set_controls=[
            "Trial document set is generated only from the validated M29 document/output chain.",
            "Trial document set is for local review only and is not customer-ready release.",
            "Trial document set does not create UAT acceptance or QMS approval records.",
        ],
        explicit_non_implementation_claims=sorted(
            REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def _generate_trial_sample_for_format(
    *,
    scenario,
    output_format: TrialDocumentOutputFormat,
) -> TrialGeneratedArtifactRefModel:
    scenario_token = _scenario_token(scenario.scenario_id)
    output_token = _output_format_token(output_format)

    draft_packet = build_controlled_draft_packet_for_template(
        draft_id=f"DRAFT-{scenario_token}-{output_token}@v1",
        drafting_mode_id=scenario.drafting_mode_id,
        template_id=scenario.template_id,
        input_values=scenario.input_values,
        intake_route_ref=scenario.intake_route_ref,
    )
    standards_packet = build_standards_backed_output_controls_for_draft(
        control_packet_id=f"STDOUT-{scenario_token}-{output_token}@v1",
        draft_packet=draft_packet,
        standards_bundle_refs=scenario.standards_bundle_refs,
    )
    artifact = render_output_artifact(
        artifact_id=f"ART-{scenario_token}-{output_token}@v1",
        output_format=output_format,
        draft_packet=draft_packet,
        standards_packet=standards_packet,
    )
    lifecycle_record = create_document_lifecycle_record_from_artifact(
        lifecycle_record_id=f"LIFECYCLE-{scenario_token}-{output_token}@v1",
        artifact=artifact,
    )
    validation_result = validate_output_artifact(
        validation_id=f"OUTVAL-{scenario_token}-{output_token}@v1",
        artifact=artifact,
        lifecycle_record=lifecycle_record,
    )
    assert_output_validation_passes(validation_result)

    return TrialGeneratedArtifactRefModel(
        sample_id=f"TRIALSAMPLE-{scenario_token}-{output_token}@v1",
        version="v1",
        scenario_id=scenario.scenario_id,
        output_format=output_format,
        draft_id=draft_packet.draft_id,
        standards_control_packet_id=standards_packet.control_packet_id,
        artifact_id=artifact.artifact_id,
        artifact_filename=artifact.artifact_filename,
        lifecycle_record_id=lifecycle_record.lifecycle_record_id,
        output_validation_result_id=validation_result.validation_id,
        output_validation_status=validation_result.status,
        placeholder_present=artifact.metadata.placeholder_present,
        limitation_present=artifact.metadata.limitation_present,
        standards_warning_present=artifact.metadata.standards_warning_present,
        limitation_carry_forward=list(lifecycle_record.carried_forward_limitations),
        review_notes=[
            "Trial sample is generated for local review only.",
            "Output validation passed before trial sample record creation.",
            "Trial sample does not create UAT acceptance or customer-ready release.",
        ],
        explicit_non_implementation_claims=sorted(
            REQUIRED_TRIAL_DOCUMENT_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def _scenario_token(scenario_id: str) -> str:
    return scenario_id.removeprefix("TRIAL-").split("@", 1)[0]


def _output_format_token(output_format: str) -> str:
    return output_format.upper().replace("_", "-")


def _schema_id_from_sample(sample: TrialGeneratedArtifactRefModel) -> str:
    if "CSV" in sample.artifact_id:
        return "SCHEMA-CSV-VALIDATION-PLAN@v1"
    return "SCHEMA-QUALIFICATION-PLAN@v1"


def _version_from_id(identifier: str) -> str:
    return identifier.rsplit("@", 1)[1]
