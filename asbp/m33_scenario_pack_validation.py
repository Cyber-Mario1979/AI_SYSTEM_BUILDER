"""M33.3 integrated scenario-pack validation helpers.

These helpers validate the M33.2 cleanroom HVAC scenario-pack contract without
running trial execution, calling AI/provider services, or upgrading source /
standards authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCENARIO_PACK_RELATIVE_PATH = Path("data/scenarios/m33/cleanroom_hvac_trial_pack")

REQUIRED_SCENARIO_PACK_FILES = {
    "readme": "README.md",
    "scenario_profile": "scenario_profile.json",
    "user_inputs": "user_inputs.json",
    "source_inventory": "source_inventory.json",
    "expected_observations": "expected_observations.md",
}

EXPECTED_SCENARIO_ID = "cleanroom-hvac-qualification-basic"
EXPECTED_WORK_PACKAGE_ID = "WP-032"
EXPECTED_TASK_COLLECTION_ID = "TC-032"
EXPECTED_PLAN_ID = "PLAN-032"
EXPECTED_SYSTEM_TYPE = "cleanroom-hvac"
EXPECTED_SCOPE_INTENT = "qualification-only"
EXPECTED_PRESET_ID = "cqv-cleanroom-hvac-basic"
EXPECTED_WORKFLOW_PATH = ["scenario", "configure", "plan", "status", "outputs"]
EXPECTED_STANDARDS_BUNDLES = {"cqv-core", "cleanroom-hvac"}
SYNTHETIC_DATA_CLASSIFICATION = "synthetic_non_confidential_local_trial_data"


def repo_root_from_file() -> Path:
    """Return the repository root for normal in-repo execution."""

    return Path(__file__).resolve().parents[1]


def scenario_pack_root(repo_root: Path | None = None) -> Path:
    """Return the M33 cleanroom HVAC scenario-pack directory."""

    root = repo_root if repo_root is not None else repo_root_from_file()
    return root / SCENARIO_PACK_RELATIVE_PATH


def required_scenario_pack_paths(repo_root: Path | None = None) -> dict[str, Path]:
    """Return required scenario-pack file paths keyed by logical name."""

    pack_root = scenario_pack_root(repo_root)
    return {
        logical_name: pack_root / file_name
        for logical_name, file_name in REQUIRED_SCENARIO_PACK_FILES.items()
    }


def missing_scenario_pack_files(repo_root: Path | None = None) -> list[str]:
    """Return relative paths for any required scenario-pack files that are absent."""

    root = repo_root if repo_root is not None else repo_root_from_file()
    missing: list[str] = []
    for path in required_scenario_pack_paths(root).values():
        if not path.exists():
            missing.append(path.relative_to(root).as_posix())
    return missing


def load_json_file(path: Path) -> dict[str, Any]:
    """Load a JSON object from a scenario-pack file."""

    with path.open(encoding="utf-8") as file_handle:
        payload = json.load(file_handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def load_scenario_profile(repo_root: Path | None = None) -> dict[str, Any]:
    return load_json_file(required_scenario_pack_paths(repo_root)["scenario_profile"])


def load_user_inputs(repo_root: Path | None = None) -> dict[str, Any]:
    return load_json_file(required_scenario_pack_paths(repo_root)["user_inputs"])


def load_source_inventory(repo_root: Path | None = None) -> dict[str, Any]:
    return load_json_file(required_scenario_pack_paths(repo_root)["source_inventory"])


def _add_issue_if_false(issues: list[str], condition: bool, message: str) -> None:
    if not condition:
        issues.append(message)


def validate_scenario_identity(profile: dict[str, Any]) -> list[str]:
    """Validate scenario identity and workflow alignment."""

    issues: list[str] = []
    work_package = profile.get("work_package", {})
    task_collection = profile.get("task_collection", {})
    plan = profile.get("plan", {})

    _add_issue_if_false(
        issues,
        profile.get("scenario_id") == EXPECTED_SCENARIO_ID,
        "scenario_id does not match the approved cleanroom HVAC trial scenario.",
    )
    _add_issue_if_false(
        issues,
        profile.get("data_classification") == SYNTHETIC_DATA_CLASSIFICATION,
        "scenario_profile data classification is not synthetic/non-confidential.",
    )
    _add_issue_if_false(
        issues,
        profile.get("system_type") == EXPECTED_SYSTEM_TYPE,
        "system_type does not match cleanroom-hvac.",
    )
    _add_issue_if_false(
        issues,
        profile.get("scope_intent") == EXPECTED_SCOPE_INTENT,
        "scope_intent does not match qualification-only.",
    )
    _add_issue_if_false(
        issues,
        profile.get("preset_id") == EXPECTED_PRESET_ID,
        "preset_id does not match cqv-cleanroom-hvac-basic.",
    )
    _add_issue_if_false(
        issues,
        work_package.get("wp_id") == EXPECTED_WORK_PACKAGE_ID,
        "work package ID does not match WP-032.",
    )
    _add_issue_if_false(
        issues,
        task_collection.get("collection_id") == EXPECTED_TASK_COLLECTION_ID,
        "task collection ID does not match TC-032.",
    )
    _add_issue_if_false(
        issues,
        plan.get("plan_id") == EXPECTED_PLAN_ID,
        "plan ID does not match PLAN-032.",
    )
    _add_issue_if_false(
        issues,
        profile.get("workflow_path") == EXPECTED_WORKFLOW_PATH,
        "workflow path does not match scenario -> configure -> plan -> status -> outputs.",
    )
    return issues


def validate_user_input_controls(user_inputs: dict[str, Any]) -> list[str]:
    """Validate synthetic input and confidentiality controls."""

    issues: list[str] = []
    workflow_inputs = user_inputs.get("workflow_inputs", {})
    data_controls = user_inputs.get("data_controls", {})

    _add_issue_if_false(
        issues,
        user_inputs.get("data_classification") == SYNTHETIC_DATA_CLASSIFICATION,
        "user_inputs data classification is not synthetic/non-confidential.",
    )
    _add_issue_if_false(
        issues,
        workflow_inputs.get("scenario_id") == EXPECTED_SCENARIO_ID,
        "workflow input scenario_id does not match approved scenario.",
    )
    _add_issue_if_false(
        issues,
        workflow_inputs.get("wp_id") == EXPECTED_WORK_PACKAGE_ID,
        "workflow input wp_id does not match WP-032.",
    )
    _add_issue_if_false(
        issues,
        workflow_inputs.get("system_type") == EXPECTED_SYSTEM_TYPE,
        "workflow input system_type does not match cleanroom-hvac.",
    )
    _add_issue_if_false(
        issues,
        set(workflow_inputs.get("standards_bundles", [])) == EXPECTED_STANDARDS_BUNDLES,
        "workflow input standards bundles do not match expected visibility bundles.",
    )

    for control_name, control_value in data_controls.items():
        _add_issue_if_false(
            issues,
            control_value is False,
            f"data control {control_name} must remain false for M33.2/M33.3.",
        )

    _add_issue_if_false(
        issues,
        bool(user_inputs.get("synthetic_task_inputs")),
        "synthetic task inputs are missing.",
    )
    return issues


def validate_source_and_ai_boundaries(source_inventory: dict[str, Any]) -> list[str]:
    """Validate source, retrieval, standards, and AI/local-model boundaries."""

    issues: list[str] = []
    retrieval_boundary = source_inventory.get("retrieval_boundary", {})
    ai_boundary = source_inventory.get("ai_boundary", {})
    standards_visibility = source_inventory.get("standards_visibility", [])

    _add_issue_if_false(
        issues,
        source_inventory.get("data_classification") == SYNTHETIC_DATA_CLASSIFICATION,
        "source inventory data classification is not synthetic/non-confidential.",
    )
    _add_issue_if_false(
        issues,
        all(
            "authority_limit" in bundle and "authority" in bundle["authority_limit"].lower()
            for bundle in standards_visibility
        ),
        "standards visibility entries must retain authority-limit language.",
    )
    _add_issue_if_false(
        issues,
        retrieval_boundary.get("retrieval_required_for_m33_2") is False,
        "retrieval must not be required for this scenario-pack validation.",
    )
    _add_issue_if_false(
        issues,
        retrieval_boundary.get("retrieval_upgraded_to_source_authority") is False,
        "retrieval must not be upgraded to source authority.",
    )
    _add_issue_if_false(
        issues,
        retrieval_boundary.get("external_documents_ingested") is False,
        "external documents must not be ingested for this scenario pack.",
    )
    _add_issue_if_false(
        issues,
        ai_boundary.get("ai_required_for_m33_2") is False,
        "AI must not be required for M33.2 scenario-pack validation.",
    )
    _add_issue_if_false(
        issues,
        ai_boundary.get("provider_call_required") is False,
        "provider calls must not be required.",
    )
    _add_issue_if_false(
        issues,
        ai_boundary.get("local_model_call_required") is False,
        "local model calls must not be required.",
    )
    _add_issue_if_false(
        issues,
        ai_boundary.get("raw_model_output_product_evidence") is False,
        "raw model output must not become product evidence.",
    )
    _add_issue_if_false(
        issues,
        ai_boundary.get("human_review_required") is True,
        "human review must remain required.",
    )
    return issues


def validate_expected_observations(repo_root: Path | None = None) -> list[str]:
    """Validate observation-category coverage for later M33 trial execution."""

    path = required_scenario_pack_paths(repo_root)["expected_observations"]
    text = path.read_text(encoding="utf-8")
    expected_terms = [
        "Bug",
        "Workflow friction",
        "Missing visibility",
        "Source/standards limitation",
        "Output limitation",
        "Validation gap",
        "AI limitation",
        "Documentation gap",
        "Out of scope",
    ]
    return [term for term in expected_terms if term not in text]


def validate_m33_integrated_scenario_pack(repo_root: Path | None = None) -> dict[str, Any]:
    """Run the M33.3 integrated scenario-pack validation checks.

    This is a deterministic repo-data validation. It does not execute trial UAT,
    call providers, call local models, or mutate repository state.
    """

    root = repo_root if repo_root is not None else repo_root_from_file()
    issues: list[str] = []

    missing_files = missing_scenario_pack_files(root)
    issues.extend(f"missing required scenario-pack file: {path}" for path in missing_files)
    if missing_files:
        return {
            "checkpoint": "M33.3 — Integrated validation suite",
            "scenario_pack_root": scenario_pack_root(root).relative_to(root).as_posix(),
            "result": "FAIL",
            "issues": issues,
        }

    profile = load_scenario_profile(root)
    user_inputs = load_user_inputs(root)
    source_inventory = load_source_inventory(root)

    issues.extend(validate_scenario_identity(profile))
    issues.extend(validate_user_input_controls(user_inputs))
    issues.extend(validate_source_and_ai_boundaries(source_inventory))
    missing_observation_terms = validate_expected_observations(root)
    issues.extend(
        f"expected observation category missing: {term}"
        for term in missing_observation_terms
    )

    return {
        "checkpoint": "M33.3 — Integrated validation suite",
        "scenario_pack_root": scenario_pack_root(root).relative_to(root).as_posix(),
        "scenario_id": profile.get("scenario_id"),
        "wp_id": profile.get("work_package", {}).get("wp_id"),
        "collection_id": profile.get("task_collection", {}).get("collection_id"),
        "plan_id": profile.get("plan", {}).get("plan_id"),
        "workflow_path": profile.get("workflow_path"),
        "result": "PASS" if not issues else "FAIL",
        "issues": issues,
        "trial_execution_started": False,
        "ai_or_provider_call_required": False,
        "human_review_required": True,
    }
