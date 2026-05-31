import pytest
from pydantic import ValidationError

from asbp.document_template_body_model import (
    DocumentTemplateBodyLibraryModel,
    DocumentTemplateBodyRecordModel,
)


def _required_claims() -> list[str]:
    return [
        "does_not_generate_documents",
        "does_not_create_signed_or_approved_records",
        "does_not_replace_human_review",
        "does_not_claim_product_release",
    ]


def _minimal_body_record_payload() -> dict:
    return {
        "body_id": "TBODY-TEST-DOCUMENT@v1",
        "version": "v1",
        "status": "mvp_template_body_record",
        "document_ref": "TEST_DOCUMENT",
        "display_name": "Test Document",
        "template_body_kind": "authored_template",
        "output_role": "planning",
        "priority": "P0",
        "mvp_status": "must_have",
        "linked_template_id": None,
        "linked_schema_id": None,
        "source_structure_references": ["unit_test_structure_reference"],
        "owner_review_required": True,
        "sections": [
            {
                "section_id": "SEC-PURPOSE",
                "title": "Purpose",
                "purpose": "Define document purpose.",
                "requirement_status": "required",
                "expected_content_types": ["narrative"],
                "source_input_refs": ["user_input.purpose"],
                "downstream_refs": [],
                "section_controls": [
                    "Missing inputs remain visible.",
                    "Section does not approve or release output.",
                ],
            }
        ],
        "tables": [
            {
                "table_id": "TBL-TEST",
                "title": "Test table",
                "columns": ["Column A", "Column B"],
            }
        ],
        "template_controls": [
            "Template body record does not generate documents.",
        ],
        "explicit_non_implementation_claims": _required_claims(),
    }


def _minimal_library_payload() -> dict:
    return {
        "library_id": "M29_DOCUMENT_TEMPLATE_BODY_LIBRARY@v1",
        "version": "v1",
        "status": "mvp_template_body_source",
        "source_authority": "unit_test",
        "body_records": [_minimal_body_record_payload()],
        "library_controls": [
            "Template body library does not generate documents.",
        ],
        "explicit_non_implementation_claims": _required_claims(),
    }


def test_document_template_body_record_accepts_controlled_minimum():
    body_record = DocumentTemplateBodyRecordModel(**_minimal_body_record_payload())

    assert body_record.body_id == "TBODY-TEST-DOCUMENT@v1"
    assert body_record.document_ref == "TEST_DOCUMENT"
    assert body_record.sections[0].section_id == "SEC-PURPOSE"


def test_document_template_body_record_rejects_version_mismatch():
    payload = _minimal_body_record_payload()
    payload["version"] = "v2"

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateBodyRecordModel(**payload)

    assert "version must match body_id suffix" in str(exc_info.value)


def test_document_template_body_record_rejects_duplicate_sections():
    payload = _minimal_body_record_payload()
    payload["sections"].append(dict(payload["sections"][0]))

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateBodyRecordModel(**payload)

    assert "Duplicate document template section_id" in str(exc_info.value)


def test_document_template_body_record_requires_non_implementation_claims():
    payload = _minimal_body_record_payload()
    payload["explicit_non_implementation_claims"] = ["does_not_generate_documents"]

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateBodyRecordModel(**payload)

    assert "missing explicit non-implementation claims" in str(exc_info.value)


def test_external_reference_plan_cannot_link_to_authored_template_id():
    payload = _minimal_body_record_payload()
    payload["template_body_kind"] = "external_reference_plan"
    payload["linked_template_id"] = "TPL-TEST-DOCUMENT@v1"

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateBodyRecordModel(**payload)

    assert "External/data-extraction template body records must not link" in str(
        exc_info.value
    )


def test_document_template_body_library_rejects_duplicate_document_refs():
    body_record = _minimal_body_record_payload()
    duplicate_document_ref = dict(body_record)
    duplicate_document_ref["body_id"] = "TBODY-TEST-DUPLICATE-REF@v1"
    payload = _minimal_library_payload()
    payload["body_records"].append(duplicate_document_ref)

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateBodyLibraryModel(**payload)

    assert "Duplicate document template document_ref" in str(exc_info.value)


def test_document_template_body_library_requires_non_implementation_claims():
    payload = _minimal_library_payload()
    payload["explicit_non_implementation_claims"] = ["does_not_generate_documents"]

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateBodyLibraryModel(**payload)

    assert "missing explicit non-implementation claims" in str(exc_info.value)
