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


def test_wp_list_filters_by_exact_associated_task_id_without_changing_output_format(
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
                    },
                    {
                        "task_id": "TASK-002",
                        "order": 2,
                        "title": "Execute FAT",
                        "status": "completed",
                        "work_package_id": "WP-002",
                        "dependencies": [],
                    },
                    {
                        "task_id": "TASK-003",
                        "order": 3,
                        "title": "Archive FAT",
                        "status": "planned",
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

    result = run_cli("wp", "list", "--task-id", "TASK-001")

    assert result.returncode == 0
    output = result.stdout
    assert "Work Packages:" in output
    assert "- WP-001 | open | Tablet press qualification" in output
    assert "- WP-002 | in_progress | Packaging line qualification" not in output


def test_wp_list_task_id_filter_shows_no_work_packages_message_when_no_matches(
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

    result = run_cli("wp", "list", "--task-id", "TASK-999")

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout


def test_wp_list_task_id_filter_combines_with_status_using_and_logic(
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
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Packaging line qualification",
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list", "--task-id", "TASK-001", "--status", "completed")

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout


def test_wp_list_task_id_filter_combines_with_title_using_and_logic(
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
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Packaging line qualification",
                        "status": "open",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "wp",
        "list",
        "--task-id",
        "TASK-001",
        "--title",
        "Packaging line qualification",
    )

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout


def test_wp_list_task_id_filter_combines_with_wp_id_using_and_logic(
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
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Packaging line qualification",
                        "status": "open",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list", "--task-id", "TASK-001", "--wp-id", "WP-002")

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout

