
import pytest

from asbp.ai_runtime.context_packaging import (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
)
from asbp.ai_runtime.context_packets import (
    ADVISORY_QA_ASSISTANCE_MODE,
    AUTHORIZED_SOURCE_AUTHORITY_STATUS,
    PRODUCT_SOURCE_CONTEXT_FAMILY,
    RETRIEVAL_RESULT_CONTEXT_FAMILY,
    SUPPORT_ONLY_AUTHORITY_STATUS,
    build_ai_context_packet,
    build_ai_context_packet_item,
)
from asbp.ai_runtime.output_acceptance import (
    ADVISORY_ONLY_OUTPUT_STATE,
    AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
    AI_OUTPUT_REVIEW_CHECKPOINT_ID,
    DRAFT_ONLY_OUTPUT_STATE,
    HUMAN_ACCEPT_DECISION,
    HUMAN_ACCEPTED_OUTPUT_STATE,
    HUMAN_REVIEW_DECISION,
    HUMAN_REVIEWED_OUTPUT_STATE,
    NOT_GENERATED_OUTPUT_STATE,
    REJECTED_OUTPUT_STATE,
    build_ai_output_review_artifact,
    build_ai_output_review_baseline,
    build_ai_output_review_decision,
    validate_ai_output_review_artifact,
    validate_ai_output_review_decision,
)
from asbp.ai_runtime.provider_contracts import build_ai_provider_adapter_boundary_request
from asbp.ai_runtime.refusal_rules import (
    DEFER_UNTIL_LATER_GATE_DECISION,
    LIMITED_ANSWER_DECISION as REFUSAL_LIMITED_ANSWER_DECISION,
    MISSING_SOURCE_TRIGGER,
    REQUEST_HUMAN_REVIEW_DECISION,
    PROVIDER_EXECUTION_BLOCKED_TRIGGER,
    REFUSE_DECISION,
    RETRIEVAL_SUPPORT_ONLY_TRIGGER,
    UNSUPPORTED_CLAIM_TRIGGER,
    build_ai_refusal_limitation_decision,
    build_ai_refusal_trigger,
    build_ai_refusal_trigger_from_context_item,
)


def _provider_boundary_request() -> dict[str, object]:
    return build_ai_provider_adapter_boundary_request(
        adapter_request_id="AIPROV-M316-OUTPUT",
    )


def _product_source_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-PRODUCT-M316",
        source_ref="PRODUCT-SOURCE-CQV@v1",
        source_family=PRODUCT_SOURCE_CONTEXT_FAMILY,
        source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
        authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
        evidence_status="validated",
        limitation_summary="Authoritative only for approved local CQV scenario scope.",
        allowed_use="May provide governed product-source facts.",
        blocked_use="Must not authorize release, approval, or provider execution.",
    )


def _retrieval_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-RETRIEVAL-M316",
        source_ref="RETRIEVAL-RESULT-M316@v1",
        source_family=RETRIEVAL_RESULT_CONTEXT_FAMILY,
        source_role=NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
        authority_status=SUPPORT_ONLY_AUTHORITY_STATUS,
        evidence_status="partial",
        limitation_summary="Retrieval result is helper-only and non-authoritative.",
        allowed_use="May help locate source-backed context.",
        blocked_use="Must not define compliance truth or source authority.",
    )


def _context_packet() -> dict[str, object]:
    return build_ai_context_packet(
        context_packet_id="CTX-PACKET-M316",
        assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
        provider_boundary_request=_provider_boundary_request(),
        context_items=[_product_source_item(), _retrieval_item()],
    )


def _review_required_decision() -> dict[str, object]:
    trigger = build_ai_refusal_trigger(
        trigger_id="REF-M316-REVIEW-REQUIRED",
        trigger_kind=UNSUPPORTED_CLAIM_TRIGGER,
        decision=REQUEST_HUMAN_REVIEW_DECISION,
        reason="Human review is required before any acceptance.",
        limitation_summary="Limitations must remain visible during review.",
    )
    return build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-M316-REVIEW-REQUIRED",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )


def _refused_decision() -> dict[str, object]:
    trigger = build_ai_refusal_trigger(
        trigger_id="REF-M316-REFUSE",
        trigger_kind=MISSING_SOURCE_TRIGGER,
        decision=REFUSE_DECISION,
        reason="Required source evidence is missing.",
        limitation_summary="Cannot accept output without governed source evidence.",
    )
    return build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-M316-REFUSE",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )


def _deferred_decision() -> dict[str, object]:
    trigger = build_ai_refusal_trigger(
        trigger_id="REF-M316-PROVIDER-BLOCKED",
        trigger_kind=PROVIDER_EXECUTION_BLOCKED_TRIGGER,
        decision=DEFER_UNTIL_LATER_GATE_DECISION,
        reason="Provider execution is blocked until a later checkpoint.",
        limitation_summary="First real provider/local runtime smoke targets M31.7 if authorized.",
    )
    return build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-M316-DEFERRED",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )


def _retrieval_limited_decision() -> dict[str, object]:
    trigger = build_ai_refusal_trigger_from_context_item(
        trigger_id="REF-M316-RETRIEVAL",
        context_item=_retrieval_item(),
        trigger_kind=RETRIEVAL_SUPPORT_ONLY_TRIGGER,
        decision=REFUSAL_LIMITED_ANSWER_DECISION,
        reason="Retrieval is support-only and cannot define source truth.",
    )
    return build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-M316-RETRIEVAL",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )


def test_output_review_baseline_exposes_m31_6_rules() -> None:
    baseline = build_ai_output_review_baseline()

    assert baseline["checkpoint"] == AI_OUTPUT_REVIEW_CHECKPOINT_ID
    assert DRAFT_ONLY_OUTPUT_STATE in baseline["supported_output_states"]
    assert HUMAN_ACCEPTED_OUTPUT_STATE in baseline["supported_output_states"]
    assert "human_review_required_for_acceptance" in baseline["required_rule_families"]
    assert "ai_approval_authority" in baseline["blocked_runtime_scope"]
    assert "M31.7" in baseline["recommended_next_checkpoint"]


def test_output_artifact_allows_review_required_ai_assisted_draft() -> None:
    artifact = build_ai_output_review_artifact(
        output_artifact_id="OUT-M316-DRAFT",
        output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
        output_state=ADVISORY_ONLY_OUTPUT_STATE,
        refusal_decision=_review_required_decision(),
        limitation_summary="Advisory output remains limitation-visible.",
        allowed_use="May be used for human review discussion.",
        blocked_use="Must not be treated as approved, released, certified, or customer-ready.",
        output_ref="AI-ASSISTED-DRAFT-M316@v1",
    )

    assert artifact["output_state"] == ADVISORY_ONLY_OUTPUT_STATE
    assert artifact["ai_approval_authority_allowed"] is False
    assert artifact["provider_execution_enabled"] is False
    validate_ai_output_review_artifact(artifact)


def test_human_accepted_ai_output_requires_human_review_evidence() -> None:
    with pytest.raises(ValueError, match="human_reviewer_ref"):
        build_ai_output_review_artifact(
            output_artifact_id="OUT-M316-NO-HUMAN",
            output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
            output_state=HUMAN_ACCEPTED_OUTPUT_STATE,
            refusal_decision=_review_required_decision(),
            limitation_summary="Human evidence is required.",
            allowed_use="May be accepted only after human review.",
            blocked_use="Must not be auto-accepted.",
            output_ref="AI-ASSISTED-DRAFT-M316@v1",
        )

    artifact = build_ai_output_review_artifact(
        output_artifact_id="OUT-M316-HUMAN-ACCEPTED",
        output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
        output_state=HUMAN_ACCEPTED_OUTPUT_STATE,
        refusal_decision=_review_required_decision(),
        limitation_summary="Human accepted within bounded advisory scope.",
        allowed_use="May be treated as human accepted for the bounded review scope.",
        blocked_use="Must not claim release, certification, productization, or customer readiness.",
        output_ref="AI-ASSISTED-DRAFT-M316@v1",
        human_reviewer_ref="project-owner",
        human_review_evidence_ref="HUMAN-REVIEW-M316@v1",
    )

    decision = build_ai_output_review_decision(
        review_decision_id="REVIEW-M316-HUMAN-ACCEPT",
        output_artifact=artifact,
        review_decision=HUMAN_ACCEPT_DECISION,
        reviewer_ref="project-owner",
        review_evidence_ref="HUMAN-REVIEW-M316@v1",
    )

    assert decision["review_decision"] == HUMAN_ACCEPT_DECISION
    validate_ai_output_review_decision(decision)


def test_refused_output_cannot_be_human_accepted() -> None:
    with pytest.raises(ValueError, match="cannot depend on refusal"):
        build_ai_output_review_artifact(
            output_artifact_id="OUT-M316-REFUSED-ACCEPT",
            output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
            output_state=HUMAN_ACCEPTED_OUTPUT_STATE,
            refusal_decision=_refused_decision(),
            limitation_summary="Refused output cannot be accepted.",
            allowed_use="None.",
            blocked_use="Must not be accepted.",
            output_ref="AI-REFUSED-M316@v1",
            human_reviewer_ref="project-owner",
            human_review_evidence_ref="HUMAN-REVIEW-M316@v1",
        )

    artifact = build_ai_output_review_artifact(
        output_artifact_id="OUT-M316-REFUSED",
        output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
        output_state=REJECTED_OUTPUT_STATE,
        refusal_decision=_refused_decision(),
        limitation_summary="Refused output is rejected.",
        allowed_use="May record refusal evidence only.",
        blocked_use="Must not be accepted.",
    )

    assert artifact["output_state"] == REJECTED_OUTPUT_STATE


def test_later_gate_provider_decision_cannot_be_accepted() -> None:
    with pytest.raises(ValueError, match="Later-gate decisions"):
        build_ai_output_review_artifact(
            output_artifact_id="OUT-M316-DEFERRED-BAD",
            output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
            output_state=HUMAN_REVIEWED_OUTPUT_STATE,
            refusal_decision=_deferred_decision(),
            limitation_summary="Provider execution belongs to M31.7 or later.",
            allowed_use="May be deferred.",
            blocked_use="Must not execute provider/model calls.",
            output_ref="AI-DEFERRED-M316@v1",
            human_reviewer_ref="project-owner",
            human_review_evidence_ref="HUMAN-REVIEW-M316@v1",
        )


def test_support_only_retrieval_cannot_support_final_acceptance() -> None:
    with pytest.raises(ValueError, match="Support-only retrieval"):
        build_ai_output_review_artifact(
            output_artifact_id="OUT-M316-RETRIEVAL-ACCEPT",
            output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
            output_state=HUMAN_ACCEPTED_OUTPUT_STATE,
            refusal_decision=_retrieval_limited_decision(),
            limitation_summary="Retrieval context is support-only.",
            allowed_use="May support discussion.",
            blocked_use="Must not support final acceptance as source truth.",
            output_ref="AI-RETRIEVAL-M316@v1",
            human_reviewer_ref="project-owner",
            human_review_evidence_ref="HUMAN-REVIEW-M316@v1",
        )


def test_output_review_rejects_ai_authority_and_payload_fields() -> None:
    artifact = build_ai_output_review_artifact(
        output_artifact_id="OUT-M316-FLAGS",
        output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
        output_state=ADVISORY_ONLY_OUTPUT_STATE,
        refusal_decision=_review_required_decision(),
        limitation_summary="No authority granted.",
        allowed_use="May be reviewed.",
        blocked_use="Must not approve, release, certify, or mutate state.",
        output_ref="AI-FLAGS-M316@v1",
    )

    for field_name in (
        "ai_approval_authority_allowed",
        "ai_release_authority_allowed",
        "ai_certification_authority_allowed",
        "model_owned_state_mutation_allowed",
        "provider_execution_enabled",
        "prompt_execution_enabled",
        "productization_claim_allowed",
        "customer_ready_output_claim_allowed",
        "retrieval_as_source_truth_allowed",
    ):
        corrupted = dict(artifact)
        corrupted[field_name] = True
        with pytest.raises(ValueError, match=field_name):
            validate_ai_output_review_artifact(corrupted)

    corrupted = dict(artifact)
    corrupted["model_output"] = "generated output text"
    with pytest.raises(ValueError, match="model_output"):
        validate_ai_output_review_artifact(corrupted)


def test_human_review_decision_requires_matching_state_and_evidence() -> None:
    artifact = build_ai_output_review_artifact(
        output_artifact_id="OUT-M316-HUMAN-REVIEWED",
        output_origin=AI_ASSISTED_DRAFT_OUTPUT_ORIGIN,
        output_state=HUMAN_REVIEWED_OUTPUT_STATE,
        refusal_decision=_review_required_decision(),
        limitation_summary="Reviewed but not accepted.",
        allowed_use="May document human review.",
        blocked_use="Must not claim human acceptance.",
        output_ref="AI-REVIEWED-M316@v1",
        human_reviewer_ref="project-owner",
        human_review_evidence_ref="HUMAN-REVIEW-M316@v1",
    )

    with pytest.raises(ValueError, match="requires human_accepted"):
        build_ai_output_review_decision(
            review_decision_id="REVIEW-M316-BAD-ACCEPT",
            output_artifact=artifact,
            review_decision=HUMAN_ACCEPT_DECISION,
            reviewer_ref="project-owner",
            review_evidence_ref="HUMAN-REVIEW-M316@v1",
        )

    decision = build_ai_output_review_decision(
        review_decision_id="REVIEW-M316-HUMAN-REVIEW",
        output_artifact=artifact,
        review_decision=HUMAN_REVIEW_DECISION,
        reviewer_ref="project-owner",
        review_evidence_ref="HUMAN-REVIEW-M316@v1",
    )
    assert decision["review_decision"] == HUMAN_REVIEW_DECISION
