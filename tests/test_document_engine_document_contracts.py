import pytest

from asbp.document_engine import (
    DOCUMENT_CONTRACT_CHECKPOINT_ID,
    DOCUMENT_OUTPUT_CONTRACT_VERSION,
    DOCUMENT_REQUEST_CONTRACT_VERSION,
    EXECUTION_CONTEXT_SOURCE_ROLE,
    GENERATED_LANGUAGE_OUTPUT_ROLE,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    build_document_input_contract,
    build_document_output_contract,
    build_document_request_contract_baseline,
    build_document_request_payload,
    validate_document_request_payload,
)


def _urs_template_identity() -> dict[str, object]:
    return {
        "template_family": "urs",
        "template_id": "URS_BASE_v1",
        "template_version": "1.0.0",
        "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
    }


def _urs_input_data() -> dict[str, object]:
    return {
        "system_name": "Tablet Press",
        "system_type": "process-equipment",
        "intended_use": "Compress tablets",
        "user_requirements": ["safe operation", "controlled compression force"],
    }


def test_build_document_request_contract_baseline_exposes_m12_2_rules() -> None:
    baseline = build_document_request_contract_baseline()

    assert baseline["checkpoint"] == DOCUMENT_CONTRACT_CHECKPOINT_ID
    assert baseline["request_contract_version"] == DOCUMENT_REQUEST_CONTRACT_VERSION
    assert baseline["output_contract_version"] == DOCUMENT_OUTPUT_CONTRACT_VERSION
    assert "urs" in baseline["supported_document_families"]
    assert "work_package" in baseline["supported_execution_context_kinds"]
    assert baseline["truth_separation"]["generated_language_output"] == (
        GENERATED_LANGUAGE_OUTPUT_ROLE
    )


def test_build_document_input_contract_returns_family_required_fields() -> None:
    contract = build_document_input_contract("urs")

    assert contract["checkpoint"] == DOCUMENT_CONTRACT_CHECKPOINT_ID
    assert contract["contract_version"] == DOCUMENT_REQUEST_CONTRACT_VERSION
    assert contract["document_family"] == "urs"
    assert "system_name" in contract["required_input_fields"]
    assert "freeform_prompt" in contract["prohibited_input_fields"]


def test_build_document_output_contract_returns_output_shape() -> None:
    contract = build_document_output_contract("report")

    assert contract["checkpoint"] == DOCUMENT_CONTRACT_CHECKPOINT_ID
    assert contract["contract_version"] == DOCUMENT_OUTPUT_CONTRACT_VERSION
    assert contract["document_family"] == "report"
    assert "generated_language_output" in contract["required_output_fields"]
    assert contract["generated_language_role"] == GENERATED_LANGUAGE_OUTPUT_ROLE


def test_build_document_request_payload_returns_valid_governed_shape() -> None:
    payload = build_document_request_payload(
        document_job_id="DOCJOB-001",
        document_family="urs",
        document_id="URS-001",
        template_identity=_urs_template_identity(),
        execution_context_kind="work_package",
        execution_context_ref="WP-001",
        input_data=_urs_input_data(),
    )

    assert payload["checkpoint"] == DOCUMENT_CONTRACT_CHECKPOINT_ID
    assert payload["contract_version"] == DOCUMENT_REQUEST_CONTRACT_VERSION
    assert payload["document_family"] == "urs"
    assert payload["template_identity"]["template_id"] == "URS_BASE_v1"
    assert payload["execution_context"]["kind"] == "work_package"
    assert payload["execution_context"]["source_role"] == (
        EXECUTION_CONTEXT_SOURCE_ROLE
    )


def test_validate_document_request_payload_rejects_missing_family_required_input() -> None:
    input_data = _urs_input_data()
    del input_data["system_name"]

    with pytest.raises(ValueError, match="required system_name"):
        build_document_request_payload(
            document_job_id="DOCJOB-001",
            document_family="urs",
            document_id="URS-001",
            template_identity=_urs_template_identity(),
            execution_context_kind="work_package",
            execution_context_ref="WP-001",
            input_data=input_data,
        )


def test_validate_document_request_payload_rejects_supporting_template_artifact() -> None:
    template_identity = _urs_template_identity()
    template_identity["artifact_kind"] = "supporting_template_reference"

    with pytest.raises(
        ValueError,
        match="Governed template retrieval may target only",
    ):
        build_document_request_payload(
            document_job_id="DOCJOB-001",
            document_family="urs",
            document_id="URS-001",
            template_identity=template_identity,
            execution_context_kind="work_package",
            execution_context_ref="WP-001",
            input_data=_urs_input_data(),
        )


def test_validate_document_request_payload_rejects_invalid_execution_context_kind() -> None:
    with pytest.raises(ValueError, match="Unsupported execution context kind"):
        build_document_request_payload(
            document_job_id="DOCJOB-001",
            document_family="urs",
            document_id="URS-001",
            template_identity=_urs_template_identity(),
            execution_context_kind="raw_database_row",
            execution_context_ref="WP-001",
            input_data=_urs_input_data(),
        )


def test_validate_document_request_payload_rejects_prohibited_input_field() -> None:
    input_data = _urs_input_data()
    input_data["freeform_prompt"] = "Write anything you want."

    with pytest.raises(
        ValueError,
        match="freeform_prompt is not allowed",
    ):
        build_document_request_payload(
            document_job_id="DOCJOB-001",
            document_family="urs",
            document_id="URS-001",
            template_identity=_urs_template_identity(),
            execution_context_kind="work_package",
            execution_context_ref="WP-001",
            input_data=input_data,
        )


def test_validate_document_request_payload_accepts_existing_valid_payload() -> None:
    payload = build_document_request_payload(
        document_job_id="DOCJOB-001",
        document_family="urs",
        document_id="URS-001",
        template_identity=_urs_template_identity(),
        execution_context_kind="work_package",
        execution_context_ref="WP-001",
        input_data=_urs_input_data(),
    )

    validate_document_request_payload(payload)