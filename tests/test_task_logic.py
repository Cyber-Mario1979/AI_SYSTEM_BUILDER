from typing import Literal
import re

from asbp.state_model import TaskModel


TaskStatus = Literal["planned", "in_progress", "completed", "over_due"]


def generate_next_task_id(tasks: list[TaskModel]) -> str:
    if not tasks:
        return "TASK-001"

    max_number = 0

    for task in tasks:
        match = re.fullmatch(r"TASK-(\d{3})", task.task_id)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number

    return f"TASK-{max_number + 1:03d}"


def generate_next_task_order(tasks: list[TaskModel]) -> int:
    if not tasks:
        return 1

    max_order = 0

    for task in tasks:
        if task.order > max_order:
            max_order = task.order

    return max_order + 1


def find_task_by_id(tasks: list[TaskModel], task_id: str) -> TaskModel | None:
    for task in tasks:
        if task.task_id == task_id:
            return task

    return None


def filter_tasks_by_status(
    tasks: list[TaskModel], status: TaskStatus
) -> list[TaskModel]:
    return [task for task in tasks if task.status == status]


def update_task_status(
    tasks: list[TaskModel], task_id: str, new_status: TaskStatus
) -> TaskModel | None:
    task = find_task_by_id(tasks, task_id)
    if task is None:
        return None

    task.status = new_status
    return task


def delete_task_by_id(
    tasks: list[TaskModel], task_id: str
) -> tuple[list[TaskModel], bool]:
    updated_tasks = [task for task in tasks if task.task_id != task_id]
    deleted_flag = len(updated_tasks) != len(tasks)
    return updated_tasks, deleted_flag


def validate_task_dependencies(
    tasks: list[TaskModel],
    task_id: str,
    dependency_ids: list[str],
) -> list[str]:
    errors: list[str] = []

    existing_task_ids = {task.task_id for task in tasks}

    if task_id in dependency_ids:
        errors.append(f"Task cannot depend on itself: {task_id}")

    seen: set[str] = set()
    duplicate_ids: set[str] = set()

    for dependency_id in dependency_ids:
        if dependency_id in seen:
            duplicate_ids.add(dependency_id)
        seen.add(dependency_id)

    for duplicate_id in sorted(duplicate_ids):
        errors.append(f"Duplicate dependency is not allowed: {duplicate_id}")

    for dependency_id in dependency_ids:
        if dependency_id not in existing_task_ids:
            errors.append(f"Dependency task not found: {dependency_id}")

    return errors


def set_task_dependencies(
    tasks: list[TaskModel],
    task_id: str,
    dependency_ids: list[str],
) -> tuple[TaskModel | None, list[str]]:
    task = find_task_by_id(tasks, task_id)
    if task is None:
        return None, [f"Task not found: {task_id}"]

    errors = validate_task_dependencies(tasks, task_id, dependency_ids)
    if errors:
        return None, errors

    task.dependencies = dependency_ids
    return task, []
from asbp.task_logic import filter_tasks


def test_filter_tasks_by_status_only():
    tasks = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
        {"task_id": "TASK-003", "title": "Task 3", "status": "planned", "dependencies": ["TASK-001"]},
    ]

    result = filter_tasks(tasks, status="planned")

    assert [task["task_id"] for task in result] == ["TASK-001", "TASK-003"]


def test_filter_tasks_by_has_dependencies_true_only():
    tasks = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
        {"task_id": "TASK-003", "title": "Task 3", "status": "planned", "dependencies": ["TASK-001"]},
    ]

    result = filter_tasks(tasks, has_dependencies=True)

    assert [task["task_id"] for task in result] == ["TASK-002", "TASK-003"]


def test_filter_tasks_by_has_dependencies_false_only():
    tasks = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
        {"task_id": "TASK-003", "title": "Task 3", "status": "planned", "dependencies": ["TASK-001"]},
    ]

    result = filter_tasks(tasks, has_dependencies=False)

    assert [task["task_id"] for task in result] == ["TASK-001"]


def test_filter_tasks_by_status_and_has_dependencies_with_and_logic():
    tasks = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
        {"task_id": "TASK-003", "title": "Task 3", "status": "planned", "dependencies": ["TASK-001"]},
        {"task_id": "TASK-004", "title": "Task 4", "status": "completed", "dependencies": ["TASK-001"]},
    ]

    result = filter_tasks(tasks, status="planned", has_dependencies=True)

    assert [task["task_id"] for task in result] == ["TASK-003"]


def test_filter_tasks_with_no_filters_returns_same_order():
    tasks = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
        {"task_id": "TASK-003", "title": "Task 3", "status": "planned", "dependencies": ["TASK-001"]},
    ]

    result = filter_tasks(tasks)

    assert [task["task_id"] for task in result] == ["TASK-001", "TASK-002", "TASK-003"]
    assert result is not tasks


def test_filter_tasks_returns_empty_list_when_no_match():
    tasks = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
    ]

    result = filter_tasks(tasks, status="completed", has_dependencies=False)

    assert result == []


def test_filter_tasks_does_not_mutate_input():
    tasks = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
    ]
    original = [
        {"task_id": "TASK-001", "title": "Task 1", "status": "planned", "dependencies": []},
        {"task_id": "TASK-002", "title": "Task 2", "status": "in_progress", "dependencies": ["TASK-001"]},
    ]

    _ = filter_tasks(tasks, status="planned", has_dependencies=False)

    assert tasks == original