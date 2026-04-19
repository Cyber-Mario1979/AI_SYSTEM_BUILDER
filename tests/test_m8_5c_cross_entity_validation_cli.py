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


def make_bound_context_work_package_payload(
    wp_id: str = "WP-001",
    title: str = "Tablet press qualification",
) -> dict:
    return {
        "wp_id": wp_id,
        "title": title,
        "status": "open",
        "selector_context": {
            "preset_id": "oral-solid-dose-standard",
            "scope_intent": "qualification-only",
            "standards_bundles": ["cqv-core", "automation"],
        },
    }


def make_generated_task_plan_payload(task_id: str) -> dict:
    return {
        "task_id": task_id,
        "sequence_order": 1,
        "duration_days": 1,
        "dependency_task_ids": [],
        "planned_start_at": "2026-04-13T08:30:00+00:00",
        "planned_finish_at": "2026-04-13T16:30:00+00:00",
    }


def test_wp_delete_rejects_delete_when_collections_are_still_bound_and_preserves_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
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
                "title": "Committed Selection",
                "collection_state": "committed",
                "work_package_id": "WP-001",
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("wp", "delete", "WP-001")

    assert result.returncode == 0
    assert (
        "Work Package cannot be deleted while collections are bound: "
        "WP-001 -> [TC-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_wp_delete_rejects_delete_when_plans_are_still_associated_and_preserves_state(
    restore_state_file,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    original_state = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
            make_bound_context_work_package_payload("WP-002", "Blister line upgrade"),
        ],
        "task_collections": [],
        "plans": [
            {
                "plan_id": "PLAN-001",
                "work_package_id": "WP-001",
                "plan_state": "draft",
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("wp", "delete", "WP-001")

    assert result.returncode == 0
    assert (
        "Work Package cannot be deleted while plans are associated: "
        "WP-001 -> [PLAN-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_task_clear_work_package_rejects_when_plans_still_reference_task_and_preserves_state(
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
                "duration": 1,
                "start_date": None,
                "end_date": None,
                "task_key": "prepare-fat",
                "work_package_id": "WP-001",
                "status": "planned",
                "dependencies": [],
            }
        ],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
        ],
        "task_collections": [],
        "plans": [
            {
                "plan_id": "PLAN-001",
                "work_package_id": "WP-001",
                "plan_state": "draft",
                "planning_basis": {
                    "duration_source": "task_duration",
                },
                "planned_start_at": "2026-04-13T08:30:00+00:00",
                "planning_calendar": {
                    "working_days": ["monday", "wednesday", "friday"],
                    "workday_hours": 8,
                    "workmonth_mode": "calendar_month",
                },
                "generated_task_plans": [
                    make_generated_task_plan_payload("TASK-001")
                ],
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("task", "clear-work-package", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task work package cannot be cleared while plans still reference it: "
        "TASK-001 -> [PLAN-001 (WP-001)]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_task_delete_rejects_when_generated_plan_still_references_task_and_preserves_state(
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
                "duration": 1,
                "start_date": None,
                "end_date": None,
                "task_key": "prepare-fat",
                "work_package_id": "WP-001",
                "status": "planned",
                "dependencies": [],
            }
        ],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
        ],
        "task_collections": [],
        "plans": [
            {
                "plan_id": "PLAN-001",
                "work_package_id": "WP-001",
                "plan_state": "draft",
                "planning_basis": {
                    "duration_source": "task_duration",
                },
                "planned_start_at": "2026-04-13T08:30:00+00:00",
                "planning_calendar": {
                    "working_days": ["monday", "wednesday", "friday"],
                    "workday_hours": 8,
                    "workmonth_mode": "calendar_month",
                },
                "generated_task_plans": [
                    make_generated_task_plan_payload("TASK-001")
                ],
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("task", "delete", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task cannot be deleted while plans still reference it: "
        "TASK-001 -> [PLAN-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state


def test_task_delete_rejects_when_plan_dependencies_still_reference_task_and_preserves_state(
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
                "duration": 1,
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
                "duration": 1,
                "start_date": None,
                "end_date": None,
                "task_key": "execute-fat",
                "work_package_id": "WP-001",
                "status": "planned",
                "dependencies": ["TASK-001"],
            },
        ],
        "work_packages": [
            make_bound_context_work_package_payload("WP-001"),
        ],
        "task_collections": [],
        "plans": [
            {
                "plan_id": "PLAN-001",
                "work_package_id": "WP-001",
                "plan_state": "draft",
                "planning_basis": {
                    "duration_source": "task_duration",
                },
                "planned_start_at": "2026-04-13T08:30:00+00:00",
                "planning_calendar": {
                    "working_days": ["monday", "wednesday", "friday"],
                    "workday_hours": 8,
                    "workmonth_mode": "calendar_month",
                },
                "generated_task_plans": [
                    {
                        "task_id": "TASK-001",
                        "sequence_order": 1,
                        "duration_days": 1,
                        "dependency_task_ids": [],
                        "planned_start_at": "2026-04-13T08:30:00+00:00",
                        "planned_finish_at": "2026-04-13T16:30:00+00:00",
                    },
                    {
                        "task_id": "TASK-002",
                        "sequence_order": 2,
                        "duration_days": 1,
                        "dependency_task_ids": ["TASK-001"],
                        "planned_start_at": "2026-04-15T08:30:00+00:00",
                        "planned_finish_at": "2026-04-15T16:30:00+00:00",
                    },
                ],
            }
        ],
    }
    STATE_FILE.write_text(
        json.dumps(original_state, indent=2),
        encoding="utf-8",
    )

    result = run_cli("task", "delete", "TASK-001")

    assert result.returncode == 0
    assert (
        "Task cannot be deleted while plans still reference it: "
        "TASK-001 -> [PLAN-001]"
    ) in result.stdout

    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved_state == original_state
