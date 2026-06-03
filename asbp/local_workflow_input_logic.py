"""Controlled local workflow input logic for M32.4.

This module keeps M32.4 input behavior behind a small application boundary.
The CLI adapter may collect controlled arguments, but selector/profile/source
binding is applied here through existing work-package core functions.
"""

from __future__ import annotations

from typing import Any

from asbp.core.work_packages import (
    set_work_package_preset,
    set_work_package_scope_intent,
    set_work_package_selector_type,
    set_work_package_standards_bundles,
)
from asbp.local_workflow_logic import build_local_workflow_plan_payload
from asbp.state_model import ScopeIntentId, StandardsBundleId, StateModel

CONTROLLED_INPUT_LIMITATIONS = [
    "Controlled input surface updates only approved selector/profile/source fields.",
    "CLI/local workflow surface remains an adapter only.",
    "Inputs are constrained by explicit command options and parser choices.",
    "No free-form user text is treated as source truth.",
    "No AI, provider, Ollama, or live model call is performed.",
    "Generated or assembled output remains human-review-required.",
    "This is not release, deployment, SaaS, commercial, or customer-ready evidence.",
]


def configure_local_workflow_inputs(
    state: StateModel,
    *,
    wp_id: str,
    system_type: str,
    preset_id: str,
    scope_intent: ScopeIntentId,
    standards_bundle_ids: list[StandardsBundleId] | None = None,
) -> dict[str, Any]:
    """Apply controlled local workflow input selections to a work package.

    The function mutates the validated in-memory state model through existing
    core work-package setters. Persistence remains the caller's responsibility
    so adapters can keep save behavior explicit and testable.
    """

    work_package = set_work_package_selector_type(
        state.work_packages,
        wp_id=wp_id,
        system_type=system_type,
    )
    if work_package is None:
        raise ValueError(f"Work Package not found: {wp_id}")

    work_package = set_work_package_preset(
        state.work_packages,
        wp_id=wp_id,
        preset_id=preset_id,
    )
    if work_package is None:
        raise ValueError(f"Work Package not found: {wp_id}")

    work_package = set_work_package_scope_intent(
        state.work_packages,
        wp_id=wp_id,
        scope_intent=scope_intent,
    )
    if work_package is None:
        raise ValueError(f"Work Package not found: {wp_id}")

    work_package = set_work_package_standards_bundles(
        state.work_packages,
        wp_id=wp_id,
        add_on_bundle_ids=standards_bundle_ids or [],
    )
    if work_package is None:
        raise ValueError(f"Work Package not found: {wp_id}")

    planning_payload = build_local_workflow_plan_payload(state, wp_id=wp_id)

    return {
        "checkpoint": "M32.4 — Controlled input surfaces",
        "surface": "cli-enhanced controlled local workflow",
        "adapter_boundary": "CLI adapter collects controlled arguments and saves validated state through approved helpers.",
        "updated_work_package": planning_payload["selected_work_package"],
        "task_staging": planning_payload["task_staging"],
        "source_selection": planning_payload["source_selection"],
        "input_warnings": planning_payload["input_warnings"],
        "readiness_gaps": planning_payload["readiness_gaps"],
        "limitations": list(CONTROLLED_INPUT_LIMITATIONS),
        "next_safe_actions": [
            "Run the local workflow plan command to review the configured payload.",
            "Continue to later M32 checkpoints for workflow visibility, output review, and failure handling.",
        ],
    }
