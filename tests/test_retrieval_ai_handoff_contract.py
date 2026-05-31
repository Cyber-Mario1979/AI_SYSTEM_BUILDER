"""Tests for M30.8 retrieval-to-AI handoff contract helpers."""

from __future__ import annotations

from asbp.retrieval.ai_handoff import HANDOFF_LIMITATION, build_ai_handoff_packet
from asbp.retrieval.evaluation import RetrievalEvaluationCase, evaluate_retrieval_results
from asbp.retrieval.models import RetrievalResult
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
        "build_id": "m30-8-test-build",
        "snippet": "bounded retrieval context snippet",
        "score": 2,
        "helper_only": True,
        "non_authoritative": True,
        "limitation_trace": ("retrieval limitation",),
    }
    values.update(overrides)
    return RetrievalResult(**values)


def _passing_evaluation(result: object) -> object:
    base = getattr(result, "retrieval_result", result)
    case = RetrievalEvaluationCase(
        case_id="case-pass",
        query_text="context",
        expected_source_ids=frozenset({base.source_id}),
        expected_chunk_refs=frozenset({base.chunk_ref}),
    )
    return evaluate_retrieval_results(case, [result])


def test_valid_handoff_packet_preserves_context_trace_and_non_authority() -> None:
    retrieval_result = _result()
    evaluation = _passing_evaluation(retrieval_result)

    build = build_ai_handoff_packet(
        packet_id="packet-1",
        purpose="future-ai-context",
        evaluation_result=evaluation,
        retrieval_results=[retrieval_result],
    )

    assert build.allowed is True
    assert build.refusals == ()
    assert build.packet is not None
    assert build.packet.helper_only is True
    assert build.packet.non_authoritative is True
    assert build.packet.ai_runtime_executed is False
    assert build.packet.model_provider is None
    assert build.packet.evaluation_passed is True
    assert build.packet.handoff_limitations == (HANDOFF_LIMITATION,)
    [item] = build.packet.context_items
    assert item.source_id == "SRC-001"
    assert item.source_path == "data/source/src_001.json"
    assert item.source_version == "v1"
    assert item.chunk_ref == "section:1"
    assert item.citation == "SRC-001 v1 section:1"
    assert item.helper_only is True
    assert item.non_authoritative is True
    assert "retrieval limitation" in item.limitations
    assert HANDOFF_LIMITATION in item.limitations


def test_handoff_refuses_missing_evaluation_evidence() -> None:
    build = build_ai_handoff_packet(
        packet_id="packet-missing-eval",
        purpose="future-ai-context",
        evaluation_result=None,
        retrieval_results=[_result()],
    )

    assert build.allowed is False
    assert build.packet is None
    assert [refusal.refusal_type for refusal in build.refusals] == ["missing_evaluation"]


def test_handoff_refuses_failed_evaluation() -> None:
    retrieval_result = _result()
    failed_case = RetrievalEvaluationCase(
        case_id="case-fail",
        query_text="context",
        expected_source_ids=frozenset({"SRC-404"}),
    )
    failed_evaluation = evaluate_retrieval_results(failed_case, [retrieval_result])

    build = build_ai_handoff_packet(
        packet_id="packet-failed-eval",
        purpose="future-ai-context",
        evaluation_result=failed_evaluation,
        retrieval_results=[retrieval_result],
    )

    assert build.allowed is False
    assert build.packet is None
    assert [refusal.refusal_type for refusal in build.refusals] == ["failed_evaluation"]


def test_handoff_refuses_missing_source_trace() -> None:
    retrieval_result = _result(source_path="")
    evaluation = evaluate_retrieval_results(RetrievalEvaluationCase(case_id="case-trace", query_text="context"), [retrieval_result])

    build = build_ai_handoff_packet(
        packet_id="packet-trace",
        purpose="future-ai-context",
        evaluation_result=evaluation,
        retrieval_results=[retrieval_result],
    )

    assert build.allowed is False
    assert build.packet is None
    assert "missing_source_trace" in {refusal.refusal_type for refusal in build.refusals}


def test_handoff_refuses_missing_limitations_when_required() -> None:
    retrieval_result = _result(limitation_trace=())
    evaluation = _passing_evaluation(retrieval_result)

    build = build_ai_handoff_packet(
        packet_id="packet-limits",
        purpose="future-ai-context",
        evaluation_result=evaluation,
        retrieval_results=[retrieval_result],
    )

    assert build.allowed is False
    assert build.packet is None
    assert [refusal.refusal_type for refusal in build.refusals] == ["missing_limitations"]


def test_handoff_refuses_raw_retrieval_truth_attempt() -> None:
    retrieval_result = _result()
    evaluation = _passing_evaluation(retrieval_result)

    build = build_ai_handoff_packet(
        packet_id="packet-truth",
        purpose="future-ai-context",
        evaluation_result=evaluation,
        retrieval_results=[retrieval_result],
        assert_retrieval_as_truth=True,
    )

    assert build.allowed is False
    assert build.packet is None
    assert [refusal.refusal_type for refusal in build.refusals] == ["raw_retrieval_truth_attempt"]


def test_handoff_preserves_explicit_standard_citation_and_limitations() -> None:
    base = _result(source_id="STD-001", chunk_ref="clause:4.2")
    standard = StandardsRetrievalResult(
        retrieval_result=base,
        citation="STD-001 v1 clause:4.2",
        limitation_warnings=("standard limitation",),
    )
    evaluation = _passing_evaluation(standard)

    build = build_ai_handoff_packet(
        packet_id="packet-standard",
        purpose="future-ai-context",
        evaluation_result=evaluation,
        retrieval_results=[standard],
    )

    assert build.allowed is True
    assert build.packet is not None
    [item] = build.packet.context_items
    assert item.citation == "STD-001 v1 clause:4.2"
    assert "standard limitation" in item.limitations
    assert "retrieval limitation" in item.limitations
    assert HANDOFF_LIMITATION in item.limitations


def test_handoff_refuses_non_helper_or_authoritative_context() -> None:
    retrieval_result = _result(helper_only=False, non_authoritative=False)
    evaluation = evaluate_retrieval_results(RetrievalEvaluationCase(case_id="case-flags", query_text="context"), [retrieval_result])

    build = build_ai_handoff_packet(
        packet_id="packet-flags",
        purpose="future-ai-context",
        evaluation_result=evaluation,
        retrieval_results=[retrieval_result],
    )

    refusal_types = {refusal.refusal_type for refusal in build.refusals}
    assert build.allowed is False
    assert "not_helper_only" in refusal_types
    assert "not_non_authoritative" in refusal_types


def test_handoff_contract_does_not_execute_ai_runtime() -> None:
    retrieval_result = _result()
    evaluation = _passing_evaluation(retrieval_result)

    build = build_ai_handoff_packet(
        packet_id="packet-runtime",
        purpose="future-ai-context",
        evaluation_result=evaluation,
        retrieval_results=[retrieval_result],
    )

    assert build.packet is not None
    assert build.packet.ai_runtime_executed is False
    assert build.packet.model_provider is None
