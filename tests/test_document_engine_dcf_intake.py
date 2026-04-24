import pytest

from asbp.document_engine import (
    AMBIGUOUS_DCF_DATA_POLICY,
    DCF_DOWNSTREAM_OUTPUT_ROLE,
    DCF_EXTRACTED_DATA_ROLE,
    DCF_INTAKE_CHECKPOINT_ID,
    DCF_INTAKE_CONTRACT_VERSION,
    DCF_NORMALIZED_INPUT_ROLE,
    DCF_RAW_USER_CONTENT_ROLE,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    MISSING_DCF_DATA_POLICY,
    build_dcf_intake_baseline,
    build_dcf_intake_payload,
    build_dcf_template_retrieval_request,
    extract_structured_fields_from_dcf_content,
    normalize_dcf_extracted_data,
    validate_dcf_intake_payload,
)


def _dcf_template_identity() -> dict[str, object]:
    return {
        "template_family": "dcf",
        "template_id": "DCF_URS_INTAKE_v1",
        "template_version": "1.0.0",
        "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
    }


def test_build_dcf_intake_baseline_exposes_m12_3_rules() -> None:
    baseline = build_dcf_intake_baseline()

    assert baseline["checkpoint"] == DCF_INTAKE_CHECKPOINT_ID
    assert baseline["contract_version"] == DCF_INTAKE_CONTRACT_VERSION
    assert DCF_RAW_USER_CONTENT_ROLE in baseline["traceability_chain"]
    assert DCF_EXTRACTED_DATA_ROLE in baseline["traceability_chain"]
    assert DCF_NORMALIZED_INPUT_ROLE in baseline["traceability_chain"]
    assert baseline["missing_data_policy"] == MISSING_DCF_DATA_POLICY
    assert baseline["ambiguous_data_policy"] == AMBIGUOUS_DCF_DATA_POLICY


def test_build_dcf_template_retrieval_request_uses_governed_dcf_lookup() -> None:
    request = build_dcf_template_retrieval_request(
        template_id="DCF_URS_INTAKE_v1",
        template_version="1.0.0",
    )

    assert request["template_family"] == "dcf"
    assert request["template_id"] == "DCF_URS_INTAKE_v1"
    assert request["template_version"] == "1.0.0"
    assert request["artifact_kind"] == GOVERNED_TEMPLATE_ARTIFACT_KIND


def test_extract_structured_fields_from_dcf_content_parses_key_value_text() -> None:
    extracted = extract_structured_fields_from_dcf_content(
        """
        System Name: Tablet Press
        System Type: process-equipment
        Intended Use = Compress tablets
        User Requirements: safe operation
        """
    )

    assert extracted["system_name"] == "Tablet Press"
    assert extracted["system_type"] == "process-equipment"
    assert extracted["intended_use"] == "Compress tablets"
    assert extracted["user_requirements"] == "safe operation"


def test_extract_structured_fields_from_dcf_content_rejects_ambiguous_duplicates() -> None:
    with pytest.raises(ValueError, match="Ambiguous DCF field"):
        extract_structured_fields_from_dcf_content(
            """
            System Name: Tablet Press
            System Name: Coating Pan
            """
        )


def test_normalize_dcf_extracted_data_marks_missing_required_fields_explicitly() -> None:
    normalized = normalize_dcf_extracted_data(
        target_document_family="urs",
        extracted_fields={
            "system_name": "Tablet Press",
            "system_type": "process-equipment",
        },
    )

    assert normalized["source_role"] == DCF_NORMALIZED_INPUT_ROLE
    assert "intended_use" in normalized["missing_fields"]
    assert normalized["input_data"]["intended_use"]["status"] == "missing"
    assert normalized["input_data"]["intended_use"]["policy"] == (
        MISSING_DCF_DATA_POLICY
    )


def test_build_dcf_intake_payload_preserves_full_traceability_chain() -> None:
    payload = build_dcf_intake_payload(
        dcf_artifact_id="DCF-UPLOAD-001",
        target_document_family="urs",
        template_identity=_dcf_template_identity(),
        raw_content={
            "system_name": "Tablet Press",
            "system_type": "process-equipment",
            "intended_use": "Compress tablets",
            "user_requirements": ["safe operation"],
        },
        content_format="mapping",
        downstream_document_id="URS-001",
    )

    assert payload["checkpoint"] == DCF_INTAKE_CHECKPOINT_ID
    assert payload["raw_user_content"]["source_role"] == DCF_RAW_USER_CONTENT_ROLE
    assert payload["extracted_data"]["source_role"] == DCF_EXTRACTED_DATA_ROLE
    assert payload["normalized_document_input"]["source_role"] == (
        DCF_NORMALIZED_INPUT_ROLE
    )
    assert payload["traceability"]["raw_content_ref"] == "DCF-UPLOAD-001"
    assert payload["traceability"]["downstream_document_id"] == "URS-001"
    assert payload["traceability"]["downstream_output_role"] == (
        DCF_DOWNSTREAM_OUTPUT_ROLE
    )


def test_build_dcf_intake_payload_rejects_non_dcf_template_identity() -> None:
    template_identity = _dcf_template_identity()
    template_identity["template_family"] = "urs"

    with pytest.raises(ValueError, match="requires a governed DCF template"):
        build_dcf_intake_payload(
            dcf_artifact_id="DCF-UPLOAD-001",
            target_document_family="urs",
            template_identity=template_identity,
            raw_content={"system_name": "Tablet Press"},
            content_format="mapping",
        )


def test_validate_dcf_intake_payload_accepts_existing_valid_payload() -> None:
    payload = build_dcf_intake_payload(
        dcf_artifact_id="DCF-UPLOAD-001",
        target_document_family="urs",
        template_identity=_dcf_template_identity(),
        raw_content={
            "system_name": "Tablet Press",
            "system_type": "process-equipment",
            "intended_use": "Compress tablets",
            "user_requirements": ["safe operation"],
        },
        content_format="mapping",
    )

    validate_dcf_intake_payload(payload)
