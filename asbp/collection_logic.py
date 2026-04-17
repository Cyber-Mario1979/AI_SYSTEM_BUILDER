import re

from asbp.state_model import (
    CollectionState,
    TaskCollectionModel,
    TaskModel,
    WorkPackageModel,
)
from asbp.task_logic import find_task_by_reference


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
        work_package_id=collection.work_package_id,
        task_ids=list(collection.task_ids),
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

    validated_collection = TaskCollectionModel(
        collection_id=collection.collection_id,
        title=collection.title,
        collection_state=collection_state,
        work_package_id=collection.work_package_id,
        task_ids=list(collection.task_ids),
    )
    collection.collection_state = validated_collection.collection_state
    return collection


def _find_conflicting_non_source_collection(
    collections: list[TaskCollectionModel],
    *,
    task_id: str,
    exclude_collection_id: str,
) -> TaskCollectionModel | None:
    for collection in collections:
        if collection.collection_id == exclude_collection_id:
            continue
        if collection.collection_state == "source":
            continue
        if task_id in collection.task_ids:
            return collection
    return None


def add_task_to_collection(
    tasks: list[TaskModel],
    collections: list[TaskCollectionModel],
    *,
    collection_id: str,
    task_ref: str,
) -> tuple[TaskCollectionModel | None, TaskModel | None, str | None]:
    collection = find_collection_by_id(collections, collection_id)
    if collection is None:
        return None, None, f"Collection not found: {collection_id}"

    target_task = find_task_by_reference(tasks, task_ref)
    if target_task is None:
        return None, None, f"Task not found: {task_ref}"

    if target_task.task_id in collection.task_ids:
        return (
            None,
            None,
            "Task already associated with collection: "
            f"{target_task.task_id} -> {collection.collection_id}",
        )

    if collection.collection_state != "source":
        conflicting_collection = _find_conflicting_non_source_collection(
            collections,
            task_id=target_task.task_id,
            exclude_collection_id=collection.collection_id,
        )
        if conflicting_collection is not None:
            return (
                None,
                None,
                "Task already associated with a different non-source collection: "
                f"{target_task.task_id} -> "
                f"{conflicting_collection.collection_id} "
                f"({conflicting_collection.collection_state})",
            )

    collection.task_ids.append(target_task.task_id)
    return collection, target_task, None


def remove_task_from_collection(
    tasks: list[TaskModel],
    collections: list[TaskCollectionModel],
    *,
    collection_id: str,
    task_ref: str,
) -> tuple[TaskCollectionModel | None, TaskModel | None, str | None]:
    collection = find_collection_by_id(collections, collection_id)
    if collection is None:
        return None, None, f"Collection not found: {collection_id}"

    target_task = find_task_by_reference(tasks, task_ref)
    if target_task is None:
        return None, None, f"Task not found: {task_ref}"

    collection.task_ids = [
        task_id
        for task_id in collection.task_ids
        if task_id != target_task.task_id
    ]

    return collection, target_task, None


def validate_persisted_collection_work_package_links(
    task_collections: list[TaskCollectionModel],
    work_packages: list[WorkPackageModel],
) -> None:
    existing_wp_ids = {work_package.wp_id for work_package in work_packages}

    for task_collection in task_collections:
        if task_collection.work_package_id is None:
            continue

        if task_collection.work_package_id not in existing_wp_ids:
            raise ValueError(
                "Persisted collection work_package_id does not exist: "
                f"{task_collection.collection_id} -> {task_collection.work_package_id}"
            )


def validate_persisted_collection_task_memberships(
    tasks: list[TaskModel],
    collections: list[TaskCollectionModel],
) -> None:
    existing_task_ids = {task.task_id for task in tasks}
    non_source_memberships: dict[str, TaskCollectionModel] = {}

    for collection in collections:
        seen_task_ids_in_collection: set[str] = set()

        for task_id in collection.task_ids:
            if task_id in seen_task_ids_in_collection:
                raise ValueError(
                    "Duplicate task membership is not allowed in collection: "
                    f"{collection.collection_id} -> {task_id}"
                )
            seen_task_ids_in_collection.add(task_id)

            if task_id not in existing_task_ids:
                raise ValueError(
                    "Persisted collection task_id does not exist: "
                    f"{collection.collection_id} -> {task_id}"
                )

            if collection.collection_state == "source":
                continue

            existing_collection = non_source_memberships.get(task_id)
            if existing_collection is not None:
                raise ValueError(
                    "Task cannot belong to more than one non-source collection: "
                    f"{task_id} -> "
                    f"{existing_collection.collection_id} "
                    f"({existing_collection.collection_state}), "
                    f"{collection.collection_id} "
                    f"({collection.collection_state})"
                )

            non_source_memberships[task_id] = collection
