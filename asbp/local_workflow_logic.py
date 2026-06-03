"""Local workflow planning logic for the M32.3 CLI adapter boundary.

This module is deliberately read-only. It builds a bounded local workflow
planning payload from validated state and existing core/service boundary data.
"""

from __future__ import annotations

from typing import Any

from asbp.core.collections import build_work_package_collection_ids
from asbp.core.work_packages import (
    build_work_package_task_ids,
    find_work_package_by_id,
)
from asbp.state_model import StateModel, WorkPackageModel

LOCAL_WORKFLOW_SURFACE = "cli-enhanced controlled local workflow"
LOCAL_WORKFLOW_CHECKPOINT = "M32.3 — UI-to-core adapter implementation"

LOCAL_WORKFLOW_LIMITATIONS = [
    "CLI/local workflow surface is an adapter only.",
    "No domain logic is implemented in the CLI surface.",
    "No state mutation is performed by this planning command.",
    "No AI, provider, Ollama, or live model call is performed.",
    "Generated or assembled output remains human-review-required.",
    "Retrieval, where later included, remains helper-only and non-authoritative.",
    "This is not release, deployment, SaaS, commercial, or customer-ready evidence.",
]

_SYSTEM_TITLE_HINTS: dict[str, tuple[str, ...]] = {
    "cleanroom-hvac": (
        "cleanroom",
        "clean room",
        "hvac",
        "ahu",
        "room",
        "suite",
    ),
    "automation": (
        "automation",
        "plc",
        "scada",
        "control",
        "controls",
        "system",
    ),
}


def _clean_selector_context(selector_context: Any) -> dict[str, Any] | None:
    if selector_context is None:
        return None

    context_payload = selector_context.model_dump()
    cleaned_payload = {
        key: value
        for key, value in context_payload.items()
        if value is not None and value != []
    }
    return cleaned_payload or None


def build_local_workflow_input_warnings(
    work_package: WorkPackageModel,
) -> list[str]:
    """Build non-blocking controlled-input consistency warnings.

    These warnings are intentionally simple title/profile alignment checks.
    They do not classify CQV scope or block execution; they make mismatches
    visible so a human can review them.
    """

    selector_context = work_package.selector_context
    if selector_context is None or selector_context.system_type is None:
        return []

    expected_title_hints = _SYSTEM_TITLE_HINTS.get(selector_context.system_type)
    if expected_title_hints is None:
        return []

    normalized_title = work_package.title.lower()
    if any(hint in normalized_title for hint in expected_title_hints):
        return []

    return [
        "Selected system_type "
        f"{selector_context.system_type} may not match work package title: "
        f"{work_package.title}"
    ]


def build_local_workflow_plan_payload(
    state: StateModel,
    *,
    wp_id: str,
) -> dict[str, Any]:
    """Build a read-only local workflow planning payload for a work package.

    The payload is intentionally conservative: it exposes selected boundaries,
    linked workflow inputs, visible limitations, and safe next actions without
    mutating state or claiming product readiness.
    """

    work_package = find_work_package_by_id(state.work_packages, wp_id)
    if work_package is None:
        raise ValueError(f"Work Package not found: {wp_id}")

    task_ids = build_work_package_task_ids(state.tasks, wp_id=work_package.wp_id)
    collection_ids = build_work_package_collection_ids(
        state.task_collections,
        wp_id=work_package.wp_id,
    )

    selector_context = _clean_selector_context(work_package.selector_context)

    readiness_gaps: list[str] = []
    if selector_context is None:
        readiness_gaps.append("No preset/profile/source selector context is bound.")
    if not task_ids:
        readiness_gaps.append("No staged tasks are associated with this work package.")
    if not collection_ids:
        readiness_gaps.append("No source/task collection is bound to this work package.")

    return {
        "checkpoint": LOCAL_WORKFLOW_CHECKPOINT,
        "surface": LOCAL_WORKFLOW_SURFACE,
        "adapter_boundary": "CLI adapter reads validated state and calls service/core boundaries only.",
        "project": state.project,
        "state_status": state.status,
        "selected_work_package": {
            "wp_id": work_package.wp_id,
            "title": work_package.title,
            "status": work_package.status,
            "selector_context": selector_context,
        },
        "task_staging": {
            "task_count": len(task_ids),
            "task_ids": task_ids,
        },
        "source_selection": {
            "collection_count": len(collection_ids),
            "collection_ids": collection_ids,
            "authority_limit": "Existing repo state only; no retrieval or standards authority is upgraded.",
        },
        "review_gates": [
            "Human review required before output acceptance.",
            "Limitations must remain visible before trial or UAT claims.",
        ],
        "input_warnings": build_local_workflow_input_warnings(work_package),
        "readiness_gaps": readiness_gaps,
        "limitations": list(LOCAL_WORKFLOW_LIMITATIONS),
        "next_safe_actions": [
            "Resolve readiness gaps before calling the workflow trial-ready.",
            "Use later M32 checkpoints for controlled inputs, visibility, output review, and failure handling.",
        ],
    }
