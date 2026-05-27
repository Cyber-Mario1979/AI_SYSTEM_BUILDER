from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.task_pool_source_model import TaskPoolLibraryModel
from asbp.task_pool_source_store import (
    build_task_source_definition_id,
    get_atomic_task_by_id,
    get_task_pool_by_id,
    list_task_pool_ids,
    load_default_task_pool_library,
    load_task_pool_library_from_payload,
)


def _minimal_task_pool_payload() -> dict:
    return {
        "task_pool_id": "TP-TEST-POOL@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "display_name": "Test task pool",
        "preset_family": "PF-PROCESS-EQUIPMENT",
        "selector_context_tags": ["test"],
        "lifecycle_events": ["LE-NEW-INSTALLATION"],
        "qualification_validation_intents": ["INT-E2E-QUALIFICATION"],
        "tasks": [
            {
                "atomic_task_id": "TEST-SCOPE",
                "title": "Confirm test scope",
                "purpose": "Confirm test scope.",
                "task_type": "SCOPE_CONFIRMATION",
                "owner_role": "CQV Lead",
                "prerequisites": ["Human-confirmed context"],
                "dependencies": [],
                "duration_ref": {"duration_ref_id": "TEST_SCOPE_DUR"},
                "document_expectations": [
                    {"document_ref": "TEST_PLAN", "status": "future_expected"}
                ],
            },
            {
                "atomic_task_id": "TEST-CLOSEOUT",
                "title": "Close test pool",
                "purpose": "Close test pool.",
                "task_type": "CLOSEOUT",
                "owner_role": "CQV / QA",
                "prerequisites": ["Scope confirmed"],
                "dependencies": [
                    {
                        "atomic_task_id": "TEST-SCOPE",
                        "dependency_type": "FS",
                        "lag_days": 0,
                    }
                ],
                "duration_ref": {"duration_ref_id": "TEST_CLOSEOUT_DUR"},
                "document_expectations": [
                    {"document_ref": "TEST_REPORT", "status": "future_expected"}
                ],
            },
        ],
    }


def _minimal_library_payload(task_pool: dict | None = None) -> dict:
    return {
        "library_id": "TEST_LIBRARY@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "task_pools": [task_pool or _minimal_task_pool_payload()],
    }


def test_default_starter_task_pool_library_loads_runtime_source_records():
    library = load_default_task_pool_library()

    assert library.library_id == "M27_TASK_POOL_STARTER_LIBRARY@v1"
    assert list_task_pool_ids(library) == [
        "TP-PE-E2E-QUAL@v1",
        "TP-QCLAB-QUAL-CAL-LINK@v1",
        "TP-CLEANROOM-HVAC-QUAL@v1",
        "TP-UTILITIES-QUAL@v1",
        "TP-CSV-BASELINE@v1",
        "TP-MANUAL-FALLBACK-ASSESS@v1",
    ]

    process_equipment_pool = get_task_pool_by_id(
        library,
        "TP-PE-E2E-QUAL@v1",
    )
    assert process_equipment_pool.preset_family == "PF-PROCESS-EQUIPMENT"
    assert process_equipment_pool.tasks[0].atomic_task_id == "PE-E2E-SCOPE"

    qc_lab_pool = get_task_pool_by_id(
        library,
        "TP-QCLAB-QUAL-CAL-LINK@v1",
    )
    assert qc_lab_pool.preset_family == "PF-QC-LAB-EQUIPMENT"
    assert get_atomic_task_by_id(
        qc_lab_pool,
        "QCLAB-CSV-LINK",
    ).owner_role == "CSV / QA / QC"


def test_task_source_definition_id_uses_pool_and_atomic_task_identity():
    assert build_task_source_definition_id(
        "TP-PE-E2E-QUAL@v1",
        "PE-E2E-SCOPE",
    ) == "TP-PE-E2E-QUAL@v1::PE-E2E-SCOPE"


def test_task_pool_library_rejects_duplicate_task_pool_ids():
    task_pool = _minimal_task_pool_payload()
    payload = _minimal_library_payload(task_pool)
    payload["task_pools"].append(deepcopy(task_pool))

    with pytest.raises(ValidationError) as exc_info:
        TaskPoolLibraryModel(**payload)

    assert "Duplicate task_pool_id is not allowed: TP-TEST-POOL@v1" in str(
        exc_info.value
    )


def test_task_pool_rejects_duplicate_atomic_task_ids():
    task_pool = _minimal_task_pool_payload()
    task_pool["tasks"][1]["atomic_task_id"] = "TEST-SCOPE"

    with pytest.raises(ValidationError) as exc_info:
        load_task_pool_library_from_payload(_minimal_library_payload(task_pool))

    assert "Duplicate atomic_task_id is not allowed: TEST-SCOPE" in str(
        exc_info.value
    )


def test_task_pool_rejects_dependency_to_missing_atomic_task_id():
    task_pool = _minimal_task_pool_payload()
    task_pool["tasks"][1]["dependencies"][0]["atomic_task_id"] = "MISSING-TASK"

    with pytest.raises(ValidationError) as exc_info:
        load_task_pool_library_from_payload(_minimal_library_payload(task_pool))

    assert (
        "Atomic task dependency does not exist in task pool TP-TEST-POOL@v1: "
        "TEST-CLOSEOUT -> MISSING-TASK"
    ) in str(exc_info.value)


def test_task_pool_rejects_self_dependency():
    task_pool = _minimal_task_pool_payload()
    task_pool["tasks"][1]["dependencies"][0]["atomic_task_id"] = "TEST-CLOSEOUT"

    with pytest.raises(ValidationError) as exc_info:
        load_task_pool_library_from_payload(_minimal_library_payload(task_pool))

    assert "Atomic task cannot depend on itself: TEST-CLOSEOUT" in str(
        exc_info.value
    )


def test_task_pool_rejects_invalid_preset_family():
    task_pool = _minimal_task_pool_payload()
    task_pool["preset_family"] = "PF-UNKNOWN"

    with pytest.raises(ValidationError) as exc_info:
        load_task_pool_library_from_payload(_minimal_library_payload(task_pool))

    assert "preset_family" in str(exc_info.value)


def test_task_pool_rejects_missing_owner_role():
    task_pool = _minimal_task_pool_payload()
    task_pool["tasks"][0]["owner_role"] = ""

    with pytest.raises(ValidationError) as exc_info:
        load_task_pool_library_from_payload(_minimal_library_payload(task_pool))

    assert "owner_role" in str(exc_info.value)


def test_task_pool_rejects_missing_duration_ref():
    task_pool = _minimal_task_pool_payload()
    task_pool["tasks"][0].pop("duration_ref")

    with pytest.raises(ValidationError) as exc_info:
        load_task_pool_library_from_payload(_minimal_library_payload(task_pool))

    assert "duration_ref" in str(exc_info.value)


def test_persisted_state_payload_is_not_task_pool_source_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_task_pool_library_from_payload(persisted_state_payload)

    assert "task-pool library payload must include task_pools" in str(exc_info.value)
