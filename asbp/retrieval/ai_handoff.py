"""Deterministic retrieval-to-AI handoff contract helpers.

M30.8 transforms already-evaluated retrieval outputs into bounded context
packets for future AI use. It does not call models, execute prompts, integrate
with providers, or treat retrieval as truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .evaluation import RetrievalEvaluationIssue, RetrievalEvaluationResult

HANDOFF_LIMITATION = (
    "Retrieval context packet is helper-only and non-authoritative; source files, registries, "
    "and approved deterministic controls remain authoritative."
)
RAW_TRUTH_REFUSAL = "Raw retrieval cannot be passed as truth or mandatory authority."


@dataclass(frozen=True)
class AIHandoffRefusal:
    """Reason a retrieval result set cannot be handed off for future AI use."""

    refusal_type: str
    message: str
    source_id: str | None = None
    chunk_ref: str | None = None


@dataclass(frozen=True)
class AIHandoffContextItem:
    """One source-traceable context item inside a future-AI context packet."""

    source_id: str
    source_path: str
    source_version: str
    chunk_ref: str
    citation: str
    snippet: str
    limitations: tuple[str, ...]
    helper_only: bool = True
    non_authoritative: bool = True


@dataclass(frozen=True)
class AIHandoffContextPacket:
    """Bounded, citation-bearing, limitation-visible packet for future AI use."""

    packet_id: str
    purpose: str
    query_text: str
    context_items: tuple[AIHandoffContextItem, ...]
    evaluation_case_id: str
    evaluation_passed: bool
    handoff_limitations: tuple[str, ...] = field(default_factory=lambda: (HANDOFF_LIMITATION,))
    helper_only: bool = True
    non_authoritative: bool = True
    ai_runtime_executed: bool = False
    model_provider: str | None = None


@dataclass(frozen=True)
class AIHandoffBuildResult:
    """Result of attempting to build a bounded AI handoff packet."""

    packet: AIHandoffContextPacket | None
    refusals: tuple[AIHandoffRefusal, ...]

    @property
    def allowed(self) -> bool:
        return self.packet is not None and not self.refusals


class AIHandoffContract:
    """Build future-AI context packets from evaluated retrieval outputs only."""

    def build_packet(
        self,
        *,
        packet_id: str,
        purpose: str,
        evaluation_result: RetrievalEvaluationResult | None,
        retrieval_results: Iterable[object],
        assert_retrieval_as_truth: bool = False,
        require_result_limitations: bool = True,
    ) -> AIHandoffBuildResult:
        refusals = self._base_refusals(evaluation_result, assert_retrieval_as_truth)
        context_items: list[AIHandoffContextItem] = []

        for retrieval_result in retrieval_results:
            context_item, item_refusals = self._context_item_from_result(
                retrieval_result,
                require_result_limitations=require_result_limitations,
            )
            refusals.extend(item_refusals)
            if context_item is not None:
                context_items.append(context_item)

        if refusals or evaluation_result is None:
            return AIHandoffBuildResult(packet=None, refusals=tuple(refusals))

        packet = AIHandoffContextPacket(
            packet_id=packet_id,
            purpose=purpose,
            query_text=evaluation_result.case_id,
            context_items=tuple(context_items),
            evaluation_case_id=evaluation_result.case_id,
            evaluation_passed=evaluation_result.passed,
        )
        return AIHandoffBuildResult(packet=packet, refusals=())

    @classmethod
    def _base_refusals(
        cls,
        evaluation_result: RetrievalEvaluationResult | None,
        assert_retrieval_as_truth: bool,
    ) -> list[AIHandoffRefusal]:
        refusals: list[AIHandoffRefusal] = []
        if evaluation_result is None:
            refusals.append(
                AIHandoffRefusal(
                    refusal_type="missing_evaluation",
                    message="Retrieval evaluation evidence is required before AI handoff packet creation.",
                )
            )
        elif not evaluation_result.passed:
            refusals.extend(cls._refusals_from_evaluation_issues(evaluation_result.issues))

        if assert_retrieval_as_truth:
            refusals.append(
                AIHandoffRefusal(
                    refusal_type="raw_retrieval_truth_attempt",
                    message=RAW_TRUTH_REFUSAL,
                )
            )
        return refusals

    @staticmethod
    def _refusals_from_evaluation_issues(issues: tuple[RetrievalEvaluationIssue, ...]) -> list[AIHandoffRefusal]:
        refusals: list[AIHandoffRefusal] = []
        for issue in issues:
            refusal_type = {
                "forbidden_source_returned": "forbidden_source",
                "missing_trace_field": "missing_source_trace",
                "not_helper_only": "not_helper_only",
                "not_non_authoritative": "not_non_authoritative",
            }.get(issue.issue_type, "failed_evaluation")
            refusals.append(
                AIHandoffRefusal(
                    refusal_type=refusal_type,
                    message=issue.message,
                    source_id=issue.source_id,
                    chunk_ref=issue.chunk_ref,
                )
            )
        return refusals

    @classmethod
    def _context_item_from_result(
        cls,
        retrieval_result: object,
        *,
        require_result_limitations: bool,
    ) -> tuple[AIHandoffContextItem | None, list[AIHandoffRefusal]]:
        wrapper = retrieval_result
        base = cls._unwrap_result(retrieval_result)
        refusals: list[AIHandoffRefusal] = []

        source_id = cls._safe_value(base, "source_id")
        source_path = cls._safe_value(base, "source_path")
        source_version = cls._safe_value(base, "source_version")
        chunk_ref = cls._safe_value(base, "chunk_ref")
        snippet = cls._safe_value(base, "snippet")

        for field_name, value in {
            "source_id": source_id,
            "source_path": source_path,
            "source_version": source_version,
            "chunk_ref": chunk_ref,
        }.items():
            if not value:
                refusals.append(
                    AIHandoffRefusal(
                        refusal_type="missing_source_trace",
                        message=f"Cannot create AI handoff context item without {field_name}.",
                        source_id=source_id or None,
                        chunk_ref=chunk_ref or None,
                    )
                )

        if getattr(base, "helper_only", False) is not True or getattr(wrapper, "helper_only", True) is not True:
            refusals.append(
                AIHandoffRefusal(
                    refusal_type="not_helper_only",
                    message="AI handoff requires helper-only retrieval context.",
                    source_id=source_id or None,
                    chunk_ref=chunk_ref or None,
                )
            )

        if getattr(base, "non_authoritative", False) is not True or getattr(wrapper, "non_authoritative", True) is not True:
            refusals.append(
                AIHandoffRefusal(
                    refusal_type="not_non_authoritative",
                    message="AI handoff requires non-authoritative retrieval context.",
                    source_id=source_id or None,
                    chunk_ref=chunk_ref or None,
                )
            )

        result_limitations = cls._limitations_for_result(wrapper, base)
        if require_result_limitations and not result_limitations:
            refusals.append(
                AIHandoffRefusal(
                    refusal_type="missing_limitations",
                    message="AI handoff requires visible retrieval limitations for every context item.",
                    source_id=source_id or None,
                    chunk_ref=chunk_ref or None,
                )
            )

        if refusals:
            return None, refusals

        return (
            AIHandoffContextItem(
                source_id=source_id,
                source_path=source_path,
                source_version=source_version,
                chunk_ref=chunk_ref,
                citation=cls._citation_for_result(wrapper, base),
                snippet=snippet,
                limitations=tuple(dict.fromkeys((*result_limitations, HANDOFF_LIMITATION))),
            ),
            [],
        )

    @staticmethod
    def _unwrap_result(retrieval_result: object) -> object:
        return getattr(retrieval_result, "retrieval_result", retrieval_result)

    @staticmethod
    def _safe_value(result: object, field_name: str) -> str:
        value = getattr(result, field_name, "")
        return str(value).strip() if value is not None else ""

    @classmethod
    def _citation_for_result(cls, wrapper: object, base: object) -> str:
        explicit_citation = cls._safe_value(wrapper, "citation")
        if explicit_citation:
            return explicit_citation
        return f"{cls._safe_value(base, 'source_id')} {cls._safe_value(base, 'source_version')} {cls._safe_value(base, 'chunk_ref')}"

    @classmethod
    def _limitations_for_result(cls, wrapper: object, base: object) -> tuple[str, ...]:
        limitations: list[str] = []
        limitations.extend(cls._string_sequence(getattr(wrapper, "limitation_warnings", ())))
        limitations.extend(cls._string_sequence(getattr(base, "limitation_trace", ())))
        return tuple(dict.fromkeys(limitations))

    @staticmethod
    def _string_sequence(values: object) -> tuple[str, ...]:
        if values is None or isinstance(values, str):
            return (values,) if isinstance(values, str) and values.strip() else ()
        return tuple(str(value).strip() for value in values if str(value).strip())


def build_ai_handoff_packet(
    *,
    packet_id: str,
    purpose: str,
    evaluation_result: RetrievalEvaluationResult | None,
    retrieval_results: Iterable[object],
    assert_retrieval_as_truth: bool = False,
    require_result_limitations: bool = True,
) -> AIHandoffBuildResult:
    """Convenience wrapper for bounded AI handoff packet creation."""

    return AIHandoffContract().build_packet(
        packet_id=packet_id,
        purpose=purpose,
        evaluation_result=evaluation_result,
        retrieval_results=retrieval_results,
        assert_retrieval_as_truth=assert_retrieval_as_truth,
        require_result_limitations=require_result_limitations,
    )
