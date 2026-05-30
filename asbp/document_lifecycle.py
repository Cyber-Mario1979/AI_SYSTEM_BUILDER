from __future__ import annotations

from asbp.document_lifecycle_model import (
    REQUIRED_DOCUMENT_LIFECYCLE_NON_IMPLEMENTATION_CLAIMS,
    DocumentLifecycleObligationModel,
    DocumentLifecycleRecordModel,
    DocumentLifecycleRuleModel,
    DocumentLifecycleState,
    DocumentLifecycleTransitionHistoryModel,
)
from asbp.document_lifecycle_store import get_default_document_lifecycle_rule
from asbp.renderer_output_model import RendererOutputArtifactModel


def create_document_lifecycle_record_from_artifact(
    *,
    lifecycle_record_id: str,
    artifact: RendererOutputArtifactModel,
    rule: DocumentLifecycleRuleModel | None = None,
    supersedes_record_id: str | None = None,
) -> DocumentLifecycleRecordModel:
    rule = rule or get_default_document_lifecycle_rule()
    carried_forward_limitations = _build_carried_forward_limitations(artifact)

    return DocumentLifecycleRecordModel(
        lifecycle_record_id=lifecycle_record_id,
        version=_version_from_id(lifecycle_record_id),
        lifecycle_state="draft",
        source_artifact_id=artifact.artifact_id,
        source_draft_id=artifact.metadata.source_draft_id,
        template_id=artifact.metadata.template_id,
        schema_id=artifact.metadata.schema_id,
        standards_control_packet_id=artifact.metadata.standards_control_packet_id,
        output_format=artifact.output_format,
        artifact_metadata_ref=f"{artifact.artifact_id}::metadata",
        review_obligations=_clone_obligations(rule.required_review_obligations),
        approval_obligations=_clone_obligations(rule.required_approval_obligations),
        task_closure_dependencies=_clone_obligations(rule.required_task_closure_dependencies),
        supersedes_record_id=supersedes_record_id,
        placeholder_present=artifact.metadata.placeholder_present,
        limitation_present=artifact.metadata.limitation_present,
        standards_warning_present=artifact.metadata.standards_warning_present,
        carried_forward_limitations=carried_forward_limitations,
        transition_history=[
            DocumentLifecycleTransitionHistoryModel(
                from_state=None,
                to_state="draft",
                transition_reason="Lifecycle record created from controlled renderer artifact metadata.",
            )
        ],
        explicit_non_implementation_claims=sorted(
            REQUIRED_DOCUMENT_LIFECYCLE_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def transition_document_lifecycle_record(
    record: DocumentLifecycleRecordModel,
    target_state: DocumentLifecycleState,
    *,
    rule: DocumentLifecycleRuleModel | None = None,
    resolved_review_obligation_ids: set[str] | None = None,
    resolved_approval_obligation_ids: set[str] | None = None,
    resolved_task_closure_dependency_ids: set[str] | None = None,
    transition_reason: str | None = None,
) -> DocumentLifecycleRecordModel:
    rule = rule or get_default_document_lifecycle_rule()
    _assert_transition_allowed(rule, record.lifecycle_state, target_state)

    payload = record.model_dump()
    payload["review_obligations"] = _resolve_obligations(
        record.review_obligations,
        resolved_review_obligation_ids or set(),
    )
    payload["approval_obligations"] = _resolve_obligations(
        record.approval_obligations,
        resolved_approval_obligation_ids or set(),
    )
    payload["task_closure_dependencies"] = _resolve_obligations(
        record.task_closure_dependencies,
        resolved_task_closure_dependency_ids or set(),
    )
    payload["lifecycle_state"] = target_state
    payload["transition_history"] = [
        *record.transition_history,
        DocumentLifecycleTransitionHistoryModel(
            from_state=record.lifecycle_state,
            to_state=target_state,
            transition_reason=transition_reason
            or f"Lifecycle transition {record.lifecycle_state} -> {target_state}.",
        ),
    ]
    return DocumentLifecycleRecordModel(**payload)


def supersede_document_lifecycle_record(
    record: DocumentLifecycleRecordModel,
    *,
    superseded_by_record_id: str,
    rule: DocumentLifecycleRuleModel | None = None,
    transition_reason: str | None = None,
) -> DocumentLifecycleRecordModel:
    rule = rule or get_default_document_lifecycle_rule()
    _assert_transition_allowed(rule, record.lifecycle_state, "superseded")

    payload = record.model_dump()
    payload["lifecycle_state"] = "superseded"
    payload["superseded_by_record_id"] = superseded_by_record_id
    payload["transition_history"] = [
        *record.transition_history,
        DocumentLifecycleTransitionHistoryModel(
            from_state=record.lifecycle_state,
            to_state="superseded",
            transition_reason=transition_reason
            or f"Lifecycle record superseded by {superseded_by_record_id}.",
        ),
    ]
    return DocumentLifecycleRecordModel(**payload)


def assert_generated_prose_cannot_mutate_lifecycle_truth(
    record: DocumentLifecycleRecordModel,
    requested_state_from_generated_content: str,
) -> None:
    if requested_state_from_generated_content != record.lifecycle_state:
        raise ValueError(
            "Generated prose cannot mutate document lifecycle truth: "
            f"{requested_state_from_generated_content} != {record.lifecycle_state}"
        )


def _assert_transition_allowed(
    rule: DocumentLifecycleRuleModel,
    from_state: DocumentLifecycleState,
    to_state: DocumentLifecycleState,
) -> None:
    for transition in rule.allowed_transitions:
        if transition.from_state == from_state and transition.to_state == to_state:
            return
    raise ValueError(f"Document lifecycle transition is not allowed: {from_state} -> {to_state}")


def _clone_obligations(
    obligations: list[DocumentLifecycleObligationModel],
) -> list[DocumentLifecycleObligationModel]:
    return [DocumentLifecycleObligationModel(**obligation.model_dump()) for obligation in obligations]


def _resolve_obligations(
    obligations: list[DocumentLifecycleObligationModel],
    resolved_ids: set[str],
) -> list[DocumentLifecycleObligationModel]:
    updated_obligations: list[DocumentLifecycleObligationModel] = []
    known_ids = {obligation.obligation_id for obligation in obligations}
    unknown_ids = sorted(resolved_ids - known_ids)
    if unknown_ids:
        raise ValueError(
            "Cannot resolve unknown document lifecycle obligation id(s): "
            f"{', '.join(unknown_ids)}"
        )

    for obligation in obligations:
        payload = obligation.model_dump()
        if obligation.obligation_id in resolved_ids:
            payload["resolved"] = True
        updated_obligations.append(DocumentLifecycleObligationModel(**payload))
    return updated_obligations


def _build_carried_forward_limitations(artifact: RendererOutputArtifactModel) -> list[str]:
    limitations: list[str] = [
        "Renderer artifact remains non-product-ready until later validation and UAT checkpoints."
    ]
    if artifact.metadata.placeholder_present:
        limitations.append("Renderer metadata indicates visible placeholders are present.")
    if artifact.metadata.limitation_present:
        limitations.append("Renderer metadata indicates visible limitations are present.")
    if artifact.metadata.standards_warning_present:
        limitations.append("Renderer metadata indicates visible standards warnings are present.")
    return limitations


def _version_from_id(identifier: str) -> str:
    return identifier.rsplit("@", 1)[1]
