"""Models for bounded retrieval.

M30.4 deliberately keeps retrieval deterministic and helper-only.
The records below carry enough metadata for source traceability and
non-authority enforcement without introducing embeddings, vector stores,
or live lookup behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence


APPROVED_SOURCE_STATUSES = frozenset({"approved", "active", "accepted", "validated"})
REJECTED_AUTHORITY_ROLES = frozenset({"mandatory_authority", "compliance_truth", "source_truth"})


@dataclass(frozen=True)
class RetrievalIndexRecord:
    """Traceable source record that may be searched by the retrieval helper."""

    source_id: str
    source_path: str
    source_version: str
    source_status: str
    authority_role: str
    eligibility_decision: str
    chunk_ref: str
    build_id: str
    text: str
    limitation_trace: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)

    def validate_for_retrieval(self) -> None:
        """Fail closed when traceability or authority metadata is incomplete."""

        required_values = {
            "source_id": self.source_id,
            "source_path": self.source_path,
            "source_version": self.source_version,
            "source_status": self.source_status,
            "authority_role": self.authority_role,
            "eligibility_decision": self.eligibility_decision,
            "chunk_ref": self.chunk_ref,
            "build_id": self.build_id,
            "text": self.text,
        }
        missing = [name for name, value in required_values.items() if not str(value).strip()]
        if missing:
            raise ValueError(f"Retrieval record missing required trace fields: {', '.join(missing)}")

        if self.eligibility_decision.lower() != "eligible":
            raise ValueError("Retrieval record is not eligible for retrieval")

        if self.source_status.lower() not in APPROVED_SOURCE_STATUSES:
            raise ValueError("Retrieval record source status is not approved for retrieval")

        if self.authority_role.lower() in REJECTED_AUTHORITY_ROLES:
            raise ValueError("Retrieval record cannot be indexed as authority/truth")


@dataclass(frozen=True)
class RetrievalQuery:
    """Simple deterministic retrieval query."""

    text: str
    limit: int = 10
    metadata_filters: Mapping[str, str] = field(default_factory=dict)

    def normalized_terms(self) -> tuple[str, ...]:
        return tuple(term for term in self.text.lower().split() if term)


@dataclass(frozen=True)
class RetrievalResult:
    """Helper-only retrieval result with source trace and limitation visibility."""

    source_id: str
    source_path: str
    source_version: str
    source_status: str
    authority_role: str
    eligibility_decision: str
    chunk_ref: str
    build_id: str
    snippet: str
    score: int
    helper_only: bool = True
    non_authoritative: bool = True
    limitation_trace: Sequence[str] = field(default_factory=tuple)

    @property
    def authority_statement(self) -> str:
        return "Retrieval result is helper-only and non-authoritative; source registry/source files remain authority."
