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


def base_state(title: str = "Cleanroom HVAC CQV workflow") -> dict:
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


def test_configure_applies_controlled_input_selection_and_persists_state(
    restore_state_file,
):
    write_state(base_state())

    result = run_local_workflow(
        "configure",
        "--wp-id",
        "WP-001",
        "--system-type",
        "cleanroom-hvac",
        "--preset-id",
        "cqv-cleanroom-hvac-basic",
        "--scope-intent",
        "qualification-only",
        "--standards-bundle",
        "cleanroom-hvac",
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["checkpoint"] == "M32.4 — Controlled input surfaces"
    assert payload["updated_work_package"]["selector_context"] == {
        "system_type": "cleanroom-hvac",
        "preset_id": "cqv-cleanroom-hvac-basic",
        "scope_intent": "qualification-only",
        "standards_bundles": ["cqv-core", "cleanroom-hvac"],
    }
    assert payload["input_warnings"] == []
    assert "No free-form user text is treated as source truth." in payload["limitations"]

    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved["work_packages"][0]["selector_context"] == {
        "system_type": "cleanroom-hvac",
        "preset_id": "cqv-cleanroom-hvac-basic",
        "scope_intent": "qualification-only",
        "standards_bundles": ["cqv-core", "cleanroom-hvac"],
    }


def test_configure_warns_when_controlled_input_may_not_match_title(
    restore_state_file,
):
    write_state(base_state(title="Tablet press qualification"))

    result = run_local_workflow(
        "configure",
        "--wp-id",
        "WP-001",
        "--system-type",
        "cleanroom-hvac",
        "--preset-id",
        "cqv-cleanroom-hvac-basic",
        "--scope-intent",
        "qualification-only",
        "--standards-bundle",
        "cleanroom-hvac",
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["input_warnings"] == [
        "Selected system_type cleanroom-hvac may not match work package title: "
        "Tablet press qualification"
    ]

    plan_result = run_local_workflow("plan", "--wp-id", "WP-001")

    assert plan_result.returncode == 0
    plan_payload = json.loads(plan_result.stdout)
    assert plan_payload["input_warnings"] == payload["input_warnings"]


def test_configure_allows_baseline_only_standards_bundle(restore_state_file):
    write_state(base_state(title="Automation system CQV workflow"))

    result = run_local_workflow(
        "configure",
        "--wp-id",
        "WP-001",
        "--system-type",
        "automation",
        "--preset-id",
        "cqv-automation-basic",
        "--scope-intent",
        "end-to-end",
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["updated_work_package"]["selector_context"] == {
        "system_type": "automation",
        "preset_id": "cqv-automation-basic",
        "scope_intent": "end-to-end",
        "standards_bundles": ["cqv-core"],
    }
    assert payload["input_warnings"] == []


def test_configure_reports_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_local_workflow(
        "configure",
        "--wp-id",
        "WP-001",
        "--system-type",
        "cleanroom-hvac",
        "--preset-id",
        "cqv-cleanroom-hvac-basic",
        "--scope-intent",
        "qualification-only",
    )

    assert result.returncode == 0
    assert "State file not found:" in result.stdout
    assert "No state file found. Run 'state init' first." in result.stdout


def test_configure_reports_missing_work_package_without_mutating_state(
    restore_state_file,
):
    state_payload = base_state()
    write_state(state_payload)

    result = run_local_workflow(
        "configure",
        "--wp-id",
        "WP-999",
        "--system-type",
        "cleanroom-hvac",
        "--preset-id",
        "cqv-cleanroom-hvac-basic",
        "--scope-intent",
        "qualification-only",
    )

    assert result.returncode == 0
    assert "Work Package not found: WP-999" in result.stdout
    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved == state_payload


def test_configure_rejects_uncontrolled_system_type_before_state_mutation(
    restore_state_file,
):
    state_payload = base_state()
    write_state(state_payload)

    result = run_local_workflow(
        "configure",
        "--wp-id",
        "WP-001",
        "--system-type",
        "uncontrolled-system",
        "--preset-id",
        "cqv-cleanroom-hvac-basic",
        "--scope-intent",
        "qualification-only",
    )

    assert result.returncode != 0
    assert "invalid choice: 'uncontrolled-system'" in result.stderr
    saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert saved == state_payload
