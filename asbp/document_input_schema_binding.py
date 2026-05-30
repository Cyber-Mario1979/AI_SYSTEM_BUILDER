from __future__ import annotations

from asbp.document_input_schema_model import (
    DocumentInputSchemaLibraryModel,
    DocumentInputSchemaRecordModel,
)
from asbp.document_input_schema_store import (
    get_document_input_schema_by_id,
    load_default_document_input_schema_library,
)
from asbp.document_template_model import (
    DocumentTemplateLibraryModel,
    DocumentTemplateRecordModel,
)
from asbp.document_template_store import (
    get_document_template_by_id,
    load_default_document_template_library,
)
from asbp.template_selection_model import TemplateSelectionResultModel


def resolve_document_input_schema_for_template(
    template: DocumentTemplateRecordModel,
    *,
    schema_library: DocumentInputSchemaLibraryModel | None = None,
) -> DocumentInputSchemaRecordModel:
    schema_library = schema_library or load_default_document_input_schema_library()

    if template.schema_binding_status != "schema_bound":
        raise ValueError(
            "Template record is not schema-bound for M29.4 input contract use: "
            f"{template.template_id}"
        )

    schema = get_document_input_schema_by_id(
        schema_library,
        template.schema_binding_ref,
    )
    assert_schema_matches_template(schema, template)
    return schema


def load_document_input_schema_for_template_id(
    template_id: str,
    *,
    template_library: DocumentTemplateLibraryModel | None = None,
    schema_library: DocumentInputSchemaLibraryModel | None = None,
) -> DocumentInputSchemaRecordModel:
    template_library = template_library or load_default_document_template_library()
    template = get_document_template_by_id(template_library, template_id)
    return resolve_document_input_schema_for_template(
        template,
        schema_library=schema_library,
    )


def load_document_input_schema_for_selection_result(
    selection_result: TemplateSelectionResultModel,
    *,
    template_library: DocumentTemplateLibraryModel | None = None,
    schema_library: DocumentInputSchemaLibraryModel | None = None,
) -> DocumentInputSchemaRecordModel:
    if selection_result.status != "selected" or selection_result.selected_template_id is None:
        raise ValueError(
            "Document input schema can only be resolved for a selected template: "
            f"{selection_result.status}"
        )

    return load_document_input_schema_for_template_id(
        selection_result.selected_template_id,
        template_library=template_library,
        schema_library=schema_library,
    )


def assert_schema_matches_template(
    schema: DocumentInputSchemaRecordModel,
    template: DocumentTemplateRecordModel,
) -> None:
    if schema.template_id != template.template_id:
        raise ValueError(
            "Document input schema template_id does not match template record: "
            f"{schema.schema_id} -> {schema.template_id} / {template.template_id}"
        )

    if schema.document_family_id != template.document_family_id:
        raise ValueError(
            "Document input schema family does not match template record: "
            f"{schema.schema_id} -> {schema.document_family_id} / "
            f"{template.document_family_id}"
        )

    if _normalize(schema.document_type) != _normalize(template.document_type):
        raise ValueError(
            "Document input schema document_type does not match template record: "
            f"{schema.schema_id} -> {schema.document_type} / {template.document_type}"
        )


def build_template_schema_binding_id(template_id: str, schema_id: str) -> str:
    return f"{template_id}::{schema_id}"


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())
