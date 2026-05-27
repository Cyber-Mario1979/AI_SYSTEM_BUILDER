from __future__ import annotations

import json
from pathlib import Path

from asbp.calendar_source_store import (
    list_calendar_ids,
    load_default_calendar_library,
)
from asbp.mapping_source_store import (
    assert_resolved_references_exist,
    load_default_mapping_library,
)
from asbp.planning_basis_source_store import (
    assert_task_pool_duration_refs_covered,
    load_default_planning_basis_library,
)
from asbp.profile_source_store import (
    list_profile_ids,
    load_default_profile_library,
)
from asbp.source_library_baseline_model import (
    SourceLibraryBaselineModel,
    SourceLibraryBaselineRuntimeModel,
)
from asbp.task_pool_source_store import (
    list_task_pool_ids,
    load_default_task_pool_library,
)


DEFAULT_SOURCE_LIBRARY_BASELINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "library_baseline"
    / "m27_library_baseline.json"
)


def load_source_library_baseline_from_payload(
    payload: dict,
) -> SourceLibraryBaselineModel:
    if "source_families" not in payload:
        raise ValueError("source-library baseline payload must include source_families")

    return SourceLibraryBaselineModel(**payload)


def load_source_library_baseline_from_path(
    path: Path,
) -> SourceLibraryBaselineModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_source_library_baseline_from_payload(payload)


def load_default_source_library_baseline() -> SourceLibraryBaselineModel:
    return load_source_library_baseline_from_path(
        DEFAULT_SOURCE_LIBRARY_BASELINE_PATH,
    )


def load_default_source_library_baseline_runtime() -> (
    SourceLibraryBaselineRuntimeModel
):
    baseline = load_default_source_library_baseline()
    task_pool_library = load_default_task_pool_library()
    profile_library = load_default_profile_library()
    calendar_library = load_default_calendar_library()
    planning_basis_library = load_default_planning_basis_library()
    mapping_library = load_default_mapping_library()

    runtime = SourceLibraryBaselineRuntimeModel(
        baseline=baseline,
        task_pool_library=task_pool_library,
        profile_library=profile_library,
        calendar_library=calendar_library,
        planning_basis_library=planning_basis_library,
        mapping_library=mapping_library,
    )

    validate_source_library_baseline_runtime(runtime)

    return runtime


def list_source_family_ids(baseline: SourceLibraryBaselineModel) -> list[str]:
    return [source_family.family_id for source_family in baseline.source_families]


def get_source_family_by_id(
    baseline: SourceLibraryBaselineModel,
    family_id: str,
):
    for source_family in baseline.source_families:
        if source_family.family_id == family_id:
            return source_family

    raise ValueError(f"Source family baseline definition not found: {family_id}")


def build_source_family_definition_id(
    baseline_id: str,
    family_id: str,
) -> str:
    return f"{baseline_id}::{family_id}"


def summarize_source_library_baseline(
    runtime: SourceLibraryBaselineRuntimeModel,
) -> dict:
    return {
        "baseline_id": runtime.baseline.baseline_id,
        "source_families": list_source_family_ids(runtime.baseline),
        "task_pool_count": len(runtime.task_pool_library.task_pools),
        "profile_count": len(runtime.profile_library.profiles),
        "calendar_count": len(runtime.calendar_library.calendars),
        "duration_source_count": len(
            runtime.planning_basis_library.duration_sources,
        ),
        "mapping_count": len(runtime.mapping_library.mappings),
    }


def validate_source_library_baseline_runtime(
    runtime: SourceLibraryBaselineRuntimeModel,
) -> None:
    _validate_manifest_library_ids(runtime)
    assert_task_pool_duration_refs_covered(
        runtime.planning_basis_library,
        runtime.task_pool_library,
    )
    assert_resolved_references_exist(
        runtime.mapping_library,
        "profile",
        set(list_profile_ids(runtime.profile_library)),
    )
    assert_resolved_references_exist(
        runtime.mapping_library,
        "task_pool",
        set(list_task_pool_ids(runtime.task_pool_library)),
    )

    # Calendar IDs are not yet mapped to selectors. They are loaded here as
    # part of the M27.8 controlled baseline and validated more broadly during
    # M27.9 cross-library validation.
    if not list_calendar_ids(runtime.calendar_library):
        raise ValueError("M27.8 baseline calendar library is empty")


def _validate_manifest_library_ids(
    runtime: SourceLibraryBaselineRuntimeModel,
) -> None:
    expected_library_ids = {
        "task_pools": runtime.task_pool_library.library_id,
        "profiles": runtime.profile_library.library_id,
        "calendars": runtime.calendar_library.library_id,
        "planning_basis": runtime.planning_basis_library.library_id,
        "mappings": runtime.mapping_library.library_id,
    }

    for source_family in runtime.baseline.source_families:
        actual_library_id = expected_library_ids[source_family.family_id]
        if source_family.library_id != actual_library_id:
            raise ValueError(
                "Source library baseline family library_id mismatch: "
                f"{source_family.family_id} expected "
                f"{source_family.library_id}, got {actual_library_id}"
            )
