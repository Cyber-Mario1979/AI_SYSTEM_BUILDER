"Refusal and limitation rules for M31.5 governed AI assistance."

from __future__ import annotations

from typing import Any

from asbp.ai_runtime.context_packets import (
    AI_CONTEXT_PACKET_STATUS_VALIDATED,
    RETRIEVAL_RESULT_CONTEXT_FAMILY,
    SUPPORT_ONLY_AUTHORITY_STATUS,
    validate_ai_context_packet,
    validate_ai_context_packet_item,
)
from asbp.ai_runtime.provider_contracts import PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS
from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

AI_REFUSAL_RULES_CHECKPOINT_ID = "M31.5"
AI_REFUSAL_RULES_CONTRACT_VERSION = "ai-refusal-limitation-rules-v1"
AI_REFUSAL_RULES_STATUS_VALIDATED = "ai_refusal_limitation_rules_validated"

REFUSE_DECISION = "refuse"
LIMITED_ANSWER_DECISION = "limited_answer"
REQUEST_SOURCE_DECISION = "request_source"
REQUEST_HUMAN_REVIEW_DECISION = "request_human_review"
DEFER_UNTIL_LATER_GATE_DECISION = "defer_until_later_gate"
SUPPORTED_REFUSAL_DECISIONS = (
    REFUSE_DECISION,
    LIMITED_ANSWER_DECISION,
    REQUEST_SOURCE_DECISION,
    REQUEST_HUMAN_REVIEW_DECISION,
    DEFER_UNTIL_LATER_GATE_DECISION,
)

MISSING_SOURCE_TRIGGER = "missing_source"
UNVERIFIED_STANDARDS_TRIGGER = "unverified_standards"
UNSUPPORTED_CLAIM_TRIGGER = "unsupported_claim"
OUT_OF_SCOPE_REQUEST_TRIGGER = "out_of_scope_request"
RETRIEVAL_SUPPORT_ONLY_TRIGGER = "retrieval_support_only"
PROVIDER_EXECUTION_BLOCKED_TRIGGER = "provider_execution_blocked"
STATE_MUTATION_BLOCKED_TRIGGER = "state_mutation_blocked"
AI_APPROVAL_BLOCKED_TRIGGER = "ai_approval_blocked"
GENERATED_OUTPUT_ACCEPTANCE_BLOCKED_TRIGGER = "generated_output_acceptance_blocked"
PRODUCTIZATION_BLOCKED_TRIGGER = "productization_blocked"
SUPPORTED_REFUSAL_TRIGGER_KINDS = (
    MISSING_SOURCE_TRIGGER,
    UNVERIFIED_STANDARDS_TRIGGER,
    UNSUPPORTED_CLAIM_TRIGGER,
    OUT_OF_SCOPE_REQUEST_TRIGGER,
    RETRIEVAL_SUPPORT_ONLY_TRIGGER,
    PROVIDER_EXECUTION_BLOCKED_TRIGGER,
    STATE_MUTATION_BLOCKED_TRIGGER,
    AI_APPROVAL_BLOCKED_TRIGGER,
    GENERATED_OUTPUT_ACCEPTANCE_BLOCKED_TRIGGER,
    PRODUCTIZATION_BLOCKED_TRIGGER,
)

_REQUIRED_TRIGGER_STRING_FIELDS = (
    "trigger_id",
    "trigger_kind",
    "decision",
    "reason",
    "limitation_summary",
)

_REQUIRED_RULE_DECISION_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "refusal_decision_id",
    "decision",
    "refusal_limitation_status",
    "context_packet_id",
    "context_packet_status",
    "provider_execution_status",
)

_REQUIRED_RULE_DECISION_FALSE_FIELDS = (
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

_PROHIBITED_REFUSAL_RULE_FIELDS = (
    "raw_prompt",
    "free_form_prompt",
    "untracked_fact",
    "untracked_facts",
    "raw_retrieval_dump",
    "raw_retrieval_chunks",
    "messages",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "api_key",
    "provider_sdk_client",
    "raw_provider_payload",
    "raw_provider_response",
    "model_output",
    "generated_final_output",
    "state_mutation_payload",
    "approval_payload",
)


def build_ai_refusal_rules_baseline() -> dict[str, Any]:
    """Return M31.5 refusal and limitation baseline rules."""
    return {
        "checkpoint": AI_REFUSAL_RULES_CHECKPOINT_ID,
        "contract_version": AI_REFUSAL_RULES_CONTRACT_VERSION,
        "refusal_limitation_status": AI_REFUSAL_RULES_STATUS_VALIDATED,
        "supported_decisions": list(SUPPORTED_REFUSAL_DECISIONS),
        "supported_trigger_kinds": list(SUPPORTED_REFUSAL_TRIGGER_KINDS),
        "required_rule_families": [
            "missing_source_refusal",
            "unverified_standards_refusal",
            "unsupported_claim_refusal",
            "out_of_scope_request_refusal",
            "retrieval_support_only_limitation",
            "provider_execution_blocked_limitation",
        ],
        "blocked_runtime_scope": [
            "real_provider_calls",
            "local_model_inference",
            "prompt_execution",
            "model_guessing_missing_truth",
            "retrieval_backed_source_truth",
            "generated_output_acceptance",
            "ai_approval_authority",
            "state_mutation",
            "productization_claims",
        ],
    }


def build_ai_refusal_trigger(
    *,
    trigger_id: str,
    trigger_kind: str,
    decision: str,
    reason: str,
    limitation_summary: str,
    source_ref: str | None = None,
    context_item_id: str | None = None,
) -> dict[str, object]:
    """Build and validate one refusal/limitation trigger."""
    trigger = {
        "trigger_id": _require_non_empty_string(
            trigger_id,
            field_name="trigger_id",
            error_prefix="AI refusal trigger",
        ),
        "trigger_kind": _normalize_supported_value(
            trigger_kind,
            field_name="trigger_kind",
            supported_values=SUPPORTED_REFUSAL_TRIGGER_KINDS,
            error_prefix="AI refusal trigger",
        ),
        "decision": _normalize_supported_value(
            decision,
            field_name="decision",
            supported_values=SUPPORTED_REFUSAL_DECISIONS,
            error_prefix="AI refusal trigger",
        ),
        "reason": _require_non_empty_string(
            reason,
            field_name="reason",
            error_prefix="AI refusal trigger",
        ),
        "limitation_summary": _require_non_empty_string(
            limitation_summary,
            field_name="limitation_summary",
            error_prefix="AI refusal trigger",
        ),
        "source_ref": (
            _parse_version_pinned_ref(source_ref, field_name="source_ref")
            if source_ref is not None
            else None
        ),
        "context_item_id": (
            _require_non_empty_string(
                context_item_id,
                field_name="context_item_id",
                error_prefix="AI refusal trigger",
            )
            if context_item_id is not None
            else None
        ),
    }
    validate_ai_refusal_trigger(trigger)
    return trigger


def build_ai_refusal_trigger_from_context_item(
    *,
    trigger_id: str,
    context_item: dict[str, object],
    trigger_kind: str,
    decision: str,
    reason: str,
) -> dict[str, object]:
    """Build a refusal trigger that propagates a context item limitation."""
    validate_ai_context_packet_item(context_item)
    return build_ai_refusal_trigger(
        trigger_id=trigger_id,
        trigger_kind=trigger_kind,
        decision=decision,
        reason=reason,
        limitation_summary=str(context_item["limitation_summary"]),
        source_ref=str(context_item["source_ref"]),
        context_item_id=str(context_item["context_item_id"]),
    )


def validate_ai_refusal_trigger(trigger: dict[str, object]) -> None:
    """Validate one M31.5 refusal/limitation trigger."""
    _validate_prohibited_fields(trigger, _PROHIBITED_REFUSAL_RULE_FIELDS)
    _validate_required_string_fields(
        trigger,
        _REQUIRED_TRIGGER_STRING_FIELDS,
        error_prefix="AI refusal trigger",
    )
    trigger_kind = _normalize_supported_value(
        trigger["trigger_kind"],
        field_name="trigger_kind",
        supported_values=SUPPORTED_REFUSAL_TRIGGER_KINDS,
        error_prefix="AI refusal trigger",
    )
    decision = _normalize_supported_value(
        trigger["decision"],
        field_name="decision",
        supported_values=SUPPORTED_REFUSAL_DECISIONS,
        error_prefix="AI refusal trigger",
    )
    _validate_trigger_decision_alignment(
        trigger_kind=trigger_kind,
        decision=decision,
    )
    source_ref = trigger.get("source_ref")
    if source_ref is not None:
        _parse_version_pinned_ref(source_ref, field_name="source_ref")
    context_item_id = trigger.get("context_item_id")
    if context_item_id is not None:
        _require_non_empty_string(
            context_item_id,
            field_name="context_item_id",
            error_prefix="AI refusal trigger",
        )


def build_ai_refusal_limitation_decision(
    *,
    refusal_decision_id: str,
    context_packet: dict[str, object],
    trigger_items: list[dict[str, object]],
) -> dict[str, object]:
    """Build and validate an M31.5 refusal/limitation decision."""
    validate_ai_context_packet(context_packet)
    decision = _select_decision(trigger_items)
    payload = {
        "checkpoint": AI_REFUSAL_RULES_CHECKPOINT_ID,
        "contract_version": AI_REFUSAL_RULES_CONTRACT_VERSION,
        "refusal_decision_id": _require_non_empty_string(
            refusal_decision_id,
            field_name="refusal_decision_id",
            error_prefix="AI refusal limitation decision",
        ),
        "decision": decision,
        "refusal_limitation_status": AI_REFUSAL_RULES_STATUS_VALIDATED,
        "context_packet_id": str(context_packet["context_packet_id"]),
        "context_packet_status": str(context_packet["context_packet_status"]),
        "assistance_mode": str(context_packet["assistance_mode"]),
        "provider_execution_status": str(context_packet["provider_execution_status"]),
        "trigger_items": list(trigger_items),
        "provider_execution_enabled": False,
        "prompt_execution_enabled": False,
        "model_guessing_allowed": False,
        "retrieval_as_source_truth_allowed": False,
        "standards_truth_invention_allowed": False,
        "state_mutation_allowed": False,
        "ai_approval_allowed": False,
        "generated_output_acceptance_enabled": False,
        "productization_claim_allowed": False,
        "context_dependency_policy": "refusal_rules_evaluate_m31_4_context_packets_only",
        "provider_dependency_policy": "refusal_rules_do_not_call_providers_or_models",
        "limitation_policy": "unsupported_or_unverified_claims_must_refuse_or_limit",
    }
    validate_ai_refusal_limitation_decision(payload)
    return payload


def validate_ai_refusal_limitation_decision(payload: dict[str, object]) -> None:
    """Validate an M31.5 refusal/limitation decision."""
    _validate_prohibited_fields(payload, _PROHIBITED_REFUSAL_RULE_FIELDS)
    _validate_required_string_fields(
        payload,
        _REQUIRED_RULE_DECISION_STRING_FIELDS,
        error_prefix="AI refusal limitation decision",
    )
    _validate_expected_exact_value(
        payload,
        field_name="checkpoint",
        expected_value=AI_REFUSAL_RULES_CHECKPOINT_ID,
        error_prefix="AI refusal limitation decision",
    )
    _validate_expected_exact_value(
        payload,
        field_name="contract_version",
        expected_value=AI_REFUSAL_RULES_CONTRACT_VERSION,
        error_prefix="AI refusal limitation decision",
    )
    _validate_expected_exact_value(
        payload,
        field_name="refusal_limitation_status",
        expected_value=AI_REFUSAL_RULES_STATUS_VALIDATED,
        error_prefix="AI refusal limitation decision",
    )
    _validate_expected_exact_value(
        payload,
        field_name="context_packet_status",
        expected_value=AI_CONTEXT_PACKET_STATUS_VALIDATED,
        error_prefix="AI refusal limitation decision",
    )
    _validate_expected_exact_value(
        payload,
        field_name="provider_execution_status",
        expected_value=PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
        error_prefix="AI refusal limitation decision",
    )
    decision = _normalize_supported_value(
        payload["decision"],
        field_name="decision",
        supported_values=SUPPORTED_REFUSAL_DECISIONS,
        error_prefix="AI refusal limitation decision",
    )
    for field_name in _REQUIRED_RULE_DECISION_FALSE_FIELDS:
        if payload.get(field_name) is not False:
            raise ValueError(
                "AI refusal limitation decision requires "
                f"{field_name} to be False."
            )

    trigger_items = payload.get("trigger_items")
    if not isinstance(trigger_items, list) or not trigger_items:
        raise ValueError("AI refusal limitation decision must declare trigger_items.")
    trigger_ids: list[str] = []
    trigger_decisions: list[str] = []
    for trigger in trigger_items:
        if not isinstance(trigger, dict):
            raise ValueError("AI refusal limitation decision trigger_items must contain dicts.")
        validate_ai_refusal_trigger(trigger)
        trigger_ids.append(str(trigger["trigger_id"]))
        trigger_decisions.append(str(trigger["decision"]))
    _reject_duplicates(trigger_ids, field_name="trigger_id")
    if decision != _highest_priority_decision(trigger_decisions):
        raise ValueError("AI refusal limitation decision does not match trigger priority.")


def validate_retrieval_context_requires_limitation(context_item: dict[str, object]) -> None:
    """Validate retrieval context remains support-only and limitation-visible."""
    validate_ai_context_packet_item(context_item)
    if context_item.get("source_family") != RETRIEVAL_RESULT_CONTEXT_FAMILY:
        raise ValueError("Expected retrieval_result context item.")
    if context_item.get("authority_status") != SUPPORT_ONLY_AUTHORITY_STATUS:
        raise ValueError("Retrieval context must remain support-only.")
    _require_non_empty_string(
        context_item.get("limitation_summary"),
        field_name="limitation_summary",
        error_prefix="AI retrieval limitation rule",
    )


def _select_decision(trigger_items: list[dict[str, object]]) -> str:
    if not isinstance(trigger_items, list) or not trigger_items:
        raise ValueError("AI refusal limitation decision must declare trigger_items.")
    decisions: list[str] = []
    for trigger in trigger_items:
        validate_ai_refusal_trigger(trigger)
        decisions.append(str(trigger["decision"]))
    return _highest_priority_decision(decisions)


def _highest_priority_decision(decisions: list[str]) -> str:
    priority = (
        REFUSE_DECISION,
        DEFER_UNTIL_LATER_GATE_DECISION,
        REQUEST_HUMAN_REVIEW_DECISION,
        REQUEST_SOURCE_DECISION,
        LIMITED_ANSWER_DECISION,
    )
    for candidate in priority:
        if candidate in decisions:
            return candidate
    raise ValueError("AI refusal limitation decision has no supported trigger decisions.")


def _validate_trigger_decision_alignment(*, trigger_kind: str, decision: str) -> None:
    allowed_by_trigger = {
        MISSING_SOURCE_TRIGGER: (REFUSE_DECISION, REQUEST_SOURCE_DECISION),
        UNVERIFIED_STANDARDS_TRIGGER: (REFUSE_DECISION, REQUEST_SOURCE_DECISION),
        UNSUPPORTED_CLAIM_TRIGGER: (REFUSE_DECISION, REQUEST_HUMAN_REVIEW_DECISION),
        OUT_OF_SCOPE_REQUEST_TRIGGER: (REFUSE_DECISION, DEFER_UNTIL_LATER_GATE_DECISION),
        RETRIEVAL_SUPPORT_ONLY_TRIGGER: (
            REFUSE_DECISION,
            LIMITED_ANSWER_DECISION,
            REQUEST_SOURCE_DECISION,
        ),
        PROVIDER_EXECUTION_BLOCKED_TRIGGER: (DEFER_UNTIL_LATER_GATE_DECISION,),
        STATE_MUTATION_BLOCKED_TRIGGER: (REFUSE_DECISION,),
        AI_APPROVAL_BLOCKED_TRIGGER: (REFUSE_DECISION,),
        GENERATED_OUTPUT_ACCEPTANCE_BLOCKED_TRIGGER: (DEFER_UNTIL_LATER_GATE_DECISION,),
        PRODUCTIZATION_BLOCKED_TRIGGER: (REFUSE_DECISION, DEFER_UNTIL_LATER_GATE_DECISION),
    }
    if decision not in allowed_by_trigger[trigger_kind]:
        raise ValueError(
            f"AI refusal trigger {trigger_kind!r} cannot use decision {decision!r}."
        )


def _parse_version_pinned_ref(raw_ref: object, *, field_name: str) -> str:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="AI refusal rule ref",
    )
    return parse_version_pinned_asset_ref(ref)["asset_ref"]


def _normalize_supported_value(
    value: object,
    *,
    field_name: str,
    supported_values: tuple[str, ...],
    error_prefix: str,
) -> str:
    normalized = _require_non_empty_string(
        value,
        field_name=field_name,
        error_prefix=error_prefix,
    )
    if normalized not in supported_values:
        raise ValueError(
            f"{error_prefix} declares unsupported {field_name}. "
            f"Expected one of: {', '.join(supported_values)}."
        )
    return normalized


def _require_non_empty_string(
    value: object,
    *,
    field_name: str,
    error_prefix: str,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        _require_non_empty_string(
            payload.get(field_name),
            field_name=field_name,
            error_prefix=error_prefix,
        )


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


def _validate_prohibited_fields(
    payload: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in M31.5 refusal/limitation rules."
            )


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate value in {field_name}: {value!r}.")
        seen.add(value)
