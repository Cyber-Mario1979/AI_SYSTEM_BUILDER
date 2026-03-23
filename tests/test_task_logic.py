from asbp.state_model import TaskModel
from asbp.task_logic import generate_next_task_id


def test_generate_next_task_id_returns_task_001_for_empty_list():
    tasks: list[TaskModel] = []

    result = generate_next_task_id(tasks)

    assert result == "TASK-001"


def test_generate_next_task_id_returns_next_number():
    tasks = [
        TaskModel(task_id="TASK-001", title="First task", status="planned"),
        TaskModel(task_id="TASK-002", title="Second task", status="in_progress"),
    ]

    result = generate_next_task_id(tasks)

    assert result == "TASK-003"


def test_generate_next_task_id_ignores_invalid_ids():
    tasks = [
        TaskModel(task_id="BAD-001", title="Bad task", status="planned"),
        TaskModel(task_id="TASK-002", title="Second task", status="completed"),
    ]

    result = generate_next_task_id(tasks)

    assert result == "TASK-003"


def test_generate_next_task_id_uses_highest_valid_number():
    tasks = [
        TaskModel(task_id="TASK-001", title="First task", status="planned"),
        TaskModel(task_id="TASK-005", title="Fifth task", status="completed"),
        TaskModel(task_id="TASK-003", title="Third task", status="over_due"),
    ]

    result = generate_next_task_id(tasks)

    assert result == "TASK-006"
    