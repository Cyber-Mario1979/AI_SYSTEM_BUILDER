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


def _build_dependent_tasks_index(tasks):
    dependent_tasks_by_task_id = {}

    for task in tasks:
        if isinstance(task, dict):
            task_id = task.get("task_id")
        else:
            task_id = task.task_id

        dependent_tasks_by_task_id.setdefault(task_id, [])

    for task in tasks:
        if isinstance(task, dict):
            dependency_ids = task.get("dependencies", [])
        else:
            dependency_ids = task.dependencies

        for dependency_id in dependency_ids:
            dependent_tasks_by_task_id.setdefault(dependency_id, []).append(task)

    return dependent_tasks_by_task_id


def filter_tasks(
    tasks,
    *,
    status=None,
    has_dependencies=None,
    has_dependents=None,
    has_task_key=None,
    task_key=None,
    task_id=None,
    dependency_task_id=None,
    dependent_task_id=None,
):
    """
    Return a filtered task list without mutating the original input.

    Filtering rules:
    - status: exact match on task["status"]
    - has_dependencies=True: keep only tasks with one or more dependencies
    - has_dependencies=False: keep only tasks with zero dependencies
    - has_dependents=True: keep only tasks referenced by one or more persisted dependencies
    - has_dependents=False: keep only tasks not referenced by any persisted dependency
    - has_task_key=True: keep only tasks with a non-null task_key
    - has_task_key=False: keep only tasks with task_key equal to None
    - task_key: keep only tasks whose normalized persisted task_key exactly matches
    - task_id: keep only tasks whose task_id exactly matches
    - dependency_task_id: keep only tasks whose dependencies include that exact stored task_id
    - dependent_task_id: keep only tasks whose derived dependent set includes that exact
      stored task_id, using the full unfiltered input and persisted dependency storage
    - if multiple filters are provided, apply AND logic
    - preserve original task order
    """
    all_tasks = list(tasks)
    filtered = list(tasks)
    dependent_tasks_index = _build_dependent_tasks_index(all_tasks)

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

    if has_dependents is True:
        filtered = [
            task for task in filtered
            if len(dependent_tasks_index.get(task.get("task_id"), [])) > 0
        ]
    elif has_dependents is False:
        filtered = [
            task for task in filtered
            if len(dependent_tasks_index.get(task.get("task_id"), [])) == 0
        ]

    if has_task_key is True:
        filtered = [
            task for task in filtered
            if task.get("task_key") is not None
        ]
    elif has_task_key is False:
        filtered = [
            task for task in filtered
            if task.get("task_key") is None
        ]

    if task_key is not None:
        filtered = [
            task for task in filtered
            if normalize_task_key(task.get("task_key")) == task_key
        ]

    if task_id is not None:
        filtered = [
            task for task in filtered
            if task.get("task_id") == task_id
        ]
    
    if dependency_task_id is not None:
        filtered = [
            task for task in filtered
            if dependency_task_id in task.get("dependencies", [])
        ]

    if dependent_task_id is not None:
        filtered = [
            task for task in filtered
            if any(
                dependent_task.get("task_id") == dependent_task_id
                for dependent_task in dependent_tasks_index.get(
                    task.get("task_id"),
                    [],
                )
            )
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


def build_dependency_reference_view(
    tasks: list[TaskModel],
    dependency_ids: list[str],
) -> list[dict[str, str]]:
    dependency_refs: list[dict[str, str]] = []

    for dependency_id in dependency_ids:
        dependency_task = find_task_by_id(tasks, dependency_id)

        if dependency_task is None:
            task_key_display = "<missing>"
        else:
            task_key_display = normalize_task_key(dependency_task.task_key) or "<none>"

        dependency_refs.append(
            {
                "task_id": dependency_id,
                "task_key": task_key_display,
            }
        )

    return dependency_refs    

def build_dependent_reference_view(
    tasks: list[TaskModel],
    target_task_id: str,
) -> list[dict[str, str]]:
    dependent_refs: list[dict[str, str]] = []
    dependent_tasks_index = _build_dependent_tasks_index(tasks)

    for task in dependent_tasks_index.get(target_task_id, []):
        task_key_display = normalize_task_key(task.task_key) or "<none>"
        dependent_refs.append(
            {
                "task_id": task.task_id,
                "task_key": task_key_display,
            }
        )

    return dependent_refs

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


def prepare_task_key_for_write(
    tasks: list[TaskModel],
    task_key: str | None,
    *,
    current_task_id: str | None = None,
) -> str | None:
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
        if current_task_id is not None and task.task_id == current_task_id:
            continue

        existing_task_key = normalize_task_key(getattr(task, "task_key", None))
        if existing_task_key == normalized_task_key:
            raise ValueError(
                f"Duplicate task_key is not allowed: {normalized_task_key}"
            )

    return normalized_task_key
def validate_persisted_task_keys(tasks: list[TaskModel]) -> None:
    seen_task_keys: set[str] = set()

    for task in tasks:
        normalized_task_key = normalize_task_key(getattr(task, "task_key", None))
        if normalized_task_key is None:
            continue

        if _TASK_KEY_RESERVED_TASK_ID_NAMESPACE_RE.fullmatch(normalized_task_key):
            raise ValueError(
                f"Reserved task_key namespace is not allowed: {normalized_task_key}"
            )

        if normalized_task_key in seen_task_keys:
            raise ValueError(
                f"Duplicate task_key is not allowed: {normalized_task_key}"
            )

        seen_task_keys.add(normalized_task_key)