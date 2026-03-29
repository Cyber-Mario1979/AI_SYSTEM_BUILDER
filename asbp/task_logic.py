from typing import Literal
import re

from asbp.state_model import TaskModel


TaskStatus = Literal["planned", "in_progress", "completed", "over_due"]

_TASK_KEY_INVALID_CHARS_RE = re.compile(r"[^a-z0-9-]")
_TASK_KEY_REPEAT_HYPHENS_RE = re.compile(r"-+")
_TASK_KEY_RESERVED_TASK_ID_NAMESPACE_RE = re.compile(r"task-\d{3}")


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


def update_task_status(tasks: list[TaskModel], task_id: str, new_status: TaskStatus) -> None:
    task = find_task_by_id(tasks, task_id)

    if task is None:
        raise ValueError(f"Task not found: {task_id}")

    current_status = task.status
    validate_task_status_transition(current_status, new_status)

    if new_status == "completed":
        readiness_errors = validate_task_completion_readiness(tasks, task_id)
        if readiness_errors:
            raise ValueError(readiness_errors[0])

    task.status = new_status
    
def delete_task_by_id(
    tasks: list[TaskModel], task_id: str
) -> tuple[list[TaskModel], bool]:
    updated_tasks = [task for task in tasks if task.task_id != task_id]
    deleted_flag = len(updated_tasks) != len(tasks)
    return updated_tasks, deleted_flag

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



def filter_tasks(tasks, *, status=None, has_dependencies=None):
    """
    Return a filtered task list without mutating the original input.

    Filtering rules:
    - status: exact match on task["status"]
    - has_dependencies=True: keep only tasks with one or more dependencies
    - has_dependencies=False: keep only tasks with zero dependencies
    - if both filters are provided, apply AND logic
    - preserve original task order
    """
    filtered = list(tasks)

    if status is not None:
        filtered = [task for task in filtered if task["status"] == status]

    if has_dependencies is True:
        filtered = [
            task for task in filtered
            if len(task.get("dependencies", [])) > 0
        ]
    elif has_dependencies is False:
        filtered = [
            task for task in filtered
            if len(task.get("dependencies", [])) == 0
        ]

    return filtered

def validate_task_status_transition(current_status, new_status):
    allowed_transitions = {
        "planned": {"in_progress"},
        "in_progress": {"completed"},
        "completed": set(),
        "over_due": set(),
    }

    if current_status == new_status:
        raise ValueError(
            f"Invalid status transition: {current_status} -> {new_status}"
        )

    if new_status not in allowed_transitions.get(current_status, set()):
        raise ValueError(
            f"Invalid status transition: {current_status} -> {new_status}"
        )
    
def validate_task_completion_readiness(
    tasks: list[TaskModel],
    task_id: str,
) -> list[str]:
    task = find_task_by_id(tasks, task_id)
    if task is None:
        return [f"Task not found: {task_id}"]

    errors: list[str] = []

    if not task.dependencies:
        return errors

    for dependency_id in task.dependencies:
        dependency_task = find_task_by_id(tasks, dependency_id)

        if dependency_task is None:
            errors.append(f"Dependency task not found: {dependency_id}")
            continue

        if dependency_task.status != "completed":
            errors.append(
                f"Task cannot be completed until dependency is completed: {dependency_id}"
            )

    return errors 
   
def normalize_task_key(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip().lower()
    normalized = normalized.replace("_", "-")
    normalized = normalized.replace(" ", "-")
    normalized = _TASK_KEY_INVALID_CHARS_RE.sub("", normalized)
    normalized = _TASK_KEY_REPEAT_HYPHENS_RE.sub("-", normalized)

    if not normalized:
        return None

    if normalized.startswith("-") or normalized.endswith("-"):
        return None

    return normalized


def find_task_by_reference(tasks, reference):
    task = find_task_by_id(tasks, reference)
    if task is not None:
        return task

    normalized_reference = normalize_task_key(reference)
    if normalized_reference is None:
        return None

    matches = []
    for task in tasks:
        task_key = normalize_task_key(getattr(task, "task_key", None))
        if task_key == normalized_reference:
            matches.append(task)

    if not matches:
        return None

    if len(matches) > 1:
        raise ValueError(
            f"Duplicate task_key detected for reference: {normalized_reference}"
        )

    return matches[0]


def prepare_task_key_for_write(tasks: list[TaskModel], task_key: str | None) -> str | None:
    if task_key is None:
        return None

    normalized_task_key = normalize_task_key(task_key)
    if normalized_task_key is None:
        raise ValueError(f"Invalid task_key: {task_key}")

    if _TASK_KEY_RESERVED_TASK_ID_NAMESPACE_RE.fullmatch(normalized_task_key):
        raise ValueError(
        f"Reserved task_key namespace is not allowed: {normalized_task_key}"
    )

    for task in tasks:
        existing_task_key = normalize_task_key(getattr(task, "task_key", None))
        if existing_task_key == normalized_task_key:
            raise ValueError(
                f"Duplicate task_key is not allowed: {normalized_task_key}"
            )

    return normalized_task_key