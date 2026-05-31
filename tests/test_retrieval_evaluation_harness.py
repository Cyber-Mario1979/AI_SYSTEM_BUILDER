"""Tests for M30.7 retrieval evaluation harness."""

from __future__ import annotations

from dataclasses import replace

from asbp.retrieval import RetrievalResult
from asbp.retrieval.assets import AssetRetrievalResult
from asbp.retrieval.evaluation import RetrievalEvaluationCase, RetrievalEvaluationHarness, evaluate_retrieval_results
from asbp.retrieval.standards import StandardsRetrievalResult


def _result(**overrides: object) -> RetrievalResult:
    values = {
        "source_id": "SRC-001",
        "source_path": "data/source/src_001.json",
        "source_version": "v1",
        "source_status": "approved",
        "authority_role": "reference_support",
        "eligibility_decision": "eligible",
        "chunk_ref": "section:1",
        "build_id": "m30-7-test-build",
        "snippet": "retrieval result snippet",
        "score": 2,
        "helper_only": True,
        "non_authoritative": True,
        "limitation_trace": (),
    }
    values.update(overrides)
    return RetrievalResult(**values)


def test_evaluation_passes_for_expected_source_and_chunk() -> None:
    case = RetrievalEvaluationCase(
        case_id="case-1",
        query_text="protocol",
        expected_source_ids=frozenset({"SRC-001"}),
        expected_chunk_refs=frozenset({"section:1"}),
    )

    result = evaluate_retrieval_results(case, [_result()])

    assert result.passed is True
    assert result.expected_source_recall == 1.0
    assert result.matched_expected_source_count == 1
    assert result.matched_expected_chunk_count == 1
    assert result.trace_complete_count == 1
    assert result.helper_only_count == 1
    assert result.non_authoritative_count == 1
    assert result.issues == ()


def test_evaluation_reports_missing_expected_source_and_chunk() -> None:
    case = RetrievalEvaluationCase(
        case_id="case-missing",
        query_text="protocol",
        expected_source_ids=frozenset({"SRC-404"}),
        expected_chunk_refs=frozenset({"section:404"}),
    )

    result = evaluate_retrieval_results(case, [_result()])

    assert result.passed is False
    assert result.expected_source_recall == 0.0
    assert result.missing_expected_source_ids == frozenset({"SRC-404"})
    assert result.missing_expected_chunk_refs == frozenset({"section:404"})
    assert {issue.issue_type for issue in result.issues} == {"missing_expected_source", "missing_expected_chunk"}


def test_evaluation_reports_forbidden_source() -> None:
    case = RetrievalEvaluationCase(
        case_id="case-forbidden",
        query_text="protocol",
        forbidden_source_ids=frozenset({"SRC-001"}),
    )

    result = evaluate_retrieval_results(case, [_result()])

    assert result.passed is False
    assert result.forbidden_source_ids_found == frozenset({"SRC-001"})
    assert [issue.issue_type for issue in result.issues] == ["forbidden_source_returned"]


def test_evaluation_detects_missing_trace_metadata() -> None:
    case = RetrievalEvaluationCase(case_id="case-trace", query_text="protocol")

    result = evaluate_retrieval_results(case, [_result(source_path="", chunk_ref="")])

    assert result.passed is False
    assert result.trace_incomplete_count == 1
    assert {issue.issue_type for issue in result.issues} == {"missing_trace_field"}
    assert {issue.message for issue in result.issues} == {
        "Retrieval result missing required trace field: source_path",
        "Retrieval result missing required trace field: chunk_ref",
    }


def test_evaluation_detects_missing_helper_and_non_authority_flags() -> None:
    case = RetrievalEvaluationCase(case_id="case-flags", query_text="protocol")

    result = RetrievalEvaluationHarness().evaluate(case, [_result(helper_only=False, non_authoritative=False)])

    assert result.passed is False
    assert result.helper_only_count == 0
    assert result.non_authoritative_count == 0
    assert {issue.issue_type for issue in result.issues} == {"not_helper_only", "not_non_authoritative"}


def test_evaluation_supports_standards_result_shape() -> None:
    base = _result(source_id="STD-001", chunk_ref="clause:4.2")
    standards_result = StandardsRetrievalResult(
        retrieval_result=base,
        citation="STD-001 v1 clause:4.2",
        limitation_warnings=("helper-only",),
    )
    case = RetrievalEvaluationCase(
        case_id="case-standards",
        query_text="standard",
        expected_source_ids=frozenset({"STD-001"}),
        expected_chunk_refs=frozenset({"clause:4.2"}),
    )

    result = evaluate_retrieval_results(case, [standards_result])

    assert result.passed is True
    assert result.result_count == 1
    assert result.expected_source_recall == 1.0


def test_evaluation_supports_asset_result_shape() -> None:
    base = _result(source_id="TPL-001", chunk_ref="template:TPL-001:v1:summary:chunk-1")
    asset_result = AssetRetrievalResult(
        retrieval_result=base,
        asset_id="TPL-001",
        asset_version="v1",
        asset_family="template",
        context_type="summary",
    )
    case = RetrievalEvaluationCase(
        case_id="case-asset",
        query_text="template",
        expected_source_ids=frozenset({"TPL-001"}),
        expected_chunk_refs=frozenset({"template:TPL-001:v1:summary:chunk-1"}),
    )

    result = evaluate_retrieval_results(case, [asset_result])

    assert result.passed is True
    assert result.matched_expected_source_count == 1
    assert result.matched_expected_chunk_count == 1


def test_empty_results_pass_only_when_no_expected_sources_or_chunks() -> None:
    no_expectations = RetrievalEvaluationCase(case_id="case-empty-ok", query_text="none")
    expected = RetrievalEvaluationCase(
        case_id="case-empty-missing",
        query_text="none",
        expected_source_ids=frozenset({"SRC-001"}),
    )

    ok = evaluate_retrieval_results(no_expectations, [])
    missing = evaluate_retrieval_results(expected, [])

    assert ok.passed is True
    assert ok.expected_source_recall == 1.0
    assert missing.passed is False
    assert missing.expected_source_recall == 0.0


def test_evaluation_does_not_mutate_results() -> None:
    base = _result()
    case = RetrievalEvaluationCase(case_id="case-no-mutation", query_text="protocol")

    evaluate_retrieval_results(case, [base])

    assert base == _result()
