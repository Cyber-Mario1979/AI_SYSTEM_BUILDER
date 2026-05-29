from __future__ import annotations

import json
from pathlib import Path

from asbp.document_template_model import (
    DocumentTemplateLibraryModel,
    DocumentTemplateRecordModel,
)


DEFAULT_DOCUMENT_TEMPLATE_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "document_templates"
    / "starter_document_templates.json"
)


def load_document_template_library_from_payload(
    payload: dict,
) -> DocumentTemplateLibraryModel:
    if "template_records" not in payload:
        raise ValueError("document template library payload must include template_records")

    return DocumentTemplateLibraryModel(**payload)


def load_document_template_library_from_path(
    path: Path,
) -> DocumentTemplateLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_document_template_library_from_payload(payload)


def load_default_document_template_library() -> DocumentTemplateLibraryModel:
    return load_document_template_library_from_path(DEFAULT_DOCUMENT_TEMPLATE_SOURCE_PATH)


def list_document_template_ids(
    library: DocumentTemplateLibraryModel,
) -> list[str]:
    return [template.template_id for template in library.template_records]


def get_document_template_by_id(
    library: DocumentTemplateLibraryModel,
    template_id: str,
) -> DocumentTemplateRecordModel:
    for template in library.template_records:
        if template.template_id == template_id:
            return template

    raise ValueError(f"Document template source record not found: {template_id}")


def list_document_template_ids_by_family(
    library: DocumentTemplateLibraryModel,
    document_family_id: str,
) -> list[str]:
    return [
        template.template_id
        for template in library.template_records
        if template.document_family_id == document_family_id
    ]


def find_missing_document_template_ids(
    library: DocumentTemplateLibraryModel,
    required_template_ids: set[str],
) -> list[str]:
    registered_template_ids = set(list_document_template_ids(library))
    return sorted(required_template_ids - registered_template_ids)


def assert_document_templates_exist(
    library: DocumentTemplateLibraryModel,
    required_template_ids: set[str],
) -> None:
    missing_template_ids = find_missing_document_template_ids(
        library,
        required_template_ids,
    )

    if missing_template_ids:
        joined_missing_ids = ", ".join(missing_template_ids)
        raise ValueError(f"Document template source records not found: {joined_missing_ids}")


def assert_template_supports_standards_bundle(
    library: DocumentTemplateLibraryModel,
    template_id: str,
    standards_bundle_ref: str,
) -> None:
    template = get_document_template_by_id(library, template_id)

    if standards_bundle_ref in template.standards_bundle_refs:
        return

    raise ValueError(
        "Document template source record does not include standards bundle ref: "
        f"{template_id} -> {standards_bundle_ref}"
    )
