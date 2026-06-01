import pytest

from asbp.ai_runtime.provider_adapter import (
    AIProviderExecutionBlocked,
    DisabledAIProviderAdapter,
)
from asbp.ai_runtime.provider_contracts import (
    AI_PROVIDER_ADAPTER_BOUNDARY_CHECKPOINT_ID,
    AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED,
    DISABLED_PROVIDER_KIND,
    EXTERNAL_API_PROVIDER_KIND,
    LOCAL_OFFLINE_PROVIDER_KIND,
    PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS,
    build_ai_provider_adapter_boundary_baseline,
    build_ai_provider_adapter_boundary_request,
    validate_ai_provider_adapter_boundary_request,
)
from asbp.ai_runtime.provider_registry import build_ai_provider_adapter_registry


def test_provider_adapter_boundary_baseline_exposes_m31_3_rules() -> None:
    baseline = build_ai_provider_adapter_boundary_baseline()

    assert baseline["checkpoint"] == AI_PROVIDER_ADAPTER_BOUNDARY_CHECKPOINT_ID
    assert baseline["boundary_status"] == AI_PROVIDER_ADAPTER_BOUNDARY_STATUS_VALIDATED
    assert "provider_neutral_boundary_contracts" in baseline["allowed_m31_3_build_scope"]
    assert "real_provider_calls" in baseline["blocked_m31_3_runtime_scope"]
    assert "no_direct_model_calls_from_core_or_ui" in baseline["boundary_rules"]
    assert "no_raw_provider_payload_leakage" in baseline["boundary_rules"]


def test_build_provider_adapter_boundary_request_accepts_disabled_boundary_only() -> None:
    request = build_ai_provider_adapter_boundary_request(
        adapter_request_id="AIPROV-DISABLED-001",
    )

    assert request["checkpoint"] == AI_PROVIDER_ADAPTER_BOUNDARY_CHECKPOINT_ID
    assert request["provider_kind"] == DISABLED_PROVIDER_KIND
    assert request["provider_execution_status"] == PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS
    assert request["direct_model_call_enabled"] is False
    assert request["prompt_execution_enabled"] is False
    assert request["provider_credentials_present"] is False
    assert request["raw_provider_payload_allowed"] is False
    assert request["model_state_mutation_allowed"] is False
    assert request["core_ui_direct_call_allowed"] is False
    assert request["context_packet_contract_required"] is True
    assert request["refusal_limitation_rules_required"] is True
    assert request["output_acceptance_rules_required"] is True
    assert request["evaluation_validation_required"] is True
    validate_ai_provider_adapter_boundary_request(request)


def test_strategy_candidate_provider_kinds_do_not_enable_execution() -> None:
    for provider_kind in (LOCAL_OFFLINE_PROVIDER_KIND, EXTERNAL_API_PROVIDER_KIND):
        request = build_ai_provider_adapter_boundary_request(
            adapter_request_id=f"AIPROV-{provider_kind}",
            provider_kind=provider_kind,
        )

        assert request["provider_kind"] == provider_kind
        assert request["provider_execution_status"] == PROVIDER_ADAPTER_EXECUTION_BLOCKED_STATUS
        assert request["provider_implementation_status"] == "strategy_candidate_only"
        assert request["direct_model_call_enabled"] is False
        assert request["prompt_execution_enabled"] is False
        validate_ai_provider_adapter_boundary_request(request)


def test_provider_adapter_boundary_rejects_prompt_provider_and_secret_fields() -> None:
    prohibited_fields = {
        "api_key": "secret-key",
        "raw_prompt": "Write a CQV protocol",
        "messages": [{"role": "user", "content": "hello"}],
        "model_name": "real-model",
        "provider_sdk_client": object(),
        "raw_provider_response": {"text": "provider output"},
        "local_model_path": "/models/local-model.gguf",
    }

    for field_name, value in prohibited_fields.items():
        request = build_ai_provider_adapter_boundary_request(
            adapter_request_id=f"AIPROV-BLOCK-{field_name}",
        )
        request[field_name] = value

        with pytest.raises(ValueError, match=field_name):
            validate_ai_provider_adapter_boundary_request(request)


def test_provider_adapter_boundary_rejects_enabled_model_or_state_mutation_flags() -> None:
    true_fields = (
        "direct_model_call_enabled",
        "prompt_execution_enabled",
        "provider_credentials_present",
        "raw_provider_payload_allowed",
        "raw_provider_response_leakage_allowed",
        "model_state_mutation_allowed",
        "core_ui_direct_call_allowed",
        "autonomous_execution_allowed",
        "retrieval_as_source_truth_allowed",
        "ai_approval_authority_allowed",
    )

    for field_name in true_fields:
        request = build_ai_provider_adapter_boundary_request(
            adapter_request_id=f"AIPROV-BLOCK-{field_name}",
        )
        request[field_name] = True

        with pytest.raises(ValueError, match=field_name):
            validate_ai_provider_adapter_boundary_request(request)


def test_provider_adapter_boundary_requires_later_dependency_gates() -> None:
    dependency_fields = (
        "context_packet_contract_required",
        "refusal_limitation_rules_required",
        "output_acceptance_rules_required",
        "evaluation_validation_required",
    )

    for field_name in dependency_fields:
        request = build_ai_provider_adapter_boundary_request(
            adapter_request_id=f"AIPROV-DEPENDENCY-{field_name}",
        )
        request[field_name] = False

        with pytest.raises(ValueError, match=field_name):
            validate_ai_provider_adapter_boundary_request(request)


def test_disabled_provider_adapter_builds_boundary_request_but_blocks_execution() -> None:
    adapter = DisabledAIProviderAdapter()
    request = adapter.build_boundary_request(adapter_request_id="AIPROV-DISABLED-EXEC")

    assert request["provider_kind"] == DISABLED_PROVIDER_KIND

    with pytest.raises(AIProviderExecutionBlocked, match="real provider calls"):
        adapter.execute(request)


def test_provider_registry_exposes_only_disabled_executable_adapter() -> None:
    registry = build_ai_provider_adapter_registry()

    assert registry.available_provider_kinds() == (DISABLED_PROVIDER_KIND,)
    assert isinstance(registry.get(DISABLED_PROVIDER_KIND), DisabledAIProviderAdapter)

    with pytest.raises(ValueError, match="strategy-only"):
        registry.get(LOCAL_OFFLINE_PROVIDER_KIND)

    with pytest.raises(ValueError, match="strategy-only"):
        registry.get(EXTERNAL_API_PROVIDER_KIND)

    with pytest.raises(ValueError, match="Unsupported provider_kind"):
        registry.get("unapproved_provider")
