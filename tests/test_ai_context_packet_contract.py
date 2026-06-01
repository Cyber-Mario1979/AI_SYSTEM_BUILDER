import pytest

from asbp.ai_runtime.context_packaging import (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    GOVERNED_CONTRACT_ROLE,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
)
from asbp.ai_runtime.context_packets import (
    ADVISORY_QA_ASSISTANCE_MODE,
    AI_CONTEXT_PACKET_CHECKPOINT_ID,
    AI_CONTEXT_PACKET_STATUS_VALIDATED,
    AUTHORIZED_SOURCE_AUTHORITY_STATUS,
    LIMITED_SOURCE_AUTHORITY_STATUS,
    PRODUCT_SOURCE_CONTEXT_FAMILY,
    RETRIEVAL_RESULT_CONTEXT_FAMILY,
    STANDARDS_REGISTRY_CONTEXT_FAMILY,
    SUPPORT_ONLY_AUTHORITY_STATUS,
    TASK_WORKFLOW_STATE_CONTEXT_FAMILY,
    build_ai_context_packet,
    build_ai_context_packet_baseline,
    build_ai_context_packet_item,
    validate_ai_context_packet,
    validate_ai_context_packet_item,
)
from asbp.ai_runtime.provider_contracts import (
    DISABLED_PROVIDER_KIND,
    build_ai_provider_adapter_boundary_request,
)


def _provider_boundary_request() -> dict[str, object]:
    return build_ai_provider_adapter_boundary_request(
        adapter_request_id="AIPROV-M314-CONTEXT",
    )


def _product_source_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-PRODUCT-001",
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
        context_item_id="CTX-STANDARDS-001",
        source_ref="STANDARDS-REGISTRY@v1",
        source_family=STANDARDS_REGISTRY_CONTEXT_FAMILY,
        source_role=GOVERNED_CONTRACT_ROLE,
        authority_status=LIMITED_SOURCE_AUTHORITY_STATUS,
        evidence_status="limited",
        limitation_summary="Registry limitations and citation depth must remain visible.",
        allowed_use="May provide standards registry status and limitations.",
        blocked_use="Must not create clause-level or legal authority.",
    )


def _workflow_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-WORKFLOW-001",
        source_ref="TASK-WORKFLOW-STATE@v1",
        source_family=TASK_WORKFLOW_STATE_CONTEXT_FAMILY,
        source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
        authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
        evidence_status="validated",
        limitation_summary="Workflow state is a snapshot only.",
        allowed_use="May describe current workflow/task state.",
        blocked_use="Must not allow model-owned state mutation.",
    )


def _retrieval_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-RETRIEVAL-001",
        source_ref="RETRIEVAL-RESULT-001@v1",
        source_family=RETRIEVAL_RESULT_CONTEXT_FAMILY,
        source_role=NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
        authority_status=SUPPORT_ONLY_AUTHORITY_STATUS,
        evidence_status="partial",
        limitation_summary="Retrieval result is helper-only and non-authoritative.",
        allowed_use="May help locate source-backed context.",
        blocked_use="Must not define compliance truth or source authority.",
    )


def test_context_packet_baseline_exposes_m31_4_rules() -> None:
    baseline = build_ai_context_packet_baseline()

    assert baseline["checkpoint"] == AI_CONTEXT_PACKET_CHECKPOINT_ID
    assert baseline["context_packet_status"] == AI_CONTEXT_PACKET_STATUS_VALIDATED
    assert "source_refs_must_be_version_pinned" in baseline["required_packet_rules"]
    assert "free_form_prompt_facts_are_blocked" in baseline["required_packet_rules"]
    assert "raw_retrieval_dumps_are_blocked" in baseline["required_packet_rules"]
    assert "real_provider_calls" in baseline["not_owned_by_m31_4"]


def test_build_context_packet_accepts_versioned_sources_and_visible_limits() -> None:
    packet = build_ai_context_packet(
        context_packet_id="CTX-PACKET-001",
        assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
        provider_boundary_request=_provider_boundary_request(),
        standards_registry_ref="STANDARDS-REGISTRY@v1",
        context_items=[
            _product_source_item(),
            _standards_item(),
            _workflow_item(),
            _retrieval_item(),
        ],
    )

    assert packet["checkpoint"] == AI_CONTEXT_PACKET_CHECKPOINT_ID
    assert packet["context_packet_status"] == AI_CONTEXT_PACKET_STATUS_VALIDATED
    assert packet["provider_kind"] == DISABLED_PROVIDER_KIND
    assert packet["provider_execution_enabled"] is False
    assert packet["prompt_execution_enabled"] is False
    assert packet["contains_raw_prompt"] is False
    assert packet["contains_raw_retrieval_dump"] is False
    assert packet["retrieval_can_define_source_truth"] is False
    validate_ai_context_packet(packet)


def test_context_packet_item_rejects_unversioned_source_ref() -> None:
    with pytest.raises(ValueError, match="exactly one '@'"):
        build_ai_context_packet_item(
            context_item_id="CTX-UNVERSIONED",
            source_ref="PRODUCT-SOURCE-CQV",
            source_family=PRODUCT_SOURCE_CONTEXT_FAMILY,
            source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
            authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
            evidence_status="validated",
            limitation_summary="Limitations visible.",
            allowed_use="Allowed.",
            blocked_use="Blocked.",
        )


def test_context_packet_item_requires_limitation_visibility() -> None:
    with pytest.raises(ValueError, match="limitation_summary"):
        build_ai_context_packet_item(
            context_item_id="CTX-NO-LIMITS",
            source_ref="PRODUCT-SOURCE-CQV@v1",
            source_family=PRODUCT_SOURCE_CONTEXT_FAMILY,
            source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
            authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
            evidence_status="validated",
            limitation_summary="",
            allowed_use="Allowed.",
            blocked_use="Blocked.",
        )


def test_retrieval_context_must_remain_support_only() -> None:
    with pytest.raises(ValueError, match="support-only"):
        build_ai_context_packet_item(
            context_item_id="CTX-RETRIEVAL-BAD-ROLE",
            source_ref="RETRIEVAL-RESULT-001@v1",
            source_family=RETRIEVAL_RESULT_CONTEXT_FAMILY,
            source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
            authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
            evidence_status="partial",
            limitation_summary="Retrieval limitations visible.",
            allowed_use="Allowed.",
            blocked_use="Blocked.",
        )

    with pytest.raises(ValueError, match="cannot declare source authority"):
        build_ai_context_packet_item(
            context_item_id="CTX-RETRIEVAL-BAD-AUTHORITY",
            source_ref="RETRIEVAL-RESULT-001@v1",
            source_family=RETRIEVAL_RESULT_CONTEXT_FAMILY,
            source_role=NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
            authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
            evidence_status="partial",
            limitation_summary="Retrieval limitations visible.",
            allowed_use="Allowed.",
            blocked_use="Blocked.",
        )


def test_context_packet_rejects_free_form_prompt_and_raw_retrieval_fields() -> None:
    prohibited_fields = {
        "raw_prompt": "write a validation plan",
        "free_form_prompt": "summarize this",
        "untracked_facts": ["unsupported fact"],
        "raw_retrieval_dump": "anonymous retrieved text",
        "raw_retrieval_chunks": ["chunk without source id"],
        "messages": [{"role": "user", "content": "hello"}],
        "prompt_template": "template text",
        "api_key": "secret-key",
    }

    for field_name, value in prohibited_fields.items():
        packet = build_ai_context_packet(
            context_packet_id=f"CTX-PACKET-BLOCK-{field_name}",
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            provider_boundary_request=_provider_boundary_request(),
            context_items=[_product_source_item()],
        )
        packet[field_name] = value

        with pytest.raises(ValueError, match=field_name):
            validate_ai_context_packet(packet)


def test_context_packet_rejects_truth_or_execution_flags() -> None:
    true_fields = (
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

    for field_name in true_fields:
        packet = build_ai_context_packet(
            context_packet_id=f"CTX-PACKET-FLAG-{field_name}",
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            provider_boundary_request=_provider_boundary_request(),
            context_items=[_product_source_item()],
        )
        packet[field_name] = True

        with pytest.raises(ValueError, match=field_name):
            validate_ai_context_packet(packet)


def test_context_packet_rejects_duplicate_item_ids() -> None:
    first = _product_source_item()
    duplicate = dict(first)

    with pytest.raises(ValueError, match="Duplicate value in context_item_id"):
        build_ai_context_packet(
            context_packet_id="CTX-PACKET-DUPLICATE",
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            provider_boundary_request=_provider_boundary_request(),
            context_items=[first, duplicate],
        )
