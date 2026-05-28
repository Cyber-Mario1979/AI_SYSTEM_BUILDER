from __future__ import annotations

import json
from pathlib import Path

from asbp.standards_bundle_binding_model import (
    StandardsBundleBindingLibraryModel,
    StandardsBundleBindingModel,
    StandardsBundleConsumerType,
)


DEFAULT_STANDARDS_BUNDLE_BINDING_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "standards_bundles"
    / "starter_standards_bundle_bindings.json"
)


def load_standards_bundle_binding_library_from_payload(
    payload: dict,
) -> StandardsBundleBindingLibraryModel:
    if "bindings" not in payload:
        raise ValueError("standards bundle binding library payload must include bindings")

    return StandardsBundleBindingLibraryModel(**payload)


def load_standards_bundle_binding_library_from_path(
    path: Path,
) -> StandardsBundleBindingLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_standards_bundle_binding_library_from_payload(payload)


def load_default_standards_bundle_binding_library() -> (
    StandardsBundleBindingLibraryModel
):
    return load_standards_bundle_binding_library_from_path(
        DEFAULT_STANDARDS_BUNDLE_BINDING_SOURCE_PATH
    )


def list_standards_bundle_ids(
    library: StandardsBundleBindingLibraryModel,
) -> list[str]:
    return [binding.bundle_id for binding in library.bindings]


def get_standards_bundle_binding_by_id(
    library: StandardsBundleBindingLibraryModel,
    bundle_id: str,
) -> StandardsBundleBindingModel:
    for binding in library.bindings:
        if binding.bundle_id == bundle_id:
            return binding

    raise ValueError(f"Standards bundle binding not found: {bundle_id}")


def list_standard_ids_for_bundle(
    library: StandardsBundleBindingLibraryModel,
    bundle_id: str,
) -> list[str]:
    binding = get_standards_bundle_binding_by_id(library, bundle_id)
    return [source.std_id for source in binding.source_bindings]


def collect_downstream_consumer_ids_by_type(
    library: StandardsBundleBindingLibraryModel,
    consumer_type: StandardsBundleConsumerType,
) -> set[str]:
    consumer_ids: set[str] = set()

    for binding in library.bindings:
        for consumer in binding.downstream_consumers:
            if consumer.consumer_type == consumer_type:
                consumer_ids.add(consumer.consumer_id)

    return consumer_ids


def find_missing_downstream_consumer_ids(
    library: StandardsBundleBindingLibraryModel,
    consumer_type: StandardsBundleConsumerType,
    known_consumer_ids: set[str],
) -> list[str]:
    mapped_consumer_ids = collect_downstream_consumer_ids_by_type(
        library,
        consumer_type,
    )
    return sorted(mapped_consumer_ids - known_consumer_ids)


def assert_downstream_consumers_exist(
    library: StandardsBundleBindingLibraryModel,
    consumer_type: StandardsBundleConsumerType,
    known_consumer_ids: set[str],
) -> None:
    missing_consumer_ids = find_missing_downstream_consumer_ids(
        library,
        consumer_type,
        known_consumer_ids,
    )
    if missing_consumer_ids:
        joined_missing_ids = ", ".join(missing_consumer_ids)
        raise ValueError(
            f"Standards bundle downstream consumers unresolved {consumer_type} IDs: "
            f"{joined_missing_ids}"
        )
