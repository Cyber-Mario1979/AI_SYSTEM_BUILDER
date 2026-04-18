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


def test_collection_add_persists_new_collection_with_default_source_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "add", "Source Pool")

    assert result.returncode == 0
    assert "Collection added: TC-001 - Source Pool (source)" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Source Pool",
            "collection_state": "source",
        }
    ]


def test_collection_add_accepts_explicit_collection_state(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "collection",
        "add",
        "Committed Selection",
        "--collection-state",
        "committed",
    )

    assert result.returncode == 0
    assert (
        "Collection added: TC-001 - Committed Selection (committed)"
        in result.stdout
    )

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Committed Selection",
            "collection_state": "committed",
        }
    ]


def test_collection_add_generates_next_collection_id_from_existing_state(
    restore_state_file,
):
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
                        "title": "First Pool",
                        "collection_state": "source",
                    },
                    {
                        "collection_id": "TC-007",
                        "title": "Seventh Pool",
                        "collection_state": "staged",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "add", "Next Pool")

    assert result.returncode == 0
    assert "Collection added: TC-008 - Next Pool (source)" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"][-1] == {
        "collection_id": "TC-008",
        "title": "Next Pool",
        "collection_state": "source",
    }


def test_collection_add_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("collection", "add", "Source Pool")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_collection_add_rejects_invalid_empty_title_without_mutating_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "add", "")

    assert result.returncode == 0
    assert "Collection validation failed:" in result.stdout
    assert "title" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == []


def test_collection_add_rejects_invalid_collection_state_at_parser_level():
    result = run_cli(
        "collection",
        "add",
        "Source Pool",
        "--collection-state",
        "draft",
    )

    assert result.returncode != 0
    combined_output = result.stdout + result.stderr
    assert "invalid choice" in combined_output

def test_collection_show_prints_matching_collection_as_json(restore_state_file):
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
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "show", "TC-002")

    assert result.returncode == 0
    payload = json.loads(result.stdout)

    assert payload == {
    "collection_id": "TC-002",
    "title": "Committed Selection",
    "collection_state": "committed",
    "task_ids": [],
    }


def test_collection_show_handles_missing_collection_id(restore_state_file):
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

    result = run_cli("collection", "show", "TC-999")

    assert result.returncode == 0
    assert "Collection not found: TC-999" in result.stdout


def test_collection_show_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("collection", "show", "TC-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout

def test_collection_list_shows_no_collections_message_for_empty_collection(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "not_started",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "list")

    assert result.returncode == 0
    assert "No collections found." in result.stdout
    assert "Collections:" not in result.stdout


def test_collection_list_shows_all_collections_in_persisted_order(restore_state_file):
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
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "list")

    assert result.returncode == 0
    output = result.stdout
    assert "Collections:" in output

    first_row = "- TC-001 | source | Source Pool"
    second_row = "- TC-002 | committed | Committed Selection"

    assert first_row in output
    assert second_row in output
    assert output.index(first_row) < output.index(second_row)


def test_collection_list_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("collection", "list")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_collection_list_filters_by_collection_state_without_changing_output_format(
    restore_state_file,
):
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
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Staged Selection",
                        "collection_state": "staged",
                    },
                    {
                        "collection_id": "TC-003",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "list", "--collection-state", "staged")

    assert result.returncode == 0
    output = result.stdout
    assert "Collections:" in output
    assert "- TC-002 | staged | Staged Selection" in output
    assert "- TC-001 | source | Source Pool" not in output
    assert "- TC-003 | committed | Committed Selection" not in output


def test_collection_list_collection_state_filter_shows_no_collections_message_when_no_matches(
    restore_state_file,
):
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

    result = run_cli("collection", "list", "--collection-state", "committed")

    assert result.returncode == 0
    assert "No collections found." in result.stdout
    assert "Collections:" not in result.stdout


def test_collection_list_filters_by_exact_title_using_and_logic(restore_state_file):
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
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Source Pool",
                        "collection_state": "staged",
                    },
                    {
                        "collection_id": "TC-003",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "collection",
        "list",
        "--collection-state",
        "source",
        "--title",
        "Source Pool",
    )

    assert result.returncode == 0
    output = result.stdout
    assert "Collections:" in output
    assert "- TC-001 | source | Source Pool" in output
    assert "- TC-002 | staged | Source Pool" not in output
    assert "- TC-003 | committed | Committed Selection" not in output


def test_collection_list_filters_by_exact_collection_id_without_changing_output_format(
    restore_state_file,
):
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
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "list", "--collection-id", "TC-002")

    assert result.returncode == 0
    output = result.stdout
    assert "Collections:" in output
    assert "- TC-002 | committed | Committed Selection" in output
    assert "- TC-001 | source | Source Pool" not in output

def test_collection_update_title_updates_only_title(restore_state_file):
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

    result = run_cli("collection", "update-title", "TC-001", "Refined Pool")

    assert result.returncode == 0
    assert "Collection title updated: TC-001 -> Refined Pool" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Refined Pool",
            "collection_state": "source",
        }
    ]


def test_collection_update_title_handles_missing_collection_id(restore_state_file):
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

    result = run_cli("collection", "update-title", "TC-999", "Refined Pool")

    assert result.returncode == 0
    assert "Collection not found: TC-999" in result.stdout


def test_collection_update_title_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("collection", "update-title", "TC-001", "Refined Pool")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_collection_update_title_rejects_invalid_empty_title_without_mutating_state(
    restore_state_file,
):
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

    result = run_cli("collection", "update-title", "TC-001", "")

    assert result.returncode == 0
    assert "Collection validation failed:" in result.stdout
    assert "title" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Source Pool",
            "collection_state": "source",
        }
    ]


def test_collection_update_state_updates_only_collection_state(restore_state_file):
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

    result = run_cli("collection", "update-state", "TC-001", "committed")

    assert result.returncode == 0
    assert "Collection state updated: TC-001 -> committed" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Source Pool",
            "collection_state": "committed",
        }
    ]


def test_collection_update_state_handles_missing_collection_id(restore_state_file):
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

    result = run_cli("collection", "update-state", "TC-999", "committed")

    assert result.returncode == 0
    assert "Collection not found: TC-999" in result.stdout


def test_collection_update_state_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("collection", "update-state", "TC-001", "committed")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_collection_update_state_rejects_invalid_collection_state_at_parser_level():
    result = run_cli("collection", "update-state", "TC-001", "draft")

    assert result.returncode != 0
    combined_output = result.stdout + result.stderr
    assert "invalid choice" in combined_output

def test_collection_add_task_rejects_duplicate_membership_without_mutating_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
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
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("collection", "add-task", "TC-001", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task already associated with collection: TASK-001 -> TC-001"
        in result.stdout
    )

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_collection_add_task_rejects_conflicting_non_source_membership_without_mutating_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
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
                "title": "Staged Selection",
                "collection_state": "staged",
                "task_ids": ["TASK-001"],
            },
            {
                "collection_id": "TC-002",
                "title": "Committed Selection",
                "collection_state": "committed",
            },
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("collection", "add-task", "TC-002", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task already associated with a different non-source collection: "
        "TASK-001 -> TC-001 (staged)"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_collection_add_task_allows_source_membership_alongside_non_source_membership(
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
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "task_ids": ["TASK-001"],
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Source Pool",
                        "collection_state": "source",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "add-task", "TC-002", "TASK-001")

    assert result.returncode == 0
    assert "Task added to collection: TC-002 <- TASK-001" in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state["task_collections"] == [
        {
            "collection_id": "TC-001",
            "title": "Committed Selection",
            "collection_state": "committed",
            "task_ids": ["TASK-001"],
        },
        {
            "collection_id": "TC-002",
            "title": "Source Pool",
            "collection_state": "source",
            "task_ids": ["TASK-001"],
        },
    ]    
def test_collection_show_show_work_package_id_flag_displays_bound_work_package_id(
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
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "show", "TC-001", "--show-work-package-id")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload == {
        "collection_id": "TC-001",
        "title": "Committed Selection",
        "collection_state": "committed",
        "work_package_id": "WP-001",
        "task_ids": ["TASK-001"],
    }


def test_collection_list_show_work_package_id_and_task_ids_displays_cross_entity_fields(
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
                    }
                ],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001", "TASK-002"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "collection",
        "list",
        "--show-work-package-id",
        "--show-task-ids",
    )

    assert result.returncode == 0
    assert (
        "- TC-001 | committed | work_package_id=WP-001 | "
        "task_ids=[TASK-001, TASK-002] | Committed Selection"
    ) in result.stdout


def test_collection_list_filters_by_work_package_id(restore_state_file):
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
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Blister line upgrade",
                        "status": "open",
                    },
                ],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "WP-001 Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "WP-002 Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-002",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "list", "--work-package-id", "WP-002")

    assert result.returncode == 0
    assert "- TC-002 | committed | WP-002 Selection" in result.stdout
    assert "- TC-001 | committed | WP-001 Selection" not in result.stdout


def test_collection_list_filters_by_task_id(restore_state_file):
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
                ],
                "work_packages": [],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "First Selection",
                        "collection_state": "committed",
                        "task_ids": ["TASK-001"],
                    },
                    {
                        "collection_id": "TC-002",
                        "title": "Second Selection",
                        "collection_state": "source",
                        "task_ids": ["TASK-002"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("collection", "list", "--task-id", "TASK-002")

    assert result.returncode == 0
    assert "- TC-002 | source | Second Selection" in result.stdout
    assert "- TC-001 | committed | First Selection" not in result.stdout