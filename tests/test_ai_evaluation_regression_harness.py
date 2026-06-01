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
from asbp.ai_runtime.evaluation_harness import (
    AI_EVALUATION_HARNESS_CHECKPOINT_ID,
    AI_EVALUATION_HARNESS_STATUS_VALIDATED,
    AI_PROVIDER_SMOKE_STATUS_BLOCKED,
    AI_PROVIDER_SMOKE_STATUS_READY,
    AI_PROVIDER_SMOKE_STATUS_SKIPPED,
    LOCAL_PROVIDER_SMOKE_KIND,
    REGRESSION_CASE_CONTEXT_PACKET,
    REGRESSION_CASE_OUTPUT_ACCEPTANCE,
    REGRESSION_CASE_PROVIDER_BOUNDARY,
    REGRESSION_CASE_PROVIDER_SMOKE,
    REGRESSION_CASE_REFUSAL_LIMITATION,
    REGRESSION_FAIL_CLOSED_STATUS,
    REGRESSION_PASS_STATUS,
    build_ai_evaluation_harness_baseline,
    build_ai_evaluation_regression_result,
    build_ai_provider_smoke_request,
    build_ai_regression_case,
    validate_ai_evaluation_regression_result,
    validate_ai_provider_smoke_request,
    validate_ai_regression_case,
)
from asbp.ai_runtime.output_acceptance import (
    HUMAN_ACCEPT_DECISION,
    HUMAN_ACCEPTED_OUTPUT_STATE,
    HUMAN_AUTHORED_REVIEW_OUTPUT_ORIGIN,
    build_ai_output_artifact,
    build_ai_output_review_decision,
)
from asbp.ai_runtime.provider_contracts import (
    build_ai_provider_adapter_boundary_request,
)
from asbp.ai_runtime.refusal_rules import (
    LIMITED_ANSWER_DECISION,
    RETRIEVAL_SUPPORT_ONLY_TRIGGER,
    build_ai_refusal_limitation_decision,
    build_ai_refusal_trigger_from_context_item,
)


def _provider_boundary_request() -> dict[str, object]:
    return build_ai_provider_adapter_boundary_request(
        adapter_request_id="AIPROV-M317-EVAL",
    )


def _product_source_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-PRODUCT-M317",
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
        context_item_id="CTX-RETRIEVAL-M317",
        source_ref="RETRIEVAL-RESULT-M317@v1",
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
        context_packet_id="CTX-PACKET-M317",
        assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
        provider_boundary_request=_provider_boundary_request(),
        context_items=[_product_source_item(), _retrieval_item()],
    )


def _refusal_decision() -> dict[str, object]:
    trigger = build_ai_refusal_trigger_from_context_item(
        trigger_id="REF-M317-RETRIEVAL-LIMIT",
        context_item=_retrieval_item(),
        trigger_kind=RETRIEVAL_SUPPORT_ONLY_TRIGGER,
        decision=LIMITED_ANSWER_DECISION,
        reason="Retrieval is support-only and cannot define source truth.",
    )
    return build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-M317",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )


def _output_review_decision() -> dict[str, object]:
    refusal_decision = _refusal_decision()
    artifact = build_ai_output_artifact(
        output_artifact_id="OUT-M317-HUMAN-ACCEPTED",
        output_origin=HUMAN_AUTHORED_REVIEW_OUTPUT_ORIGIN,
        output_state=HUMAN_ACCEPTED_OUTPUT_STATE,
        refusal_decision=refusal_decision,
        limitation_summary="Human review accepted limited advisory output only.",
        allowed_use="May be used as reviewed advisory evidence.",
        blocked_use="Must not approve, release, certify, or claim customer readiness.",
        output_ref="OUT-M317@v1",
        human_review_evidence_ref="HUMAN-REVIEW-M317@v1",
    )
    return build_ai_output_review_decision(
        review_decision_id="REVIEW-M317-HUMAN-ACCEPT",
        output_artifact=artifact,
        review_decision=HUMAN_ACCEPT_DECISION,
        reviewer_ref="project-owner",
        review_evidence_ref="HUMAN-REVIEW-M317@v1",
    )


def _regression_cases() -> list[dict[str, object]]:
    return [
        build_ai_regression_case(
            case_id="CASE-M317-CONTEXT",
            case_kind=REGRESSION_CASE_CONTEXT_PACKET,
            description="M31.4 context packet dependency remains required.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_context_packet_contract.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M317-REFUSAL",
            case_kind=REGRESSION_CASE_REFUSAL_LIMITATION,
            description="M31.5 refusal and limitation dependency remains required.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_refusal_limitation_rules.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M317-OUTPUT",
            case_kind=REGRESSION_CASE_OUTPUT_ACCEPTANCE,
            description="M31.6 output acceptance and review dependency remains required.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_output_acceptance_review_rules.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M317-PROVIDER-BOUNDARY",
            case_kind=REGRESSION_CASE_PROVIDER_BOUNDARY,
            description="M31.3 provider boundary remains blocked by default.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_provider_adapter_boundary.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M317-SMOKE-GATE",
            case_kind=REGRESSION_CASE_PROVIDER_SMOKE,
            description="Provider/local smoke is disabled by default and explicitly gated.",
            expected_status=REGRESSION_FAIL_CLOSED_STATUS,
            evidence_ref="M31.7 smoke gate",
        ),
    ]


def test_evaluation_harness_baseline_exposes_m31_7_rules() -> None:
    baseline = build_ai_evaluation_harness_baseline()

    assert baseline["checkpoint"] == AI_EVALUATION_HARNESS_CHECKPOINT_ID
    assert baseline["evaluation_harness_status"] == AI_EVALUATION_HARNESS_STATUS_VALIDATED
    assert REGRESSION_CASE_CONTEXT_PACKET in baseline["supported_regression_case_kinds"]
    assert baseline["provider_smoke_default_status"] == AI_PROVIDER_SMOKE_STATUS_BLOCKED
    assert baseline["m31_8_boundary"] == "app_coupled_heavy_use_shakedown_is_deferred_to_m31_8"


def test_regression_case_rejects_raw_prompt_payloads() -> None:
    case = build_ai_regression_case(
        case_id="CASE-BLOCK-PROMPT",
        case_kind=REGRESSION_CASE_CONTEXT_PACKET,
        description="No raw prompt payloads in harness cases.",
        expected_status=REGRESSION_PASS_STATUS,
        evidence_ref="evidence",
    )
    case["raw_prompt"] = "summarize this freely"

    with pytest.raises(ValueError, match="raw_prompt"):
        validate_ai_regression_case(case)


def test_provider_smoke_is_blocked_by_default() -> None:
    smoke = build_ai_provider_smoke_request(
        smoke_request_id="SMOKE-M317-BLOCKED",
        provider_boundary_request=_provider_boundary_request(),
    )

    assert smoke["smoke_status"] == AI_PROVIDER_SMOKE_STATUS_BLOCKED
    assert smoke["enable_provider_smoke"] is False
    assert smoke["allow_prompt_execution"] is False
    assert smoke["app_coupled_heavy_use_enabled"] is False
    validate_ai_provider_smoke_request(smoke)


def test_provider_smoke_skips_when_prompt_execution_not_enabled() -> None:
    smoke = build_ai_provider_smoke_request(
        smoke_request_id="SMOKE-M317-SKIP",
        provider_boundary_request=_provider_boundary_request(),
        smoke_kind=LOCAL_PROVIDER_SMOKE_KIND,
        enable_provider_smoke=True,
        allow_prompt_execution=False,
    )

    assert smoke["smoke_status"] == AI_PROVIDER_SMOKE_STATUS_SKIPPED
    validate_ai_provider_smoke_request(smoke)


def test_provider_smoke_ready_requires_two_explicit_opt_ins() -> None:
    smoke = build_ai_provider_smoke_request(
        smoke_request_id="SMOKE-M317-READY",
        provider_boundary_request=_provider_boundary_request(),
        smoke_kind=LOCAL_PROVIDER_SMOKE_KIND,
        enable_provider_smoke=True,
        allow_prompt_execution=True,
    )

    assert smoke["smoke_status"] == AI_PROVIDER_SMOKE_STATUS_READY
    assert smoke["provider_execution_status"] == "provider_adapter_execution_blocked"
    validate_ai_provider_smoke_request(smoke)


def test_evaluation_regression_result_accepts_complete_dependency_chain() -> None:
    smoke = build_ai_provider_smoke_request(
        smoke_request_id="SMOKE-M317-BLOCKED-RESULT",
        provider_boundary_request=_provider_boundary_request(),
    )
    result = build_ai_evaluation_regression_result(
        evaluation_result_id="EVAL-M317-COMPLETE",
        context_packet=_context_packet(),
        refusal_decision=_refusal_decision(),
        output_review_decision=_output_review_decision(),
        provider_boundary_request=_provider_boundary_request(),
        regression_cases=_regression_cases(),
        provider_smoke_request=smoke,
    )

    assert result["checkpoint"] == AI_EVALUATION_HARNESS_CHECKPOINT_ID
    assert result["evaluation_status"] == AI_EVALUATION_HARNESS_STATUS_VALIDATED
    assert result["provider_smoke_status"] == AI_PROVIDER_SMOKE_STATUS_BLOCKED
    assert result["app_coupled_heavy_use_enabled"] is False
    assert result["productization_claim_allowed"] is False
    validate_ai_evaluation_regression_result(result)


def test_evaluation_result_requires_all_regression_case_kinds() -> None:
    incomplete_cases = [
        case for case in _regression_cases()
        if case["case_kind"] != REGRESSION_CASE_PROVIDER_SMOKE
    ]

    with pytest.raises(ValueError, match=REGRESSION_CASE_PROVIDER_SMOKE):
        build_ai_evaluation_regression_result(
            evaluation_result_id="EVAL-M317-MISSING-SMOKE",
            context_packet=_context_packet(),
            refusal_decision=_refusal_decision(),
            output_review_decision=_output_review_decision(),
            provider_boundary_request=_provider_boundary_request(),
            regression_cases=incomplete_cases,
        )


def test_evaluation_result_rejects_heavy_use_and_productization_flags() -> None:
    result = build_ai_evaluation_regression_result(
        evaluation_result_id="EVAL-M317-FLAGS",
        context_packet=_context_packet(),
        refusal_decision=_refusal_decision(),
        output_review_decision=_output_review_decision(),
        provider_boundary_request=_provider_boundary_request(),
        regression_cases=_regression_cases(),
    )

    for field_name in (
        "app_coupled_heavy_use_enabled",
        "ui_api_behavior_enabled",
        "productization_claim_allowed",
        "customer_ready_output_claim_allowed",
        "ai_approval_authority_allowed",
        "model_owned_state_mutation_allowed",
        "retrieval_as_source_truth_allowed",
    ):
        mutated = dict(result)
        mutated[field_name] = True
        with pytest.raises(ValueError, match=field_name):
            validate_ai_evaluation_regression_result(mutated)


def test_evaluation_result_rejects_provider_payloads_and_model_output() -> None:
    result = build_ai_evaluation_regression_result(
        evaluation_result_id="EVAL-M317-PROHIBITED",
        context_packet=_context_packet(),
        refusal_decision=_refusal_decision(),
        output_review_decision=_output_review_decision(),
        provider_boundary_request=_provider_boundary_request(),
        regression_cases=_regression_cases(),
    )

    for field_name in (
        "api_key",
        "raw_provider_payload",
        "raw_provider_response",
        "model_output",
        "generated_final_output",
        "state_mutation_payload",
        "approval_payload",
    ):
        mutated = dict(result)
        mutated[field_name] = "blocked"
        with pytest.raises(ValueError, match=field_name):
            validate_ai_evaluation_regression_result(mutated)
