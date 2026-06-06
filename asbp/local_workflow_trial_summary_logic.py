"""Compact local workflow trial-summary payloads for M33.6.

The trial summary reduces repeated manual JSON capture friction without changing
scenario, configure, plan, status, or outputs command behavior.
"""

from __future__ import annotations

from typing import Any

from asbp.local_workflow_logic import build_local_workflow_plan_payload
from asbp.local_workflow_output_logic import build_local_workflow_output_payload
from asbp.local_workflow_visibility_logic import build_local_workflow_visibility_payload
from asbp.state_model import StateModel


def _bool_from_path(payload: dict[str, Any], *keys: str) -> bool | None:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current if isinstance(current, bool) else None


def build_local_workflow_trial_summary_payload(
    state: StateModel,
    *,
    wp_id: str,
) -> dict[str, Any]:
    """Build a compact reviewer-facing local trial summary.

    The payload is read-only and deterministic. It calls the existing validated
    local workflow payload builders and summarizes boundary evidence for the
    accepted trial path.
    """

    plan_payload = build_local_workflow_plan_payload(state, wp_id=wp_id)
    status_payload = build_local_workflow_visibility_payload(state, wp_id=wp_id)
    outputs_payload = build_local_workflow_output_payload(state, wp_id=wp_id)

    selected_work_package = plan_payload["selected_work_package"]
    selector_context = selected_work_package.get("selector_context", {})
    source_selection = plan_payload.get("source_selection", {})
    ai_limitation_state = status_payload.get("ai_limitation_state", {})
    review_acceptance_status = outputs_payload.get("review_acceptance_status", {})
    safe_artifact_access = outputs_payload.get("safe_artifact_access", {})
    artifact_metadata = outputs_payload.get("artifact_metadata", {})

    command_results = [
        {
            "command": "plan",
            "result": "summarized",
            "key_observation": "Planning payload available from existing validated state.",
        },
        {
            "command": "status",
            "result": "summarized",
            "key_observation": "Workflow visibility payload available from existing validated state.",
        },
        {
            "command": "outputs",
            "result": "summarized",
            "key_observation": "Output review payload available from existing validated state.",
        },
    ]

    boundary_checks = {
        "human_review_required": _bool_from_path(
            outputs_payload,
            "review_acceptance_status",
            "human_review_required",
        ),
        "accepted": _bool_from_path(
            outputs_payload,
            "review_acceptance_status",
            "accepted",
        ),
        "approval_claimed": _bool_from_path(
            outputs_payload,
            "review_acceptance_status",
            "approval_claimed",
        ),
        "release_claimed": _bool_from_path(
            outputs_payload,
            "review_acceptance_status",
            "release_claimed",
        ),
        "download_allowed": _bool_from_path(
            outputs_payload,
            "safe_artifact_access",
            "download_allowed",
        ),
        "ai_call_performed": _bool_from_path(
            status_payload,
            "ai_limitation_state",
            "ai_call_performed",
        ),
        "provider_call_performed": _bool_from_path(
            status_payload,
            "ai_limitation_state",
            "provider_call_performed",
        ),
        "ollama_call_performed": _bool_from_path(
            status_payload,
            "ai_limitation_state",
            "ollama_call_performed",
        ),
    }

    issues_observed: list[str] = []
    readiness_gaps = plan_payload.get("readiness_gaps", [])
    input_warnings = plan_payload.get("input_warnings", [])
    if readiness_gaps:
        issues_observed.append("readiness_gaps_present")
    if input_warnings:
        issues_observed.append("input_warnings_present")
    if boundary_checks["human_review_required"] is not True:
        issues_observed.append("human_review_not_confirmed")
    if boundary_checks["accepted"] is not False:
        issues_observed.append("accepted_state_not_false")
    if boundary_checks["approval_claimed"] is not False:
        issues_observed.append("approval_claim_not_false")
    if boundary_checks["release_claimed"] is not False:
        issues_observed.append("release_claim_not_false")
    if boundary_checks["download_allowed"] is not False:
        issues_observed.append("download_allowed_not_false")

    return {
        "checkpoint": "M33.6 — Corrective implementation package",
        "surface": "cli-enhanced controlled local workflow",
        "correction_id": "M33.5-001",
        "correction_summary": "Compact trial-summary command for repeated manual local workflow trial output capture.",
        "adapter_boundary": "Read-only summary assembled from existing local workflow payload builders.",
        "selected_work_package": {
            "wp_id": selected_work_package.get("wp_id"),
            "title": selected_work_package.get("title"),
            "status": selected_work_package.get("status"),
            "selector_context": selector_context,
        },
        "trial_summary": {
            "workflow_path": ["scenario", "configure", "plan", "status", "outputs"],
            "summarized_commands": ["plan", "status", "outputs"],
            "task_count": plan_payload.get("task_staging", {}).get("task_count"),
            "task_ids": plan_payload.get("task_staging", {}).get("task_ids", []),
            "source_collection_ids": source_selection.get("collection_ids", []),
            "standards_bundles": selector_context.get("standards_bundles", []),
            "plan_count": status_payload.get("schedule_lifecycle", {}).get("plan_count"),
            "generated_schedule_present": status_payload.get("schedule_lifecycle", {}).get("generated_schedule_present"),
            "artifact_available": artifact_metadata.get("artifact_available"),
            "output_validation_available": outputs_payload.get("output_validation_state", {}).get("validation_available"),
        },
        "command_results": command_results,
        "boundary_checks": boundary_checks,
        "source_and_standards_boundary": {
            "collection_ids": source_selection.get("collection_ids", []),
            "authority_limit": source_selection.get("authority_limit"),
        },
        "ai_boundary": ai_limitation_state,
        "output_review_boundary": {
            "human_review_required": review_acceptance_status.get("human_review_required"),
            "accepted": review_acceptance_status.get("accepted"),
            "approval_claimed": review_acceptance_status.get("approval_claimed"),
            "release_claimed": review_acceptance_status.get("release_claimed"),
            "download_allowed": safe_artifact_access.get("download_allowed"),
        },
        "issues_observed": issues_observed,
        "limitations": [
            "Trial summary is read-only and does not mutate workflow state.",
            "Trial summary reduces evidence-capture friction but does not replace detailed command evidence when required.",
            "No AI, provider, Ollama, or live model call is performed by this command.",
            "Generated or assembled output remains human-review-required.",
            "This is not release, deployment, SaaS, commercial, or customer-ready evidence.",
        ],
    }
