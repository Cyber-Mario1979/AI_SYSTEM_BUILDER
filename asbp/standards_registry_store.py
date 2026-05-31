from __future__ import annotations

import json
from pathlib import Path

from asbp.standards_registry_model import (
    StandardsAuthorityStatus,
    StandardsCitationDepth,
    StandardsRegistryModel,
    StandardsRegistrySourceRecordModel,
)


DEFAULT_STANDARDS_REGISTRY_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "standards_registry"
    / "standards_source_registry_v0_1.json"
)


def load_standards_registry_from_payload(payload: dict) -> StandardsRegistryModel:
    if "source_records" not in payload:
        raise ValueError("standards registry payload must include source_records")

    return StandardsRegistryModel(**payload)


def load_standards_registry_from_path(path: Path) -> StandardsRegistryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_standards_registry_from_payload(payload)


def load_default_standards_registry() -> StandardsRegistryModel:
    return load_standards_registry_from_path(DEFAULT_STANDARDS_REGISTRY_SOURCE_PATH)


def list_standard_source_ids(registry: StandardsRegistryModel) -> list[str]:
    return [source.std_id for source in registry.source_records]


def get_standard_source_by_id(
    registry: StandardsRegistryModel,
    std_id: str,
) -> StandardsRegistrySourceRecordModel:
    for source in registry.source_records:
        if source.std_id == std_id:
            return source

    raise ValueError(f"Standards registry source not found: {std_id}")


def list_limited_standard_source_ids(registry: StandardsRegistryModel) -> list[str]:
    return [
        source.std_id
        for source in registry.source_records
        if source.requires_visible_limitations()
    ]


def list_mandatory_eligible_standard_source_ids(
    registry: StandardsRegistryModel,
) -> list[str]:
    return [
        source.std_id
        for source in registry.source_records
        if source.can_support_mandatory_use()
    ]


def list_standard_source_ids_by_authority_status(
    registry: StandardsRegistryModel,
    authority_status: StandardsAuthorityStatus,
) -> list[str]:
    return [
        source.std_id
        for source in registry.source_records
        if source.authority_status == authority_status
    ]


def source_requires_visible_limitations(
    registry: StandardsRegistryModel,
    std_id: str,
) -> bool:
    source = get_standard_source_by_id(registry, std_id)
    return source.requires_visible_limitations()


def source_can_support_mandatory_use(
    registry: StandardsRegistryModel,
    std_id: str,
) -> bool:
    source = get_standard_source_by_id(registry, std_id)
    return source.can_support_mandatory_use()


def assert_source_can_support_mandatory_use(
    registry: StandardsRegistryModel,
    std_id: str,
) -> None:
    source = get_standard_source_by_id(registry, std_id)

    if source.can_support_mandatory_use():
        return

    raise ValueError(
        "Standards registry source cannot support mandatory use until authority, "
        f"verification, and mandatory flag limits are satisfied: {std_id}"
    )


def assert_citation_depth_allowed(
    registry: StandardsRegistryModel,
    std_id: str,
    citation_depth: StandardsCitationDepth,
) -> None:
    source = get_standard_source_by_id(registry, std_id)

    if citation_depth not in source.citation_depths:
        raise ValueError(
            "Citation depth is not available for standards registry source: "
            f"{std_id} -> {citation_depth}"
        )

    if citation_depth in {"section", "clause"} and source.verification_status != "verified":
        raise ValueError(
            "Section or clause citation depth requires verified source evidence: "
            f"{std_id}"
        )

    if (
        citation_depth == "version"
        and source.version_or_effective_date.strip().upper() == "TBD"
    ):
        raise ValueError(
            "Version-level citation requires known version or effective date: "
            f"{std_id}"
        )


def assert_registry_contains_standard_ids(
    registry: StandardsRegistryModel,
    required_standard_ids: set[str],
) -> None:
    registered_ids = set(list_standard_source_ids(registry))
    missing_ids = sorted(required_standard_ids - registered_ids)

    if missing_ids:
        raise ValueError(
            "Standards registry is missing required source IDs: "
            f"{', '.join(missing_ids)}"
        )
