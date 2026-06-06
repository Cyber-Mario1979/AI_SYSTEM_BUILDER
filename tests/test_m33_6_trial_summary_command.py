import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / "data" / "state" / "state.json"
SCENARIO_ID = "cleanroom-hvac-qualification-basic"
SCENARIO_WP_ID = "WP-032"


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


def stage_and_configure_cleanroom_hvac() -> None:
    scenario_result = run_local_workflow("scenario", "--scenario-id", SCENARIO_ID)
    assert scenario_result.returncode == 0

    configure_result = run_local_workflow(
        "configure",
        "--wp-id",
        SCENARIO_WP_ID,
        "--system-type",
        "cleanroom-hvac",
        "--preset-id",
        "cqv-cleanroom-hvac-basic",
        "--scope-intent",
        "qualification-only",
        "--standards-bundle",
        "cleanroom-hvac",
    )
    assert configure_result.returncode == 0


def test_trial_summary_returns_compact_reviewer_payload(restore_state_file):
    stage_and_configure_cleanroom_hvac()

    result = run_local_workflow("trial-summary", "--wp-id", SCENARIO_WP_ID)

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["checkpoint"] == "M33.6 — Corrective implementation package"
    assert payload["correction_id"] == "M33.5-001"
    assert payload["selected_work_package"]["wp_id"] == SCENARIO_WP_ID
    assert payload["trial_summary"]["workflow_path"] == [
        "scenario",
        "configure",
        "plan",
        "status",
        "outputs",
    ]
    assert payload["trial_summary"]["summarized_commands"] == [
        "plan",
        "status",
        "outputs",
    ]
    assert payload["trial_summary"]["task_count"] == 3
    assert payload["trial_summary"]["source_collection_ids"] == ["TC-032"]
    assert payload["trial_summary"]["standards_bundles"] == [
        "cqv-core",
        "cleanroom-hvac",
    ]
    assert payload["trial_summary"]["generated_schedule_present"] is True
    assert payload["trial_summary"]["artifact_available"] is False
    assert payload["issues_observed"] == []


def test_trial_summary_preserves_review_and_ai_boundaries(restore_state_file):
    stage_and_configure_cleanroom_hvac()

    result = run_local_workflow("trial-summary", "--wp-id", SCENARIO_WP_ID)

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["boundary_checks"] == {
        "human_review_required": True,
        "accepted": False,
        "approval_claimed": False,
        "release_claimed": False,
        "download_allowed": False,
        "ai_call_performed": False,
        "provider_call_performed": False,
        "ollama_call_performed": False,
    }
    assert payload["output_review_boundary"] == {
        "human_review_required": True,
        "accepted": False,
        "approval_claimed": False,
        "release_claimed": False,
        "download_allowed": False,
    }
    assert payload["ai_boundary"] == {
        "ai_call_performed": False,
        "provider_call_performed": False,
        "ollama_call_performed": False,
        "human_review_required": True,
        "limitation": "No AI, provider, Ollama, or live model call is performed.",
    }


def test_trial_summary_is_read_only_after_state_exists(restore_state_file):
    stage_and_configure_cleanroom_hvac()
    before = STATE_FILE.read_text(encoding="utf-8")

    result = run_local_workflow("trial-summary", "--wp-id", SCENARIO_WP_ID)

    assert result.returncode == 0
    after = STATE_FILE.read_text(encoding="utf-8")
    assert after == before


def test_trial_summary_reports_missing_state_without_mutation(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_local_workflow("trial-summary", "--wp-id", SCENARIO_WP_ID)

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_MISSING_STATE"
    assert not STATE_FILE.exists()
