"""Document artifact lifecycle model for M12.6.

This module defines controlled GMP/CQV document lifecycle truth.
It intentionally does not integrate document state with task/workflow state;
that boundary belongs to M12.7.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .template_governance import validate_template_identity

DOCUMENT_ARTIFACT_LIFECYCLE_CHECKPOINT_ID = "M12.6"
DOCUMENT_ARTIFACT_LIFECYCLE_CONTRACT_VERSION = (
    "document-artifact-lifecycle-contract-v1"
)

DRAFT_LIFECYCLE_STATE = "draft"
IN_REVIEW_LIFECYCLE_STATE = "in_review"
IN_APPROVAL_LIFECYCLE_STATE = "in_approval"
TRAINING_DELIVERY_LIFECYCLE_STATE = "training_delivery"
ACTIVE_LIFECYCLE_STATE = "active"
SUPERSEDED_LIFECYCLE_STATE = "superseded"
EXPIRED_LIFECYCLE_STATE = "expired"
ARCHIVED_LIFECYCLE_STATE = "archived"

SUPPORTED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES = (
    DRAFT_LIFECYCLE_STATE,
    IN_REVIEW_LIFECYCLE_STATE,
    IN_APPROVAL_LIFECYCLE_STATE,
    TRAINING_DELIVERY_LIFECYCLE_STATE,
    ACTIVE_LIFECYCLE_STATE,
    SUPERSEDED_LIFECYCLE_STATE,
    EXPIRED_LIFECYCLE_STATE,
    ARCHIVED_LIFECYCLE_STATE,
)

PROHIBITED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES = (
    "approved",
    "finalized",
    "reopened",
)

DOCUMENT_LIFECYCLE_TRUTH_BOUNDARY = (
    "document_lifecycle_truth_is_deterministic_and_independent_of_ai_phrasing"
)
POST_ACTIVE_CHANGE_POLICY = (
    "post_active_changes_require_new_version_and_supersede_previous_active_version"
)
RETENTION_BASIS_ACTIVE_LIFETIME_PLUS_POLICY = (
    "active_lifetime_plus_policy_defined_retention_period"
)

DOCUMENT_ARTIFACT_TRANSITION_RULES: dict[str, tuple[str, ...]] = {
    DRAFT_LIFECYCLE_STATE: (IN_REVIEW_LIFECYCLE_STATE,),
    IN_REVIEW_LIFECYCLE_STATE: (IN_APPROVAL_LIFECYCLE_STATE,),
    IN_APPROVAL_LIFECYCLE_STATE: (
        TRAINING_DELIVERY_LIFECYCLE_STATE,
        ACTIVE_LIFECYCLE_STATE,
    ),
    TRAINING_DELIVERY_LIFECYCLE_STATE: (ACTIVE_LIFECYCLE_STATE,),
    ACTIVE_LIFECYCLE_STATE: (
        SUPERSEDED_LIFECYCLE_STATE,
        EXPIRED_LIFECYCLE_STATE,
    ),
    SUPERSEDED_LIFECYCLE_STATE: (ARCHIVED_LIFECYCLE_STATE,),
    EXPIRED_LIFECYCLE_STATE: (ARCHIVED_LIFECYCLE_STATE,),
    ARCHIVED_LIFECYCLE_STATE: (),
}

_REQUIRED_ARTIFACT_FIELDS = (
    "checkpoint",
    "contract_version",
    "artifact_id",
    "document_family",
    "document_id",
    "artifact_version",
    "template_identity",
    "document_request_ref",
    "lifecycle_state",
    "lifecycle_history",
    "training_required",
    "effective_date",
    "expiry_due_date",
    "previous_version_ref",
    "supersedes_ref",
    "superseded_by_ref",
    "event_ref",
    "retention_metadata",
    "lifecycle_truth_boundary",
    "post_active_change_policy",
)

_REQUIRED_DOCUMENT_REQUEST_REF_FIELDS = (
    "document_job_id",
    "document_id",
    "document_request_contract_version",
)

_REQUIRED_HISTORY_EVENT_FIELDS = (
    "from_state",
    "to_state",
    "event_ref",
    "transition_reason",
)

_REQUIRED_RETENTION_METADATA_FIELDS = (
    "retention_basis",
    "retention_period_source",
    "retention_trigger",
    "dependency_refs",
)

_PROHIBITED_ARTIFACT_FIELDS = (
    "generated_language_output",
    "generated_content",
    "approval_decision",
    "approved_document_state",
    "finalized_document_state",
    "reopened_document_state",
    "task_state_update",
    "workflow_state_update",
)


def build_document_artifact_lifecycle_baseline() -> dict[str, Any]:
    """Return the explicit M12.6 lifecycle baseline."""

    return {
        "checkpoint": DOCUMENT_ARTIFACT_LIFECYCLE_CHECKPOINT_ID,
        "contract_version": DOCUMENT_ARTIFACT_LIFECYCLE_CONTRACT_VERSION,
        "supported_lifecycle_states": list(
            SUPPORTED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES
        ),
        "prohibited_lifecycle_states": list(
            PROHIBITED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES
        ),
        "transition_rules": {
            state: list(next_states)
            for state, next_states in DOCUMENT_ARTIFACT_TRANSITION_RULES.items()
        },
        "training_delivery_policy": (
            "training_delivery_is_optional_and_required_only_when_training_required_is_true"
        ),
        "post_active_change_policy": POST_ACTIVE_CHANGE_POLICY,
        "retention_basis": RETENTION_BASIS_ACTIVE_LIFETIME_PLUS_POLICY,
        "lifecycle_truth_boundary": DOCUMENT_LIFECYCLE_TRUTH_BOUNDARY,
        "m12_7_boundary": (
            "task_and_workflow_state_effects_are_explicitly_deferred_to_M12_7"
        ),
    }


def build_document_artifact_lifecycle_payload(
    *,
    artifact_id: str,
    document_family: str,
    document_id: str,
    artifact_version: str,
    template_identity: dict[str, object],
    document_request_ref: dict[str, object],
    training_required: bool = False,
    lifecycle_state: str = DRAFT_LIFECYCLE_STATE,
    effective_date: str | None = None,
    expiry_due_date: str | None = None,
    previous_version_ref: str | None = None,
    supersedes_ref: str | None = None,
    superseded_by_ref: str | None = None,
    event_ref: str | None = None,
    retention_metadata: dict[str, object] | None = None,
) -> dict[str, Any]:
    """Build a governed document artifact lifecycle payload."""

    _validate_lifecycle_state(lifecycle_state)
    _validate_non_empty_string(artifact_id, "artifact_id")
    _validate_non_empty_string(document_family, "document_family")
    _validate_non_empty_string(document_id, "document_id")
    _validate_non_empty_string(artifact_version, "artifact_version")
    validate_template_identity(template_identity, allow_supporting_artifacts=False)
    _validate_document_request_ref(document_request_ref)

    payload: dict[str, Any] = {
        "checkpoint": DOCUMENT_ARTIFACT_LIFECYCLE_CHECKPOINT_ID,
        "contract_version": DOCUMENT_ARTIFACT_LIFECYCLE_CONTRACT_VERSION,
        "artifact_id": artifact_id,
        "document_family": document_family,
        "document_id": document_id,
        "artifact_version": artifact_version,
        "template_identity": template_identity,
        "document_request_ref": document_request_ref,
        "lifecycle_state": lifecycle_state,
        "lifecycle_history": [
            _build_lifecycle_history_event(
                from_state=None,
                to_state=lifecycle_state,
                event_ref=event_ref or f"{artifact_id}:created",
                transition_reason="artifact_lifecycle_created",
            )
        ],
        "training_required": training_required,
        "effective_date": effective_date,
        "expiry_due_date": expiry_due_date,
        "previous_version_ref": previous_version_ref,
        "supersedes_ref": supersedes_ref,
        "superseded_by_ref": superseded_by_ref,
        "event_ref": event_ref,
        "retention_metadata": retention_metadata,
        "lifecycle_truth_boundary": DOCUMENT_LIFECYCLE_TRUTH_BOUNDARY,
        "post_active_change_policy": POST_ACTIVE_CHANGE_POLICY,
    }
    validate_document_artifact_lifecycle_payload(payload)
    return payload


def build_document_artifact_retention_metadata(
    *,
    retention_period_source: str,
    retention_trigger: str,
    dependency_refs: list[str] | tuple[str, ...] | None = None,
    retention_period_years: int | None = None,
) -> dict[str, Any]:
    """Build policy-driven retention metadata for archive transition."""

    _validate_non_empty_string(retention_period_source, "retention_period_source")
    _validate_non_empty_string(retention_trigger, "retention_trigger")
    dependencies = list(dependency_refs or [])
    _validate_string_list(dependencies, "dependency_refs")

    if retention_period_years is not None and retention_period_years < 0:
        raise ValueError("retention_period_years must not be negative.")

    metadata: dict[str, Any] = {
        "retention_basis": RETENTION_BASIS_ACTIVE_LIFETIME_PLUS_POLICY,
        "retention_period_source": retention_period_source,
        "retention_period_years": retention_period_years,
        "retention_trigger": retention_trigger,
        "dependency_refs": dependencies,
    }
    validate_document_artifact_retention_metadata(metadata)
    return metadata


def transition_document_artifact_lifecycle(
    payload: dict[str, object],
    *,
    to_state: str,
    event_ref: str,
    transition_reason: str,
    effective_date: str | None = None,
    expiry_due_date: str | None = None,
    superseded_by_ref: str | None = None,
    retention_metadata: dict[str, object] | None = None,
) -> dict[str, Any]:
    """Return a new payload with one deterministic lifecycle transition applied."""

    validate_document_artifact_lifecycle_payload(payload)
    _validate_lifecycle_state(to_state)
    _validate_non_empty_string(event_ref, "event_ref")
    _validate_non_empty_string(transition_reason, "transition_reason")

    current_state = str(payload["lifecycle_state"])
    _validate_transition(current_state, to_state)

    next_payload = deepcopy(payload)
    next_payload["lifecycle_state"] = to_state
    next_payload["event_ref"] = event_ref

    if effective_date is not None:
        _validate_non_empty_string(effective_date, "effective_date")
        next_payload["effective_date"] = effective_date

    if expiry_due_date is not None:
        _validate_non_empty_string(expiry_due_date, "expiry_due_date")
        next_payload["expiry_due_date"] = expiry_due_date

    if superseded_by_ref is not None:
        _validate_non_empty_string(superseded_by_ref, "superseded_by_ref")
        next_payload["superseded_by_ref"] = superseded_by_ref

    if retention_metadata is not None:
        validate_document_artifact_retention_metadata(retention_metadata)
        next_payload["retention_metadata"] = retention_metadata

    _validate_transition_side_conditions(
        next_payload,
        from_state=current_state,
        to_state=to_state,
    )

    history = next_payload["lifecycle_history"]
    if not isinstance(history, list):
        raise ValueError("lifecycle_history must be a list.")
    history.append(
        _build_lifecycle_history_event(
            from_state=current_state,
            to_state=to_state,
            event_ref=event_ref,
            transition_reason=transition_reason,
        )
    )

    validate_document_artifact_lifecycle_payload(next_payload)
    return next_payload


def validate_document_artifact_lifecycle_payload(payload: dict[str, object]) -> None:
    """Validate a governed document artifact lifecycle payload."""

    _validate_required_fields(payload, _REQUIRED_ARTIFACT_FIELDS, "Document artifact lifecycle payload")
    _validate_no_prohibited_artifact_fields(payload)
    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=DOCUMENT_ARTIFACT_LIFECYCLE_CHECKPOINT_ID,
        error_prefix="Document artifact lifecycle payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=DOCUMENT_ARTIFACT_LIFECYCLE_CONTRACT_VERSION,
        error_prefix="Document artifact lifecycle payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="lifecycle_truth_boundary",
        expected_value=DOCUMENT_LIFECYCLE_TRUTH_BOUNDARY,
        error_prefix="Document artifact lifecycle payload",
    )
    _validate_expected_exact_value(
        payload,
        field_name="post_active_change_policy",
        expected_value=POST_ACTIVE_CHANGE_POLICY,
        error_prefix="Document artifact lifecycle payload",
    )

    for field_name in ("artifact_id", "document_family", "document_id", "artifact_version"):
        value = payload[field_name]
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string.")
        _validate_non_empty_string(value, field_name)

    template_identity = payload["template_identity"]
    if not isinstance(template_identity, dict):
        raise ValueError("template_identity must be a mapping.")
    validate_template_identity(template_identity, allow_supporting_artifacts=False)

    document_request_ref = payload["document_request_ref"]
    if not isinstance(document_request_ref, dict):
        raise ValueError("document_request_ref must be a mapping.")
    _validate_document_request_ref(document_request_ref)

    lifecycle_state = payload["lifecycle_state"]
    if not isinstance(lifecycle_state, str):
        raise ValueError("lifecycle_state must be a string.")
    _validate_lifecycle_state(lifecycle_state)

    training_required = payload["training_required"]
    if not isinstance(training_required, bool):
        raise ValueError("training_required must be a boolean.")

    lifecycle_history = payload["lifecycle_history"]
    if not isinstance(lifecycle_history, list) or not lifecycle_history:
        raise ValueError("lifecycle_history must be a non-empty list.")
    _validate_lifecycle_history(lifecycle_history, lifecycle_state)

    _validate_optional_string_field(payload, "effective_date")
    _validate_optional_string_field(payload, "expiry_due_date")
    _validate_optional_string_field(payload, "previous_version_ref")
    _validate_optional_string_field(payload, "supersedes_ref")
    _validate_optional_string_field(payload, "superseded_by_ref")
    _validate_optional_string_field(payload, "event_ref")

    retention_metadata = payload["retention_metadata"]
    if retention_metadata is not None:
        if not isinstance(retention_metadata, dict):
            raise ValueError("retention_metadata must be a mapping when present.")
        validate_document_artifact_retention_metadata(retention_metadata)

    _validate_state_required_metadata(payload)


def validate_document_artifact_retention_metadata(metadata: dict[str, object]) -> None:
    """Validate document artifact retention metadata."""

    _validate_required_fields(metadata, _REQUIRED_RETENTION_METADATA_FIELDS, "Document artifact retention metadata")
    _validate_expected_exact_value(
        metadata,
        field_name="retention_basis",
        expected_value=RETENTION_BASIS_ACTIVE_LIFETIME_PLUS_POLICY,
        error_prefix="Document artifact retention metadata",
    )

    retention_period_source = metadata["retention_period_source"]
    if not isinstance(retention_period_source, str):
        raise ValueError("retention_period_source must be a string.")
    _validate_non_empty_string(retention_period_source, "retention_period_source")

    retention_trigger = metadata["retention_trigger"]
    if not isinstance(retention_trigger, str):
        raise ValueError("retention_trigger must be a string.")
    _validate_non_empty_string(retention_trigger, "retention_trigger")

    dependency_refs = metadata["dependency_refs"]
    _validate_string_list(dependency_refs, "dependency_refs")

    retention_period_years = metadata.get("retention_period_years")
    if retention_period_years is not None:
        if not isinstance(retention_period_years, int):
            raise ValueError("retention_period_years must be an integer when present.")
        if retention_period_years < 0:
            raise ValueError("retention_period_years must not be negative.")


def _validate_transition_side_conditions(payload: dict[str, object], *, from_state: str, to_state: str) -> None:
    training_required = payload["training_required"]
    assert isinstance(training_required, bool)

    if from_state == IN_APPROVAL_LIFECYCLE_STATE and to_state == TRAINING_DELIVERY_LIFECYCLE_STATE:
        if not training_required:
            raise ValueError("training_delivery is allowed only when training_required is true.")

    if from_state == IN_APPROVAL_LIFECYCLE_STATE and to_state == ACTIVE_LIFECYCLE_STATE:
        if training_required:
            raise ValueError("training_required documents must pass through training_delivery before active.")

    if to_state == ACTIVE_LIFECYCLE_STATE:
        effective_date = payload["effective_date"]
        expiry_due_date = payload["expiry_due_date"]
        if not isinstance(effective_date, str) or not effective_date.strip():
            raise ValueError("active lifecycle transition requires effective_date.")
        if not isinstance(expiry_due_date, str) or not expiry_due_date.strip():
            raise ValueError("active lifecycle transition requires expiry_due_date.")

    if from_state == ACTIVE_LIFECYCLE_STATE and to_state == SUPERSEDED_LIFECYCLE_STATE:
        superseded_by_ref = payload["superseded_by_ref"]
        if not isinstance(superseded_by_ref, str) or not superseded_by_ref.strip():
            raise ValueError("active -> superseded requires superseded_by_ref for the new version.")

    if to_state == ARCHIVED_LIFECYCLE_STATE:
        retention_metadata = payload["retention_metadata"]
        if not isinstance(retention_metadata, dict):
            raise ValueError("archive transition requires retention_metadata based on active lifetime plus policy.")
        validate_document_artifact_retention_metadata(retention_metadata)


def _validate_state_required_metadata(payload: dict[str, object]) -> None:
    lifecycle_state = payload["lifecycle_state"]

    if lifecycle_state == ACTIVE_LIFECYCLE_STATE:
        effective_date = payload["effective_date"]
        expiry_due_date = payload["expiry_due_date"]
        if not isinstance(effective_date, str) or not effective_date.strip():
            raise ValueError("active lifecycle state requires effective_date.")
        if not isinstance(expiry_due_date, str) or not expiry_due_date.strip():
            raise ValueError("active lifecycle state requires expiry_due_date.")

    if lifecycle_state == SUPERSEDED_LIFECYCLE_STATE:
        superseded_by_ref = payload["superseded_by_ref"]
        if not isinstance(superseded_by_ref, str) or not superseded_by_ref.strip():
            raise ValueError("superseded lifecycle state requires superseded_by_ref.")

    if lifecycle_state == ARCHIVED_LIFECYCLE_STATE:
        retention_metadata = payload["retention_metadata"]
        if not isinstance(retention_metadata, dict):
            raise ValueError("archived lifecycle state requires retention_metadata.")
        validate_document_artifact_retention_metadata(retention_metadata)


def _validate_transition(from_state: str, to_state: str) -> None:
    allowed_next_states = DOCUMENT_ARTIFACT_TRANSITION_RULES[from_state]
    if to_state not in allowed_next_states:
        raise ValueError(f"Invalid document artifact lifecycle transition: {from_state} -> {to_state}.")


def _validate_lifecycle_state(lifecycle_state: str) -> None:
    if lifecycle_state in PROHIBITED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES:
        raise ValueError(f"{lifecycle_state!r} is not a controlled GMP/CQV lifecycle state.")
    if lifecycle_state not in SUPPORTED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES:
        raise ValueError(
            "Unsupported lifecycle_state. Expected one of: "
            f"{', '.join(SUPPORTED_DOCUMENT_ARTIFACT_LIFECYCLE_STATES)}."
        )


def _validate_lifecycle_history(lifecycle_history: list[object], current_state: str) -> None:
    previous_to_state: str | None = None

    for index, event in enumerate(lifecycle_history):
        if not isinstance(event, dict):
            raise ValueError("Each lifecycle_history event must be a mapping.")
        _validate_required_fields(event, _REQUIRED_HISTORY_EVENT_FIELDS, "Lifecycle history event")

        from_state = event["from_state"]
        to_state = event["to_state"]

        if from_state is not None:
            if not isinstance(from_state, str):
                raise ValueError("Lifecycle history from_state must be a string or None.")
            _validate_lifecycle_state(from_state)

        if not isinstance(to_state, str):
            raise ValueError("Lifecycle history to_state must be a string.")
        _validate_lifecycle_state(to_state)

        event_ref = event["event_ref"]
        transition_reason = event["transition_reason"]
        if not isinstance(event_ref, str):
            raise ValueError("Lifecycle history event_ref must be a string.")
        if not isinstance(transition_reason, str):
            raise ValueError("Lifecycle history transition_reason must be a string.")
        _validate_non_empty_string(event_ref, "event_ref")
        _validate_non_empty_string(transition_reason, "transition_reason")

        if index == 0:
            if from_state is not None:
                raise ValueError("First lifecycle history event must start from None.")
        else:
            if from_state != previous_to_state:
                raise ValueError("Lifecycle history must be sequential and append-only.")
            assert isinstance(from_state, str)
            _validate_transition(from_state, to_state)

        previous_to_state = to_state

    if previous_to_state != current_state:
        raise ValueError("Final lifecycle_history event must match lifecycle_state.")


def _build_lifecycle_history_event(*, from_state: str | None, to_state: str, event_ref: str, transition_reason: str) -> dict[str, str | None]:
    return {
        "from_state": from_state,
        "to_state": to_state,
        "event_ref": event_ref,
        "transition_reason": transition_reason,
    }


def _validate_document_request_ref(document_request_ref: dict[str, object]) -> None:
    _validate_required_fields(document_request_ref, _REQUIRED_DOCUMENT_REQUEST_REF_FIELDS, "document_request_ref")
    for field_name in _REQUIRED_DOCUMENT_REQUEST_REF_FIELDS:
        value = document_request_ref[field_name]
        if not isinstance(value, str):
            raise ValueError(f"document_request_ref.{field_name} must be a string.")
        _validate_non_empty_string(value, f"document_request_ref.{field_name}")


def _validate_no_prohibited_artifact_fields(payload: dict[str, object]) -> None:
    for field_name in _PROHIBITED_ARTIFACT_FIELDS:
        if field_name in payload:
            raise ValueError(f"{field_name} is not allowed in document artifact lifecycle payload.")


def _validate_required_fields(payload: dict[str, object], required_fields: tuple[str, ...], error_prefix: str) -> None:
    for field_name in required_fields:
        if field_name not in payload:
            raise ValueError(f"{error_prefix} must declare {field_name}.")


def _validate_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _validate_optional_string_field(payload: dict[str, object], field_name: str) -> None:
    value = payload[field_name]
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ValueError(f"{field_name} must be a non-empty string when present.")


def _validate_string_list(value: object, field_name: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list of strings.")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name} must contain only non-empty strings.")


def _validate_expected_exact_value(payload: dict[str, object], *, field_name: str, expected_value: str, error_prefix: str) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: expected {expected_value!r}, got {actual_value!r}."
        )
