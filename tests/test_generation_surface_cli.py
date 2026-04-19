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
    state_exists = STATE_FILE.exists()
    state_text = STATE_FILE.read_text(encoding="utf-8") if state_exists else None

    yield

    if state_exists and state_text is not None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(state_text, encoding="utf-8")
    elif STATE_FILE.exists():
        STATE_FILE.unlink()


def test_runtime_generate_request_wp_cli_returns_generation_payload(
    restore_state_file,
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

    result = run_cli(
        "runtime",
        "generate-request-wp",
        "WP-001",
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["wp_id"] == "WP-001"
    assert payload["generation_surface_metadata"]["generation_state"] == "blocked"
    assert payload["candidate_response_template"]["response_mode"] == (
        "blocked_explainer"
    )


def test_runtime_generate_request_wp_cli_reports_missing_work_package(
    restore_state_file,
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

    result = run_cli(
        "runtime",
        "generate-request-wp",
        "WP-404",
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "Work Package not found: WP-404"
