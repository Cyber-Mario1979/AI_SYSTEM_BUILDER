"""Document lifecycle to task/workflow-state integration for M12.7.

This module evaluates deterministic readiness effects from governed document
artifact lifecycle state. It intentionally returns workflow-readiness signals
and recommended effects only; it does not mutate persisted task, work package,
collection, plan, or document artifact state.
"""

from __future__ import annotations

from typing import Any

from .artifact_lifecycle import (
    ACTIVE_LIFECYCLE_STATE,
    ARCHIVED_LIFECYCLE_STATE,
    EXPIRED_LIFECYCLE_STATE,
    IN_APPROVAL_LIFECYCLE_STATE,
    IN_REVIEW_LIFECYCLE_STATE,
    SUPERSEDED_LIFECYCLE_STATE,
    SUPPORTED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES,
    TRAINING_DELIVERY_LIFECYCLE_STATE,
    validate_document_artifact_lifecycle_payload,
)

DOCUMENT_WORKFLOW_INTEGRATION_CHECKPOINT_ID = "M12.7"
DOCUMENT_WORKFLOW_INTEGRATION_CONTRACT_VERSION = (
    "document-workflow-integration-contract-v1"
)

READINESS_EVALUATION_ONLY_BOUNDARY = (
    "document_lifecycle_integration_evaluates_readiness_without_mutating_task_or_workflow_state"
)

NO_STATE_CHANGE_EFFECT = "no_state_change"
BLOCK_COMPLETION_EFFECT = "block_completion"
ALLOW_COMPLETION_EFFECT = "allow_completion"
REQUIRES_REPLACEMENT_DOCUMENT_EFFECT = "requires_replacement_document"
HISTORICAL_RECORD_ONLY_EFFECT = "historical_record_only"

SUPPORTED_WORKFLOW_EFFECTS = (
    NO_STATE_CHANGE_EFFECT,
    BLOCK_COMPLETION_EFFECT,
    ALLOW_COMPLETION_EFFECT,
    REQUIRES_REPLACEMENT_DOCUMENT_EFFECT,
    HISTORICAL_RECORD_ONLY_EFFECT,
)

TASK_CLOSURE_READY_SIGNAL = "task_closure_ready"
TASK_CLOSURE_BLOCKED_SIGNAL = "task_closure_blocked"
REPLACEMENT_DOCUMENT_REQUIRED_SIGNAL = "replacement_document_required"
HISTORICAL_RECORD_ONLY_SIGNAL = "historical_record_only"

SUPPORTED_WORKFLOW_READINESS_SIGNALS = (
    TASK_CLOSURE_READY_SIGNAL,
    TASK_CLOSURE_BLOCKED_SIGNAL,
    REPLACEMENT_DOCUMENT_REQUIRED_SIGNAL,
    HISTORICAL_RECORD_ONLY_SIGNAL,
)

SUPPORTED_TASK_STATUSES = (
    "planned",
    "in_progress",
    "completed",
    "over_due",
)

_REQUIRED_OBLIGATION_FIELDS = (
    "obligation_id",
    "task_id",
    "required_document_family",
    "required_artifact_id",
    "required_lifecycle_state",
    "obligation_scope",
    "closure_required",
    "allowed_interim_lifecycle_states",
)

_REQUIRED_READINESS_FIELDS = (
    "checkpoint",
    "contract_version",
    "task_id",
    "task_current_status",
    "document_obligations",
    "satisfied_obligations",
    "blocked_obligations",
    "task_closure_ready",
    "recommended_task_state_effect",
    "workflow_readiness_signal",
    "mutation_boundary",
)

_PROHIBITED_INTEGRATION_FIELDS = (
    "task_state_update",
    "workflow_state_update",
    "persisted_state_write",
    "document_lifecycle_mutation",
    "work_package_state_update",
)


def build_document_workflow_integration_baseline() -> dict[str, Any]:
    """Return the explicit M12.7 workflow-integration baseline."""

    return {
        "checkpoint": DOCUMENT_WORKFLOW_INTEGRATION_CHECKPOINT_ID,
        "contract_version": DOCUMENT_WORKFLOW_INTEGRATION_CONTRACT_VERSION,
        "mutation_boundary": READINESS_EVALUATION_ONLY_BOUNDARY,
        "supported_workflow_effects": list(SUPPORTED_WORKFLOW_EFFECTS),
        "supported_workflow_readiness_signals": list(
            SUPPORTED_WORKFLOW_READINESS_SIGNALS
        ),
        "default_required_lifecycle_state": ACTIVE_LIFECYCLE_STATE,
        "closure_policy": (
            "closure_required_document_obligations_must_be_satisfied_before_task_completion"
        ),
        "training_delivery_policy": (
            "training_delivery_blocks_closure_unless_explicitly_allowed_as_interim"
        ),
        "superseded_or_expired_policy": (
            "superseded_or_expired_documents_require_replacement_active_document"
        ),
        "archived_policy": (
            "archived_documents_are_historical_records_only_not_active_closure_evidence"
        ),
    }


def build_task_document_obligation(
    *,
    obligation_id: str,
    task_id: str,
    required_document_family: str,
    required_artifact_id: str,
    required_lifecycle_state: str = ACTIVE_LIFECYCLE_STATE,
    obligation_scope: str = "task_closure",
    closure_required: bool = True,
    allowed_interim_lifecycle_states: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Build one deterministic task-document obligation."""

    _validate_non_empty_string(obligation_id, "obligation_id")
    _validate_non_empty_string(task_id, "task_id")
    _validate_non_empty_string(
        required_document_family,
        "required_document_family",
    )
    _validate_non_empty_string(required_artifact_id, "required_artifact_id")
    _validate_lifecycle_state(required_lifecycle_state)

    interim_states = list(allowed_interim_lifecycle_states or [])
    for state in interim_states:
        _validate_lifecycle_state(state)

    obligation = {
        "obligation_id": obligation_id,
        "task_id": task_id,
        "required_document_family": required_document_family,
        "required_artifact_id": required_artifact_id,
        "required_lifecycle_state": required_lifecycle_state,
        "obligation_scope": obligation_scope,
        "closure_required": closure_required,
        "allowed_interim_lifecycle_states": interim_states,
    }
    validate_task_document_obligation(obligation)
    return obligation


def evaluate_task_document_workflow_readiness(
    *,
    task_payload: dict[str, object],
    document_obligations: list[dict[str, object]]
    | tuple[dict[str, object], ...],
    document_artifacts: list[dict[str, object]]
    | tuple[dict[str, object], ...],
) -> dict[str, Any]:
    """Evaluate task closure readiness from document lifecycle obligations.

    This function is intentionally read-only. It returns recommended task-state
    effects and workflow-readiness signals without changing task or artifact
    payloads.
    """

    task_id = _extract_task_id(task_payload)
    task_current_status = _extract_task_status(task_payload)
    artifact_index = _build_artifact_index(document_artifacts)

    obligation_results = [
        _evaluate_single_obligation(
            obligation,
            task_id=task_id,
            artifact_index=artifact_index,
        )
        for obligation in document_obligations
    ]

    satisfied_obligations = [
        result for result in obligation_results if result["satisfied"] is True
    ]
    blocked_obligations = [
        result for result in obligation_results if result["blocking"] is True
    ]

    task_closure_ready = not blocked_obligations
    recommended_effect = _select_recommended_task_state_effect(
        obligation_results,
        task_closure_ready=task_closure_ready,
    )
    readiness_signal = _select_workflow_readiness_signal(
        recommended_effect,
        task_closure_ready=task_closure_ready,
    )

    payload: dict[str, Any] = {
        "checkpoint": DOCUMENT_WORKFLOW_INTEGRATION_CHECKPOINT_ID,
        "contract_version": DOCUMENT_WORKFLOW_INTEGRATION_CONTRACT_VERSION,
        "task_id": task_id,
        "task_current_status": task_current_status,
        "document_obligations": list(document_obligations),
        "satisfied_obligations": satisfied_obligations,
        "blocked_obligations": blocked_obligations,
        "task_closure_ready": task_closure_ready,
        "recommended_task_state_effect": recommended_effect,
        "workflow_readiness_signal": readiness_signal,
        "mutation_boundary": READINESS_EVALUATION_ONLY_BOUNDARY,
    }
    validate_task_document_workflow_readiness_payload(payload)
    return payload


def validate_task_document_obligation(obligation: dict[str, object]) -> None:
    """Validate one M12.7 task-document obligation."""

    _validate_required_fields(
        obligation,
        _REQUIRED_OBLIGATION_FIELDS,
        "Task document obligation",
    )

    for field_name in (
        "obligation_id",
        "task_id",
        "required_document_family",
        "required_artifact_id",
        "required_lifecycle_state",
        "obligation_scope",
    ):
        value = obligation[field_name]
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string.")
        _validate_non_empty_string(value, field_name)

    _validate_lifecycle_state(str(obligation["required_lifecycle_state"]))

    closure_required = obligation["closure_required"]
    if not isinstance(closure_required, bool):
        raise ValueError("closure_required must be a boolean.")

    interim_states = obligation["allowed_interim_lifecycle_states"]
    if not isinstance(interim_states, list):
        raise ValueError("allowed_interim_lifecycle_states must be a list.")
    for state in interim_states:
        if not isinstance(state, str):
            raise ValueError(
                "allowed_interim_lifecycle_states must contain strings."
            )
        _validate_lifecycle_state(state)


def validate_task_document_workflow_readiness_payload(
    payload: dict[str, object],
) -> None:
    """Validate an M12.7 task-document workflow-readiness payload."""

    _validate_required_fields(
        payload,
        _REQUIRED_READINESS_FIELDS,
        "Task document workflow readiness payload",
    )
    _validate_no_prohibited_integration_fields(payload)

    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=DOCUMENT_WORKFLOW_INTEGRATION_CHECKPOINT_ID,
        error_prefix="Task document workflow readiness payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=DOCUMENT_WORKFLOW_INTEGRATION_CONTRACT_VERSION,
        error_prefix="Task document workflow readiness payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="mutation_boundary",
        expected_value=READINESS_EVALUATION_ONLY_BOUNDARY,
        error_prefix="Task document workflow readiness payload",
    )

    task_id = payload["task_id"]
    if not isinstance(task_id, str):
        raise ValueError("task_id must be a string.")
    _validate_non_empty_string(task_id, "task_id")

    task_status = payload["task_current_status"]
    if not isinstance(task_status, str) or task_status not in SUPPORTED_TASK_STATUSES:
        raise ValueError(
            "Unsupported task_current_status. Expected one of: "
            f"{', '.join(SUPPORTED_TASK_STATUSES)}."
        )

    obligations = payload["document_obligations"]
    if not isinstance(obligations, list):
        raise ValueError("document_obligations must be a list.")
    for obligation in obligations:
        if not isinstance(obligation, dict):
            raise ValueError("Each document obligation must be a mapping.")
        validate_task_document_obligation(obligation)

    satisfied = payload["satisfied_obligations"]
    blocked = payload["blocked_obligations"]
    if not isinstance(satisfied, list):
        raise ValueError("satisfied_obligations must be a list.")
    if not isinstance(blocked, list):
        raise ValueError("blocked_obligations must be a list.")

    task_closure_ready = payload["task_closure_ready"]
    if not isinstance(task_closure_ready, bool):
        raise ValueError("task_closure_ready must be a boolean.")

    recommended_effect = payload["recommended_task_state_effect"]
    if (
        not isinstance(recommended_effect, str)
        or recommended_effect not in SUPPORTED_WORKFLOW_EFFECTS
    ):
        raise ValueError(
            "Unsupported recommended_task_state_effect. Expected one of: "
            f"{', '.join(SUPPORTED_WORKFLOW_EFFECTS)}."
        )

    readiness_signal = payload["workflow_readiness_signal"]
    if (
        not isinstance(readiness_signal, str)
        or readiness_signal not in SUPPORTED_WORKFLOW_READINESS_SIGNALS
    ):
        raise ValueError(
            "Unsupported workflow_readiness_signal. Expected one of: "
            f"{', '.join(SUPPORTED_WORKFLOW_READINESS_SIGNALS)}."
        )

    if task_closure_ready and blocked:
        raise ValueError(
            "task_closure_ready cannot be true when blocked_obligations exist."
        )
    if not task_closure_ready and not blocked:
        raise ValueError(
            "task_closure_ready cannot be false without blocked_obligations."
        )


def _evaluate_single_obligation(
    obligation: dict[str, object],
    *,
    task_id: str,
    artifact_index: dict[str, dict[str, object]],
) -> dict[str, Any]:
    validate_task_document_obligation(obligation)

    if obligation["task_id"] != task_id:
        raise ValueError(
            "Task document obligation task_id must match task_payload task_id."
        )

    artifact_id = str(obligation["required_artifact_id"])
    artifact = artifact_index.get(artifact_id)

    if artifact is None:
        return _build_obligation_result(
            obligation,
            actual_lifecycle_state=None,
            satisfied=False,
            blocking=bool(obligation["closure_required"]),
            recommended_effect=BLOCK_COMPLETION_EFFECT,
            reason="required_document_artifact_not_bound",
            artifact_ref=None,
        )

    artifact_family = artifact["document_family"]
    if artifact_family != obligation["required_document_family"]:
        return _build_obligation_result(
            obligation,
            actual_lifecycle_state=str(artifact["lifecycle_state"]),
            satisfied=False,
            blocking=bool(obligation["closure_required"]),
            recommended_effect=BLOCK_COMPLETION_EFFECT,
            reason="required_document_family_mismatch",
            artifact_ref=artifact_id,
        )

    lifecycle_state = str(artifact["lifecycle_state"])
    required_state = str(obligation["required_lifecycle_state"])
    interim_states = obligation["allowed_interim_lifecycle_states"]
    assert isinstance(interim_states, list)

    if lifecycle_state == required_state or lifecycle_state in interim_states:
        return _build_obligation_result(
            obligation,
            actual_lifecycle_state=lifecycle_state,
            satisfied=True,
            blocking=False,
            recommended_effect=NO_STATE_CHANGE_EFFECT,
            reason="document_obligation_satisfied",
            artifact_ref=artifact_id,
        )

    if lifecycle_state in (SUPERSEDED_LIFECYCLE_STATE, EXPIRED_LIFECYCLE_STATE):
        return _build_obligation_result(
            obligation,
            actual_lifecycle_state=lifecycle_state,
            satisfied=False,
            blocking=bool(obligation["closure_required"]),
            recommended_effect=REQUIRES_REPLACEMENT_DOCUMENT_EFFECT,
            reason="document_requires_replacement_active_version",
            artifact_ref=artifact_id,
        )

    if lifecycle_state == ARCHIVED_LIFECYCLE_STATE:
        return _build_obligation_result(
            obligation,
            actual_lifecycle_state=lifecycle_state,
            satisfied=False,
            blocking=bool(obligation["closure_required"]),
            recommended_effect=HISTORICAL_RECORD_ONLY_EFFECT,
            reason="archived_document_is_historical_record_only",
            artifact_ref=artifact_id,
        )

    if lifecycle_state == TRAINING_DELIVERY_LIFECYCLE_STATE:
        return _build_obligation_result(
            obligation,
            actual_lifecycle_state=lifecycle_state,
            satisfied=False,
            blocking=bool(obligation["closure_required"]),
            recommended_effect=BLOCK_COMPLETION_EFFECT,
            reason="training_delivery_blocks_closure_without_explicit_interim_allowance",
            artifact_ref=artifact_id,
        )

    if lifecycle_state in (
        IN_REVIEW_LIFECYCLE_STATE,
        IN_APPROVAL_LIFECYCLE_STATE,
    ):
        return _build_obligation_result(
            obligation,
            actual_lifecycle_state=lifecycle_state,
            satisfied=False,
            blocking=bool(obligation["closure_required"]),
            recommended_effect=BLOCK_COMPLETION_EFFECT,
            reason="document_not_yet_active",
            artifact_ref=artifact_id,
        )

    return _build_obligation_result(
        obligation,
        actual_lifecycle_state=lifecycle_state,
        satisfied=False,
        blocking=bool(obligation["closure_required"]),
        recommended_effect=BLOCK_COMPLETION_EFFECT,
        reason="document_lifecycle_state_does_not_satisfy_obligation",
        artifact_ref=artifact_id,
    )


def _build_obligation_result(
    obligation: dict[str, object],
    *,
    actual_lifecycle_state: str | None,
    satisfied: bool,
    blocking: bool,
    recommended_effect: str,
    reason: str,
    artifact_ref: str | None,
) -> dict[str, Any]:
    return {
        "obligation_id": obligation["obligation_id"],
        "task_id": obligation["task_id"],
        "required_document_family": obligation["required_document_family"],
        "required_artifact_id": obligation["required_artifact_id"],
        "required_lifecycle_state": obligation["required_lifecycle_state"],
        "actual_lifecycle_state": actual_lifecycle_state,
        "obligation_scope": obligation["obligation_scope"],
        "closure_required": obligation["closure_required"],
        "satisfied": satisfied,
        "blocking": blocking,
        "recommended_effect": recommended_effect,
        "reason": reason,
        "artifact_ref": artifact_ref,
    }


def _select_recommended_task_state_effect(
    obligation_results: list[dict[str, object]],
    *,
    task_closure_ready: bool,
) -> str:
    effects = [str(result["recommended_effect"]) for result in obligation_results]

    if REQUIRES_REPLACEMENT_DOCUMENT_EFFECT in effects:
        return REQUIRES_REPLACEMENT_DOCUMENT_EFFECT
    if HISTORICAL_RECORD_ONLY_EFFECT in effects:
        return HISTORICAL_RECORD_ONLY_EFFECT
    if BLOCK_COMPLETION_EFFECT in effects:
        return BLOCK_COMPLETION_EFFECT
    if task_closure_ready:
        return ALLOW_COMPLETION_EFFECT
    return NO_STATE_CHANGE_EFFECT


def _select_workflow_readiness_signal(
    recommended_effect: str,
    *,
    task_closure_ready: bool,
) -> str:
    if recommended_effect == REQUIRES_REPLACEMENT_DOCUMENT_EFFECT:
        return REPLACEMENT_DOCUMENT_REQUIRED_SIGNAL
    if recommended_effect == HISTORICAL_RECORD_ONLY_EFFECT:
        return HISTORICAL_RECORD_ONLY_SIGNAL
    if task_closure_ready:
        return TASK_CLOSURE_READY_SIGNAL
    return TASK_CLOSURE_BLOCKED_SIGNAL


def _build_artifact_index(
    document_artifacts: list[dict[str, object]] | tuple[dict[str, object], ...],
) -> dict[str, dict[str, object]]:
    artifact_index: dict[str, dict[str, object]] = {}

    for artifact in document_artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("Each document artifact must be a mapping.")
        validate_document_artifact_lifecycle_payload(artifact)
        artifact_id = artifact["artifact_id"]
        if not isinstance(artifact_id, str):
            raise ValueError("artifact_id must be a string.")
        if artifact_id in artifact_index:
            raise ValueError(f"Duplicate document artifact_id is not allowed: {artifact_id}.")
        artifact_index[artifact_id] = artifact

    return artifact_index


def _extract_task_id(task_payload: dict[str, object]) -> str:
    task_id = task_payload.get("task_id")
    if not isinstance(task_id, str) or not task_id.strip():
        raise ValueError("task_payload must declare non-empty task_id.")
    return task_id


def _extract_task_status(task_payload: dict[str, object]) -> str:
    status = task_payload.get("status")
    if not isinstance(status, str) or status not in SUPPORTED_TASK_STATUSES:
        raise ValueError(
            "Unsupported task status. Expected one of: "
            f"{', '.join(SUPPORTED_TASK_STATUSES)}."
        )
    return status


def _validate_lifecycle_state(lifecycle_state: str) -> None:
    if lifecycle_state not in SUPPORTED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES:
        raise ValueError(
            "Unsupported lifecycle_state. Expected one of: "
            f"{', '.join(SUPPORTED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES)}."
        )


def _validate_no_prohibited_integration_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_INTEGRATION_FIELDS:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in document workflow integration payloads."
            )


def _validate_required_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        if field_name not in payload:
            raise ValueError(f"{error_prefix} must declare {field_name}.")


def _validate_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _validate_expected_exact_value(
    payload: dict[str, object],
    *,
    field_name: str,
    expected_value: str,
    error_prefix: str,
) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: "
            f"expected {expected_value!r}, got {actual_value!r}."
        )
