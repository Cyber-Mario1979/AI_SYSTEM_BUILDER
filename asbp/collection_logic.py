import re

from asbp.state_model import CollectionState, TaskCollectionModel


def generate_next_collection_id(collections: list[TaskCollectionModel]) -> str:
    if not collections:
        return "TC-001"

    max_number = 0

    for collection in collections:
        match = re.fullmatch(r"TC-(\d{3})", collection.collection_id)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number

    return f"TC-{max_number + 1:03d}"


def find_collection_by_id(
    collections: list[TaskCollectionModel],
    collection_id: str,
) -> TaskCollectionModel | None:
    for collection in collections:
        if collection.collection_id == collection_id:
            return collection
    return None


def validate_unique_collection_ids(
    collections: list[TaskCollectionModel],
) -> None:
    seen_collection_ids: set[str] = set()

    for collection in collections:
        if collection.collection_id in seen_collection_ids:
            raise ValueError(
                f"Duplicate collection_id is not allowed: {collection.collection_id}"
            )
        seen_collection_ids.add(collection.collection_id)


def create_collection(
    collections: list[TaskCollectionModel],
    *,
    title: str,
    collection_state: CollectionState = "source",
) -> TaskCollectionModel:
    return TaskCollectionModel(
        collection_id=generate_next_collection_id(collections),
        title=title,
        collection_state=collection_state,
    )