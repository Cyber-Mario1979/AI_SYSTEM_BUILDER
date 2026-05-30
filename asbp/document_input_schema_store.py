from __future__ import annotations

import json
from pathlib import Path

from asbp.document_input_schema_model import (
    DocumentInputSchemaLibraryModel,
    DocumentInputSchemaRecordModel,
)


DEFAULT_DOCUMENT_INPUT_SCHEMA_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "document_input_schemas"
    / "starter_document_input_schemas.json"
)


def load_document_input_schema_library_from_payload(
    payload: dict,
) -> DocumentInputSchemaLibraryModel:
    if "schema_records" not in payload:
        raise ValueError("document input schema library payload must include schema_records")

    return DocumentInputSchemaLibraryModel(**payload)


def load_document_input_schema_library_from_path(
    path: Path,
) -> DocumentInputSchemaLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_document_input_schema_library_from_payload(payload)


def load_default_document_input_schema_library() -> DocumentInputSchemaLibraryModel:
    return load_document_input_schema_library_from_path(
        DEFAULT_DOCUMENT_INPUT_SCHEMA_SOURCE_PATH,
    )


def list_document_input_schema_ids(
    library: DocumentInputSchemaLibraryModel,
) -> list[str]:
    return [schema.schema_id for schema in library.schema_records]


def get_document_input_schema_by_id(
    library: DocumentInputSchemaLibraryModel,
    schema_id: str,
) -> DocumentInputSchemaRecordModel:
    for schema in library.schema_records:
        if schema.schema_id == schema_id:
            return schema

    raise ValueError(f"Document input schema source record not found: {schema_id}")


def list_document_input_schema_ids_by_template(
    library: DocumentInputSchemaLibraryModel,
    template_id: str,
) -> list[str]:
    return [
        schema.schema_id
        for schema in library.schema_records
        if schema.template_id == template_id
    ]


def get_document_input_schema_by_template_id(
    library: DocumentInputSchemaLibraryModel,
    template_id: str,
) -> DocumentInputSchemaRecordModel:
    matched_schemas = [
        schema
        for schema in library.schema_records
        if schema.template_id == template_id
    ]

    if len(matched_schemas) == 1:
        return matched_schemas[0]

    if not matched_schemas:
        raise ValueError(
            "Document input schema source record not found for template: "
            f"{template_id}"
        )

    raise ValueError(
        "Multiple document input schema records found for template: "
        f"{template_id}"
    )


def find_missing_document_input_schema_ids(
    library: DocumentInputSchemaLibraryModel,
    required_schema_ids: set[str],
) -> list[str]:
    registered_schema_ids = set(list_document_input_schema_ids(library))
    return sorted(required_schema_ids - registered_schema_ids)


def assert_document_input_schemas_exist(
    library: DocumentInputSchemaLibraryModel,
    required_schema_ids: set[str],
) -> None:
    missing_schema_ids = find_missing_document_input_schema_ids(
        library,
        required_schema_ids,
    )

    if missing_schema_ids:
        joined_missing_ids = ", ".join(missing_schema_ids)
        raise ValueError(
            "Document input schema source records not found: "
            f"{joined_missing_ids}"
        )
