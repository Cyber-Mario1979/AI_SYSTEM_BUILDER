import json
import subprocess
import sys
from pathlib import Path

import pytest

from asbp.local_workflow_output_logic import build_local_workflow_output_payload
from asbp.renderer_output_model import RendererArtifactMetadataModel
from asbp.state_model import StateModel


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
                "selector_context": {
                    "system_type": "cleanroom-hvac",
                    "preset_id": "cqv-cleanroom-hvac-basic",
                    "scope_intent": "qualification-only",
                    "standards_bundles": ["cqv-core", "cleanroom-hvac"],
                },
            }
        ],
        "tasks": [],
        "task_collections": [],
        "plans": [],
    }


def artifact_metadata() -> RendererArtifactMetadataModel:
    return RendererArtifactMetadataModel(
        artifact_id="ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        output_format="markdown",
        artifact_filename="art_qualification_plan_markdown_v1.md",
        media_type="text/markdown",
        source_draft_id="DRAFT-QUALIFICATION-PLAN-CONTROLS@v1",
        template_id="TPL-FUTURE-QUALIFICATION-PLAN@v1",
        schema_id="SCHEMA-QUALIFICATION-PLAN@v1",
        standards_control_packet_id="STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        placeholder_present=True,
        limitation_present=True,
        standards_warning_present=True,
        non_product_ready=True,
        lifecycle_state_mutated=False,
        approval_claimed=False,
    )


def test_outputs_command_returns_controlled_not_available_state(restore_state_file):
    write_state(base_state())

    result = run_local_workflow("outputs", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["checkpoint"] == "M32.6 — Output review/download surfaces"
    assert payload["selected_work_package"]["wp_id"] == "WP-001"
    assert payload["document_export_view"]["document_output_status"] == "not_available"
    assert payload["document_export_view"]["export_output_status"] == "not_available"
    assert payload["artifact_metadata"]["artifact_available"] is False
    assert payload["safe_artifact_access"] == {
        "access_available": False,
        "access_mode": "not_available",
        "artifact_reference": None,
        "download_allowed": False,
        "download_performed": False,
        "path_exposed": False,
    }


def test_output_payload_exposes_artifact_metadata_without_download_claim():
    state = StateModel(**base_state())

    payload = build_local_workflow_output_payload(
        state,
        wp_id="WP-001",
        artifact_metadata=artifact_metadata(),
    )

    assert payload["artifact_metadata"] == {
        "artifact_available": True,
        "artifact_id": "ART-QUALIFICATION-PLAN-MARKDOWN@v1",
        "artifact_filename": "art_qualification_plan_markdown_v1.md",
        "output_format": "markdown",
        "media_type": "text/markdown",
        "source_draft_id": "DRAFT-QUALIFICATION-PLAN-CONTROLS@v1",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "schema_id": "SCHEMA-QUALIFICATION-PLAN@v1",
        "standards_control_packet_id": "STDOUT-QUALIFICATION-PLAN-CONTROLS@v1",
        "placeholder_present": True,
        "limitation_present": True,
        "standards_warning_present": True,
        "non_product_ready": True,
    }
    assert payload["document_export_view"]["document_output_status"] == "available"
    assert payload["safe_artifact_access"] == {
        "access_available": True,
        "access_mode": "metadata_reference_only",
        "artifact_reference": "art_qualification_plan_markdown_v1.md",
        "download_allowed": False,
        "download_performed": False,
        "path_exposed": False,
    }


def test_outputs_keeps_validation_limitations_visible(restore_state_file):
    write_state(base_state())

    result = run_local_workflow("outputs", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["output_validation_state"] == {
        "validation_available": False,
        "validation_id": None,
        "status": "not_available",
        "checks_performed": [],
        "issues": [],
    }
    assert payload["validation_limitations"] == [
        "No output artifact metadata is available for this work package.",
        "No output validation result is available for this work package.",
        "Output review surface does not approve, sign, release, or certify artifacts.",
        "Download/access remains metadata-reference-only unless a separately scoped safe artifact access path exists.",
    ]


def test_outputs_marks_human_review_required_and_no_acceptance(restore_state_file):
    write_state(base_state())

    result = run_local_workflow("outputs", "--wp-id", "WP-001")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["review_acceptance_status"] == {
        "lifecycle_record_available": False,
        "lifecycle_record_id": None,
        "lifecycle_state": "not_available",
        "human_review_required": True,
        "accepted": False,
        "approval_claimed": False,
        "release_claimed": False,
    }


def test_outputs_does_not_create_or_claim_generated_output(restore_state_file):
    write_state(base_state())
    original_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    result = run_local_workflow("outputs", "--wp-id", "WP-001")

    assert result.returncode == 0
    saved_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    payload = json.loads(result.stdout)
    assert saved_state == original_state
    assert "No document, export, report, or rendered artifact is generated by this surface." in payload[
        "limitations"
    ]
    assert "No output is silently accepted, approved, signed, released, or certified." in payload[
        "limitations"
    ]


def test_outputs_reports_missing_state_file(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_local_workflow("outputs", "--wp-id", "WP-001")

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "failed"
    assert payload["success"] is False
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_STATE_MISSING"
    assert payload["failure_state"]["blocking"] is True
    assert payload["failure_state"]["safe_to_continue"] is False


def test_outputs_reports_missing_work_package(restore_state_file):
    payload = base_state()
    payload["work_packages"] = []
    write_state(payload)

    result = run_local_workflow("outputs", "--wp-id", "WP-999")

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "failed"
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_INVALID_REFERENCE"
    assert payload["failure_state"]["message"] == "Work Package not found: WP-999"
