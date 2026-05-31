"""Standards-specific controls for bounded retrieval.

M30.5 adds standards source-status filtering, citation fallback, and visible
limitation warnings on top of the M30.4 deterministic in-memory retrieval
skeleton.

This module does not implement embeddings, vector stores, live standards lookup,
clause fabrication, retrieval-backed standards authority, AI/model/provider
behavior, or UI/API behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import RetrievalIndexRecord, RetrievalQuery, RetrievalResult
from .search import InMemoryRetrievalIndex

STANDARD_FAMILY_VALUES = frozenset({"standard", "standards", "regulatory_standard", "standards_registry"})
APPROVED_STANDARD_STATUSES = frozenset({"approved", "active", "accepted", "validated"})
REJECTED_STANDARD_STATUSES = frozenset({"pending", "tbd", "draft", "reference_only", "reference-only"})
DEFAULT_STANDARDS_LIMITATION = (
    "Standards retrieval is helper-only and non-authoritative; verified source registry/citation records remain authority."
)
MISSING_CLAUSE_LIMITATION = "Clause-level citation is unavailable; fallback citation uses source ID, version, and chunk reference."


@dataclass(frozen=True)
class StandardsRetrievalResult:
    """Standards retrieval result with explicit citation and limitation controls."""

    retrieval_result: RetrievalResult
    citation: str
    limitation_warnings: tuple[str, ...]
    helper_only: bool = True
    non_authoritative: bool = True

    @property
    def authority_statement(self) -> str:
        return DEFAULT_STANDARDS_LIMITATION


class StandardsRetrievalControls:
    """Bounded standards retrieval wrapper around the M30.4 in-memory index."""

    def __init__(self, records: Iterable[RetrievalIndexRecord]):
        standards_records = [self._prepare_standard_record(record) for record in records]
        self._index = InMemoryRetrievalIndex(tuple(standards_records))

    @property
    def records(self) -> tuple[RetrievalIndexRecord, ...]:
        return self._index.records

    def search(self, query: RetrievalQuery) -> list[StandardsRetrievalResult]:
        return [self._to_standards_result(result) for result in self._index.search(query)]

    @classmethod
    def _prepare_standard_record(cls, record: RetrievalIndexRecord) -> RetrievalIndexRecord:
        cls._validate_standard_family(record)
        cls._validate_standard_status(record)
        warnings = cls._limitation_warnings_for_record(record)
        limitation_trace = tuple(dict.fromkeys((*record.limitation_trace, *warnings)))
        return RetrievalIndexRecord(
            source_id=record.source_id,
            source_path=record.source_path,
            source_version=record.source_version,
            source_status=record.source_status,
            authority_role=record.authority_role,
            eligibility_decision=record.eligibility_decision,
            chunk_ref=record.chunk_ref,
            build_id=record.build_id,
            text=record.text,
            limitation_trace=limitation_trace,
            metadata=record.metadata,
        )

    @staticmethod
    def _validate_standard_family(record: RetrievalIndexRecord) -> None:
        family = (record.metadata.get("source_family") or record.metadata.get("family") or "").lower()
        if family not in STANDARD_FAMILY_VALUES:
            raise ValueError("Standards retrieval controls only accept standards-family records")

    @staticmethod
    def _validate_standard_status(record: RetrievalIndexRecord) -> None:
        status = record.source_status.lower()
        if status in REJECTED_STANDARD_STATUSES:
            raise ValueError("Standards retrieval record status is blocked from standards retrieval")
        if status not in APPROVED_STANDARD_STATUSES:
            raise ValueError("Standards retrieval record status is not approved for standards retrieval")

    @classmethod
    def _limitation_warnings_for_record(cls, record: RetrievalIndexRecord) -> tuple[str, ...]:
        warnings = [DEFAULT_STANDARDS_LIMITATION]
        if not cls._has_verified_clause_citation(record):
            warnings.append(MISSING_CLAUSE_LIMITATION)
        return tuple(warnings)

    @staticmethod
    def _has_verified_clause_citation(record: RetrievalIndexRecord) -> bool:
        return bool(record.metadata.get("verified_clause_citation") or record.metadata.get("clause_ref"))

    @classmethod
    def _to_standards_result(cls, result: RetrievalResult) -> StandardsRetrievalResult:
        citation = cls._citation_for_result(result)
        warnings = tuple(dict.fromkeys((*result.limitation_trace, DEFAULT_STANDARDS_LIMITATION)))
        return StandardsRetrievalResult(
            retrieval_result=result,
            citation=citation,
            limitation_warnings=warnings,
        )

    @staticmethod
    def _citation_for_result(result: RetrievalResult) -> str:
        return f"{result.source_id} {result.source_version} {result.chunk_ref}"
