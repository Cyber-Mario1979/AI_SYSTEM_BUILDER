import pytest
from pydantic import ValidationError

from asbp.document_template_model import DocumentTemplateRecordModel


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_select_or_load_templates",
        "does_not_generate_documents",
        "does_not_validate_document_input_schemas",
        "does_not_render_or_export_documents",
    ]


def _template_payload() -> dict:
    return {
        "template_id": "TPL-TEST-QUALIFICATION-PLAN@v1",
        "version": "v1",
        "status": "runtime_facing_template_record",
        "lifecycle_status": "active",
        "display_name": "Test qualification plan template",
        "document_family_id": "DOCF-PLAN-STRATEGY",
        "document_type": "Qualification Plan",
        "source_location": "data/source/document_templates/test.json::TPL-TEST-QUALIFICATION-PLAN@v1",
        "applicability": ["qualification"],
        "schema_binding_status": "schema_bound",
        "schema_binding_ref": "SCHEMA-QUALIFICATION-PLAN@v1",
        "standards_bundle_refs": ["SB-CQV-GMP@v1"],
        "intake_route_refs": ["ROUTE-DCF", "ROUTE-SKIP-DCF"],
        "template_controls": ["Template record only."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def test_schema_bound_template_accepts_controlled_schema_ref():
    template = DocumentTemplateRecordModel(**_template_payload())

    assert template.schema_binding_status == "schema_bound"
    assert template.schema_binding_ref == "SCHEMA-QUALIFICATION-PLAN@v1"


def test_schema_bound_template_rejects_future_schema_ref():
    payload = _template_payload()
    payload["schema_binding_ref"] = "SCHEMA-FUTURE-QUALIFICATION-PLAN@v1"

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateRecordModel(**payload)

    assert "must not use SCHEMA-FUTURE" in str(exc_info.value)


def test_pending_schema_binding_still_requires_future_schema_ref():
    payload = _template_payload()
    payload["schema_binding_status"] = "schema_binding_pending_m29_4"
    payload["schema_binding_ref"] = "SCHEMA-FUTURE-QUALIFICATION-PLAN@v1"

    template = DocumentTemplateRecordModel(**payload)
    assert template.schema_binding_ref == "SCHEMA-FUTURE-QUALIFICATION-PLAN@v1"
