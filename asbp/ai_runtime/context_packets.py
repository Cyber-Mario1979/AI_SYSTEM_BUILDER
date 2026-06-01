"Provider-facing context packet contract for M31.4 governed AI assistance."

from __future__ import annotations

from typing import Any

from asbp.ai_runtime.context_packaging import (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_ENGINE_INPUT_ROLE,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
)
from asbp.ai_runtime.provider_contracts import (
    AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
    DISABLED_PROVIDER_KIND,
    PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
    validate_ai_provider_adapter_boundary_request,
)
from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

AI_CONTEXT_PACKET_CHECKPOINT_ID = "M31.4"
AI_CONTEXT_PACKET_CONTRACT_VERSION = "ai-context-packet-v1"
AI_CONTEXT_PACKET_STATUS_VALIDATED = "ai_context_packet_validated"

ADVISORY_QA_ASSISTANCE_MODE = "advisory_q_and_a"
DOCUMENT_DRAFTING_SUPPORT_ASSISTANCE_MODE = "document_drafting_support"
REVIEW_SUPPORT_ASSISTANCE_MODE = "review_support"
COMPARISON_SUPPORT_ASSISTANCE_MODE = "comparison_support"
WORKFLOW_GUIDANCE_ASSISTANCE_MODE = "workflow_guidance"
SUPPORTED_ASSISTANCE_MODES = (
    ADVISORY_QA_ASSISTANCE_MODE,
    DOCUMENT_DRAFTING_SUPPORT_ASSISTANCE_MODE,
    REVIEW_SUPPORT_ASSISTANCE_MODE,
    COMPARISON_SUPPORT_ASSISTANCE_MODE,
    WORKFLOW_GUIDANCE_ASSISTANCE_MODE,
)

PRODUCT_SOURCE_CONTEXT_FAMILY = "product_source"
STANDARDS_REGISTRY_CONTEXT_FAMILY = "standards_registry"
TASK_WORKFLOW_STATE_CONTEXT_FAMILY = "task_workflow_state"
RETRIEVAL_RESULT_CONTEXT_FAMILY = "retrieval_result"
DOCUMENT_OUTPUT_CONTEXT_FAMILY = "document_output"
SUPPORTED_CONTEXT_PACKET_FAMILIES = (
    PRODUCT_SOURCE_CONTEXT_FAMILY,
    STANDARDS_REGISTRY_CONTEXT_FAMILY,
    TASK_WORKFLOW_STATE_CONTEXT_FAMILY,
    RETRIEVAL_RESULT_CONTEXT_FAMILY,
    DOCUMENT_OUTPUT_CONTEXT_FAMILY,
)

AUTHORIZED_SOURCE_AUTHORITY_STATUS = "authorized_source"
LIMITED_SOURCE_AUTHORITY_STATUS = "limited_source"
SUPPORT_ONLY_AUTHORITY_STATUS = "support_only"
SUPPORTED_AUTHORITY_STATUSES = (
    AUTHORIZED_SOURCE_AUTHORITY_STATUS,
    LIMITED_SOURCE_AUTHORITY_STATUS,
    SUPPORT_ONLY_AUTHORITY_STATUS,
)

_CONTEXT_PACKET_ITEM_REQUIRED_STRING_FIELDS = (
    "context_item_id",
    "source_ref",
    "source_family",
    "source_role",
    "authority_status",
    "evidence_status",
    "limitation_summary",
    "allowed_use",
    "blocked_use",
)

_CONTEXT_PACKET_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "context_packet_id",
    "assistance_mode",
    "consumer_boundary",
    "context_packet_status",
    "provider_boundary_status",
    "provider_execution_status",
)

_CONTEXT_PACKET_REQUIRED_FALSE_FIELDS = (
    "contains_raw_prompt",
    "contains_free_form_facts",
    "contains_raw_retrieval_dump",
    "retrieval_can_define_source_truth",
    "context_can_define_execution_truth",
    "context_can_authorize_state_mutation",
    "context_can_authorize_ai_approval",
    "provider_execution_enabled",
    "prompt_execution_enabled",
)

_PROHIBITED_CONTEXT_PACKET_FIELDS = (
    "raw_prompt",
    "free_form_prompt",
    "untracked_fact",
    "untracked_facts",
    "raw_retrieval_dump",
    "raw_retrieval_chunks",
    "anonymous_chunk",
    "messages",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "api_key",
    "provider_sdk_client",
    "raw_provider_payload",
    "state_mutation_payload",
    "approval_payload",
)


def build_ai_context_packet_baseline() -> dict[str, Any]:
    """Return M31.4 provider-facing context packet rules."""
    return {
        "checkpoint": AI_CONTEXT_PACKET_CHECKPOINT_ID,
        "contract_version": AI_CONTEXT_PACKET_CONTRACT_VERSION,
        "context_packet_status": AI_CONTEXT_PACKET_STATUS_VALIDATED,
        "supported_assistance_modes": list(SUPPORTED_ASSISTANCE_MODES),
        "supported_context_families": list(SUPPORTED_CONTEXT_PACKET_FAMILIES),
        "supported_authority_statuses": list(SUPPORTED_AUTHORITY_STATUSES),
        "required_packet_rules": [
            "source_refs_must_be_version_pinned",
            "limitations_must_be_visible",
            "retrieval_context_must_remain_support_only",
            "free_form_prompt_facts_are_blocked",
            "raw_retrieval_dumps_are_blocked",
            "provider_execution_remains_blocked",
        ],
        "not_owned_by_m31_4": [
            "real_provider_calls",
            "local_model_inference",
            "prompt_execution",
            "refusal_rule_execution",
            "output_acceptance",
            "evaluation_harness",
            "app_coupled_heavy_use_testing",
        ],
    }


def build_ai_context_packet_item(
    *,
    context_item_id: str,
    source_ref: str,
    source_family: str,
    source_role: str,
    authority_status: str,
    evidence_status: str,
    limitation_summary: str,
    allowed_use: str,
    blocked_use: str,
) -> dict[str, object]:
    """Build and validate one M31.4 context packet item."""
    item = {
        "context_item_id": _require_non_empty_string(
            context_item_id,
            field_name="context_item_id",
            error_prefix="AI context packet item",
        ),
        "source_ref": _parse_version_pinned_ref(source_ref, field_name="source_ref"),
        "source_family": _normalize_supported_value(
            source_family,
            field_name="source_family",
            supported_values=SUPPORTED_CONTEXT_PACKET_FAMILIES,
            error_prefix="AI context packet item",
        ),
        "source_role": _normalize_supported_value(
            source_role,
            field_name="source_role",
            supported_values=(
                AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
                GOVERNED_ENGINE_INPUT_ROLE,
                GOVERNED_CONTRACT_ROLE,
                NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
            ),
            error_prefix="AI context packet item",
        ),
        "authority_status": _normalize_supported_value(
            authority_status,
            field_name="authority_status",
            supported_values=SUPPORTED_AUTHORITY_STATUSES,
            error_prefix="AI context packet item",
        ),
        "evidence_status": _require_non_empty_string(
            evidence_status,
            field_name="evidence_status",
            error_prefix="AI context packet item",
        ),
        "limitation_summary": _require_non_empty_string(
            limitation_summary,
            field_name="limitation_summary",
            error_prefix="AI context packet item",
        ),
        "allowed_use": _require_non_empty_string(
            allowed_use,
            field_name="allowed_use",
            error_prefix="AI context packet item",
        ),
        "blocked_use": _require_non_empty_string(
            blocked_use,
            field_name="blocked_use",
            error_prefix="AI context packet item",
        ),
    }
    validate_ai_context_packet_item(item)
    return item


def validate_ai_context_packet_item(item: dict[str, object]) -> None:
    """Validate one M31.4 context packet item."""
    _validate_prohibited_fields(item, _PROHIBITED_CONTEXT_PACKET_FIELDS)
    _validate_required_string_fields(
        item,
        _CONTEXT_PACKET_ITEM_REQUIRED_STRING_FIELDS,
        error_prefix="AI context packet item",
    )
    source_family = _normalize_supported_value(
        item["source_family"],
        field_name="source_family",
        supported_values=SUPPORTED_CONTEXT_PACKET_FAMILIES,
        error_prefix="AI context packet item",
    )
    source_role = _normalize_supported_value(
        item["source_role"],
        field_name="source_role",
        supported_values=(
            AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
            GOVERNED_ENGINE_INPUT_ROLE,
            GOVERNED_CONTRACT_ROLE,
            NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
        ),
        error_prefix="AI context packet item",
    )
    authority_status = _normalize_supported_value(
        item["authority_status"],
        field_name="authority_status",
        supported_values=SUPPORTED_AUTHORITY_STATUSES,
        error_prefix="AI context packet item",
    )
    _parse_version_pinned_ref(item["source_ref"], field_name="source_ref")

    if source_family == RETRIEVAL_RESULT_CONTEXT_FAMILY:
        if source_role != NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE:
            raise ValueError("Retrieval context packet items must be support-only.")
        if authority_status != SUPPORT_ONLY_AUTHORITY_STATUS:
            raise ValueError("Retrieval context packet items cannot declare source authority.")
    if source_role == NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE:
        if authority_status == AUTHORIZED_SOURCE_AUTHORITY_STATUS:
            raise ValueError("Support context cannot declare authorized source authority.")


def build_ai_context_packet(
    *,
    context_packet_id: str,
    assistance_mode: str,
    provider_boundary_request: dict[str, object],
    context_items: list[dict[str, object]],
    standards_registry_ref: str | None = None,
) -> dict[str, object]:
    """Build and validate a provider-facing context packet."""
    validate_ai_provider_adapter_boundary_request(provider_boundary_request)
    packet = {
        "checkpoint": AI_CONTEXT_PACKET_CHECKPOINT_ID,
        "contract_version": AI_CONTEXT_PACKET_CONTRACT_VERSION,
        "context_packet_id": _require_non_empty_string(
            context_packet_id,
            field_name="context_packet_id",
            error_prefix="AI context packet",
        ),
        "assistance_mode": _normalize_supported_value(
            assistance_mode,
            field_name="assistance_mode",
            supported_values=SUPPORTED_ASSISTANCE_MODES,
            error_prefix="AI context packet",
        ),
        "consumer_boundary": str(provider_boundary_request["adapter_request_id"]),
        "context_packet_status": AI_CONTEXT_PACKET_STATUS_VALIDATED,
        "provider_boundary_status": str(provider_boundary_request["boundary_status"]),
        "provider_execution_status": str(
            provider_boundary_request["provider_execution_status"]
        ),
        "provider_kind": str(provider_boundary_request["provider_kind"]),
        "context_items": list(context_items),
        "standards_registry_ref": (
            _parse_version_pinned_ref(
                standards_registry_ref,
                field_name="standards_registry_ref",
            )
            if standards_registry_ref is not None
            else None
        ),
        "contains_raw_prompt": False,
        "contains_free_form_facts": False,
        "contains_raw_retrieval_dump": False,
        "retrieval_can_define_source_truth": False,
        "context_can_define_execution_truth": False,
        "context_can_authorize_state_mutation": False,
        "context_can_authorize_ai_approval": False,
        "provider_execution_enabled": False,
        "prompt_execution_enabled": False,
        "limitation_visibility_policy": "every_context_item_must_declare_limitation_summary",
        "retrieval_policy": "retrieval_context_is_support_only_non_authoritative",
        "prompt_policy": "free_form_prompt_with_untracked_facts_is_blocked",
    }
    validate_ai_context_packet(packet)
    return packet


def validate_ai_context_packet(packet: dict[str, object]) -> None:
    """Validate a provider-facing M31.4 context packet."""
    _validate_prohibited_fields(packet, _PROHIBITED_CONTEXT_PACKET_FIELDS)
    _validate_required_string_fields(
        packet,
        _CONTEXT_PACKET_REQUIRED_STRING_FIELDS,
        error_prefix="AI context packet",
    )
    _validate_expected_exact_value(
        packet,
        field_name="checkpoint",
        expected_value=AI_CONTEXT_PACKET_CHECKPOINT_ID,
        error_prefix="AI context packet",
    )
    _validate_expected_exact_value(
        packet,
        field_name="contract_version",
        expected_value=AI_CONTEXT_PACKET_CONTRACT_VERSION,
        error_prefix="AI context packet",
    )
    _validate_expected_exact_value(
        packet,
        field_name="context_packet_status",
        expected_value=AI_CONTEXT_PACKET_STATUS_VALIDATED,
        error_prefix="AI context packet",
    )
    _validate_expected_exact_value(
        packet,
        field_name="provider_boundary_status",
        expected_value=AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
        error_prefix="AI context packet",
    )
    _validate_expected_exact_value(
        packet,
        field_name="provider_execution_status",
        expected_value=PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
        error_prefix="AI context packet",
    )
    _validate_expected_exact_value(
        packet,
        field_name="provider_kind",
        expected_value=DISABLED_PROVIDER_KIND,
        error_prefix="AI context packet",
    )
    _normalize_supported_value(
        packet["assistance_mode"],
        field_name="assistance_mode",
        supported_values=SUPPORTED_ASSISTANCE_MODES,
        error_prefix="AI context packet",
    )
    for field_name in _CONTEXT_PACKET_REQUIRED_FALSE_FIELDS:
        if packet.get(field_name) is not False:
            raise ValueError(f"AI context packet requires {field_name} to be False.")

    standards_registry_ref = packet.get("standards_registry_ref")
    if standards_registry_ref is not None:
        _parse_version_pinned_ref(
            standards_registry_ref,
            field_name="standards_registry_ref",
        )

    context_items = packet.get("context_items")
    if not isinstance(context_items, list) or not context_items:
        raise ValueError("AI context packet must declare non-empty context_items.")

    item_ids: list[str] = []
    for item in context_items:
        if not isinstance(item, dict):
            raise ValueError("AI context packet context_items must contain dicts.")
        validate_ai_context_packet_item(item)
        item_ids.append(str(item["context_item_id"]))
    _reject_duplicates(item_ids, field_name="context_item_id")


def _parse_version_pinned_ref(raw_ref: object, *, field_name: str) -> str:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="AI context packet ref",
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
                f"{field_name} is not allowed in M31.4 context packets."
            )


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate value in {field_name}: {value!r}.")
        seen.add(value)
