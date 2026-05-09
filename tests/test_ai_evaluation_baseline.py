import pytest

from asbp.ai_evaluation import (
    ACCEPTANCE_DECISION_CONSISTENCY_DIMENSION,
    AI_EVALUATION_BASELINE_CHECKPOINT_ID,
    DOCUMENT_OUTPUT_EVALUATION_FAMILY,
    REGRESSION_CASE_FAIL,
    REGRESSION_CASE_PASS,
    REGRESSION_RUN_FAIL,
    REGRESSION_RUN_PASS,
    build_ai_evaluation_baseline,
    build_ai_evaluation_case,
    build_ai_regression_run,
    build_ai_regression_suite,
    validate_ai_evaluation_case,
    validate_ai_regression_run,
    validate_ai_regression_suite,
)
from asbp.ai_runtime import (
    ACCEPT_CANDIDATE_OUTPUT_DECISION,
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    GOVERNED_CONTRACT_ROLE,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_ENGINE_INPUT_ROLE,
    REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
    STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
    STRONG_STRUCTURED_INPUT_FILL_MODE,
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    URS_DOCUMENT_FAMILY,
    VALIDATED_EVIDENCE_STATUS,
    build_ai_candidate_output,
    build_ai_context_item,
    build_ai_context_package,
    build_ai_generation_mode_request,
    build_ai_output_acceptance_decision,
    build_ai_runtime_entry_request,
)


def _runtime_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-EVAL-001",
        job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
        caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
        governed_source_refs=[
            "TEMPLATE-URS@v1",
            "DOCUMENT-LIFECYCLE-STATE@v1",
            "STANDARDS-GUARDRAIL-CONTEXT@v1",
        ],
        engine_contract_refs=[
            "DOCUMENT-REQUEST-CONTRACT@v1",
            "DOCUMENT-OUTPUT-CONTRACT@v1",
        ],
    )


def _context_package() -> dict[str, object]:
    return build_ai_context_package(
        context_package_id="CTXPKG-EVAL-001",
        ai_runtime_entry_request=_runtime_request(),
        context_items=[
            build_ai_context_item(
                context_item_id="CTX-TEMPLATE",
                source_family=TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
                source_ref="TEMPLATE-URS@v1",
                source_role=AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
                payload_classification=REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
                evidence_status=VALIDATED_EVIDENCE_STATUS,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
            build_ai_context_item(
                context_item_id="CTX-LIFECYCLE",
                source_family=DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
                source_ref="DOCUMENT-LIFECYCLE-STATE@v1",
                source_role=GOVERNED_ENGINE_INPUT_ROLE,
                payload_classification=STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
                evidence_status=VALIDATED_EVIDENCE_STATUS,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
            build_ai_context_item(
                context_item_id="CTX-STANDARDS",
                source_family=STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
                source_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
                source_role=GOVERNED_CONTRACT_ROLE,
                payload_classification=REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
                evidence_status=VALIDATED_EVIDENCE_STATUS,
                is_authoritative=True,
                may_be_used_for_generation=True,
            ),
        ],
    )


def _generation_request() -> dict[str, object]:
    return build_ai_generation_mode_request(
        generation_request_id="GEN-EVAL-001",
        context_package=_context_package(),
        output_family=URS_DOCUMENT_FAMILY,
        generation_mode=STRONG_STRUCTURED_INPUT_FILL_MODE,
        standards_guardrail_ref="STANDARDS-GUARDRAIL-CONTEXT@v1",
    )


def _acceptance_decision(
    *,
    content_contract_satisfied: bool = True,
) -> dict[str, object]:
    candidate = build_ai_candidate_output(
        output_candidate_id="CAND-EVAL-001",
        generation_mode_request=_generation_request(),
        candidate_output_ref="CANDIDATE-URS-OUTPUT@v1",
        candidate_evidence_status=VALIDATED_EVIDENCE_STATUS,
        content_contract_satisfied=content_contract_satisfied,
        family_constraints_satisfied=True,
        standards_guardrails_satisfied=True,
        evidence_claims_supported=True,
        assumptions_labeled_when_required=True,
        placeholders_used_for_missing_truth=True,
    )
    return build_ai_output_acceptance_decision(
        acceptance_decision_id="ACC-EVAL-001",
        candidate_output=candidate,
    )


def test_evaluation_baseline_exposes_m17_1_rules() -> None:
    baseline = build_ai_evaluation_baseline()

    assert baseline["checkpoint"] == AI_EVALUATION_BASELINE_CHECKPOINT_ID
    assert DOCUMENT_OUTPUT_EVALUATION_FAMILY in baseline["supported_evaluation_families"]
    assert ACCEPTANCE_DECISION_CONSISTENCY_DIMENSION in baseline[
        "supported_baseline_evaluation_dimensions"
    ]
    assert "quality_gates" in baseline["not_owned_by_m17_1"]
    assert "retrieval_use_governance" in baseline["not_owned_by_m17_1"]


def test_build_evaluation_case_accepts_valid_acceptance_decision() -> None:
    case = build_ai_evaluation_case(
        evaluation_case_id="EVAL-CASE-001",
        acceptance_decision=_acceptance_decision(),
        evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
        baseline_ref="AI-EVAL-BASELINE@v1",
        regression_group="m17_1_document_baseline",
    )

    assert case["checkpoint"] == AI_EVALUATION_BASELINE_CHECKPOINT_ID
    assert case["expected_acceptance_decision"] == ACCEPT_CANDIDATE_OUTPUT_DECISION
    validate_ai_evaluation_case(case)


def test_build_regression_suite_accepts_unique_cases() -> None:
    case = build_ai_evaluation_case(
        evaluation_case_id="EVAL-CASE-SUITE-001",
        acceptance_decision=_acceptance_decision(),
        evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
        baseline_ref="AI-EVAL-BASELINE@v1",
        regression_group="m17_1_document_baseline",
    )

    suite = build_ai_regression_suite(
        evaluation_suite_id="EVAL-SUITE-001",
        baseline_ref="AI-EVAL-BASELINE@v1",
        evaluation_cases=[case],
    )

    assert suite["evaluation_suite_status"] == "ai_evaluation_suite_validated"
    validate_ai_regression_suite(suite)


def test_regression_run_passes_when_expected_decision_matches_actual_decision() -> None:
    case = build_ai_evaluation_case(
        evaluation_case_id="EVAL-CASE-RUN-PASS",
        acceptance_decision=_acceptance_decision(),
        evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
        baseline_ref="AI-EVAL-BASELINE@v1",
        regression_group="m17_1_document_baseline",
    )
    suite = build_ai_regression_suite(
        evaluation_suite_id="EVAL-SUITE-PASS",
        baseline_ref="AI-EVAL-BASELINE@v1",
        evaluation_cases=[case],
    )

    run = build_ai_regression_run(
        regression_run_id="REG-RUN-PASS",
        regression_suite=suite,
    )

    assert run["regression_run_result"] == REGRESSION_RUN_PASS
    assert run["case_results"][0]["regression_case_result"] == REGRESSION_CASE_PASS
    validate_ai_regression_run(run)


def test_regression_run_fails_when_expected_decision_mismatches_actual_decision() -> None:
    case = build_ai_evaluation_case(
        evaluation_case_id="EVAL-CASE-RUN-FAIL",
        acceptance_decision=_acceptance_decision(),
        evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
        baseline_ref="AI-EVAL-BASELINE@v1",
        regression_group="m17_1_document_baseline",
        expected_acceptance_decision="fallback_or_refuse_output",
    )
    suite = build_ai_regression_suite(
        evaluation_suite_id="EVAL-SUITE-FAIL",
        baseline_ref="AI-EVAL-BASELINE@v1",
        evaluation_cases=[case],
    )

    run = build_ai_regression_run(
        regression_run_id="REG-RUN-FAIL",
        regression_suite=suite,
    )

    assert run["regression_run_result"] == REGRESSION_RUN_FAIL
    assert run["case_results"][0]["regression_case_result"] == REGRESSION_CASE_FAIL
    assert run["failed_case_count"] == 1


def test_evaluation_case_rejects_unversioned_baseline_ref() -> None:
    with pytest.raises(ValueError, match="exactly one '@'"):
        build_ai_evaluation_case(
            evaluation_case_id="EVAL-CASE-BAD-REF",
            acceptance_decision=_acceptance_decision(),
            evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
            baseline_ref="AI-EVAL-BASELINE",
            regression_group="m17_1_document_baseline",
        )


def test_regression_suite_rejects_duplicate_case_ids() -> None:
    case = build_ai_evaluation_case(
        evaluation_case_id="EVAL-CASE-DUP",
        acceptance_decision=_acceptance_decision(),
        evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
        baseline_ref="AI-EVAL-BASELINE@v1",
        regression_group="m17_1_document_baseline",
    )

    with pytest.raises(ValueError, match="Duplicate value"):
        build_ai_regression_suite(
            evaluation_suite_id="EVAL-SUITE-DUP",
            baseline_ref="AI-EVAL-BASELINE@v1",
            evaluation_cases=[case, case],
        )


def test_evaluation_case_rejects_future_quality_or_groundedness_fields() -> None:
    case = build_ai_evaluation_case(
        evaluation_case_id="EVAL-CASE-FUTURE",
        acceptance_decision=_acceptance_decision(),
        evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
        baseline_ref="AI-EVAL-BASELINE@v1",
        regression_group="m17_1_document_baseline",
    )

    case["groundedness_score"] = 0.9
    with pytest.raises(ValueError, match="groundedness_score"):
        validate_ai_evaluation_case(case)

    del case["groundedness_score"]
    case["quality_gate_result"] = "pass"
    with pytest.raises(ValueError, match="quality_gate_result"):
        validate_ai_evaluation_case(case)


def test_evaluation_case_rejects_misaligned_evaluation_family() -> None:
    case = build_ai_evaluation_case(
        evaluation_case_id="EVAL-CASE-ALIGN",
        acceptance_decision=_acceptance_decision(),
        evaluation_family=DOCUMENT_OUTPUT_EVALUATION_FAMILY,
        baseline_ref="AI-EVAL-BASELINE@v1",
        regression_group="m17_1_document_baseline",
    )
    case["evaluation_family"] = "reporting_output_evaluation"

    with pytest.raises(ValueError, match="reporting evaluation family"):
        validate_ai_evaluation_case(case)
