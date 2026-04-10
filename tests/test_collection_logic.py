import pytest
from pydantic import ValidationError

from asbp.collection_logic import (
    find_collection_by_id,
    generate_next_collection_id,
    validate_unique_collection_ids,
)
from asbp.state_model import TaskCollectionModel


def test_generate_next_collection_id_returns_tc_001_for_empty_collection_list():
    assert generate_next_collection_id([]) == "TC-001"


def test_generate_next_collection_id_increments_highest_valid_collection_id():
    collections = [
        TaskCollectionModel(collection_id="TC-001"),
        TaskCollectionModel(collection_id="TC-007"),
        TaskCollectionModel(collection_id="TC-003"),
    ]

    assert generate_next_collection_id(collections) == "TC-008"


def test_find_collection_by_id_returns_matching_collection():
    collections = [
        TaskCollectionModel(collection_id="TC-001"),
        TaskCollectionModel(collection_id="TC-002"),
    ]

    collection = find_collection_by_id(collections, "TC-002")

    assert collection is not None
    assert collection.collection_id == "TC-002"


def test_find_collection_by_id_returns_none_when_collection_is_missing():
    collections = [
        TaskCollectionModel(collection_id="TC-001"),
        TaskCollectionModel(collection_id="TC-002"),
    ]

    assert find_collection_by_id(collections, "TC-999") is None


def test_validate_unique_collection_ids_accepts_unique_collection_ids():
    collections = [
        TaskCollectionModel(collection_id="TC-001"),
        TaskCollectionModel(collection_id="TC-002"),
    ]

    validate_unique_collection_ids(collections)


def test_validate_unique_collection_ids_rejects_duplicates():
    collections = [
        TaskCollectionModel(collection_id="TC-001"),
        TaskCollectionModel(collection_id="TC-001"),
    ]

    with pytest.raises(
        ValueError,
        match=r"Duplicate collection_id is not allowed: TC-001",
    ):
        validate_unique_collection_ids(collections)


def test_task_collection_model_rejects_non_collection_identity_namespace():
    with pytest.raises(ValidationError):
        TaskCollectionModel(collection_id="WP-001")