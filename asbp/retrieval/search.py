"""Deterministic in-memory retrieval search.

This module intentionally avoids embeddings, vector stores, external services,
AI/model calls, live standards lookup, and source mutation.
"""

from __future__ import annotations

from .models import RetrievalIndexRecord, RetrievalQuery, RetrievalResult


class InMemoryRetrievalIndex:
    """Small helper-only retrieval index with fail-closed validation."""

    def __init__(self, records: list[RetrievalIndexRecord] | tuple[RetrievalIndexRecord, ...]):
        validated: list[RetrievalIndexRecord] = []
        for record in records:
            record.validate_for_retrieval()
            validated.append(record)
        self._records = tuple(validated)

    @property
    def records(self) -> tuple[RetrievalIndexRecord, ...]:
        return self._records

    def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        terms = query.normalized_terms()
        if not terms:
            return []

        scored: list[tuple[int, RetrievalIndexRecord]] = []
        for record in self._records:
            if not self._matches_filters(record, query.metadata_filters):
                continue
            text = record.text.lower()
            score = sum(text.count(term) for term in terms)
            if score > 0:
                scored.append((score, record))

        scored.sort(key=lambda item: (-item[0], item[1].source_id, item[1].chunk_ref))
        return [self._to_result(record, score) for score, record in scored[: query.limit]]

    @staticmethod
    def _matches_filters(record: RetrievalIndexRecord, filters: dict[str, str] | object) -> bool:
        if not filters:
            return True
        for key, expected_value in dict(filters).items():
            if record.metadata.get(key) != expected_value:
                return False
        return True

    @staticmethod
    def _to_result(record: RetrievalIndexRecord, score: int) -> RetrievalResult:
        snippet = record.text[:240]
        return RetrievalResult(
            source_id=record.source_id,
            source_path=record.source_path,
            source_version=record.source_version,
            source_status=record.source_status,
            authority_role=record.authority_role,
            eligibility_decision=record.eligibility_decision,
            chunk_ref=record.chunk_ref,
            build_id=record.build_id,
            snippet=snippet,
            score=score,
            limitation_trace=record.limitation_trace,
        )
