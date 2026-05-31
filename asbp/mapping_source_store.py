from __future__ import annotations

import json
from pathlib import Path

from asbp.mapping_source_model import MappingKind, MappingLibraryModel, MappingSourceModel, ReferenceType


MAPPING_SOURCE_DIR = Path(__file__).resolve().parents[1] / "data" / "source" / "mappings"
DEFAULT_MAPPING_SOURCE_PATH = MAPPING_SOURCE_DIR / "starter_mappings.json"
MVP_MAPPING_SOURCE_PATH = MAPPING_SOURCE_DIR / "mvp_mappings.json"


def load_mapping_library_from_payload(payload: dict) -> MappingLibraryModel:
    if "mappings" not in payload:
        raise ValueError("mapping library payload must include mappings")
    return MappingLibraryModel(**payload)


def load_mapping_library_from_path(path: Path) -> MappingLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return load_mapping_library_from_payload(payload)


def load_default_mapping_library() -> MappingLibraryModel:
    return load_mapping_library_from_path(DEFAULT_MAPPING_SOURCE_PATH)


def load_mvp_mapping_library() -> MappingLibraryModel:
    return load_mapping_library_from_path(MVP_MAPPING_SOURCE_PATH)


def list_mapping_ids(library: MappingLibraryModel) -> list[str]:
    return [mapping.mapping_id for mapping in library.mappings]


def get_mapping_by_id(library: MappingLibraryModel, mapping_id: str) -> MappingSourceModel:
    for mapping in library.mappings:
        if mapping.mapping_id == mapping_id:
            return mapping
    raise ValueError(f"Mapping source definition not found: {mapping_id}")


def list_mappings_by_kind(library: MappingLibraryModel, mapping_kind: MappingKind) -> list[MappingSourceModel]:
    return [mapping for mapping in library.mappings if mapping.mapping_kind == mapping_kind]


def collect_resolved_reference_ids_by_type(library: MappingLibraryModel, reference_type: ReferenceType) -> set[str]:
    reference_ids: set[str] = set()
    for mapping in library.mappings:
        for reference in [*mapping.source_refs, *mapping.target_refs]:
            if reference.reference_type == reference_type and reference.reference_status == "resolved_source":
                reference_ids.add(reference.reference_id)
    return reference_ids


def find_missing_resolved_reference_ids(library: MappingLibraryModel, reference_type: ReferenceType, known_reference_ids: set[str]) -> list[str]:
    mapped_reference_ids = collect_resolved_reference_ids_by_type(library, reference_type)
    return sorted(mapped_reference_ids - known_reference_ids)


def assert_resolved_references_exist(library: MappingLibraryModel, reference_type: ReferenceType, known_reference_ids: set[str]) -> None:
    missing_reference_ids = find_missing_resolved_reference_ids(library, reference_type, known_reference_ids)
    if missing_reference_ids:
        joined_missing_ids = ", ".join(missing_reference_ids)
        raise ValueError(f"Mapping references unresolved {reference_type} IDs: {joined_missing_ids}")


def build_mapping_reference_definition_id(mapping_id: str, reference_type: ReferenceType, reference_id: str) -> str:
    return f"{mapping_id}::{reference_type}::{reference_id}"
