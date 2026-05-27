from copy import deepcopy
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from asbp.source_library_baseline_model import SourceLibraryBaselineModel
from asbp.source_library_baseline_store import (
    build_source_family_definition_id,
    get_source_family_by_id,
    list_source_family_ids,
    load_default_source_library_baseline,
    load_default_source_library_baseline_runtime,
    load_source_library_baseline_from_payload,
    summarize_source_library_baseline,
)


def _minimal_baseline_payload() -> dict:
    return {
        "baseline_id": "M27_LIBRARY_CONTENT_BASELINE_WAVE_1@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "display_name": "Test baseline",
        "source_families": [
            {
                "family_id": "task_pools",
                "library_id": "M27_TASK_POOL_STARTER_LIBRARY@v1",
                "expected_status": "starter_runtime_source",
                "source_path": "data/source/task_pools/starter_task_pools.json",
                "implementation_checkpoint": "M27.3",
            },
            {
                "family_id": "profiles",
                "library_id": "M27_PROFILE_STARTER_LIBRARY@v1",
                "expected_status": "starter_runtime_source",
                "source_path": "data/source/profiles/starter_profiles.json",
                "implementation_checkpoint": "M27.4",
            },
            {
                "family_id": "calendars",
                "library_id": "M27_CALENDAR_STARTER_LIBRARY@v1",
                "expected_status": "starter_runtime_source",
                "source_path": "data/source/calendars/starter_calendars.json",
                "implementation_checkpoint": "M27.5",
            },
            {
                "family_id": "planning_basis",
                "library_id": "M27_PLANNING_BASIS_STARTER_LIBRARY@v1",
                "expected_status": "starter_runtime_source",
                "source_path": "data/source/planning_basis/starter_planning_basis.json",
                "implementation_checkpoint": "M27.6",
            },
            {
                "family_id": "mappings",
                "library_id": "M27_MAPPING_STARTER_LIBRARY@v1",
                "expected_status": "starter_runtime_source",
                "source_path": "data/source/mappings/starter_mappings.json",
                "implementation_checkpoint": "M27.7",
            },
        ],
        "integration_controls": [
            "M27.8 integrates the controlled starter source-library baseline."
        ],
    }


def test_default_source_library_baseline_manifest_loads_expected_families():
    baseline = load_default_source_library_baseline()

    assert baseline.baseline_id == "M27_LIBRARY_CONTENT_BASELINE_WAVE_1@v1"
    assert list_source_family_ids(baseline) == [
        "task_pools",
        "profiles",
        "calendars",
        "planning_basis",
        "mappings",
    ]

    mapping_family = get_source_family_by_id(baseline, "mappings")
    assert mapping_family.library_id == "M27_MAPPING_STARTER_LIBRARY@v1"


def test_default_source_library_baseline_runtime_loads_all_m27_families():
    runtime = load_default_source_library_baseline_runtime()
    summary = summarize_source_library_baseline(runtime)

    assert summary["baseline_id"] == "M27_LIBRARY_CONTENT_BASELINE_WAVE_1@v1"
    assert summary["task_pool_count"] == 6
    assert summary["profile_count"] == 7
    assert summary["calendar_count"] == 5
    assert summary["duration_source_count"] == 36
    assert summary["mapping_count"] == 20


def test_source_family_definition_id_uses_baseline_and_family_identity():
    assert build_source_family_definition_id(
        "M27_LIBRARY_CONTENT_BASELINE_WAVE_1@v1",
        "task_pools",
    ) == "M27_LIBRARY_CONTENT_BASELINE_WAVE_1@v1::task_pools"


def test_baseline_rejects_duplicate_source_family():
    payload = _minimal_baseline_payload()
    payload["source_families"].append(deepcopy(payload["source_families"][0]))

    with pytest.raises(ValidationError) as exc_info:
        SourceLibraryBaselineModel(**payload)

    assert "Duplicate source family is not allowed in baseline: task_pools" in str(
        exc_info.value
    )


def test_baseline_rejects_missing_source_family():
    payload = _minimal_baseline_payload()
    payload["source_families"] = [
        family
        for family in payload["source_families"]
        if family["family_id"] != "mappings"
    ]

    with pytest.raises(ValidationError) as exc_info:
        load_source_library_baseline_from_payload(payload)

    assert "M27.8 baseline is missing source families: mappings" in str(
        exc_info.value
    )


def test_baseline_rejects_blank_integration_control():
    payload = _minimal_baseline_payload()
    payload["integration_controls"] = [" "]

    with pytest.raises(ValidationError) as exc_info:
        load_source_library_baseline_from_payload(payload)

    assert "Blank integration control is not allowed" in str(exc_info.value)


def test_missing_source_family_lookup_raises_clear_error():
    baseline = load_source_library_baseline_from_payload(_minimal_baseline_payload())

    with pytest.raises(ValueError) as exc_info:
        get_source_family_by_id(baseline, "unknown")

    assert "Source family baseline definition not found: unknown" in str(
        exc_info.value
    )


def test_baseline_rejects_persisted_state_payload():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_source_library_baseline_from_payload(persisted_state_payload)

    assert "source-library baseline payload must include source_families" in str(
        exc_info.value
    )
