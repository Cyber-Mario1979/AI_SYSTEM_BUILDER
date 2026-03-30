import pytest

from asbp.state_model import TaskModel
from asbp.task_logic import (
    filter_tasks,
    update_task_status,
    validate_task_status_transition,
    validate_task_completion_readiness,
    find_task_by_reference,
    normalize_task_key,
    prepare_task_key_for_write,
    validate_persisted_task_keys,
)

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

def test_validate_task_status_transition_allows_planned_to_in_progress():
    validate_task_status_transition("planned", "in_progress")


def test_validate_task_status_transition_allows_in_progress_to_completed():
    validate_task_status_transition("in_progress", "completed")


def test_validate_task_status_transition_rejects_planned_to_completed():
    with pytest.raises(ValueError, match="Invalid status transition"):
        validate_task_status_transition("planned", "completed")


def test_validate_task_status_transition_rejects_in_progress_to_planned():
    with pytest.raises(ValueError, match="Invalid status transition"):
        validate_task_status_transition("in_progress", "planned")


def test_validate_task_status_transition_rejects_completed_to_in_progress():
    with pytest.raises(ValueError, match="Invalid status transition"):
        validate_task_status_transition("completed", "in_progress")


def test_validate_task_status_transition_rejects_same_status():
    with pytest.raises(ValueError, match="Invalid status transition"):
        validate_task_status_transition("planned", "planned")    


def test_update_task_status_allows_valid_transition():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="planned",
            dependencies=[],
            order=1,
        ),
    ]

    update_task_status(tasks, "TASK-001", "in_progress")

    assert tasks[0].status == "in_progress"


def test_update_task_status_rejects_invalid_transition():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="planned",
            dependencies=[],
            order=1,
        ),
    ]

    with pytest.raises(ValueError, match="Invalid status transition"):
        update_task_status(tasks, "TASK-001", "completed")


def test_update_task_status_does_not_mutate_on_invalid_transition():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="in_progress",
            dependencies=[],
            order=1,
        ),
    ]

    with pytest.raises(ValueError, match="Invalid status transition"):
        update_task_status(tasks, "TASK-001", "planned")

    assert tasks[0].status == "in_progress"

def test_validate_task_completion_readiness_returns_no_errors_when_no_dependencies():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="in_progress",
            dependencies=[],
            order=1,
        ),
    ]

    result = validate_task_completion_readiness(tasks, "TASK-001")

    assert result == []


def test_validate_task_completion_readiness_returns_no_errors_when_all_dependencies_completed():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="completed",
            dependencies=[],
            order=1,
        ),
        TaskModel(
            task_id="TASK-002",
            title="Task 2",
            status="in_progress",
            dependencies=["TASK-001"],
            order=2,
        ),
    ]

    result = validate_task_completion_readiness(tasks, "TASK-002")

    assert result == []


def test_validate_task_completion_readiness_returns_error_for_one_incomplete_dependency():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="planned",
            dependencies=[],
            order=1,
        ),
        TaskModel(
            task_id="TASK-002",
            title="Task 2",
            status="in_progress",
            dependencies=["TASK-001"],
            order=2,
        ),
    ]

    result = validate_task_completion_readiness(tasks, "TASK-002")

    assert result == [
        "Task cannot be completed until dependency is completed: TASK-001"
    ]


def test_validate_task_completion_readiness_returns_deterministic_errors_for_multiple_incomplete_dependencies():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="planned",
            dependencies=[],
            order=1,
        ),
        TaskModel(
            task_id="TASK-002",
            title="Task 2",
            status="in_progress",
            dependencies=[],
            order=2,
        ),
        TaskModel(
            task_id="TASK-003",
            title="Task 3",
            status="planned",
            dependencies=["TASK-001", "TASK-002"],
            order=3,
        ),
    ]

    result = validate_task_completion_readiness(tasks, "TASK-003")

    assert result == [
        "Task cannot be completed until dependency is completed: TASK-001",
        "Task cannot be completed until dependency is completed: TASK-002",
    ]


def test_validate_task_completion_readiness_returns_error_for_missing_dependency():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="in_progress",
            dependencies=["TASK-999"],
            order=1,
        ),
    ]

    result = validate_task_completion_readiness(tasks, "TASK-001")

    assert result == ["Dependency task not found: TASK-999"]

def test_update_task_status_allows_completion_when_dependencies_completed():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="completed",
            dependencies=[],
            order=1,
        ),
        TaskModel(
            task_id="TASK-002",
            title="Task 2",
            status="in_progress",
            dependencies=["TASK-001"],
            order=2,
        ),
    ]

    update_task_status(tasks, "TASK-002", "completed")

    assert tasks[1].status == "completed"


def test_update_task_status_rejects_completion_when_dependency_incomplete():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="planned",
            dependencies=[],
            order=1,
        ),
        TaskModel(
            task_id="TASK-002",
            title="Task 2",
            status="in_progress",
            dependencies=["TASK-001"],
            order=2,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Task cannot be completed until dependency is completed: TASK-001",
    ):
        update_task_status(tasks, "TASK-002", "completed")


def test_update_task_status_does_not_mutate_on_blocked_completion():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            title="Task 1",
            status="planned",
            dependencies=[],
            order=1,
        ),
        TaskModel(
            task_id="TASK-002",
            title="Task 2",
            status="in_progress",
            dependencies=["TASK-001"],
            order=2,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Task cannot be completed until dependency is completed: TASK-001",
    ):
        update_task_status(tasks, "TASK-002", "completed")

    assert tasks[1].status == "in_progress"        

def test_normalize_task_key_returns_kebab_case():
    assert normalize_task_key(" Prepare_FAT Protocol ") == "prepare-fat-protocol"


def test_find_task_by_reference_falls_back_to_task_key():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT protocol",
            task_key="prepare-fat-protocol",
            status="planned",
            dependencies=[],
        )
    ]

    task = find_task_by_reference(tasks, "Prepare_FAT Protocol")
    assert task is not None
    assert task.task_id == "TASK-001"

def test_validate_persisted_task_keys_rejects_reserved_task_id_namespace():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Task A",
            task_key="task_001",
            status="planned",
            dependencies=[],
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Reserved task_key namespace is not allowed: task-001",
    ):
        validate_persisted_task_keys(tasks)


def test_validate_persisted_task_keys_rejects_duplicate_normalized_task_key():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Task A",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Task B",
            task_key="Prepare FAT",
            status="planned",
            dependencies=[],
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Duplicate task_key is not allowed: prepare-fat",
    ):
        validate_persisted_task_keys(tasks)

def test_find_task_by_reference_raises_on_duplicate_task_key():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Task A",
            task_key="prepare-fat-protocol",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Task B",
            task_key="prepare-fat-protocol",
            status="planned",
            dependencies=[],
        ),
    ]

    with pytest.raises(ValueError, match="Duplicate task_key detected"):
        find_task_by_reference(tasks, "prepare-fat-protocol")


def test_prepare_task_key_for_write_returns_normalized_task_key():
    assert prepare_task_key_for_write([], " Prepare_FAT Protocol ") == "prepare-fat-protocol"


def test_prepare_task_key_for_write_rejects_duplicate_normalized_task_key():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Task A",
            task_key="prepare-fat-protocol",
            status="planned",
            dependencies=[],
        ),
    ]

    with pytest.raises(ValueError, match="Duplicate task_key is not allowed"):
        prepare_task_key_for_write(tasks, "Prepare FAT Protocol")


def test_prepare_task_key_for_write_allows_same_normalized_task_key_for_existing_task():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Task A",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
    ]

    assert (
        prepare_task_key_for_write(
            tasks,
            " Prepare FAT ",
            current_task_id="TASK-001",
        )
        == "prepare-fat"
    )


def test_prepare_task_key_for_write_rejects_duplicate_normalized_task_key_for_other_task_on_update():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Task A",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Task B",
            task_key="execute-fat",
            status="planned",
            dependencies=[],
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Duplicate task_key is not allowed: prepare-fat",
    ):
        prepare_task_key_for_write(
            tasks,
            "Prepare FAT",
            current_task_id="TASK-002",
        )
