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


def filter_collections(
    collections: list[TaskCollectionModel],
    *,
    collection_state: CollectionState | None = None,
    title: str | None = None,
    collection_id: str | None = None,
) -> list[TaskCollectionModel]:
    filtered = list(collections)

    if collection_state is not None:
        filtered = [
            collection
            for collection in filtered
            if collection.collection_state == collection_state
        ]

    if title is not None:
        filtered = [
            collection
            for collection in filtered
            if collection.title == title
        ]

    if collection_id is not None:
        filtered = [
            collection
            for collection in filtered
            if collection.collection_id == collection_id
        ]

    return filtered


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


def update_collection_title(
    collections: list[TaskCollectionModel],
    *,
    collection_id: str,
    title: str,
) -> TaskCollectionModel | None:
    collection = find_collection_by_id(collections, collection_id)
    if collection is None:
        return None

    validated_collection = TaskCollectionModel(
        collection_id=collection.collection_id,
        title=title,
        collection_state=collection.collection_state,
    )
    collection.title = validated_collection.title
    return collection


def update_collection_state(
    collections: list[TaskCollectionModel],
    *,
    collection_id: str,
    collection_state: CollectionState,
) -> TaskCollectionModel | None:
    collection = find_collection_by_id(collections, collection_id)
    if collection is None:
        return None

    collection.collection_state = collection_state
    return collection