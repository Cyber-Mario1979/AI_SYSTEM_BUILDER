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


def test_orchestrate_wp_handles_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_orchestrate_wp_handles_missing_work_package_id(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.8.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-999")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout


def test_orchestrate_wp_reports_binding_context_required(restore_state_file):
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
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "binding_context_required"
    assert payload["blocking_conditions"] == ["selector_context_missing"]
    assert payload["selector_context_ready"] is False


def test_orchestrate_wp_reports_selection_required_when_no_bound_committed_collection_exists(
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
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "selection_required"
    assert payload["blocking_conditions"] == ["bound_committed_collection_missing"]
    assert payload["bound_committed_collection_ids"] == []


def test_orchestrate_wp_reports_planning_setup_required_when_no_plan_exists(
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
                        "duration": 1,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "work_package_id": "WP-001",
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "planning_setup_required"
    assert payload["blocking_conditions"] == ["draft_plan_missing"]
    assert payload["bound_committed_task_ids"] == ["TASK-001"]


def test_orchestrate_wp_reports_plan_generation_required_for_ready_draft_plan(
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
                        "duration": 1,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "work_package_id": "WP-001",
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
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
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "plan_generation_required"
    assert payload["selected_plan_id"] == "PLAN-001"


def test_orchestrate_wp_reports_plan_commit_required_for_generated_draft_plan(
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
                        "duration": 1,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "work_package_id": "WP-001",
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
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
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "plan_commit_required"
    assert payload["selected_plan_id"] == "PLAN-001"


def test_orchestrate_wp_reports_execution_ready_for_committed_plan(
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
                        "duration": 1,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "work_package_id": "WP-001",
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
                "plans": [
                    {
                        "plan_id": "PLAN-001",
                        "work_package_id": "WP-001",
                        "plan_state": "committed",
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
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "execution_ready"
    assert payload["selected_plan_id"] == "PLAN-001"


def test_orchestrate_wp_blocks_on_multiple_draft_plans(restore_state_file):
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
                        "duration": 1,
                        "start_date": None,
                        "end_date": None,
                        "task_key": "prepare-fat",
                        "work_package_id": "WP-001",
                        "status": "planned",
                        "dependencies": [],
                    }
                ],
                "work_packages": [make_bound_context_work_package_payload()],
                "task_collections": [
                    {
                        "collection_id": "TC-001",
                        "title": "Committed Selection",
                        "collection_state": "committed",
                        "work_package_id": "WP-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
                "plans": [
                    {
                        "plan_id": "PLAN-001",
                        "work_package_id": "WP-001",
                        "plan_state": "draft",
                    },
                    {
                        "plan_id": "PLAN-002",
                        "work_package_id": "WP-001",
                        "plan_state": "draft",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli("orchestrate", "wp", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["orchestration_stage"] == "blocked"
    assert payload["blocking_conditions"] == ["multiple_draft_plans"]
