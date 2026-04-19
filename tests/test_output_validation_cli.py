import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = REPO_ROOT / "data" / "state" / "state.json"
CANDIDATE_FILE = REPO_ROOT / "data" / "state" / "candidate_response.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "asbp", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def restore_files():
    state_exists = STATE_FILE.exists()
    state_text = STATE_FILE.read_text(encoding="utf-8") if state_exists else None
    candidate_exists = CANDIDATE_FILE.exists()
    candidate_text = (
        CANDIDATE_FILE.read_text(encoding="utf-8")
        if candidate_exists
        else None
    )

    yield

    if state_exists and state_text is not None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(state_text, encoding="utf-8")
    elif STATE_FILE.exists():
        STATE_FILE.unlink()

    if candidate_exists and candidate_text is not None:
        CANDIDATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CANDIDATE_FILE.write_text(candidate_text, encoding="utf-8")
    elif CANDIDATE_FILE.exists():
        CANDIDATE_FILE.unlink()


def test_runtime_validate_response_wp_cli_returns_validation_payload(
    restore_files,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
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
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    CANDIDATE_FILE.write_text(
        json.dumps(
            {
                "response_mode": "blocked_explainer",
                "operator_message": "Selector context is still required.",
                "recommended_next_actions": [
                    "Complete deterministic selector context before orchestration can proceed."
                ],
                "grounded_input_fields_used": [
                    "wp_id",
                    "deterministic_facts.orchestration_stage",
                    "deterministic_facts.next_actions",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "runtime",
        "validate-response-wp",
        "WP-001",
        str(CANDIDATE_FILE),
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["wp_id"] == "WP-001"
    assert payload["validation_state"] == "accepted"


def test_runtime_validate_response_wp_cli_reports_missing_work_package(
    restore_files,
):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "in_flight",
                "tasks": [],
                "work_packages": [],
                "task_collections": [],
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    CANDIDATE_FILE.write_text(
        json.dumps(
            {
                "response_mode": "blocked_explainer",
                "operator_message": "Selector context is still required.",
                "recommended_next_actions": [],
                "grounded_input_fields_used": [
                    "wp_id",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_cli(
        "runtime",
        "validate-response-wp",
        "WP-404",
        str(CANDIDATE_FILE),
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "Work Package not found: WP-404"
