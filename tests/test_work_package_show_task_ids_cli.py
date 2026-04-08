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


def test_wp_show_show_task_ids_flag_displays_associated_task_ids_in_persisted_task_order(
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
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "planned",
                        "work_package_id": "WP-001",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-001",
                        "order": 1,
                        "title": "Prepare FAT",
                        "status": "planned",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Review FAT",
                        "status": "completed",
                        "work_package_id": "WP-001",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-004",
                        "order": 4,
                        "title": "Archive FAT",
                        "status": "planned",
                        "work_package_id": "WP-002",
                        "dependencies": [],
                    },
                ],
                "work_packages": [
                    {
                        "wp_id": "WP-001",
                        "title": "Tablet press qualification",
                        "status": "open",
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Packaging line qualification",
                        "status": "in_progress",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "show", "WP-001", "--show-task-ids")

    assert result.returncode == 0
    payload = json.loads(result.stdout)

    assert payload == {
        "wp_id": "WP-001",
        "title": "Tablet press qualification",
        "status": "open",
        "task_ids": ["TASK-002", "TASK-003"],
    }


def test_wp_show_show_task_ids_flag_returns_empty_list_when_work_package_has_no_tasks(
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
                        "work_package_id": "WP-002",
                        "dependencies": [],
                    }
                ],
                "work_packages": [
                    {
                        "wp_id": "WP-001",
                        "title": "Tablet press qualification",
                        "status": "open",
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Packaging line qualification",
                        "status": "in_progress",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "show", "WP-001", "--show-task-ids")

    assert result.returncode == 0
    payload = json.loads(result.stdout)

    assert payload == {
        "wp_id": "WP-001",
        "title": "Tablet press qualification",
        "status": "open",
        "task_ids": [],
    }


def test_wp_show_preserves_default_contract_without_show_task_ids_flag(
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
                        "work_package_id": "WP-001",
                        "dependencies": [],
                    }
                ],
                "work_packages": [
                    {
                        "wp_id": "WP-001",
                        "title": "Tablet press qualification",
                        "status": "open",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "show", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)

    assert payload == {
        "wp_id": "WP-001",
        "title": "Tablet press qualification",
        "status": "open",
    }


def test_wp_show_show_task_ids_flag_handles_missing_work_package_id(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [
                    {
                        "wp_id": "WP-001",
                        "title": "Tablet press qualification",
                        "status": "open",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "show", "WP-999", "--show-task-ids")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout


def test_wp_show_show_task_ids_flag_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "show", "WP-001", "--show-task-ids")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout
