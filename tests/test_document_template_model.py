from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.document_template_model import (
    DocumentTemplateLibraryModel,
    DocumentTemplateRecordModel,
)


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_select_or_load_templates",
        "does_not_generate_documents",
        "does_not_validate_document_input_schemas",
        "does_not_render_or_export_documents",
    ]


def _minimal_template_payload() -> dict:
    return {
        "template_id": "TPL-TEST-QUALIFICATION-PLAN@v1",
        "version": "v1",
        "status": "runtime_facing_template_record",
        "lifecycle_status": "active",
        "display_name": "Test qualification plan template",
        "document_family_id": "DOCF-PLAN-STRATEGY",
        "document_type": "Qualification Plan",
        "source_location": (
            "data/source/document_templates/starter_document_templates.json::"
            "TPL-TEST-QUALIFICATION-PLAN@v1"
        ),
        "applicability": ["qualification", "validation"],
        "schema_binding_status": "schema_binding_pending_m29_4",
        "schema_binding_ref": "SCHEMA-FUTURE-QUALIFICATION-PLAN@v1",
        "standards_bundle_refs": ["SB-CQV-GMP@v1"],
        "intake_route_refs": ["ROUTE-DCF", "ROUTE-SKIP-DCF"],
        "template_controls": [
            "Template record establishes controlled identity only.",
        ],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def _minimal_library_payload(template: dict | None = None) -> dict:
    return {
        "library_id": "M29_DOCUMENT_TEMPLATE_LIBRARY@v1",
        "version": "v1",
        "status": "runtime_facing_template_source",
        "template_records": [template or _minimal_template_payload()],
        "library_controls": [
            "Template library records identity, applicability, and binding metadata only.",
        ],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def test_template_record_accepts_controlled_minimum():
    template = DocumentTemplateRecordModel(**_minimal_template_payload())

    assert template.template_id == "TPL-TEST-QUALIFICATION-PLAN@v1"
    assert template.version == "v1"
    assert template.schema_binding_status == "schema_binding_pending_m29_4"
    assert template.standards_bundle_refs == ["SB-CQV-GMP@v1"]


def test_template_record_rejects_version_mismatch():
    template = _minimal_template_payload()
    template["version"] = "v2"

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateRecordModel(**template)

    assert "version must match template_id suffix" in str(exc_info.value)


def test_template_record_rejects_blank_applicability_value():
    template = _minimal_template_payload()
    template["applicability"] = ["qualification", ""]

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateRecordModel(**template)

    assert "Blank document template source value is not allowed" in str(
        exc_info.value
    )


def test_template_record_rejects_unsupported_intake_route():
    template = _minimal_template_payload()
    template["intake_route_refs"] = ["ROUTE-DCF", "ROUTE-UNCONTROLLED"]

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateRecordModel(**template)

    assert "unsupported route" in str(exc_info.value)


def test_pending_schema_binding_requires_future_schema_ref():
    template = _minimal_template_payload()
    template["schema_binding_ref"] = "SCHEMA-QUALIFICATION-PLAN@v1"

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateRecordModel(**template)

    assert "SCHEMA-FUTURE" in str(exc_info.value)


def test_template_record_requires_explicit_non_implementation_claims():
    template = _minimal_template_payload()
    template["explicit_non_implementation_claims"] = [
        "does_not_select_or_load_templates"
    ]

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateRecordModel(**template)

    assert "M29.2 document template record is missing explicit" in str(
        exc_info.value
    )


def test_template_library_rejects_duplicate_template_ids():
    template = _minimal_template_payload()
    payload = _minimal_library_payload(template)
    payload["template_records"].append(deepcopy(template))

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateLibraryModel(**payload)

    assert "Duplicate document template id is not allowed" in str(exc_info.value)


def test_template_library_requires_explicit_non_implementation_claims():
    payload = _minimal_library_payload()
    payload["explicit_non_implementation_claims"] = [
        "does_not_select_or_load_templates"
    ]

    with pytest.raises(ValidationError) as exc_info:
        DocumentTemplateLibraryModel(**payload)

    assert "M29.2 document template library is missing explicit" in str(
        exc_info.value
    )
