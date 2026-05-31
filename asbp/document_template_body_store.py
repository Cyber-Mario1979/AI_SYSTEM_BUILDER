from __future__ import annotations

import json
from pathlib import Path

from asbp.document_template_body_model import (
    DocumentTemplateBodyLibraryModel,
    DocumentTemplateBodyRecordModel,
    TemplateBodyOutputRole,
)


DEFAULT_DOCUMENT_TEMPLATE_BODY_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "document_template_bodies"
    / "mvp_document_template_bodies.json"
)


MVP_MUST_HAVE_DOCUMENT_REFS = {
    "CCF",
    "VMP",
    "SIA",
    "URS",
    "VENDOR_DOC_EXTRACTION_SOURCE",
    "RA_FMEA",
    "URS_DEVIATION_LIST",
    "RTM",
    "DQ",
    "CP",
    "QP",
    "FAT_PROTOCOL_REPORT",
    "A0_CERTIFICATE",
    "CTOP",
    "A1_CERTIFICATE",
    "SAT_PROTOCOL_REPORT",
    "CR",
    "A2_CERTIFICATE",
    "IQ_PROTOCOL_REPORT",
    "OQ_PROTOCOL_REPORT",
    "PQ_PROTOCOL_REPORT",
    "DEVIATION_INCIDENT_REPORT",
    "CAPA_CLOSURE_FORM",
    "VSR",
    "DECOMMISSIONING_DOCUMENT_SET",
}


def load_document_template_body_library_from_payload(
    payload: dict,
) -> DocumentTemplateBodyLibraryModel:
    if "body_records" not in payload:
        raise ValueError(
            "document template body library payload must include body_records"
        )

    return DocumentTemplateBodyLibraryModel(**payload)


def load_document_template_body_library_from_path(
    path: Path,
) -> DocumentTemplateBodyLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_document_template_body_library_from_payload(payload)


def load_default_document_template_body_library() -> DocumentTemplateBodyLibraryModel:
    return load_document_template_body_library_from_path(
        DEFAULT_DOCUMENT_TEMPLATE_BODY_SOURCE_PATH,
    )


def list_document_template_body_ids(
    library: DocumentTemplateBodyLibraryModel,
) -> list[str]:
    return [body_record.body_id for body_record in library.body_records]


def list_document_template_body_document_refs(
    library: DocumentTemplateBodyLibraryModel,
) -> list[str]:
    return [body_record.document_ref for body_record in library.body_records]


def get_document_template_body_by_ref(
    library: DocumentTemplateBodyLibraryModel,
    document_ref: str,
) -> DocumentTemplateBodyRecordModel:
    for body_record in library.body_records:
        if body_record.document_ref == document_ref:
            return body_record

    raise ValueError(f"Document template body source record not found: {document_ref}")


def list_document_template_bodies_by_output_role(
    library: DocumentTemplateBodyLibraryModel,
    output_role: TemplateBodyOutputRole,
) -> list[DocumentTemplateBodyRecordModel]:
    return [
        body_record
        for body_record in library.body_records
        if body_record.output_role == output_role
    ]


def find_missing_document_template_body_refs(
    library: DocumentTemplateBodyLibraryModel,
    required_document_refs: set[str],
) -> list[str]:
    registered_document_refs = set(list_document_template_body_document_refs(library))
    return sorted(required_document_refs - registered_document_refs)


def assert_document_template_body_refs_exist(
    library: DocumentTemplateBodyLibraryModel,
    required_document_refs: set[str],
) -> None:
    missing_refs = find_missing_document_template_body_refs(
        library,
        required_document_refs,
    )
    if missing_refs:
        joined_missing_refs = ", ".join(missing_refs)
        raise ValueError(
            "Document template body source records not found: "
            f"{joined_missing_refs}"
        )


def assert_mvp_document_template_body_coverage(
    library: DocumentTemplateBodyLibraryModel,
) -> None:
    assert_document_template_body_refs_exist(
        library,
        MVP_MUST_HAVE_DOCUMENT_REFS,
    )
