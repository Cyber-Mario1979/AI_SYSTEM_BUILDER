import re
from typing import Literal

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
