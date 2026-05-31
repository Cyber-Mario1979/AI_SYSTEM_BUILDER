"""Deterministic retrieval evaluation helpers.

M30.7 evaluates existing bounded retrieval results from M30.4 through M30.6.
It does not mutate retrieval indexes, change ranking, broaden retrieval behavior,
introduce embeddings/vector stores, or create source authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence


@dataclass(frozen=True)
class RetrievalEvaluationCase:
    """Evaluation expectations for one retrieval query/result set."""

    case_id: str
    query_text: str
    expected_source_ids: frozenset[str] = field(default_factory=frozenset)
    expected_chunk_refs: frozenset[str] = field(default_factory=frozenset)
    forbidden_source_ids: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class RetrievalEvaluationIssue:
    """One deterministic retrieval evaluation issue."""

    issue_type: str
    message: str
    source_id: str | None = None
    chunk_ref: str | None = None


@dataclass(frozen=True)
class RetrievalEvaluationResult:
    """Deterministic evaluation summary for a retrieval result set."""

    case_id: str
    result_count: int
    expected_source_count: int
    matched_expected_source_count: int
    missing_expected_source_ids: frozenset[str]
    forbidden_source_ids_found: frozenset[str]
    expected_source_recall: float
    expected_chunk_count: int
    matched_expected_chunk_count: int
    missing_expected_chunk_refs: frozenset[str]
    trace_complete_count: int
    trace_incomplete_count: int
    helper_only_count: int
    non_authoritative_count: int
    issues: tuple[RetrievalEvaluationIssue, ...]

    @property
    def passed(self) -> bool:
        return not self.issues


class RetrievalEvaluationHarness:
    """Evaluate bounded retrieval outputs without changing retrieval behavior."""

    REQUIRED_TRACE_FIELDS = ("source_id", "source_path", "source_version", "chunk_ref")

    def evaluate(
        self,
        evaluation_case: RetrievalEvaluationCase,
        results: Iterable[object],
    ) -> RetrievalEvaluationResult:
        normalized_results = tuple(self._unwrap_result(result) for result in results)
        source_ids = frozenset(self._safe_value(result, "source_id") for result in normalized_results if self._safe_value(result, "source_id"))
        chunk_refs = frozenset(self._safe_value(result, "chunk_ref") for result in normalized_results if self._safe_value(result, "chunk_ref"))

        matched_expected_sources = evaluation_case.expected_source_ids.intersection(source_ids)
        missing_expected_sources = evaluation_case.expected_source_ids.difference(source_ids)
        forbidden_sources_found = evaluation_case.forbidden_source_ids.intersection(source_ids)

        matched_expected_chunks = evaluation_case.expected_chunk_refs.intersection(chunk_refs)
        missing_expected_chunks = evaluation_case.expected_chunk_refs.difference(chunk_refs)

        issues: list[RetrievalEvaluationIssue] = []
        for missing_source in sorted(missing_expected_sources):
            issues.append(
                RetrievalEvaluationIssue(
                    issue_type="missing_expected_source",
                    message=f"Expected source was not returned: {missing_source}",
                    source_id=missing_source,
                )
            )
        for forbidden_source in sorted(forbidden_sources_found):
            issues.append(
                RetrievalEvaluationIssue(
                    issue_type="forbidden_source_returned",
                    message=f"Forbidden source was returned: {forbidden_source}",
                    source_id=forbidden_source,
                )
            )
        for missing_chunk in sorted(missing_expected_chunks):
            issues.append(
                RetrievalEvaluationIssue(
                    issue_type="missing_expected_chunk",
                    message=f"Expected chunk was not returned: {missing_chunk}",
                    chunk_ref=missing_chunk,
                )
            )

        trace_complete_count = 0
        helper_only_count = 0
        non_authoritative_count = 0
        for result in normalized_results:
            result_issues = self._issues_for_result(result)
            issues.extend(result_issues)
            if not any(issue.issue_type == "missing_trace_field" for issue in result_issues):
                trace_complete_count += 1
            if getattr(result, "helper_only", False) is True:
                helper_only_count += 1
            if getattr(result, "non_authoritative", False) is True:
                non_authoritative_count += 1

        expected_source_count = len(evaluation_case.expected_source_ids)
        expected_chunk_count = len(evaluation_case.expected_chunk_refs)
        return RetrievalEvaluationResult(
            case_id=evaluation_case.case_id,
            result_count=len(normalized_results),
            expected_source_count=expected_source_count,
            matched_expected_source_count=len(matched_expected_sources),
            missing_expected_source_ids=missing_expected_sources,
            forbidden_source_ids_found=forbidden_sources_found,
            expected_source_recall=self._ratio(len(matched_expected_sources), expected_source_count),
            expected_chunk_count=expected_chunk_count,
            matched_expected_chunk_count=len(matched_expected_chunks),
            missing_expected_chunk_refs=missing_expected_chunks,
            trace_complete_count=trace_complete_count,
            trace_incomplete_count=len(normalized_results) - trace_complete_count,
            helper_only_count=helper_only_count,
            non_authoritative_count=non_authoritative_count,
            issues=tuple(issues),
        )

    @classmethod
    def _issues_for_result(cls, result: object) -> tuple[RetrievalEvaluationIssue, ...]:
        issues: list[RetrievalEvaluationIssue] = []
        source_id = cls._safe_value(result, "source_id")
        chunk_ref = cls._safe_value(result, "chunk_ref")
        for field_name in cls.REQUIRED_TRACE_FIELDS:
            if not cls._safe_value(result, field_name):
                issues.append(
                    RetrievalEvaluationIssue(
                        issue_type="missing_trace_field",
                        message=f"Retrieval result missing required trace field: {field_name}",
                        source_id=source_id,
                        chunk_ref=chunk_ref,
                    )
                )
        if getattr(result, "helper_only", False) is not True:
            issues.append(
                RetrievalEvaluationIssue(
                    issue_type="not_helper_only",
                    message="Retrieval result is not marked helper-only",
                    source_id=source_id,
                    chunk_ref=chunk_ref,
                )
            )
        if getattr(result, "non_authoritative", False) is not True:
            issues.append(
                RetrievalEvaluationIssue(
                    issue_type="not_non_authoritative",
                    message="Retrieval result is not marked non-authoritative",
                    source_id=source_id,
                    chunk_ref=chunk_ref,
                )
            )
        return tuple(issues)

    @staticmethod
    def _unwrap_result(result: object) -> object:
        """Support base, standards, and asset result shapes."""

        return getattr(result, "retrieval_result", result)

    @staticmethod
    def _safe_value(result: object, field_name: str) -> str:
        value = getattr(result, field_name, "")
        return str(value).strip() if value is not None else ""

    @staticmethod
    def _ratio(numerator: int, denominator: int) -> float:
        if denominator == 0:
            return 1.0
        return numerator / denominator


def evaluate_retrieval_results(
    evaluation_case: RetrievalEvaluationCase,
    results: Sequence[object],
) -> RetrievalEvaluationResult:
    """Convenience wrapper for evaluating a retrieval result sequence."""

    return RetrievalEvaluationHarness().evaluate(evaluation_case, results)
