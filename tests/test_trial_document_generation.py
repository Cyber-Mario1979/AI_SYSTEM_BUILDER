import pytest

from asbp.output_validation_model import OutputValidationIssueModel, OutputValidationResultModel
from asbp.trial_document_generation import generate_trial_document_set


def test_qp_trial_document_set_generation_succeeds():
    trial_set = generate_trial_document_set(
        trial_set_id="TRIALSET-QP-LOCAL-CQV@v1",
        scenario_id="TRIAL-QP-LOCAL-CQV@v1",
    )

    assert trial_set.status == "controlled_trial_document_set"
    assert trial_set.scenario_id == "TRIAL-QP-LOCAL-CQV@v1"
    assert trial_set.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert [sample.output_format for sample in trial_set.generated_artifacts] == [
        "markdown",
        "csv_summary",
    ]
    assert all(sample.output_validation_status == "passed" for sample in trial_set.generated_artifacts)
    assert all(not sample.customer_ready_release_claimed for sample in trial_set.generated_artifacts)
    assert all(not sample.uat_acceptance_claimed for sample in trial_set.generated_artifacts)


def test_csv_trial_document_set_generation_succeeds():
    trial_set = generate_trial_document_set(
        trial_set_id="TRIALSET-CSV-LOCAL-CQV@v1",
        scenario_id="TRIAL-CSV-LOCAL-CQV@v1",
    )

    assert trial_set.scenario_id == "TRIAL-CSV-LOCAL-CQV@v1"
    assert trial_set.template_id == "TPL-FUTURE-CSV-VALIDATION-PLAN@v1"
    assert trial_set.schema_id == "SCHEMA-CSV-VALIDATION-PLAN@v1"
    assert len(trial_set.generated_artifacts) == 2


def test_trial_generation_can_limit_requested_output_format():
    trial_set = generate_trial_document_set(
        trial_set_id="TRIALSET-QP-LOCAL-CQV-MARKDOWN@v1",
        scenario_id="TRIAL-QP-LOCAL-CQV@v1",
        output_formats=["markdown"],
    )

    assert len(trial_set.generated_artifacts) == 1
    assert trial_set.generated_artifacts[0].output_format == "markdown"


def test_trial_generation_rejects_unsupported_requested_output_format():
    with pytest.raises(ValueError) as exc_info:
        generate_trial_document_set(
            trial_set_id="TRIALSET-QP-LOCAL-CQV-UNSUPPORTED@v1",
            scenario_id="TRIAL-QP-LOCAL-CQV@v1",
            output_formats=["pdf"],  # type: ignore[list-item]
        )

    assert "does not support requested output format" in str(exc_info.value)


def test_output_validation_must_pass_before_trial_record_creation(monkeypatch):
    import asbp.trial_document_generation as trial_generation_module

    def fake_failed_validation(*, validation_id, artifact, lifecycle_record, rule_id=None, rule_library=None):
        return OutputValidationResultModel(
            validation_id=validation_id,
            version="v1",
            status="failed",
            artifact_id=artifact.artifact_id,
            lifecycle_record_id=lifecycle_record.lifecycle_record_id,
            output_format=artifact.output_format,
            rule_id="OUTVALRULE-MARKDOWN-ARTIFACT@v1",
            checks_performed=["artifact_content_presence"],
            issues=[
                OutputValidationIssueModel(
                    issue_code="EMPTY_RENDERED_CONTENT",
                    message="Forced validation failure for trial generation test.",
                    related_ids=[artifact.artifact_id],
                )
            ],
            explicit_non_implementation_claims=[
                "does_not_create_uat_acceptance",
                "does_not_approve_sign_or_release_documents",
                "does_not_generate_trial_document_sets",
                "does_not_deploy_or_productize_outputs",
            ],
        )

    monkeypatch.setattr(
        trial_generation_module,
        "validate_output_artifact",
        fake_failed_validation,
    )

    with pytest.raises(ValueError) as exc_info:
        generate_trial_document_set(
            trial_set_id="TRIALSET-QP-LOCAL-CQV-FAILED-VALIDATION@v1",
            scenario_id="TRIAL-QP-LOCAL-CQV@v1",
            output_formats=["markdown"],
        )

    assert "Output validation failed" in str(exc_info.value)


def test_trial_sample_preserves_limitation_and_review_boundaries():
    trial_set = generate_trial_document_set(
        trial_set_id="TRIALSET-QP-LOCAL-CQV-BOUNDARY@v1",
        scenario_id="TRIAL-QP-LOCAL-CQV@v1",
        output_formats=["markdown"],
    )

    sample = trial_set.generated_artifacts[0]
    assert sample.placeholder_present is True
    assert sample.limitation_present is True
    assert sample.standards_warning_present is True
    assert sample.limitation_carry_forward
    assert "does_not_create_uat_acceptance" in sample.explicit_non_implementation_claims
    assert "does_not_release_or_deploy_documents" in sample.explicit_non_implementation_claims
