import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from asbp.cli import (
    _attach_reference_views_to_task_payload,
    _build_task_list_row_parts,
    _format_reference_view_for_task_list,
    _prepare_task_list_filter_inputs,
    handle_task_add,
    load_state_or_none,
    load_validated_state,
    save_validated_state,
)
from asbp.state_model import StateModel, TaskModel

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

def test_attach_reference_views_to_task_payload_attaches_only_enabled_dependency_refs():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            task_key=None,
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-003",
            order=3,
            title="Review FAT Package",
            task_key="review-fat-package",
            status="completed",
            dependencies=["TASK-001", "TASK-002"],
        ),
    ]

    result = _attach_reference_views_to_task_payload(
        tasks,
        tasks[2].model_dump(),
        show_dependency_refs=True,
        show_dependent_refs=False,
    )

    assert result["dependency_refs"] == [
        {"task_id": "TASK-001", "task_key": "prepare-fat"},
        {"task_id": "TASK-002", "task_key": "<none>"},
    ]
    assert "dependent_refs" not in result


def test_attach_reference_views_to_task_payload_attaches_both_reference_views_when_enabled():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            task_key=None,
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-003",
            order=3,
            title="Review FAT Package",
            task_key="review-fat-package",
            status="completed",
            dependencies=["TASK-001", "TASK-002"],
        ),
        TaskModel(
            task_id="TASK-004",
            order=4,
            title="Archive FAT Package",
            task_key="archive-fat-package",
            status="planned",
            dependencies=["TASK-003"],
        ),
    ]

    result = _attach_reference_views_to_task_payload(
        tasks,
        tasks[2].model_dump(),
        show_dependency_refs=True,
        show_dependent_refs=True,
    )

    assert result["dependency_refs"] == [
        {"task_id": "TASK-001", "task_key": "prepare-fat"},
        {"task_id": "TASK-002", "task_key": "<none>"},
    ]
    assert result["dependent_refs"] == [
        {"task_id": "TASK-004", "task_key": "archive-fat-package"},
    ]


def test_format_reference_view_for_task_list_formats_populated_reference_surface():
    result = _format_reference_view_for_task_list(
        "dependency_refs",
        [
            {"task_id": "TASK-001", "task_key": "prepare-fat"},
            {"task_id": "TASK-002", "task_key": "<none>"},
        ],
    )

    assert result == "dependency_refs=[TASK-001:prepare-fat, TASK-002:<none>]"


def test_format_reference_view_for_task_list_formats_empty_reference_surface():
    result = _format_reference_view_for_task_list("dependent_refs", [])

    assert result == "dependent_refs=[]"


def test_build_task_list_row_parts_preserves_default_contract_without_visibility_flags():
    result = _build_task_list_row_parts(
        {
            "task_id": "TASK-001",
            "status": "planned",
            "title": "Prepare FAT",
            "task_key": "prepare-fat",
        }
    )

    assert result == [
        "- TASK-001",
        "planned",
        "Prepare FAT",
    ]


def test_build_task_list_row_parts_includes_current_visibility_surfaces_in_contract_order():
    result = _build_task_list_row_parts(
        {
            "task_id": "TASK-003",
            "status": "completed",
            "title": "Review FAT Package",
            "task_key": "review-fat-package",
            "dependency_refs": [
                {"task_id": "TASK-001", "task_key": "prepare-fat"},
                {"task_id": "TASK-002", "task_key": "<none>"},
            ],
            "dependent_refs": [
                {"task_id": "TASK-004", "task_key": "archive-fat-package"},
            ],
        },
        show_task_key=True,
        show_dependency_refs=True,
        show_dependent_refs=True,
    )

    assert result == [
        "- TASK-003",
        "completed",
        "task_key=review-fat-package",
        "dependency_refs=[TASK-001:prepare-fat, TASK-002:<none>]",
        "dependent_refs=[TASK-004:archive-fat-package]",
        "Review FAT Package",
    ]


def test_prepare_task_list_filter_inputs_resolves_current_list_filter_surfaces():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-002",
            order=2,
            title="Execute FAT",
            task_key="execute-fat",
            status="planned",
            dependencies=[],
        ),
        TaskModel(
            task_id="TASK-003",
            order=3,
            title="Review FAT Package",
            task_key="review-fat-package",
            status="completed",
            dependencies=["TASK-001", "TASK-002"],
        ),
        TaskModel(
            task_id="TASK-004",
            order=4,
            title="Archive FAT Package",
            task_key="archive-fat-package",
            status="planned",
            dependencies=["TASK-003"],
        ),
    ]

    args = SimpleNamespace(
        has_dependencies="true",
        has_dependents="false",
        has_task_key="true",
        task_key=" Review FAT Package ",
        task_ref="TASK-003",
        dependency_ref=" Prepare FAT ",
        dependent_ref="Archive FAT Package",
    )

    result = _prepare_task_list_filter_inputs(args, tasks)

    assert result == {
        "has_dependencies": True,
        "has_dependents": False,
        "has_task_key": True,
        "normalized_task_key_filter": "review-fat-package",
        "resolved_task_id_filter": "TASK-003",
        "resolved_dependency_task_id_filter": "TASK-001",
        "resolved_dependent_task_id_filter": "TASK-004",
        "should_return_no_tasks": False,
        "task_key_filter_requested_and_invalid": False,
    }


def test_prepare_task_list_filter_inputs_marks_no_tasks_for_unresolved_reference_and_invalid_task_key():
    tasks = [
        TaskModel(
            task_id="TASK-001",
            order=1,
            title="Prepare FAT",
            task_key="prepare-fat",
            status="planned",
            dependencies=[],
        ),
    ]

    args = SimpleNamespace(
        has_dependencies=None,
        has_dependents=None,
        has_task_key=None,
        task_key="***",
        task_ref="missing-task",
        dependency_ref=None,
        dependent_ref=None,
    )

    result = _prepare_task_list_filter_inputs(args, tasks)

    assert result == {
        "has_dependencies": None,
        "has_dependents": None,
        "has_task_key": None,
        "normalized_task_key_filter": None,
        "resolved_task_id_filter": None,
        "resolved_dependency_task_id_filter": None,
        "resolved_dependent_task_id_filter": None,
        "should_return_no_tasks": True,
        "task_key_filter_requested_and_invalid": True,
    }

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


def test_task_list_show_task_key_flag_displays_task_key_and_placeholder(
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
                        "task_key": "prepare-fat",
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "description": None,
                        "status": "completed",
                        "task_key": None,
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--show-task-key")

    assert result.returncode == 0
    output = result.stdout
    assert "Tasks:" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | First real task" in output
    assert "- TASK-002 | completed | task_key=<none> | Second real task" in output


def test_task_list_preserves_default_contract_without_show_task_key_flag(
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
                        "task_key": "prepare-fat",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list")

    assert result.returncode == 0
    output = result.stdout
    assert "- TASK-001 | planned | First real task" in output
    assert "task_key=" not in output


def test_task_list_filters_tasks_by_status_with_show_task_key_flag(
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
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Third real task",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--status", "planned", "--show-task-key")

    assert result.returncode == 0
    output = result.stdout
    assert "- TASK-001 | planned | task_key=prepare-fat | First real task" in output
    assert "- TASK-003 | planned | task_key=<none> | Third real task" in output
    assert "- TASK-002 | completed | task_key=execute-fat | Second real task" not in output


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


def test_task_show_show_dependency_refs_flag_displays_resolved_dependency_refs(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "TASK-003", "--show-dependency-refs")

    assert result.returncode == 0
    output = result.stdout
    assert '"task_id": "TASK-003"' in output
    assert '"dependencies": [' in output
    assert '"dependency_refs": [' in output
    assert '"task_id": "TASK-001"' in output
    assert '"task_key": "prepare-fat"' in output
    assert '"task_id": "TASK-002"' in output
    assert '"task_key": "<none>"' in output



def test_task_show_preserves_default_contract_without_show_dependency_refs_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001"],
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
    assert '"dependencies": [' in output
    assert '"dependency_refs":' not in output



def test_task_show_show_dependency_refs_flag_uses_missing_placeholder_for_unresolved_dependency(
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
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-999"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "TASK-001", "--show-dependency-refs")

    assert result.returncode == 0
    output = result.stdout
    assert '"dependency_refs": [' in output
    assert '"task_id": "TASK-999"' in output
    assert '"task_key": "<missing>"' in output



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


def test_task_set_key_updates_normalized_task_key_by_task_id(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": None,
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "set-key", "TASK-001", " Prepare_FAT ")

    assert result.returncode == 0
    assert "Task key updated: TASK-001 -> prepare-fat" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] == "prepare-fat"


def test_task_set_key_resolves_target_by_existing_task_key(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
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
        "set-key",
        " Prepare FAT ",
        "Prepare FAT Protocol",
    )

    assert result.returncode == 0
    assert "Task key updated: TASK-001 -> prepare-fat-protocol" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] == "prepare-fat-protocol"


def test_task_set_key_allows_equivalent_normalized_value_for_same_task(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "set-key", "TASK-001", " Prepare FAT ")

    assert result.returncode == 0
    assert "Task key updated: TASK-001 -> prepare-fat" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] == "prepare-fat"


def test_task_set_key_rejects_duplicate_normalized_task_key_without_saving(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "set-key", "TASK-002", "Prepare FAT")

    assert result.returncode == 0
    assert "Duplicate task_key is not allowed: prepare-fat" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] == "prepare-fat"
    assert saved_state["tasks"][1]["task_key"] == "execute-fat"


@pytest.mark.parametrize(
    "raw_task_key",
    [
        "TASK-002",
        " task_002 ",
        "Task 002",
    ],
)
def test_task_set_key_rejects_reserved_task_id_namespace_without_saving(
    restore_state_file,
    raw_task_key,
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": None,
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "set-key", "TASK-001", raw_task_key)

    assert result.returncode == 0
    assert "Reserved task_key namespace is not allowed: task-002" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] is None


def test_task_clear_key_clears_persisted_task_key_by_task_id(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "clear-key", "TASK-001")

    assert result.returncode == 0
    assert "Task key cleared: TASK-001" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] is None


def test_task_clear_key_resolves_target_by_existing_task_key(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "clear-key", " Prepare FAT ")

    assert result.returncode == 0
    assert "Task key cleared: TASK-001" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] is None


def test_task_clear_key_removes_secondary_lookup_resolution(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    clear_result = run_cli("task", "clear-key", "TASK-001")

    assert clear_result.returncode == 0
    assert "Task key cleared: TASK-001" in clear_result.stdout

    show_result = run_cli("task", "show", "prepare-fat")

    assert show_result.returncode == 0
    assert "Task not found: prepare-fat" in show_result.stdout


def test_task_clear_key_handles_unknown_task_id(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "clear-key", "TASK-999")

    assert result.returncode == 0
    assert "Task not found: TASK-999" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["task_key"] == "prepare-fat"


def test_task_clear_key_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("task", "clear-key", "TASK-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout



@pytest.mark.parametrize(
    "raw_task_key",
    [
        "TASK-001",
        " task_001 ",
        "Task 001",
    ],
)

def test_task_add_rejects_reserved_task_id_namespace_task_key_without_saving(
    restore_state_file,
    raw_task_key,
):
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
        "Reserved key task",
        "--task-key",
        raw_task_key,
    )

    assert result.returncode == 0
    assert "Reserved task_key namespace is not allowed: task-001" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"] == []

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

def test_task_set_dependencies_resolves_dependency_inputs_by_task_key(restore_state_file):
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
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "execute-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "review-fat-package",
                        "status": "planned",
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
        " prepare-fat ",
        "execute-fat",
    )

    assert result.returncode == 0
    assert (
        "Task dependencies updated: TASK-003 -> ['TASK-001', 'TASK-002']"
        in result.stdout
    )

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    target_task = next(task for task in saved_state["tasks"] if task["task_id"] == "TASK-003")
    assert target_task["dependencies"] == ["TASK-001", "TASK-002"]


def test_task_set_dependencies_allows_mixed_task_id_and_task_key_inputs(restore_state_file):
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
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "execute-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "review-fat-package",
                        "status": "planned",
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
        "review-fat-package",
        "TASK-001",
        " execute-fat ",
    )

    assert result.returncode == 0
    assert (
        "Task dependencies updated: TASK-003 -> ['TASK-001', 'TASK-002']"
        in result.stdout
    )

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    target_task = next(task for task in saved_state["tasks"] if task["task_id"] == "TASK-003")
    assert target_task["dependencies"] == ["TASK-001", "TASK-002"]


def test_task_set_dependencies_preserves_unknown_dependency_contract_for_task_key_input(
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
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "execute-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "review-fat-package",
                        "status": "planned",
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
        "prepare-fat",
        "missing-key",
    )

    assert result.returncode == 0
    assert "Dependency validation failed:" in result.stdout
    assert "- Dependency task not found: missing-key" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    target_task = next(task for task in saved_state["tasks"] if task["task_id"] == "TASK-003")
    assert target_task["dependencies"] == []


def test_task_set_dependencies_preserves_self_dependency_validation_through_task_key_resolution(
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
                        "title": "Prepare FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "execute-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "review-fat-package",
                        "status": "planned",
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
        "review-fat-package",
        "review-fat-package",
    )

    assert result.returncode == 0
    assert "Dependency validation failed:" in result.stdout
    assert "- Task cannot depend on itself: TASK-003" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    target_task = next(task for task in saved_state["tasks"] if task["task_id"] == "TASK-003")
    assert target_task["dependencies"] == []

def test_task_show_rejects_ambiguous_task_key_reference(restore_state_file):
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
                        "title": "Prepare FAT A",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Prepare FAT B",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "Prepare FAT",
                        "status": "planned",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "prepare-fat")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert "Duplicate task_key is not allowed: prepare-fat" in result.stdout



def test_task_update_status_rejects_ambiguous_task_key_reference_without_saving(
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
                        "title": "Prepare FAT A",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Prepare FAT B",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "Prepare FAT",
                        "status": "planned",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "update-status", "prepare-fat", "in_progress")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert "Duplicate task_key is not allowed: prepare-fat" in result.stdout



def test_task_delete_rejects_ambiguous_task_key_reference_without_saving(
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
                        "title": "Prepare FAT A",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Prepare FAT B",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "Prepare FAT",
                        "status": "planned",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "delete", "prepare-fat")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert "Duplicate task_key is not allowed: prepare-fat" in result.stdout



def test_task_set_dependencies_rejects_ambiguous_target_reference_without_saving(
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
                        "title": "Prepare FAT A",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Prepare FAT B",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "Prepare FAT",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "review-fat-package",
                        "status": "planned",
                        "dependencies": ["TASK-001"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "set-dependencies", "prepare-fat", "TASK-003")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert "Duplicate task_key is not allowed: prepare-fat" in result.stdout



def test_task_set_dependencies_rejects_ambiguous_dependency_reference_without_saving(
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
                        "title": "Prepare FAT A",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Prepare FAT B",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "Prepare FAT",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "description": None,
                        "owner": None,
                        "duration": None,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "review-fat-package",
                        "status": "planned",
                        "dependencies": ["TASK-002"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "set-dependencies", "TASK-003", "prepare-fat")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert "Duplicate task_key is not allowed: prepare-fat" in result.stdout



def test_load_validated_state_rejects_reserved_persisted_task_key_namespace(tmp_path):
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
      "title": "Reserved key task",
      "status": "planned",
      "task_key": "Task 001",
      "dependencies": []
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Reserved task_key namespace is not allowed: task-001",
    ):
        load_validated_state(state_file)


def test_task_list_rejects_duplicate_normalized_persisted_task_key_state(
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
                        "title": "Prepare FAT A",
                        "status": "planned",
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Prepare FAT B",
                        "status": "planned",
                        "task_key": "Prepare FAT",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list")

    assert result.returncode == 0
    assert "State validation failed:" in result.stdout
    assert "Duplicate task_key is not allowed: prepare-fat" in result.stdout

def test_task_list_show_dependency_refs_flag_displays_resolved_dependency_refs(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--show-dependency-refs")

    assert result.returncode == 0
    output = result.stdout
    assert "Tasks:" in output
    assert "- TASK-001 | planned | dependency_refs=[] | Prepare FAT" in output
    assert (
        "- TASK-003 | completed | "
        "dependency_refs=[TASK-001:prepare-fat, TASK-002:<none>] | "
        "Review FAT Package"
    ) in output


def test_task_show_show_dependent_refs_flag_displays_resolved_dependent_refs(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": ["TASK-001"],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": None,
                        "dependencies": ["TASK-001"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "TASK-001", "--show-dependent-refs")

    assert result.returncode == 0
    output = result.stdout
    assert '"task_id": "TASK-001"' in output
    assert '"dependent_refs": [' in output
    assert '"task_id": "TASK-002"' in output
    assert '"task_key": "execute-fat"' in output
    assert '"task_id": "TASK-003"' in output
    assert '"task_key": "<none>"' in output
    assert '"task_id": "TASK-004"' not in output


def test_task_show_show_dependent_refs_flag_returns_empty_list_when_no_dependents(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "TASK-001", "--show-dependent-refs")

    assert result.returncode == 0
    assert '"dependent_refs": []' in result.stdout


def test_task_show_preserves_default_contract_without_show_dependent_refs_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": ["TASK-001"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "show", "TASK-001")

    assert result.returncode == 0
    assert '"task_id": "TASK-001"' in result.stdout
    assert '"dependent_refs":' not in result.stdout


def test_task_list_preserves_default_contract_without_show_dependency_refs_flag(
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
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-002"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list")

    assert result.returncode == 0
    output = result.stdout
    assert "- TASK-001 | completed | Review FAT Package" in output
    assert "dependency_refs=" not in output


def test_task_list_show_dependency_refs_flag_uses_missing_placeholder_for_unresolved_dependency(
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
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-999"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--show-dependency-refs")

    assert result.returncode == 0
    output = result.stdout
    assert (
        "- TASK-001 | completed | dependency_refs=[TASK-999:<missing>] | "
        "Review FAT Package"
    ) in output


def test_task_list_show_dependency_refs_flag_preserves_compatibility_with_show_task_key_and_status(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
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
        "list",
        "--status",
        "completed",
        "--show-task-key",
        "--show-dependency-refs",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert (
        "- TASK-003 | completed | task_key=review-fat-package | "
        "dependency_refs=[TASK-001:prepare-fat, TASK-002:<none>] | "
        "Review FAT Package"
    ) in output
    assert "- TASK-001 | planned |" not in output
    assert "- TASK-004 | planned |" not in output    


def test_task_list_show_dependent_refs_flag_displays_resolved_dependent_refs(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": ["TASK-001"],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": None,
                        "dependencies": ["TASK-001"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
                        "dependencies": [],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("task", "list", "--show-dependent-refs")

    assert result.returncode == 0
    output = result.stdout
    assert "Tasks:" in output
    assert (
        "- TASK-001 | planned | "
        "dependent_refs=[TASK-002:execute-fat, TASK-003:<none>] | "
        "Prepare FAT"
    ) in output
    assert "- TASK-004 | planned | dependent_refs=[] | Archive FAT Package" in output


def test_task_list_preserves_default_contract_without_show_dependent_refs_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": ["TASK-001"],
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
    assert "- TASK-001 | planned | Prepare FAT" in output
    assert "dependent_refs=" not in output


def test_task_list_show_dependent_refs_flag_preserves_compatibility_with_show_task_key_show_dependency_refs_and_status(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
                        "dependencies": ["TASK-003"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "task",
        "list",
        "--status",
        "completed",
        "--show-task-key",
        "--show-dependency-refs",
        "--show-dependent-refs",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert (
        "- TASK-003 | completed | task_key=review-fat-package | "
        "dependency_refs=[TASK-001:prepare-fat, TASK-002:<none>] | "
        "dependent_refs=[TASK-004:archive-fat-package] | "
        "Review FAT Package"
    ) in output
    assert "- TASK-001 | planned |" not in output
    assert "- TASK-004 | planned |" not in output


def test_task_list_filters_tasks_by_exact_normalized_task_key_with_show_task_key_flag(
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
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "planned",
                        "description": None,
                        "task_key": "Prepare FAT Protocol",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Third real task",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
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
        "list",
        "--task-key",
        " Prepare_FAT Protocol ",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-002 | planned | task_key=prepare-fat-protocol | Second real task" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | First real task" not in output
    assert "- TASK-003 | planned | task_key=<none> | Third real task" not in output


def test_task_list_filters_tasks_by_task_key_and_status_with_and_logic(
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
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Second real task",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Third real task",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
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
        "list",
        "--task-key",
        "execute-fat",
        "--status",
        "completed",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-002 | completed | task_key=execute-fat | Second real task" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | First real task" not in output
    assert "- TASK-003 | completed | task_key=review-fat-package | Third real task" not in output


def test_task_list_invalid_task_key_filter_returns_no_tasks(restore_state_file):
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
                        "task_key": "prepare-fat",
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
        "list",
        "--task-key",
        "***",
        "--show-task-key",
    )

    assert result.returncode == 0
    assert "No tasks found." in result.stdout
    assert "Tasks:" not in result.stdout

def test_task_list_filters_tasks_by_task_ref_task_id_with_show_task_key_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
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
        "list",
        "--task-ref",
        "TASK-002",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-003 | completed | task_key=review-fat-package | Review FAT Package" not in output


def test_task_list_filters_tasks_by_task_ref_resolved_by_task_key_and_status_with_and_logic(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
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
        "list",
        "--task-ref",
        " Execute FAT ",
        "--status",
        "completed",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-003 | completed | task_key=review-fat-package | Review FAT Package" not in output


def test_task_list_invalid_task_ref_filter_returns_no_tasks(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
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
        "list",
        "--task-ref",
        "***",
        "--show-task-key",
    )

    assert result.returncode == 0
    assert "No tasks found." in result.stdout
    assert "Tasks:" not in result.stdout

def test_task_list_filters_tasks_by_dependency_ref_task_id_with_show_task_key_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": ["TASK-001"],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
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
        "list",
        "--dependency-ref",
        "TASK-001",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-002 | planned | task_key=execute-fat | Execute FAT" in output
    assert "- TASK-003 | completed | task_key=review-fat-package | Review FAT Package" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-004 | planned | task_key=archive-fat-package | Archive FAT Package" not in output


def test_task_list_filters_tasks_by_dependency_ref_resolved_by_task_key_and_status_with_and_logic(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
                        "dependencies": ["TASK-002"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "task",
        "list",
        "--dependency-ref",
        " Execute FAT ",
        "--status",
        "completed",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-003 | completed | task_key=review-fat-package | Review FAT Package" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" not in output
    assert "- TASK-004 | planned | task_key=archive-fat-package | Archive FAT Package" not in output


def test_task_list_invalid_dependency_ref_filter_returns_no_tasks(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
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
        "list",
        "--dependency-ref",
        "***",
        "--show-task-key",
    )

    assert result.returncode == 0
    assert "No tasks found." in result.stdout
    assert "Tasks:" not in result.stdout

def test_task_list_filters_tasks_by_dependent_ref_task_id_with_show_task_key_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
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
        "list",
        "--dependent-ref",
        "TASK-003",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" in output
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" in output
    assert "- TASK-003 | planned | task_key=review-fat-package | Review FAT Package" not in output
    assert "- TASK-004 | planned | task_key=archive-fat-package | Archive FAT Package" not in output


def test_task_list_filters_tasks_by_dependent_ref_resolved_by_task_key_and_status_with_and_logic(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "archive-fat-package",
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
        "list",
        "--dependent-ref",
        " Review FAT Package ",
        "--status",
        "completed",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-003 | planned | task_key=review-fat-package | Review FAT Package" not in output
    assert "- TASK-004 | completed | task_key=archive-fat-package | Archive FAT Package" not in output


def test_task_list_invalid_dependent_ref_filter_returns_no_tasks(restore_state_file):
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
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
        "list",
        "--dependent-ref",
        "***",
        "--show-task-key",
    )

    assert result.returncode == 0
    assert "No tasks found." in result.stdout
    assert "Tasks:" not in result.stdout

def test_task_list_filters_tasks_by_has_dependents_true_with_show_task_key_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
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
        "list",
        "--has-dependents",
        "true",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" in output
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" in output
    assert "- TASK-003 | planned | task_key=review-fat-package | Review FAT Package" not in output
    assert "- TASK-004 | planned | task_key=<none> | Archive FAT Package" not in output


def test_task_list_filters_tasks_by_has_dependents_false_with_show_task_key_flag(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": None,
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
        "list",
        "--has-dependents",
        "false",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-003 | planned | task_key=review-fat-package | Review FAT Package" in output
    assert "- TASK-004 | planned | task_key=<none> | Archive FAT Package" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" not in output


def test_task_list_filters_tasks_by_has_dependents_and_status_with_and_logic(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": None,
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
        "list",
        "--has-dependents",
        "true",
        "--status",
        "completed",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-003 | planned | task_key=review-fat-package | Review FAT Package" not in output
    assert "- TASK-004 | completed | task_key=<none> | Archive FAT Package" not in output
def test_task_list_combines_task_ref_dependency_ref_and_dependent_ref_with_shared_reference_resolution(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
                        "dependencies": ["TASK-003"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "task",
        "list",
        "--task-ref",
        " Review FAT Package ",
        "--dependency-ref",
        " Execute FAT ",
        "--dependent-ref",
        "Archive FAT Package",
        "--show-task-key",
    )

    assert result.returncode == 0
    output = result.stdout
    assert output.count("Tasks:") == 1
    assert "- TASK-003 | completed | task_key=review-fat-package | Review FAT Package" in output
    assert "- TASK-001 | planned | task_key=prepare-fat | Prepare FAT" not in output
    assert "- TASK-002 | completed | task_key=execute-fat | Execute FAT" not in output
    assert "- TASK-004 | planned | task_key=archive-fat-package | Archive FAT Package" not in output


def test_task_list_invalid_task_ref_still_returns_no_tasks_with_other_reference_filters_present(
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
                        "title": "Prepare FAT",
                        "status": "planned",
                        "description": None,
                        "task_key": "prepare-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "description": None,
                        "task_key": "execute-fat",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT Package",
                        "status": "completed",
                        "description": None,
                        "task_key": "review-fat-package",
                        "dependencies": ["TASK-001", "TASK-002"],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT Package",
                        "status": "planned",
                        "description": None,
                        "task_key": "archive-fat-package",
                        "dependencies": ["TASK-003"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "task",
        "list",
        "--task-ref",
        "***",
        "--dependency-ref",
        "Execute FAT",
        "--dependent-ref",
        "Archive FAT Package",
        "--show-task-key",
    )

    assert result.returncode == 0
    assert "No tasks found." in result.stdout
    assert "Tasks:" not in result.stdout