from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.document_input_schema_model import (
    DocumentInputSchemaLibraryModel,
    DocumentInputSchemaRecordModel,
)


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_draft_document_content",
        "does_not_generate_documents",
        "does_not_validate_final_document_output",
        "does_not_render_or_export_documents",
    ]


def _field_payload(field_id: str, requirement_status: str = "required") -> dict:
    payload = {
        "field_id": field_id,
        "display_name": field_id.replace("_", " ").title(),
        "requirement_status": requirement_status,
        "value_type": "string",
        "applies_to_routes": ["ROUTE-DCF", "ROUTE-SKIP-DCF"],
        "placeholder_policy": "placeholder_required_when_missing",
        "missing_data_behavior": "review_required",
        "normalization_rules": ["trim_whitespace"],
        "source_input_refs": [f"user_input.{field_id}"],
        "section_binding_refs": ["section.test"],
    }
    if requirement_status == "conditional":
        payload["conditional_reason"] = "Required when the condition applies."
    return payload


def _route_mapping(route_ref: str, field_ids: list[str]) -> dict:
    return {
        "route_ref": route_ref,
        "field_ids": field_ids,
        "mapping_controls": ["Route mapping remains input-contract only."],
    }


def _minimal_schema_payload() -> dict:
    return {
        "schema_id": "SCHEMA-TEST-QUALIFICATION-PLAN@v1",
        "version": "v1",
        "status": "runtime_facing_document_input_schema_record",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "document_family_id": "DOCF-PLAN-STRATEGY",
        "document_type": "Qualification Plan",
        "required_fields": [
            _field_payload("project_title"),
            _field_payload("cqv_scope"),
        ],
        "optional_fields": [_field_payload("standards_context", "optional")],
        "conditional_fields": [_field_payload("cleanroom_classification", "conditional")],
        "dcf_intake_mapping": _route_mapping(
            "ROUTE-DCF",
            [
                "project_title",
                "cqv_scope",
                "standards_context",
                "cleanroom_classification",
            ],
        ),
        "skip_dcf_minimum_input_mapping": _route_mapping(
            "ROUTE-SKIP-DCF",
            ["project_title", "cqv_scope"],
        ),
        "missing_data_controls": ["Missing data remains visible."],
        "schema_controls": ["Schema binds inputs to template expectations only."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def _minimal_library_payload(schema: dict | None = None) -> dict:
    return {
        "library_id": "M29_DOCUMENT_INPUT_SCHEMA_LIBRARY@v1",
        "version": "v1",
        "status": "runtime_facing_document_input_schema_source",
        "schema_records": [schema or _minimal_schema_payload()],
        "library_controls": ["Schema library remains source truth only."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def test_schema_record_accepts_controlled_minimum():
    schema = DocumentInputSchemaRecordModel(**_minimal_schema_payload())

    assert schema.schema_id == "SCHEMA-TEST-QUALIFICATION-PLAN@v1"
    assert schema.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"
    assert schema.dcf_intake_mapping.route_ref == "ROUTE-DCF"


def test_schema_record_rejects_version_mismatch():
    payload = _minimal_schema_payload()
    payload["version"] = "v2"

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaRecordModel(**payload)

    assert "version must match schema_id suffix" in str(exc_info.value)


def test_schema_record_rejects_duplicate_field_ids():
    payload = _minimal_schema_payload()
    payload["optional_fields"].append(_field_payload("project_title", "optional"))

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaRecordModel(**payload)

    assert "Duplicate document input schema field_id" in str(exc_info.value)


def test_schema_record_rejects_field_in_wrong_requirement_bucket():
    payload = _minimal_schema_payload()
    payload["optional_fields"] = [_field_payload("optional_but_required", "required")]

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaRecordModel(**payload)

    assert "wrong requirement bucket" in str(exc_info.value)


def test_conditional_field_requires_reason():
    payload = _minimal_schema_payload()
    del payload["conditional_fields"][0]["conditional_reason"]

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaRecordModel(**payload)

    assert "requires conditional_reason" in str(exc_info.value)


def test_route_mapping_rejects_unknown_field_id():
    payload = _minimal_schema_payload()
    payload["dcf_intake_mapping"]["field_ids"].append("missing_field")

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaRecordModel(**payload)

    assert "unknown field_id" in str(exc_info.value)


def test_schema_requires_explicit_non_implementation_claims():
    payload = _minimal_schema_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_draft_document_content"
    ]

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaRecordModel(**payload)

    assert "M29.4 document input schema is missing explicit" in str(exc_info.value)


def test_schema_library_rejects_duplicate_schema_ids():
    schema = _minimal_schema_payload()
    payload = _minimal_library_payload(schema)
    payload["schema_records"].append(deepcopy(schema))

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaLibraryModel(**payload)

    assert "Duplicate document input schema id" in str(exc_info.value)


def test_schema_library_rejects_duplicate_template_ids():
    schema = _minimal_schema_payload()
    duplicate = deepcopy(schema)
    duplicate["schema_id"] = "SCHEMA-TEST-QUALIFICATION-PLAN-ALT@v1"
    payload = _minimal_library_payload(schema)
    payload["schema_records"].append(duplicate)

    with pytest.raises(ValidationError) as exc_info:
        DocumentInputSchemaLibraryModel(**payload)

    assert "Duplicate document input schema template_id" in str(exc_info.value)
