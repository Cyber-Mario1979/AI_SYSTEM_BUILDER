import json
import subprocess
import sys
from pathlib import Path

import pytest

from asbp.local_workflow_failure_logic import (
    build_provider_failure_payload,
    build_source_limitation_failure_payload,
    build_validation_error_failure_payload,
)


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


def write_state_text(text: str) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(text, encoding="utf-8")


def base_state() -> dict:
    return {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.1.0",
        "status": "in_flight",
        "work_packages": [
            {
                "wp_id": "WP-001",
                "title": "Cleanroom HVAC CQV workflow",
                "status": "open",
            }
        ],
        "tasks": [],
        "task_collections": [],
        "plans": [],
    }


def test_missing_command_returns_structured_failure_payload():
    result = run_local_workflow()

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["checkpoint"] == "M32.7 — Local workflow error/failure handling"
    assert payload["status"] == "failed"
    assert payload["success"] is False
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_MISSING_INPUT"
    assert payload["failure_state"]["blocking"] is True
    assert payload["failure_state"]["safe_to_continue"] is False


def test_missing_required_argument_returns_structured_failure_payload(restore_state_file):
    write_state_text(json.dumps(base_state(), indent=2))

    result = run_local_workflow("plan")

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_MISSING_INPUT"
    assert "required" in payload["failure_state"]["message"]
    assert "No workflow payload is treated as successful when a blocking failure is present." in payload[
        "limitations"
    ]


def test_invalid_json_returns_structured_state_failure(restore_state_file):
    write_state_text("{not-valid-json")

    result = run_local_workflow("status", "--wp-id", "WP-001")

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_STATE_INVALID"
    assert payload["failure_state"]["message"].startswith("Invalid JSON in state file")
    assert payload["failure_state"]["blocking"] is True
    assert payload["success"] is False


def test_invalid_state_schema_returns_structured_state_failure(restore_state_file):
    write_state_text(json.dumps({"project": "AI_SYSTEM_BUILDER"}, indent=2))

    result = run_local_workflow("status", "--wp-id", "WP-001")

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_STATE_INVALID"
    assert payload["failure_state"]["message"] == "State validation failed."
    assert payload["failure_state"]["blocking"] is True


def test_invalid_work_package_reference_returns_structured_failure(restore_state_file):
    write_state_text(json.dumps(base_state(), indent=2))

    result = run_local_workflow("status", "--wp-id", "WP-999")

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_INVALID_REFERENCE"
    assert payload["failure_state"]["message"] == "Work Package not found: WP-999"
    assert payload["failure_state"]["safe_to_continue"] is False


def test_source_limitation_payload_is_visible_and_not_successful():
    payload = build_source_limitation_failure_payload(
        command="status",
        message="Source collection is unavailable.",
        detail="No source collection is bound to the selected work package.",
    )

    assert payload["status"] == "failed"
    assert payload["success"] is False
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_SOURCE_LIMITATION"
    assert payload["failure_state"]["blocking"] is True
    assert payload["failure_state"]["safe_to_continue"] is False
    assert any("Source, citation, retrieval" in item for item in payload["limitations"])


def test_validation_error_payload_does_not_claim_acceptance_or_release():
    payload = build_validation_error_failure_payload(
        command="outputs",
        message="Output validation failed.",
        detail="Required checks did not pass.",
    )

    assert payload["status"] == "failed"
    assert payload["success"] is False
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_VALIDATION_ERROR"
    assert any("acceptance, approval, release, or certification" in item for item in payload["limitations"])


def test_provider_failure_payload_does_not_call_or_claim_ai_result():
    payload = build_provider_failure_payload(
        command="status",
        message="Provider unavailable.",
        detail="Provider behavior is outside this local workflow failure scope.",
    )

    assert payload["status"] == "failed"
    assert payload["success"] is False
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_PROVIDER_FAILURE"
    assert payload["failure_state"]["context"] == {
        "ai_call_performed": False,
        "provider_call_performed": False,
        "ollama_call_performed": False,
        "ai_result_claimed": False,
    }
    assert any("no fallback model output" in item for item in payload["limitations"])
