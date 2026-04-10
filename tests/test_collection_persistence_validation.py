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