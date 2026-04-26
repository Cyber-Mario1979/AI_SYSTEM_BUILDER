from copy import deepcopy

import pytest

from asbp.document_engine import (
    ACTIVE_LIFECYCLE_STATE,
    ALLOW_COMPLETION_EFFECT,
    ARCHIVED_LIFECYCLE_STATE,
    BLOCK_COMPLETION_EFFECT,
    DOCUMENT_WORKFLOW_INTEGRATION_CHECKPOINT_ID,
    DOCUMENT_WORKFLOW_INTEGRATION_CONTRACT_VERSION,
    DRAFT_LIFECYCLE_STATE,
    EXPIRED_LIFECYCLE_STATE,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    HISTORICAL_RECORD_ONLY_EFFECT,
    HISTORICAL_RECORD_ONLY_SIGNAL,
    IN_APPROVAL_LIFECYCLE_STATE,
    IN_REVIEW_LIFECYCLE_STATE,
    READINESS_EVALUATION_ONLY_BOUNDARY,
    REPLACEMENT_DOCUMENT_REQUIRED_SIGNAL,
    REQUIRES_REPLACEMENT_DOCUMENT_EFFECT,
    SUPERSEDED_LIFECYCLE_STATE,
    TASK_CLOSURE_BLOCKED_SIGNAL,
    TASK_CLOSURE_READY_SIGNAL,
    TRAINING_DELIVERY_LIFECYCLE_STATE,
    build_document_artifact_lifecycle_payload,
    build_document_artifact_retention_metadata,
    build_document_workflow_integration_baseline,
    build_task_document_obligation,
    evaluate_task_document_workflow_readiness,
    transition_document_artifact_lifecycle,
    validate_task_document_workflow_readiness_payload,
)


def _task_payload(task_id: str = "T-045") -> dict[str, object]:
    return {
        "task_id": task_id,
        "status": "in_progress",
        "title": "Complete OQ execution package for Tablet Press",
    }


def _template_identity(document_family: str = "protocol") -> dict[str, object]:
    return {
        "template_family": document_family,
        "template_id": f"{document_family.upper()}_BASE_v1",
        "template_version": "1.0.0",
        "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
    }


def _document_request_ref(document_family: str = "protocol") -> dict[str, object]:
    return {
        "document_job_id": f"DOCJOB-{document_family.upper()}-001",
        "document_id": f"{document_family.upper()}-001",
        "document_request_contract_version": "document-request-contract-v1",
    }


def _artifact(
    *,
    artifact_id: str = "OQ_PROTOCOL_TP_001",
    document_family: str = "protocol",
    lifecycle_state: str = ACTIVE_LIFECYCLE_STATE,
    training_required: bool = False,
) -> dict[str, object]:
    artifact = build_document_artifact_lifecycle_payload(
        artifact_id=artifact_id,
        document_family=document_family,
        document_id=f"{document_family.upper()}-001",
        artifact_version="1.0.0",
        template_identity=_template_identity(document_family),
        document_request_ref=_document_request_ref(document_family),
        training_required=training_required,
    )

    if lifecycle_state == DRAFT_LIFECYCLE_STATE:
        return artifact

    artifact = transition_document_artifact_lifecycle(
        artifact,
        to_state=IN_REVIEW_LIFECYCLE_STATE,
        event_ref=f"{artifact_id}:review",
        transition_reason="submit_for_review",
    )

    if lifecycle_state == IN_REVIEW_LIFECYCLE_STATE:
        return artifact

    artifact = transition_document_artifact_lifecycle(
        artifact,
        to_state=IN_APPROVAL_LIFECYCLE_STATE,
        event_ref=f"{artifact_id}:approval",
        transition_reason="submit_for_approval",
    )

    if lifecycle_state == IN_APPROVAL_LIFECYCLE_STATE:
        return artifact

    if training_required:
        artifact = transition_document_artifact_lifecycle(
            artifact,
            to_state=TRAINING_DELIVERY_LIFECYCLE_STATE,
            event_ref=f"{artifact_id}:training",
            transition_reason="training_required_before_effective_use",
        )

        if lifecycle_state == TRAINING_DELIVERY_LIFECYCLE_STATE:
            return artifact

    artifact = transition_document_artifact_lifecycle(
        artifact,
        to_state=ACTIVE_LIFECYCLE_STATE,
        event_ref=f"{artifact_id}:active",
        transition_reason="activate_document",
        effective_date="2026-04-27",
        expiry_due_date="2027-04-27",
    )

    if lifecycle_state == ACTIVE_LIFECYCLE_STATE:
        return artifact

    if lifecycle_state == SUPERSEDED_LIFECYCLE_STATE:
        return transition_document_artifact_lifecycle(
            artifact,
            to_state=SUPERSEDED_LIFECYCLE_STATE,
            event_ref=f"{artifact_id}:superseded",
            transition_reason="new_version_issued",
            superseded_by_ref=f"{artifact_id}_v2",
        )

    if lifecycle_state == EXPIRED_LIFECYCLE_STATE:
        return transition_document_artifact_lifecycle(
            artifact,
            to_state=EXPIRED_LIFECYCLE_STATE,
            event_ref=f"{artifact_id}:expired",
            transition_reason="not_updated_before_due_date",
        )

    if lifecycle_state == ARCHIVED_LIFECYCLE_STATE:
        superseded = transition_document_artifact_lifecycle(
            artifact,
            to_state=SUPERSEDED_LIFECYCLE_STATE,
            event_ref=f"{artifact_id}:superseded",
            transition_reason="new_version_issued",
            superseded_by_ref=f"{artifact_id}_v2",
        )
        retention_metadata = build_document_artifact_retention_metadata(
            retention_period_source="document_type_content_dependency_policy",
            retention_period_years=5,
            retention_trigger=f"{artifact_id}:superseded",
            dependency_refs=["WP-001"],
        )
        return transition_document_artifact_lifecycle(
            superseded,
            to_state=ARCHIVED_LIFECYCLE_STATE,
            event_ref=f"{artifact_id}:archived",
            transition_reason="archive_under_retention_policy",
            retention_metadata=retention_metadata,
        )

    raise AssertionError(f"Unsupported helper lifecycle_state: {lifecycle_state}")


def _obligation(
    *,
    artifact_id: str = "OQ_PROTOCOL_TP_001",
    document_family: str = "protocol",
) -> dict[str, object]:
    return build_task_document_obligation(
        obligation_id=f"OBL-{artifact_id}",
        task_id="T-045",
        required_document_family=document_family,
        required_artifact_id=artifact_id,
        required_lifecycle_state=ACTIVE_LIFECYCLE_STATE,
        obligation_scope="task_closure",
        closure_required=True,
    )


def test_build_document_workflow_integration_baseline_exposes_m12_7_boundary() -> None:
    baseline = build_document_workflow_integration_baseline()

    assert baseline["checkpoint"] == DOCUMENT_WORKFLOW_INTEGRATION_CHECKPOINT_ID
    assert baseline["contract_version"] == DOCUMENT_WORKFLOW_INTEGRATION_CONTRACT_VERSION
    assert baseline["mutation_boundary"] == READINESS_EVALUATION_ONLY_BOUNDARY
    assert baseline["default_required_lifecycle_state"] == ACTIVE_LIFECYCLE_STATE


def test_task_with_no_required_document_is_closure_ready() -> None:
    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=[],
        document_artifacts=[],
    )

    assert readiness["task_closure_ready"] is True
    assert readiness["recommended_task_state_effect"] == ALLOW_COMPLETION_EFFECT
    assert readiness["workflow_readiness_signal"] == TASK_CLOSURE_READY_SIGNAL


@pytest.mark.parametrize(
    "lifecycle_state",
    [
        DRAFT_LIFECYCLE_STATE,
        IN_REVIEW_LIFECYCLE_STATE,
        IN_APPROVAL_LIFECYCLE_STATE,
    ],
)
def test_task_requiring_active_document_is_blocked_before_activation(
    lifecycle_state: str,
) -> None:
    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=[_obligation()],
        document_artifacts=[_artifact(lifecycle_state=lifecycle_state)],
    )

    assert readiness["task_closure_ready"] is False
    assert readiness["recommended_task_state_effect"] == BLOCK_COMPLETION_EFFECT
    assert readiness["workflow_readiness_signal"] == TASK_CLOSURE_BLOCKED_SIGNAL
    assert readiness["blocked_obligations"][0]["actual_lifecycle_state"] == lifecycle_state


def test_task_requiring_active_document_is_blocked_during_training_delivery_by_default() -> None:
    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=[_obligation()],
        document_artifacts=[
            _artifact(
                lifecycle_state=TRAINING_DELIVERY_LIFECYCLE_STATE,
                training_required=True,
            )
        ],
    )

    assert readiness["task_closure_ready"] is False
    assert readiness["recommended_task_state_effect"] == BLOCK_COMPLETION_EFFECT
    assert readiness["blocked_obligations"][0]["reason"] == (
        "training_delivery_blocks_closure_without_explicit_interim_allowance"
    )


def test_task_requiring_active_document_is_closure_ready_when_document_is_active() -> None:
    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=[_obligation()],
        document_artifacts=[_artifact(lifecycle_state=ACTIVE_LIFECYCLE_STATE)],
    )

    assert readiness["task_closure_ready"] is True
    assert readiness["recommended_task_state_effect"] == ALLOW_COMPLETION_EFFECT
    assert readiness["workflow_readiness_signal"] == TASK_CLOSURE_READY_SIGNAL
    assert readiness["satisfied_obligations"][0]["actual_lifecycle_state"] == ACTIVE_LIFECYCLE_STATE


@pytest.mark.parametrize(
    "lifecycle_state",
    [
        SUPERSEDED_LIFECYCLE_STATE,
        EXPIRED_LIFECYCLE_STATE,
    ],
)
def test_superseded_or_expired_document_requires_replacement_document(
    lifecycle_state: str,
) -> None:
    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=[_obligation()],
        document_artifacts=[_artifact(lifecycle_state=lifecycle_state)],
    )

    assert readiness["task_closure_ready"] is False
    assert readiness["recommended_task_state_effect"] == REQUIRES_REPLACEMENT_DOCUMENT_EFFECT
    assert readiness["workflow_readiness_signal"] == REPLACEMENT_DOCUMENT_REQUIRED_SIGNAL
    assert readiness["blocked_obligations"][0]["reason"] == (
        "document_requires_replacement_active_version"
    )


def test_archived_document_is_historical_record_only_and_cannot_satisfy_closure() -> None:
    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=[_obligation()],
        document_artifacts=[_artifact(lifecycle_state=ARCHIVED_LIFECYCLE_STATE)],
    )

    assert readiness["task_closure_ready"] is False
    assert readiness["recommended_task_state_effect"] == HISTORICAL_RECORD_ONLY_EFFECT
    assert readiness["workflow_readiness_signal"] == HISTORICAL_RECORD_ONLY_SIGNAL
    assert readiness["blocked_obligations"][0]["reason"] == (
        "archived_document_is_historical_record_only"
    )


def test_multiple_required_documents_require_all_obligations_satisfied() -> None:
    obligations = [
        _obligation(artifact_id="OQ_PROTOCOL_TP_001", document_family="protocol"),
        _obligation(artifact_id="OQ_REPORT_TP_001", document_family="report"),
        _obligation(
            artifact_id="DEV_TP_003",
            document_family="other_governed_document",
        ),
    ]
    documents = [
        _artifact(
            artifact_id="OQ_PROTOCOL_TP_001",
            document_family="protocol",
            lifecycle_state=ACTIVE_LIFECYCLE_STATE,
        ),
        _artifact(
            artifact_id="OQ_REPORT_TP_001",
            document_family="report",
            lifecycle_state=ACTIVE_LIFECYCLE_STATE,
        ),
        _artifact(
            artifact_id="DEV_TP_003",
            document_family="other_governed_document",
            lifecycle_state=IN_APPROVAL_LIFECYCLE_STATE,
        ),
    ]

    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=obligations,
        document_artifacts=documents,
    )

    assert readiness["task_closure_ready"] is False
    assert len(readiness["satisfied_obligations"]) == 2
    assert len(readiness["blocked_obligations"]) == 1
    assert readiness["blocked_obligations"][0]["required_artifact_id"] == "DEV_TP_003"


def test_multiple_required_documents_ready_when_all_are_active() -> None:
    obligations = [
        _obligation(artifact_id="OQ_PROTOCOL_TP_001", document_family="protocol"),
        _obligation(artifact_id="OQ_REPORT_TP_001", document_family="report"),
    ]
    documents = [
        _artifact(
            artifact_id="OQ_PROTOCOL_TP_001",
            document_family="protocol",
            lifecycle_state=ACTIVE_LIFECYCLE_STATE,
        ),
        _artifact(
            artifact_id="OQ_REPORT_TP_001",
            document_family="report",
            lifecycle_state=ACTIVE_LIFECYCLE_STATE,
        ),
    ]

    readiness = evaluate_task_document_workflow_readiness(
        task_payload=_task_payload(),
        document_obligations=obligations,
        document_artifacts=documents,
    )

    assert readiness["task_closure_ready"] is True
    assert len(readiness["satisfied_obligations"]) == 2
    assert readiness["recommended_task_state_effect"] == ALLOW_COMPLETION_EFFECT


def test_workflow_integration_recommends_effects_without_mutating_task_payload() -> None:
    task = _task_payload()
    original_task = deepcopy(task)

    readiness = evaluate_task_document_workflow_readiness(
        task_payload=task,
        document_obligations=[_obligation()],
        document_artifacts=[_artifact(lifecycle_state=ACTIVE_LIFECYCLE_STATE)],
    )

    assert task == original_task
    assert readiness["mutation_boundary"] == READINESS_EVALUATION_ONLY_BOUNDARY
    assert "task_state_update" not in readiness
    validate_task_document_workflow_readiness_payload(readiness)


def test_task_obligation_must_match_task_payload_task_id() -> None:
    obligation = build_task_document_obligation(
        obligation_id="OBL-WRONG-TASK",
        task_id="T-999",
        required_document_family="protocol",
        required_artifact_id="OQ_PROTOCOL_TP_001",
    )

    with pytest.raises(ValueError, match="task_id must match"):
        evaluate_task_document_workflow_readiness(
            task_payload=_task_payload(),
            document_obligations=[obligation],
            document_artifacts=[_artifact(lifecycle_state=ACTIVE_LIFECYCLE_STATE)],
        )
