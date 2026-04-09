from typing import Literal

from asbp.state_model import TaskModel, WorkPackageModel
from asbp.task_logic import find_task_by_reference


def find_work_package_by_id(
    work_packages: list[WorkPackageModel],
    wp_id: str,
) -> WorkPackageModel | None:
    for work_package in work_packages:
        if work_package.wp_id == wp_id:
            return work_package
    return None


def filter_work_packages(
    work_packages: list[WorkPackageModel],
    *,
    tasks: list[TaskModel] | None = None,
    status: str | None = None,
    title: str | None = None,
    wp_id: str | None = None,
    task_id: str | None = None,
) -> list[WorkPackageModel]:
    filtered = list(work_packages)

    if status is not None:
        filtered = [
            work_package
            for work_package in filtered
            if work_package.status == status
        ]

    if title is not None:
        filtered = [
            work_package
            for work_package in filtered
            if work_package.title == title
        ]

    if wp_id is not None:
        filtered = [
            work_package
            for work_package in filtered
            if work_package.wp_id == wp_id
        ]

    if task_id is not None:
        matching_work_package_ids = {
            task.work_package_id
            for task in (tasks or [])
            if task.task_id == task_id and task.work_package_id is not None
        }
        filtered = [
            work_package
            for work_package in filtered
            if work_package.wp_id in matching_work_package_ids
        ]

    return filtered


def create_work_package(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    title: str,
) -> WorkPackageModel:
    if find_work_package_by_id(work_packages, wp_id) is not None:
        raise ValueError(f"Duplicate wp_id is not allowed: {wp_id}")

    return WorkPackageModel(
        wp_id=wp_id,
        title=title,
        status="open",
    )


def update_work_package_status(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    status: Literal["open", "in_progress", "completed"],
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    work_package.status = status
    return work_package


def delete_work_package_by_id(
    work_packages: list[WorkPackageModel],
    tasks: list[TaskModel],
    *,
    wp_id: str,
) -> tuple[list[WorkPackageModel], bool, str | None]:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return list(work_packages), False, None

    associated_task_ids = build_work_package_task_ids(tasks, wp_id=wp_id)
    if associated_task_ids:
        task_ids_display = ", ".join(associated_task_ids)
        return (
            list(work_packages),
            False,
            f"Work Package cannot be deleted while tasks are associated: "
            f"{wp_id} -> [{task_ids_display}]",
        )

    updated_work_packages = [
        existing_work_package
        for existing_work_package in work_packages
        if existing_work_package.wp_id != wp_id
    ]
    return updated_work_packages, True, None


def update_work_package_title(
    work_packages: list[WorkPackageModel],
    *,
    wp_id: str,
    title: str,
) -> WorkPackageModel | None:
    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None

    validated_work_package = WorkPackageModel(
        wp_id=work_package.wp_id,
        title=title,
        status=work_package.status,
    )
    work_package.title = validated_work_package.title
    return work_package


def set_task_work_package(
    tasks: list[TaskModel],
    work_packages: list[WorkPackageModel],
    *,
    task_ref: str,
    wp_id: str,
) -> tuple[TaskModel | None, str | None]:
    target_task = find_task_by_reference(tasks, task_ref)
    if target_task is None:
        return None, f"Task not found: {task_ref}"

    work_package = find_work_package_by_id(work_packages, wp_id)
    if work_package is None:
        return None, f"Work Package not found: {wp_id}"

    if (
        target_task.work_package_id is not None
        and target_task.work_package_id != work_package.wp_id
    ):
        return (
            None,
            "Task already associated with a different Work Package: "
            f"{target_task.task_id} -> {target_task.work_package_id}",
        )

    target_task.work_package_id = work_package.wp_id
    return target_task, None


def clear_task_work_package(
    tasks: list[TaskModel],
    *,
    task_ref: str,
) -> tuple[TaskModel | None, str | None]:
    target_task = find_task_by_reference(tasks, task_ref)
    if target_task is None:
        return None, f"Task not found: {task_ref}"

    target_task.work_package_id = None
    return target_task, None


def build_work_package_task_ids(
    tasks: list[TaskModel],
    *,
    wp_id: str,
) -> list[str]:
    return [
        task.task_id
        for task in tasks
        if task.work_package_id == wp_id
    ]


def validate_persisted_task_work_package_links(
    tasks: list[TaskModel],
    work_packages: list[WorkPackageModel],
) -> None:
    existing_wp_ids = {work_package.wp_id for work_package in work_packages}

    for task in tasks:
        if task.work_package_id is None:
            continue

        if task.work_package_id not in existing_wp_ids:
            raise ValueError(
                "Persisted task work_package_id does not exist: "
                f"{task.task_id} -> {task.work_package_id}"
            )