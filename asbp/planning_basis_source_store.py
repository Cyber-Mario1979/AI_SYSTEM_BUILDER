from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from asbp.planning_basis_source_model import (
    DurationSourceModel,
    PlanningBasisLibraryModel,
    collect_planning_basis_duration_refs,
    collect_task_pool_duration_refs,
)


DEFAULT_PLANNING_BASIS_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "planning_basis"
    / "starter_planning_basis.json"
)


def load_planning_basis_library_from_payload(
    payload: dict,
) -> PlanningBasisLibraryModel:
    if "duration_sources" not in payload:
        raise ValueError(
            "planning-basis library payload must include duration_sources"
        )

    return PlanningBasisLibraryModel(**payload)


def load_planning_basis_library_from_path(path: Path) -> PlanningBasisLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_planning_basis_library_from_payload(payload)


def load_default_planning_basis_library() -> PlanningBasisLibraryModel:
    return load_planning_basis_library_from_path(DEFAULT_PLANNING_BASIS_SOURCE_PATH)


def list_duration_ref_ids(library: PlanningBasisLibraryModel) -> list[str]:
    return [
        duration_source.duration_ref_id
        for duration_source in library.duration_sources
    ]


def get_duration_source_by_ref_id(
    library: PlanningBasisLibraryModel,
    duration_ref_id: str,
) -> DurationSourceModel:
    for duration_source in library.duration_sources:
        if duration_source.duration_ref_id == duration_ref_id:
            return duration_source

    raise ValueError(
        f"Duration source definition not found: {duration_ref_id}"
    )


def find_missing_task_pool_duration_refs(
    planning_basis_library: PlanningBasisLibraryModel,
    task_pool_library: Any,
) -> list[str]:
    task_pool_refs = collect_task_pool_duration_refs(task_pool_library)
    planning_basis_refs = collect_planning_basis_duration_refs(
        planning_basis_library,
    )

    return sorted(task_pool_refs - planning_basis_refs)


def assert_task_pool_duration_refs_covered(
    planning_basis_library: PlanningBasisLibraryModel,
    task_pool_library: Any,
) -> None:
    missing_refs = find_missing_task_pool_duration_refs(
        planning_basis_library,
        task_pool_library,
    )
    if missing_refs:
        joined_missing_refs = ", ".join(missing_refs)
        raise ValueError(
            "Planning-basis duration sources do not cover task-pool "
            f"duration refs: {joined_missing_refs}"
        )


def build_duration_source_definition_id(duration_ref_id: str) -> str:
    return f"M27.6::{duration_ref_id}"
