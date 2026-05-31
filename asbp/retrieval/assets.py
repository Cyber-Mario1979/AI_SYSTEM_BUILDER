"""Library/template retrieval controls for bounded retrieval.

M30.6 adds asset-family filtering, asset ID/version requirements, and
deterministic context fetch on top of the M30.4 in-memory retrieval skeleton.

This module does not implement embeddings, vector stores, live lookup,
deterministic resolver replacement, template-selection replacement,
retrieval-backed source authority, AI/model/provider behavior, or UI/API
behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import RetrievalIndexRecord, RetrievalQuery, RetrievalResult
from .search import InMemoryRetrievalIndex

ASSET_FAMILY_VALUES = frozenset({"template", "library"})
REJECTED_ASSET_AUTHORITY_ROLES = frozenset(
    {"deterministic_resolver", "template_selector", "source_library_authority", "stage_commit_authority"}
)
DEFAULT_ASSET_LIMITATION = (
    "Asset retrieval is helper-only and non-authoritative; deterministic resolver, template selection, "
    "and source-library authority remain authoritative."
)


@dataclass(frozen=True)
class AssetRetrievalResult:
    """Asset retrieval result with deterministic asset trace controls."""

    retrieval_result: RetrievalResult
    asset_id: str
    asset_version: str
    asset_family: str
    context_type: str | None
    helper_only: bool = True
    non_authoritative: bool = True

    @property
    def authority_statement(self) -> str:
        return DEFAULT_ASSET_LIMITATION


class AssetRetrievalControls:
    """Bounded library/template retrieval wrapper around the M30.4 index."""

    def __init__(self, records: Iterable[RetrievalIndexRecord]):
        asset_records = [self._prepare_asset_record(record) for record in records]
        self._index = InMemoryRetrievalIndex(tuple(asset_records))

    @property
    def records(self) -> tuple[RetrievalIndexRecord, ...]:
        return self._index.records

    def search(self, query: RetrievalQuery) -> list[AssetRetrievalResult]:
        return [self._to_asset_result(result) for result in self._index.search(query)]

    def fetch_context(self, asset_id: str, asset_version: str, context_type: str | None = None) -> list[AssetRetrievalResult]:
        """Fetch deterministic asset context by asset ID/version and optional context type."""

        filters = {"asset_id": asset_id, "asset_version": asset_version}
        if context_type is not None:
            filters["context_type"] = context_type

        query = RetrievalQuery(text=" ".join(self._terms_for_asset(asset_id, asset_version, context_type)), metadata_filters=filters)
        results = self.search(query)
        return [result for result in results if self._matches_asset(result, asset_id, asset_version, context_type)]

    @classmethod
    def _prepare_asset_record(cls, record: RetrievalIndexRecord) -> RetrievalIndexRecord:
        cls._validate_asset_metadata(record)
        cls._validate_asset_authority_role(record)
        limitation_trace = tuple(dict.fromkeys((*record.limitation_trace, DEFAULT_ASSET_LIMITATION)))
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
    def _validate_asset_metadata(record: RetrievalIndexRecord) -> None:
        family = (record.metadata.get("asset_family") or record.metadata.get("family") or "").lower()
        if family not in ASSET_FAMILY_VALUES:
            raise ValueError("Asset retrieval controls only accept template/library asset records")

        missing = [field for field in ("asset_id", "asset_version") if not record.metadata.get(field)]
        if missing:
            raise ValueError(f"Asset retrieval record missing required asset metadata: {', '.join(missing)}")

    @staticmethod
    def _validate_asset_authority_role(record: RetrievalIndexRecord) -> None:
        if record.authority_role.lower() in REJECTED_ASSET_AUTHORITY_ROLES:
            raise ValueError("Asset retrieval cannot replace deterministic resolver/template/source-library authority")

    @staticmethod
    def _terms_for_asset(asset_id: str, asset_version: str, context_type: str | None) -> tuple[str, ...]:
        terms = [asset_id, asset_version]
        if context_type:
            terms.append(context_type)
        return tuple(terms)

    @staticmethod
    def _matches_asset(
        result: AssetRetrievalResult,
        asset_id: str,
        asset_version: str,
        context_type: str | None,
    ) -> bool:
        if result.asset_id != asset_id or result.asset_version != asset_version:
            return False
        if context_type is not None and result.context_type != context_type:
            return False
        return True

    @staticmethod
    def _to_asset_result(result: RetrievalResult) -> AssetRetrievalResult:
        # RetrievalResult intentionally exposes trace metadata, not arbitrary metadata.
        # Asset fields are reconstructed from the source trace contract encoded in chunk_ref.
        # The canonical format is: asset_family:asset_id:asset_version[:context_type]:chunk
        parts = result.chunk_ref.split(":")
        if len(parts) < 4:
            raise ValueError("Asset retrieval result chunk_ref lacks asset trace fields")
        asset_family, asset_id, asset_version = parts[0], parts[1], parts[2]
        context_type = parts[3] if len(parts) > 4 else None
        return AssetRetrievalResult(
            retrieval_result=result,
            asset_id=asset_id,
            asset_version=asset_version,
            asset_family=asset_family,
            context_type=context_type,
        )
