from __future__ import annotations

import json
from pathlib import Path

from asbp.document_input_dependency_model import (
    DocumentDependencyContractLibraryModel,
    DocumentDependencyContractModel,
    UrsDcfIntakeCatalogModel,
    UrsDcfIntakeRecordModel,
    VendorDocumentExtractionLibraryModel,
    VendorDocumentExtractionSourceModel,
)

BASE_DOCUMENT_INPUT_CONTRACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "document_input_schemas"
)
DEFAULT_URS_DCF_INTAKE_CATALOG_PATH = (
    BASE_DOCUMENT_INPUT_CONTRACT_PATH / "mvp_urs_dcf_intake_catalog.json"
)
DEFAULT_DOCUMENT_DEPENDENCY_CONTRACTS_PATH = (
    BASE_DOCUMENT_INPUT_CONTRACT_PATH / "mvp_downstream_document_dependency_contracts.json"
)
DEFAULT_VENDOR_DOCUMENT_EXTRACTION_PATH = (
    BASE_DOCUMENT_INPUT_CONTRACT_PATH / "mvp_vendor_document_extraction_sources.json"
)


def _load_payload_from_path(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_urs_dcf_intake_catalog_from_payload(payload: dict) -> UrsDcfIntakeCatalogModel:
    if "dcf_records" not in payload:
        raise ValueError("URS DCF intake catalog payload must include dcf_records")
    return UrsDcfIntakeCatalogModel(**payload)


def load_urs_dcf_intake_catalog_from_path(path: Path) -> UrsDcfIntakeCatalogModel:
    return load_urs_dcf_intake_catalog_from_payload(_load_payload_from_path(path))


def load_default_urs_dcf_intake_catalog() -> UrsDcfIntakeCatalogModel:
    return load_urs_dcf_intake_catalog_from_path(DEFAULT_URS_DCF_INTAKE_CATALOG_PATH)


def list_urs_dcf_ids(catalog: UrsDcfIntakeCatalogModel) -> list[str]:
    return [record.dcf_id for record in catalog.dcf_records]


def get_urs_dcf_by_domain(
    catalog: UrsDcfIntakeCatalogModel,
    domain: str,
) -> UrsDcfIntakeRecordModel:
    for record in catalog.dcf_records:
        if record.domain == domain:
            return record
    raise ValueError(f"URS DCF intake record not found for domain: {domain}")


def get_urs_dcf_by_id(
    catalog: UrsDcfIntakeCatalogModel,
    dcf_id: str,
) -> UrsDcfIntakeRecordModel:
    for record in catalog.dcf_records:
        if record.dcf_id == dcf_id:
            return record
    raise ValueError(f"URS DCF intake record not found: {dcf_id}")


def load_document_dependency_contract_library_from_payload(
    payload: dict,
) -> DocumentDependencyContractLibraryModel:
    if "dependency_contracts" not in payload:
        raise ValueError(
            "document dependency contract library payload must include "
            "dependency_contracts"
        )
    return DocumentDependencyContractLibraryModel(**payload)


def load_document_dependency_contract_library_from_path(
    path: Path,
) -> DocumentDependencyContractLibraryModel:
    return load_document_dependency_contract_library_from_payload(
        _load_payload_from_path(path)
    )


def load_default_document_dependency_contract_library() -> (
    DocumentDependencyContractLibraryModel
):
    return load_document_dependency_contract_library_from_path(
        DEFAULT_DOCUMENT_DEPENDENCY_CONTRACTS_PATH
    )


def list_document_dependency_refs(
    library: DocumentDependencyContractLibraryModel,
) -> list[str]:
    return [contract.document_ref for contract in library.dependency_contracts]


def get_document_dependency_contract_by_ref(
    library: DocumentDependencyContractLibraryModel,
    document_ref: str,
) -> DocumentDependencyContractModel:
    for contract in library.dependency_contracts:
        if contract.document_ref == document_ref:
            return contract
    raise ValueError(f"Document dependency contract not found: {document_ref}")


def load_vendor_document_extraction_library_from_payload(
    payload: dict,
) -> VendorDocumentExtractionLibraryModel:
    if "vendor_sources" not in payload:
        raise ValueError("vendor document extraction payload must include vendor_sources")
    return VendorDocumentExtractionLibraryModel(**payload)


def load_vendor_document_extraction_library_from_path(
    path: Path,
) -> VendorDocumentExtractionLibraryModel:
    return load_vendor_document_extraction_library_from_payload(
        _load_payload_from_path(path)
    )


def load_default_vendor_document_extraction_library() -> (
    VendorDocumentExtractionLibraryModel
):
    return load_vendor_document_extraction_library_from_path(
        DEFAULT_VENDOR_DOCUMENT_EXTRACTION_PATH
    )


def list_vendor_document_source_ids(
    library: VendorDocumentExtractionLibraryModel,
) -> list[str]:
    return [source.source_id for source in library.vendor_sources]


def get_vendor_document_source_by_id(
    library: VendorDocumentExtractionLibraryModel,
    source_id: str,
) -> VendorDocumentExtractionSourceModel:
    for source in library.vendor_sources:
        if source.source_id == source_id:
            return source
    raise ValueError(f"Vendor document extraction source not found: {source_id}")
