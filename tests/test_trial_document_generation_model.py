from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.trial_document_generation_model import (
    TrialDocumentScenarioLibraryModel,
    TrialDocumentScenarioModel,
    TrialDocumentSetModel,
)


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_create_uat_acceptance",
        "does_not_release_or_deploy_documents",
        "does_not_create_customer_ready_output",
        "does_not_create_qms_approval_records",
    ]


def _minimal_scenario_payload() -> dict:
    return {
        "scenario_id": "TRIAL-TEST-LOCAL-CQV@v1",
        "version": "v1",
        "status": "runtime_facing_trial_document_scenario_record",
        "display_name": "Test trial scenario",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "drafting_mode_id": "DRAFTMODE-MINIMAL-SCAFFOLD-PLACEHOLDERS@v1",
        "standards_bundle_refs": ["SB-CQV-GMP@v1"],
        "input_values": {"project_title": "Project Alpha"},
        "intake_route_ref": "ROUTE-SKIP-DCF",
        "output_formats": ["markdown"],
        "scenario_controls": ["Trial scenario controls local sample generation only."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def _minimal_sample_payload() -> dict:
    return {
        "sample_id": "TRIALSAMPLE-TEST-LOCAL-CQV-MARKDOWN@v1",
        "version": "v1",
        "status": "controlled_trial_document_sample_record",
        "scenario_id": "TRIAL-TEST-LOCAL-CQV@v1",
        "output_format": "markdown",
        "draft_id": "DRAFT-TEST-LOCAL-CQV-MARKDOWN@v1",
        "standards_control_packet_id": "STDOUT-TEST-LOCAL-CQV-MARKDOWN@v1",
        "artifact_id": "ART-TEST-LOCAL-CQV-MARKDOWN@v1",
        "artifact_filename": "art_test_local_cqv_markdown_v1.md",
        "lifecycle_record_id": "LIFECYCLE-TEST-LOCAL-CQV-MARKDOWN@v1",
        "output_validation_result_id": "OUTVAL-TEST-LOCAL-CQV-MARKDOWN@v1",
        "output_validation_status": "passed",
        "placeholder_present": True,
        "limitation_present": True,
        "standards_warning_present": True,
        "limitation_carry_forward": ["Visible limitations carried forward."],
        "review_notes": ["Trial sample is for local review only."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def _minimal_trial_set_payload(sample: dict | None = None) -> dict:
    return {
        "trial_set_id": "TRIALSET-TEST-LOCAL-CQV@v1",
        "version": "v1",
        "status": "controlled_trial_document_set",
        "scenario_id": "TRIAL-TEST-LOCAL-CQV@v1",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "schema_id": "SCHEMA-QUALIFICATION-PLAN@v1",
        "generated_artifacts": [sample or _minimal_sample_payload()],
        "trial_set_controls": ["Trial set is not a release or UAT record."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def test_trial_document_scenario_accepts_controlled_minimum():
    scenario = TrialDocumentScenarioModel(**_minimal_scenario_payload())

    assert scenario.scenario_id == "TRIAL-TEST-LOCAL-CQV@v1"
    assert scenario.output_formats == ["markdown"]


def test_trial_document_scenario_rejects_duplicate_output_formats():
    scenario = _minimal_scenario_payload()
    scenario["output_formats"] = ["markdown", "markdown"]

    with pytest.raises(ValidationError) as exc_info:
        TrialDocumentScenarioModel(**scenario)

    assert "Duplicate trial document output_formats" in str(exc_info.value)


def test_trial_document_scenario_library_rejects_duplicate_scenario_ids():
    scenario = _minimal_scenario_payload()
    payload = {
        "library_id": "M29_TRIAL_DOCUMENT_SCENARIO_LIBRARY@v1",
        "version": "v1",
        "status": "runtime_facing_trial_document_scenario_source",
        "scenarios": [scenario, deepcopy(scenario)],
        "library_controls": ["Trial scenario library controls local sample generation."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }

    with pytest.raises(ValidationError) as exc_info:
        TrialDocumentScenarioLibraryModel(**payload)

    assert "Duplicate trial document scenario id" in str(exc_info.value)


def test_trial_sample_rejects_customer_ready_release_claim():
    sample = _minimal_sample_payload()
    sample["customer_ready_release_claimed"] = True

    payload = _minimal_trial_set_payload(sample)

    with pytest.raises(ValidationError) as exc_info:
        TrialDocumentSetModel(**payload)

    assert "customer-ready release" in str(exc_info.value)


def test_trial_sample_rejects_uat_acceptance_claim():
    sample = _minimal_sample_payload()
    sample["uat_acceptance_claimed"] = True

    payload = _minimal_trial_set_payload(sample)

    with pytest.raises(ValidationError) as exc_info:
        TrialDocumentSetModel(**payload)

    assert "UAT acceptance" in str(exc_info.value)


def test_trial_document_set_requires_non_implementation_claims():
    payload = _minimal_trial_set_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_create_uat_acceptance"
    ]

    with pytest.raises(ValidationError) as exc_info:
        TrialDocumentSetModel(**payload)

    assert "M29.10 trial document set is missing explicit" in str(exc_info.value)
