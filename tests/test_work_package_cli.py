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


def test_wp_list_shows_no_work_packages_message_for_empty_collection(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list")

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout


def test_wp_list_shows_all_work_packages_in_persisted_order(restore_state_file):
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
                        "status": "in_progress",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list")

    assert result.returncode == 0
    output = result.stdout
    assert "Work Packages:" in output

    first_row = "- WP-001 | open | Tablet press qualification"
    second_row = "- WP-002 | in_progress | Blister line upgrade"

    assert first_row in output
    assert second_row in output
    assert output.index(first_row) < output.index(second_row)


def test_wp_list_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "list")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_wp_show_prints_matching_work_package_as_json(restore_state_file):
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
                        "status": "in_progress",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "show", "WP-002")

    assert result.returncode == 0
    payload = json.loads(result.stdout)

    assert payload == {
        "wp_id": "WP-002",
        "title": "Blister line upgrade",
        "status": "in_progress",
    }


def test_wp_show_handles_missing_work_package_id(restore_state_file):
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

    result = run_cli("wp", "show", "WP-999")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout


def test_wp_show_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "show", "WP-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_wp_add_persists_new_work_package_with_default_open_status(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "add", "WP-001", "Tablet press qualification")

    assert result.returncode == 0
    assert "Work Package added: WP-001 - Tablet press qualification" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]


def test_wp_add_rejects_duplicate_wp_id_without_mutating_state(restore_state_file):
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

    result = run_cli("wp", "add", "WP-001", "Duplicate title")

    assert result.returncode == 0
    assert "Duplicate wp_id is not allowed: WP-001" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]


def test_wp_add_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "add", "WP-001", "Tablet press qualification")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_wp_add_rejects_invalid_wp_id_format(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "add", "WP-1", "Tablet press qualification")

    assert result.returncode == 0
    assert "Work Package validation failed:" in result.stdout
    assert "wp_id" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == []

def test_wp_delete_removes_existing_work_package_only(restore_state_file):
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
                        "status": "completed",
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

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-002",
            "title": "Blister line upgrade",
            "status": "completed",
        }
    ]


def test_wp_delete_handles_missing_work_package_id(restore_state_file):
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

    result = run_cli("wp", "delete", "WP-999")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]


def test_wp_delete_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "delete", "WP-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout    

def test_wp_update_title_updates_only_existing_work_package_title(restore_state_file):
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
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "update-title", "WP-002", "Blister line modernization")

    assert result.returncode == 0
    assert "Work Package title updated: WP-002 -> Blister line modernization" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        },
        {
            "wp_id": "WP-002",
            "title": "Blister line modernization",
            "status": "completed",
        },
    ]


def test_wp_update_title_handles_missing_work_package_id(restore_state_file):
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

    result = run_cli("wp", "update-title", "WP-999", "Missing work package")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]


def test_wp_update_title_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "update-title", "WP-001", "Tablet press modernization")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_wp_update_title_rejects_invalid_empty_title_without_mutating_state(restore_state_file):
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

    result = run_cli("wp", "update-title", "WP-001", "")

    assert result.returncode == 0
    assert "Work Package validation failed:" in result.stdout
    assert "title" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]    

def test_wp_list_filters_by_status_without_changing_output_format(restore_state_file):
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
                        "status": "completed",
                    },
                    {
                        "wp_id": "WP-003",
                        "title": "Granulation refresh",
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list", "--status", "completed")

    assert result.returncode == 0
    output = result.stdout
    assert "Work Packages:" in output
    assert "- WP-002 | completed | Blister line upgrade" in output
    assert "- WP-003 | completed | Granulation refresh" in output
    assert "- WP-001 | open | Tablet press qualification" not in output


def test_wp_list_status_filter_shows_no_work_packages_message_when_no_matches(restore_state_file):
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

    result = run_cli("wp", "list", "--status", "completed")

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout


def test_wp_list_status_filter_rejects_invalid_choice_at_parser_level():
    result = run_cli("wp", "list", "--status", "planned")

    assert result.returncode != 0
    combined_output = result.stdout + result.stderr
    assert "invalid choice" in combined_output

def test_wp_list_filters_by_exact_title_without_changing_output_format(restore_state_file):
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
                        "status": "completed",
                    },
                    {
                        "wp_id": "WP-003",
                        "title": "Blister line modernization",
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list", "--title", "Blister line upgrade")

    assert result.returncode == 0
    output = result.stdout
    assert "Work Packages:" in output
    assert "- WP-002 | completed | Blister line upgrade" in output
    assert "- WP-001 | open | Tablet press qualification" not in output
    assert "- WP-003 | completed | Blister line modernization" not in output


def test_wp_list_title_filter_shows_no_work_packages_message_when_no_matches(restore_state_file):
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

    result = run_cli("wp", "list", "--title", "Blister line upgrade")

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout


def test_wp_list_title_filter_combines_with_status_using_and_logic(restore_state_file):
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
                        "title": "Blister line upgrade",
                        "status": "open",
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Blister line upgrade",
                        "status": "completed",
                    },
                    {
                        "wp_id": "WP-003",
                        "title": "Granulation refresh",
                        "status": "completed",
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
        "--status",
        "completed",
        "--title",
        "Blister line upgrade",
    )

    assert result.returncode == 0
    output = result.stdout
    assert "Work Packages:" in output
    assert "- WP-002 | completed | Blister line upgrade" in output
    assert "- WP-001 | open | Blister line upgrade" not in output
    assert "- WP-003 | completed | Granulation refresh" not in output

def test_wp_list_filters_by_exact_wp_id_without_changing_output_format(restore_state_file):
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
                        "status": "completed",
                    },
                    {
                        "wp_id": "WP-003",
                        "title": "Granulation refresh",
                        "status": "completed",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "list", "--wp-id", "WP-002")

    assert result.returncode == 0
    output = result.stdout
    assert "Work Packages:" in output
    assert "- WP-002 | completed | Blister line upgrade" in output
    assert "- WP-001 | open | Tablet press qualification" not in output
    assert "- WP-003 | completed | Granulation refresh" not in output


def test_wp_list_wp_id_filter_shows_no_work_packages_message_when_no_matches(restore_state_file):
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

    result = run_cli("wp", "list", "--wp-id", "WP-999")

    assert result.returncode == 0
    assert "No work packages found." in result.stdout
    assert "Work Packages:" not in result.stdout


def test_wp_list_wp_id_filter_combines_with_status_using_and_logic(restore_state_file):
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
                        "title": "Blister line upgrade",
                        "status": "open",
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Blister line upgrade",
                        "status": "completed",
                    },
                    {
                        "wp_id": "WP-003",
                        "title": "Granulation refresh",
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
        "--status",
        "open",
        "--wp-id",
        "WP-001",
    )

    assert result.returncode == 0
    output = result.stdout
    assert "Work Packages:" in output
    assert "- WP-001 | open | Blister line upgrade" in output
    assert "- WP-002 | completed | Blister line upgrade" not in output
    assert "- WP-003 | open | Granulation refresh" not in output

def test_wp_set_selector_type_persists_selector_context_for_target_work_package_only(
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
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Blister line upgrade",
                        "status": "in_progress",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "set-selector-type", "WP-001", "process-equipment")

    assert result.returncode == 0
    assert (
        "Work Package selector type updated: WP-001 -> process-equipment"
        in result.stdout
    )

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
            "selector_context": {
                "system_type": "process-equipment",
            },
        },
        {
            "wp_id": "WP-002",
            "title": "Blister line upgrade",
            "status": "in_progress",
        },
    ]


def test_wp_set_selector_type_handles_missing_work_package_id(restore_state_file):
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

    result = run_cli("wp", "set-selector-type", "WP-999", "process-equipment")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout


def test_wp_set_selector_type_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "set-selector-type", "WP-001", "process-equipment")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_wp_set_selector_type_rejects_invalid_empty_value_without_mutating_state(
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

    result = run_cli("wp", "set-selector-type", "WP-001", "")

    assert result.returncode == 0
    assert "Work Package validation failed:" in result.stdout
    assert "system_type" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]


def test_wp_show_show_selector_context_flag_displays_selector_context(
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
                        "selector_context": {
                            "system_type": "process-equipment",
                        },
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "show", "WP-001", "--show-selector-context")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload == {
        "wp_id": "WP-001",
        "title": "Tablet press qualification",
        "status": "open",
        "selector_context": {
            "system_type": "process-equipment",
        },
    }


def test_wp_show_preserves_default_contract_without_show_selector_context_flag(
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
                        "selector_context": {
                            "system_type": "process-equipment",
                        },
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
def test_wp_set_preset_persists_preset_id_for_target_work_package_only(
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
                    },
                    {
                        "wp_id": "WP-002",
                        "title": "Blister line upgrade",
                        "status": "in_progress",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "set-preset", "WP-001", "oral-solid-dose-standard")

    assert result.returncode == 0
    assert (
        "Work Package preset updated: "
        "WP-001 -> oral-solid-dose-standard"
        in result.stdout
    )

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
            "selector_context": {
                "preset_id": "oral-solid-dose-standard",
            },
        },
        {
            "wp_id": "WP-002",
            "title": "Blister line upgrade",
            "status": "in_progress",
        },
    ]


def test_wp_set_preset_preserves_existing_selector_type(
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
                        "selector_context": {
                            "system_type": "process-equipment",
                        },
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "set-preset", "WP-001", "oral-solid-dose-standard")

    assert result.returncode == 0
    assert (
        "Work Package preset updated: "
        "WP-001 -> oral-solid-dose-standard"
        in result.stdout
    )

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
            "selector_context": {
                "system_type": "process-equipment",
                "preset_id": "oral-solid-dose-standard",
            },
        }
    ]


def test_wp_show_show_selector_context_flag_displays_preset_id_without_null_system_type(
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
                        "selector_context": {
                            "preset_id": "oral-solid-dose-standard",
                        },
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("wp", "show", "WP-001", "--show-selector-context")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload == {
        "wp_id": "WP-001",
        "title": "Tablet press qualification",
        "status": "open",
        "selector_context": {
            "preset_id": "oral-solid-dose-standard",
        },
    }


def test_wp_set_preset_handles_missing_work_package_id(restore_state_file):
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

    result = run_cli("wp", "set-preset", "WP-999", "oral-solid-dose-standard")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout


def test_wp_set_preset_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("wp", "set-preset", "WP-001", "oral-solid-dose-standard")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_wp_set_preset_rejects_invalid_empty_value_without_mutating_state(
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

    result = run_cli("wp", "set-preset", "WP-001", "")

    assert result.returncode == 0
    assert "Work Package validation failed:" in result.stdout
    assert "preset_id" in result.stdout

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"] == [
        {
            "wp_id": "WP-001",
            "title": "Tablet press qualification",
            "status": "open",
        }
    ]