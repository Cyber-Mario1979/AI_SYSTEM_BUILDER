import json
import subprocess
import sys
from pathlib import Path

import pytest

from asbp.m33_scenario_pack_validation import (
    EXPECTED_PLAN_ID,
    EXPECTED_SCENARIO_ID,
    EXPECTED_TASK_COLLECTION_ID,
    EXPECTED_WORK_PACKAGE_ID,
    load_scenario_profile,
    load_source_inventory,
    load_user_inputs,
    missing_scenario_pack_files,
    validate_expected_observations,
    validate_m33_integrated_scenario_pack,
    validate_scenario_identity,
    validate_source_and_ai_boundaries,
    validate_user_input_controls,
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


def test_m33_3_scenario_pack_required_files_exist():
    assert missing_scenario_pack_files(REPO_ROOT) == []


def test_m33_3_scenario_pack_json_files_are_valid_objects():
    assert isinstance(load_scenario_profile(REPO_ROOT), dict)
    assert isinstance(load_user_inputs(REPO_ROOT), dict)
    assert isinstance(load_source_inventory(REPO_ROOT), dict)


def test_m33_3_scenario_identity_matches_trial_scope():
    profile = load_scenario_profile(REPO_ROOT)

    assert validate_scenario_identity(profile) == []
    assert profile["scenario_id"] == EXPECTED_SCENARIO_ID
    assert profile["work_package"]["wp_id"] == EXPECTED_WORK_PACKAGE_ID
    assert profile["task_collection"]["collection_id"] == EXPECTED_TASK_COLLECTION_ID
    assert profile["plan"]["plan_id"] == EXPECTED_PLAN_ID
    assert profile["workflow_path"] == ["scenario", "configure", "plan", "status", "outputs"]


def test_m33_3_user_inputs_preserve_data_sensitivity_controls():
    user_inputs = load_user_inputs(REPO_ROOT)

    assert validate_user_input_controls(user_inputs) == []
    assert user_inputs["data_controls"] == {
        "real_customer_data_used": False,
        "real_facility_data_used": False,
        "personal_data_used": False,
        "production_gmp_records_used": False,
        "confidential_vendor_documents_used": False,
        "raw_model_output_used_as_product_evidence": False,
    }


def test_m33_3_source_inventory_preserves_authority_and_ai_boundaries():
    source_inventory = load_source_inventory(REPO_ROOT)

    assert validate_source_and_ai_boundaries(source_inventory) == []
    assert source_inventory["retrieval_boundary"] == {
        "retrieval_required_for_m33_2": False,
        "retrieval_upgraded_to_source_authority": False,
        "external_documents_ingested": False,
    }
    assert source_inventory["ai_boundary"] == {
        "ai_required_for_m33_2": False,
        "provider_call_required": False,
        "local_model_call_required": False,
        "raw_model_output_product_evidence": False,
        "human_review_required": True,
    }


def test_m33_3_expected_observations_cover_trial_categories():
    assert validate_expected_observations(REPO_ROOT) == []


def test_m33_3_integrated_scenario_pack_validation_passes():
    result = validate_m33_integrated_scenario_pack(REPO_ROOT)

    assert result["result"] == "PASS"
    assert result["issues"] == []
    assert result["scenario_id"] == EXPECTED_SCENARIO_ID
    assert result["wp_id"] == EXPECTED_WORK_PACKAGE_ID
    assert result["collection_id"] == EXPECTED_TASK_COLLECTION_ID
    assert result["plan_id"] == EXPECTED_PLAN_ID
    assert result["trial_execution_started"] is False
    assert result["ai_or_provider_call_required"] is False
    assert result["human_review_required"] is True


def test_m33_3_cli_path_exercises_cleanroom_hvac_scenario(restore_state_file):
    scenario_result = run_local_workflow("scenario", "--scenario-id", EXPECTED_SCENARIO_ID)
    assert scenario_result.returncode == 0
    scenario_payload = json.loads(scenario_result.stdout)
    assert scenario_payload["scenario_id"] == EXPECTED_SCENARIO_ID
    assert scenario_payload["selected_work_package"]["wp_id"] == EXPECTED_WORK_PACKAGE_ID

    configure_result = run_local_workflow(
        "configure",
        "--wp-id",
        EXPECTED_WORK_PACKAGE_ID,
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

    plan_result = run_local_workflow("plan", "--wp-id", EXPECTED_WORK_PACKAGE_ID)
    assert plan_result.returncode == 0
    plan_payload = json.loads(plan_result.stdout)
    assert plan_payload["source_selection"]["authority_limit"] == (
        "Existing repo state only; no retrieval or standards authority is upgraded."
    )

    status_result = run_local_workflow("status", "--wp-id", EXPECTED_WORK_PACKAGE_ID)
    assert status_result.returncode == 0
    status_payload = json.loads(status_result.stdout)
    assert status_payload["ai_limitation_state"] == {
        "ai_call_performed": False,
        "provider_call_performed": False,
        "ollama_call_performed": False,
        "human_review_required": True,
        "limitation": "No AI, provider, Ollama, or live model call is performed.",
    }

    outputs_result = run_local_workflow("outputs", "--wp-id", EXPECTED_WORK_PACKAGE_ID)
    assert outputs_result.returncode == 0
    outputs_payload = json.loads(outputs_result.stdout)
    assert outputs_payload["review_acceptance_status"]["human_review_required"] is True
    assert outputs_payload["review_acceptance_status"]["accepted"] is False
    assert outputs_payload["safe_artifact_access"]["download_allowed"] is False
