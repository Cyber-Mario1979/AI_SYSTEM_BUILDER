import json
import subprocess
import sys
from pathlib import Path

import pytest
from asbp.cli import (
    handle_task_add,
    load_state_or_none,
    load_validated_state,
    save_validated_state,
)
from asbp.state_model import StateModel

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
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
            "dependencies": [],
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
                        "description": None,
                        "dependencies": [],
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
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
            "dependencies": [],
        },
        {
            "task_id": "TASK-002",
            "order": 2,
            "title": "Second real task",
            "status": "planned",
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
            "dependencies": [],
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
                        "description": None,
                        "status": "planned",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "description": None,
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
                        "description": None,
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "description": None,
                        "status": "planned",
                        "dependencies": [],
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
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
            "status": "in_progress",
            "dependencies": [],
        },
        {
            "task_id": "TASK-002",
            "order": 2,
            "title": "Second real task",
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
            "status": "planned",
            "dependencies": [],
        },
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
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "dependencies": [],
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
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "dependencies": [],
        }
    ]


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
                        "description": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "description": None,
                        "status": "completed",
                        "dependencies": [],
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
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": None,
            "status": "completed",
            "dependencies": [],
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
                        "description": None,
                        "dependencies": [],
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
                        "description": None,
                        "dependencies": [],
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
                        "description": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "completed",
                        "description": None,
                        "dependencies": [],
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
    assert '"dependencies": []' in output


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
                        "description": None,
                        "dependencies": [],
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


def test_task_set_dependencies_updates_dependencies_when_valid(restore_state_file):
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
                        "description": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "planned",
                        "description": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Third real task",
                        "status": "planned",
                        "description": None,
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "task",
        "set-dependencies",
        "TASK-003",
        "TASK-001",
        "TASK-002",
    )

    assert result.returncode == 0
    assert (
        "Task dependencies updated: TASK-003 -> ['TASK-001', 'TASK-002']"
        in result.stdout
    )

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][2]["dependencies"] == ["TASK-001", "TASK-002"]


def test_task_set_dependencies_rejects_invalid_dependencies_without_saving(
    restore_state_file,
):
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
                        "description": None,
                        "status": "planned",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "planned",
                        "description": None,
                        "dependencies": ["TASK-001"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "task",
        "set-dependencies",
        "TASK-002",
        "TASK-002",
        "TASK-999",
    )

    assert result.returncode == 0
    output = result.stdout
    assert "Dependency validation failed:" in output
    assert "- Task cannot depend on itself: TASK-002" in output
    assert "- Dependency task not found: TASK-999" in output

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][1]["dependencies"] == ["TASK-001"]


def test_task_set_dependencies_handles_unknown_task_id(restore_state_file):
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
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "set-dependencies", "TASK-999", "TASK-001")

    assert result.returncode == 0
    assert "Dependency validation failed:" in result.stdout
    assert "- Task not found: TASK-999" in result.stdout


def test_task_set_dependencies_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("task", "set-dependencies", "TASK-001", "TASK-002")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout


def test_task_add_accepts_optional_description(restore_state_file):
    save_validated_state(
        StateModel(
            project="Test Project",
            version="1.0",
            status="not_started",
            tasks=[],
        )
    )

    class Args:
        title = "My task"
        description = "First enriched task"
        owner = None
        duration = None
        start_date = None
        end_date = None

    handle_task_add(Args())

    state = load_state_or_none()

    assert state is not None
    assert len(state.tasks) == 1
    assert state.tasks[0].title == "My task"
    assert state.tasks[0].description == "First enriched task"
    assert state.tasks[0].owner is None
    assert state.tasks[0].duration is None
    assert state.tasks[0].start_date is None
    assert state.tasks[0].end_date is None
    assert state.tasks[0].status == "planned"


def test_task_add_accepts_optional_duration(restore_state_file):
    save_validated_state(
        StateModel(
            project="Test Project",
            version="1.0",
            status="not_started",
            tasks=[],
        )
    )

    class Args:
        title = "My task"
        description = None
        owner = None
        duration = 5
        start_date = None
        end_date = None

    handle_task_add(Args())

    state = load_state_or_none()

    assert state is not None
    assert len(state.tasks) == 1
    assert state.tasks[0].title == "My task"
    assert state.tasks[0].description is None
    assert state.tasks[0].owner is None
    assert state.tasks[0].duration == 5
    assert state.tasks[0].start_date is None
    assert state.tasks[0].end_date is None
    assert state.tasks[0].status == "planned"


def test_task_add_accepts_optional_start_date(restore_state_file):
    save_validated_state(
        StateModel(
            project="Test Project",
            version="1.0",
            status="not_started",
            tasks=[],
        )
    )

    class Args:
        title = "My task"
        description = None
        owner = None
        duration = None
        start_date = "2026-03-27"
        end_date = None

    handle_task_add(Args())

    state = load_state_or_none()

    assert state is not None
    assert len(state.tasks) == 1
    assert state.tasks[0].title == "My task"
    assert state.tasks[0].description is None
    assert state.tasks[0].owner is None
    assert state.tasks[0].duration is None
    assert state.tasks[0].start_date == "2026-03-27"
    assert state.tasks[0].end_date is None
    assert state.tasks[0].status == "planned"


def test_task_add_accepts_optional_end_date(restore_state_file):
    save_validated_state(
        StateModel(
            project="Test Project",
            version="1.0",
            status="not_started",
            tasks=[],
        )
    )

    class Args:
        title = "My task"
        description = None
        owner = None
        duration = None
        start_date = None
        end_date = "2026-03-30"

    handle_task_add(Args())

    state = load_state_or_none()

    assert state is not None
    assert len(state.tasks) == 1
    assert state.tasks[0].title == "My task"
    assert state.tasks[0].description is None
    assert state.tasks[0].owner is None
    assert state.tasks[0].duration is None
    assert state.tasks[0].start_date is None
    assert state.tasks[0].end_date == "2026-03-30"
    assert state.tasks[0].status == "planned"


def test_task_add_persists_normalized_task_key_when_provided(restore_state_file):
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

    result = run_cli(
        "task",
        "add",
        "Prepare FAT protocol",
        "--task-key",
        " Prepare_FAT Protocol ",
    )

    assert result.returncode == 0
    assert "Task added: TASK-001 - Prepare FAT protocol" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    assert saved_state["tasks"] == [
        {
            "task_id": "TASK-001",
            "order": 1,
            "title": "Prepare FAT protocol",
            "status": "planned",
            "description": None,
            "owner": None,
            "duration": None,
            "start_date": None,
            "end_date": None,
            "task_key": "prepare-fat-protocol",
            "dependencies": [],
        }
    ]


def test_task_add_rejects_duplicate_normalized_task_key_without_saving(restore_state_file):
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
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat-protocol",
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "task",
        "add",
        "Second task",
        "--task-key",
        "Prepare FAT Protocol",
    )

    assert result.returncode == 0
    assert "Duplicate task_key is not allowed: prepare-fat-protocol" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert len(saved_state["tasks"]) == 1


def test_load_validated_state_accepts_legacy_task_without_duration(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(
        """
{
  "project": "AI_SYSTEM_BUILDER",
  "version": "0.8.0",
  "status": "in_flight",
  "tasks": [
    {
      "task_id": "TASK-001",
      "order": 1,
      "title": "Legacy task",
      "description": null,
      "owner": null,
      "status": "planned",
      "dependencies": []
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    state = load_validated_state(state_file)

    assert len(state.tasks) == 1
    assert state.tasks[0].title == "Legacy task"
    assert state.tasks[0].description is None
    assert state.tasks[0].owner is None
    assert state.tasks[0].duration is None
    assert state.tasks[0].start_date is None
    assert state.tasks[0].end_date is None

    