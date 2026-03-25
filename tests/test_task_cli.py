import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / "data" / "state" / "state.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "asbp", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def restore_state_file():
    original_exists = STATE_FILE.exists()
    original_text = STATE_FILE.read_text(encoding="utf-8") if original_exists else None

    yield

    if original_exists and original_text is not None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(original_text, encoding="utf-8")
    elif STATE_FILE.exists():
        STATE_FILE.unlink()


def test_task_add_creates_first_task_with_planned_status(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "add", "First real task")

    assert result.returncode == 0
    assert "Task added: TASK-001 - First real task" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    assert saved_state["tasks"] == [
        {
            "task_id": "TASK-001",
            "order": 1,
            "title": "First real task",
            "status": "planned",
        }
    ]


def test_task_add_uses_next_deterministic_task_id(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "Existing task",
                        "status": "planned",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "add", "Second real task")

    assert result.returncode == 0
    assert "Task added: TASK-002 - Second real task" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    assert saved_state["tasks"] == [
        {
            "task_id": "TASK-001",
            "order": 1,
            "title": "Existing task",
            "status": "planned",
        },
        {
            "task_id": "TASK-002",
            "order": 2,
            "title": "Second real task",
            "status": "planned",
        },
    ]


def test_task_list_shows_no_tasks_message_for_empty_task_list(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list")

    assert result.returncode == 0
    assert "No tasks found." in result.stdout


def test_task_list_shows_all_tasks_in_readable_format(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list")

    assert result.returncode == 0
    output = result.stdout
    assert "Tasks:" in output
    assert "- TASK-001 | planned | First real task" in output
    assert "- TASK-002 | completed | Second real task" in output


def test_task_list_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("task", "list")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout


def test_task_update_status_updates_only_target_task(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "planned",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "update-status", "TASK-001", "in_progress")

    assert result.returncode == 0
    assert "Task status updated: TASK-001 -> in_progress" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    assert saved_state["tasks"] == [
        {
            "task_id": "TASK-001",
            "order": 1,
            "title": "First real task",
            "status": "in_progress",
        },
        {
            "task_id": "TASK-002",
            "order": 2,
            "title": "Second real task",
            "status": "planned",
        },
    ]


def test_task_update_status_handles_unknown_task_id(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "update-status", "TASK-999", "completed")

    assert result.returncode == 0
    assert "Task not found: TASK-999" in result.stdout


def test_task_update_status_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("task", "update-status", "TASK-001", "completed")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout


def test_task_update_status_rejects_invalid_status_at_parser_level():
    result = run_cli("task", "update-status", "TASK-001", "wrong_value")

    assert result.returncode != 0
    combined_output = result.stdout + result.stderr
    assert "invalid choice" in combined_output


def test_task_delete_removes_only_target_task(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "delete", "TASK-001")

    assert result.returncode == 0
    assert "Task deleted: TASK-001" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    assert saved_state["tasks"] == [
        {
            "task_id": "TASK-002",
            "order": 2,
            "title": "Second real task",
            "status": "completed",
        }
    ]


def test_task_delete_handles_unknown_task_id(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "delete", "TASK-999")

    assert result.returncode == 0
    assert "Task not found: TASK-999" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    assert saved_state["tasks"] == [
        {
            "task_id": "TASK-001",
            "order": 1,
            "title": "First real task",
            "status": "planned",
        }
    ]


def test_task_delete_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("task", "delete", "TASK-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout


def test_task_list_filters_tasks_by_status(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "completed",
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Third real task",
                        "status": "planned",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--status", "planned")

    assert result.returncode == 0
    output = result.stdout
    assert "Tasks:" in output
    assert "- TASK-001 | planned | First real task" in output
    assert "- TASK-003 | planned | Third real task" in output
    assert "- TASK-002 | completed | Second real task" not in output


def test_task_list_filters_to_no_results(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--status", "completed")

    assert result.returncode == 0
    assert "No tasks found." in result.stdout


def test_task_show_displays_matching_task_as_json(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "TASK-002")

    assert result.returncode == 0
    output = result.stdout
    assert '"task_id": "TASK-002"' in output
    assert '"order": 2' in output
    assert '"title": "Second real task"' in output
    assert '"status": "completed"' in output


def test_task_show_handles_unknown_task_id(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "First real task",
                        "status": "planned",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "TASK-999")

    assert result.returncode == 0
    assert "Task not found: TASK-999" in result.stdout


def test_task_show_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("task", "show", "TASK-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    