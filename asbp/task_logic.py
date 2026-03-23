import re

from asbp.state_model import TaskModel


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
