import pytest

from asbp.ai_runtime.context_packaging import (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    GOVERNED_CONTRACT_ROLE,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
)
from asbp.ai_runtime.context_packets import (
    ADVISORY_QA_ASSISTANCE_MODE,
    AUTHORIZED_SOURCE_AUTHORITY_STATUS,
    LIMITED_SOURCE_AUTHORITY_STATUS,
    PRODUCT_SOURCE_CONTEXT_FAMILY,
    RETRIEVAL_RESULT_CONTEXT_FAMILY,
    STANDARDS_REGISTRY_CONTEXT_FAMILY,
    SUPPORT_ONLY_AUTHORITY_STATUS,
    build_ai_context_packet,
    build_ai_context_packet_item,
)
from asbp.ai_runtime.provider_contracts import build_ai_provider_adapter_boundary_request
from asbp.ai_runtime.refusal_rules import (
    AI_APPROVAL_BLOCKED_TRIGGER,
    AI_REFUSAL_RULES_CHECKPOINT_ID,
    AI_REFUSAL_RULES_STATUS_VALIDATED,
    DEFER_UNTIL_LATER_GATE_DECISION,
    LIMITED_ANSWER_DECISION,
    MISSING_SOURCE_TRIGGER,
    OUT_OF_SCOPE_REQUEST_TRIGGER,
    PRODUCTIZATION_BLOCKED_TRIGGER,
    PROVIDER_EXECUTION_BLOCKED_TRIGGER,
    REFUSE_DECISION,
    RETRIEVAL_SUPPORT_ONLY_TRIGGER,
    STATE_MUTATION_BLOCKED_TRIGGER,
    UNVERIFIED_STANDARDS_TRIGGER,
    UNSUPPORTED_CLAIM_TRIGGER,
    build_ai_refusal_limitation_decision,
    build_ai_refusal_rules_baseline,
    build_ai_refusal_trigger,
    build_ai_refusal_trigger_from_context_item,
    validate_ai_refusal_limitation_decision,
    validate_ai_refusal_trigger,
    validate_retrieval_context_requires_limitation,
)


def _provider_boundary_request() -> dict[str, object]:
    return build_ai_provider_adapter_boundary_request(
        adapter_request_id="AIPROV-M315-REFUSAL",
    )


def _product_source_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-PRODUCT-REFUSAL",
        source_ref="PRODUCT-SOURCE-CQV@v1",
        source_family=PRODUCT_SOURCE_CONTEXT_FAMILY,
        source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
        authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
        evidence_status="validated",
        limitation_summary="Authoritative only for approved local CQV scenario scope.",
        allowed_use="May provide governed product-source facts.",
        blocked_use="Must not authorize release, approval, or provider execution.",
    )


def _standards_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-STANDARDS-REFUSAL",
        source_ref="STANDARDS-REGISTRY@v1",
        source_family=STANDARDS_REGISTRY_CONTEXT_FAMILY,
        source_role=GOVERNED_CONTRACT_ROLE,
        authority_status=LIMITED_SOURCE_AUTHORITY_STATUS,
        evidence_status="limited",
        limitation_summary="Registry coverage is limited and not clause-level authority.",
        allowed_use="May provide standards registry status and limitations.",
        blocked_use="Must not create legal, regulatory, or clause-level authority.",
    )


def _retrieval_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-RETRIEVAL-REFUSAL",
        source_ref="RETRIEVAL-RESULT-REFUSAL@v1",
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
        context_packet_id="CTX-PACKET-M315",
        assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
        provider_boundary_request=_provider_boundary_request(),
        standards_registry_ref="STANDARDS-REGISTRY@v1",
        context_items=[_product_source_item(), _standards_item(), _retrieval_item()],
    )


def test_refusal_rules_baseline_exposes_m31_5_rules() -> None:
    baseline = build_ai_refusal_rules_baseline()

    assert baseline["checkpoint"] == AI_REFUSAL_RULES_CHECKPOINT_ID
    assert baseline["refusal_limitation_status"] == AI_REFUSAL_RULES_STATUS_VALIDATED
    assert "missing_source_refusal" in baseline["required_rule_families"]
    assert "unverified_standards_refusal" in baseline["required_rule_families"]
    assert "retrieval_support_only_limitation" in baseline["required_rule_families"]
    assert "model_guessing_missing_truth" in baseline["blocked_runtime_scope"]


def test_build_refusal_decision_for_missing_source() -> None:
    trigger = build_ai_refusal_trigger(
        trigger_id="REF-MISSING-SOURCE",
        trigger_kind=MISSING_SOURCE_TRIGGER,
        decision=REFUSE_DECISION,
        reason="Required source evidence is missing.",
        limitation_summary="Cannot answer without governed source evidence.",
    )
    decision = build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-MISSING-SOURCE",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )

    assert decision["checkpoint"] == AI_REFUSAL_RULES_CHECKPOINT_ID
    assert decision["decision"] == REFUSE_DECISION
    assert decision["model_guessing_allowed"] is False
    assert decision["provider_execution_enabled"] is False
    assert decision["prompt_execution_enabled"] is False
    validate_ai_refusal_limitation_decision(decision)


def test_unverified_standards_trigger_propagates_context_limitation() -> None:
    trigger = build_ai_refusal_trigger_from_context_item(
        trigger_id="REF-STANDARDS-LIMITED",
        context_item=_standards_item(),
        trigger_kind=UNVERIFIED_STANDARDS_TRIGGER,
        decision=REFUSE_DECISION,
        reason="Standards context is limited and cannot support requested authority.",
    )

    assert trigger["source_ref"] == "STANDARDS-REGISTRY@v1"
    assert "not clause-level authority" in str(trigger["limitation_summary"])
    validate_ai_refusal_trigger(trigger)


def test_unsupported_claim_and_out_of_scope_trigger_decision_alignment() -> None:
    unsupported = build_ai_refusal_trigger(
        trigger_id="REF-UNSUPPORTED-CLAIM",
        trigger_kind=UNSUPPORTED_CLAIM_TRIGGER,
        decision=REFUSE_DECISION,
        reason="Claim is not supported by governed context.",
        limitation_summary="Unsupported claim must not be guessed.",
    )
    out_of_scope = build_ai_refusal_trigger(
        trigger_id="REF-OUT-OF-SCOPE",
        trigger_kind=OUT_OF_SCOPE_REQUEST_TRIGGER,
        decision=DEFER_UNTIL_LATER_GATE_DECISION,
        reason="Request belongs to a later release/productization gate.",
        limitation_summary="Productization and release claims remain blocked.",
    )

    decision = build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-PRIORITY",
        context_packet=_context_packet(),
        trigger_items=[out_of_scope, unsupported],
    )

    assert decision["decision"] == REFUSE_DECISION
    validate_ai_refusal_limitation_decision(decision)


def test_retrieval_support_only_context_can_only_limit_or_request_source() -> None:
    retrieval_item = _retrieval_item()
    validate_retrieval_context_requires_limitation(retrieval_item)
    trigger = build_ai_refusal_trigger_from_context_item(
        trigger_id="REF-RETRIEVAL-SUPPORT-ONLY",
        context_item=retrieval_item,
        trigger_kind=RETRIEVAL_SUPPORT_ONLY_TRIGGER,
        decision=LIMITED_ANSWER_DECISION,
        reason="Retrieval is support-only and cannot define source truth.",
    )
    decision = build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-RETRIEVAL",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )

    assert decision["decision"] == LIMITED_ANSWER_DECISION
    assert decision["retrieval_as_source_truth_allowed"] is False
    validate_ai_refusal_limitation_decision(decision)


def test_provider_execution_blocked_defers_until_later_gate() -> None:
    trigger = build_ai_refusal_trigger(
        trigger_id="REF-PROVIDER-BLOCKED",
        trigger_kind=PROVIDER_EXECUTION_BLOCKED_TRIGGER,
        decision=DEFER_UNTIL_LATER_GATE_DECISION,
        reason="Provider/model execution is blocked by M31.5 scope.",
        limitation_summary="No provider/model execution is authorized yet.",
    )
    decision = build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-PROVIDER-BLOCKED",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )

    assert decision["decision"] == DEFER_UNTIL_LATER_GATE_DECISION
    assert decision["provider_execution_enabled"] is False
    assert decision["prompt_execution_enabled"] is False


def test_state_mutation_ai_approval_and_productization_are_refused() -> None:
    triggers = [
        build_ai_refusal_trigger(
            trigger_id="REF-STATE-MUTATION",
            trigger_kind=STATE_MUTATION_BLOCKED_TRIGGER,
            decision=REFUSE_DECISION,
            reason="AI cannot mutate workflow state.",
            limitation_summary="State mutation must remain deterministic and human/system controlled.",
        ),
        build_ai_refusal_trigger(
            trigger_id="REF-AI-APPROVAL",
            trigger_kind=AI_APPROVAL_BLOCKED_TRIGGER,
            decision=REFUSE_DECISION,
            reason="AI cannot approve or release work.",
            limitation_summary="Approval authority remains human/governed workflow only.",
        ),
        build_ai_refusal_trigger(
            trigger_id="REF-PRODUCTIZATION",
            trigger_kind=PRODUCTIZATION_BLOCKED_TRIGGER,
            decision=REFUSE_DECISION,
            reason="Productization claim belongs to later gates.",
            limitation_summary="Commercial release/SaaS readiness remains blocked.",
        ),
    ]
    decision = build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-BLOCKED-AUTHORITY",
        context_packet=_context_packet(),
        trigger_items=triggers,
    )

    assert decision["decision"] == REFUSE_DECISION
    assert decision["state_mutation_allowed"] is False
    assert decision["ai_approval_allowed"] is False
    assert decision["productization_claim_allowed"] is False


def test_refusal_rules_reject_prohibited_prompt_provider_and_output_fields() -> None:
    prohibited_fields = {
        "raw_prompt": "answer freely",
        "raw_retrieval_dump": "retrieved text without source",
        "messages": [{"role": "user", "content": "hello"}],
        "api_key": "secret-key",
        "raw_provider_response": {"text": "provider output"},
        "model_output": "final answer",
        "generated_final_output": "approved output",
        "state_mutation_payload": {"status": "done"},
        "approval_payload": {"approved": True},
    }

    for field_name, value in prohibited_fields.items():
        trigger = build_ai_refusal_trigger(
            trigger_id=f"REF-BLOCK-{field_name}",
            trigger_kind=MISSING_SOURCE_TRIGGER,
            decision=REFUSE_DECISION,
            reason="Blocked field test.",
            limitation_summary="Blocked fields must not enter refusal rules.",
        )
        trigger[field_name] = value

        with pytest.raises(ValueError, match=field_name):
            validate_ai_refusal_trigger(trigger)


def test_refusal_decision_rejects_enabled_execution_and_acceptance_flags() -> None:
    trigger = build_ai_refusal_trigger(
        trigger_id="REF-FLAG-BASE",
        trigger_kind=MISSING_SOURCE_TRIGGER,
        decision=REFUSE_DECISION,
        reason="Required source evidence is missing.",
        limitation_summary="Cannot answer without governed source evidence.",
    )
    false_fields = (
        "provider_execution_enabled",
        "prompt_execution_enabled",
        "model_guessing_allowed",
        "retrieval_as_source_truth_allowed",
        "standards_truth_invention_allowed",
        "state_mutation_allowed",
        "ai_approval_allowed",
        "generated_output_acceptance_enabled",
        "productization_claim_allowed",
    )

    for field_name in false_fields:
        decision = build_ai_refusal_limitation_decision(
            refusal_decision_id=f"REF-DECISION-FLAG-{field_name}",
            context_packet=_context_packet(),
            trigger_items=[trigger],
        )
        decision[field_name] = True

        with pytest.raises(ValueError, match=field_name):
            validate_ai_refusal_limitation_decision(decision)


def test_refusal_trigger_rejects_invalid_decision_for_trigger_kind() -> None:
    with pytest.raises(ValueError, match="cannot use decision"):
        build_ai_refusal_trigger(
            trigger_id="REF-BAD-ALIGNMENT",
            trigger_kind=PROVIDER_EXECUTION_BLOCKED_TRIGGER,
            decision=REFUSE_DECISION,
            reason="Provider blocked should defer, not refuse.",
            limitation_summary="Provider execution belongs to later gates.",
        )
