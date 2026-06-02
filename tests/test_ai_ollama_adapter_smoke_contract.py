import pytest

from asbp.ai_runtime.ollama_adapter import (
    M3110A_CHECKPOINT_ID,
    M3110A_DEFAULT_ENDPOINT,
    M3110A_MODEL_NAME,
    M3110A_PROVIDER_KIND,
    M3110A_SMOKE_STATUS_CAPTURED,
    build_bounded_ollama_smoke_baseline,
    build_bounded_ollama_smoke_evidence,
    build_bounded_ollama_smoke_request,
    build_ollama_generate_payload,
    execute_bounded_ollama_smoke,
    validate_bounded_ollama_smoke_evidence,
    validate_bounded_ollama_smoke_request,
)
from asbp.ai_runtime.runtime_shakedown import (
    APPROVED_BOUNDED_RUNTIME_TARGET,
    RUNTIME_TARGET_STATUS_READY,
)


def _ready_request() -> dict[str, object]:
    return build_bounded_ollama_smoke_request(
        smoke_request_id="SMOKE-M3110A-READY",
        enable_local_runtime=True,
        allow_prompt_execution=True,
    )


def _safe_response() -> dict[str, object]:
    return {
        "response": (
            "Draft support only: verify installed HVAC equipment identification, "
            "confirm component location against governed project documents, and "
            "record installation observations for human review. Limitation: this is "
            "simplified demonstration evidence only and requires human review before use."
        ),
        "done": True,
    }


def test_baseline_declares_local_only_no_api_key_policy() -> None:
    baseline = build_bounded_ollama_smoke_baseline()

    assert baseline["checkpoint"] == M3110A_CHECKPOINT_ID
    assert baseline["provider_kind"] == M3110A_PROVIDER_KIND
    assert baseline["model_name"] == M3110A_MODEL_NAME
    assert baseline["default_endpoint_url"] == M3110A_DEFAULT_ENDPOINT
    assert baseline["normal_pytest_requires_ollama"] is False
    assert baseline["api_key_required"] is False
    assert baseline["cloud_provider_call_allowed"] is False


def test_smoke_request_requires_explicit_runtime_and_prompt_opt_in() -> None:
    with pytest.raises(ValueError, match="explicit local runtime opt-in"):
        build_bounded_ollama_smoke_request(
            smoke_request_id="SMOKE-M3110A-NO-RUNTIME",
        )

    with pytest.raises(ValueError, match="explicit prompt execution opt-in"):
        build_bounded_ollama_smoke_request(
            smoke_request_id="SMOKE-M3110A-NO-PROMPT",
            enable_local_runtime=True,
        )

    request = _ready_request()
    assert request["runtime_target"] == APPROVED_BOUNDED_RUNTIME_TARGET
    assert request["runtime_target_status"] == RUNTIME_TARGET_STATUS_READY
    assert request["api_key_required"] is False
    validate_bounded_ollama_smoke_request(request)


def test_smoke_request_rejects_api_keys_cloud_endpoints_and_raw_payloads() -> None:
    request = _ready_request()

    for field_name in (
        "api_key",
        "provider_api_key",
        "openai_api_key",
        "raw_prompt",
        "raw_provider_payload",
        "raw_ollama_response",
        "model_output",
    ):
        mutated = dict(request)
        mutated[field_name] = "blocked"
        with pytest.raises(ValueError, match=field_name):
            validate_bounded_ollama_smoke_request(mutated)

    with pytest.raises(ValueError, match="localhost"):
        build_bounded_ollama_smoke_request(
            smoke_request_id="SMOKE-M3110A-CLOUD-BLOCKED",
            endpoint_url="https://api.example.com/v1/chat/completions",
            enable_local_runtime=True,
            allow_prompt_execution=True,
        )


def test_generate_payload_is_bounded_and_uses_local_model() -> None:
    request = _ready_request()
    payload = build_ollama_generate_payload(request)

    assert payload["model"] == M3110A_MODEL_NAME
    assert payload["stream"] is False
    assert payload["keep_alive"] == "10m"
    assert "Context packet ref" in payload["prompt"]
    assert "Do not claim approval" in payload["prompt"]
    assert "customer readiness" in payload["prompt"]
    assert "api_key" not in payload
    assert "messages" not in payload


def test_execute_smoke_uses_injected_post_json_without_requiring_ollama() -> None:
    request = _ready_request()
    calls: list[tuple[str, dict[str, object]]] = []

    def fake_post_json(endpoint_url: str, payload: dict[str, object]) -> dict[str, object]:
        calls.append((endpoint_url, payload))
        return _safe_response()

    evidence = execute_bounded_ollama_smoke(request, post_json=fake_post_json)

    assert calls
    assert calls[0][0] == M3110A_DEFAULT_ENDPOINT
    assert calls[0][1]["model"] == M3110A_MODEL_NAME
    assert evidence["result_status"] == M3110A_SMOKE_STATUS_CAPTURED
    assert evidence["api_key_required"] is False
    assert evidence["cloud_provider_call_allowed"] is False
    assert evidence["output_review_state"] == "human_review_required_before_use"
    validate_bounded_ollama_smoke_evidence(evidence)


def test_evidence_rejects_forbidden_claims_and_fails_closed() -> None:
    request = _ready_request()
    evidence = build_bounded_ollama_smoke_evidence(
        smoke_run_id="RUN-M3110A-FORBIDDEN",
        request=request,
        response={
            "response": "This checklist is approved and compliance is confirmed.",
        },
    )

    assert evidence["result_status"] == "fail_closed_for_forbidden_claims"
    assert "approved" in evidence["forbidden_terms_detected"]
    assert "compliance is confirmed" in evidence["forbidden_terms_detected"]
    assert evidence["output_review_state"] == "requires_correction_before_acceptance"
    validate_bounded_ollama_smoke_evidence(evidence)


def test_evidence_rejects_raw_model_output_and_productization_flags() -> None:
    evidence = build_bounded_ollama_smoke_evidence(
        smoke_run_id="RUN-M3110A-SAFE",
        request=_ready_request(),
        response=_safe_response(),
    )

    for field_name in (
        "raw_provider_response",
        "raw_ollama_response",
        "model_output",
        "customer_ready_output_payload",
    ):
        mutated = dict(evidence)
        mutated[field_name] = "blocked"
        with pytest.raises(ValueError, match=field_name):
            validate_bounded_ollama_smoke_evidence(mutated)

    for field_name in (
        "productization_claim_allowed",
        "customer_ready_output_claim_allowed",
        "commercialization_launch_planning_allowed",
        "ui_api_behavior_enabled",
    ):
        mutated = dict(evidence)
        mutated[field_name] = True
        with pytest.raises(ValueError, match=field_name):
            validate_bounded_ollama_smoke_evidence(mutated)
