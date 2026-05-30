from __future__ import annotations

import json
from pathlib import Path

from asbp.controlled_drafting_model import (
    ControlledDraftingLibraryModel,
    ControlledDraftingMode,
    ControlledDraftingModeDefinitionModel,
)


DEFAULT_CONTROLLED_DRAFTING_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "controlled_drafting"
    / "starter_controlled_drafting_modes.json"
)


def load_controlled_drafting_library_from_payload(
    payload: dict,
) -> ControlledDraftingLibraryModel:
    if "drafting_modes" not in payload:
        raise ValueError("controlled drafting library payload must include drafting_modes")

    return ControlledDraftingLibraryModel(**payload)


def load_controlled_drafting_library_from_path(
    path: Path,
) -> ControlledDraftingLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_controlled_drafting_library_from_payload(payload)


def load_default_controlled_drafting_library() -> ControlledDraftingLibraryModel:
    return load_controlled_drafting_library_from_path(DEFAULT_CONTROLLED_DRAFTING_SOURCE_PATH)


def list_controlled_drafting_mode_ids(
    library: ControlledDraftingLibraryModel,
) -> list[str]:
    return [mode.drafting_mode_id for mode in library.drafting_modes]


def get_controlled_drafting_mode_by_id(
    library: ControlledDraftingLibraryModel,
    drafting_mode_id: str,
) -> ControlledDraftingModeDefinitionModel:
    for mode in library.drafting_modes:
        if mode.drafting_mode_id == drafting_mode_id:
            return mode

    raise ValueError(f"Controlled drafting mode source record not found: {drafting_mode_id}")


def get_controlled_drafting_mode_by_mode(
    library: ControlledDraftingLibraryModel,
    drafting_mode: ControlledDraftingMode,
) -> ControlledDraftingModeDefinitionModel:
    for mode in library.drafting_modes:
        if mode.drafting_mode == drafting_mode:
            return mode

    raise ValueError(f"Controlled drafting mode source record not found: {drafting_mode}")


def assert_controlled_drafting_modes_exist(
    library: ControlledDraftingLibraryModel,
    required_mode_ids: set[str],
) -> None:
    registered_mode_ids = set(list_controlled_drafting_mode_ids(library))
    missing_mode_ids = sorted(required_mode_ids - registered_mode_ids)
    if missing_mode_ids:
        joined_missing_ids = ", ".join(missing_mode_ids)
        raise ValueError(f"Controlled drafting mode source records not found: {joined_missing_ids}")


def assert_drafting_mode_supports_template_and_schema(
    mode: ControlledDraftingModeDefinitionModel,
    template_id: str,
    schema_id: str,
) -> None:
    if template_id not in mode.supported_template_ids:
        raise ValueError(
            "Controlled drafting mode does not support template: "
            f"{mode.drafting_mode_id} -> {template_id}"
        )

    if schema_id not in mode.supported_schema_ids:
        raise ValueError(
            "Controlled drafting mode does not support schema: "
            f"{mode.drafting_mode_id} -> {schema_id}"
        )
