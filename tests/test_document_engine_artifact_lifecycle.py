import pytest

from asbp.document_engine import (
    ACTIVE_LIFECYCLE_STATE,
    ARCHIVED_LIFECYCLE_STATE,
    DOCUMENT_ARTIFACT_LIFECYCLE_CHECKPOINT_ID,
    DOCUMENT_ARTIFACT_LIFECYCLE_CONTRACT_VERSION,
    DOCUMENT_LIFECYCLE_TRUTH_BOUNDARY,
    DRAFT_LIFECYCLE_STATE,
    EXPIRED_LIFECYCLE_STATE,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    IN_APPROVAL_LIFECYCLE_STATE,
    IN_REVIEW_LIFECYCLE_STATE,
    POST_ACTIVE_CHANGE_POLICY,
    RETENTION_BASIS_ACTIVE_LIFETIME_PLUS_POLICY,
    SUPERSEDED_LIFECYCLE_STATE,
    TRAINING_DELIVERY_LIFECYCLE_STATE,
    build_document_artifact_lifecycle_baseline,
    build_document_artifact_lifecycle_payload,
    build_document_artifact_retention_metadata,
    transition_document_artifact_lifecycle,
    validate_document_artifact_lifecycle_payload,
)


def _template_identity() -> dict[str, object]:
    return {
        "template_family": "urs",
        "template_id": "URS_BASE_v1",
        "template_version": "1.0.0",
        "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
    }


def _document_request_ref() -> dict[str, object]:
    return {
        "document_job_id": "DOCJOB-001",
        "document_id": "URS-001",
        "document_request_contract_version": "document-request-contract-v1",
    }


def _draft_artifact(*, training_required: bool = False) -> dict[str, object]:
    return build_document_artifact_lifecycle_payload(
        artifact_id="ART-URS-001-v1",
        document_family="urs",
        document_id="URS-001",
        artifact_version="1.0.0",
        template_identity=_template_identity(),
        document_request_ref=_document_request_ref(),
        training_required=training_required,
    )


def _move_to_in_approval(artifact: dict[str, object]) -> dict[str, object]:
    in_review = transition_document_artifact_lifecycle(
        artifact,
        to_state=IN_REVIEW_LIFECYCLE_STATE,
        event_ref="review-started",
        transition_reason="technical_review_started",
    )
    return transition_document_artifact_lifecycle(
        in_review,
        to_state=IN_APPROVAL_LIFECYCLE_STATE,
        event_ref="approval-started",
        transition_reason="formal_approval_started",
    )


def _active_artifact(*, training_required: bool = False) -> dict[str, object]:
    in_approval = _move_to_in_approval(_draft_artifact(training_required=training_required))

    if training_required:
        training = transition_document_artifact_lifecycle(
            in_approval,
            to_state=TRAINING_DELIVERY_LIFECYCLE_STATE,
            event_ref="training-started",
            transition_reason="training_delivery_required_before_effective_use",
        )
        return transition_document_artifact_lifecycle(
            training,
            to_state=ACTIVE_LIFECYCLE_STATE,
            event_ref="effective-release",
            transition_reason="training_delivery_completed_and_document_effective",
            effective_date="2026-04-27",
            expiry_due_date="2028-04-27",
        )

    return transition_document_artifact_lifecycle(
        in_approval,
        to_state=ACTIVE_LIFECYCLE_STATE,
        event_ref="effective-release",
        transition_reason="approval_completed_and_document_effective",
        effective_date="2026-04-27",
        expiry_due_date="2028-04-27",
    )


def _retention_metadata() -> dict[str, object]:
    return build_document_artifact_retention_metadata(
        retention_period_source="document_type_content_dependencies_policy",
        retention_trigger="superseded_or_expired_date",
        dependency_refs=["URS-001", "WP-001"],
        retention_period_years=7,
    )


def test_lifecycle_baseline_uses_gmp_cqv_states_without_reopened_approved_or_finalized() -> None:
    baseline = build_document_artifact_lifecycle_baseline()

    assert baseline["checkpoint"] == DOCUMENT_ARTIFACT_LIFECYCLE_CHECKPOINT_ID
    assert baseline["contract_version"] == DOCUMENT_ARTIFACT_LIFECYCLE_CONTRACT_VERSION
    assert baseline["lifecycle_truth_boundary"] == DOCUMENT_LIFECYCLE_TRUTH_BOUNDARY
    assert baseline["post_active_change_policy"] == POST_ACTIVE_CHANGE_POLICY

    states = baseline["supported_lifecycle_states"]
    assert states == [
        DRAFT_LIFECYCLE_STATE,
        IN_REVIEW_LIFECYCLE_STATE,
        IN_APPROVAL_LIFECYCLE_STATE,
        TRAINING_DELIVERY_LIFECYCLE_STATE,
        ACTIVE_LIFECYCLE_STATE,
        SUPERSEDED_LIFECYCLE_STATE,
        EXPIRED_LIFECYCLE_STATE,
        ARCHIVED_LIFECYCLE_STATE,
    ]
    assert "reopened" not in states
    assert "approved" not in states
    assert "finalized" not in states


def test_build_document_artifact_lifecycle_payload_starts_as_draft() -> None:
    payload = _draft_artifact()

    assert payload["checkpoint"] == DOCUMENT_ARTIFACT_LIFECYCLE_CHECKPOINT_ID
    assert payload["lifecycle_state"] == DRAFT_LIFECYCLE_STATE
    assert payload["lifecycle_history"][-1]["to_state"] == DRAFT_LIFECYCLE_STATE


def test_draft_to_review_to_approval_transition_sequence_is_valid() -> None:
    draft = _draft_artifact()
    in_review = transition_document_artifact_lifecycle(
        draft,
        to_state=IN_REVIEW_LIFECYCLE_STATE,
        event_ref="review-started",
        transition_reason="technical_review_started",
    )
    in_approval = transition_document_artifact_lifecycle(
        in_review,
        to_state=IN_APPROVAL_LIFECYCLE_STATE,
        event_ref="approval-started",
        transition_reason="formal_approval_started",
    )

    assert draft["lifecycle_state"] == DRAFT_LIFECYCLE_STATE
    assert in_review["lifecycle_state"] == IN_REVIEW_LIFECYCLE_STATE
    assert in_approval["lifecycle_state"] == IN_APPROVAL_LIFECYCLE_STATE
    assert len(draft["lifecycle_history"]) == 1
    assert len(in_approval["lifecycle_history"]) == 3


def test_in_review_does_not_transition_back_to_draft() -> None:
    draft = _draft_artifact()
    in_review = transition_document_artifact_lifecycle(
        draft,
        to_state=IN_REVIEW_LIFECYCLE_STATE,
        event_ref="review-started",
        transition_reason="technical_review_started",
    )

    with pytest.raises(ValueError, match="Invalid document artifact lifecycle transition"):
        transition_document_artifact_lifecycle(
            in_review,
            to_state=DRAFT_LIFECYCLE_STATE,
            event_ref="review-return",
            transition_reason="review_returned_to_draft",
        )


def test_training_required_document_must_pass_through_training_delivery_before_active() -> None:
    in_approval = _move_to_in_approval(_draft_artifact(training_required=True))

    with pytest.raises(ValueError, match="must pass through training_delivery"):
        transition_document_artifact_lifecycle(
            in_approval,
            to_state=ACTIVE_LIFECYCLE_STATE,
            event_ref="effective-release",
            transition_reason="approval_completed",
            effective_date="2026-04-27",
            expiry_due_date="2028-04-27",
        )

    training = transition_document_artifact_lifecycle(
        in_approval,
        to_state=TRAINING_DELIVERY_LIFECYCLE_STATE,
        event_ref="training-started",
        transition_reason="training_delivery_required_before_effective_use",
    )
    active = transition_document_artifact_lifecycle(
        training,
        to_state=ACTIVE_LIFECYCLE_STATE,
        event_ref="effective-release",
        transition_reason="training_delivery_completed_and_document_effective",
        effective_date="2026-04-27",
        expiry_due_date="2028-04-27",
    )

    assert active["lifecycle_state"] == ACTIVE_LIFECYCLE_STATE


def test_non_training_document_moves_from_approval_to_active_with_effective_and_due_dates() -> None:
    active = _active_artifact(training_required=False)

    assert active["lifecycle_state"] == ACTIVE_LIFECYCLE_STATE
    assert active["effective_date"] == "2026-04-27"
    assert active["expiry_due_date"] == "2028-04-27"


def test_active_document_cannot_return_to_draft_review_or_approval() -> None:
    active = _active_artifact()

    for blocked_state in (
        DRAFT_LIFECYCLE_STATE,
        IN_REVIEW_LIFECYCLE_STATE,
        IN_APPROVAL_LIFECYCLE_STATE,
    ):
        with pytest.raises(ValueError, match="Invalid document artifact lifecycle transition"):
            transition_document_artifact_lifecycle(
                active,
                to_state=blocked_state,
                event_ref=f"blocked-{blocked_state}",
                transition_reason="blocked_backward_transition",
            )


def test_active_to_superseded_requires_new_version_reference() -> None:
    active = _active_artifact()

    with pytest.raises(ValueError, match="requires superseded_by_ref"):
        transition_document_artifact_lifecycle(
            active,
            to_state=SUPERSEDED_LIFECYCLE_STATE,
            event_ref="periodic-review-update",
            transition_reason="planned_periodic_update_requires_new_version",
        )

    superseded = transition_document_artifact_lifecycle(
        active,
        to_state=SUPERSEDED_LIFECYCLE_STATE,
        event_ref="periodic-review-update",
        transition_reason="planned_periodic_update_requires_new_version",
        superseded_by_ref="ART-URS-001-v2",
    )

    assert superseded["lifecycle_state"] == SUPERSEDED_LIFECYCLE_STATE
    assert superseded["superseded_by_ref"] == "ART-URS-001-v2"


def test_active_to_expired_then_archive_models_missed_due_date_path() -> None:
    active = _active_artifact()
    expired = transition_document_artifact_lifecycle(
        active,
        to_state=EXPIRED_LIFECYCLE_STATE,
        event_ref="expiry-due-date-missed",
        transition_reason="document_due_date_passed_without_update",
    )

    assert expired["lifecycle_state"] == EXPIRED_LIFECYCLE_STATE

    archived = transition_document_artifact_lifecycle(
        expired,
        to_state=ARCHIVED_LIFECYCLE_STATE,
        event_ref="expired-record-archived",
        transition_reason="expired_document_record_archived_under_retention",
        retention_metadata=_retention_metadata(),
    )

    assert archived["lifecycle_state"] == ARCHIVED_LIFECYCLE_STATE
    assert archived["retention_metadata"]["retention_basis"] == RETENTION_BASIS_ACTIVE_LIFETIME_PLUS_POLICY


def test_superseded_to_archived_requires_retention_metadata() -> None:
    active = _active_artifact()
    superseded = transition_document_artifact_lifecycle(
        active,
        to_state=SUPERSEDED_LIFECYCLE_STATE,
        event_ref="event-driven-update",
        transition_reason="event_outcome_requires_new_document_version",
        superseded_by_ref="ART-URS-001-v2",
    )

    with pytest.raises(ValueError, match="archive transition requires retention_metadata"):
        transition_document_artifact_lifecycle(
            superseded,
            to_state=ARCHIVED_LIFECYCLE_STATE,
            event_ref="archive-started",
            transition_reason="archive_superseded_record",
        )

    archived = transition_document_artifact_lifecycle(
        superseded,
        to_state=ARCHIVED_LIFECYCLE_STATE,
        event_ref="archive-started",
        transition_reason="archive_superseded_record",
        retention_metadata=_retention_metadata(),
    )

    assert archived["lifecycle_state"] == ARCHIVED_LIFECYCLE_STATE


def test_archived_state_is_terminal() -> None:
    active = _active_artifact()
    expired = transition_document_artifact_lifecycle(
        active,
        to_state=EXPIRED_LIFECYCLE_STATE,
        event_ref="expiry-due-date-missed",
        transition_reason="document_due_date_passed_without_update",
    )
    archived = transition_document_artifact_lifecycle(
        expired,
        to_state=ARCHIVED_LIFECYCLE_STATE,
        event_ref="archive-expired-record",
        transition_reason="archive_expired_record",
        retention_metadata=_retention_metadata(),
    )

    with pytest.raises(ValueError, match="Invalid document artifact lifecycle transition"):
        transition_document_artifact_lifecycle(
            archived,
            to_state=ACTIVE_LIFECYCLE_STATE,
            event_ref="reactivate",
            transition_reason="blocked_reactivation",
        )


def test_generated_language_cannot_override_lifecycle_truth() -> None:
    payload = _draft_artifact()
    payload["generated_language_output"] = "The AI declares this document active."

    with pytest.raises(ValueError, match="generated_language_output is not allowed"):
        validate_document_artifact_lifecycle_payload(payload)


def test_reopened_approved_and_finalized_states_are_rejected() -> None:
    for prohibited_state in ("reopened", "approved", "finalized"):
        with pytest.raises(ValueError, match="not a controlled GMP/CQV lifecycle state"):
            build_document_artifact_lifecycle_payload(
                artifact_id=f"ART-{prohibited_state}",
                document_family="urs",
                document_id="URS-001",
                artifact_version="1.0.0",
                template_identity=_template_identity(),
                document_request_ref=_document_request_ref(),
                lifecycle_state=prohibited_state,
            )
