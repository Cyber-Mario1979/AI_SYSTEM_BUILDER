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


def test_task_set_work_package_rejects_conflicting_reassignment_without_mutating_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
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
                "work_package_id": "WP-001",
                "status": "planned",
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
                "title": "Blister line upgrade",
                "status": "open",
            },
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("task", "set-work-package", "TASK-001", "WP-002")

    assert result.returncode == 0
    assert (
        "Task already associated with a different Work Package: "
        "TASK-001 -> WP-001"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_task_set_work_package_allows_idempotent_reattach_to_same_work_package(
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
                        "work_package_id": "WP-001",
                        "status": "planned",
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

    result = run_cli("task", "set-work-package", "prepare-fat", "WP-001")

    assert result.returncode == 0
    assert "Task work package updated: TASK-001 -> WP-001" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["tasks"][0]["work_package_id"] == "WP-001"