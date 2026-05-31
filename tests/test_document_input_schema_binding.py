from copy import deepcopy

import pytest

from asbp.document_input_schema_binding import (
    build_template_schema_binding_id,
    load_document_input_schema_for_selection_result,
    load_document_input_schema_for_template_id,
    resolve_document_input_schema_for_template,
)
from asbp.document_input_schema_store import (
    load_default_document_input_schema_library,
    load_document_input_schema_library_from_payload,
)
from asbp.document_template_store import load_default_document_template_library
from asbp.template_selection import select_template_for_request
from asbp.template_selection_model import TemplateSelectionInputModel


def _required_selection_claims() -> list[str]:
    return [
        "does_not_generate_documents",
        "does_not_validate_document_input_schemas",
        "does_not_render_or_export_documents",
        "does_not_use_ai_to_choose_templates",
    ]


def _qualification_selection_request() -> TemplateSelectionInputModel:
    return TemplateSelectionInputModel(
        selection_id="TPLSEL-QUALIFICATION-PLAN@v1",
        document_family_id="DOCF-PLAN-STRATEGY",
        document_type="Qualification Plan",
        standards_bundle_refs=["SB-CQV-GMP@v1"],
        intake_route_ref="ROUTE-DCF",
        selection_controls=["Deterministic selection test."],
        explicit_non_implementation_claims=_required_selection_claims(),
    )


def test_template_id_resolves_bound_document_input_schema():
    schema = load_document_input_schema_for_template_id(
        "TPL-FUTURE-QUALIFICATION-PLAN@v1",
    )

    assert schema.schema_id == "SCHEMA-QUALIFICATION-PLAN@v1"
    assert schema.template_id == "TPL-FUTURE-QUALIFICATION-PLAN@v1"


def test_selection_result_resolves_bound_document_input_schema():
    result = select_template_for_request(_qualification_selection_request())
    schema = load_document_input_schema_for_selection_result(result)

    assert result.status == "selected"
    assert schema.schema_id == "SCHEMA-QUALIFICATION-PLAN@v1"


def test_unselected_result_does_not_resolve_schema():
    request = _qualification_selection_request()
    request.document_type = "Missing Document Type"
    result = select_template_for_request(request)

    with pytest.raises(ValueError) as exc_info:
        load_document_input_schema_for_selection_result(result)

    assert "selected template" in str(exc_info.value)


def test_schema_template_mismatch_is_rejected():
    template_library = load_default_document_template_library()
    schema_payload = load_default_document_input_schema_library().model_dump()
    schema_payload["schema_records"] = [schema_payload["schema_records"][0]]
    schema_payload["schema_records"][0]["template_id"] = (
        "TPL-FUTURE-CSV-VALIDATION-PLAN@v1"
    )
    schema_library = load_document_input_schema_library_from_payload(schema_payload)
    template = template_library.template_records[0]

    with pytest.raises(ValueError) as exc_info:
        resolve_document_input_schema_for_template(
            template,
            schema_library=schema_library,
        )

    assert "template_id does not match" in str(exc_info.value)


def test_missing_schema_ref_is_rejected():
    template_library = load_default_document_template_library()
    template = deepcopy(template_library.template_records[0])
    template.schema_binding_ref = "SCHEMA-MISSING@v1"

    with pytest.raises(ValueError) as exc_info:
        resolve_document_input_schema_for_template(template)

    assert "Document input schema source record not found" in str(exc_info.value)


def test_template_schema_binding_id_is_deterministic():
    assert build_template_schema_binding_id(
        "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "SCHEMA-QUALIFICATION-PLAN@v1",
    ) == "TPL-FUTURE-QUALIFICATION-PLAN@v1::SCHEMA-QUALIFICATION-PLAN@v1"
