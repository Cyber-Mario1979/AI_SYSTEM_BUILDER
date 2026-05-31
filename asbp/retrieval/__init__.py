"""Retrieval boundary package.

This package preserves the earlier M11.4 retrieval architecture boundary helpers
and exposes the M30.4/M30.5/M30.6 bounded retrieval APIs.

Retrieval remains deterministic, helper-only, non-authoritative, and
source-traceable. It does not implement embeddings, vector stores, live lookup,
AI/model/provider behavior, or UI/API behavior.
"""

from .assets import AssetRetrievalControls, AssetRetrievalResult
from .contracts import (
    GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
    GOVERNED_SOURCE_OF_TRUTH_ROLE,
    PROBABILISTIC_SEARCH_RETRIEVAL_MODE,
    PROBABILISTIC_SOURCE_OF_TRUTH_ROLE,
    build_governed_retrieval_request,
    build_probabilistic_search_retrieval_request,
    build_retrieval_architecture_baseline,
    validate_retrieval_request,
)
from .models import RetrievalIndexRecord, RetrievalQuery, RetrievalResult
from .search import InMemoryRetrievalIndex
from .standards import StandardsRetrievalControls, StandardsRetrievalResult

__all__ = [
    "GOVERNED_DETERMINISTIC_RETRIEVAL_MODE",
    "GOVERNED_SOURCE_OF_TRUTH_ROLE",
    "PROBABILISTIC_SEARCH_RETRIEVAL_MODE",
    "PROBABILISTIC_SOURCE_OF_TRUTH_ROLE",
    "build_governed_retrieval_request",
    "build_probabilistic_search_retrieval_request",
    "build_retrieval_architecture_baseline",
    "validate_retrieval_request",
    "AssetRetrievalControls",
    "AssetRetrievalResult",
    "InMemoryRetrievalIndex",
    "RetrievalIndexRecord",
    "RetrievalQuery",
    "RetrievalResult",
    "StandardsRetrievalControls",
    "StandardsRetrievalResult",
]
