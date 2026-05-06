"AI evaluation baseline and regression harness for M17.1."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

from asbp.ai_runtime.output_acceptance import (
    ACCEPT_CANDIDATE_OUTPUT_DECISION,
    FALLBACK_OR_REFUSE_OUTPUT_DECISION,
    RETRY_CANDIDATE_OUTPUT_DECISION,
    SUPPORTED_OUTPUT_ACCEPTANCE_DECISIONS,
    validate_ai_output_acceptance_decision,
)

AI_EVALUATION_BASELINE_CHECKPOINT_ID = "M17.1"
AI_EVALUATION_BASELINE_CONTRACT_VERSION = "ai-evaluation-baseline-v1"
AI_EVALUATION_CASE_STATUS_VALIDATED = "ai_evaluation_case_validated"
AI_EVALUATION_SUITE_STATUS_VALIDATED = "ai_evaluation_suite_validated"
AI_REGRESSION_RUN_STATUS_VALIDATED = "ai_regression_run_validated"

DOCUMENT_OUTPUT_EVALUATION_FAMILY = "document_output_evaluation"
REPORTING_OUTPUT_EVALUATION_FAMILY = "reporting_output_evaluation"
SUPPORTED_EVALUATION_FAMILIES = (
    DOCUMENT_OUTPUT_EVALUATION_FAMILY,
    REPORTING_OUTPUT_EVALUATION_FAMILY,
)

ACCEPTANCE_DECISION_CONSISTENCY_DIMENSION = "acceptance_decision_consistency"
CANDIDATE_CONTRACT_COVERAGE_DIMENSION = "candidate_contract_coverage"
REGRESSION_STABILITY_DIMENSION = "regression_stability"
SUPPORTED_BASELINE_EVALUATION_DIMENSIONS = (
    ACCEPTANCE_DECISION_CONSISTENCY_DIMENSION,
    CANDIDATE_CONTRACT_COVERAGE_DIMENSION,
    REGRESSION_STABILITY_DIMENSION,
)

REGRESSION_CASE_PASS = "regression_case_pass"
REGRESSION_CASE_FAIL = "regression_case_fail"
SUPPORTED_REGRESSION_CASE_RESULTS = (
    REGRESSION_CASE_PASS,
    REGRESSION_CASE_FAIL,
)

REGRESSION_RUN_PASS = "regression_run_pass"
REGRESSION_RUN_FAIL = "regression_run_fail"
SUPPORTED_REGRESSION_RUN_RESULTS = (
    REGRESSION_RUN_PASS,
    REGRESSION_RUN_FAIL,
)

_PROHIBITED_EVALUATION_FIELDS = (
    "raw_prompt",
    "free_form_prompt",
    "unvalidated_user_prompt",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "direct_llm_call",
    "llm_provider",
    "model_name",
    "api_key",
    "generated_document_text",
    "generated_report_text",
    "generated_output_text",
    "quality_gate_result",
    "quality_gate_decision",
    "groundedness_score",
    "groundedness_check",
    "evidence_link_check",
    "standards_conformance_score",
    "standards_conformance_check",
    "detail_consistency_score",
    "detail_consistency_check",
    "retrieval_use_rule",
    "retrieval_use_decision",
    "recommendation_payload",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "source_truth_override",
    "execution_truth_override",
    "validation_truth_override",
)

_CASE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "evaluation_case_id",
    "evaluation_family",
    "evaluation_case_status",
    "baseline_ref",
    "regression_group",
    "source_acceptance_decision_id",
    "source_output_candidate_id",
    "source_output_family",
    "source_generation_mode",
    "expected_acceptance_decision",
)

_CASE_REQUIRED_FALSE_FIELDS = (
    "actual_llm_call_required",
    "prompt_template_required",
    "quality_gate_in_scope",
    "groundedness_gate_in_scope",
    "standards_conformance_gate_in_scope",
    "detail_consistency_gate_in_scope",
    "retrieval_use_governance_in_scope",
    "recommendation_behavior_in_scope",
    "state_mutation_allowed",
    "approval_or_release_allowed",
)

_SUITE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "evaluation_suite_id",
    "evaluation_suite_status",
    "baseline_ref",
)

_RUN_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "regression_run_id",
    "evaluation_suite_id",
    "regression_run_status",
    "regression_run_result",
)


def build_ai_evaluation_baseline() -> dict[str, Any]:
    """Return the M17.1 AI evaluation baseline contract."""
    return {
        "checkpoint": AI_EVALUATION_BASELINE_CHECKPOINT_ID,
        "contract_version": AI_EVALUATION_BASELINE_CONTRACT_VERSION,
        "supported_evaluation_families": list(SUPPORTED_EVALUATION_FAMILIES),
        "supported_baseline_evaluation_dimensions": list(
            SUPPORTED_BASELINE_EVALUATION_DIMENSIONS
        ),
        "supported_regression_case_results": list(SUPPORTED_REGRESSION_CASE_RESULTS),
        "supported_regression_run_results": list(SUPPORTED_REGRESSION_RUN_RESULTS),
        "baseline_policy": (
            "evaluation_baseline_records_measurable_contract_regression_expectations"
        ),
        "regression_policy": (
            "regression_harness_compares_expected_acceptance_decisions_against_"
            "validated_m16_output_acceptance_decisions"
        ),
        "authority_policy": (
            "m17_1_evaluation_records_do_not_create_source_execution_validation_"
            "approval_or_release_truth"
        ),
        "not_owned_by_m17_1": [
            "actual_llm_calls",
            "prompt_templates",
            "quality_gates",
            "groundedness_checks",
            "evidence_link_checks",
            "standards_conformance_checks",
            "detail_level_consistency_checks",
            "retrieval_use_governance",
            "recommendation_behavior",
            "ui_api_behavior",
            "workflow_state_mutation",
            "document_approval_or_release",
        ],
    }


def build_ai_evaluation_case(
    *,
    evaluation_case_id: str,
    acceptance_decision: dict[str, object],
    evaluation_family: str,
    baseline_ref: str,
    regression_group: str,
    expected_acceptance_decision: str | None = None,
    evaluation_dimensions: list[str] | None = None,
) -> dict[str, object]:
    """Build and validate one M17.1 regression evaluation case."""
    validate_ai_output_acceptance_decision(acceptance_decision)
    dimensions = list(
        evaluation_dimensions
        if evaluation_dimensions is not None
        else SUPPORTED_BASELINE_EVALUATION_DIMENSIONS
    )
    normalized_expected_decision = _normalize_supported_value(
        expected_acceptance_decision
        or acceptance_decision["acceptance_decision"],
        field_name="expected_acceptance_decision",
        supported_values=SUPPORTED_OUTPUT_ACCEPTANCE_DECISIONS,
        error_prefix="AI evaluation case",
    )

    case = {
        "checkpoint": AI_EVALUATION_BASELINE_CHECKPOINT_ID,
        "contract_version": AI_EVALUATION_BASELINE_CONTRACT_VERSION,
        "evaluation_case_id": _require_non_empty_string(
            evaluation_case_id,
            field_name="evaluation_case_id",
            error_prefix="AI evaluation case",
        ),
        "evaluation_family": _normalize_supported_value(
            evaluation_family,
            field_name="evaluation_family",
            supported_values=SUPPORTED_EVALUATION_FAMILIES,
            error_prefix="AI evaluation case",
        ),
        "evaluation_case_status": AI_EVALUATION_CASE_STATUS_VALIDATED,
        "baseline_ref": _parse_version_pinned_ref(
            baseline_ref,
            field_name="baseline_ref",
        ),
        "regression_group": _require_non_empty_string(
            regression_group,
            field_name="regression_group",
            error_prefix="AI evaluation case",
        ),
        "evaluation_dimensions": dimensions,
        "source_acceptance_decision_id": str(
            acceptance_decision["acceptance_decision_id"]
        ),
        "source_output_candidate_id": str(acceptance_decision["output_candidate_id"]),
        "source_output_family": str(acceptance_decision["output_family"]),
        "source_generation_mode": str(acceptance_decision["generation_mode"]),
        "source_acceptance_decision": str(acceptance_decision["acceptance_decision"]),
        "expected_acceptance_decision": normalized_expected_decision,
        "source_acceptance_decision_payload": dict(acceptance_decision),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "quality_gate_in_scope": False,
        "groundedness_gate_in_scope": False,
        "standards_conformance_gate_in_scope": False,
        "detail_consistency_gate_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "recommendation_behavior_in_scope": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "measurement_policy": (
            "m17_1_measures_regression_expectations_only_no_quality_gate_decision"
        ),
    }
    validate_ai_evaluation_case(case)
    return case


def validate_ai_evaluation_case(case: dict[str, object]) -> None:
    """Validate one M17.1 AI evaluation baseline case."""
    _validate_prohibited_fields(case, _PROHIBITED_EVALUATION_FIELDS)
    _validate_required_string_fields(
        case,
        _CASE_REQUIRED_STRING_FIELDS,
        error_prefix="AI evaluation case",
    )
    _validate_expected_exact_value(
        case,
        field_name="checkpoint",
        expected_value=AI_EVALUATION_BASELINE_CHECKPOINT_ID,
        error_prefix="AI evaluation case",
    )
    _validate_expected_exact_value(
        case,
        field_name="contract_version",
        expected_value=AI_EVALUATION_BASELINE_CONTRACT_VERSION,
        error_prefix="AI evaluation case",
    )
    _validate_expected_exact_value(
        case,
        field_name="evaluation_case_status",
        expected_value=AI_EVALUATION_CASE_STATUS_VALIDATED,
        error_prefix="AI evaluation case",
    )

    for field_name in _CASE_REQUIRED_FALSE_FIELDS:
        if case.get(field_name) is not False:
            raise ValueError(f"AI evaluation case requires {field_name} to be False.")

    acceptance_decision = case.get("source_acceptance_decision_payload")
    if not isinstance(acceptance_decision, dict):
        raise ValueError(
            "AI evaluation case must include source_acceptance_decision_payload dict."
        )
    validate_ai_output_acceptance_decision(acceptance_decision)

    for case_field, decision_field in (
        ("source_acceptance_decision_id", "acceptance_decision_id"),
        ("source_output_candidate_id", "output_candidate_id"),
        ("source_output_family", "output_family"),
        ("source_generation_mode", "generation_mode"),
        ("source_acceptance_decision", "acceptance_decision"),
    ):
        if case[case_field] != acceptance_decision[decision_field]:
            raise ValueError(
                f"AI evaluation case {case_field} must match "
                "source_acceptance_decision_payload."
            )

    _normalize_supported_value(
        case["evaluation_family"],
        field_name="evaluation_family",
        supported_values=SUPPORTED_EVALUATION_FAMILIES,
        error_prefix="AI evaluation case",
    )
    _validate_evaluation_family_alignment(
        evaluation_family=str(case["evaluation_family"]),
        source_output_family=str(case["source_output_family"]),
    )
    _normalize_supported_value(
        case["expected_acceptance_decision"],
        field_name="expected_acceptance_decision",
        supported_values=SUPPORTED_OUTPUT_ACCEPTANCE_DECISIONS,
        error_prefix="AI evaluation case",
    )
    _parse_version_pinned_ref(case["baseline_ref"], field_name="baseline_ref")
    _validate_dimensions(case.get("evaluation_dimensions"))


def build_ai_regression_suite(
    *,
    evaluation_suite_id: str,
    baseline_ref: str,
    evaluation_cases: list[dict[str, object]],
) -> dict[str, object]:
    """Build and validate an M17.1 regression suite."""
    suite = {
        "checkpoint": AI_EVALUATION_BASELINE_CHECKPOINT_ID,
        "contract_version": AI_EVALUATION_BASELINE_CONTRACT_VERSION,
        "evaluation_suite_id": _require_non_empty_string(
            evaluation_suite_id,
            field_name="evaluation_suite_id",
            error_prefix="AI regression suite",
        ),
        "evaluation_suite_status": AI_EVALUATION_SUITE_STATUS_VALIDATED,
        "baseline_ref": _parse_version_pinned_ref(
            baseline_ref,
            field_name="baseline_ref",
        ),
        "evaluation_cases": list(evaluation_cases),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "quality_gate_in_scope": False,
        "groundedness_gate_in_scope": False,
        "standards_conformance_gate_in_scope": False,
        "detail_consistency_gate_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "recommendation_behavior_in_scope": False,
    }
    validate_ai_regression_suite(suite)
    return suite


def validate_ai_regression_suite(suite: dict[str, object]) -> None:
    """Validate one M17.1 regression suite."""
    _validate_prohibited_fields(suite, _PROHIBITED_EVALUATION_FIELDS)
    _validate_required_string_fields(
        suite,
        _SUITE_REQUIRED_STRING_FIELDS,
        error_prefix="AI regression suite",
    )
    _validate_expected_exact_value(
        suite,
        field_name="checkpoint",
        expected_value=AI_EVALUATION_BASELINE_CHECKPOINT_ID,
        error_prefix="AI regression suite",
    )
    _validate_expected_exact_value(
        suite,
        field_name="contract_version",
        expected_value=AI_EVALUATION_BASELINE_CONTRACT_VERSION,
        error_prefix="AI regression suite",
    )
    _validate_expected_exact_value(
        suite,
        field_name="evaluation_suite_status",
        expected_value=AI_EVALUATION_SUITE_STATUS_VALIDATED,
        error_prefix="AI regression suite",
    )

    for field_name in (
        "actual_llm_call_required",
        "prompt_template_required",
        "quality_gate_in_scope",
        "groundedness_gate_in_scope",
        "standards_conformance_gate_in_scope",
        "detail_consistency_gate_in_scope",
        "retrieval_use_governance_in_scope",
        "recommendation_behavior_in_scope",
    ):
        if suite.get(field_name) is not False:
            raise ValueError(f"AI regression suite requires {field_name} to be False.")

    cases = suite.get("evaluation_cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("AI regression suite must declare non-empty evaluation_cases.")

    baseline_ref = _parse_version_pinned_ref(
        suite["baseline_ref"],
        field_name="baseline_ref",
    )
    case_ids: list[str] = []
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("AI regression suite evaluation_cases must contain dicts.")
        validate_ai_evaluation_case(case)
        case_ids.append(str(case["evaluation_case_id"]))
        if case["baseline_ref"] != baseline_ref:
            raise ValueError(
                "AI regression suite baseline_ref must match every evaluation case."
            )
    _reject_duplicates(case_ids, field_name="evaluation_case_id")


def build_ai_regression_run(
    *,
    regression_run_id: str,
    regression_suite: dict[str, object],
) -> dict[str, object]:
    """Build and validate an M17.1 regression run result."""
    validate_ai_regression_suite(regression_suite)
    case_results = [
        _build_case_result(case)
        for case in _suite_cases(regression_suite)
    ]
    failed_case_count = sum(
        1 for case_result in case_results
        if case_result["regression_case_result"] == REGRESSION_CASE_FAIL
    )
    passed_case_count = len(case_results) - failed_case_count
    regression_run_result = (
        REGRESSION_RUN_PASS if failed_case_count == 0 else REGRESSION_RUN_FAIL
    )
    run = {
        "checkpoint": AI_EVALUATION_BASELINE_CHECKPOINT_ID,
        "contract_version": AI_EVALUATION_BASELINE_CONTRACT_VERSION,
        "regression_run_id": _require_non_empty_string(
            regression_run_id,
            field_name="regression_run_id",
            error_prefix="AI regression run",
        ),
        "evaluation_suite_id": str(regression_suite["evaluation_suite_id"]),
        "regression_run_status": AI_REGRESSION_RUN_STATUS_VALIDATED,
        "regression_run_result": regression_run_result,
        "case_results": case_results,
        "case_count": len(case_results),
        "passed_case_count": passed_case_count,
        "failed_case_count": failed_case_count,
        "source_regression_suite": dict(regression_suite),
        "actual_llm_call_required": False,
        "prompt_template_required": False,
        "quality_gate_in_scope": False,
        "groundedness_gate_in_scope": False,
        "standards_conformance_gate_in_scope": False,
        "detail_consistency_gate_in_scope": False,
        "retrieval_use_governance_in_scope": False,
        "recommendation_behavior_in_scope": False,
        "state_mutation_allowed": False,
        "approval_or_release_allowed": False,
        "regression_policy": (
            "m17_1_regression_run_reports_expected_vs_actual_contract_outcomes_only"
        ),
    }
    validate_ai_regression_run(run)
    return run


def validate_ai_regression_run(run: dict[str, object]) -> None:
    """Validate one M17.1 regression run result."""
    _validate_prohibited_fields(run, _PROHIBITED_EVALUATION_FIELDS)
    _validate_required_string_fields(
        run,
        _RUN_REQUIRED_STRING_FIELDS,
        error_prefix="AI regression run",
    )
    _validate_expected_exact_value(
        run,
        field_name="checkpoint",
        expected_value=AI_EVALUATION_BASELINE_CHECKPOINT_ID,
        error_prefix="AI regression run",
    )
    _validate_expected_exact_value(
        run,
        field_name="contract_version",
        expected_value=AI_EVALUATION_BASELINE_CONTRACT_VERSION,
        error_prefix="AI regression run",
    )
    _validate_expected_exact_value(
        run,
        field_name="regression_run_status",
        expected_value=AI_REGRESSION_RUN_STATUS_VALIDATED,
        error_prefix="AI regression run",
    )

    suite = run.get("source_regression_suite")
    if not isinstance(suite, dict):
        raise ValueError("AI regression run must include source_regression_suite dict.")
    validate_ai_regression_suite(suite)

    if run["evaluation_suite_id"] != suite["evaluation_suite_id"]:
        raise ValueError(
            "AI regression run evaluation_suite_id must match source_regression_suite."
        )

    case_results = run.get("case_results")
    if not isinstance(case_results, list) or not case_results:
        raise ValueError("AI regression run must declare non-empty case_results.")

    expected_case_results = [_build_case_result(case) for case in _suite_cases(suite)]
    if case_results != expected_case_results:
        raise ValueError(
            "AI regression run case_results must match deterministic suite evaluation."
        )

    failed_case_count = sum(
        1 for case_result in case_results
        if case_result["regression_case_result"] == REGRESSION_CASE_FAIL
    )
    passed_case_count = len(case_results) - failed_case_count
    expected_run_result = (
        REGRESSION_RUN_PASS if failed_case_count == 0 else REGRESSION_RUN_FAIL
    )
    if run.get("case_count") != len(case_results):
        raise ValueError("AI regression run case_count is incorrect.")
    if run.get("passed_case_count") != passed_case_count:
        raise ValueError("AI regression run passed_case_count is incorrect.")
    if run.get("failed_case_count") != failed_case_count:
        raise ValueError("AI regression run failed_case_count is incorrect.")
    if run["regression_run_result"] != expected_run_result:
        raise ValueError("AI regression run result is inconsistent with case results.")

    for field_name in (
        "actual_llm_call_required",
        "prompt_template_required",
        "quality_gate_in_scope",
        "groundedness_gate_in_scope",
        "standards_conformance_gate_in_scope",
        "detail_consistency_gate_in_scope",
        "retrieval_use_governance_in_scope",
        "recommendation_behavior_in_scope",
        "state_mutation_allowed",
        "approval_or_release_allowed",
    ):
        if run.get(field_name) is not False:
            raise ValueError(f"AI regression run requires {field_name} to be False.")


def _build_case_result(case: dict[str, object]) -> dict[str, object]:
    actual_decision = str(case["source_acceptance_decision"])
    expected_decision = str(case["expected_acceptance_decision"])
    result = (
        REGRESSION_CASE_PASS
        if actual_decision == expected_decision
        else REGRESSION_CASE_FAIL
    )
    return {
        "evaluation_case_id": str(case["evaluation_case_id"]),
        "source_acceptance_decision_id": str(case["source_acceptance_decision_id"]),
        "expected_acceptance_decision": expected_decision,
        "actual_acceptance_decision": actual_decision,
        "regression_case_result": result,
    }


def _suite_cases(suite: dict[str, object]) -> list[dict[str, object]]:
    cases = suite.get("evaluation_cases")
    if not isinstance(cases, list):
        raise ValueError("AI regression suite must expose list evaluation_cases.")
    normalized_cases: list[dict[str, object]] = []
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("AI regression suite evaluation_cases must contain dicts.")
        normalized_cases.append(case)
    return normalized_cases


def _validate_evaluation_family_alignment(
    *, evaluation_family: str, source_output_family: str
) -> None:
    if evaluation_family == DOCUMENT_OUTPUT_EVALUATION_FAMILY:
        if not source_output_family.endswith("_document"):
            raise ValueError(
                "AI evaluation case document evaluation family must use a document output family."
            )
        return
    if evaluation_family == REPORTING_OUTPUT_EVALUATION_FAMILY:
        if not source_output_family.endswith("_reporting"):
            raise ValueError(
                "AI evaluation case reporting evaluation family must use a reporting output family."
            )
        return
    raise ValueError(f"Unsupported AI evaluation family: {evaluation_family!r}.")


def _validate_dimensions(raw_dimensions: object) -> None:
    if not isinstance(raw_dimensions, list) or not raw_dimensions:
        raise ValueError(
            "AI evaluation case must declare non-empty evaluation_dimensions."
        )
    normalized = [
        _normalize_supported_value(
            dimension,
            field_name="evaluation_dimension",
            supported_values=SUPPORTED_BASELINE_EVALUATION_DIMENSIONS,
            error_prefix="AI evaluation case",
        )
        for dimension in raw_dimensions
    ]
    _reject_duplicates(normalized, field_name="evaluation_dimensions")


def _parse_version_pinned_ref(raw_ref: object, *, field_name: str) -> str:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="AI evaluation baseline ref",
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


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate value in {field_name}: {value!r}.")
        seen.add(value)


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
                f"{field_name} is not allowed in M17.1 AI evaluation baseline payloads."
            )
