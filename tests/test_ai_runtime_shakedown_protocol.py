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
    AI_PROVIDER_SMOKE_STATUS_BLOCKED,
    REGRESSION_CASE_CONTEXT_PACKET,
    REGRESSION_CASE_OUTPUT_ACCEPTANCE,
    REGRESSION_CASE_PROVIDER_BOUNDARY,
    REGRESSION_CASE_PROVIDER_SMOKE,
    REGRESSION_CASE_REFUSAL_LIMITATION,
    REGRESSION_FAIL_CLOSED_STATUS,
    REGRESSION_PASS_STATUS,
    build_ai_evaluation_regression_result,
    build_ai_provider_smoke_request,
    build_ai_regression_case,
)
from asbp.ai_runtime.output_acceptance import (
    HUMAN_AUTHORED_REVIEW_OUTPUT_ORIGIN,
    HUMAN_REVIEWED_OUTPUT_STATE,
    HUMAN_REVIEW_DECISION,
    build_ai_output_review_artifact,
    build_ai_output_review_decision,
)
from asbp.ai_runtime.provider_contracts import build_ai_provider_adapter_boundary_request
from asbp.ai_runtime.refusal_rules import (
    LIMITED_ANSWER_DECISION,
    RETRIEVAL_SUPPORT_ONLY_TRIGGER,
    build_ai_refusal_limitation_decision,
    build_ai_refusal_trigger_from_context_item,
)
from asbp.ai_runtime.runtime_shakedown import (
    AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID,
    AI_RUNTIME_SHAKEDOWN_STATUS_VALIDATED,
    APPROVED_BOUNDED_RUNTIME_TARGET,
    DISABLED_RUNTIME_TARGET,
    LOCAL_RUNTIME_CANDIDATE_TARGET,
    RUNTIME_TARGET_STATUS_DISABLED,
    RUNTIME_TARGET_STATUS_READY,
    RUNTIME_TARGET_STATUS_SKIPPED,
    SCENARIO_ADVISORY_QA,
    SCENARIO_DRAFT_OUTPUT_SUPPORT,
    SCENARIO_HUMAN_REVIEW_REQUIRED,
    SCENARIO_MISSING_SOURCE_REFUSAL,
    SCENARIO_RETRIEVAL_LIMITED,
    SHAKEDOWN_RESULT_EVIDENCE_CAPTURED,
    SHAKEDOWN_RESULT_FAIL_CLOSED,
    STOP_MISSING_CONTEXT_PACKET,
    STOP_NONE_EXPECTED,
    build_ai_runtime_shakedown_baseline,
    build_ai_runtime_shakedown_evidence,
    build_ai_runtime_shakedown_protocol,
    build_ai_runtime_shakedown_scenario,
    build_ai_runtime_target_descriptor,
    validate_ai_runtime_shakedown_evidence,
    validate_ai_runtime_shakedown_protocol,
    validate_ai_runtime_shakedown_scenario,
    validate_ai_runtime_target_descriptor,
)


def _provider_boundary_request() -> dict[str, object]:
    return build_ai_provider_adapter_boundary_request(
        adapter_request_id="AIPROV-M318-SHAKEDOWN",
    )


def _product_source_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-PRODUCT-M318",
        source_ref="PRODUCT-SOURCE-CQV@v1",
        source_family=PRODUCT_SOURCE_CONTEXT_FAMILY,
        source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
        authority_status=AUTHORIZED_SOURCE_AUTHORITY_STATUS,
        evidence_status="validated",
        limitation_summary="Authoritative only for approved M31.8 shakedown scope.",
        allowed_use="May provide governed product-source facts.",
        blocked_use="Must not authorize release, approval, or provider execution.",
    )


def _retrieval_item() -> dict[str, object]:
    return build_ai_context_packet_item(
        context_item_id="CTX-RETRIEVAL-M318",
        source_ref="RETRIEVAL-RESULT-M318@v1",
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
        context_packet_id="CTX-PACKET-M318",
        assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
        provider_boundary_request=_provider_boundary_request(),
        context_items=[_product_source_item(), _retrieval_item()],
    )


def _refusal_decision() -> dict[str, object]:
    trigger = build_ai_refusal_trigger_from_context_item(
        trigger_id="REF-M318-RETRIEVAL-LIMIT",
        context_item=_retrieval_item(),
        trigger_kind=RETRIEVAL_SUPPORT_ONLY_TRIGGER,
        decision=LIMITED_ANSWER_DECISION,
        reason="Retrieval is support-only and cannot define source truth.",
    )
    return build_ai_refusal_limitation_decision(
        refusal_decision_id="REF-DECISION-M318",
        context_packet=_context_packet(),
        trigger_items=[trigger],
    )


def _output_review_decision() -> dict[str, object]:
    refusal_decision = _refusal_decision()
    artifact = build_ai_output_review_artifact(
        output_artifact_id="OUT-M318-HUMAN-REVIEWED",
        output_origin=HUMAN_AUTHORED_REVIEW_OUTPUT_ORIGIN,
        output_state=HUMAN_REVIEWED_OUTPUT_STATE,
        refusal_decision=refusal_decision,
        limitation_summary="Human reviewed limited advisory output only.",
        allowed_use="May be used as reviewed advisory evidence.",
        blocked_use="Must not approve, release, certify, or claim customer readiness.",
        output_ref="OUT-M318@v1",
        human_review_evidence_ref="HUMAN-REVIEW-M318@v1",
        human_reviewer_ref="project-owner",
    )
    return build_ai_output_review_decision(
        review_decision_id="REVIEW-M318-HUMAN-REVIEW",
        output_artifact=artifact,
        review_decision=HUMAN_REVIEW_DECISION,
        reviewer_ref="project-owner",
        review_evidence_ref="HUMAN-REVIEW-M318@v1",
    )


def _regression_cases() -> list[dict[str, object]]:
    return [
        build_ai_regression_case(
            case_id="CASE-M318-CONTEXT",
            case_kind=REGRESSION_CASE_CONTEXT_PACKET,
            description="M31.4 context packet dependency remains required.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_context_packet_contract.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M318-REFUSAL",
            case_kind=REGRESSION_CASE_REFUSAL_LIMITATION,
            description="M31.5 refusal and limitation dependency remains required.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_refusal_limitation_rules.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M318-OUTPUT",
            case_kind=REGRESSION_CASE_OUTPUT_ACCEPTANCE,
            description="M31.6 output acceptance and review dependency remains required.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_output_acceptance_review_rules.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M318-PROVIDER-BOUNDARY",
            case_kind=REGRESSION_CASE_PROVIDER_BOUNDARY,
            description="M31.3 provider boundary remains blocked by default.",
            expected_status=REGRESSION_PASS_STATUS,
            evidence_ref="tests/test_ai_provider_adapter_boundary.py",
        ),
        build_ai_regression_case(
            case_id="CASE-M318-SMOKE-GATE",
            case_kind=REGRESSION_CASE_PROVIDER_SMOKE,
            description="Provider/local smoke remains explicitly gated.",
            expected_status=REGRESSION_FAIL_CLOSED_STATUS,
            evidence_ref="M31.8 shakedown gate",
        ),
    ]


def _evaluation_result() -> dict[str, object]:
    smoke = build_ai_provider_smoke_request(
        smoke_request_id="SMOKE-M318-BLOCKED",
        provider_boundary_request=_provider_boundary_request(),
    )
    return build_ai_evaluation_regression_result(
        evaluation_result_id="EVAL-M318-COMPLETE",
        context_packet=_context_packet(),
        refusal_decision=_refusal_decision(),
        output_review_decision=_output_review_decision(),
        provider_boundary_request=_provider_boundary_request(),
        regression_cases=_regression_cases(),
        provider_smoke_request=smoke,
    )


def _scenarios() -> list[dict[str, object]]:
    return [
        build_ai_runtime_shakedown_scenario(
            scenario_id="M318-S1-ADVISORY-QA",
            scenario_kind=SCENARIO_ADVISORY_QA,
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            runtime_target=DISABLED_RUNTIME_TARGET,
            prompt_contract_ref="PROMPT-CONTRACT-M318-S1@v1",
            context_packet_ref="CTX-PACKET-M318@v1",
            expected_refusal_decision="limited_answer",
            expected_output_state="human_reviewed",
        ),
        build_ai_runtime_shakedown_scenario(
            scenario_id="M318-S2-RETRIEVAL-LIMITED",
            scenario_kind=SCENARIO_RETRIEVAL_LIMITED,
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            runtime_target=DISABLED_RUNTIME_TARGET,
            prompt_contract_ref="PROMPT-CONTRACT-M318-S2@v1",
            context_packet_ref="CTX-PACKET-M318@v1",
            expected_refusal_decision="limited_answer",
            expected_output_state="human_reviewed",
        ),
        build_ai_runtime_shakedown_scenario(
            scenario_id="M318-S3-MISSING-SOURCE",
            scenario_kind=SCENARIO_MISSING_SOURCE_REFUSAL,
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            runtime_target=DISABLED_RUNTIME_TARGET,
            prompt_contract_ref="PROMPT-CONTRACT-M318-S3@v1",
            context_packet_ref="CTX-PACKET-M318@v1",
            expected_refusal_decision="request_source_evidence",
            expected_output_state="not_generated",
            expected_stop_condition=STOP_MISSING_CONTEXT_PACKET,
        ),
        build_ai_runtime_shakedown_scenario(
            scenario_id="M318-S4-DRAFT-OUTPUT",
            scenario_kind=SCENARIO_DRAFT_OUTPUT_SUPPORT,
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            runtime_target=DISABLED_RUNTIME_TARGET,
            prompt_contract_ref="PROMPT-CONTRACT-M318-S4@v1",
            context_packet_ref="CTX-PACKET-M318@v1",
            expected_refusal_decision="limited_answer",
            expected_output_state="draft_only",
        ),
        build_ai_runtime_shakedown_scenario(
            scenario_id="M318-S5-HUMAN-REVIEW",
            scenario_kind=SCENARIO_HUMAN_REVIEW_REQUIRED,
            assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
            runtime_target=DISABLED_RUNTIME_TARGET,
            prompt_contract_ref="PROMPT-CONTRACT-M318-S5@v1",
            context_packet_ref="CTX-PACKET-M318@v1",
            expected_refusal_decision="request_human_review",
            expected_output_state="review_required",
        ),
    ]


def _protocol() -> dict[str, object]:
    return build_ai_runtime_shakedown_protocol(
        protocol_id="PROTO-M318-BOUNDED-SHAKEDOWN",
        evaluation_result=_evaluation_result(),
        runtime_target_descriptor=build_ai_runtime_target_descriptor(
            runtime_target_id="RUNTIME-M318-DISABLED",
        ),
        scenarios=_scenarios(),
    )


def test_runtime_shakedown_baseline_exposes_m31_8_controls_without_api_key() -> None:
    baseline = build_ai_runtime_shakedown_baseline()

    assert baseline["checkpoint"] == AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID
    assert baseline["runtime_shakedown_status"] == AI_RUNTIME_SHAKEDOWN_STATUS_VALIDATED
    assert baseline["default_runtime_target"] == DISABLED_RUNTIME_TARGET
    assert baseline["api_key_required_by_default"] is False
    assert "M31.9" in baseline["next_checkpoint"]


def test_runtime_target_defaults_to_disabled_without_api_key() -> None:
    descriptor = build_ai_runtime_target_descriptor(
        runtime_target_id="RUNTIME-M318-DISABLED",
    )

    assert descriptor["runtime_target"] == DISABLED_RUNTIME_TARGET
    assert descriptor["runtime_target_status"] == RUNTIME_TARGET_STATUS_DISABLED
    assert descriptor["enable_runtime"] is False
    assert descriptor["allow_prompt_execution"] is False
    assert descriptor["api_key_required"] is False
    validate_ai_runtime_target_descriptor(descriptor)


def test_runtime_target_skips_when_prompt_execution_not_enabled() -> None:
    descriptor = build_ai_runtime_target_descriptor(
        runtime_target_id="RUNTIME-M318-SKIP",
        runtime_target=LOCAL_RUNTIME_CANDIDATE_TARGET,
        enable_runtime=True,
        allow_prompt_execution=False,
    )

    assert descriptor["runtime_target_status"] == RUNTIME_TARGET_STATUS_SKIPPED
    validate_ai_runtime_target_descriptor(descriptor)


def test_runtime_target_ready_requires_approved_bounded_runtime_and_prompt_opt_in() -> None:
    descriptor = build_ai_runtime_target_descriptor(
        runtime_target_id="RUNTIME-M318-READY",
        runtime_target=APPROVED_BOUNDED_RUNTIME_TARGET,
        enable_runtime=True,
        allow_prompt_execution=True,
    )

    assert descriptor["runtime_target_status"] == RUNTIME_TARGET_STATUS_READY
    validate_ai_runtime_target_descriptor(descriptor)


def test_runtime_target_rejects_api_key_or_raw_provider_payload() -> None:
    descriptor = build_ai_runtime_target_descriptor(
        runtime_target_id="RUNTIME-M318-BLOCK-SECRETS",
    )

    for field_name in ("api_key", "provider_api_key", "raw_provider_payload", "model_output"):
        mutated = dict(descriptor)
        mutated[field_name] = "blocked"
        with pytest.raises(ValueError, match=field_name):
            validate_ai_runtime_target_descriptor(mutated)


def test_shakedown_scenario_rejects_unbounded_prompt_payloads() -> None:
    scenario = build_ai_runtime_shakedown_scenario(
        scenario_id="M318-PROMPT-BLOCK",
        scenario_kind=SCENARIO_ADVISORY_QA,
        assistance_mode=ADVISORY_QA_ASSISTANCE_MODE,
        runtime_target=DISABLED_RUNTIME_TARGET,
        prompt_contract_ref="PROMPT-CONTRACT-M318@v1",
        context_packet_ref="CTX-PACKET-M318@v1",
        expected_refusal_decision="limited_answer",
        expected_output_state="human_reviewed",
    )
    scenario["raw_prompt"] = "answer this freely"

    with pytest.raises(ValueError, match="raw_prompt"):
        validate_ai_runtime_shakedown_scenario(scenario)


def test_shakedown_protocol_accepts_complete_predeclared_scenario_set() -> None:
    protocol = _protocol()

    assert protocol["checkpoint"] == AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID
    assert protocol["runtime_shakedown_status"] == AI_RUNTIME_SHAKEDOWN_STATUS_VALIDATED
    assert protocol["provider_smoke_status"] == AI_PROVIDER_SMOKE_STATUS_BLOCKED
    assert protocol["api_key_required"] is False
    assert protocol["customer_ready_output_claim_allowed"] is False
    assert len(protocol["scenarios"]) == 5
    validate_ai_runtime_shakedown_protocol(protocol)


def test_shakedown_protocol_requires_all_scenario_kinds() -> None:
    incomplete = [
        scenario for scenario in _scenarios()
        if scenario["scenario_kind"] != SCENARIO_HUMAN_REVIEW_REQUIRED
    ]

    with pytest.raises(ValueError, match=SCENARIO_HUMAN_REVIEW_REQUIRED):
        build_ai_runtime_shakedown_protocol(
            protocol_id="PROTO-M318-MISSING-SCENARIO",
            evaluation_result=_evaluation_result(),
            runtime_target_descriptor=build_ai_runtime_target_descriptor(
                runtime_target_id="RUNTIME-M318-DISABLED",
            ),
            scenarios=incomplete,
        )


def test_shakedown_protocol_rejects_productization_customer_ready_and_commercial_flags() -> None:
    protocol = _protocol()

    for field_name in (
        "productization_claim_allowed",
        "customer_ready_output_claim_allowed",
        "commercialization_launch_planning_allowed",
        "ui_api_behavior_enabled",
        "autonomous_agentic_execution_allowed",
        "unbounded_prompt_execution_allowed",
    ):
        mutated = dict(protocol)
        mutated[field_name] = True
        with pytest.raises(ValueError, match=field_name):
            validate_ai_runtime_shakedown_protocol(mutated)


def test_shakedown_evidence_captures_bounded_result_without_human_observation_claim() -> None:
    evidence = build_ai_runtime_shakedown_evidence(
        shakedown_run_id="RUN-M318-CAPTURED",
        protocol=_protocol(),
        scenario_id="M318-S1-ADVISORY-QA",
        result_status=SHAKEDOWN_RESULT_EVIDENCE_CAPTURED,
        stop_condition=STOP_NONE_EXPECTED,
    )

    assert evidence["checkpoint"] == AI_RUNTIME_SHAKEDOWN_CHECKPOINT_ID
    assert evidence["api_key_required"] is False
    assert evidence["human_observation_completed"] is False
    assert evidence["customer_ready_output_claim_allowed"] is False
    validate_ai_runtime_shakedown_evidence(evidence)


def test_shakedown_evidence_fail_closed_requires_concrete_stop_condition() -> None:
    with pytest.raises(ValueError, match="concrete stop condition"):
        build_ai_runtime_shakedown_evidence(
            shakedown_run_id="RUN-M318-BAD-FAIL-CLOSED",
            protocol=_protocol(),
            scenario_id="M318-S1-ADVISORY-QA",
            result_status=SHAKEDOWN_RESULT_FAIL_CLOSED,
            stop_condition=STOP_NONE_EXPECTED,
        )


def test_shakedown_evidence_rejects_undeclared_scenario_and_human_observation_claim() -> None:
    protocol = _protocol()

    with pytest.raises(ValueError, match="Undeclared M31.8 shakedown scenario"):
        build_ai_runtime_shakedown_evidence(
            shakedown_run_id="RUN-M318-UNDECLARED",
            protocol=protocol,
            scenario_id="M318-NOT-DECLARED",
            result_status=SHAKEDOWN_RESULT_EVIDENCE_CAPTURED,
            stop_condition=STOP_NONE_EXPECTED,
        )

    evidence = build_ai_runtime_shakedown_evidence(
        shakedown_run_id="RUN-M318-NO-HUMAN-CLAIM",
        protocol=protocol,
        scenario_id="M318-S1-ADVISORY-QA",
        result_status=SHAKEDOWN_RESULT_EVIDENCE_CAPTURED,
        stop_condition=STOP_NONE_EXPECTED,
    )
    evidence["human_observation_completed"] = True

    with pytest.raises(ValueError, match="M31.9 human observation"):
        validate_ai_runtime_shakedown_evidence(evidence)
