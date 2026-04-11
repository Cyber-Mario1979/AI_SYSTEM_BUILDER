import json

import pytest
from pydantic import ValidationError

from asbp.state_model import StateModel, TaskCollectionModel, CollectionState
from asbp.state_store import load_validated_state, save_validated_state_to_path


def make_collection(
    collection_id: str,
    title: str = "Default Collection",
    collection_state: CollectionState = "source",
) -> TaskCollectionModel:
    return TaskCollectionModel(
        collection_id=collection_id,
        title=title,
        collection_state=collection_state,
    )


def test_load_validated_state_accepts_legacy_state_without_task_collections(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    state = load_validated_state(state_file)

    assert state.task_collections == []


def test_save_validated_state_to_path_persists_task_collections(tmp_path):
    state_file = tmp_path / "state.json"
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.1.0",
        status="not_started",
        task_collections=[
            make_collection(
                "TC-001",
                title="Source Pool",
                collection_state="source",
            ),
            make_collection(
                "TC-002",
                title="Committed Selection",
                collection_state="committed",
            ),
        ],
    )

    save_validated_state_to_path(state, state_file)

    payload = json.loads(state_file.read_text(encoding="utf-8"))

    assert "task_collections" in payload
    assert len(payload["task_collections"]) == 2
    assert payload["task_collections"][0]["collection_id"] == "TC-001"
    assert payload["task_collections"][0]["title"] == "Source Pool"
    assert payload["task_collections"][0]["collection_state"] == "source"
    assert payload["task_collections"][1]["collection_id"] == "TC-002"
    assert payload["task_collections"][1]["collection_state"] == "committed"


def test_load_validated_state_reads_persisted_task_collections(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Refined Pool",
                        "collection_state": "refined",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    state = load_validated_state(state_file)

    assert len(state.task_collections) == 2
    assert state.task_collections[0].collection_id == "TC-001"
    assert state.task_collections[0].title == "Source Pool"
    assert state.task_collections[0].collection_state == "source"
    assert state.task_collections[1].collection_state == "refined"


def test_load_validated_state_rejects_invalid_persisted_collection_state(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Broken Pool",
                        "collection_state": "draft",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        load_validated_state(state_file)


def test_load_validated_state_rejects_duplicate_persisted_collection_ids(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                    },
                    {
                        "collection_id": "TC-001",
                        "title": "Duplicate Pool",
                        "collection_state": "staged",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValidationError,
        match=r"Duplicate collection_id is not allowed: TC-001",
    ):
        load_validated_state(state_file)


def test_load_validated_state_defaults_missing_collection_task_ids_to_empty_list(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    state = load_validated_state(state_file)

    assert state.task_collections[0].task_ids == []


def test_save_validated_state_to_path_persists_non_empty_collection_task_ids(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.1.0",
        status="not_started",
        task_collections=[
            TaskCollectionModel(
                collection_id="TC-001",
                title="Source Pool",
                collection_state="source",
                task_ids=["TASK-001", "TASK-002"],
            )
        ],
    )

    save_validated_state_to_path(state, state_file)

    payload = json.loads(state_file.read_text(encoding="utf-8"))

    assert payload["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Source Pool",
            "collection_state": "source",
            "task_ids": ["TASK-001", "TASK-002"],
        }
    ]

def test_load_validated_state_rejects_duplicate_task_membership_inside_one_collection(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": None,
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                        "task_ids": ["TASK-001", "TASK-001"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match=r"Duplicate task membership is not allowed in collection: TC-001 -> TASK-001",
    ):
        load_validated_state(state_file)


def test_load_validated_state_rejects_missing_persisted_collection_task_id(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                        "task_ids": ["TASK-999"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match=r"Persisted collection task_id does not exist: TC-001 -> TASK-999",
    ):
        load_validated_state(state_file)


def test_load_validated_state_rejects_task_in_multiple_non_source_collections(
    tmp_path,
):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": None,
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Staged Selection",
                        "collection_state": "staged",
                        "task_ids": ["TASK-001"],
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "task_ids": ["TASK-001"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match=r"Task cannot belong to more than one non-source collection: TASK-001 -> TC-001 \(staged\), TC-002 \(committed\)",
    ):
        load_validated_state(state_file)