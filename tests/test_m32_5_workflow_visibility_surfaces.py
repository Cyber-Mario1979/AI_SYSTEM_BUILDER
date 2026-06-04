import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / "data" / "state" / "state.json"


def run_local_workflow(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "asbp.adapters.local_workflow_cli", *args],
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


def write_state(payload: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def configured_state() -> dict:
    return {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.1.0",
        "status": "in_flight",
        "work_packages": [
            {
                "wp_id": "WP-001",
                "title": "Cleanroom HVAC CQV workflow",
                "status": "open",
                "selector_context": {
                    "system_type": "cleanroom-hvac",
                    "preset_id": "cqv-cleanroom-hvac-basic",
                    "scope_intent": "qualification-only",
                    "standards_bundles": ["cqv-core", "cleanroom-hvac"],
                },
            }
        ],
        "tasks": [
            {
                "task_id": "TASK-001",
                "order": 1,
                "title": "Prepare qualification plan",
                "status": "planned",
                "duration": 2,
                "work_package_id": "WP-001",
                "dependencies": [],
            },
            {
                "task_id": "TASK-002",
                "order": 2,
                "title": "Execute field checks",
                "status": "in_progress",
                "duration": 1,
                "work_package_id": "WP-001",
                "dependencies": ["TASK-001"],
            },
        ],
        "task_collections": [
            {
                "collection_id": "TC-001",
                "title": "Selected cleanroom HVAC source pack",
                "collection_state": "staged",
                "work_package_id": "WP-001",
                "task_ids": ["TASK-001", "TASK-002"],
            }
        ],
        "plans": [],
    }


def state_with_generated_schedule() -> dict:
    payload = configured_state()
    payload["task_collections"][0]["collection_state"] = "committed"
    payload["plans"] = [
        {
            "plan_id": "PLAN-001",
            "work_package_id": "WP-001",
            "plan_state": "draft",
            "planning_basis": {
                "duration_source": "task_duration",
                "basis_label": "Task durations",
            },
            "planned_start_at": "2026-06-08T08:00:00+00:00",
            "planning_calendar": {
                "working_days": [
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                ],
                "workday_hours": 8,
                "workmonth_mode": "calendar_month",
            },
            "generated_task_plans": [
                {
                    "task_id": "TASK-001",
                    "sequence_order": 1,
                    "duration_days": 2,
                    "dependency_task_ids": [],
                    "planned_start_at": "2026-06-08T08:00:00+00:00",
                    "planned_finish_at": "2026-06-09T16:00:00+00:00",
                },
                {
                    "task_id": "TASK-002",
                    "sequence_order": 2,
                    "duration_days": 1,
                    "dependency_task_ids": ["TASK-001"],
                    "planned_start_at": "2026-06-10T08:00:00+00:00",
                    "planned_finish_at": "2026-06-10T16:00:00+00:00",
                },
            ],
        }
    ]
    return payload


def incomplete_state(title: str = "Incomplete workflow") -> dict:
    return {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.1.0",
        "status": "in_flight",
        "work_packages": [
            {
                "wp_id": "WP-001",
                "title": title,
                "status": "open",
            }
        ],
        "tasks": [],
        "task_collections": [],
        "plans": [],
    }


def test_status_outputs_workflow_visibility_state_and_limitations(restore_state_file):
    write_state(configured_state())

    result = run_local_workflow("status", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["checkpoint"] == "M32.5 — Workflow visibility surfaces"
    assert payload["surface"] == "cli-enhanced controlled local workflow"
    assert payload["workflow_state"]["selected_work_package"]["wp_id"] == "WP-001"
    assert payload["task_lifecycle"]["task_count"] == 2
    assert payload["task_lifecycle"]["status_counts"] == {
        "planned": 1,
        "in_progress": 1,
    }
    assert payload["source_and_citation_state"]["collection_ids"] == ["TC-001"]
    assert payload["source_and_citation_state"]["standards_bundles"] == [
        "cqv-core",
        "cleanroom-hvac",
    ]
    assert payload["ai_limitation_state"] == {
        "ai_call_performed": False,
        "provider_call_performed": False,
        "ollama_call_performed": False,
        "human_review_required": True,
        "limitation": "No AI, provider, Ollama, or live model call is performed.",
    }
    assert "No AI, provider, Ollama, or live model call is performed." in payload[
        "limitations"
    ]


def test_status_outputs_schedule_lifecycle_when_plan_exists(restore_state_file):
    write_state(state_with_generated_schedule())

    result = run_local_workflow("status", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["schedule_lifecycle"]["plan_count"] == 1
    assert payload["schedule_lifecycle"]["generated_schedule_present"] is True
    assert payload["schedule_lifecycle"]["plans"] == [
        {
            "plan_id": "PLAN-001",
            "plan_state": "draft",
            "planning_basis": {
                "duration_source": "task_duration",
                "basis_label": "Task durations",
            },
            "planned_start_at": "2026-06-08T08:00:00+00:00",
            "planning_calendar": {
                "working_days": [
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                ],
                "workday_hours": 8,
                "workmonth_mode": "calendar_month",
            },
            "generated_task_plan_count": 2,
            "generated_schedule_start_at": "2026-06-08T08:00:00Z",
            "generated_schedule_finish_at": "2026-06-10T16:00:00Z",
        }
    ]
    assert "No generated schedule is visible for this work package." not in payload[
        "readiness_gaps"
    ]


def test_status_keeps_document_lifecycle_explicitly_not_implemented(
    restore_state_file,
):
    write_state(configured_state())

    result = run_local_workflow("status", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["document_lifecycle"] == {
        "status": "not_implemented_in_current_surface",
        "limitation": "Document review/download behavior belongs to M32.6 unless separately scoped.",
    }
    assert "Document review/download behavior belongs to M32.6 unless separately scoped." in payload[
        "limitations"
    ]


def test_status_keeps_limitations_visible_with_incomplete_state(restore_state_file):
    write_state(incomplete_state())

    result = run_local_workflow("status", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["readiness_gaps"] == [
        "No preset/profile/source selector context is bound.",
        "No staged tasks are associated with this work package.",
        "No source/task collection is bound to this work package.",
        "No schedule plan is associated with this work package.",
    ]
    assert payload["limitations"][0] == "CLI/local workflow surface is an adapter only."
    assert payload["ai_limitation_state"]["human_review_required"] is True


def test_status_reports_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_local_workflow("status", "--wp-id", "WP-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_status_reports_missing_work_package(restore_state_file):
    write_state(incomplete_state())

    result = run_local_workflow("status", "--wp-id", "WP-999")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout
