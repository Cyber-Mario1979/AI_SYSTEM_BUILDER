from __future__ import annotations

import json
from pathlib import Path

from asbp.standards_document_applicability_model import (
    DocumentCitationPolicyLibraryModel,
    DocumentCitationPolicyRecordModel,
    DocumentStandardsApplicabilityMatrixModel,
    DocumentStandardsApplicabilityRecordModel,
)


DEFAULT_DOCUMENT_STANDARDS_APPLICABILITY_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "standards_applicability"
    / "mvp_document_standards_applicability_matrix.json"
)

DEFAULT_DOCUMENT_CITATION_POLICY_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "standards_citation"
    / "mvp_document_citation_policy.json"
)


def load_document_standards_applicability_matrix_from_payload(
    payload: dict,
) -> DocumentStandardsApplicabilityMatrixModel:
    if "document_records" not in payload:
        raise ValueError(
            "document standards applicability matrix payload must include "
            "document_records"
        )
    return DocumentStandardsApplicabilityMatrixModel(**payload)


def load_document_standards_applicability_matrix_from_path(
    path: Path,
) -> DocumentStandardsApplicabilityMatrixModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_document_standards_applicability_matrix_from_payload(payload)


def load_default_document_standards_applicability_matrix() -> (
    DocumentStandardsApplicabilityMatrixModel
):
    return load_document_standards_applicability_matrix_from_path(
        DEFAULT_DOCUMENT_STANDARDS_APPLICABILITY_PATH
    )


def list_document_standards_applicability_refs(
    matrix: DocumentStandardsApplicabilityMatrixModel,
) -> list[str]:
    return [record.document_ref for record in matrix.document_records]


def get_document_standards_applicability_by_ref(
    matrix: DocumentStandardsApplicabilityMatrixModel,
    document_ref: str,
) -> DocumentStandardsApplicabilityRecordModel:
    for record in matrix.document_records:
        if record.document_ref == document_ref:
            return record

    raise ValueError(
        f"Document standards applicability record not found: {document_ref}"
    )


def assert_document_standards_applicability_refs_exist(
    matrix: DocumentStandardsApplicabilityMatrixModel,
    required_document_refs: set[str],
) -> None:
    existing_refs = set(list_document_standards_applicability_refs(matrix))
    missing_refs = sorted(required_document_refs - existing_refs)
    if missing_refs:
        raise ValueError(
            "Document standards applicability refs not found: "
            f"{', '.join(missing_refs)}"
        )


def load_document_citation_policy_library_from_payload(
    payload: dict,
) -> DocumentCitationPolicyLibraryModel:
    if "policies" not in payload:
        raise ValueError("document citation policy payload must include policies")
    return DocumentCitationPolicyLibraryModel(**payload)


def load_document_citation_policy_library_from_path(
    path: Path,
) -> DocumentCitationPolicyLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_document_citation_policy_library_from_payload(payload)


def load_default_document_citation_policy_library() -> (
    DocumentCitationPolicyLibraryModel
):
    return load_document_citation_policy_library_from_path(
        DEFAULT_DOCUMENT_CITATION_POLICY_PATH
    )


def list_document_citation_policy_refs(
    library: DocumentCitationPolicyLibraryModel,
) -> list[str]:
    return [policy.document_ref for policy in library.policies]


def get_document_citation_policy_by_ref(
    library: DocumentCitationPolicyLibraryModel,
    document_ref: str,
) -> DocumentCitationPolicyRecordModel:
    for policy in library.policies:
        if policy.document_ref == document_ref:
            return policy

    raise ValueError(f"Document citation policy record not found: {document_ref}")


def assert_document_citation_policy_refs_exist(
    library: DocumentCitationPolicyLibraryModel,
    required_document_refs: set[str],
) -> None:
    existing_refs = set(list_document_citation_policy_refs(library))
    missing_refs = sorted(required_document_refs - existing_refs)
    if missing_refs:
        raise ValueError(
            "Document citation policy refs not found: "
            f"{', '.join(missing_refs)}"
        )
