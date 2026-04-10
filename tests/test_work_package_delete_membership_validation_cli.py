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


def test_wp_delete_rejects_delete_when_tasks_are_still_associated_and_preserves_state(
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
                "work_package_id": "WP-001",
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
                "title": "Blister line upgrade",
                "status": "open",
            },
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("wp", "delete", "WP-001")

    assert result.returncode == 0
    assert (
        "Work Package cannot be deleted while tasks are associated: "
        "WP-001 -> [TASK-001, TASK-002]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_wp_delete_allows_delete_when_no_tasks_are_associated_to_target_work_package(
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
                        "work_package_id": "WP-002",
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
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "delete", "WP-001")

    assert result.returncode == 0
    assert "Work Package deleted: WP-001" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["work_packages"] == [
        {
            "wp_id": "WP-002",
            "title": "Blister line upgrade",
            "status": "open",
        }
    ]
    assert saved_state["tasks"][0]["work_package_id"] == "WP-002"

def test_collection_remove_task_removes_existing_membership_and_omits_empty_task_ids_on_save(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
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
                    }
                ],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                        "task_ids": ["TASK-001"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "remove-task", "TC-001", "TASK-001")

    assert result.returncode == 0
    assert "Task removed from collection: TC-001 <- TASK-001" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Source Pool",
            "collection_state": "source",
        }
    ]


def test_collection_remove_task_resolves_target_by_task_key(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
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
                    }
                ],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                        "task_ids": ["TASK-001"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "remove-task", "TC-001", "prepare-fat")

    assert result.returncode == 0
    assert "Task removed from collection: TC-001 <- TASK-001" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Source Pool",
            "collection_state": "source",
        }
    ]


def test_collection_remove_task_is_idempotent_for_non_member_task(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
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
                    }
                ],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "remove-task", "TC-001", "TASK-001")

    assert result.returncode == 0
    assert "Task removed from collection: TC-001 <- TASK-001" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Source Pool",
            "collection_state": "source",
        }
    ]


def test_collection_remove_task_handles_unknown_collection_id(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
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
                    }
                ],
                "work_packages": [],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "remove-task", "TC-999", "TASK-001")

    assert result.returncode == 0
    assert "Collection not found: TC-999" in result.stdout


def test_collection_remove_task_handles_unknown_task_reference(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Source Pool",
                        "collection_state": "source",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "remove-task", "TC-001", "TASK-999")

    assert result.returncode == 0
    assert "Task not found: TASK-999" in result.stdout


def test_collection_remove_task_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("collection", "remove-task", "TC-001", "TASK-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout

    
        