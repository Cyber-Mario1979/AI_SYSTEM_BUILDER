import json

import pytest
from pydantic import ValidationError

from asbp.state_model import StateModel, TaskModel, WorkPackageModel
from asbp.state_store import build_persisted_state_payload, load_validated_state


def write_state_file(state_file, payload: dict) -> None:
    state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_load_validated_state_defaults_legacy_task_source_fields_to_manual(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "status": "planned",
                }
            ],
            "work_packages": [],
            "task_collections": [],
        },
    )

    state = load_validated_state(state_file)

    assert state.tasks == [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            status="planned",
            instantiation_mode="manual",
        )
    ]


def test_build_persisted_state_payload_omits_manual_source_fields_for_backward_compatibility():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        tasks=[
            TaskModel(
                task_id="TASK-001",
                order=1,
                title="Prepare FAT",
                status="planned",
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["tasks"] == [
        {
            "task_id": "TASK-001",
            "order": 1,
            "title": "Prepare FAT",
            "status": "planned",
            "dependencies": [],
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
        }
    ]


def test_load_validated_state_accepts_preset_resolved_task_with_task_pool_source(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "work_package_id": "WP-001",
                    "instantiation_mode": "preset_resolved",
                    "source_definition_kind": "task_pool",
                    "source_definition_id": "PE-OSD:E2E:T001",
                    "status": "planned",
                }
            ],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
        },
    )

    state = load_validated_state(state_file)

    assert state.tasks == [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            work_package_id="WP-001",
            instantiation_mode="preset_resolved",
            source_definition_kind="task_pool",
            source_definition_id="PE-OSD:E2E:T001",
            status="planned",
        )
    ]


def test_load_validated_state_rejects_manual_task_with_source_definition_id(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "source_definition_id": "PE-OSD:E2E:T001",
                    "status": "planned",
                }
            ],
            "work_packages": [],
            "task_collections": [],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "Manual task cannot declare source_definition_id" in str(exc_info.value)


def test_load_validated_state_rejects_preset_resolved_task_without_source_definition_id(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "work_package_id": "WP-001",
                    "instantiation_mode": "preset_resolved",
                    "source_definition_kind": "task_pool",
                    "status": "planned",
                }
            ],
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Tablet press qualification",
                    "status": "open",
                }
            ],
            "task_collections": [],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "Preset-resolved task must declare source_definition_id" in str(exc_info.value)


def test_load_validated_state_rejects_preset_resolved_task_without_work_package_id(tmp_path):
    state_file = tmp_path / "state.json"
    write_state_file(
        state_file,
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.8.0",
            "status": "in_flight",
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "order": 1,
                    "title": "Prepare FAT",
                    "instantiation_mode": "preset_resolved",
                    "source_definition_kind": "task_pool",
                    "source_definition_id": "PE-OSD:E2E:T001",
                    "status": "planned",
                }
            ],
            "work_packages": [],
            "task_collections": [],
        },
    )

    with pytest.raises(ValidationError) as exc_info:
        load_validated_state(state_file)

    assert "Preset-resolved task must declare work_package_id" in str(exc_info.value)


def test_build_persisted_state_payload_persists_non_manual_task_source_fields():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.8.0",
        status="in_flight",
        work_packages=[
            WorkPackageModel(
                wp_id="WP-001",
                title="Tablet press qualification",
                status="open",
            )
        ],
        tasks=[
            TaskModel(
                task_id="TASK-001",
                order=1,
                title="Prepare FAT",
                work_package_id="WP-001",
                instantiation_mode="preset_resolved",
                source_definition_kind="task_pool",
                source_definition_id="PE-OSD:E2E:T001",
                status="planned",
            )
        ],
    )

    payload = build_persisted_state_payload(state)

    assert payload["tasks"] == [
        {
            "task_id": "TASK-001",
            "order": 1,
            "title": "Prepare FAT",
            "work_package_id": "WP-001",
            "instantiation_mode": "preset_resolved",
            "source_definition_kind": "task_pool",
            "source_definition_id": "PE-OSD:E2E:T001",
            "status": "planned",
            "dependencies": [],
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
        }
    ]
