"""Visible and safe local workflow error/failure handling for M32.7.

This module builds bounded failure payloads for the local workflow adapter.
It does not mutate state, call AI/providers, approve output, or claim
readiness when a failure or limitation is present.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from asbp.local_workflow_logic import LOCAL_WORKFLOW_SURFACE

LOCAL_WORKFLOW_FAILURE_CHECKPOINT = "M32.7 — Local workflow error/failure handling"

LOCAL_WORKFLOW_FAILURE_LIMITATIONS = [
    "CLI/local workflow surface is an adapter only.",
    "Failure handling is visibility/control behavior only and does not mutate state.",
    "No workflow payload is treated as successful when a blocking failure is present.",
    "No traceback, raw provider payload, raw model output, approval, release, or certification evidence is produced.",
    "No AI, provider, Ollama, or live model call is performed by this failure surface.",
    "Generated or assembled output remains human-review-required.",
    "This is not release, deployment, SaaS, commercial, or customer-ready evidence.",
]

LOCAL_WORKFLOW_FAILURE_SAFE_ACTIONS = [
    "Resolve the blocking failure before continuing the local workflow.",
    "Do not treat the failed command as readiness, validation, output, approval, release, or UAT evidence.",
]


def _clean_optional_list(values: list[str] | None) -> list[str]:
    return [value for value in values or [] if value]


def build_local_workflow_failure_payload(
    *,
    command: str | None,
    error_code: str,
    message: str,
    detail: str | None = None,
    blocking: bool = True,
    safe_to_continue: bool = False,
    context: dict[str, Any] | None = None,
    limitations: list[str] | None = None,
    next_safe_actions: list[str] | None = None,
) -> dict[str, Any]:
    """Build a bounded local workflow failure/limitation payload."""

    failure_state: dict[str, Any] = {
        "error_code": error_code,
        "message": message,
        "detail": detail,
        "blocking": blocking,
        "safe_to_continue": safe_to_continue,
    }

    if context:
        failure_state["context"] = context

    return {
        "checkpoint": LOCAL_WORKFLOW_FAILURE_CHECKPOINT,
        "surface": LOCAL_WORKFLOW_SURFACE,
        "adapter_boundary": "CLI adapter reports bounded failure state through M32.7 failure handling only.",
        "command": command,
        "status": "failed" if blocking else "limited",
        "success": False,
        "failure_state": failure_state,
        "limitations": list(LOCAL_WORKFLOW_FAILURE_LIMITATIONS)
        + _clean_optional_list(limitations),
        "next_safe_actions": list(LOCAL_WORKFLOW_FAILURE_SAFE_ACTIONS)
        + _clean_optional_list(next_safe_actions),
    }


def build_missing_input_failure_payload(
    *,
    command: str | None,
    message: str,
) -> dict[str, Any]:
    """Build a failure payload for missing or uncontrolled CLI input."""

    return build_local_workflow_failure_payload(
        command=command,
        error_code="LOCAL_WORKFLOW_MISSING_INPUT",
        message=message,
        detail="Required local workflow command/input was missing or invalid.",
        next_safe_actions=[
            "Supply one supported local workflow command with its required controlled arguments.",
        ],
    )


def build_missing_state_failure_payload(
    *,
    command: str | None,
    state_file_path: Path,
) -> dict[str, Any]:
    """Build a failure payload for a missing local workflow state file."""

    return build_local_workflow_failure_payload(
        command=command,
        error_code="LOCAL_WORKFLOW_STATE_MISSING",
        message=f"State file not found: {state_file_path}",
        detail="No state file found. Run 'state init' first.",
        context={"state_file_path": str(state_file_path)},
        next_safe_actions=[
            "Initialize state or restore a validated local state file before retrying.",
        ],
    )


def build_invalid_state_failure_payload(
    *,
    command: str | None,
    message: str,
    detail: str | None = None,
) -> dict[str, Any]:
    """Build a failure payload for invalid JSON or failed state validation."""

    return build_local_workflow_failure_payload(
        command=command,
        error_code="LOCAL_WORKFLOW_STATE_INVALID",
        message=message,
        detail=detail,
        next_safe_actions=[
            "Correct the state file and reload it through the approved state boundary.",
        ],
    )


def build_invalid_reference_failure_payload(
    *,
    command: str | None,
    message: str,
) -> dict[str, Any]:
    """Build a failure payload for an invalid work-package or local reference."""

    return build_local_workflow_failure_payload(
        command=command,
        error_code="LOCAL_WORKFLOW_INVALID_REFERENCE",
        message=message,
        detail="The requested local workflow reference was not found in validated state.",
        next_safe_actions=[
            "Select a valid work package or restore state containing the requested reference.",
        ],
    )


def build_source_limitation_failure_payload(
    *,
    command: str | None,
    message: str,
    detail: str | None = None,
    blocking: bool = True,
) -> dict[str, Any]:
    """Build a visible source/citation limitation payload."""

    return build_local_workflow_failure_payload(
        command=command,
        error_code="LOCAL_WORKFLOW_SOURCE_LIMITATION",
        message=message,
        detail=detail,
        blocking=blocking,
        safe_to_continue=not blocking,
        limitations=[
            "Source, citation, retrieval, and standards limitations must remain visible and cannot be upgraded into authority by this surface.",
        ],
        next_safe_actions=[
            "Resolve missing source/citation evidence or keep the workflow explicitly limited.",
        ],
    )


def build_validation_error_failure_payload(
    *,
    command: str | None,
    message: str,
    detail: str | None = None,
    blocking: bool = True,
) -> dict[str, Any]:
    """Build a visible validation error/limitation payload."""

    return build_local_workflow_failure_payload(
        command=command,
        error_code="LOCAL_WORKFLOW_VALIDATION_ERROR",
        message=message,
        detail=detail,
        blocking=blocking,
        safe_to_continue=not blocking,
        limitations=[
            "Validation errors or missing validation evidence cannot be treated as acceptance, approval, release, or certification.",
        ],
        next_safe_actions=[
            "Run or repair validation before making readiness or output claims.",
        ],
    )


def build_provider_failure_payload(
    *,
    command: str | None,
    message: str,
    detail: str | None = None,
    blocking: bool = True,
) -> dict[str, Any]:
    """Build a safe provider/AI failure payload without performing provider calls."""

    return build_local_workflow_failure_payload(
        command=command,
        error_code="LOCAL_WORKFLOW_PROVIDER_FAILURE",
        message=message,
        detail=detail,
        blocking=blocking,
        safe_to_continue=not blocking,
        context={
            "ai_call_performed": False,
            "provider_call_performed": False,
            "ollama_call_performed": False,
            "ai_result_claimed": False,
        },
        limitations=[
            "AI/provider/Ollama failure is visible only; no fallback model output or provider payload is treated as product evidence.",
        ],
        next_safe_actions=[
            "Keep AI/provider behavior out of scope unless separately authorized and validated.",
        ],
    )
