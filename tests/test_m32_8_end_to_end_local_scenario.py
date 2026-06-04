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


def test_scenario_command_stages_cleanroom_hvac_workflow_from_missing_state(
    restore_state_file,
):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_local_workflow("scenario", "--scenario-id", SCENARIO_ID)

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["checkpoint"] == "M32.8 — End-to-end local scenario implementation"
    assert payload["scenario_id"] == SCENARIO_ID
    assert payload["selected_work_package"]["wp_id"] == SCENARIO_WP_ID
    assert payload["scenario_assets"] == {
        "task_ids": ["TASK-M32-8-001", "TASK-M32-8-002", "TASK-M32-8-003"],
        "task_count": 3,
        "collection_id": "TC-032",
        "collection_state": "committed",
        "plan_id": "PLAN-032",
        "generated_task_plan_count": 3,
    }
    assert payload["scenario_evidence"] == {
        "can_be_exercised_through_local_workflow": True,
        "commands_to_exercise": ["configure", "plan", "status", "outputs"],
        "human_review_required": True,
        "approval_claimed": False,
        "release_claimed": False,
        "product_ready_claimed": False,
    }
    assert len(payload["executable_local_use_steps"]) == 4
    assert "No AI, provider, Ollama, or live model call is performed." in payload[
        "limitations"
    ]

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert state["status"] == "in_flight"
    assert state["work_packages"][0]["wp_id"] == SCENARIO_WP_ID
    assert state["task_collections"][0]["collection_id"] == "TC-032"
    assert state["plans"][0]["plan_id"] == "PLAN-032"
    assert len(state["plans"][0]["generated_task_plans"]) == 3


def test_scenario_command_is_idempotent_for_owned_scenario_rows(restore_state_file):
    first_result = run_local_workflow("scenario", "--scenario-id", SCENARIO_ID)
    second_result = run_local_workflow("scenario", "--scenario-id", SCENARIO_ID)

    assert first_result.returncode == 0
    assert second_result.returncode == 0
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    assert [wp["wp_id"] for wp in state["work_packages"]].count(SCENARIO_WP_ID) == 1
    assert [task["task_id"] for task in state["tasks"]].count("TASK-M32-8-001") == 1
    assert [collection["collection_id"] for collection in state["task_collections"]].count("TC-032") == 1
    assert [plan["plan_id"] for plan in state["plans"]].count("PLAN-032") == 1


def test_staged_scenario_can_be_exercised_through_local_workflow_commands(
    restore_state_file,
):
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
    configure_payload = json.loads(configure_result.stdout)
    assert configure_payload["updated_work_package"]["wp_id"] == SCENARIO_WP_ID
    assert configure_payload["updated_work_package"]["selector_context"] == {
        "system_type": "cleanroom-hvac",
        "preset_id": "cqv-cleanroom-hvac-basic",
        "scope_intent": "qualification-only",
        "standards_bundles": ["cqv-core", "cleanroom-hvac"],
    }

    plan_result = run_local_workflow("plan", "--wp-id", SCENARIO_WP_ID)
    assert plan_result.returncode == 0
    plan_payload = json.loads(plan_result.stdout)
    assert plan_payload["selected_work_package"]["wp_id"] == SCENARIO_WP_ID
    assert plan_payload["task_staging"] == {
        "task_count": 3,
        "task_ids": ["TASK-M32-8-001", "TASK-M32-8-002", "TASK-M32-8-003"],
    }
    assert plan_payload["source_selection"] == {
        "collection_count": 1,
        "collection_ids": ["TC-032"],
        "authority_limit": "Existing repo state only; no retrieval or standards authority is upgraded.",
    }
    assert plan_payload["readiness_gaps"] == []

    status_result = run_local_workflow("status", "--wp-id", SCENARIO_WP_ID)
    assert status_result.returncode == 0
    status_payload = json.loads(status_result.stdout)
    assert status_payload["workflow_state"]["selected_work_package"]["wp_id"] == SCENARIO_WP_ID
    assert status_payload["task_lifecycle"]["task_count"] == 3
    assert status_payload["schedule_lifecycle"]["generated_schedule_present"] is True
    assert status_payload["source_and_citation_state"]["collection_ids"] == ["TC-032"]
    assert status_payload["ai_limitation_state"] == {
        "ai_call_performed": False,
        "provider_call_performed": False,
        "ollama_call_performed": False,
        "human_review_required": True,
        "limitation": "No AI, provider, Ollama, or live model call is performed.",
    }

    outputs_result = run_local_workflow("outputs", "--wp-id", SCENARIO_WP_ID)
    assert outputs_result.returncode == 0
    outputs_payload = json.loads(outputs_result.stdout)
    assert outputs_payload["selected_work_package"]["wp_id"] == SCENARIO_WP_ID
    assert outputs_payload["artifact_metadata"]["artifact_available"] is False
    assert outputs_payload["review_acceptance_status"]["human_review_required"] is True
    assert outputs_payload["review_acceptance_status"]["accepted"] is False
    assert outputs_payload["safe_artifact_access"]["download_allowed"] is False


def test_scenario_rejects_unapproved_scenario_id_without_mutation(restore_state_file):
    if STATE_FILE.exists():
        STATE_FILE.unlink()

    result = run_local_workflow("scenario", "--scenario-id", "unapproved-scenario")

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["failure_state"]["error_code"] == "LOCAL_WORKFLOW_MISSING_INPUT"
    assert "invalid choice: 'unapproved-scenario'" in payload["failure_state"]["message"]
    assert not STATE_FILE.exists()


def test_scenario_preserves_unrelated_state_rows(restore_state_file):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": "AI_SYSTEM_BUILDER",
                "version": "0.1.0",
                "status": "in_flight",
                "work_packages": [
                    {
                        "wp_id": "WP-001",
                        "title": "Existing unrelated workflow",
                        "status": "open",
                    }
                ],
                "tasks": [],
                "task_collections": [],
                "plans": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_local_workflow("scenario", "--scenario-id", SCENARIO_ID)

    assert result.returncode == 0
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    wp_ids = [work_package["wp_id"] for work_package in state["work_packages"]]
    assert wp_ids == ["WP-001", SCENARIO_WP_ID]
