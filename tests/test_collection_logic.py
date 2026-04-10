import pytest
from pydantic import ValidationError
from typing import cast

from asbp.collection_logic import (
    find_collection_by_id,
    generate_next_collection_id,
    validate_unique_collection_ids,
)
from asbp.state_model import CollectionState, StateModel, TaskCollectionModel


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


def test_generate_next_collection_id_returns_tc_001_for_empty_collection_list():
    assert generate_next_collection_id([]) == "TC-001"


def test_generate_next_collection_id_increments_highest_valid_collection_id():
    collections = [
        make_collection("TC-001"),
        make_collection("TC-007"),
        make_collection("TC-003"),
    ]

    assert generate_next_collection_id(collections) == "TC-008"


def test_find_collection_by_id_returns_matching_collection():
    collections = [
        make_collection("TC-001"),
        make_collection("TC-002", title="Matched Collection"),
    ]

    collection = find_collection_by_id(collections, "TC-002")

    assert collection is not None
    assert collection.collection_id == "TC-002"
    assert collection.title == "Matched Collection"


def test_find_collection_by_id_returns_none_when_collection_is_missing():
    collections = [
        make_collection("TC-001"),
        make_collection("TC-002"),
    ]

    assert find_collection_by_id(collections, "TC-999") is None


def test_validate_unique_collection_ids_accepts_unique_collection_ids():
    collections = [
        make_collection("TC-001"),
        make_collection("TC-002"),
    ]

    validate_unique_collection_ids(collections)


def test_validate_unique_collection_ids_rejects_duplicates():
    collections = [
        make_collection("TC-001"),
        make_collection("TC-001"),
    ]

    with pytest.raises(
        ValueError,
        match=r"Duplicate collection_id is not allowed: TC-001",
    ):
        validate_unique_collection_ids(collections)


def test_task_collection_model_rejects_non_collection_identity_namespace():
    with pytest.raises(ValidationError):
        TaskCollectionModel(
            collection_id="WP-001",
            title="Wrong Namespace",
            collection_state="source",
        )


def test_task_collection_model_requires_non_empty_title():
    with pytest.raises(ValidationError):
        TaskCollectionModel(
            collection_id="TC-001",
            title="",
            collection_state="source",
        )


def test_task_collection_model_rejects_invalid_collection_state():
    with pytest.raises(ValidationError):
        TaskCollectionModel(
            collection_id="TC-001",
            title="Invalid State Collection",
            collection_state=cast(CollectionState, "draft"),
        )


def test_task_collection_model_accepts_refined_state():
    collection = TaskCollectionModel(
        collection_id="TC-001",
        title="Refined Collection",
        collection_state="refined",
    )

    assert collection.collection_state == "refined"


def test_state_model_accepts_task_collections():
    state = StateModel(
        project="AI_SYSTEM_BUILDER",
        version="0.1.0",
        status="not_started",
        task_collections=[
            make_collection("TC-001", title="Source Pool", collection_state="source"),
            make_collection(
                "TC-002",
                title="Committed Selection",
                collection_state="committed",
            ),
        ],
    )

    assert len(state.task_collections) == 2
    assert state.task_collections[0].collection_id == "TC-001"
    assert state.task_collections[1].collection_state == "committed"


def test_state_model_rejects_duplicate_task_collection_ids():
    with pytest.raises(
        ValidationError,
        match=r"Duplicate collection_id is not allowed: TC-001",
    ):
        StateModel(
            project="AI_SYSTEM_BUILDER",
            version="0.1.0",
            status="not_started",
            task_collections=[
                make_collection("TC-001"),
                make_collection("TC-001", title="Duplicate Collection"),
            ],
        )