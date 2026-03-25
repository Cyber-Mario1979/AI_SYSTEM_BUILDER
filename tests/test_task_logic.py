from asbp.state_model import TaskModel
from asbp.task_logic import (
    delete_task_by_id,
    filter_tasks_by_status,
    find_task_by_id,
    generate_next_task_id,
    generate_next_task_order,
    update_task_status,
)


def test_generate_next_task_id_empty_tasks_returns_task_001() -> None:
    tasks: list[TaskModel] = []

    result = generate_next_task_id(tasks)

    assert result == "TASK-001"


def test_generate_next_task_id_returns_next_highest_task_id() -> None:
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="First task",
            status="planned",
        ),
        TaskModel(
            task_id="TASK-003",
            order=2,
            title="Third task",
            status="in_progress",
        ),
    ]

    result = generate_next_task_id(tasks)

    assert result == "TASK-004"


def test_generate_next_task_order_empty_tasks_returns_1() -> None:
    tasks: list[TaskModel] = []

    result = generate_next_task_order(tasks)

    assert result == 1


def test_generate_next_task_order_returns_next_highest_order() -> None:
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="First task",
            status="planned",
        ),
        TaskModel(
            task_id="TASK-002",
            order=3,
            title="Second task",
            status="completed",
        ),
    ]

    result = generate_next_task_order(tasks)

    assert result == 4


def test_find_task_by_id_returns_matching_task() -> None:
    task_1 = TaskModel(
        task_id="TASK-001",
        order=1,
        title="First task",
        status="planned",
    )
    task_2 = TaskModel(
        task_id="TASK-002",
        order=2,
        title="Second task",
        status="completed",
    )
    tasks = [task_1, task_2]

    result = find_task_by_id(tasks, "TASK-002")

    assert result == task_2


def test_find_task_by_id_returns_none_when_not_found() -> None:
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="First task",
            status="planned",
        )
    ]

    result = find_task_by_id(tasks, "TASK-999")

    assert result is None


def test_filter_tasks_by_status_returns_only_matching_tasks() -> None:
    task_1 = TaskModel(
        task_id="TASK-001",
        order=1,
        title="First task",
        status="planned",
    )
    task_2 = TaskModel(
        task_id="TASK-002",
        order=2,
        title="Second task",
        status="completed",
    )
    task_3 = TaskModel(
        task_id="TASK-003",
        order=3,
        title="Third task",
        status="planned",
    )
    tasks = [task_1, task_2, task_3]

    result = filter_tasks_by_status(tasks, "planned")

    assert result == [task_1, task_3]


def test_update_task_status_updates_matching_task() -> None:
    task = TaskModel(
        task_id="TASK-001",
        order=1,
        title="First task",
        status="planned",
    )
    tasks = [task]

    result = update_task_status(tasks, "TASK-001", "completed")

    assert result is task
    assert task.status == "completed"


def test_update_task_status_returns_none_when_task_not_found() -> None:
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="First task",
            status="planned",
        )
    ]

    result = update_task_status(tasks, "TASK-999", "completed")

    assert result is None


def test_delete_task_by_id_removes_matching_task_and_returns_true() -> None:
    task_1 = TaskModel(
        task_id="TASK-001",
        order=1,
        title="First task",
        status="planned",
    )
    task_2 = TaskModel(
        task_id="TASK-002",
        order=2,
        title="Second task",
        status="completed",
    )
    tasks = [task_1, task_2]

    updated_tasks, deleted_flag = delete_task_by_id(tasks, "TASK-001")

    assert updated_tasks == [task_2]
    assert deleted_flag is True


def test_delete_task_by_id_returns_original_list_and_false_when_not_found() -> None:
    task_1 = TaskModel(
        task_id="TASK-001",
        order=1,
        title="First task",
        status="planned",
    )
    task_2 = TaskModel(
        task_id="TASK-002",
        order=2,
        title="Second task",
        status="completed",
    )
    tasks = [task_1, task_2]

    updated_tasks, deleted_flag = delete_task_by_id(tasks, "TASK-999")

    assert updated_tasks == tasks
    assert deleted_flag is False