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


def test_local_workflow_plan_outputs_read_only_adapter_payload(restore_state_file):
    write_state(
        {
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
                    "work_package_id": "WP-001",
                    "dependencies": [],
                }
            ],
            "task_collections": [
                {
                    "collection_id": "TC-001",
                    "title": "Selected source pack",
                    "collection_state": "staged",
                    "work_package_id": "WP-001",
                    "task_ids": ["TASK-001"],
                }
            ],
            "plans": [],
        }
    )

    result = run_local_workflow("plan", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["checkpoint"] == "M32.3 — UI-to-core adapter implementation"
    assert payload["surface"] == "cli-enhanced controlled local workflow"
    assert payload["selected_work_package"]["wp_id"] == "WP-001"
    assert payload["selected_work_package"]["selector_context"] == {
        "system_type": "cleanroom-hvac",
        "preset_id": "cqv-cleanroom-hvac-basic",
        "scope_intent": "qualification-only",
        "standards_bundles": ["cqv-core", "cleanroom-hvac"],
    }
    assert payload["task_staging"] == {
        "task_count": 1,
        "task_ids": ["TASK-001"],
    }
    assert payload["source_selection"]["collection_ids"] == ["TC-001"]
    assert payload["readiness_gaps"] == []
    assert "No AI, provider, Ollama, or live model call is performed." in payload["limitations"]

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"][0]["wp_id"] == "WP-001"


def test_local_workflow_plan_reports_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_local_workflow("plan", "--wp-id", "WP-001")

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_local_workflow_plan_reports_missing_work_package(restore_state_file):
    write_state(
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.1.0",
            "status": "in_flight",
            "tasks": [],
            "work_packages": [],
            "task_collections": [],
            "plans": [],
        }
    )

    result = run_local_workflow("plan", "--wp-id", "WP-999")

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout


def test_local_workflow_plan_keeps_limitations_visible_with_incomplete_state(
    restore_state_file,
):
    write_state(
        {
            "project": "AI_SYSTEM_BUILDER",
            "version": "0.1.0",
            "status": "in_flight",
            "work_packages": [
                {
                    "wp_id": "WP-001",
                    "title": "Incomplete workflow",
                    "status": "open",
                }
            ],
            "tasks": [],
            "task_collections": [],
            "plans": [],
        }
    )

    result = run_local_workflow("plan", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["readiness_gaps"] == [
        "No preset/profile/source selector context is bound.",
        "No staged tasks are associated with this work package.",
        "No source/task collection is bound to this work package.",
    ]
    assert payload["limitations"][0] == "CLI/local workflow surface is an adapter only."
